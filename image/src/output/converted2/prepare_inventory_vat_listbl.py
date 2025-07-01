#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def prepare_inventory_vat_listbl():

    prepare_cache ([Queasy])

    invvat_list_list = []
    queasy = None

    invvat_list = None

    invvat_list_list, Invvat_list = create_model("Invvat_list", {"nr":int, "bezeich":string, "vat_value":Decimal, "fibukonto":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal invvat_list_list, queasy


        nonlocal invvat_list
        nonlocal invvat_list_list

        return {"invvat-list": invvat_list_list}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 303)).order_by(Queasy._recid).all():
        invvat_list = Invvat_list()
        invvat_list_list.append(invvat_list)

        invvat_list.nr = queasy.number1
        invvat_list.bezeich = queasy.char1
        invvat_list.vat_value =  to_decimal(queasy.deci1)
        invvat_list.fibukonto = queasy.char2

    return generate_output()