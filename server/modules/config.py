import yaml

with open('config.yaml', 'r') as f:
    config = yaml.load(f)

messages = config['messages']['en']
app_config = config['app']
