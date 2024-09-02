from functions.additional_functions import *
import decimal
from models import H_bill

def ldry_compli_p_list_namebl(c_list_rechnr:int, c_list_dept:int, gname:str):
    h_bill = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill


        return {}


    h_bill = db_session.query(H_bill).filter(
            (H_bill.rechnr == c_list_rechnr) &  (H_bill.departement == c_list_dept)).first()

    if h_bill:

        h_bill = db_session.query(H_bill).first()
        h_bill.bilname = gname

        h_bill = db_session.query(H_bill).first()

    return generate_output()