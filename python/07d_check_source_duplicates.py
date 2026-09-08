import json
import os

FILE_PATH = "../cricsheet_json/1527678.json"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    match = json.load(f)

for innings_no, innings in enumerate(match.get("innings", []), start=1):

    for over in innings.get("overs", []):

        for delivery in over.get("deliveries", []):

            actual_delivery = delivery.get("actual_delivery")

            if actual_delivery == "0.2":

                print("Innings:", innings_no)
                print("Over:", over.get("over"))
                print("Delivery:")
                print(delivery)
                print("-" * 60)