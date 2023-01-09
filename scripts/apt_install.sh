#!/bin/bash
sed 's/#.*//' "$PROJECT_DIR"/requirements/apt/*.txt | xargs sudo apt-get install
