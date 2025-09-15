from os.path import join, dirname
from setuptools import find_packages, setup

__version__ = None
exec(open('./_version.py', 'r').read())


def get_file_contents(file_name):
    """Reads the contents of the file."""
    with open(join(dirname(__file__), file_name)) as fp:
        return fp.read()


def get_requirements():
    """Reads the requirements.txt file."""
    requirements = get_file_contents('requirements.txt')
    install_requirements = []
    for line in requirements.split('\n'):
        line = line.strip()
        if line and not line.startswith('-'):
            install_requirements.append(line)
    return install_requirements


setup(
    name='IWS',
    version=__version__,
    description="The Posts IWS (Internal Web Service)",
    long_description=get_file_contents('README.rst'),
    author="Rohtash Lakra",
    author_email="rslakra@lakra.com",
    url='https://github.com/rslakra/posts-iws',
    install_requires=get_requirements(),
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    license="MIT",
    classifiers=(
        "Development Status :: 1 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
    )
)