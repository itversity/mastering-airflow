#!/bin/bash -x

sudo service ssh start
/home/itversity/.local/bin/jupyter lab --ip 0.0.0.0
