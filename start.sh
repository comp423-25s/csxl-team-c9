# run: ./start.sh

pushd frontend
npm install
popd
python3 -m backend.script.create_database
python3 -m backend.script.reset_demo
honcho start