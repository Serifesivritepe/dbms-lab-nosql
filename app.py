from flask import Flask, jsonify
import redis
import pymongo
import hazelcast
import json

app = Flask(__name__)

# Redis bağlantısı
rd = redis.Redis(host='localhost', port=6379, db=0)

# MongoDB bağlantısı
mc = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_col = mc["nosql_lab"]["students"]

# Hazelcast bağlantısı
hz = hazelcast.HazelcastClient()
hz_map = hz.get_map("students").blocking()


@app.route("/")
def index():
    return """
    <h1>NoSQL Lab API</h1>
    <p>Örnek öğrenci numarası: <strong>2025000001</strong></p>
    <ul>
      <li><a href="/nosql-lab-rd/student_no=2025000001">Redis: student_no=2025000001</a></li>
      <li><a href="/nosql-lab-mon/student_no=2025000001">MongoDB: student_no=2025000001</a></li>
      <li><a href="/nosql-lab-hz/student_no=2025000001">Hazelcast: student_no=2025000001</a></li>
    </ul>
    """


@app.route("/nosql-lab-rd/student_no=<sn>")
def get_redis(sn):
    raw = rd.get(f"student:{sn}")
    if not raw:
        return jsonify({"error": "Not found"}), 404
    student = json.loads(raw)
    return jsonify(student)


@app.route("/nosql-lab-mon/student_no=<sn>")
def get_mongo(sn):
    student = mongo_col.find_one({"student_no": sn}, {"_id": 0})
    if not student:
        return jsonify({"error": "Not found"}), 404
    return jsonify(student)


@app.route("/nosql-lab-hz/student_no=<sn>")
def get_hz(sn):
    raw = hz_map.get(sn)
    if not raw:
        return jsonify({"error": "Not found"}), 404
    student = json.loads(raw)
    return jsonify(student)


if __name__ == "__main__":
    app.run(port=8080)
