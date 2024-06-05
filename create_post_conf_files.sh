python3 -m pip install virtualenv
python3 -m virtualenv ./venv
. ./venv/bin/activate
pip install -U pip
pip install wheel
pip install -r ./requirements.txt

pip list
sudo python3 ./create_configs.py 
deactivate
