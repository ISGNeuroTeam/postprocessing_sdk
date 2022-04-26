import sys
from pathlib import Path
from otlang.otl import OTL
from pp_exec_env.command_executor import CommandExecutor

from .basecommand import BaseCommand, CommandError

POST_PROC_SRC_DIR = Path(__file__).resolve().parent.parent

POST_PROC_COMMAND_DIR = POST_PROC_SRC_DIR / 'pp_cmd'


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
        commands_dir = options['commands_dir'] or POST_PROC_COMMAND_DIR
        if otl_query is None:
            self.repl(storage, commands_dir)
        else:
            self.run_otl(otl_query, storage, commands_dir)

    def repl(self, storage, commands_dir):
        while True:
            print('>>>', end='')
            otl_query = input()
            self.run_otl(otl_query, storage, commands_dir)

    def run_otl(self, otl_query, storage, commands_dir):
        storages = {
            'shared_post_processing': storage,
            'local_post_processing': storage,
            'interproc_storage': storage,
        }

        command_executor = CommandExecutor(storages, commands_dir, self.progress_notifier)
        for command_class in command_executor.command_classes.keys():
            setattr(command_executor.command_classes[command_class], 'storage', storage)

        syntax = command_executor.get_command_syntax()
        o = OTL(syntax)
        commands = o.translate(otl_query)
        commands = list(
            map(
                lambda command: command.to_dict(),
                commands
            )
        )
        df = command_executor.execute(commands)
        print(df)

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
    command.run_from_argv(sys.argv)


if __name__ == '__main__':
    main()
