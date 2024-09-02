from functions.additional_functions import *
import decimal
from models import H_bill, Htparam, H_bill_line

def prepare_ts_biltransferbl(h_recid:int):
    multi_vat = False
    dept = 0
    splitted = False
    t_h_bill_list = []
    h_bill = htparam = h_bill_line = None

    t_h_bill = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal multi_vat, dept, splitted, t_h_bill_list, h_bill, htparam, h_bill_line


        nonlocal t_h_bill
        nonlocal t_h_bill_list
        return {"multi_vat": multi_vat, "dept": dept, "splitted": splitted, "t-h-bill": t_h_bill_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 271)).first()

    if htparam.feldtyp == 4:
        multi_vat = htparam.flogical

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == h_recid)).first()
    dept = h_bill.departement

    h_bill_line = db_session.query(H_bill_line).filter(
            (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == dept) &  (H_bill_line.waehrungsnr > 0)).first()

    if h_bill_line:
        splitted = True
    t_h_bill = T_h_bill()
    t_h_bill_list.append(t_h_bill)

    buffer_copy(h_bill, t_h_bill)
    t_h_bill.rec_id = h_bill._recid

    return generate_output()