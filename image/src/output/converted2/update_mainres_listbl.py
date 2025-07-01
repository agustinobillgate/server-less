#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Res_line

mainres_list_list, Mainres_list = create_model("Mainres_list", {"resnr":int, "zimanz":int, "ankunft":date, "abreise":date, "segm":int, "deposit":Decimal, "until":date, "paid":Decimal, "id1":string, "id2":string, "id2_date":date, "groupname":string, "grpflag":bool, "bemerk":string, "voucher":string, "vesrdepot2":string, "arrival":bool, "resident":bool, "arr_today":bool}, {"ankunft": date_mdy(1, 1, 2099), "abreise": date_mdy(1, 1, 1998)})

def update_mainres_listbl(mainres_list_list:[Mainres_list]):

    prepare_cache ([Res_line])

    ci_date:date = None
    res_line = None

    mainres_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, res_line


        nonlocal mainres_list

        return {"mainres-list": mainres_list_list}

    def update_mainres():

        nonlocal ci_date, res_line


        nonlocal mainres_list


        mainres_list.ankunft = date_mdy(1, 1, 2099)
        mainres_list.abreise = date_mdy(1, 1, 1998)
        mainres_list.zimanz = 0
        mainres_list.arrival = False
        mainres_list.arr_today = False
        mainres_list.resident = False

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == mainres_list.resnr) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12)).order_by(Res_line._recid).all():

            if res_line.resstatus <= 6:
                mainres_list.zimanz = mainres_list.zimanz + res_line.zimmeranz

            if mainres_list.ankunft > res_line.ankunft:
                mainres_list.ankunft = res_line.ankunft

            if mainres_list.abreise < res_line.abreise:
                mainres_list.abreise = res_line.abreise

            if (res_line.resstatus <= 5 or res_line.resstatus == 11):
                mainres_list.arrival = True

            if mainres_list.arrival  and res_line.ankunft == ci_date:
                mainres_list.arr_today = True

            if res_line.resstatus == 6 or res_line.resstatus == 13:
                mainres_list.resident = True

    ci_date = get_output(htpdate(87))

    mainres_list = query(mainres_list_list, first=True)
    update_mainres()

    return generate_output()