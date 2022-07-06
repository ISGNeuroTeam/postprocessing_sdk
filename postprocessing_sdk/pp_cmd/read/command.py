import logging
import pandas as pd
from pathlib import Path
from otlang.sdk.syntax import Keyword, Positional, OTLType
from pp_exec_env.base_command import BaseCommand, Syntax


log = logging.getLogger('pp_exec_env.r')


class ReadCommand(BaseCommand):

    # define syntax of your command here
    syntax = Syntax(
        [
            Positional("filename", required=True, otl_type=OTLType.TEXT),
            Keyword("type", required=False, otl_type=OTLType.TEXT),
        ],
    )

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:

        filename = self.get_arg("filename").value
        type = self.get_arg("type").value or filename.split('.')[-1]

        storage = self.storage
        # check file exists
        if not Path(f'{storage}/{filename}').exists():
            raise ValueError('File not exists')
        if type == 'json':
            df = pd.read_json(f'{storage}/{filename}', lines=True)
        elif type == 'parquet':
            df = pd.read_parquet(
                f'{storage}/{filename}', engine='pyarrow', use_pandas_metadata=True
            )
        else:
            raise ValueError('Unknown type')
        return df
