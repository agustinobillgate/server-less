# VHP Serverless

## Merge Request Process
Figma link here:
https://www.figma.com/board/XPyRlIOxmIqdNlruglSl2A/VHP-Serverless?node-id=0-1&t=lZzAYq58jC4eiHIU-1

## Folder Usage Description
| Folder             | Description                                                                      |
|--------------------|----------------------------------------------------------------------------------|
| backup_            | Save your backup files                                                           |
| bash               | All the bash (*.sh) files                                                        |
| check-p-files2     | All the OE (*.p) files that you want to convert                                  |
| converted2         | All the conversion (*.py) files from check-p-files2                              |
| functions          | Un-indexed folder. Used for deployment purpose (converted2 + functions_py)       |
| functions_py       | All the manually converted (*.py) files                                          |
| models             | All the database models                                                          |
| modules            | All the endpoint mapping files                                                   |
| table_usage_info   | Un-indexed folder. Used for conversion purpose                                   |
| templates          | Project html files                                                               |

## Conversion
To convert (*.p) files into (*.py), please try this method:
```
# Create the python environment
python3 -m venv lenv

# Activate the environment
source lenv/bin/activate

# Install the required packages
pip install -r requirements.txt

# Put all the (*.p) files in the check-p-files2 folder and run the converter
python3 tflinux_p_py_converter.py

# All converted files will appear in the converted2 folder
```

## Deployment
To start the project on Unix, follow these steps:
```
# Create the python environment
python3 -m venv venv

# Activate the environment
source venv/bin/activate

# Run the backend using bash command
bash bash/start_ec2_gunicorn.sh
```

---

## 🛠 GitLab CI/CD Runner (Production Deployment)

> Deployment will be triggered automatically **whenever a merge to the `production` branch happens** in GitLab.

### How It Works:

- GitLab Runner (`shell executor`) is configured on the `stagingpython` server as user `vhpadmin`
- The `.gitlab-ci.yml` file will run:
  ```bash
  bash/bash/sync_and_restart.sh
  ```
  every time a new commit is pushed to `production`

### Important:

- Runner must include the tag: `production-environment`
- Your `.gitlab-ci.yml` should include:
  ```yaml
  tags:
    - production-environment
  only:
    - production
  ```

### Tips:

- Make sure the runner runs under user `vhpadmin` to access local scripts like virtualenv or SSH
- To re-install the runner as a system service:
  ```bash
  sudo gitlab-runner install \
      --user vhpadmin \
      --working-directory /usr1/gitlab-runner \
      --config /usr1/gitlab-runner/config.toml
  ```
