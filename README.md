# Boilerplate Web Service
My bare minimum web service deployment

## Setup
Add a `config.py` file similar to:
```python
from configparser import ConfigParser


config = ConfigParser()
config.read('../.secure/config.ini')
```

Also, add a `config.ini` file similar to:
```ini
[github_hook]
secret = mySuper5ecretSecr3t!
```
where `mySuper5ecretSecr3t!` is the secret you specify in your GitHub repository `PUSH` ONLY webhook settings: https://github.com/YOUR_GITHUB_USERNAME/YOUR_GITHUB_REPOSITORY/settings/hooks/.
