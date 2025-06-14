import hazelcast

# 1) Client’ı oluştur ve ayağa kaldır
client = hazelcast.HazelcastClient()

# 2) Bir map alın, blocking modda çalıştır
hz_map = client.get_map("test-map").blocking()

# 3) Basit bir put/get işlemi yapın
hz_map.put("ping", "pong")
value = hz_map.get("ping")
print("Hazelcast test-map ping→", value)

# 4) Kaynakları kapatın
client.shutdown()
