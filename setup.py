from setuptools import setup


try:
    with open('requirements.txt') as f:
        requirements = f.readlines()
except OSError:
    requirements = []

setup(
    name='postprocessing_sdk',
    version='0.1.0',
    description='SDK for creating postprocessing commands',
    author='Artem Zenkov',
    author_email='azenkov@isgneuro.com',
    packages=['postprocessing_sdk', 'postprocessing_sdk.commands'],
    package_data={'postprocessing_sdk': [
        'templates/*', 'templates/*/*', 'templates/*/*/*',
    ]},
    entry_points={
        'console_scripts': ['pp_sdk=postprocessing_sdk.__main__:main'],
    },
    zip_safe=False,
    install_requires=requirements,
)

