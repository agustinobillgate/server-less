#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

supplier_list, Supplier = create_model("Supplier", {"supplier_name":string, "lief_nr":string, "supplierid":string})

def mapping_supplier_save_horekabl(supplier_list:[Supplier]):

    prepare_cache ([Queasy])

    queasy = None

    supplier = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy


        nonlocal supplier

        return {}

    for supplier in query(supplier_list):

        queasy = get_cache (Queasy, {"key": [(eq, 256)],"char1": [(eq, supplier.supplier_name)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 256
            queasy.char1 = supplier.supplier_name
            queasy.char2 = supplier.lief_nr
            queasy.char3 = supplier.supplierid


        else:
            pass
            queasy.char1 = supplier.supplier_name
            queasy.char2 = supplier.lief_nr
            queasy.char3 = supplier.supplierid


            pass
            pass

    return generate_output()