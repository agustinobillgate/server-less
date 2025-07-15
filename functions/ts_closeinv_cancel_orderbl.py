from functions.additional_functions import *
import decimal
from models import H_artikel, H_bill_line

def ts_closeinv_cancel_orderbl(h_bline_rec_id:int):
    fl_code = 0
    fl_code1 = 0
    fl_code2 = 0
    qty = 0
    answer = False
    cancel_flag = False
    billart = 0
    description = ""
    price = to_decimal("0.0")
    rec_id_h_art = 0
    anz = 0
    tmp_hartikel_list = []
    h_artikel = h_bill_line = None

    tmp_hartikel = h_art = hbline = None

    tmp_hartikel_list, Tmp_hartikel = create_model_like(H_artikel, {"rec_id":int})

    H_art = create_buffer("H_art",H_artikel)
    Hbline = create_buffer("Hbline",H_bill_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, fl_code1, fl_code2, qty, answer, cancel_flag, billart, description, price, rec_id_h_art, anz, tmp_hartikel_list, h_artikel, h_bill_line
        nonlocal h_bline_rec_id
        nonlocal h_art, hbline


        nonlocal tmp_hartikel, h_art, hbline
        nonlocal tmp_hartikel_list
        return {"fl_code": fl_code, "fl_code1": fl_code1, "fl_code2": fl_code2, "qty": qty, "answer": answer, "cancel_flag": cancel_flag, "billart": billart, "description": description, "price": price, "rec_id_h_art": rec_id_h_art, "anz": anz, "tmp-hartikel": tmp_hartikel_list}

    h_bill_line = db_session.query(H_bill_line).filter(
             (H_bill_line._recid == h_bline_rec_id)).first()

    h_art = db_session.query(H_art).filter(
             (H_art.artnr == h_bill_line.artnr) & (H_art.departement == h_bill_line.departement)).first()
    rec_id_h_art = h_art._recid

    if h_art.artart == 0:

        for hbline in db_session.query(Hbline).filter(
                 (Hbline.rechnr == h_bill_line.rechnr) & (Hbline.bill_datum == h_bill_line.bill_datum) & (Hbline.departement == h_bill_line.departement) & (Hbline.artnr == h_bill_line.artnr) & (Hbline.bezeich == h_bill_line.bezeich) & (Hbline.epreis == h_bill_line.epreis)).order_by(Hbline._recid).all():
            anz = anz + hbline.anzahl

        if anz == 0:
            fl_code = 1

            return generate_output()
        qty = - h_bill_line.anzahl
        answer = False
        cancel_flag = True

        h_artikel = db_session.query(H_artikel).filter(
                     (H_artikel._recid == h_art._recid)).first()
        billart = h_bill_line.artnr
        description = h_bill_line.bezeich
        price =  to_decimal(h_bill_line.epreis)
        fl_code2 = 1
        tmp_hartikel = Tmp_hartikel()
        tmp_hartikel_list.append(tmp_hartikel)

        buffer_copy(h_artikel, tmp_hartikel)
        tmp_hartikel.rec_id = h_artikel._recid

    return generate_output()