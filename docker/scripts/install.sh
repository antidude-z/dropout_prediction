#!/bin/sh
python -m pip install --upgrade pip

if [ "$LIGHTWEIGHT" = "true" ]; then
  pip install --no-cache-dir -r light.txt
else
  pip install --no-cache-dir -r heavy.txt
fi
