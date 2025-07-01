#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ap_debtpay_settle_paymentbl import ap_debtpay_settle_paymentbl

age_list_list, Age_list = create_model("Age_list", {"selected":bool, "ap_recid":int, "counter":int, "docu_nr":string, "rechnr":int, "lief_nr":int, "lscheinnr":string, "supplier":string, "rgdatum":date, "rabatt":Decimal, "rabattbetrag":Decimal, "ziel":date, "netto":Decimal, "user_init":string, "debt":Decimal, "credit":Decimal, "bemerk":string, "tot_debt":Decimal, "rec_id":int, "resname":string, "comments":string, "fibukonto":string, "t_bezeich":string, "debt2":Decimal, "recv_date":date})
pay_list_list, Pay_list = create_model("Pay_list", {"dummy":string, "artnr":int, "bezeich":string, "proz":Decimal, "betrag":Decimal, "remark":string})

def ap_web_settle_paymentbl(age_list_list:[Age_list], pay_list_list:[Pay_list], rundung:int, outstand:Decimal, outstand1:Decimal, pay_date:date, remark:string, user_init:string):
    msg_str = ""
    anzahl:int = 0
    okflag:bool = False

    age_list = pay_list = t_l_lieferant = None

    t_l_lieferant_list, T_l_lieferant = create_model("T_l_lieferant", {"telefon":string, "fax":string, "adresse1":string, "notizen_1":string, "lief_nr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, anzahl, okflag
        nonlocal rundung, outstand, outstand1, pay_date, remark, user_init


        nonlocal age_list, pay_list, t_l_lieferant
        nonlocal t_l_lieferant_list

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

    return generate_output()