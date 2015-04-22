from distutils.core import setup


setup(
    name='Pythonbits',
    author='Ichabond',
    version='2.0.0',
    packages=['pythonbits'],
    scripts=['bin/pythonbits'],
    url='https://github.com/Ichabond/Pythonbits',
    license='LICENSE',
    description='A Python pretty printer for generating attractive movie descriptions with screenshots.',
    install_requires=[
        "imdbpie >= 2.0.0",
        "requests >= 2.3.0",
        "tvdb-api == 1.9",
        "wsgiref>=0.1.2"
    ],
)
