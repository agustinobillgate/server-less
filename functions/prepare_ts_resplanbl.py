#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam, Tisch, H_bill

def prepare_ts_resplanbl(curr_dept:int):

    prepare_cache ([Queasy, Htparam, Tisch])

    d_param87 = None
    table_list_data = []
    t_queasy33_data = []
    curr_date:date = None
    queasy = htparam = tisch = h_bill = None

    t_queasy33 = table_list = buf_queasy = None

    t_queasy33_data, T_queasy33 = create_model_like(Queasy, {"rec_id":int})
    table_list_data, Table_list = create_model("Table_list", {"tischnr":int, "belegung":int, "uhrzeit":[string,32], "s_recid":[int,32], "bcol":int, "fcol":int})

    Buf_queasy = create_buffer("Buf_queasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal d_param87, table_list_data, t_queasy33_data, curr_date, queasy, htparam, tisch, h_bill
        nonlocal curr_dept
        nonlocal buf_queasy


        nonlocal t_queasy33, table_list, buf_queasy
        nonlocal t_queasy33_data, table_list_data

        return {"d_param87": d_param87, "table-list": table_list_data, "t-queasy33": t_queasy33_data}

    def create_list():

        nonlocal d_param87, table_list_data, t_queasy33_data, curr_date, queasy, htparam, tisch, h_bill
        nonlocal curr_dept
        nonlocal buf_queasy


        nonlocal t_queasy33, table_list, buf_queasy
        nonlocal t_queasy33_data, table_list_data

        for tisch in db_session.query(Tisch).filter(
                 (Tisch.departement == curr_dept)).order_by(Tisch.tischnr).all():
            table_list = Table_list()
            table_list_data.append(table_list)

            table_list.tischnr = tisch.tischnr
            table_list.belegung = tisch.normalbeleg


            row_disp()


    def row_disp():

        nonlocal d_param87, table_list_data, t_queasy33_data, curr_date, queasy, htparam, tisch, h_bill
        nonlocal curr_dept
        nonlocal buf_queasy


        nonlocal t_queasy33, table_list, buf_queasy
        nonlocal t_queasy33_data, table_list_data

        bcol:int = 12
        fcol:int = 15
        zeit:int = 0

        h_bill = get_cache (H_bill, {"departement": [(eq, curr_dept)],"tischnr": [(eq, tisch.tischnr)],"flag": [(eq, 0)]})

        if h_bill:

            buf_queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, curr_dept)],"number2": [(eq, tisch.tischnr)],"betriebsnr": [(eq, 0)]})

            if buf_queasy:
                zeit = ((get_current_date() - buf_queasy.date1).days) * 86400 + get_current_time_in_seconds() - buf_queasy.number3

                if zeit > 0 and zeit <= 1800:
                    bcol = 14
                    fcol = 0

                elif zeit > 1800 and zeit <= 3600:
                    bcol = 4

                elif zeit > 3600:
                    bcol = 12


            table_list.bcol = bcol
            table_list.fcol = fcol


        else:
            bcol = 0
            fcol = 15


            table_list.bcol = bcol
            table_list.fcol = fcol

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    d_param87 = htparam.fdate
    curr_date = d_param87
    create_list()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 33) & (Queasy.number1 == curr_dept) & (Queasy.date1 == curr_date) & (Queasy.logi2 == False) & (Queasy.logi3) & (Queasy.betriebsnr == 0)).order_by(Queasy._recid).all():
        t_queasy33 = T_queasy33()
        t_queasy33_data.append(t_queasy33)

        buffer_copy(queasy, t_queasy33)
        t_queasy33.rec_id = queasy._recid

    return generate_output()