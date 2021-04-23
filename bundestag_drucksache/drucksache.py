from typing import Union, IO

import requests

from bundestag_drucksache.config import get_config_object


class Drucksache:
    @staticmethod
    def get(identification):
        """
        Get a Drucksache object by the identification.
        :param identification: Note following syntax: '{legislaturperiode}/{ongoing_number}'. The parliament structure
            uses this identification.
        :return: A Drucksache object.
        """
        if type(identification) == str and "/" in identification:
            identification = identification.split("/")
            if len(identification) == 2:
                return Drucksache(int(identification[0]), int(identification[1]))

        raise TypeError(
            "'identification' argument should have the following string syntax: '{legislaturperiode}/{"
            "ongoing_number}'. "
        )

    @staticmethod
    def parse_from_link(link: str):
        """
        Parse the Drucksache object by a link to the Drucksache pdf file.
        :param link: The link to the pdf file of the Drucksache. Note that you have to leave
            the filename with the suffix unchanged.
        :return: A Drucksache object.
        """
        if "/" in link:
            link = link.split("/")
            pdf = link[-1]
            if ".pdf" in pdf:
                try:
                    full_number = pdf.replace(".pdf", "")
                    if len(full_number) >= 5:
                        full_number = full_number[:-5] + "/" + full_number[-5:]
                        return Drucksache.get(full_number)
                except TypeError:
                    pass

    def __init__(self, legislaturperiode: int, number: int, **config_kwargs):
        """
        :param legislaturperiode: The number of the legislaturperiode of the Drucksache.
        :param number: The ongoing Drucksache number. (If you have the XX/XXXXX number use the static get method.)
        :param config_kwargs: Config kwargs of bundestag_drucksache.config.Config
            or the kwargs 'config' with the config itself.
        """
        self.legislaturperiode = legislaturperiode
        self.number = number
        self._config = get_config_object(**config_kwargs)
        self._pdf_link = None

    @property
    def identification(self) -> str:
        """
        Get the identification of the Drucksache. The identification would be used by the parliament.
        :return: The identification with the following syntax: '{legislaturperiode}/{ongoing_number}'.
        """
        return f"{self.legislaturperiode}/{str(self.number).zfill(5)}"

    @property
    def pdf_link(self) -> str:
        """
        Generate a link to the pdf file
        :return:
        """
        if not self._pdf_link:
            self._pdf_link = (
                self._config.dserver_pdf.replace(
                    "{legislaturperiode}", str(self.legislaturperiode)
                )
                .replace("{number}", str(self.number).zfill(5))
                .replace("{first_3_digits_of_number}", str(self.number).zfill(5)[:3])
            )
        return self._pdf_link

    def exists(self) -> bool:
        """
        Check if the Drucksache (PDF-File) exists.
        :return: true or false
        """
        response = requests.head(self.pdf_link, allow_redirects=False)
        if response.status_code == 200:
            return True
        elif response.status_code == 302:
            return False
        response.raise_for_status()
        return False

    def download_pdf(self, file: Union[str, IO[bytes]], close_file=True):
        """
        Download the Drucksache pdf to a file.
        :param file: The opened file (use a binary open mode like 'wb') or the filename.
        :param close_file: Should the file be closed after writing?
        :return: The opened/closed file. (You don't have to save it)
        """
        if type(file) == str:
            file = open(file, "wb")
        if hasattr(file, "writeable") and not file.writeable():
            raise TypeError(
                f"'file' argument for download_pdf function should be writeable. Open the file with a writeable "
                f"binary mode like 'wb'. "
            )
        block_size = 1024
        current_loaded_data = 0
        response = requests.get(self.pdf_link, stream=True)
        response.raise_for_status()
        for data in response.iter_content(block_size):
            current_loaded_data += len(data)
            file.write(data)
        if current_loaded_data != int(response.headers["Content-Length"]):
            raise RuntimeError(
                f"The request to {self.pdf_link} failed, because Content-Length is {response.headers['Content-Length']} and real length is {current_loaded_data}."
            )
        del response
        if close_file:
            file.close()
        return file

    def __repr__(self):
        return f"<{self.__class__.__name__} identification={self.identification} >"
