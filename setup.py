import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="neterraproxy",
    version="0.0.1",
    author="Anton Nanchev",
    author_email="ananchev@gmail.com",
    description="A python version of the neterra proxy java app written by @sgloutnikov",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ananchev/neterraproxy",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)