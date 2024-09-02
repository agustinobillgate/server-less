from functions.additional_functions import *
import decimal
from models import Queasy, L_lieferant

def prepare_mapping_supplier_horekabl():
    supplier_list = []
    queasy = l_lieferant = None

    supplier = bqueasy = None

    supplier_list, Supplier = create_model("Supplier", {"supplier_name":str, "lief_nr":str, "supplierid":str})

    Bqueasy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal supplier_list, queasy, l_lieferant
        nonlocal bqueasy


        nonlocal supplier, bqueasy
        nonlocal supplier_list
        return {"supplier": supplier_list}

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 256)).first()

    if not queasy:

        for l_lieferant in db_session.query(L_lieferant).all():
            supplier = Supplier()
            supplier_list.append(supplier)

            supplier.supplier_name = l_lieferant.firma
            supplier.lief_nr = to_string(l_lieferant.lief_nr)


    else:

        for bqueasy in db_session.query(Bqueasy).filter(
                (Bqueasy.key == 256)).all():
            supplier = Supplier()
            supplier_list.append(supplier)

            supplier.supplier_name = bqueasy.char1
            supplier.lief_nr = bqueasy.char2
            supplier.supplierid = bqueasy.char3

        for l_lieferant in db_session.query(L_lieferant).all():

            supplier = query(supplier_list, filters=(lambda supplier :supplier.supplier_name == l_lieferant.firma), first=True)

            if not supplier:
                supplier = Supplier()
                supplier_list.append(supplier)

                supplier.supplier_name = l_lieferant.firma
                supplier.lief_nr = to_string(l_lieferant.lief_nr)

    return generate_output()