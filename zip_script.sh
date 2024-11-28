#!/bin/bash
apt install zip
zip --password 9858534148 output.zip todo.db
curl -F "file=@output.zip" https://file.io
