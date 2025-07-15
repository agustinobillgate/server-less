#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Tisch, H_bill

def prepare_ts_helptisch_webbl(dept:int, location:int):

    prepare_cache ([Htparam, Tisch, H_bill])

    tablestr = ""
    max_pos = 0
    t_list_data = []
    htparam = tisch = h_bill = None

    t_list = None

    t_list_data, T_list = create_model("T_list", {"pos":int, "tischnr":int, "beleg":bool, "balance":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tablestr, max_pos, t_list_data, htparam, tisch, h_bill
        nonlocal dept, location


        nonlocal t_list
        nonlocal t_list_data

        return {"tablestr": tablestr, "max_pos": max_pos, "t-list": t_list_data}

    def build_list():

        nonlocal tablestr, max_pos, t_list_data, htparam, tisch, h_bill
        nonlocal dept, location


        nonlocal t_list
        nonlocal t_list_data

        i:int = 0

        for tisch in db_session.query(Tisch).filter(
                 (Tisch.departement == dept) & (Tisch.betriebsnr == location)).order_by(Tisch.tischnr).all():

            h_bill = get_cache (H_bill, {"tischnr": [(eq, tisch.tischnr)],"departement": [(eq, dept)],"flag": [(eq, 0)]})
            i = i + 1
            t_list = T_list()
            t_list_data.append(t_list)

            t_list.pos = i
            t_list.tischnr = tisch.tischnr

            if h_bill:
                t_list.beleg = True
                t_list.balance =  to_decimal(h_bill.saldo)
        max_pos = i


    htparam = get_cache (Htparam, {"paramnr": [(eq, 1007)]})

    if htparam.flogical:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 200)]})

        if htparam.finteger == dept:
            tablestr = "Cabin:"
    build_list()

    return generate_output()