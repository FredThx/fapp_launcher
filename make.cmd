python create_ico.py
python make_properties.py
pyinstaller ^
    --clean ^
    --windowed ^
    --add-data="icon.jpg;." ^
    --onefile ^
    --noconsole ^
    --noupx ^
    --icon=icon.ico ^
    --noconfirm ^
    --version-file=properties.rc ^
    fapp_launcher.py