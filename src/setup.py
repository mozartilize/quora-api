from setuptools import setup

packages = ["libs.password", "utils",
            # modules
            "accounts", "questions",
            "migrations",
            # app
            "quora"]

setup(
    name="quora",
    version="0.1.0",
    author="mozartilize",
    author_email="mozartilize@gmail.com",
    description="Quora-liked API",
    url="https://github.com/mozartilize/quora-api",
    packages=packages,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
