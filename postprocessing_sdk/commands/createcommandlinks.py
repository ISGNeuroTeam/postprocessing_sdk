import os
import sys
from pathlib import Path
from .basecommand import BaseCommand, POST_PROC_COMMAND_DIR, POST_PROC_COMMAND_DIR_NAME


def create_command_links(directory):
    pp_cmd_dir = (directory / POST_PROC_COMMAND_DIR_NAME)
    pp_cmd_dir.mkdir(parents=True, exist_ok=True)
    for cmd_dir in POST_PROC_COMMAND_DIR.iterdir():
        if cmd_dir.is_dir() and cmd_dir.name != '__pycache__':
            print(f'Link to command {cmd_dir.name}')
            os.symlink(cmd_dir, pp_cmd_dir / cmd_dir.name)


class Command(BaseCommand):
    """
    Management utility to create postprocessing command repo
    """
    help = 'Creates commands directory and sepecified directory and makes links to postprocessing command'

    def add_arguments(self, parser):
        parser.add_argument(
            'dir',
            help='Directory where to create command links', default=None, nargs='?'
        )

    def handle(self, *args, **options):
        d = Path(options['dir'] or os.getcwd())
        create_command_links(d)


def main():
    command = Command()
    command.run_from_argv(['', 'createcommandlinks'] + sys.argv[1:])


if __name__ == '__main__':
    main()

