git submodule init
git submodule update

cd JavPy/JavPy/app/webfe/ || exit
npm install
npm run build

pip install -r requirements.txt
python setup.py install