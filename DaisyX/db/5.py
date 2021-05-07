from pymongo import InsertOne

from DaisyX.services.mongo import mongodb
from DaisyX.utils.logger import log

log.info("Daisy Database v5")
log.info("Feds: migrate to old feds database structure")
log.info("Starting updating all feds...")

all_feds = mongodb.feds.find({})
all_feds_count = all_feds.count()
counter = 0
changed_feds = 0
for fed in all_feds:
    counter += 1
    log.info(f"Updating {counter} of {all_feds_count}...")

    queue = []
    if "banned" not in fed:
        continue

    for item in fed["banned"].items():
        user_id = item[0]
        ban = item[1]
        new = {
            "fed_id": fed["fed_id"],
            "user_id": user_id,
            "by": ban["by"],
            "time": ban["time"],
        }

        if "reason" in ban:
            new["reason"] = ban["reason"]

        if "banned_chats" in ban:
            new["banned_chats"] = ban["banned_chats"]

        queue.append(InsertOne(new))

    mongodb.fed_bans.bulk_write(queue)
    mongodb.feds.update_one({"fed_id": fed["fed_id"]}, {"$unset": {"banned": 1}})
    changed_feds += 1

log.info("Update done!")
log.info("Modified feds - " + str(changed_feds))
log.info("Unchanged feds - " + str(all_feds_count - changed_feds))