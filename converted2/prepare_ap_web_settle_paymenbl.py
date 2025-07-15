#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpchar import htpchar
from functions.ap_read_approvalbl import ap_read_approvalbl
from functions.load_artikelbl import load_artikelbl
from models import Queasy, Artikel

age_list_data, Age_list = create_model("Age_list", {"selected":bool, "ap_recid":int, "counter":int, "docu_nr":string, "rechnr":int, "lief_nr":int, "lscheinnr":string, "supplier":string, "rgdatum":date, "rabatt":Decimal, "rabattbetrag":Decimal, "ziel":date, "netto":Decimal, "user_init":string, "debt":Decimal, "credit":Decimal, "bemerk":string, "tot_debt":Decimal, "rec_id":int, "resname":string, "comments":string})

def prepare_ap_web_settle_paymenbl(age_list_data:[Age_list], rundung:int, outstand:Decimal):
    outstand1 = to_decimal("0.0")
    msg_str = ""
    artikel_list_data = []
    p_786:string = ""
    queasy = artikel = None

    age_list = artikel_list = t_queasy = t_artikel = age_list_buff = None

    artikel_list_data, Artikel_list = create_model("Artikel_list", {"artnr":int, "departement":int, "bezeich":string, "artart":int})
    t_queasy_data, T_queasy = create_model_like(Queasy)
    t_artikel_data, T_artikel = create_model_like(Artikel)

    Age_list_buff = Age_list
    age_list_buff_data = age_list_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal outstand1, msg_str, artikel_list_data, p_786, queasy, artikel
        nonlocal rundung, outstand
        nonlocal age_list_buff


        nonlocal age_list, artikel_list, t_queasy, t_artikel, age_list_buff
        nonlocal artikel_list_data, t_queasy_data, t_artikel_data

        return {"outstand": outstand, "outstand1": outstand1, "msg_str": msg_str, "artikel-list": artikel_list_data}

    p_786 = get_output(htpchar(786))

    age_list = query(age_list_data, first=True)

    if p_786 != "" and age_list:
        t_queasy_data = get_output(ap_read_approvalbl(1, age_list.lief_nr, ""))

    age_list = query(age_list_data, filters=(lambda age_list: age_list.selected), first=True)

    if not age_list:
        msg_str = "No Selected Record, payment not possible!"

        return generate_output()

    for age_list_buff in query(age_list_buff_data, filters=(lambda age_list_buff: age_list_buff.selected)):

        if p_786 != "" and age_list_buff.rechnr == 0:
            msg_str = "A/P Voucher No not attched, transaction is not possible"

            return generate_output()

        t_queasy = query(t_queasy_data, filters=(lambda t_queasy: t_queasy.number1 == age_list_buff.lief_nr and t_queasy.number2 == age_list_buff.rechnr), first=True)

        if t_queasy:
            msg_str = "A/P Voucher No, not approved completedly"

            return generate_output()
    artikel_list_data, t_artikel_data = get_output(load_artikelbl(9, None))
    outstand =  to_decimal(round (outstand , rundung))
    outstand1 =  to_decimal(outstand)

    return generate_output()