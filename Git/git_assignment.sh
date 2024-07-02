#!/bin/bash

git init

nano README.md  # Edit the file and add content 

git add README.md && git commit -m "First version of README.md"

nano README.md  # Edit the file again 

git add README.md && git commit -m "Added a new line to README.md"
