from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    """
    This function will return list of external library requirement.
    """
    with open("requirements.txt") as requirement_file:
        return requirement_file.readlines().remove("-e .")


setup(
    name = "sensor",
    version = "0.0.5",
    author = "Liji Alex",
    author_email = "liji.alex@gmail.com",
    packages = find_packages(),   # project src packages
    install_requires = get_requirements()
)