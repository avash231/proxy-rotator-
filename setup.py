from setuptools import setup, find_packages
import os

# Try to read README.md, but don't fail if it doesn't exist
long_description = "A simple proxy rotator to change IP addresses using free proxies"
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

setup(
    name="proxy-rotator",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple proxy rotator to change IP addresses using free proxies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/proxy-rotator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "proxy-rotator=proxy_rotator.main:main",
        ],
    },
)