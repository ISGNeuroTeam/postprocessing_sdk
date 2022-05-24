import sys
import importlib

from postprocessing_sdk.commands.basecommand import CommandError


def main():
    """Run administrative commands."""

    try:
        try:
            command = sys.argv[1]
        except IndexError:
            raise CommandError('Missing command name')
        module = importlib.import_module(f'postprocessing_sdk.commands.{command}')
    except ImportError:
        raise CommandError('Command not found')

    command = module.Command()
    command.run_from_argv(sys.argv)


if __name__ == '__main__':
    main()

