#using conversion tools version: 1.0.0.117
"""_yusufwijasena_29/10/2025

    Ticket ID: CF3E24
        _remark_:   - fix python indentation
                    - fix var declaration
                    - add import from functions_py
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
# from functions.htpdate import htpdate
from functions_py.htpdate import htpdate
from models import Htparam, Queasy, H_bill_line, H_journal

menu_list_data, Menu_list = create_model(
    "Menu_list", {
        "request":str, 
        "krecid":int, 
        "posted":bool, 
        "nr":int, 
        "artnr":int, 
        "bezeich":str,
        "anzahl":int, 
        "price":Decimal, 
        "betrag":Decimal, 
        "voucher":str
        }, {
            "voucher": ""
            })

def ts_restinv_add_kds_cldbl(menu_list_data:Menu_list, tischnr:int, curr_dept:int, curr_waiter:int, rechnr:int, user_init:str):

    prepare_cache ([Htparam, Queasy, H_bill_line, H_journal])

    mess_result = ""
    disc_art1:int = 0
    disc_art2:int = 0
    disc_art3:int = 0
    head_recid:int = 0
    i:int = 0
    pvilanguage:int = 0
    bill_date:date 
    htparam = queasy = h_bill_line = h_journal = None

    menu_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, disc_art1, disc_art2, disc_art3, head_recid, i, pvilanguage, bill_date, htparam, queasy, h_bill_line, h_journal
        nonlocal tischnr, curr_dept, curr_waiter, rechnr, user_init
        nonlocal menu_list

        return {
            "mess_result": mess_result
            }

    def create_request_journal():
        nonlocal mess_result, disc_art1, disc_art2, disc_art3, head_recid, i, pvilanguage, bill_date, htparam, queasy, h_bill_line, h_journal
        nonlocal tischnr, curr_dept, curr_waiter, rechnr, user_init
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

    if tischnr == None or tischnr == 0:
        mess_result = "Table Number Can't Be Null!"

        return generate_output()

    if curr_dept == None or curr_dept == 0:
        mess_result = "Dept Number Can't Be Null!"

        return generate_output()

    if curr_waiter == None or curr_waiter == 0:
        mess_result = "Waiter Number Can't Be Null!"

        return generate_output()

    if rechnr == None or rechnr == 0:
        mess_result = "Bill Number Can't Be Null!"

        return generate_output()

    if user_init == None or user_init == "":
        mess_result = "User Init Can't Be Null!"

        return generate_output()

    for menu_list in query(menu_list_data, filters=(lambda menu_list: menu_list.nr == 0 and menu_list.request != "")):
        create_request_journal()
        menu_list_data.remove(menu_list)
    bill_date = get_output(htpdate(110))

    for menu_list in query(menu_list_data, filters=(lambda menu_list: menu_list.artnr == disc_art1 or menu_list.artnr == disc_art2 or menu_list.artnr == disc_art3)):
        menu_list_data.remove(menu_list)
    queasy = Queasy()

    queasy.key = 257
    queasy.number1 = curr_dept
    queasy.number2 = rechnr
    queasy.number3 = tischnr
    queasy.char1 = "kds-header"
    queasy.char2 = user_init
    queasy.date1 = bill_date
    queasy.logi1 = False
    queasy.deci1 =  to_decimal(get_current_time_in_seconds)()

    db_session.add(queasy)

    head_recid = queasy._recid

    for menu_list in query(menu_list_data, sort_by=[("nr",False)]):
        for h_bill_line in db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == rechnr) & (H_bill_line.departement == curr_dept) & (H_bill_line.artnr == menu_list.artnr) & (H_bill_line.anzahl == menu_list.anzahl) & (H_bill_line.bill_datum == bill_date)).order_by(H_bill_line._recid).all():
            queasy = get_cache (Queasy, {
                "key": [(eq, 255)],
                "char1": [(eq, "kds-line")],
                "number3": [(eq, to_int(h_bill_line._recid))]})

            if not queasy:
                for i in range(1,h_bill_line.anzahl + 1) :
                    queasy = Queasy()

                    queasy.key = 255
                    queasy.number1 = curr_dept
                    queasy.number2 = rechnr
                    queasy.number3 = h_bill_line._recid
                    queasy.char1 = "kds-line"
                    queasy.char2 = user_init
                    queasy.date1 = h_bill_line.bill_datum
                    queasy.deci1 =  to_decimal(h_bill_line.zeit)
                    queasy.deci2 =  to_decimal(head_recid)
                    queasy.logi1 = False
                    queasy.betriebsnr = i

                    db_session.add(queasy)

    mess_result = "Post KDS Success!"

    return generate_output()