from functions.additional_functions import *
import decimal
from models import Zimmer

def eg_repmaintaincancel_create_roombl(tlocation:[Tlocation]):
    troom_list = []
    zimmer = None

    troom = tlocation = qbuff = qbuff1 = None

    troom_list, Troom = create_model("Troom", {"room_nm":str, "room_selected":bool})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":str, "loc_selected":bool, "loc_guest":bool})

    Qbuff = Zimmer
    Qbuff1 = Tlocation
    qbuff1_list = tlocation_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal troom_list, zimmer
        nonlocal qbuff, qbuff1


        nonlocal troom, tlocation, qbuff, qbuff1
        nonlocal troom_list, tlocation_list
        return {"troom": troom_list}

    def create_room():

        nonlocal troom_list, zimmer
        nonlocal qbuff, qbuff1


        nonlocal troom, tlocation, qbuff, qbuff1
        nonlocal troom_list, tlocation_list

        i:int = 0
        Qbuff = Zimmer
        Qbuff1 = Tlocation
        troom_list.clear()

        qbuff1 = query(qbuff1_list, filters=(lambda qbuff1 :qbuff1.loc_selected  and qbuff1.loc_guest), first=True)

        if qbuff1:

            for qbuff in db_session.query(Qbuff).all():
                troom = Troom()
                troom_list.append(troom)

                troom.room_nm = qbuff.zinr
                troom.room_SELECTED = False

    create_room()

    return generate_output()