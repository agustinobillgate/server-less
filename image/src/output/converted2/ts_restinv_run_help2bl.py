#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.add_kitchprbl import add_kitchprbl
from functions.htpdate import htpdate
from models import Htparam, H_journal

menu_list_list, Menu_list = create_model("Menu_list", {"request":string, "krecid":int, "posted":bool, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "price":Decimal, "betrag":Decimal, "voucher":string}, {"anzahl": 1, "voucher": ""})

def ts_restinv_run_help2bl(menu_list_list:[Menu_list], pvilanguage:int, session_parameter:string, do_it:bool, tischnr:int, curr_dept:int, curr_waiter:int, rechnr:int, departement:int, user_init:string):

    prepare_cache ([Htparam, H_journal])

    bill_date = None
    error_str = ""
    disc_art1:int = 0
    disc_art2:int = 0
    disc_art3:int = 0
    head_recid:int = 0
    i:int = 0
    htparam = h_journal = None

    menu_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, error_str, disc_art1, disc_art2, disc_art3, head_recid, i, htparam, h_journal
        nonlocal pvilanguage, session_parameter, do_it, tischnr, curr_dept, curr_waiter, rechnr, departement, user_init


        nonlocal menu_list

        return {"bill_date": bill_date, "error_str": error_str}

    def create_request_journal():

        nonlocal bill_date, error_str, disc_art1, disc_art2, disc_art3, head_recid, i, htparam, h_journal
        nonlocal pvilanguage, session_parameter, do_it, tischnr, curr_dept, curr_waiter, rechnr, departement, user_init


        nonlocal menu_list


        bill_date = get_output(htpdate(110))
        h_journal = H_journal()
        db_session.add(h_journal)

        h_journal.artnr = menu_list.artnr
        h_journal.bezeich = "<!" + menu_list.bezeich + "!>"
        h_journal.aendertext = menu_list.request
        h_journal.anzahl = 0
        h_journal.epreis =  to_decimal("0")
        h_journal.rechnr = rechnr
        h_journal.tischnr = tischnr
        h_journal.departement = curr_dept
        h_journal.zeit = get_current_time_in_seconds()
        h_journal.kellner_nr = curr_waiter
        h_journal.bill_datum = bill_date
        h_journal.sysdate = get_current_date()


    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})

    if htparam:
        disc_art1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})

    if htparam:
        disc_art2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})

    if htparam:
        disc_art3 = htparam.finteger

    for menu_list in query(menu_list_list, filters=(lambda menu_list: menu_list.nr == 0 and menu_list.request != "")):
        create_request_journal()
        menu_list_list.remove(menu_list)

    if do_it:
        error_str = get_output(add_kitchprbl(pvilanguage, session_parameter, departement, rechnr, bill_date, user_init))

    return generate_output()