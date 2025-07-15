#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_kredit, Queasy

age_list_data, Age_list = create_model("Age_list", {"selected":bool, "ap_recid":int, "counter":int, "docu_nr":string, "rechnr":int, "lief_nr":int, "lscheinnr":string, "supplier":string, "rgdatum":date, "rabatt":Decimal, "rabattbetrag":Decimal, "ziel":date, "netto":Decimal, "user_init":string, "debt":Decimal, "credit":Decimal, "bemerk":string, "tot_debt":Decimal, "rec_id":int, "resname":string, "comments":string, "fibukonto":string, "t_bezeich":string, "debt2":Decimal, "recv_date":date})

def ap_debtpay_remove_voucherbl(age_list_data:[Age_list]):

    prepare_cache ([L_kredit])

    l_kredit = queasy = None

    age_list = abuff = debt = None

    Abuff = Age_list
    abuff_data = age_list_data

    Debt = create_buffer("Debt",L_kredit)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_kredit, queasy
        nonlocal abuff, debt


        nonlocal age_list, abuff, debt

        return {"age-list": age_list_data}

    for age_list in query(age_list_data, filters=(lambda age_list: age_list.selected)):

        queasy = get_cache (Queasy, {"key": [(eq, 173)],"number1": [(eq, age_list.lief_nr)],"number2": [(eq, age_list.rechnr)]})

        if queasy:
            pass
            db_session.delete(queasy)
            pass
        age_list.rechnr = 0
        age_list.selected = False

        l_kredit = get_cache (L_kredit, {"_recid": [(eq, age_list.ap_recid)]})
        l_kredit.rechnr = 0


        pass

    return generate_output()