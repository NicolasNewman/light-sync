rm -rf ./build ./dist
pyinstaller --onefile --paths ./venv/Lib/site-packages light_sync.py frame_color_lib.py convertor_lib.py