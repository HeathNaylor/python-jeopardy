import redis

db = redis.Redis(host='localhost', port=6379, db=0)

class Clue():
    def allowed_to_buzz():
        response = db.hget("clue", "buzzable")
        if response.decode() == "False":
            return False
        return True

    def allow_buzzer():
        db.hset("clue", "buzzable", "True")

    def disallow_buzzer():
        db.hset("clue", "buzzable", "False")
