import sys
import traceback
import readline
import re
import itertools
import pandas as pd

from pathlib import Path
from otlang.otl import OTL
from otlang.exceptions import OTLException
from pp_exec_env.command_executor import CommandExecutor

from .basecommand import BaseCommand, CommandError, POST_PROC_SRC_DIR, POST_PROC_COMMAND_DIR, POST_PROC_COMMAND_DIR_NAME


readline.parse_and_bind("tab: complete")

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)


class Completer:
    """
    OTL command name completer for pp utility
    """
    def __init__(self, command_executor: CommandExecutor):
        self.command_executor = command_executor
        self.syntax = self.command_executor.get_command_syntax()

    @staticmethod
    def nth(iterable, n, default=None):
        """
        Returns the `n`-th item or a default value
        See: https://docs.python.org/3/library/itertools.html#itertools-recipes
        """
        return next(itertools.islice(iterable, n, None), default)

    def complete(self, text, state):
        """
        Returns `state`-th command that can be substituted in `text`
        """
        cmds = self.syntax.keys()
        current = text.split("|")[-1]
        if len(current) != 0 and re.match("\s", current[-1]) is None:
            return Completer.nth(filter(lambda s: s.startswith(current.strip()), cmds), state, default=None)
        return Completer.nth(cmds, state, None)


class Command(BaseCommand):
    """
    Management utility to create postprocessing command repo
    """
    help = 'Creates postprocessing command repository.'

    def add_arguments(self, parser):
        parser.add_argument(
            'otl_query', nargs='?',
            help='Otl query string',
            default=None
        )
        parser.add_argument(
            '--commands_dir',
            help='Directory for commands', nargs='?', default=None,
        )
        parser.add_argument(
            '--storage',
            help='Directory for dataframes storage', nargs='?', default=None,
        )
        parser.add_argument(
            '--user',
            help='User unique identifier', nargs='?', default=None,
        )
        parser.add_argument(
            '--file', '-f',
            help='File with otl command', nargs='?', default=None
        )

    def handle(self, *args, **options):
        otl_query = options['otl_query']
        if otl_query is None:
            otl_file = options['file']
            if otl_file:
                with open(otl_file, 'r') as f:
                    otl_query = f.read()

        storage = options['storage'] or 'storage'
        commands_dir = options['commands_dir']
        user_id = options['user'] or 'admin'
        Path(storage).mkdir(parents=True, exist_ok=True)

        if not commands_dir:
            if Path(POST_PROC_COMMAND_DIR_NAME).exists():
                commands_dir = POST_PROC_COMMAND_DIR_NAME
            else:
                commands_dir = POST_PROC_COMMAND_DIR

        self._create_command_executor(storage, commands_dir)
        platform_envs = {'user_guid': user_id}
        if otl_query is None:
            self.repl(storage, commands_dir, platform_envs)
        else:
            self.run_otl(otl_query, storage, commands_dir, platform_envs)

    def repl(self, storage, commands_dir, platform_envs=None):
        print(f'Storage directory is {Path(storage).resolve()}')
        print(f'Commmands directory is {Path(commands_dir).resolve()}')
        completer = Completer(self.command_executor)
        readline.set_completer(completer.complete)

        while True:
            otl_query = input('query: ')
            if otl_query == r'\q' or otl_query == 'exit':
                exit(0)
            if otl_query == r'\?' or otl_query == 'help':
                self.print_help()
            else:
                self.run_otl(otl_query, storage, commands_dir, platform_envs)

    def _create_command_executor(self, storage, commands_dir):
        storages = {
            'shared_post_processing': storage,
            'local_post_processing': storage,
            'interproc_storage': storage,
        }
        self.command_executor = CommandExecutor(storages, commands_dir, self.progress_notifier)

    def print_help(self):
        syntax = self.command_executor.get_command_syntax()
        print('Available OTL commands')
        for command, command_syntax_dict in syntax.items():
            print(f'{command}:')
            if 'help' in command_syntax_dict:
                print(command_syntax_dict['help'])
            else:
                print(self._get_help_from_command_syntax_dict(command_syntax_dict))

    @staticmethod
    def _get_help_from_command_syntax_dict(command_syntax_dict):
        command_help = ['\tArguments: ', ]
        for rule in command_syntax_dict['rules']:
            command_help.append(f"\t\t{rule['name']}")
            for cmd_attr in ['type', 'required', 'inf', 'input_types']:
                if cmd_attr in rule:
                    command_help.append(f"\t\t\t{cmd_attr}: {rule[cmd_attr]}")
        command_help.append('\tProperties:')
        command_help.append(f"\t\tuse_timewindow: {command_syntax_dict['use_timewindow']}")
        return '\n'.join(command_help)

    def run_otl(self, otl_query, storage, commands_dir=None, platform_envs=None, raise_error: bool = False,
                df_print: bool = True) -> pd.DataFrame:
        command_executor = self.command_executor
        # set dev storage for all user commands
        for command_class in command_executor.command_classes.keys():
            setattr(command_executor.command_classes[command_class], 'storage', storage)

        # read otl_v2 config  from current directory
        if 'otl_v1' in command_executor.command_classes:
            otl_v1_command = command_executor.command_classes['otl_v1']
            otl_v1_dict_conf = {
                'spark': {
                    'base_address': 'http://localhost',
                    'username': 'admin',
                    'password': '12345678',
                },
                'caching': {
                    'login_cache_ttl': 86400,
                    'default_request_cache_ttl': 100,
                    'default_job_timeout': 100,
                }
            }
            otl_v1_command.config.read_dict(otl_v1_dict_conf)
            if Path(POST_PROC_COMMAND_DIR / "otl_v1" / "config.ini").exists():
                otl_v1_command.config.read(POST_PROC_COMMAND_DIR / "otl_v1" / "config.ini")

            if Path('otl_v1_config.ini').exists():
                otl_v1_command.config.read('otl_v1_config.ini')

        syntax = command_executor.get_command_syntax()
        o = OTL(syntax)
        try:
            try:
                commands = o.translate(otl_query)
            except OTLException as err:
                print('Translation error')
                print(err)
                if raise_error:
                    raise OTLException('Translation error')
            commands = list(
                map(
                    lambda command: command.to_dict(),
                    commands
                )
            )
            df: pd.DataFrame = command_executor.execute(commands, platform_envs)
            print_df(df, do_print=df_print)
            return df
        except Exception as err:
            if raise_error:
                raise err
            tb = traceback.format_exc()
            print(tb)
            return pd.DataFrame()

    @staticmethod
    def progress_notifier(
            message,
            command_name, command_index_in_pipeline,
            total_commands_in_pipeline, stage=None, total_stages=None, depth=0
    ):
        command_message = '\t' * depth + f'{command_index_in_pipeline} out of {total_commands_in_pipeline} command.' \
                                         f' Command {command_name}.'
        if stage is None:
            stage_message = ''
        else:
            stage_message = f'Stage {stage}/{total_stages}'
        result_message = command_message + ' ' + stage_message + ' ' + message
        print(result_message)

def print_df(string: str, do_print: bool) -> None:
    if do_print:
        print(string)

def main():
    command = Command()
    command.run_from_argv(['', 'pp'] + sys.argv[1:])


if __name__ == '__main__':
    main()
