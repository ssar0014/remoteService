# the setup.py file is used to build the package
# contain information about your package, specifically the name of the package,
# its version, platform-dependencies and a whole lot more.
from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Remote Service Package'

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()


# Setting up
setup(
       # the name must match the folder name 'remoteService'
        name="remoteService",
        version=VERSION,
        author="Subhasish Sarkar",
        author_email="subhasish.sarkar@gada.io",
        url='https://github.com/ssar0014/remoteService',
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        packages=find_packages(),
        python_requires='>=3',
        install_requires=['numpy',\
                          'pandas',\
                          'matplotlib',\
                          'sklearn',\
                          'flask',\
                          'Flask-SQLAlchemy',\
                          'Flask-Marshmallow',\
                          'Marshmallow-SQLAlchemy',\
                          'mpld3',\
                          'wordcloud'], # add any additional packages that
        # extra things that are only needed during development or testing
        extras_require={
            "dev": [
                "pytest>=3.7",
            ],
        },
        # needs to be installed along with your package.
        keywords=['python', 'remote service'],
        classifiers= [
             "Development Status :: 3 - Alpha",
             'Intended Audience :: Developers',
             'Topic :: Software Development :: Build Tools',
             'License :: OSI Approved :: MIT License',
             'Programming Language :: Python :: 3',
             'Programming Language :: Python :: 3.6',
             'Programming Language :: Python :: 3.7',
             'Programming Language :: Python :: 3.8',
             'Programming Language :: Python :: 3.9',
             "Programming Language :: Python :: 3.9",
             "Operating System :: MacOS :: OS Independent",
        ]
)
