import redis

r = redis.Redis(host="localhost", port=6379)

# Сохраняем значение
print("Устанавливаем значение ключа key1=123:")
print(r.set("key1", "123"))

# Получаем значение
print("Получаем значение ключа key1:")
print(r.get("key1"))