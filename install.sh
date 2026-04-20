#!/bin/bash
pkg update -y && pkg upgrade -y
pkg install python git -y
git clone https://github.com/သင့်ရဲ့Username/သင့်ရဲ့Zyan 
cd သင့်ရဲ့Zyan
python main.py
