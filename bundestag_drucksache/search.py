from datetime import date, datetime, timedelta
from typing import List, Union

import requests
from datetimerange import DateTimeRange

from bundestag_drucksache.config import get_config_object
from bundestag_drucksache.drucksache import Drucksache
from bs4 import BeautifulSoup


def _get_drucksache_search_params(
    search: str = None, legislaturperiode: int = None, offset: int = None
) -> dict:
    params = {}
    if not (search or legislaturperiode):
        raise ValueError(f"You must set 'search' and/or 'legislaturperiode'.")
    if search:
        params = {"q": search, "dart": "Drucksache"}
        if legislaturperiode and legislaturperiode > 0:
            params["wp"] = str(legislaturperiode)
    else:
        if legislaturperiode:
            params = {"q": f"{legislaturperiode}/*"}
    if offset and offset > 0:
        params["offset"] = str(offset)
    return params


def _datetime_range_tester(start_date: Union[date, datetime] = None, end_date: Union[date, datetime] = None):
    if start_date and type(start_date) == datetime:
        start_date = start_date.date()
    if end_date and type(end_date) == datetime:
        end_date = end_date.date()

    datetime_range = DateTimeRange(start_date, end_date)

    def test(d: date):
        if start_date and end_date:
            return d in datetime_range.range(timedelta(days=1))
        elif start_date:
            return d >= start_date
        elif end_date:
            return d <= end_date
        else:
            return True

    return test


def search_drucksache(
    search: str = None,
    legislaturperiode: int = None,
    offset: int = None,
    start_date: date = None,
    end_date: date = None,
    **config_kwargs,
) -> List[Drucksache]:
    """
    :param search: A search string, the documents would be filtered by this string.
    :param legislaturperiode: The number of the legislaturperiode.
    :param offset: The starting value (default=0), you will get 10 items per
    request. If you want to see items on page 3, you have to calculate (page - 1) * 10 -> offset=20.

    [WARNING] for start_date and end_date: The datetime filtering is extremely unsafe,
        because the server doesn't have any method for datetime filtering,
        the response data would be filtered by the client. But you get only the first 10 elements,
        so time filtering is not possible.
    :param start_date: Read warning above!
    :param end_date: Read warning above!

    :param config_kwargs: Config kwargs of bundestag_drucksache.config.Config
        or the kwargs 'config' with the config itself.

    :return: A list of Drucksache objects.
    """
    config = get_config_object(**config_kwargs)
    params = _get_drucksache_search_params(
        search=search, legislaturperiode=legislaturperiode, offset=offset
    )
    datetime_range = _datetime_range_tester(start_date=start_date, end_date=end_date)
    response = requests.get(config.pdok_uri, params=params)
    response.raise_for_status()
    if "keine passenden dokumente gefunden" in response.text.lower():
        return []
    soup = BeautifulSoup(response.text, features="html.parser")
    tbody = (
        soup.find("div", attrs={"class": "suchErgebnis"}).find("table").find("tbody")
    )
    drucksachen = []
    for tr in tbody.find_all("tr"):
        td = tr.find("td")
        content = td.find_all("strong")
        num = content[0].text
        d = datetime.strptime(content[1].text, "%d.%m.%Y").date()
        if datetime_range(d):
            try:
                drucksachen.append(Drucksache.get(num))
            except Exception as e:
                try:
                    drucksachen.append(
                        Drucksache.parse_from_link(
                            td.find("div", attr={"class": "resultTitle"})
                            .find("div", attr={"class": "linkGeneric"})
                            .find("a")["href"]
                        )
                    )
                except Exception:
                    raise e
    return drucksachen
