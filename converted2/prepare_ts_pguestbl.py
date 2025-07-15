#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.htpdec import htpdec
from models import Guest, Bill, Res_line, Queasy

def prepare_ts_pguestbl():

    prepare_cache ([Guest, Res_line, Queasy])

    pguest_list_data = []
    d_klimit:Decimal = to_decimal("0.0")
    guest = bill = res_line = queasy = None

    pguest_list = None

    pguest_list_data, Pguest_list = create_model("Pguest_list", {"ankunft":date, "abreise":date, "nation1":string, "zinr":string, "gname":string, "pin_code":string, "kreditlimit":Decimal, "saldo":Decimal, "s_recid":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pguest_list_data, d_klimit, guest, bill, res_line, queasy


        nonlocal pguest_list
        nonlocal pguest_list_data

        return {"pguest-list": pguest_list_data}


    d_klimit = get_output(htpdec(68))

    res_line_obj_list = {}
    for res_line, guest, bill in db_session.query(Res_line, Guest, Bill).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).join(Bill,(Bill.resnr == Res_line.resnr) & (Bill.reslinnr == Res_line.reslinnr)).filter(
             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.zinr, Res_line.name).all():
        if res_line_obj_list.get(res_line._recid):
            continue
        else:
            res_line_obj_list[res_line._recid] = True


        pguest_list = Pguest_list()
        pguest_list_data.append(pguest_list)

        pguest_list.zinr = res_line.zinr
        pguest_list.ankunft = res_line.ankunft
        pguest_list.abreise = res_line.abreise
        pguest_list.gname = res_line.name
        pguest_list.nation1 = guest.nation1
        pguest_list.kreditlimit =  to_decimal(guest.kreditlimit)
        pguest_list.pin_code = ";" + res_line.pin_code + ";"
        pguest_list.s_recid = to_int(res_line._recid)

        if pguest_list.kreditlimit == 0:
            pguest_list.kreditlimit =  to_decimal(d_klimit)

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 16) & (Queasy.number1 == res_line.resnr) & (Queasy.number2 == res_line.reslinnr)).order_by(Queasy._recid).all():
            pguest_list.pin_code = pguest_list.pin_code + ";" + queasy.char1 + ";"

    return generate_output()