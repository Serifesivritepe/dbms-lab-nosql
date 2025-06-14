from faker import Faker
import redis
import pymongo
import hazelcast
import json

fake = Faker()

# Redis’e bağlan
rd = redis.Redis(host='localhost', port=6379, db=0)
# İstersen Redis’i tamamen temizle
rd.flushdb()

# MongoDB’ye bağlan
mc = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mc["nosql_lab"]
mongo_col = mongo_db["students"]
# İstersen MongoDB koleksiyonunu sil
mongo_col.drop()

# Hazelcast’e bağlan
hz_client = hazelcast.HazelcastClient()
hz_map = hz_client.get_map("students").blocking()
# Hazelcast map’ini temizle
hz_map.clear()

BASE = 2025000001
for i in range(10000):
    sn = str(BASE + i)
    student = {
        "student_no": sn,
        "name": fake.name(),
        "department": fake.job()
    }

    # Redis: JSON string olarak sakla
    rd.set(f"student:{sn}", json.dumps(student, default=str))

    # MongoDB
    mongo_col.insert_one(student)

    # Hazelcast: JSON string olarak sakla
    hz_map.put(sn, json.dumps(student, default=str))

hz_client.shutdown()
print("10.000 kayıt her üç veritabanına da yüklendi.")
