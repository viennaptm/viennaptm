import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
       name="viennaptm",
       version="0.0.1",
       description="Python package to apply post-translational modifications to protein structures.",
       long_description=long_description,
       long_description_content_type="text/markdown",
       url="https://vienna-ptm.univie.ac.at",
       author="Sophie Margreitter, Drazen Petrov, Christian Margreitter and Bojan Zagrovic",
       author_email="christian.margreitter@gmail.com",
       entry_points={
           "console_scripts": [
               "viennaptm = viennaptm.entrypoints.viennaptm:main"
                ]
       },
       packages=setuptools.find_packages(),
       install_requires = [
           "pip>=25",
           "setuptools>=60",
           "pydantic>=2",
           "pandas",
           "biopython>=1.8",
           "scipy"
       ],
       classifiers=[
           "Programming Language :: Python :: 3",
           "Operating System :: OS Independent"
    ]
)
