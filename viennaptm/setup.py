import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="viennaptm",  
    version='0.1',
    scripts=["viennaptm"] ,
    author="Christian Margreitter",
    author_email="christian.margreitter@gmail.com",
    description="A python package to add post-translational modifications to protein structures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )
