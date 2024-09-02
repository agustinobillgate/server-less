from functions.additional_functions import *
import decimal
from models import H_bill_line, H_bill, H_umsatz, Queasy

def ts_closeinv_btn_stopbl(t_p_list:[T_p_list], rec_id:int, pax:int, belegung:int):
    h_bill_line = h_bill = h_umsatz = queasy = None

    t_p_list = hbline = None

    t_p_list_list, T_p_list = create_model("T_p_list", {"rechnr":int, "dept":int, "billno":int, "printed_line":int, "b_recid":int, "last_amount":decimal, "last_famount":decimal})

    Hbline = H_bill_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill_line, h_bill, h_umsatz, queasy
        nonlocal hbline


        nonlocal t_p_list, hbline
        nonlocal t_p_list_list
        return {}

    def del_queasy():

        nonlocal h_bill_line, h_bill, h_umsatz, queasy
        nonlocal hbline


        nonlocal t_p_list, hbline
        nonlocal t_p_list_list

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 4) &  (Queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) &  (Queasy.number2 >= 0) &  (Queasy.deci2 >= 0)).all():
            db_session.delete(queasy)

        for t_p_list in query(t_p_list_list, filters=(lambda t_p_list :t_p_list.rechnr == h_bill.rechnr and t_p_list.dept == h_bill.departement)):
            t_p_list_list.remove(t_p_list)

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id)).first()

    if pax != belegung:

        hbline = db_session.query(Hbline).filter(
                (Hbline.rechnr == h_bill.rechnr) &  (Hbline.departement == h_bill.departement)).first()

        if hbline:

            h_umsatz = db_session.query(H_umsatz).filter(
                    (H_umsatz.artnr == 0) &  (H_umsatz.departement == h_bill.departement) &  (H_umsatz.betriebsnr == h_bill.departement) &  (H_umsatz.datum == hbline.bill_datum)).first()

            if h_umsatz:
                h_umsatz.anzahl = h_umsatz.anzahl -\
                        h_bill.belegung + pax

                h_umsatz = db_session.query(H_umsatz).first()

        h_bill = db_session.query(H_bill).first()

        if h_bill:
            h_bill.belegung = pax

            h_bill = db_session.query(H_bill).first()
    del_queasy()

    return generate_output()