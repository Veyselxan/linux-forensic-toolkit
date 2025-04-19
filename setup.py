from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="linux-forensic-toolkit",
    version="1.0.1",
    author="veyselxan",
    author_email="info@veyse-xan.com",
    description="Linux Forensic Analysis Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Veyselxan/linux-forensic-toolkit",
    packages=find_packages(),
    install_requires=[
        "psutil>=5.8.0",
        "prettytable>=3.0.0"
    ],
    entry_points={
        "console_scripts": [
            "lft = lft.main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
)
