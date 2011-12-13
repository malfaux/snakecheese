from setuptools import setup, find_packages

setup(
    name = "django-contrib-requestprovider",
    install_requires = ['django',],
    packages = find_packages('.'),
    package_dir = {'':'.'},
    version = "1.0.0",
    description = "access django request object whenever you need it",
    author = "adrian ilarion ciobanu",
    author_email = "cia@mud.ro",
    url = "http://shrd.net/p/loophole/trunk/python/src/",
    download_url = "http://shrd.net/files/django-contrib-requestprovider-1.0.0.tar.gz",
    keywords = ["django contrib","request object provider"],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Environment :: Web Environment',
        'Operating System :: OS Independent'
        ],
    license = 'License :: OSI Approved :: BSD License',
    long_description=open('README.txt').read(-1)
)
