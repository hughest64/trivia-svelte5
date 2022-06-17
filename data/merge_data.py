import json


output_data = {
    "event_data": {
        "event_id": 65,
        "game_id": 233,
        "game_title": "20220606 - A - Sound",
        "location": "Todd's Garage",
        "join_code": "1154",
        "current_round": "1",
        "current_question": "1",
        "reveal_answers": False,
    },
    "game_data": {"id": 233, "title": "20220606 - A - Sound", "rounds": []},
}

# load game_data.json
with open("game_data.json", "r") as f:
    input_data = json.load(f)
    rounds = input_data.get("rounds", [])

# loop rounds
for round in rounds:
    round["scored"] = False
    round["locked"] = False

    for question in round["questions"]:
        question["question_displayed"] = False
        question["answer_displayed"] = False

    output_data["game_data"]["rounds"].append(round)


# with open("game_data_merged.json", "w") as out_f:
#     json.dump(output_data, out_f)
