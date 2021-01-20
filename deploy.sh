#!/bin/bash
export DEBUG="FALSE"
python3.8 manage.py collectstatic

git checkout prod
git merge master
git push
git checkout master

export DEBUG="TRUE"
