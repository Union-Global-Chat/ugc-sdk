from setuptools import setup, find_packages


with open("requirements.txt", "r") as f:
    requirements = f.readlines()

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="ugc-sdk",
    version="0.1.0",
    description="Ugc client",
    long_description=long_description,
    author="tuna2134",
    author_email="masato.04.11.2007@gmail.com",
    url="https://github.com",
    license="MIT",
    packages=find_packages(),
    requires=requirements
)