from DaisyX.services.mongo import mongodb
from DaisyX.utils.logger import log

log.info("Daisy Database v4")
log.info("Filters: move 'note' to 'note_name'")
log.info("Starting updating all filters...")

all_filters = mongodb.filters.find({})
all_filters_count = all_filters.count()
counter = 0
changed_filters = 0
for item in all_filters:
    counter += 1
    log.info(f"Updating {counter} of {all_filters_count}...")

    if "note" in item:
        changed_filters += 1
        item["note_name"] = item["note"]
        del item["note"]
        mongodb.notes_v2.replace_one({"_id": item["_id"]}, item)

log.info("Update done!")
log.info("Modified filters - " + str(changed_filters))
log.info("Unchanged filters - " + str(all_filters_count - changed_filters))