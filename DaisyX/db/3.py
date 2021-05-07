from DaisyX.services.mongo import mongodb
from DaisyX.utils.logger import log

log.info("Daisy Database v3")
log.info("Support notes aliases")
log.info("Starting updating all notes...")

all_notes = mongodb.notes_v2.find({})
all_notes_count = all_notes.count()
counter = 0
changed_notes = 0
for note in all_notes:
    counter += 1
    log.info(f"Updating {counter} of {all_notes_count}...")

    if "name" in note:
        changed_notes += 1
        names = [note["name"]]
        del note["name"]
        note["names"] = names
        mongodb.notes_v2.replace_one({"_id": note["_id"]}, note)

log.info("Update done!")
log.info("Modified notes - " + str(changed_notes))
log.info("Unchanged notes - " + str(all_notes_count - changed_notes))