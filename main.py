import argparse
import os
import sys
import configparser
from github import Github
import imghdr
import random
import string

CONFIG_PATH = 'settings.gimg'
GITHUB_URL = 'https://github.com/'
TOKEN = ''
REPO_NAME = ''
FILE_PATH = ''

arg = sys.argv[-1]
if len(sys.argv) > 1 and arg[0] != '--':
    sys.argv[-1] = '--file'
    sys.argv.append(arg)

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

def generate_file_name(files, filetype):
    file_name = ''.join(random.choices(string.ascii_lowercase, k=5)) + '.' + filetype
    filenames = [f.path for f in files]
    while file_name in filenames:
        file_name = ''.join(random.choices(string.ascii_lowercase, k=5)) + '.' + filetype
    return file_name


arg_parser = argparse.ArgumentParser(description='Gimage - Github as image hosting')
arg_parser.add_argument('-nr', dest='nr', action='store_true', help='Set if needed to create new repo')
arg_parser.add_argument('--repo', dest='repo', type=str, help='Repository name to create')
arg_parser.add_argument('--add_token', dest='token', type=str, help='Github personal access token')
arg_parser.add_argument('--file', dest='file', type=is_file_valid, help='Image to upload')

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

FILE_PATH = args.file

# check if image
FILE_TYPE = imghdr.what(FILE_PATH)
if FILE_TYPE is None:
    print('Unsupported image type. Currently supported image types: rgb, gif, pbm, pgm, ppm, tiff, rast, xbm, jpeg, bmp, png, webp and exr.')
    sys.exit()

g = Github(TOKEN)
user = g.get_user()

# create the repo if needed
if args.nr:
    repos = user.get_repos()
    in_repo = False
    for repo in repos:
        if repo.name == REPO_NAME and repo.fork is False:
            in_repo = True
    if not in_repo:
        img_repo = user.create_repo(REPO_NAME)
else:
    img_repo = user.get_repo(REPO_NAME)

with open(FILE_PATH, 'rb') as f:
    data = f.read()

file_name = generate_file_name(img_repo.get_contents(''), FILE_TYPE)
commit_message = 'Add ' + file_name
img_repo.create_file(file_name, commit_message, data)