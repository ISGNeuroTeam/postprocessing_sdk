# Postprocessing SDK

SDK for creating postprocessing commands 

## Getting started
###  Prerequisites
1. [Optional] [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

### Installing
1. [Optional] Create python virtual environment. You may just use existing Python 3.9.7 if it is installed in the system.
```bash
conda create -p ./venv -y
conda install -p ./venv python==3.9.7 -y
```
2. Install postprocessing_sdk from ISGNeuro Python index
```bash
python3 -m pip install postprocessing_sdk \
--extra-index-url http://s.dev.isgneuro.com/repository/ot.platform/simple \
--trusted-host s.dev.isgneuro.com
```

### Available shell commands
Three shell commands are available:
1. Finds all commands in the current directory and its children and links them to the interpreter
```bash
python -m postprocessing_sdk createcommandlinks
```
or
```bash
pp_sdk createcommandlinks
```

2. Creates new command repository
```bash
python -m postprocessing_sdk createcommandrepo <command name>
```
or
```bash
pp_create_cmd <command name>
```
3. Post-processing interpreter
```bash
python -m postprocessing_sdk pp 
```
or
```bash
pp
```

## Creating new post-processing command

1. Create new repository for post-processing command. If you used conda-venv, then activate it.
```bash
pp_create_cmd <command_name> <parent directory for repository>
```
2. Go to the command directory and configure connection to platform in `otl_v1_config.ini`. Example:
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
