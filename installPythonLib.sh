#!/bin/sh

# echo ---
# echo 1
# curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# echo ---
# echo 2
# /usr/local/bin/python3.7 get-pip.py --user
# echo ---
# echo 3
# /usr/local/bin/python3.7 -m pip install --upgrade pip

# echo ---
# echo 4
# /usr/local/bin/python3.7 -m pip install line-bot-sdk

# ↓不要だったかも
# echo ---
# echo 5
# /usr/local/bin/python3.7 -m pip install requests

#  urllib3のバージョンがOpenSSLに対応していないため、低いバージョンをインストール
# echo ---
# echo 6
# /usr/local/bin/python3.7 -m pip install urllib3==1.25.11


exit
