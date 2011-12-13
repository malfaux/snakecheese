from distutils.core import setup

setup(
    name = "subtypes",
    packages = ["subtypes"],
    version = "0.1.19",
    description = "types with new or removed constraints/properties",
    author = "adrian ilarion ciobanu",
    author_email = "cia@mud.ro",
    url = "http://shrd.net/p/loophole/trunk/python/src/handjobs/subtypes",
    download_url = "http://shrd.net/files/subtypes-0.1.19.tar.gz",
    keywords = ["subtypes"],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Python Software Foundation License',
        'Programming Language :: Python :: 2.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent'
        ],
    license = 'License :: OSI Approved :: Python Software Foundation License',
    long_description=open('README.txt').read(-1)
)
