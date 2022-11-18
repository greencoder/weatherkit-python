from distutils.core import setup

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='weatherkit-python',
    version='1.0',
    packages=['weatherkit'],
    license='MIT',
    description='A Python interface for Apple\'s WeatherKit APIs',
    url='https://github.com/greencoder/weatherkit-python',
    download_url='https://github.com/greencoder/weatherkit-python/archive/1.0.tar.gz',
    author='Scott Newman',
    author_email='snewman18@gmail.com',
    long_description=long_description,
    long_description_content_type = "text/markdown",
    package_dir = {"": "src"},
    python_requires = ">=3.6",
    install_requires=[
        'jsonpickle>=1.4.3',
        'cryptography>=38',
        'pyjwt>=2.6.0',
        'requests>=2.28.1',
    ],
)
