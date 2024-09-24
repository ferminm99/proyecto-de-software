from sqlalchemy.sql.elements import Null
from app.models.complaint import Complaint
from app.models.followup import FollowUp 
from app.db import db
from sqlalchemy import func

class FollowUpDao:

    @classmethod
    def getAll(cls):
        return FollowUp.query.all()
    
    @classmethod
    def getCount(cls):
        return FollowUp.query.count()
    
    @classmethod
    def getUniqueComplaintsCount(cls):
        list = set()
        for followup in FollowUp.query.all():
            complaint = followup.getComplaint()
            if(complaint != None):
                list.add(int(complaint.getId()))
        print(list)
        set(list)
        print(list)
        return len(list)