# bundestag-drucksache
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

Download and find official Drucksache objects from the bundestag. Search yourself there: https://pdok.bundestag.de

# Installation

```shell
pip install bundestag-drucksache
```

# How to use?

## Drucksache
```python
from bundestag_drucksache import Drucksache

# Get object

d = Drucksache(19, 28444)
d = Drucksache.get("19/28444") # get the object by the identification
d = Drucksache.parse_from_link("https://dip21.bundestag.de/dip21/btd/19/284/1928444.pdf") # parse object by the link

# Do things with the object

if d.exists(): # checks if the Drucksache pdf exists
    pdf_link = d.pdf_link # get the link to the pdf file
    identification = d.identification # get identification id like 19/28444
    
    # Download PDF
    d.download_pdf("drucksache.pdf")
    # or 
    file = open("drucksache.pdf", "wb")
    d.download_pdf(file, close_file=False)
```

## Search

```python
from bundestag_drucksache import search_drucksache, Drucksache

page = 1
drucksache: list[Drucksache] = search_drucksache(
    search="Stadtentwicklung",
    legislaturperiode=19,
    offset=(page - 1) * 10 # the request would be answered with 10 items, so you need 10 as offset for page 2.
                           # the default value for offset is 0 (starting offset).
)
# You can set start_date or end_date but note that time ranges are very unsafe.
# Read following Warning:
"""
[WARNING] for start_date and end_date: The datetime filtering is extremely unsafe,
        because the server doesn't have any method for datetime filtering,
        the response data would be filtered by the client. But you get only the first 10 elements,
        so time filtering is not possible.
"""
```

# Config (not important)

You can pass config values for `search_drucksache` and `Drucksache` (`__init__`, `get`, `parse_from_link`).
You can pass all values eachself or create a `bundestag_drucksache.config.Config` object and pass the object
as the `config` kwarg.

The keys and default values are:
```json
{
  "pdok": "https://pdok.bundestag.de",
  "dserver": "https://dserver.bundestag.de"
}
```
## Contributors ???

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://adridoesthings.com"><img src="https://avatars.githubusercontent.com/u/45321107?v=4?s=100" width="100px;" alt=""/><br /><sub><b>AdriDevelopsThings</b></sub></a><br /><a href="https://github.com/AdriDevelopsThings/bundestag-drucksache/commits?author=AdriDevelopsThings" title="Code">????</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!