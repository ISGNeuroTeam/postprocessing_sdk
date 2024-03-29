import os
import sys
from pathlib import Path
from .basecommand import BaseCommand, CommandError,  POST_PROC_SRC_DIR, POST_PROC_COMMAND_DIR, POST_PROC_COMMAND_DIR_NAME
from jinja2 import Template


class Command(BaseCommand):
    """
    Management utility to create postprocessing command repo
    """
    help = 'Creates postprocessing command repository.'

    def add_arguments(self, parser):
        parser.add_argument(
            'command_name',
            help='Command name',
        )
        parser.add_argument(
            'dir',
            help='Directory for repo', default=None, nargs='?'
        )

    @staticmethod
    def validate_name(name):
        """
        Validates command name `name`, raises CommandError if command name is invalid
        """
        if name is None:
            raise CommandError('Please provide a non-empty name.')
        # Check it's a valid directory name.
        if not name.isidentifier():
            raise CommandError(
                f'{name} is not a valid command name. Please make sure the' 
                'name is a valid identifier.'
            )

    def handle(self, *args, **options):
        command_name = options['command_name']

        self.validate_name(command_name)

        # directory with command template
        command_template_dir = self.BASE_DIR / 'templates' / 'pp_cmd_{{command_name}}'

        repo_dir = options['dir'] or os.getcwd()
        repo_dir = Path(repo_dir).resolve()
        pascal_case = ''.join(map(str.title, command_name.split("_")))
        context = {
            'command_name': command_name,
            'command_name_uppercase': command_name.upper(),
            'command_class_name': f'{pascal_case}Command'
        }
        command_repo = repo_dir / f'pp_cmd_{command_name}'
        self.render_dir(command_template_dir, command_repo, context)

        # create a symlink for `pp` utility in pp_cmd
        os.symlink(command_repo / command_name, POST_PROC_COMMAND_DIR / command_name)

        print(f'Command repository with name {command_repo} created')

    def render_dir(self, template_directory_path, command_directory_path, context):
        print(f'Create directory {str(command_directory_path)}')
        # create directory command_directory_path
        command_directory_path.mkdir(parents=True, exist_ok=True)

        # iterate through template directory and call render function for all files and directories
        for child in template_directory_path.iterdir():
            rendered_name = Template(str(child.name)).render(context) + ''
            if child.is_dir():
                self.render_dir(
                    template_directory_path / str(child.name),
                    command_directory_path / rendered_name,
                    context
                )
            else:
                self.render_file(
                    template_directory_path / str(child.name),
                    command_directory_path / rendered_name,
                    context
                )

    @staticmethod
    def render_file(template_file, rendered_file, context):
        print(f'Create file {str(rendered_file)}')
        rendered_file.write_text(Template(template_file.read_text()).render(context))


def main():
    command = Command()
    command.run_from_argv(['', 'createcommandrepo'] + sys.argv[1:])


if __name__ == '__main__':
    main()
