#using conversion tools version: 1.0.0.119
#-------------------------------------------
# Rd, 26/11/2025, with_for_update
#-------------------------------------------

# ===========================================
# Rulita, 11-12-2025
# - Added with_for_update before delete query
# ===========================================

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill, Queasy, H_queasy

p_list_data, P_list = create_model("P_list", {"rechnr":int, "dept":int, "billno":int, "printed_line":int, "b_recid":int, "last_amount":Decimal, "last_famount":Decimal})

def tada_post_payment_delqueasybl(p_list_data:[P_list], rec_id:int, use_h_queasy:bool):

    prepare_cache ([H_bill])

    h_bill = queasy = h_queasy = None

    p_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill, queasy, h_queasy
        nonlocal rec_id, use_h_queasy


        nonlocal p_list

        return {"p-list": p_list_data}

    def del_queasy():

        nonlocal h_bill, queasy, h_queasy
        nonlocal rec_id, use_h_queasy
        nonlocal p_list

        if not use_h_queasy:

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 4) & (Queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) & 
                     (Queasy.number2 >= 0) & (Queasy.deci2 >= 0)).order_by(Queasy._recid).with_for_update().all():
                db_session.delete(queasy)

            else:

                for h_queasy in db_session.query(H_queasy).filter(
                         (H_queasy.number1 == (h_bill.departement + h_bill.rechnr * 100))).order_by(H_queasy._recid).with_for_update().all():
                    db_session.delete(h_queasy)


        for p_list in query(p_list_data, filters=(lambda p_list: p_list.rechnr == h_bill.rechnr and p_list.dept == h_bill.departement)):
            p_list_data.remove(p_list)


    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})
    del_queasy()

    return generate_output()