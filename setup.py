from setuptools import setup, find_packages

setup(
    name="ms_util_boilerplate",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "pydantic",
        "pytest"
    ],
)