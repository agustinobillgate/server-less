#using conversion tools version: 1.0.0.112

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, Queasy, Res_history

def hk_lostfound_1bl(casetype:int, comments:string, sorttype:int, fr_date:date, to_date:date, user_init:string, rec_id:int):

    prepare_cache ([Bediener, Res_history])

    buf_s_list_list = []
    bediener = queasy = res_history = None

    s_list = buf_s_list = None

    s_list_list, S_list = create_model("S_list", {"nr":int, "betriebsnr":int, "s_recid":int, "date1":date, "zeit":string, "zinr":string, "userinit":string, "bezeich":string, "foundby":string, "submitted":string, "reportby":string, "report_date":date, "location":string, "refno":string, "phoneno":string, "claimby":string, "claim_date":date, "expired":date, "bemerk":string})
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

        queasy_obj_list = {}
        for queasy, bediener in db_session.query(Queasy, Bediener).join(Bediener,(Bediener.nr == Queasy.number2)).filter(
                 (Queasy.key == 7)).order_by(Queasy.date1, Queasy.char1, Queasy.number1).all():
            if queasy_obj_list.get(queasy._recid):
                continue
            else:
                queasy_obj_list[queasy._recid] = True


            s_list = S_list()
            s_list_list.append(s_list)

            s_list.nr = queasy.number3
            s_list.date1 = queasy.date1
            s_list.zeit = to_string(queasy.number1, "HH:MM:SS")
            s_list.zinr = queasy.char1
            s_list.userinit = bediener.userinit
            s_list.bezeich = entry(0, queasy.char2, chr_unicode(2))
            s_list.betriebsnr = queasy.betriebsnr
            s_list.s_recid = queasy._recid

            if num_entries(queasy.char2, chr_unicode(2)) > 1:
                s_list.bemerk = entry(1, queasy.char2, chr_unicode(2))
            for i in range(1,num_entries(queasy.char3, "|")  + 1) :

                if i == 1:
                    s_list.foundby = entry(0, queasy.char3, "|")
                elif i == 2:
                    s_list.submitted = entry(1, queasy.char3, "|")
                elif i == 3:
                    s_list.reportby = entry(2, queasy.char3, "|")
                elif i == 4:
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
                    s_list.claim_date = date_mdy(entry(8, queasy.char3, "|"))
                elif i == 10:
                    s_list.expired = date_mdy(entry(9, queasy.char3, "|"))


    def disp_it():

        nonlocal buf_s_list_list, bediener, queasy, res_history
        nonlocal casetype, comments, sorttype, fr_date, to_date, user_init, rec_id


        nonlocal s_list, buf_s_list
        nonlocal s_list_list, buf_s_list_list

        s:string = ""
        s = "*" + comments + "*"

        if comments == "":

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.betriebsnr == sorttype and s_list.date1 >= fr_date and s_list.date1 <= to_date), sort_by=[("date1",False),("zinr",False),("nr",False)]):

                queasy = get_cache (Queasy, {"_recid": [(eq, s_list.s_recid)]})

                if queasy:
                    assign_it()

        else:

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.betriebsnr == sorttype and s_list.date1 >= fr_date and s_list.date1 <= to_date and matches(s_list.bezeich,s)), sort_by=[("date1",False),("zinr",False),("nr",False)]):

                queasy = get_cache (Queasy, {"_recid": [(eq, s_list.s_recid)]})

                if queasy:
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

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
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
        pass

        queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})
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