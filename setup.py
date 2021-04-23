from distutils.core import setup

version = "0.1"
install_requires = []
with open("requirements.txt") as requirements_file:
    install_requires.extend(requirements_file.readlines())

setup(
    name="bundestag-drucksache",
    packages=["bundestag_drucksache"],
    version=version,
    license="gpl-3.0",
    description="Download and find official Drucksache objects from the bundestag. Search yourself there: https://pdok.bundestag.de",
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
    ]
)