from functions.additional_functions import *
import decimal
from models import Queasy

def mapping_supplier_save_horekabl(supplier:[Supplier]):
    queasy = None

    supplier = None

    supplier_list, Supplier = create_model("Supplier", {"supplier_name":str, "lief_nr":str, "supplierid":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy


        nonlocal supplier
        nonlocal supplier_list
        return {}

    for supplier in query(supplier_list):

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 256) &  (Queasy.char1 == supplier.supplier_name)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 256
            queasy.char1 = supplier.supplier_name
            queasy.char2 = supplier.lief_nr
            queasy.char3 = supplier.supplierid


        else:

            queasy = db_session.query(Queasy).first()
            queasy.char1 = supplier.supplier_name
            queasy.char2 = supplier.lief_nr
            queasy.char3 = supplier.supplierid

            queasy = db_session.query(Queasy).first()


    return generate_output()