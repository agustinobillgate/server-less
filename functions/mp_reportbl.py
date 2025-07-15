#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener

def mp_reportbl(reporttype:int):

    prepare_cache ([Bediener])

    t_master_data = []
    t_bk_queasy_data = []
    t_bediener_data = []
    bediener = None

    t_master = t_master1 = t_bk_queasy = t_bediener = None

    t_master_data, T_master = create_model("T_master", {"resnr":int, "gastnr":int, "name":string, "startdate":date, "enddate":date, "resstatus":int, "market_nr":int, "source_nr":int, "sales_nr":int, "restype":int, "origins":int, "sob":int, "catering_flag":bool, "room_flag":bool, "cancel_flag":[bool,2], "cancel_type":string, "cancel_reason":string, "cancel_destination":string, "cancel_property":string, "res_character":[string,9], "res_int":[int,9], "res_dec":[Decimal,9], "block_id":string, "block_code":string, "reservation_method":string, "rooming_list_due":date, "arrival_time":int, "departure_time":int, "payment":string, "cancel_penalty":Decimal})
    t_master1_data, T_master1 = create_model_like(T_master)
    t_bk_queasy_data, T_bk_queasy = create_model("T_bk_queasy", {"key":int, "number1":int, "number2":int, "number3":int, "date1":date, "date2":date, "date3":date, "char1":string, "char2":string, "char3":string, "deci1":Decimal, "deci2":Decimal, "deci3":Decimal, "logi1":bool, "logi2":bool, "logi3":bool, "betriebsnr":int})
    t_bediener_data, T_bediener = create_model("T_bediener", {"nr":int, "username":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_master_data, t_bk_queasy_data, t_bediener_data, bediener
        nonlocal reporttype


        nonlocal t_master, t_master1, t_bk_queasy, t_bediener
        nonlocal t_master_data, t_master1_data, t_bk_queasy_data, t_bediener_data

        return {"t-master": t_master_data, "t-bk-queasy": t_bk_queasy_data, "t-bediener": t_bediener_data}


    for bk_master in query(bk_master_data):
        t_master = T_master()
        t_master_data.append(t_master)

        buffer_copy(bk_master, t_master)

    for t_master in query(t_master_data):

        bk_queasy = db_session.query(Bk_queasy).filter(
                 (Bk_queasy.key == 1) & (Bk_queasy.number1 == t_master.resstatus)).first()

        if bk_queasy:
            t_master.resstatus = bk_queasy.number2

    if reporttype == 1:

        for t_master in query(t_master_data, filters=(lambda t_master: t_master.resstatus != 6)):
            t_master_data.remove(t_master)

    elif reporttype == 2:

        for t_master in query(t_master_data, filters=(lambda t_master: t_master.resstatus != 7)):
            t_master_data.remove(t_master)

    for bk_queasy in query(bk_queasy_data):
        t_bk_queasy = T_bk_queasy()
        t_bk_queasy_data.append(t_bk_queasy)

        buffer_copy(bk_queasy, t_bk_queasy)

    for bediener in db_session.query(Bediener).order_by(Bediener._recid).all():
        t_bediener = T_bediener()
        t_bediener_data.append(t_bediener)

        t_bediener.nr = bediener.nr
        t_bediener.username = bediener.username

    return generate_output()