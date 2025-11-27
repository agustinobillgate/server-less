#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 26-11-2025
# - Added with_for_update all query 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Queasy, Guest_remark, Guest

g_list_data, G_list = create_model("G_list", {"key":int, "number1":int, "number2":int, "number3":int, "date1":date, "date2":date, "date3":date, "char1":string, "char2":string, "char3":string, "deci1":Decimal, "deci2":Decimal, "deci3":Decimal, "logi1":bool, "logi2":bool, "logi3":bool, "betriebsnr":int})
t_guest_remark_data, T_guest_remark = create_model("T_guest_remark", {"gastnr":int, "resnr":int, "reslinnr":int, "codenum":int, "datum":date, "zeit":int, "userinit":string, "cid":string, "chgdate":date, "chgtime":int, "bemerkung":string, "display_flag":bool, "res_integer":[int,3], "res_char":[string,3], "guest_name":string, "g_recid":int})
payload_list_data, Payload_list = create_model("Payload_list", {"curr_mode":string, "g_recid":int, "gastnrmember":int, "mode":int})

def guest_remark_webbl(g_list_data:[G_list], t_guest_remark_data:[T_guest_remark], payload_list_data:[Payload_list]):

    prepare_cache ([Htparam, Guest])

    t_queasy_data = []
    output_list_data = []
    last_categ:string = ""
    bill_date:date = None
    htparam = queasy = guest_remark = guest = None

    t_queasy = g_list = t_guest_remark = payload_list = output_list = None

    t_queasy_data, T_queasy = create_model("T_queasy", {"key":int, "number1":int, "number2":int, "number3":int, "date1":date, "date2":date, "date3":date, "char1":string, "char2":string, "char3":string, "deci1":Decimal, "deci2":Decimal, "deci3":Decimal, "logi1":bool, "logi2":bool, "logi3":bool, "betriebsnr":int})
    output_list_data, Output_list = create_model("Output_list", {"logic_param1109":bool, "guest_name":string, "remark":string, "success_flag":bool, "breakline":string, "gastnr":int, "resnr":int, "reslinnr":int, "codenum":int, "datum":date, "zeit":int, "userinit":string, "cid":string, "chgdate":date, "chgtime":int, "bemerkung":string, "display_flag":bool, "res_integer":[int,3], "res_char":[string,3], "guest_name2":string, "g_recid":int}, {"breakline": "############# PREPARE GUEST REMARK #############"})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_data, output_list_data, last_categ, bill_date, htparam, queasy, guest_remark, guest


        nonlocal t_queasy, g_list, t_guest_remark, payload_list, output_list
        nonlocal t_queasy_data, output_list_data

        return {"t-queasy": t_queasy_data, "output-list": output_list_data}


    output_list = Output_list()
    output_list_data.append(output_list)


    payload_list = query(payload_list_data, first=True)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1109)]})

    if htparam:
        output_list.logic_param1109 = htparam.flogical

    if payload_list.mode == 1:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 154)).order_by(Queasy.char1).all():
            t_queasy = T_queasy()
            t_queasy_data.append(t_queasy)

            buffer_copy(queasy, t_queasy)

    elif payload_list.mode == 2:

        if payload_list.curr_mode  == ("add") :

            for g_list in query(g_list_data):
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 154
                queasy.number1 = g_list.number1
                queasy.char1 = g_list.char1
                queasy.char3 = g_list.char3
                queasy.logi1 = g_list.logi1


                pass
                pass
            output_list.success_flag = True

        elif payload_list.curr_mode  == ("chg") :

            g_list = query(g_list_data, first=True)

            if g_list:

                # queasy = get_cache (Queasy, {"key": [(eq, g_list.key)],"number1": [(eq, g_list.number1)]})
                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == g_list.key) & (Queasy.number1 == g_list.number1)).with_for_update().first()

                if queasy:
                    pass
                    queasy.char1 = g_list.char1
                    queasy.char3 = g_list.char3
                    queasy.logi1 = g_list.logi1

                    db_session.refresh(queasy,with_for_update=True)
                    pass
                    pass
                    output_list.success_flag = True

        elif payload_list.curr_mode  == ("del") :

            g_list = query(g_list_data, first=True)

            if g_list:

                # queasy = get_cache (Queasy, {"key": [(eq, 154)],"number1": [(eq, g_list.number1)]})
                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 154) & (Queasy.number1 == g_list.number1)).with_for_update().first()

                if queasy:
                    pass
                    db_session.delete(queasy)
                    db_session.refresh(queasy,with_for_update=True)
                    pass
                    output_list.success_flag = True

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 154)).order_by(Queasy.char1).all():
            t_queasy = T_queasy()
            t_queasy_data.append(t_queasy)

            buffer_copy(queasy, t_queasy)

    elif payload_list.mode == 3:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 154)).order_by(Queasy.char1).all():
            t_queasy = T_queasy()
            t_queasy_data.append(t_queasy)

            buffer_copy(queasy, t_queasy)

    elif payload_list.mode == 4:

        for guest_remark in db_session.query(Guest_remark).filter(
                 (Guest_remark.gastnr == payload_list.gastnrmember)).order_by(Guest_remark._recid).all():

            guest = get_cache (Guest, {"gastnr": [(eq, payload_list.gastnrmember)]})

            if guest:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.gastnr = guest_remark.gastnr
                output_list.resnr = guest_remark.resnr
                output_list.reslinnr = guest_remark.reslinnr
                output_list.codenum = guest_remark.codenum
                output_list.datum = guest_remark.datum
                output_list.zeit = guest_remark.zeit
                output_list.userinit = guest_remark.userinit
                output_list.cid = guest_remark.CID
                output_list.chgdate = guest_remark.chgdate
                output_list.chgtime = guest_remark.chgtime
                output_list.bemerkung = guest_remark.bemerkung
                output_list.display_flag = guest_remark.display_flag
                output_list.res_integer = guest_remark.res_integer
                output_list.res_char = guest_remark.res_char
                output_list.g_recid = guest_remark._recid
                output_list.guest_name2 = guest.name

    elif payload_list.mode == 5:

        t_guest_remark = query(t_guest_remark_data, first=True)

        if t_guest_remark:

            # guest_remark = get_cache (Guest_remark, {"_recid": [(eq, t_guest_remark.g_recid)]})
            guest_remark = db_session.query(Guest_remark).filter(Guest_remark._recid == t_guest_remark.g_recid).with_for_update().first()

            if guest_remark:
                pass
                guest_remark.res_char[0] = t_guest_remark.res_char[0]
                guest_remark.userinit = t_guest_remark.userinit
                guest_remark.chgdate = get_current_date()
                guest_remark.chgtime = get_current_time_in_seconds()
                guest_remark.bemerkung = t_guest_remark.bemerkung
                guest_remark.display_flag = t_guest_remark.display_flag

                db_session.refresh(guest_remark,with_for_update=True)
                pass
                pass
                output_list.success_flag = True

    elif payload_list.mode == 6:

        t_guest_remark = query(t_guest_remark_data, first=True)

        if t_guest_remark:
            guest_remark = Guest_remark()
            db_session.add(guest_remark)

            guest_remark.gastnr = t_guest_remark.gastnr
            guest_remark.resnr = t_guest_remark.resnr
            guest_remark.reslinnr = t_guest_remark.reslinnr
            guest_remark.datum = bill_date
            guest_remark.zeit = get_current_time_in_seconds()
            guest_remark.userinit = t_guest_remark.userinit


            output_list.success_flag = True

    elif payload_list.mode == 7:

        # guest_remark = get_cache (Guest_remark, {"_recid": [(eq, payload_list.g_recid)]})
        guest_remark = db_session.query(Guest_remark).filter(Guest_remark._recid == payload_list.g_recid).with_for_update().first()

        if guest_remark:
            pass
            db_session.delete(guest_remark)
            db_session.refresh(guest_remark,with_for_update=True)
            pass
            output_list.success_flag = True

    elif payload_list.mode == 8:

        guest = get_cache (Guest, {"gastnr": [(eq, payload_list.gastnrmember)]})

        if guest:
            output_list.guest_name = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

        for guest_remark in db_session.query(Guest_remark).filter(
                 (Guest_remark.display_flag) & (Guest_remark.gastnr == payload_list.gastnrmember)).order_by(Guest_remark.res_char[inc_value(0)], Guest_remark.chgdate.desc(), Guest_remark.chgtime).all():

            if last_categ != guest_remark.res_char[0]:

                if last_categ != "":
                    output_list.remark = output_list.remark + chr_unicode(10)
                last_categ = guest_remark.res_char[0]
                output_list.remark = output_list.remark + guest_remark.res_char[0] + ":" + chr_unicode(10) +\
                        "- " + guest_remark.bemerkung + chr_unicode(10)


            else:
                output_list.remark = output_list.remark + "- " + guest_remark.bemerkung + chr_unicode(10)

    return generate_output()