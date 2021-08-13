import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="perseus-Drakomire",
    version="0.0.1",
    author="Drakomire",
    author_email="author@example.com",
    description="Azur Lane Python API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Drakomire/perseus.py",
    project_urls={
        "Bug Tracker": "https://github.com/Drakomire/perseus.py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
