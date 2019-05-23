import redis

db = redis.Redis(host='localhost', port=6379, db=0)

class Clue():
    def allowed_to_buzz():
        response = db.hget("clue", "buzzable")
        if response and response.decode() == "False":
            return False
        return True

    def allow_buzzer():
        db.hset("clue", "buzzable", "True")

    def disallow_buzzer():
        db.hset("clue", "buzzable", "False")

class Player():
    def all_buzzed_players():
        length = db.llen("buzzed_player")
        return [(db.lindex("buzzed_player", index)).decode() for index in range(length)]

    def add_buzzed_player(player):
        db.rpush("buzzed_player", player)

    def get_first_buzzed_player():
        return (db.lindex("buzzed_player", 0)).decode()

    def clear_buzzed_players():
        db.delete("buzzed_player")

    def get_all_players():
        return {key.decode():value.decode() for key, value in (db.hgetall("player")).items()}

    def get_player_name(hostname):
        player = db.hget("player", hostname)
        if player:
            return player.decode()

    def add_player(hostname, player):
        db.hset("player", hostname, player)

class Points():
    def adjust_points(hostname, new_points):
        old_points = db.hget("points", hostname)
        if old_points:
            old_points = int(old_points.decode())
            new_points += old_points
        db.hset("points", hostname, new_points)

    def get_points(hostname):
        points = db.hget("points", hostname)
        if points:
            return points.decode()
