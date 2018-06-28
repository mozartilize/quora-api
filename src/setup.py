from setuptools import setup

packages = ["utils",
            # modules
            "accounts", "questions",
            # app
            "quora"]

setup(
    name="quora",
    version="0.1.0",
    author="mozartilize",
    author_email="mozartilize@gmail.com",
    description="Quora-liked API",
    url="https://github.com/mozartilize/quora-api",
    zip_safe=False,
    packages=packages,
    include_package_data=True,
    install_requires=[
        'flask>=1.0,<2',
        'sqlalchemy>=1.2,<2',
        'psycopg2-binary>=2.7,<3',
        'flask-restful>=0.3.6,<1',
        'flask-migrate>=2.1,<3',
        'pyjwt>=1.6,<2',
        'passlib>=1.7,<2',
        'flask-sqlalchemy>=2.3,<3',
        'flask-httpauth>=3.2,<4',
        'marshmallow>=3.0.0b11,<3.1',
        'flask-mail>=0.9.1,<1',
    ],
    extras_require={
        'passlib': ['bcrypt'],
        'dotenv': ['python-dotenv'],
        'dev': [
            'pytest',
            'watchdog',
            'flask-shell-ipython',
            'pylint'
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
