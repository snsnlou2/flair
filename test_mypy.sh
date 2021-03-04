#!/bin/bash
set -e
serverIp=159.89.154.87
git clone https://github.com/snsnlou2/mypy.git
cd mypy
git checkout release-0.800
git submodule init
git submodule update
cd ..
pip install -U ./mypy
rm -rf ./mypy
python3 typecheck.py
eval "$(ssh-agent -s)"
chmod 600 root_key
ssh-keyscan $serverIp >> ~/.ssh/known_hosts
ssh-add root_key
zip -r mypy_test_cache.zip mypy_test_cache/
owner=flairNLP
repo=flair-Pair386-after
pv=$(python3 -V | cut -c8-10)
arc=$(uname -m)
yes | scp -i root_key ./mypy_test_cache.zip "root@$serverIp:~/cache/$owner---$repo\($pv---$arc\).zip"
