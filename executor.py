import db
import inst


def updateStatus(task,status):
    db.update_task_status(task.get(db.FIELD_TARGET_USER), task.get(db.FIELD_USER_ID), status)

def run(isLikes=False,photos=0,likers=0,isUnfollow=False):
    task = db.get_first_new_tasks()
    if task is None:
        return "Нету заданий"
    try:
        updateStatus(task, db.CONST_STATUS_INPROCESS)
        if (isLikes):
            inst.follow_likers(task,photos,likers)
        else :
            if (isUnfollow):
                inst.unfollow(task)
            else :
                inst.follow_and_like(task)
        updateStatus(task, db.CONST_STATUS_FINISHED)
    except Exception as e:
        updateStatus(task, db.CONST_STATUS_FAILED)
        return "Че то поломалось "+ str(e)
    return None




