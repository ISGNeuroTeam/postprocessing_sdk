import sys
import traceback
import readline

from pprint import pp
from pathlib import Path
from otlang.otl import OTL
from otlang.exceptions import OTLException
from pp_exec_env.command_executor import CommandExecutor

from .basecommand import BaseCommand, CommandError, POST_PROC_SRC_DIR, POST_PROC_COMMAND_DIR, POST_PROC_COMMAND_DIR_NAME


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

    def handle(self, *args, **options):
        otl_query = options['otl_query']
        storage = options['storage'] or 'storage'
        commands_dir = options['commands_dir']
        Path(storage).mkdir(parents=True, exist_ok=True)

        if not commands_dir:
            if Path('pp_cmd').exists():
                commands_dir = POST_PROC_COMMAND_DIR_NAME
            else:
                commands_dir = POST_PROC_COMMAND_DIR

        self._create_command_executor(storage, commands_dir)

        if otl_query is None:
            self.repl(storage, commands_dir)
        else:
            self.run_otl(otl_query, storage, commands_dir)

    def repl(self, storage, commands_dir):
        print(f'Storage directory is {Path(storage).resolve()}')
        print(f'Commmands directory is {Path(commands_dir).resolve()}')

        while True:
            otl_query = input('query: ')
            if otl_query == '\q' or otl_query == 'exit':
                exit(0)
            if otl_query == '\?' or otl_query == 'help':
                self.print_help()
            else:
                self.run_otl(otl_query, storage, commands_dir)

    def _create_command_executor(self, storage, commands_dir):
        storages = {
            'shared_post_processing': storage,
            'local_post_processing': storage,
            'interproc_storage': storage,
        }
        self.command_executor = CommandExecutor(storages, commands_dir, self.progress_notifier)

    def print_help(self):
        syntax = self.command_executor.get_command_syntax()
        for command, command_syntax_dict in syntax.items():
            print(f'{command}:')
            pp(command_syntax_dict)

    def run_otl(self, otl_query, storage, commands_dir):
        storages = {
            'shared_post_processing': storage,
            'local_post_processing': storage,
            'interproc_storage': storage,
        }

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
                return
            commands = list(
                map(
                    lambda command: command.to_dict(),
                    commands
                )
            )
            df = command_executor.execute(commands)
            print(df)
        except Exception as err:
            tb = traceback.format_exc()
            print(tb)

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


def main():
    command = Command()
    command.run_from_argv(['', 'pp'] + sys.argv[1:])


if __name__ == '__main__':
    main()
