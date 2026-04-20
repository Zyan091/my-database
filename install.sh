#!/bin/bash
pkg update -y && pkg upgrade -y
pkg install python git -y
git clone https://github.com/Zyan091/my-database
cd my-database
python main.py
