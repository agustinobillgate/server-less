#using conversion tools version: 1.0.0.117
#-------------------------------------------
# Rd, 27/11/2025, with_for_update
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

supplier_data, Supplier = create_model("Supplier", {"supplier_name":string, "lief_nr":string, "supplierid":string})

def mapping_supplier_save_horekabl(supplier_data:[Supplier]):

    prepare_cache ([Queasy])

    queasy = None

    supplier = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy


        nonlocal supplier

        return {}

    for supplier in query(supplier_data):

        # queasy = get_cache (Queasy, {"key": [(eq, 256)],"char1": [(eq, supplier.supplier_name)]})
        queasy = db_session.query(Queasy).filter(Queasy.key == 256, Queasy.char1 == supplier.supplier_name).with_for_update().first()

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