#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_maintain

def eg_maincalendardel_deletebl(smaintain_maintainnr:int):
    msgint = 0
    eg_maintain = None

    buf_maintain = None

    Buf_maintain = create_buffer("Buf_maintain",Eg_maintain)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msgint, eg_maintain
        nonlocal smaintain_maintainnr
        nonlocal buf_maintain


        nonlocal buf_maintain

        return {"msgint": msgint}


    buf_maintain = db_session.query(Buf_maintain).filter(
             (Buf_maintain.maintainnr == smaintain_maintainnr) & (Buf_maintain.delete_flag)).first()

    if buf_maintain:
        db_session.delete(buf_maintain)
        pass
        msgint = 1

    return generate_output()