from functions.additional_functions import *
import decimal
from datetime import date
from models import L_kredit, Queasy

def ap_debtpay_remove_voucherbl(age_list:[Age_list]):
    l_kredit = queasy = None

    age_list = abuff = debt = None

    age_list_list, Age_list = create_model("Age_list", {"selected":bool, "ap_recid":int, "counter":int, "docu_nr":str, "rechnr":int, "lief_nr":int, "lscheinnr":str, "supplier":str, "rgdatum":date, "rabatt":decimal, "rabattbetrag":decimal, "ziel":date, "netto":decimal, "user_init":str, "debt":decimal, "credit":decimal, "bemerk":str, "tot_debt":decimal, "rec_id":int, "resname":str, "comments":str, "fibukonto":str, "t_bezeich":str, "debt2":decimal, "recv_date":date})

    Abuff = Age_list
    abuff_list = age_list_list

    Debt = L_kredit

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_kredit, queasy
        nonlocal abuff, debt


        nonlocal age_list, abuff, debt
        nonlocal age_list_list
        return {}

    for age_list in query(age_list_list, filters=(lambda age_list :age_list.SELECTED)):

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 173) &  (Queasy.number1 == age_list.lief_nr) &  (Queasy.number2 == age_list.rechnr)).first()

        if queasy:

            queasy = db_session.query(Queasy).first()
            db_session.delete(queasy)

        age_list.rechnr = 0
        age_list.SELECTED = False

        l_kredit = db_session.query(L_kredit).filter(
                (L_kredit._recid == age_list.ap_recid)).first()
        l_kredit.rechnr = 0

        l_kredit = db_session.query(L_kredit).first()

    return generate_output()