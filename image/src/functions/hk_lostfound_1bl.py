from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bediener, Queasy, Res_history

def hk_lostfound_1bl(casetype:int, comments:str, sorttype:int, fr_date:date, to_date:date, user_init:str, rec_id:int):
    buf_s_list_list = []
    bediener = queasy = res_history = None

    s_list = buf_s_list = None

    s_list_list, S_list = create_model("S_list", {"nr":int, "betriebsnr":int, "s_recid":int, "date1":date, "zeit":str, "zinr":str, "userinit":str, "bezeich":str, "foundby":str, "submitted":str, "reportby":str, "report_date":date, "location":str, "refno":str, "phoneno":str, "claimby":str, "claim_date":date, "expired":date, "bemerk":str})
    buf_s_list_list, Buf_s_list = create_model_like(S_list)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal buf_s_list_list, bediener, queasy, res_history
        nonlocal casetype, comments, sorttype, fr_date, to_date, user_init, rec_id


        nonlocal s_list, buf_s_list
        nonlocal s_list_list, buf_s_list_list

        return {"buf-s-list": buf_s_list_list}

    def create_list():

        nonlocal buf_s_list_list, bediener, queasy, res_history
        nonlocal casetype, comments, sorttype, fr_date, to_date, user_init, rec_id


        nonlocal s_list, buf_s_list
        nonlocal s_list_list, buf_s_list_list

        i:int = 0

        queasy_obj_list = []
        for queasy, bediener in db_session.query(Queasy, Bediener).join(Bediener,(Bediener.nr == Queasy.number2)).filter(
                (Queasy.key == 7)).order_by(Queasy.date1, Queasy.char1, Queasy.number1).all():
            if queasy._recid in queasy_obj_list:
                continue
            else:
                queasy_obj_list.append(queasy._recid)


            s_list = S_list()
            s_list_list.append(s_list)

            s_list.nr = queasy.number3
            s_list.date1 = queasy.date1
            s_list.zeit = to_string(queasy.number1, "HH:MM:SS")
            s_list.zinr = queasy.char1
            s_list.userinit = bediener.userinit
            s_list.bezeich = entry(0, queasy.char2, chr(2))
            s_list.betriebsnr = queasy.betriebsnr
            s_list.s_recid = queasy._recid

            if num_entries(queasy.char2, chr(2)) > 1:
                s_list.bemerk = entry(1, queasy.char2, chr(2))
            for i in range(1,num_entries(queasy.char3, "|")  + 1) :
                # local_storage.debugging = local_storage.debugging + ",C3:" + queasy.char3
                if i == 1:
                    s_list.foundby = entry(0, queasy.char3, "|")
                elif i == 2:
                    s_list.submitted = entry(1, queasy.char3, "|")
                elif i == 3:
                    s_list.reportby = entry(2, queasy.char3, "|")
                elif i == 4:
                    if entry(3, queasy.char3, "|") != '99/99/99':
                        s_list.report_date = date_mdy(entry(3, queasy.char3, "|"))
                elif i == 5:
                    s_list.phoneno = entry(4, queasy.char3, "|")
                elif i == 6:
                    s_list.refno = entry(5, queasy.char3, "|")
                elif i == 7:
                    s_list.location = entry(6, queasy.char3, "|")
                elif i == 8:
                    s_list.claimby = entry(7, queasy.char3, "|")
                elif i == 9:
                    if entry(8, queasy.char3, "|") != '99/99/99':
                        s_list.claim_date = date_mdy(entry(8, queasy.char3, "|"))
                elif i == 10:
                    if entry(9, queasy.char3, "|") != '99/99/99':
                        s_list.expired = date_mdy(entry(9, queasy.char3, "|"))

        # --- Rd update ----
        buf_s_list_list = s_list_list


    def disp_it():

        nonlocal buf_s_list_list, bediener, queasy, res_history
        nonlocal casetype, comments, sorttype, fr_date, to_date, user_init, rec_id


        nonlocal s_list, buf_s_list
        nonlocal s_list_list, buf_s_list_list

        s:str = ""
        s = "*" + comments + "*"

        if comments == "":

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.betriebsnr == sorttype and s_list.date1 >= fr_date and s_list.date1 <= to_date), sort_by=[("nr",False)]):
                assign_it()

        else:

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.betriebsnr == sorttype and s_list.date1 >= fr_date and s_list.date1 <= to_date and re.match(s,s_list.bezeich, re.IGNORECASE)), sort_by=[("nr",False)]):
                assign_it()

    def assign_it():

        nonlocal buf_s_list_list, bediener, queasy, res_history
        nonlocal casetype, comments, sorttype, fr_date, to_date, user_init, rec_id

        nonlocal s_list, buf_s_list
        nonlocal s_list_list, buf_s_list_list


        buf_s_list = Buf_s_list()
        buf_s_list_list.append(buf_s_list)

        buffer_copy(s_list, buf_s_list)

    def del_lostfound():

        nonlocal buf_s_list_list, bediener, queasy, res_history
        nonlocal casetype, comments, sorttype, fr_date, to_date, user_init, rec_id


        nonlocal s_list, buf_s_list
        nonlocal s_list_list, buf_s_list_list

        if not bediener or not(bediener.userinit.lower()  == (user_init).lower()):
            bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Delete LostFound No" +\
                to_string(sorttype, ">>>9") +\
                " Room " + comments


        res_history.action = "HouseKeeping"
        pass

        if not queasy or not(queasy._recid == rec_id):
            queasy = db_session.query(Queasy).filter(
                (Queasy._recid == rec_id)).first()
        db_session.delete(queasy)

    if casetype == 1:
        s_list_list.clear()
        create_list()
        disp_it()

    elif casetype == 2:
        del_lostfound()
        s_list_list.clear()
        create_list()
        disp_it()

    return generate_output()