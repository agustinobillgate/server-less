from functions.additional_functions import *
import decimal
from functions.htpdec import htpdec
from models import Guest, Bill, Res_line, Queasy

def prepare_ts_pguestbl():
    pguest_list_list = []
    d_klimit:decimal = 0
    guest = bill = res_line = queasy = None

    pguest_list = None

    pguest_list_list, Pguest_list = create_model("Pguest_list", {"ankunft":date, "abreise":date, "nation1":str, "zinr":str, "gname":str, "pin_code":str, "kreditlimit":decimal, "saldo":decimal, "s_recid":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal pguest_list_list, d_klimit, guest, bill, res_line, queasy


        nonlocal pguest_list
        nonlocal pguest_list_list
        return {"pguest-list": pguest_list_list}


    d_klimit = get_output(htpdec(68))

    res_line_obj_list = []
    for res_line, guest, bill in db_session.query(Res_line, Guest, Bill).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).join(Bill,(Bill.resnr == Res_line.resnr) &  (Bill.reslinnr == Res_line.reslinnr)).filter(
            (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.l_zuordnung[2] == 0)).all():
        if res_line._recid in res_line_obj_list:
            continue
        else:
            res_line_obj_list.append(res_line._recid)


        pguest_list = Pguest_list()
        pguest_list_list.append(pguest_list)

        pguest_list.zinr = res_line.zinr
        pguest_list.ankunft = res_line.ankunft
        pguest_list.abreise = res_line.abreise
        pguest_list.gname = res_line.name
        pguest_list.nation1 = guest.nation1
        pguest_list.kreditlimit = guest.kreditlimit
        pguest_list.pin_code = ";" + res_line.pin_code + ";"
        pguest_list.s_recid = to_int(res_line._recid)

        if pguest_list.kreditlimit == 0:
            pguest_list.kreditlimit = d_klimit

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 16) &  (Queasy.number1 == res_line.resnr) &  (Queasy.number2 == res_line.reslinnr)).all():
            pguest_list.pin_code = pguest_list.pin_code + ";" + queasy.char1 + ";"

    return generate_output()