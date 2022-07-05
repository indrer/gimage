import argparse
from os import environ
import os.path
import sys
import configparser
from github import Github
import imghdr

CONFIG_PATH = 'settings.gimg'
TOKEN = ''
REPO_NAME = ''

config = configparser.ConfigParser()
arg_parser = argparse.ArgumentParser(description='Gimage - Github as image hosting')


def is_file_valid(filepath):
    if not os.path.exists(filepath):
        print('This file does not exists!')
        sys.exit()
    else:
        return filepath

def save_config(conf):
    with open(CONFIG_PATH, 'w') as configfile:
        conf.write(configfile)


arg_parser = argparse.ArgumentParser(description='Gimage - Github as image hosting')
arg_parser.add_argument('-nr', dest='nr', action='store_true', help='Set if needed to create new repo')
arg_parser.add_argument('--repo', dest='repo', type=str, help='Repository name to create')
arg_parser.add_argument('--upload', dest='file', type=lambda x: is_file_valid(x), help='Image to upload')
arg_parser.add_argument('--add_token', dest='token', type=str, help='Github personal access token')

args = arg_parser.parse_args()
config.read(CONFIG_PATH)


if not os.path.exists(CONFIG_PATH):
    config['gimage'] = {'pat': '', 'repo': ''}
    save_config(config)
else:
    TOKEN = config['gimage']['pat']
    REPO_NAME = config['gimage']['repo']


if args.token:
    TOKEN = args.token
    config['gimage']['pat'] = TOKEN
    save_config(config)
elif len(TOKEN) == 0:
    print('Set your personal access token first using --add_token flag.')
    sys.exit()

if args.repo:
    REPO_NAME = args.repo
    config['gimage']['repo'] = REPO_NAME
    save_config(config)
elif len(REPO_NAME) == 0:
    print('Make sure to set a repo name using --repo flag. To create a new repo, add -nr flag to the command.')
    sys.exit()

if args.file:
    print(args.file)
    sys.exit()

if args.file is None and (args.repo is None or args.token is None):
    print()

g = Github(TOKEN)
print(g.get_user().login)