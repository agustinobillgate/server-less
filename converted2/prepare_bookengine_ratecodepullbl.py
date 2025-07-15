#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

def prepare_bookengine_ratecodepullbl(bookengid:int):
    bookeng_name = ""
    t_pull_list_data = []
    t_ratecode_list_data = []
    queasy = None

    t_pull_list = temp_rate_list = sum_list = room_list = t_pull_ratecode = t_ratecode_list = quecateg = None

    t_pull_list_data, T_pull_list = create_model("T_pull_list", {"rcodevhp":string, "rcodebe":string, "rmtypevhp":string, "rmtypebe":string, "argtvhp":string, "flag":int})
    temp_rate_list_data, Temp_rate_list = create_model("Temp_rate_list", {"room_type":string, "room_categ":string, "dcode":string, "scode":string, "currency":string, "dydatum_str":string, "dmdatum_str":string, "dtdatum_str":string, "argt_str":string})
    sum_list_data, Sum_list = create_model("Sum_list", {"allot_flag":bool, "bezeich":string, "summe":[int,30]})
    room_list_data, Room_list = create_model("Room_list", {"avail_flag":bool, "allot_flag":bool, "zikatnr":int, "i_typ":int, "sleeping":bool, "allotment":[int,30], "bezeich":string, "room":[int,30], "coom":[string,30], "rmrate":[Decimal,30], "currency":int, "wabkurz":string, "i_counter":int, "rateflag":bool, "adult":int, "child":int, "prcode":[string,30], "rmcat":string, "argt":string, "rcode":string, "segmentcode":string, "dynarate":bool, "expired":bool, "argt_remark":string, "minstay":int, "maxstay":int, "minadvance":int, "maxadvance":int, "frdate":date, "todate":date, "marknr":int, "datum":[date,30]}, {"sleeping": True, "frdate": None, "todate": None})
    t_pull_ratecode_data, T_pull_ratecode = create_model("T_pull_ratecode", {"rcodevhp":string, "rcodebe":string, "rmtypevhp":string, "rmtypebe":string, "argtvhp":string})
    t_ratecode_list_data, T_ratecode_list = create_model_like(Queasy, {"selected":bool}, {"selected": True})

    Quecateg = create_buffer("Quecateg",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bookeng_name, t_pull_list_data, t_ratecode_list_data, queasy
        nonlocal bookengid
        nonlocal quecateg


        nonlocal t_pull_list, temp_rate_list, sum_list, room_list, t_pull_ratecode, t_ratecode_list, quecateg
        nonlocal t_pull_list_data, temp_rate_list_data, sum_list_data, room_list_data, t_pull_ratecode_data, t_ratecode_list_data

        return {"bookeng_name": bookeng_name, "t-pull-list": t_pull_list_data, "t-ratecode-list": t_ratecode_list_data}


    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 163) & (Queasy.number1 == bookengid)).order_by(Queasy._recid).all():
        t_pull_list = T_pull_list()
        t_pull_list_data.append(t_pull_list)

        t_pull_list.rcodevhp = entry(0, queasy.char1, ";")
        t_pull_list.rcodebe = entry(1, queasy.char1, ";")
        t_pull_list.rmtypevhp = entry(2, queasy.char1, ";")
        t_pull_list.rmtypebe = entry(3, queasy.char1, ";")
        t_pull_list.argtvhp = entry(4, queasy.char1, ";")

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 2)).order_by(Queasy._recid).all():
        t_ratecode_list = T_ratecode_list()
        t_ratecode_list_data.append(t_ratecode_list)

        buffer_copy(queasy, t_ratecode_list)

    return generate_output()