#!/usr/bin/env bash

pipreqs . --savepath requirements/prod.txt

echo "git+https://github.com/mohamed-aziz/python-nginx.git" >> requirements/prod.txt
