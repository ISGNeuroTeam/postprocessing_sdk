import logging
import pandas as pd
from otlang.sdk.syntax import Keyword, Positional, OTLType
from pp_exec_env.base_command import BaseCommand, Syntax


log = logging.getLogger('pp_exec_env.{{command_name}}')


class {{command_name_uppercase}}Command(BaseCommand):

    # define syntax of your command here
    syntax = Syntax(
        [
            Positional("first_positional_string_argument", required=True, otl_type=OTLType.STRING),
            Keyword("kwarg_int_argument", required=False, otl_type=OTLType.INTEGER),
        ],
        use_timewindow=False # if true keyword argument 'tws' and 'twf' will be added
    )

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.log_progress('Start {{command_name}} command')

        # make your logic here

        # that is how you get arguments
        first_positional_string_argument = self.get_arg("first_positional_string_argument").value
        kwarg_int_argument = self.get_arg("kwarg_int_argument").value or 5

        # Add description of what going on for log progress
        self.log_progress('First part is complete.', stage=1, total_stages=2)
        #
        self.log_progress('Last transformation is complete', stage=2, total_stages=2)

        #use ordinary log if you need

        log.debug(f'Command {{command_name}} get first positional argument = {first_positional_string_argument}')
        log.debug(f'Command {{command_name}} get keyword argument = {kwarg_int_argument}')

        return df