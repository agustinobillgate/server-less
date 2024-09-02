from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bediener, Debitor, Waehrung, Res_history

def ar_debtlist_frame2bl(pvilanguage:int, user_init:str, edit_list:[Edit_list]):
    msg_str = ""
    lvcarea:str = "ar_debtlist"
    old_curr:str = ""
    bediener = debitor = waehrung = res_history = None

    edit_list = None

    edit_list_list, Edit_list = create_model("Edit_list", {"rechnr":int, "datum":date, "zinr":str, "billname":str, "lamt":decimal, "famt":decimal, "fcurr":str, "ar_recid":int, "amt_change":bool, "curr_change":bool, "curr_nr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, old_curr, bediener, debitor, waehrung, res_history


        nonlocal edit_list
        nonlocal edit_list_list
        return {"msg_str": msg_str}

    pass


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    for edit_list in query(edit_list_list, filters=(lambda edit_list :edit_list.curr_change or edit_list.amt_change)):

        debitor = db_session.query(Debitor).filter(
                (Debitor._recid == edit_list.ar_recid)).first()

        if debitor:

            debitor = db_session.query(Debitor).first()

            if curr_change:

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrungsnr == debitor.betrieb_gastmem)).first()

                if waehrung:
                    old_curr = waehrung.wabkurz
                else:
                    old_curr = ""

                bediener = db_session.query(Bediener).filter(
                        (func.lower(Bediener.userinit) == (user_init).lower())).first()
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "A/R"
                res_history.aenderung = "Change Foreign Currency: " +\
                        old_curr + " To " +\
                        to_string(edit_list.fcurr, "x(4)")

                res_history = db_session.query(Res_history).first()
                debitor.betrieb_gastmem = edit_list.curr_nr

            if amt_change:

                bediener = db_session.query(Bediener).filter(
                        (func.lower(Bediener.userinit) == (user_init).lower())).first()
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "A/R"
                res_history.aenderung = "Change Foreign Amount: " +\
                        trim(to_string(debitor.vesrdep, "->>>,>>>,>>9.99")) + " To " +\
                        trim(to_string(edit_list.famt, "->>>,>>>,>>9.99"))

                res_history = db_session.query(Res_history).first()
                debitor.vesrdep = edit_list.famt

            debitor = db_session.query(Debitor).first()
        else:
            msg_str = msg_str + translateExtended ("Unable to update A/R Record BillNo", lvcarea, "") + " " + to_string(edit_list.rechnr) + "." + chr(2)

    return generate_output()