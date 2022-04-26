import logging
import pandas as pd
from otlang.sdk.syntax import Keyword, Positional, OTLType
from pp_exec_env.base_command import BaseCommand, Syntax


log = logging.getLogger('pp_exec_env.r')


class READCommand(BaseCommand):

    # define syntax of your command here
    syntax = Syntax(
        [
            Positional("filename", required=True, otl_type=OTLType.TEXT),
            Keyword("type", required=True, otl_type=OTLType.TEXT),
        ],
        use_timewindow=False,
    )

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:

        filename = self.get_arg("filename").value
        type = self.get_arg("type").value

        if type == 'json':
            df = pd.read_json(f'data/{filename}', lines=True)
        elif type == 'parquet':
            df = pd.read_parquet(
                f'data/{filename}', engine='pyarrow', use_pandas_metadata=True
            )
        else:
            raise ValueError('Unknown type')
        return df
