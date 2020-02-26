#!/bin/bash

PROG=python3
SCRIPT=main.py
VENVDIR=.venv
REQIREMENTS=requirements.txt

cd "$( dirname "${BASH_SOURCE[0]}" )"

$PROG -m pip install virtualenv > /dev/null 2> /dev/null

if [ ! -d "$VENVDIR" ]; then
    echo "creating virtual environment for python"
    $PROG -m virtualenv $VENVDIR > /dev/null
    source $VENVDIR/bin/activate
    python3 -m pip install -r $REQIREMENTS > /dev/null
fi

source $VENVDIR/bin/activate
python3 -m pip install -r $REQIREMENTS > /dev/null

python3 $SCRIPT

deactivate
