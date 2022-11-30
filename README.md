# Postprocessing SDK

SDK for creating postprocessing commands 

## Getting started
###  Prerequisites
1. [Optional] [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

### Deploy
1. [Optional] Create python virtual environment. You may just use existing Python 3.9.7 if it is installed in the system.
    ```bash
    conda create -p ./venv -y
    conda install -p ./venv python==3.9.7 -y
    conda activate ./venv
    ```
2. Install postprocessing_sdk from ISGNeuro Python index
    ```bash
    python3 -m pip install postprocessing_sdk \
    --extra-index-url http://s.dev.isgneuro.com/repository/ot.platform/simple \
    --trusted-host s.dev.isgneuro.com
    ```
3. Configure `otl_v1` command to connect with otl platform
    ```bash
    cp venv/lib/python3.9/site-packages/postprocessing_sdk/pp_cmd/otl_v1/config.example.ini venv/lib/python3.9/site-packages/postprocessing_sdk/pp_cmd/otl_v1/config.ini
    vi venv/lib/python3.9/site-packages/postprocessing_sdk/pp_cmd/otl_v1/config.ini
    ```
    Example:
    ```ini
    [spark]
    base_address = http://localhost
    username = admin
    password = 12345678
   
    [caching]
    # 24 hours in seconds
    login_cache_ttl = 86400
    # Command syntax defaults
    default_request_cache_ttl = 100
    default_job_timeout = 100
    ```
   
4. Launch post-processing interpreter  
    ```bash
    pp
    ```
5. Make sure that `otl_v1` command works:  
    ```bash
    pp
    Storage directory is /tmp/pp_cmd_head/storage
    Commmands directory is /tmp/pp_cmd_head/pp_cmd
    query: | otl_v1 <# makeresults count=100 #> | head 5 
    ```

    Type `exit` or `\q` to exit from interpreter

6. Create new post-processing command
    ```bash
    pp_create_cmd <command_name> <parent directory for repository>
    ```
7. Write your code in `command.py`. Example:
    ```python
    import logging
    import pandas as pd
    from otlang.sdk.syntax import Keyword, Positional, OTLType
    from pp_exec_env.base_command import BaseCommand, Syntax


    log = logging.getLogger('pp_exec_env.head2')

    DEFAULT_NUMBER = 10

    class HeadCommand(BaseCommand):
        # define syntax of your command here
        syntax = Syntax(
            [
                Positional("number", required=True, otl_type=OTLType.INTEGER),
            ],
            use_timewindow=False # if true keyword argument 'tws' and 'twf' will be added
        )

        def transform(self, df: pd.DataFrame) -> pd.DataFrame:
            number = self.get_arg('number').value
            return df.head(number or DEFAULT_NUMBER)
    ```

8. Create command archive for deploying on post-processing computing node:
    ```bash
    make pack
    ```
