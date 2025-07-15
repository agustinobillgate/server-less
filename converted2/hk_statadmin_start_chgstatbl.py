#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Zimmer

bline_list_data, Bline_list = create_model("Bline_list", {"zinr":string, "selected":bool, "bl_recid":int})

def hk_statadmin_start_chgstatbl(chgsort:int, bline_list_data:[Bline_list]):

    prepare_cache ([Zimmer])

    flag = 0
    t_zinr = ""
    t_zistatus = 0
    zimmer = None

    bline_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, t_zinr, t_zistatus, zimmer
        nonlocal chgsort


        nonlocal bline_list

        return {"flag": flag, "t_zinr": t_zinr, "t_zistatus": t_zistatus}

    def start_chgstat():

        nonlocal flag, t_zinr, t_zistatus, zimmer
        nonlocal chgsort


        nonlocal bline_list

        anz:int = 0
        answer:bool = False
        room = None
        Room =  create_buffer("Room",Zimmer)

        bline_list = query(bline_list_data, filters=(lambda bline_list: bline_list.selected), first=True)

        if not bline_list:
            flag = 1

            return

        zimmer = get_cache (Zimmer, {"zinr": [(eq, bline_list.zinr)]})
        t_zinr = zimmer.zinr
        t_zistatus = zimmer.zistatus

        if zimmer.zistatus == 8 and chgsort != 3:
            flag = 2

            return

        if chgsort == 8 and zimmer.zistatus != 4:
            flag = 3

            return

        if chgsort == 5:

            bline_list = query(bline_list_data, filters=(lambda bline_list: bline_list.selected), next=True)

            if bline_list:
                flag = 4

                return

            if zimmer.zistatus >= 6 and zimmer.zistatus <= 7:
                flag = 5

                return
        flag = 6

    start_chgstat()

    return generate_output()