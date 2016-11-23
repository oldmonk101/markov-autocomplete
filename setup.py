from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()


def setup_package():

    build_requires = []
    try:
        import numpy
        import nltk
    except:
        build_requires = ['numpy>=1.6.2', 'nltk>=3.2.1']

    metadata = dict(
        name='markov-autocomplete',
        packages=['markov-autocomplete'],
        # Versions should comply with PEP440.  For a discussion on single-sourcing
        # the version across setup.py and the project code, see
        # https://packaging.python.org/en/latest/single_source_version.html
        version='1.0.0',
        description='Autocomplete model easy to integrate with Flask apps',
        long_description=long_description,

        # The project's main homepage.
        url='https://github.com/YourMD/markov-autocomplete',

        download_url='https://github.com/YourMD/markov-autocomplete/tarball/autocomplete',

        # Author details
        author='Matteo Tomassetti (Data Scientist at Your.MD)',
        author_email='matteo.tomassetti@your.md',

        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 4 - Beta',

            # Indicate who your project is intended for
            'Intended Audience :: Information Technology',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Education',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',

            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: MIT License',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 3.4',
        ],

        # What does your project relate to?
        keywords='autocomplete hidden-markov model nlp natural language processing',

        # You can just specify the packages manually here if your project is
        # simple. Or you can use find_packages().

        # List run-time dependencies here.  These will be installed by pip when your
        # project is installed. For an analysis of "install_requires" vs pip's
        # requirements files see:
        # https://packaging.python.org/en/latest/requirements.html
        # See also https://github.com/scipy/scipy/blob/master/setup.py (malemi)
        setup_requires=build_requires,
        tests_require=build_requires,
        install_requires=build_requires,

        # If there are data files included in your packages that need to be
        # installed, specify them here.  If using Python 2.6 or less, then these
        # have to be included in MANIFEST.in as well.
        package_data={
            'markov-autocomplete': ['*.py']
        },

        # To provide executable scripts, use entry points in preference to the
        # "scripts" keyword. Entry points provide cross-platform support and allow
        # pip to create the appropriate form of executable for the target platform.
        entry_points={
            'console_scripts': [
                'sample=sample:main',
            ],
        },
    )

    setup(**metadata)

if __name__ == '__main__':
    setup_package()
