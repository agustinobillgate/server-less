#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, Debitor, Waehrung, Res_history

edit_list_data, Edit_list = create_model("Edit_list", {"rechnr":int, "datum":date, "zinr":string, "billname":string, "lamt":Decimal, "famt":Decimal, "fcurr":string, "ar_recid":int, "amt_change":bool, "curr_change":bool, "curr_nr":int})

def ar_debtlist_frame2bl(pvilanguage:int, user_init:string, edit_list_data:[Edit_list]):

    prepare_cache ([Bediener, Debitor, Waehrung, Res_history])

    msg_str = ""
    lvcarea:string = "ar-debtlist"
    old_curr:string = ""
    bediener = debitor = waehrung = res_history = None

    edit_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, old_curr, bediener, debitor, waehrung, res_history
        nonlocal pvilanguage, user_init


        nonlocal edit_list

        return {"msg_str": msg_str}


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    for edit_list in query(edit_list_data, filters=(lambda edit_list: edit_list.curr_change or edit_list.amt_change)):

        debitor = get_cache (Debitor, {"_recid": [(eq, edit_list.ar_recid)]})

        if debitor:
            pass

            if curr_change:

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                if waehrung:
                    old_curr = waehrung.wabkurz
                else:
                    old_curr = ""

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "A/R"
                res_history.aenderung = "Change Foreign Currency: " +\
                        old_curr + " To " +\
                        to_string(edit_list.fcurr, "x(4)")


                pass
                debitor.betrieb_gastmem = edit_list.curr_nr

            if amt_change:

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "A/R"
                res_history.aenderung = "Change Foreign Amount: " +\
                        trim(to_string(debitor.vesrdep, "->>>,>>>,>>9.99")) + " To " +\
                        trim(to_string(edit_list.famt, "->>>,>>>,>>9.99"))


                pass
                debitor.vesrdep =  to_decimal(edit_list.famt)


            pass
        else:
            msg_str = msg_str + translateExtended ("Unable to update A/R Record BillNo", lvcarea, "") + " " + to_string(edit_list.rechnr) + "." + chr_unicode(2)

    return generate_output()