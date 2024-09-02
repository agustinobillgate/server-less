from functions.additional_functions import *
import decimal
from models import Zimmer
bline_list_list, Bline_list = create_model("Bline_list", {"zinr":str, "selected":bool, "bl_recid":int})


def hk_statadmin_start_chgstatbl(chgsort:int, bline_list:[Bline_list]):
    flag = 0
    t_zinr = ""
    t_zistatus = 0
    zimmer = None

    bline_list = room = None

    print("BLine:", bline_list)

    Room = Zimmer

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, t_zinr, t_zistatus, zimmer
        nonlocal room


        nonlocal bline_list, room
        global bline_list_list
        return {"flag": flag, "t_zinr": t_zinr, "t_zistatus": t_zistatus}

    def start_chgstat():

        nonlocal flag, t_zinr, t_zistatus, zimmer
        nonlocal room


        nonlocal bline_list, room
        global bline_list_list

        anz:int = 0
        answer:bool = False
        Room = Zimmer

        bline_list = query(bline_list_list, filters=(lambda bline_list :bline_list.selected), first=True)

        if not bline_list:
            flag = 1

            return

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zinr == bline_list.zinr)).first()
        t_zinr = zimmer.zinr
        t_zistatus = zimmer.zistatus

        if zimmer.zistatus == 8 and chgsort != 3:
            flag = 2

            return

        if chgsort == 8 and zimmer.zistatus != 4:
            flag = 3

            return

        if chgsort == 5:

            bline_list = query(bline_list_list, filters=(lambda bline_list :bline_list.selected==True), next=True)

            if bline_list:
                flag = 4

                return

            if zimmer.zistatus >= 6 and zimmer.zistatus <= 7:
                flag = 5

                return
        flag = 6


    start_chgstat()

    return generate_output()