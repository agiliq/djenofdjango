A Django book for people with intermediate level Django skills.

Inspired by James Bennett's Practical Django projects.

Generating documentation requires [Sphinx](http://pypi.python.org/pypi/Sphinx)

To create HTML documentation, run:

    cd src
    make html

To create a PDF version of the book on Ubuntu Linux:

    sudo apt-get install git texlive-full python-sphinx
    cd djenofdjango/src
    make latex latex_paper_size=letter
    cd build/latex
    make all-pdf

The generated file is located at `djenofdjango/src/build/latex/djenofdjango.pdf`
