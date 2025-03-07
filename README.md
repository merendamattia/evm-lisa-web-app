# Run the EVMLiSA web app
Start the web-app:
```bash
docker compose up --build -d
```
then, you will be able to use the web-app at [http://localhost](http://localhost:5173/).

Stop the web-app:
```bash
docker compose down
```

---

# Debugging mode
## Start the backend
From a new bash, run:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip3 install -r app/requirements.txt
python3 run.py
```

## Start the frontend
From a new bash, run:
```bash
cd frontend
npm install
npm run dev
```

then, you will be able to use the web-app at [http://localhost](http://localhost:5173/).
