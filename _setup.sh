rm -rf .venv
python -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install pillow setuptools webvtt-py yt-dlp
pip install ext/chat-downloader

cmake ext/subchat -B ext/subchat/build -DBUILD_GUI=OFF
cmake --build ext/subchat/build

deactivate

source _incremental.sh
