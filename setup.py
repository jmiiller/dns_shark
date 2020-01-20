import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="dns_shark",
    version="1.0.2",
    description="A simple DNS resolver that can resolve a domain name to either an IPv4 or IPv6 address.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jmiiller/dns_shark",
    author="Jeffrey Miiller",
    author_email="jeffrey.miiller@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Topic :: Internet :: Name Service (DNS)",
        "Topic :: Software Development :: Version Control :: Git",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["dns_shark"],
    include_package_data=True,
    install_requires=[],
    entry_points={"console_scripts": [
            "dns_shark=dns_shark.__main__:main",
        ]},
)