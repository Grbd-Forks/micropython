#!/bin/bash

if [ -z "$1" ]
then
      venv="py27dev"
else
      venv=$1
fi

if [ ! -d "$venv" ]; then
  echo "Creating virtual environment $venv"
  tox -c tox_dev.ini
fi

# Enter the python virtual enviro on the current shell
echo "Entering virtual environment $venv"
bash --rcfile <(echo "source $venv/bin/activate")

