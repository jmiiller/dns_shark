import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="dns_shark",
    version="1.0.0",
    description="A simple DNS resolver that can resolve a domain name to either an IPv4 or IPv6 address.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jmiiller/dns_shark",
    author="Jeffrey Miiller",
    author_email="jeffrey.miiller@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["dns_shark"],
    include_package_data=True,
    install_requires=[],
    entry_points={},
)