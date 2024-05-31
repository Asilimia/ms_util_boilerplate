from setuptools import setup, find_packages

setup(
    name="ms_util_boilerplate",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "uvicorn>=0.29.0",
        "python_jose>=3.3.0",
        "cryptography>=42.0.5",
        "pytest>=8.1.1",
        "setuptools",
        "fastapi==0.110.1",
    ],
    python_requires='>=3.8, <3.12',  # Python 3.6 up to but not including Python 4
)
