with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

max_values = {"red": 12, "green": 13, "blue": 14}

# Q1
good_ids = 0
for line in input_data:
    game_id, game_data = line.split(": ")
    game_id = int(game_id[5:])
    games = game_data.split(";")
    for game in games:
        colors = game.split(", ")
        bad_id = False
        for c in colors:
            number, color_name = c.strip().split(" ")
            if int(number) > max_values[color_name]:
                bad_id = True
                break
        if bad_id:
            break
    if not bad_id:
        good_ids += game_id

print(good_ids)

# Q2
powers = 0
for line in input_data:
    game_id, game_data = line.split(": ")
    game_id = int(game_id[5:])
    draws = game_data.split(";")
    min_colors = {"blue": 0, "red": 0, "green": 0}
    for draw in draws:
        colors = draw.split(", ")
        for c in colors:
            number, color_name = c.strip().split(" ")
            min_colors[color_name] = max(min_colors[color_name], int(number))
    powers += min_colors["red"] * min_colors["green"] * min_colors["blue"]

print(powers)
