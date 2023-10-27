"""Module for testing {{command_name}} command"""
import os
import pandas as pd
from unittest import TestCase
from sys import prefix

from postprocessing_sdk.commands.pp import Command

from otlang.exceptions import OTLException

class TestCommand(TestCase):
    """Class for testing tail command"""

    def setUp(self):
        self.command = Command()
        commands_dir = os.path.join(prefix, 'lib/python3.9/site-packages/postprocessing_sdk/pp_cmd')
        self.command._create_command_executor(storage='', commands_dir=commands_dir)
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        # add current command to self.command with _import_user_commands()
        self.command.command_executor.command_classes.update(
            self.command.command_executor._import_user_commands(commands_directory=parent_dir, follow_links=True))

    def run_otl(self, otl_query: str = ''):
        self.command.run_otl(otl_query=otl_query, storage='', df_print=False)

    def test_{{command_name}}_command(self):
        # enter sample dataframe
        sample = pd.DataFrame([[1, 2, 3], [2, 3, 4]], columns=["a", "b", "c"])
        # create otl query that should return the same dataframe as you have in sample
        otl_query = '| {{command_name}} first_positional_argument'
        # calculate otl query with postprocessing
        result = self.run_otl(otl_query=otl_query)
        # check if sample and result are the same
        pd.testing.assert_frame_equal(sample, result)


