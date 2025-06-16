
import redis

# Connexion à Redis via le nom du service Docker (redis)
r = redis.redis(host="redis",port=6379,decode_responses=True)


r.set("yo","nkm")
print(r.get("yo"))