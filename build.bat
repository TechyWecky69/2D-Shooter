@echo off
pip install pyinstaller
pip install pygame
pyinstaller --noconfirm --onefile --windowed --name "2D Shooter"  "./main.py"
