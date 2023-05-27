from setuptools import find_packages
from setuptools import setup

if __name__ == "__main__":
    setup(
        name="lyrics_analysis",
        packages=find_packages(exclude=["tests", "data"]),
        # install_requires=[
        #     "polars",
        # ],
    )
