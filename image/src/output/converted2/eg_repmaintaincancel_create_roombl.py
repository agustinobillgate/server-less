#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Zimmer

tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool})

def eg_repmaintaincancel_create_roombl(tlocation_list:[Tlocation]):

    prepare_cache ([Zimmer])

    troom_list = []
    zimmer = None

    troom = tlocation = qbuff1 = None

    troom_list, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal troom_list, zimmer


        nonlocal troom, tlocation, qbuff1
        nonlocal troom_list

        return {"troom": troom_list}

    def create_room():

        nonlocal troom_list, zimmer


        nonlocal troom, tlocation, qbuff1
        nonlocal troom_list

        i:int = 0
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Zimmer)
        Qbuff1 = Tlocation
        qbuff1_list = tlocation_list
        troom_list.clear()

        qbuff1 = query(qbuff1_list, filters=(lambda qbuff1: qbuff1.loc_selected  and qbuff1.loc_guest), first=True)

        if qbuff1:

            for qbuff in db_session.query(Qbuff).order_by(Qbuff._recid).all():
                troom = Troom()
                troom_list.append(troom)

                troom.room_nm = qbuff.zinr
                troom.room_selected = False


    create_room()

    return generate_output()