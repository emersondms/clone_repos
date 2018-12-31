#!/usr/bin/env python

import sys
import requests
from os.path import exists, join
from subprocess import CalledProcessError, check_call

if len(sys.argv) > 1:
    github_user = sys.argv[1]
else:
    sys.exit("Usage: python clone_repos.py <username>")

all_repos = requests.get('https://api.github.com/users/%s/repos' % github_user)

for repo in all_repos.json():
    try:
        repo_name = repo['name']

        if exists(repo_name):
            check_call(['rm', '-rf', repo_name])
            print("Repository '%s' deleted" % repo_name)

        repo_master = join(repo_name, '-master')

        if exists(repo_master):
            check_call(['rm', '-rf', repo_master])
            print("Repository '%s' deleted" % repo_master)

        check_call(['git', 'clone', repo['clone_url']])
    except CalledProcessError:
        print("ERROR cloning repository '%s'" % repo_name)
    except KeyboardInterrupt:
        break