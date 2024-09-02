from functions.additional_functions import *
import decimal
from models import Segment

def delete_segmentbl(case_type:int, int1:int, char1:str):
    successflag = False
    segment = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, segment


        return {"successflag": successflag}


    if case_type == 1:

        segment = db_session.query(Segment).filter(
                (Segment.segmentcode == int1)).first()

        if segment:
            db_session.delete(segment)

            successflag = True

    return generate_output()