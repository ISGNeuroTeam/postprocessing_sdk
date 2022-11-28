import logging
import pandas as pd
from otlang.sdk.syntax import Keyword, Positional, OTLType
from pp_exec_env.base_command import BaseCommand, Syntax


log = logging.getLogger('pp_exec_env.w')


class WriteCommand(BaseCommand):

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
        if df is None:
            df = pd.DataFrame()

        self.log_progress(f'Start writing to {storage}/{filename}', stage=1, total_stages=2)
        if type == 'parquet':
            df.to_parquet(
                f'{storage}/{filename}', engine='pyarrow', compression=None
            )
        elif type == 'json':
            df.to_json(
                f'{storage}/{filename}', orient='records', lines=True
            )
        else:
            raise ValueError('Unknown type')
        self.log_progress(f'Writing is done {storage}/{filename}', stage=2, total_stages=2)
        return df
