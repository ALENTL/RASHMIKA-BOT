from pymongo import UpdateOne

from DaisyX.services.mongo import mongodb
from DaisyX.utils.logger import log

log.info("Daisy Database v6")
log.info("Filters: migrate 'reply_message'")
log.info("Starting to updating all filters...")

all_filters = mongodb.filters.find({"action": "reply_message"})
count = all_filters.count()
changed = 0
updated_list = []

for i in all_filters:
    if not isinstance(i["reply_text"], dict):
        changed += 1
        log.info(f"Updated {changed} filters of {count}")
        updated_list.append(
            UpdateOne(
                {"_id": i["_id"]},
                {"$set": {"reply_text": {"parse_mode": "md", "text": i["reply_text"]}}},
            )
        )

log.info("Updating Database ...")
if updated_list:
    mongodb.filters.bulk_write(updated_list)