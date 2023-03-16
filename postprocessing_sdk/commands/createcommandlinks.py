import os
import sys
from pathlib import Path
from postprocessing_sdk.commands.basecommand import BaseCommand, POST_PROC_COMMAND_DIR
import importlib.util
import pp_exec_env.base_command


def create_command_links(directory):
    """
    Find all commands in the given directory and create symlinks for them.
    """
    print(POST_PROC_COMMAND_DIR)
    for root, dirs, files in os.walk(directory):
        if "__init__.py" in files:
            module_name = Path(root).name
            spec = importlib.util.spec_from_file_location(module_name, Path(root) / "__init__.py")
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            try:
                spec.loader.exec_module(module)
            except Exception as e:
                print(f"Could not import {module_name} from {root}\n{e}")
                continue

            sys.modules.pop(spec.name)
            if module.__dict__.get('__all__', None) is None or not module.__all__:
                continue
            if len(module.__all__) != 1:
                continue

            cls = module.__getattribute__(module.__all__[0])
            if cls.__base__ == pp_exec_env.base_command.BaseCommand:
                try:
                    os.symlink(Path(root), POST_PROC_COMMAND_DIR / module_name, target_is_directory=True)
                    print(f"Success: Added {module_name} command")
                except FileExistsError:
                    print(f"Link to {cls} already exists")


class Command(BaseCommand):
    """
    Management utility to create postprocessing command repo
    """
    help = 'Creates symlinks for all commands in the given directory for the `pp` interpreter'

    def add_arguments(self, parser):
        parser.add_argument(
            'dir',
            help='Directory where to create command links, default is current directory', default=None, nargs='?'
        )

    def handle(self, *args, **options):
        d = Path(options['dir'] or os.getcwd())
        create_command_links(d)


def main():
    command = Command()
    command.run_from_argv(['', 'createcommandlinks'] + sys.argv[1:])


if __name__ == '__main__':
    main()
