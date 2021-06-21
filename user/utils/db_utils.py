import ast

from user.models import Activity


def from_db_to_dict(resource: Activity, db_dict: dict) -> dict:
    db_dict[resource.id] = {
        "day": resource.day,
        "teacherName": resource.teacher_name,
        "activityType": resource.activity_type,
        "courseName": resource.course_name,
        "timeInterval": resource.time_interval,
        "groups": ast.literal_eval(resource.groups)
    }
    return db_dict
