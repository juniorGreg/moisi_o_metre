#!/bin/bash
export DEBUG="FALSE"
python3 manage.py collecstatic

git checkout prod
git merge master
git push
git checkout master
