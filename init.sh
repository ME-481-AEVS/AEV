#!/bin/bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt install git
sudo apt-get install python
git clone https://github.com/ME-481-AEVS/AEV.git
pip install -r AEV/requirements.txt
python webstreaming.py &
python main.py