from setuptools import setup, find_namespace_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="MultiSC",  # How you named your package folder
    packages=find_namespace_packages(),  # Chose the same as "name"
    version="v0.0.7",  # Start with a small number and increase it with every change you make
    license="MIT",  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="Server and client for your app needs",  # Give a short description about your library
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yehoyada.s",  # Type in your name
    author_email="hvuhsg6@gmail.com",  # Type in your E-Mail
    url="https://github.com/hvuhsg/MultiSC",  # Provide either the link to your github or to your website
    download_url="https://github.com/hvuhsg/MultiSC/archive/v0.0.7.tar.gz",  # I explain this later on
    keywords=[
        "Server",
        "Client",
        "Easy",
        "app",
        "client",
        "server",
    ],  # Keywords that define your package best
    install_requires=["cryptography", "rsa", "pymongo"],  # I get to this in a second
    entry_points={
        'console_scripts': [
            'get_config = MultiSC.get_config:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",  # Again, pick a license
        "Programming Language :: Python :: 3",  # Specify which pyhton versions that you want to support
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
