from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import Res_line

def update_mainres_listbl(mainres_list:[Mainres_list]):
    ci_date:date = None
    res_line = None

    mainres_list = None

    mainres_list_list, Mainres_list = create_model("Mainres_list", {"resnr":int, "zimanz":int, "ankunft":date, "abreise":date, "segm":int, "deposit":decimal, "until":date, "paid":decimal, "id1":str, "id2":str, "id2_date":date, "groupname":str, "grpflag":bool, "bemerk":str, "voucher":str, "vesrdepot2":str, "arrival":bool, "resident":bool, "arr_today":bool}, {"ankunft": 01/01/2099, "abreise": 01/01/1998})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, res_line


        nonlocal mainres_list
        nonlocal mainres_list_list
        return {}

    def update_mainres():

        nonlocal ci_date, res_line


        nonlocal mainres_list
        nonlocal mainres_list_list


        mainres_list.ankunft = 01/01/2099
        mainres_list.abreise = 01/01/1998
        mainres_list.zimanz = 0
        mainres_list.arrival = False
        mainres_list.arr_today = False
        mainres_list.resident = False

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == mainres_list.resnr) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12)).all():

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