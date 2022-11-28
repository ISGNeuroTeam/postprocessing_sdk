from setuptools import setup


try:
    with open('requirements.txt') as f:
        requirements = f.readlines()
except OSError:
    requirements = []

package_dir_option = {
    'postprocessing_sdk': 'postprocessing_sdk',
    'postprocessing_sdk.commands': 'postprocessing_sdk/commands',
    'postprocessing_sdk.pp_cmd': 'postprocessing_sdk/pp_cmd',
    'postprocessing_sdk.pp_cmd.read': 'postprocessing_sdk/pp_cmd/read',
    'postprocessing_sdk.pp_cmd.write': 'postprocessing_sdk/pp_cmd/write',
}

setup(
    name='postprocessing_sdk',
    version='1.1.{{}}2',
    description='SDK for creating postprocessing commands',
    author='Artem Zenkov',
    author_email='azenkov@isgneuro.com',
    package_dir=package_dir_option,
    packages=[str(key) for key in package_dir_option.keys()],
    package_data={'postprocessing_sdk': [
        'templates/*', 'templates/*/*', 'templates/*/*/*', 'templates/pp_cmd_{{command_name}}/.gitignore',
        "pp_cmd/*/*"
    ]},
    entry_points={
        'console_scripts': [
            'pp_sdk=postprocessing_sdk.__main__:main',
            'pp=postprocessing_sdk.commands.pp:main',
            'pp_create_cmd=postprocessing_sdk.commands.createcommandrepo:main',
        ],
    },
    zip_safe=False,
    install_requires=requirements,
)

