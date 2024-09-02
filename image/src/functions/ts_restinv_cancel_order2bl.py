from functions.additional_functions import *
import decimal
from models import H_artikel, H_bill_line

def ts_restinv_cancel_order2bl(rec_id_h_art:int, rec_id_hbline:int):
    answer = False
    cancel_flag = False
    billart = 0
    description = ""
    price = 0
    t_h_artikel_list = []
    h_artikel = h_bill_line = None

    t_h_artikel = None

    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal answer, cancel_flag, billart, description, price, t_h_artikel_list, h_artikel, h_bill_line


        nonlocal t_h_artikel
        nonlocal t_h_artikel_list
        return {"answer": answer, "cancel_flag": cancel_flag, "billart": billart, "description": description, "price": price, "t-h-artikel": t_h_artikel_list}

    h_bill_line = db_session.query(H_bill_line).filter(
            (H_bill_line._recid == rec_id_hbline)).first()
    answer = False
    cancel_flag = True

    h_artikel = db_session.query(H_artikel).filter(
                (H_artikel._recid == rec_id_h_art)).first()
    billart = h_bill_line.artnr
    description = h_bill_line.bezeich
    price = h_bill_line.epreis
    t_h_artikel = T_h_artikel()
    t_h_artikel_list.append(t_h_artikel)

    buffer_copy(h_artikel, t_h_artikel)
    t_h_artikel.rec_id = h_artikel._recid

    return generate_output()