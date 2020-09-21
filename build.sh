git submodule init
git submodule update
cd frontend/ && npm install && npm run build
cd / && npm install && pkg . --out-path=./build/
