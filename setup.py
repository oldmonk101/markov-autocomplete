from setuptools import setup
long_description = open('README.rst').read()

def setup_package():

    build_requires = []
    try:
        import numpy
        import nltk
    except:
        build_requires = ['numpy>=1.6.2', 'nltk>=3.2.1']

    metadata = dict(
        name='markov_autocomplete',
        packages=['markov_autocomplete'],
        install_requires=build_requires,
        long_description=long_description,
        # Versions should comply with PEP440.  For a discussion on single-sourcing
        # the version across setup.py and the project code, see
        # https://packaging.python.org/en/latest/single_source_version.html
        version='1.0.1',
        description='Autocomplete model easy to integrate with Flask apps',

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


    )

    setup(**metadata)

if __name__ == '__main__':
    setup_package()
