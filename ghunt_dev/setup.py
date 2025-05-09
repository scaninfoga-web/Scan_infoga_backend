from setuptools import setup, find_packages

setup(
    name="ghunt",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "httpx",
        "beautifulsoup4",
        "rich",
        "autoslot",
        "python-dateutil"
    ],
    entry_points={
        "console_scripts": [
            "ghunt=ghunt.ghunt:main",
        ],
    },
)