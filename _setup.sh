rm -rf .venv
python -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install chat-downloader@git+https://github.com/Indigo128/chat-downloader pillow setuptools webvtt-py yt-dlp

cmake ext/subchat -B ext/subchat/build -DBUILD_GUI=OFF
cmake --build ext/subchat/build

deactivate

source _incremental.sh
