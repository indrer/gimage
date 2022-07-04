import argparse
import os.path
import sys
from github import Github
import imghdr

def is_file_valid(filepath):
    if not os.path.exists(filepath):
        print('This file does not exists!')
        sys.exit()
    else:
        return filepath

arg_parser = argparse.ArgumentParser(description='Gimage - Github as image hosting')
arg_parser.add_argument('--create', dest='repo', type=str, help='Repository name to create')
arg_parser.add_argument('--upload', dest='file', type=lambda x: is_file_valid(x), help='Image to upload')
arg_parser.add_argument('--add_token', dest='token', type=str, help='Github personal access token')

args = arg_parser.parse_args()

if args.file:
    print(args.file)
    sys.exit()

if args.file is None and (args.repo is None or args.token is None):
    print()

g = Github('')
print(g.get_user().login)