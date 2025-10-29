"""Setup configuration for My Own Git."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="xgit",
    version="0.1.0",
    author="Jorge Gomez",
    description="A basic Python implementation of Git core features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jorgeadev/my-own-git",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "xgit=xgit.cli:main",
        ],
    },
)
