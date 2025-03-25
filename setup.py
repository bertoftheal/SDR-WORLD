from setuptools import setup, find_packages

setup(
    name="sdr_assistant",
    version="1.0.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "flask-cors",
    ],
)
