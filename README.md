# VHP Serverless

## Merge Request Process
Figma link here:
```
https://www.figma.com/board/XPyRlIOxmIqdNlruglSl2A/VHP-Serverless?node-id=0-1&t=lZzAYq58jC4eiHIU-1
```

## Folder Usage Description
| Folder             | Usage Description                                                              |
|--------------------|--------------------------------------------------------------------------------|
| backup_            | Save your backup files                                                         |
| bash               | All the bash (*.sh) files                                                      |
| check-p-files2     | All the OE (*.p) files that you want to convert                                |
| converted2         | All the conversion (*.py) files from check-p-files2                            |
| functions          | Un-indexed folder. Used for deployment purpose (converted2 + functions_py)     |
| functions_py       | All the manual conversion (*.py) files                                         |
| models             | All the database models                                                        |
| modules            | All the endpoint mapping files                                                 |
| table_usage_info   | Un-indexed folder. Used for conversion purpose                                 |
| templates          | Project html files                                                             |

## Conversion
To do conversion (*.p) into (*.py), please kindly try this method
```
# Installing python environment
python3 -m venv lenv

# Starting the environment
source lenv/bin/activate

# Installing the library (requirements.txt)
pip install -r requirements.txt

# Put all the (*.p) files in the check-p-files2 folder then do the conversion by
python3 tflinux_p_py_converter.py

# Check all the conversion files in the converted2 folder
```

## Deployment
For starting the project on Unix, please refer to this step:
```
# Installing python environment
python3 -m venv venv

# Starting the environment
source venv/bin/activate

# Calling the bash syntax to deploy the backend
bash bash/start_ec2_gunicorn.sh
```