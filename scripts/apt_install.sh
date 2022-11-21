#!/bin/bash
sed 's/#.*//' $PROJECT_DIR/requirements/apt_*.txt | xargs sudo apt-get install
