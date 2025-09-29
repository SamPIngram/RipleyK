import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ripleyk",
    version="0.9",
    author="Sam Ingram",
    author_email="sp_ingram12@yahoo.co.uk",
    description=("Calculation of the Ripley K (spatial statistics) value in python"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SamPIngram/RipleyK",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy>=1.19.2",
        "scipy>=1.5.2",
    ],
    python_requires=">=3.5",
)
