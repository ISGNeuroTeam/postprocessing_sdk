# Postprocessing SDK

SDK for creating postprocessing commands 

## Getting started
###  Prerequisites
1. [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

### Installing
1. Create python virtual environment
```bash
conda create -p ./venv -y
conda install -p ./venv python==3.9.7 -y
./venv/bin/python3 ./venv/bin/pip install -r /work/postprocessing_sdk/requirements.txt 
```

### Available shell commands
Three shell commands are available:
1. Creates `pp_cmd` directory in current directory with postprocessing command links in it 
```bash
python ./postprocessing_sdk/__main__.py createcommandlinks
```
2. Creates new command repository
```bash
python ./postprocessing_sdk/__main__.py createcommandrepo <command name>
```
3. Post-processing interpreter
```bash
python ./postprocessing_sdk/__main__.py pp 
```

## Creating new post-processing command

1. Install postprocessing sdk
```bash
conda create -p ./venv -y
conda install -p ./venv python==3.9.7 -y
./venv/bin/python3 ./venv/bin/pip install postprocessing_sdk@git+ssh://git@github.com/ISGNeuroTeam/postprocessing_sdk.git@develop 
```
2. Create new repository for post-processing command
```bash
conda activate ./venv
pp_create_cmd <command_name> <parent directory for repository>
```
3. Go to just created command repository and configure connection to platform in `otl_v1_config.ini`. Example:
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
4. Write your code in `command.py`. Example:
```python
import logging
import pandas as pd
from otlang.sdk.syntax import Keyword, Positional, OTLType
from pp_exec_env.base_command import BaseCommand, Syntax


log = logging.getLogger('pp_exec_env.head2')

DEFAULT_NUMBER = 10

class HEADCommand(BaseCommand):
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

Available python packages:  
- pandas==1.4.1
- numpy==1.21.3
- pyarrow==7.0.0 

5. Check command execution using `pp` interpreter. Example:
```bash
pp
Storage directory is /tmp/pp_cmd_head/storage
Commmands directory is /tmp/pp_cmd_head/pp_cmd
query: | otl_v1 <# makeresults count=100 #> | head 5 
```
6. Type `exit` or `\q` to exit from interpreter

7. Create command archive for deploying on post-processing computing node:
```bash
make pack
```
