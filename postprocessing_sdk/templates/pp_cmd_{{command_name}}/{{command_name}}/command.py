import pandas as pd
from otlang.sdk.syntax import Keyword, Positional, OTLType
from pp_exec_env.base_command import BaseCommand, Syntax


class {{command_class_name}}(BaseCommand):

    # define syntax of your command here
    syntax = Syntax(
        [
            Positional("first_positional_string_argument", required=True, otl_type=OTLType.TEXT),
            Keyword("kwarg_int_argument", required=False, otl_type=OTLType.INTEGER),
            Keyword("kwarg_int_double_argument", required=False, otl_type=OTLType.NUMBERIC),
            Keyword("some_kwargs", otl_type=OTLType.ALL, inf=True),
        ],
        use_timewindow=False # if true keyword argument 'tws' and 'twf' will be added
    )

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.log_progress('Start {{command_name}} command')
        # that is how you get arguments
        first_positional_string_argument = self.get_arg("first_positional_string_argument").value
        kwarg_int_argument = self.get_arg("kwarg_int_argument").value or 5
        some_kwargs = {k.key: k.value for k in self.get_iter("some_kwargs")}

        # Make your logic here
        df = pd.DataFrame([[1, 2, 3], [2, 3, 4]], columns=["a", "b", "c"])

        # Add description of what going on for log progress
        self.log_progress('First part is complete.', stage=1, total_stages=2)
        #
        self.log_progress('Last transformation is complete', stage=2, total_stages=2)

        # Use ordinary logger if you need

        self.logger.debug(f'Command {{command_name}} get first positional argument = {first_positional_string_argument}')
        self.logger.debug(f'Command {{command_name}} get keyword argument = {kwarg_int_argument}')

        return df

