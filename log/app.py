from datetime import datetime, timezone

from flask import Flask, jsonify, request, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

licznik = Counter("log_attempts", "Liczba prob sprawdzenia hasla", ["found"])

@app.post("/log")
def log_attempt():
    data = request.get_json(silent=True) or {}
    found_bool = bool(data.get("found"))

    # Zwiększenie licznika z odpowiednią etykietą
    found_label = "true" if found_bool else "false"
    licznik.labels(found=found_label).inc()

    # Tylko metadane próby - usługa log nie dostaje pełnego skrótu, hasła ani dostępu do bazy
    entry = {
        "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "hash_prefix": str(data.get("hash_prefix", ""))[:5],
        "found": bool(data.get("found")),
    }
    print(f"log: {entry}", flush=True)
    return jsonify({"status": "logged"}), 201

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype = CONTENT_TYPE_LATEST)