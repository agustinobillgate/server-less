from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from sqlalchemy import func
from models import Htparam, Queasy, H_bill_line, H_journal

def ts_restinv_add_kdsbl(menu_list:[Menu_list], tischnr:int, curr_dept:int, curr_waiter:int, rechnr:int, user_init:str):
    mess_result = ""
    disc_art1:int = 0
    disc_art2:int = 0
    disc_art3:int = 0
    head_recid:int = 0
    i:int = 0
    pvilanguage:int = 0
    bill_date:date = None
    htparam = queasy = h_bill_line = h_journal = None

    menu_list = None

    menu_list_list, Menu_list = create_model("Menu_list", {"request":str, "krecid":int, "posted":bool, "nr":int, "artnr":int, "bezeich":str, "anzahl":int, "price":decimal, "betrag":decimal, "voucher":str}, {"voucher": ""})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, disc_art1, disc_art2, disc_art3, head_recid, i, pvilanguage, bill_date, htparam, queasy, h_bill_line, h_journal


        nonlocal menu_list
        nonlocal menu_list_list
        return {"mess_result": mess_result}

    def create_request_journal():

        nonlocal mess_result, disc_art1, disc_art2, disc_art3, head_recid, i, pvilanguage, bill_date, htparam, queasy, h_bill_line, h_journal


        nonlocal menu_list
        nonlocal menu_list_list


        bill_date = get_output(htpdate(110))
        h_journal = H_journal()
        db_session.add(h_journal)

        h_journal.artnr = menu_list.artnr
        h_journal.bezeich = "<!" + menu_list.bezeich + "!>"
        h_journal.aendertext = menu_list.REQUEST
        h_journal.anzahl = 0
        h_journal.epreis = 0
        h_journal.rechnr = rechnr
        h_journal.tischnr = tischnr
        h_journal.departement = curr_dept
        h_journal.zeit = get_current_time_in_seconds()
        h_journal.kellner_nr = curr_waiter
        h_journal.bill_datum = bill_date
        h_journal.sysdate = get_current_date()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 557)).first()

    if htparam:
        disc_art1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 596)).first()

    if htparam:
        disc_art2 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 556)).first()

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

    for menu_list in query(menu_list_list, filters=(lambda menu_list :menu_list.nr == 0 and menu_list.REQUEST != "")):
        create_request_journal()
        menu_list_list.remove(menu_list)
    bill_date = get_output(htpdate(110))

    for menu_list in query(menu_list_list, filters=(lambda menu_list :menu_list.artnr == disc_art1 or menu_list.artnr == disc_art2 or menu_list.artnr == disc_art3)):
        menu_list_list.remove(menu_list)
    queasy = Queasy()
    db_session.add(queasy)

    queasy.key = 257
    queasy.number1 = curr_dept
    queasy.number2 = rechnr
    queasy.number3 = tischnr
    queasy.char1 = "kds_header"
    queasy.char2 = user_init
    queasy.date1 = bill_date
    queasy.logi1 = False
    queasy.deci1 = get_current_time_in_seconds()

    queasy = db_session.query(Queasy).first()
    head_recid = queasy._recid

    for menu_list in query(menu_list_list):

        for h_bill_line in db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == rechnr) &  (H_bill_line.departement == curr_dept) &  (H_bill_line.artnr == menu_list.artnr) &  (H_bill_line.anzahl == menu_list.anzahl) &  (H_bill_line.bill_datum == bill_date)).all():

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 255) &  (func.lower(Queasy.char1) == "kds_line") &  (Queasy.number3 == to_int(h_bill_line._recid))).first()

            if not queasy:
                for i in range(1,h_bill_line.anzahl + 1) :
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 255
                    queasy.number1 = curr_dept
                    queasy.number2 = rechnr
                    queasy.number3 = h_bill_line._recid
                    queasy.char1 = "kds_line"
                    queasy.char2 = user_init
                    queasy.date1 = h_bill_line.bill_datum
                    queasy.deci1 = h_bill_line.zeit
                    queasy.deci2 = head_recid
                    queasy.logi1 = False
                    queasy.betriebsnr = i


    mess_result = "Post KDS Success!"

    return generate_output()