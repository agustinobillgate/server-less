#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.ts_restinv_disp_requestbl import ts_restinv_disp_requestbl
from models import H_bill_line, H_artikel

def ts_restinv_disp_bill_linebl(double_currency:bool, rechnr:int, curr_dept:int, avail_t_h_bill:bool):

    prepare_cache ([H_artikel])

    t_h_bill_line_data = []
    h_bill_line = h_artikel = None

    t_h_bill_line = None

    t_h_bill_line_data, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int, "request_str":string, "flag_code":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_bill_line_data, h_bill_line, h_artikel
        nonlocal double_currency, rechnr, curr_dept, avail_t_h_bill


        nonlocal t_h_bill_line
        nonlocal t_h_bill_line_data

        return {"t-h-bill-line": t_h_bill_line_data}

    def show_submenu():

        nonlocal t_h_bill_line_data, h_bill_line, h_artikel
        nonlocal double_currency, rechnr, curr_dept, avail_t_h_bill


        nonlocal t_h_bill_line
        nonlocal t_h_bill_line_data

        h_art2 = None
        H_art2 =  create_buffer("H_art2",H_artikel)

        h_art2 = get_cache (H_artikel, {"departement": [(eq, h_bill_line.departement)],"artnr": [(eq, h_bill_line.artnr)]})

        if not h_art2 or not avail_t_h_bill:
            t_h_bill_line.flag_code = 0

        elif h_art2.artart == 0 and h_art2.betriebsnr > 0:
            t_h_bill_line.flag_code = 1


    if double_currency:

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == rechnr) & (H_bill_line.departement == curr_dept)).order_by(H_bill_line.bill_datum.desc(), H_bill_line.zeit.desc()).all():
            t_h_bill_line = T_h_bill_line()
            t_h_bill_line_data.append(t_h_bill_line)

            buffer_copy(h_bill_line, t_h_bill_line)
            t_h_bill_line.rec_id = h_bill_line._recid


            show_submenu()
            request_str = get_output(ts_restinv_disp_requestbl(h_bill_line._recid))
            t_h_bill_line.request_str = request_str

    else:

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == rechnr) & (H_bill_line.departement == curr_dept)).order_by(H_bill_line.bill_datum.desc(), H_bill_line.zeit.desc()).all():
            t_h_bill_line = T_h_bill_line()
            t_h_bill_line_data.append(t_h_bill_line)

            buffer_copy(h_bill_line, t_h_bill_line)
            t_h_bill_line.rec_id = h_bill_line._recid


            show_submenu()
            request_str = get_output(ts_restinv_disp_requestbl(h_bill_line._recid))
            t_h_bill_line.request_str = request_str


    return generate_output()