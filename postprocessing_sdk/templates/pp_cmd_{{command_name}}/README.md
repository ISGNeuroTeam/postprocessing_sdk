# pp_cmd_{{command_name}}
Postprocessing command "{{command_name}}"
## Description
{{command_name}} do (write here what it does)  


### Arguments
- first_positional_string_argument - positional argument, text, write what it means
- kwarg_int_argument - keyword argument, integer, write what it means
- ...

### Usage example
Show how it can be used  
```
... | {{command_name}} positional_arg, kwarg_int_argument=4  ...
```
Input dataframe example  
Output dataframe example  

## Getting started
### Installing
1. Create virtual environment with post-processing sdk 
```bash
    make dev
```
That command  
- downloads [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- creates python virtual environment with [postprocessing_sdk](https://github.com/ISGNeuroTeam/postprocessing_sdk)
- creates link to current command in postprocessing `pp_cmd` directory 

2. Configure `otl_v1` command. Example:  
```bash
    vi ./venv/lib/python3.9/site-packages/postprocessing_sdk/pp_cmd/otl_v1/config.ini
```
Config example:  
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

3. Configure storages for `readFile` and `writeFile` commands:  
```bash
   vi ./venv/lib/python3.9/site-packages/postprocessing_sdk/pp_cmd/readFile/config.ini
   
```
Config example:  
```ini
[storages]
lookups = /opt/otp/lookups
pp_shared = /opt/otp/shared_storage/persistent
```

### Run {{command_name}}
Use `pp` to run {{command_name}} command:  
```bash
pp
Storage directory is /tmp/pp_cmd_test/storage
Commmands directory is /tmp/pp_cmd_test/pp_cmd
query: | otl_v1 <# makeresults count=100 #> |  {{command_name}} 
```
## Deploy
1. Unpack archive `pp_cmd_{{command_name}}` to postprocessing commands directory
2. Configure config.ini if command need it.