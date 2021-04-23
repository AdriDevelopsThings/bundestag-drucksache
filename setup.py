from os import path
from setuptools import setup

version = "0.1.4"
this_directory = path.abspath(path.dirname(__file__))

install_requires = []
with open(path.join(this_directory, "requirements.txt")) as requirements_file:
    install_requires.extend(requirements_file.readlines())
long_description = ""
with open(path.join(this_directory, "README.md"), encoding="utf-8") as readme_file:
    long_description += readme_file.read()
setup(
    name="bundestag-drucksache",
    packages=["bundestag_drucksache"],
    version=version,
    license="gpl-3.0",
    description="Download and find official Drucksache objects from the bundestag. Search yourself there: "
                "https://pdok.bundestag.de",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="adridoesthings",
    author_email="github@adridoesthings.com",
    url="https://github.com/AdriDevelopsThings/bundestag-drucksache",
    download_url=f"https://github.com/AdriDevelopsThings/bundestag-drucksache/archive/refs/tags/{version}.tar.gz",
    keywords=["bundestag", "drucksache", "germany", "politic", "parliament"],
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
