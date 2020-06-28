#!/bin/bash

sudo apt install mecab libmecab-dev mecab-ipadic-utf8

# ipadic-neologd
#sudo apt install git make curl xz-utils file
#cd /tmp
#git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
#cd mecab-ipadic-neologd
#echo yes | ./bin/install-mecab-ipadic-neologd -n

# unidic
#sudo apt install unidic-mecab

# unidic-neologd
#sudo apt install git make curl xz-utils file
#cd /tmp
#git clone --depth 1 https://github.com/neologd/mecab-unidic-neologd.git
#cd mecab-unidic-neologd
#echo yes | ./bin/install-mecab-unidic-neologd -n

pip install -r requirements.txt
