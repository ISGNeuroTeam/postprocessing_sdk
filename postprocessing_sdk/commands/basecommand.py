import sys
import os

from pathlib import Path
from argparse import ArgumentParser, HelpFormatter


class CommandError(Exception):
    """
    Exception class indicating a problem while executing a management
    command.
    """
    def __init__(self, *args, returncode=1, **kwargs):
        self.returncode = returncode
        super().__init__(*args, **kwargs)


class BaseCommand:
    BASE_DIR = Path(__file__).resolve().parent.parent
    help = ''

    def __init__(self):
        self.stdout = sys.stdout
        self.stderr = sys.stderr

    def create_parser(self, prog_name, subcommand, **kwargs):
        """
        Create and return the ``ArgumentParser`` which will be used to
        parse the arguments to this command.
        """
        parser = ArgumentParser(
            prog='%s %s' % (os.path.basename(prog_name), subcommand),
            description=self.help or None,
            **kwargs
        )
        self.add_arguments(parser)
        return parser

    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments.
        """
        pass

    def print_help(self, prog_name, subcommand):
        """
        Print the help message for this command, derived from
        ``self.usage()``.
        """
        parser = self.create_parser(prog_name, subcommand)
        parser.print_help()

    def run_from_argv(self, argv):
        """
        Set up any environment changes requested (e.g., Python path
        and Django settings), then run this command. If the
        command raises a ``CommandError``, intercept it and print it sensibly
        to stderr. If the ``--traceback`` option is present or the raised
        ``Exception`` is not ``CommandError``, raise it.
        """
        parser = self.create_parser(argv[0], argv[1])

        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)
        # Move positional args out of options to mimic legacy optparse
        args = cmd_options.pop('args', ())
        try:
            self.handle(*args, **cmd_options)
        except CommandError as e:
            # SystemCheckError takes care of its own formatting.
            self.stderr.write('%s: %s' % (e.__class__.__name__, e))
            sys.exit(e.returncode)

    def handle(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement
        this method.
        """
        raise NotImplementedError('subclasses of BaseCommand must provide a handle() method')
