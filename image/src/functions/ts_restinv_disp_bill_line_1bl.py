from functions.additional_functions import *
import decimal
from functions.ts_restinv_disp_requestbl import ts_restinv_disp_requestbl
from models import H_bill_line, H_artikel

def ts_restinv_disp_bill_line_1bl(double_currency:bool, rechnr:int, curr_dept:int, avail_t_h_bill:bool):
    t_h_bill_line_list = []
    amount_bill = 0
    h_bill_line = h_artikel = None

    t_h_bill_line = h_art2 = None

    t_h_bill_line_list, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int, "request_str":str, "flag_code":int})

    H_art2 = H_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_bill_line_list, amount_bill, h_bill_line, h_artikel
        nonlocal h_art2


        nonlocal t_h_bill_line, h_art2
        nonlocal t_h_bill_line_list
        return {"t-h-bill-line": t_h_bill_line_list, "amount_bill": amount_bill}

    def show_submenu():

        nonlocal t_h_bill_line_list, amount_bill, h_bill_line, h_artikel
        nonlocal h_art2


        nonlocal t_h_bill_line, h_art2
        nonlocal t_h_bill_line_list


        H_art2 = H_artikel

        h_art2 = db_session.query(H_art2).filter(
                (H_art2.departement == h_bill_line.departement) &  (H_art2.artnr == h_bill_line.artnr)).first()

        if not h_art2 or not avail_t_h_bill:
            t_h_bill_line.flag_code = 0

        elif h_art2.artart == 0 and h_art2.betriebsnr > 0:
            t_h_bill_line.flag_code = 1

    if double_currency:

        for h_bill_line in db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == rechnr) &  (H_bill_line.departement == curr_dept)).all():
            t_h_bill_line = T_h_bill_line()
            t_h_bill_line_list.append(t_h_bill_line)

            buffer_copy(h_bill_line, t_h_bill_line)
            t_h_bill_line.rec_id = h_bill_line._recid


            show_submenu()
            request_str = get_output(ts_restinv_disp_requestbl(h_bill_line._recid))
            t_h_bill_line.request_str = request_str
            amount_bill = amount_bill + h_bill_line.betrag

    else:

        for h_bill_line in db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == rechnr) &  (H_bill_line.departement == curr_dept)).all():
            t_h_bill_line = T_h_bill_line()
            t_h_bill_line_list.append(t_h_bill_line)

            buffer_copy(h_bill_line, t_h_bill_line)
            t_h_bill_line.rec_id = h_bill_line._recid


            show_submenu()
            request_str = get_output(ts_restinv_disp_requestbl(h_bill_line._recid))
            t_h_bill_line.request_str = request_str
            amount_bill = amount_bill + h_bill_line.betrag


    return generate_output()