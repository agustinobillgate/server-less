from functions.additional_functions import *
import decimal
from datetime import date
from models import Queasy

def prepare_bookengine_ratecodepullbl(bookengid:int):
    bookeng_name = ""
    t_pull_list_list = []
    t_ratecode_list_list = []
    queasy = None

    t_pull_list = temp_rate_list = sum_list = room_list = t_pull_ratecode = t_ratecode_list = quecateg = None

    t_pull_list_list, T_pull_list = create_model("T_pull_list", {"rcodevhp":str, "rcodebe":str, "rmtypevhp":str, "rmtypebe":str, "argtvhp":str, "flag":int})
    temp_rate_list_list, Temp_rate_list = create_model("Temp_rate_list", {"room_type":str, "room_categ":str, "dcode":str, "scode":str, "currency":str, "dydatum_str":str, "dmdatum_str":str, "dtdatum_str":str, "argt_str":str})
    sum_list_list, Sum_list = create_model("Sum_list", {"allot_flag":bool, "bezeich":str, "summe":[int, 30]})
    room_list_list, Room_list = create_model("Room_list", {"avail_flag":bool, "allot_flag":bool, "zikatnr":int, "i_typ":int, "sleeping":bool, "allotment":[int, 30], "bezeich":str, "room":[int, 30], "coom":[str, 30], "rmrate":[decimal, 30], "currency":int, "wabkurz":str, "i_counter":int, "rateflag":bool, "adult":int, "child":int, "prcode":[str, 30], "rmcat":str, "argt":str, "rcode":str, "segmentcode":str, "dynarate":bool, "expired":bool, "argt_remark":str, "minstay":int, "maxstay":int, "minadvance":int, "maxadvance":int, "frdate":date, "todate":date, "marknr":int, "datum":[date, 30]}, {"sleeping": True, "frdate": None, "todate": None})
    t_pull_ratecode_list, T_pull_ratecode = create_model("T_pull_ratecode", {"rcodevhp":str, "rcodebe":str, "rmtypevhp":str, "rmtypebe":str, "argtvhp":str})
    t_ratecode_list_list, T_ratecode_list = create_model_like(Queasy, {"selected":bool}, {"selected": True})

    Quecateg = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bookeng_name, t_pull_list_list, t_ratecode_list_list, queasy
        nonlocal quecateg


        nonlocal t_pull_list, temp_rate_list, sum_list, room_list, t_pull_ratecode, t_ratecode_list, quecateg
        nonlocal t_pull_list_list, temp_rate_list_list, sum_list_list, room_list_list, t_pull_ratecode_list, t_ratecode_list_list
        return {"bookeng_name": bookeng_name, "t-pull-list": t_pull_list_list, "t-ratecode-list": t_ratecode_list_list}


    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 163) &  (Queasy.number1 == bookengid)).all():
        t_pull_list = T_pull_list()
        t_pull_list_list.append(t_pull_list)

        t_pull_list.rcodeVHP = entry(0, queasy.char1, ";")
        t_pull_list.rcodeBE = entry(1, queasy.char1, ";")
        t_pull_list.rmtypeVHP = entry(2, queasy.char1, ";")
        t_pull_list.rmtypeBE = entry(3, queasy.char1, ";")
        t_pull_list.argtVHP = entry(4, queasy.char1, ";")

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 2)).all():
        t_ratecode_list = T_ratecode_list()
        t_ratecode_list_list.append(t_ratecode_list)

        buffer_copy(queasy, t_ratecode_list)

    return generate_output()