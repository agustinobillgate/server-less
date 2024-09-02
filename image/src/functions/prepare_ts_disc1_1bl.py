from functions.additional_functions import *
import decimal
from models import H_bill_line, Htparam, Waehrung, H_bill

def prepare_ts_disc1_1bl(dept:int, tischnr:int):
    price_decimal = 0
    exchg_rate = 0
    p_134 = False
    p_135 = False
    p_479 = False
    t_h_bill_line_list = []
    h_bill_line = htparam = waehrung = h_bill = None

    t_h_bill_line = None

    t_h_bill_line_list, T_h_bill_line = create_model_like(H_bill_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, exchg_rate, p_134, p_135, p_479, t_h_bill_line_list, h_bill_line, htparam, waehrung, h_bill


        nonlocal t_h_bill_line
        nonlocal t_h_bill_line_list
        return {"price_decimal": price_decimal, "exchg_rate": exchg_rate, "p_134": p_134, "p_135": p_135, "p_479": p_479, "t-h-bill-line": t_h_bill_line_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if waehrung:
        exchg_rate = waehrung.ankauf / waehrung.einheit
    else:
        exchg_rate = 1

    h_bill = db_session.query(H_bill).filter(
            (H_bill.departement == dept) &  (H_bill.tischnr == tischnr) &  (H_bill.flag == 0)).first()

    for h_bill_line in db_session.query(H_bill_line).filter(
            (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == dept)).all():
        t_h_bill_line = T_h_bill_line()
        t_h_bill_line_list.append(t_h_bill_line)

        buffer_copy(h_bill_line, t_h_bill_line)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 134)).first()
    p_134 = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 135)).first()
    p_135 = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 479)).first()
    p_479 = htparam.flogical

    return generate_output()