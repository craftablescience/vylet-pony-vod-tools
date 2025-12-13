source .venv/bin/activate

cd src || exit 1
python -m subtitle_dl
python -m thumbnail_generator
cd ..

deactivate
