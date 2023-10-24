"""Module for testing {{command_name}} command"""
import os
from hypothesis import given, strategies as st
import pandas as pd
from pytest import raises
from unittest import TestCase

from postprocessing_sdk.commands.pp import Command

from otlang.exceptions import OTLException

class TestCommand(TestCase):
    """Class for testing tail command"""

    def setUp(self):
        self.command = Command()
        commands_dir = os.path.join(os.path.dirname(os.getcwd()),
                                    'venv/lib/python3.9/site-packages/postprocessing_sdk/pp_cmd')
        self.command._create_command_executor(storage='', commands_dir=commands_dir)
        parent_dir = os.path.dirname(os.getcwd())
        # add current command to self.command with _import_user_commands()
        self.command.command_executor.command_classes.update(
            self.command.command_executor._import_user_commands(commands_directory=parent_dir, follow_links=True))

    def test_{{command_name}}_command(self):
        # enter sample dataframe
        sample = pd.DataFrame()
        # create otl query that should return the same dataframe as you have in sample
        otl_query = ''
        # calculate otl query with postprocessing
        result = self.command.run_otl(otl_query=otl_query_readfile_only, storage='', df_print=False)
        # check if sample and result are the same
        pd.testing.assert_frame_equal(sample, result)


    def run_failing_test_with_otl_query_loop(self, otl: str = "") -> None:
        sample = pd.DataFrame()
        # run tested command
        result = self.command.run_otl(otl_query=otl, storage='', raise_error=True, df_print=False)
        # check
        pd.testing.assert_frame_equal(sample, result)


def test_no_{{command_name}}_command(self):
    otl_query: str = f''  # enter query that has no {{command_name}} in it
    # this test should fail with OTLException
    # you may also try making tests with other errors like ValueError
    with raises(OTLException):
        self.run_failing_test_with_otl_query_loop(otl=otl_query)



