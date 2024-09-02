from functions.additional_functions import *
import decimal
from models import H_artikel, H_bill_line, Htparam

def ts_restinv_cancel_orderbl(h_bline_rec_id:int, zugriff:bool):
    fl_code = 0
    fl_code1 = 0
    fl_code2 = 0
    fl_code3 = 0
    qty = 0
    answer = False
    cancel_flag = False
    billart = 0
    description = ""
    price = 0
    rec_id_h_art = 0
    anz = 0
    t_h_artikel_list = []
    h_artikel = h_bill_line = htparam = None

    t_h_artikel = h_art = hbline = None

    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})

    H_art = H_artikel
    Hbline = H_bill_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, fl_code1, fl_code2, fl_code3, qty, answer, cancel_flag, billart, description, price, rec_id_h_art, anz, t_h_artikel_list, h_artikel, h_bill_line, htparam
        nonlocal h_art, hbline


        nonlocal t_h_artikel, h_art, hbline
        nonlocal t_h_artikel_list
        return {"fl_code": fl_code, "fl_code1": fl_code1, "fl_code2": fl_code2, "fl_code3": fl_code3, "qty": qty, "answer": answer, "cancel_flag": cancel_flag, "billart": billart, "description": description, "price": price, "rec_id_h_art": rec_id_h_art, "anz": anz, "t-h-artikel": t_h_artikel_list}

    h_bill_line = db_session.query(H_bill_line).filter(
            (H_bill_line._recid == h_bline_rec_id)).first()

    h_art = db_session.query(H_art).filter(
            (H_art.artnr == h_bill_line.artnr) &  (H_art.departement == h_bill_line.departement)).first()
    rec_id_h_art = h_art._recid

    if h_art.artart == 0:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 261)).first()

        if htparam.flogical:

            if not zugriff:
                fl_code3 = 1

                return generate_output()

        for hbline in db_session.query(Hbline).filter(
                (Hbline.rechnr == h_bill_line.rechnr) &  (Hbline.bill_datum == h_bill_line.bill_datum) &  (Hbline.departement == h_bill_line.departement) &  (Hbline.artnr == h_bill_line.artnr) &  (Hbline.bezeich == h_bill_line.bezeich) &  (Hbline.epreis == h_bill_line.epreis)).all():
            anz = anz + hbline.anzahl

        if anz == 0:
            fl_code = 1

            return generate_output()

        if h_bill_line.anzahl > 1:
            fl_code1 = 1

            return generate_output()
        else:
            qty = - h_bill_line.anzahl
        answer = False
        cancel_flag = True

        h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel._recid == h_art._recid)).first()
        billart = h_bill_line.artnr
        description = h_bill_line.bezeich
        price = h_bill_line.epreis
        fl_code2 = 1
        t_h_artikel = T_h_artikel()
        t_h_artikel_list.append(t_h_artikel)

        buffer_copy(h_artikel, t_h_artikel)
        t_h_artikel.rec_id = h_artikel._recid

    return generate_output()