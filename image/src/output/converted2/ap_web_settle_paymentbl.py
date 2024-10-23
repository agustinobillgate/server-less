from functions.additional_functions import *
import decimal
from datetime import date
from functions.ap_debtpay_settle_paymentbl import ap_debtpay_settle_paymentbl

age_list_list, Age_list = create_model("Age_list", {"selected":bool, "ap_recid":int, "counter":int, "docu_nr":str, "rechnr":int, "lief_nr":int, "lscheinnr":str, "supplier":str, "rgdatum":date, "rabatt":decimal, "rabattbetrag":decimal, "ziel":date, "netto":decimal, "user_init":str, "debt":decimal, "credit":decimal, "bemerk":str, "tot_debt":decimal, "rec_id":int, "resname":str, "comments":str})
pay_list_list, Pay_list = create_model("Pay_list", {"dummy":str, "artnr":int, "bezeich":str, "proz":decimal, "betrag":decimal})

def ap_web_settle_paymentbl(age_list_list:[Age_list], pay_list_list:[Pay_list], rundung:int, outstand:decimal, outstand1:decimal, pay_date:date, remark:str, user_init:str):
    msg_str = ""
    anzahl:int = 0
    okflag:bool = False

    age_list = pay_list = t_l_lieferant = None

    t_l_lieferant_list, T_l_lieferant = create_model("T_l_lieferant", {"telefon":str, "fax":str, "adresse1":str, "notizen_1":str, "lief_nr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, anzahl, okflag
        nonlocal rundung, outstand, outstand1, pay_date, remark, user_init


        nonlocal age_list, pay_list, t_l_lieferant
        nonlocal age_list_list, pay_list_list, t_l_lieferant_list
        return {"msg_str": msg_str}


    okflag = False

    if outstand == 0:
        okflag = True
    else:
        anzahl = 0

        for age_list in query(age_list_list, filters=(lambda age_list: age_list.selected)):
            anzahl = anzahl + 1

        if anzahl == 1:
            okflag = True

    if okflag:
        pay_list_list, age_list_list, t_l_lieferant_list = get_output(ap_debtpay_settle_paymentbl(pay_list_list, age_list_list, user_init, outstand, outstand1, rundung, pay_date, remark))
        msg_str = "AP Payment Success"
    else:
        msg_str = "Partial Payment for multi-selected A/P records not possible"

        return generate_output()