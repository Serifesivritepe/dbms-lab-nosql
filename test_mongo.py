from pymongo import MongoClient

# MongoDB servisi localhost:27017 üzerinde çalışıyor
client = MongoClient("mongodb://localhost:27017/")

# Ping atıp sonucu yazdır
result = client.admin.command("ping")
print("MongoDB ping response:", result)
