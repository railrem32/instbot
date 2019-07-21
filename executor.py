import db
import inst


def updateStatus(task,status):
    db.update_task_status(task.get(db.FIELD_TARGET_USER), task.get(db.FIELD_USER_ID), status)

def run():
    task = db.get_first_new_tasks()
    if task is None:
        return
    try:
        updateStatus(task, db.CONST_STATUS_INPROCESS)
        inst.follow_and_like(task)
        updateStatus(task, db.CONST_STATUS_FINISHED)
    except Exception:
        updateStatus(task, db.CONST_STATUS_FAILED)
'''
while(True):
    task = db.get_first_new_tasks()
    if task is None:
        time.sleep(1000)
        continue
    try:
        updateStatus(task,db.CONST_STATUS_INPROCESS)
        inst.follow_and_like(task)
        updateStatus(task,db.CONST_STATUS_FINISHED)
    except Exception :
        updateStatus(task,db.CONST_STATUS_FAILED)
        continue
'''




