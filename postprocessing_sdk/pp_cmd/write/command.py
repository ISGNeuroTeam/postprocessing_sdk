import logging
import pandas as pd
from otlang.sdk.syntax import Keyword, Positional, OTLType
from pp_exec_env.base_command import BaseCommand, Syntax


log = logging.getLogger('pp_exec_env.w')


class WRITECommand(BaseCommand):

    # define syntax of your command here
    syntax = Syntax(
        [
            Positional("filename", required=True, otl_type=OTLType.TEXT),
            Keyword("type", required=True, otl_type=OTLType.TEXT),
        ],
        use_timewindow=False # if true keyword argument 'tws' and 'twf' will be added
    )

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        filename = self.get_arg("filename").value
        type = self.get_arg("type").value

        if type == 'parquet':
            df.to_parquet(
                f'data/{filename}', engine='pyarrow', compression=None
            )
        elif type == 'json':
            df.to_json(
                f'data/{filename}', orient='records', lines=True
            )
        else:
            raise ValueError('Unknown type')
        return df
