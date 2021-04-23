class Config:
    def __init__(
        self, pdok="https://pdok.bundestag.de", dserver="https://dserver.bundestag.de"
    ):
        if pdok.endswith("/"):
            pdok = pdok[-1]
        if dserver.endswith("/"):
            dserver = dserver[-1]
        self.pdok = pdok
        self.pdok_uri = pdok + "/treffer.php"
        self.dserver = dserver
        self.dserver_pdf = (
            dserver
            + "/btd/{legislaturperiode}/{first_3_digits_of_number}/{legislaturperiode}{number}.pdf"
        )


def parse_config(**kwargs):
    kwargs = {key: value for key, value in kwargs.items() if key in ["pdok", "dserver"]}
    return Config(**kwargs)


def get_config_object(**kwargs):
    if "config" in kwargs:
        return kwargs["config"]
    elif kwargs:
        return parse_config(**kwargs)
    else:
        return Config()
