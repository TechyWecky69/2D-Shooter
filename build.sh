pip install pyinstaller --break-system-packages
pip install pygame --break-system-packages
pyinstaller --noconfirm --onefile --windowed --name "2D Shooter"  "./main.py"
