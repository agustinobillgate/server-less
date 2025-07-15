#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Zimmer

tlocation_data, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool})

def eg_repmaintaincancel_create_roombl(tlocation_data:[Tlocation]):

    prepare_cache ([Zimmer])

    troom_data = []
    zimmer = None

    troom = tlocation = qbuff1 = None

    troom_data, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal troom_data, zimmer


        nonlocal troom, tlocation, qbuff1
        nonlocal troom_data

        return {"troom": troom_data}

    def create_room():

        nonlocal troom_data, zimmer


        nonlocal troom, tlocation, qbuff1
        nonlocal troom_data

        i:int = 0
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Zimmer)
        Qbuff1 = Tlocation
        qbuff1_data = tlocation_data
        troom_data.clear()

        qbuff1 = query(qbuff1_data, filters=(lambda qbuff1: qbuff1.loc_selected  and qbuff1.loc_guest), first=True)

        if qbuff1:

            for qbuff in db_session.query(Qbuff).order_by(Qbuff._recid).all():
                troom = Troom()
                troom_data.append(troom)

                troom.room_nm = qbuff.zinr
                troom.room_selected = False


    create_room()

    return generate_output()