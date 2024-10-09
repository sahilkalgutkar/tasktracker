from setuptools import setup, find_packages

setup(
    name="tasktracker",
    version="0.1",
    description="A simple task tracking CLI application",
    author="Sahil Kalgutkar",
    author_email="your.email@example.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "tasktracker = tasktracker.cli:main",
        ],
    },
)
