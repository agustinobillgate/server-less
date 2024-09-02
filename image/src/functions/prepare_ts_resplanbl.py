from functions.additional_functions import *
import decimal
from datetime import date
from models import Queasy, Htparam, Tisch, H_bill

def prepare_ts_resplanbl(curr_dept:int):
    d_param87 = None
    table_list_list = []
    t_queasy33_list = []
    curr_date:date = None
    queasy = htparam = tisch = h_bill = None

    t_queasy33 = table_list = buf_queasy = None

    t_queasy33_list, T_queasy33 = create_model_like(Queasy, {"rec_id":int})
    table_list_list, Table_list = create_model("Table_list", {"tischnr":int, "belegung":int, "uhrzeit":[str, 32], "s_recid":[int, 32], "bcol":int, "fcol":int})

    Buf_queasy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal d_param87, table_list_list, t_queasy33_list, curr_date, queasy, htparam, tisch, h_bill
        nonlocal buf_queasy


        nonlocal t_queasy33, table_list, buf_queasy
        nonlocal t_queasy33_list, table_list_list
        return {"d_param87": d_param87, "table-list": table_list_list, "t-queasy33": t_queasy33_list}

    def create_list():

        nonlocal d_param87, table_list_list, t_queasy33_list, curr_date, queasy, htparam, tisch, h_bill
        nonlocal buf_queasy


        nonlocal t_queasy33, table_list, buf_queasy
        nonlocal t_queasy33_list, table_list_list

        for tisch in db_session.query(Tisch).filter(
                (Tisch.departement == curr_dept)).all():
            table_list = Table_list()
            table_list_list.append(table_list)

            table_list.tischnr = tischnr
            table_list.belegung = tisch.normalbeleg


            row_disp()

    def row_disp():

        nonlocal d_param87, table_list_list, t_queasy33_list, curr_date, queasy, htparam, tisch, h_bill
        nonlocal buf_queasy


        nonlocal t_queasy33, table_list, buf_queasy
        nonlocal t_queasy33_list, table_list_list

        bcol:int = 12
        fcol:int = 15
        zeit:int = 0

        h_bill = db_session.query(H_bill).filter(
                (H_bill.departement == curr_dept) &  (H_bill.tischnr == tischnr) &  (H_bill.flag == 0)).first()

        if h_bill:

            buf_queasy = db_session.query(Buf_queasy).filter(
                    (Buf_queasy.key == 31) &  (Buf_queasy.number1 == curr_dept) &  (Buf_queasy.number2 == tischnr) &  (Buf_queasy.betriebsnr == 0)).first()

            if buf_queasy:
                zeit = (get_current_date() - buf_queasy.date1) * 86400 + get_current_time_in_seconds() - buf_queasy.number3

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


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    d_param87 = htparam.fdate
    curr_date = d_param87
    create_list()

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 33) &  (Queasy.number1 == curr_dept) &  (Queasy.date1 == curr_date) &  (Queasy.logi2 == False) &  (Queasy.logi3) &  (Queasy.betriebsnr == 0)).all():
        t_queasy33 = T_queasy33()
        t_queasy33_list.append(t_queasy33)

        buffer_copy(queasy, t_queasy33)
        t_queasy33.rec_id = queasy._recid

    return generate_output()