#!/bin/bash

cd /Users/shamsulazhar/Documents/odesk/jp/emas_my_scrapy 
export PATH=$PATH:/Users/shamsulazhar/opt/miniconda3/envs/scrapy/bin
echo $PATH
export PYTHONPATH=/Applications
/Users/shamsulazhar/opt/miniconda3/envs/scrapy/bin/scrapy crawl emas_my
