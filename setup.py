from setuptools import setup
from pathlib import Path


try:
    with open('requirements.txt') as f:
        requirements = f.readlines()
except OSError:
    requirements = []


def get_pp_cmd_packages():
    """
    Reruns list post proc cmd packages
    """
    return [pp_rep.name for pp_rep in Path('pp_cmd_reps').iterdir() if pp_rep.is_dir()]


def find_pp_cmd_package_src_dir(pp_cmd_package_name):
    """
    Returns relative path to src dir of cmd package
    """
    package_path = Path('pp_cmd_reps') / pp_cmd_package_name
    return [d for d in package_path.iterdir() if d.is_dir()][0]


def get_pp_cmd_package_dir_option():
    return {
        'postprocessing_sdk.pp_cmd.' + pp_cmd_src_dir.name: str(pp_cmd_src_dir)
        for pp_cmd_src_dir in [
            find_pp_cmd_package_src_dir(pp_cmd_package_name) for pp_cmd_package_name in get_pp_cmd_packages()
        ]
    }


package_dir_option = {
    'postprocessing_sdk': 'postprocessing_sdk',
    'postprocessing_sdk.commands': 'postprocessing_sdk/commands',
    'postprocessing_sdk.pp_cmd': 'postprocessing_sdk/pp_cmd',
    'postprocessing_sdk.pp_cmd.read': 'postprocessing_sdk/pp_cmd/read',
    'postprocessing_sdk.pp_cmd.write': 'postprocessing_sdk/pp_cmd/write',
}

package_dir_option.update(get_pp_cmd_package_dir_option())

setup(
    name='postprocessing_sdk',
    version='0.1.0',
    description='SDK for creating postprocessing commands',
    author='Artem Zenkov',
    author_email='azenkov@isgneuro.com',
    package_dir=package_dir_option,
    packages=[str(key) for key in package_dir_option.keys()],
    package_data={'postprocessing_sdk': [
        'templates/*', 'templates/*/*', 'templates/*/*/*', 'templates/pp_cmd_{{command_name}}/.gitignore'
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

