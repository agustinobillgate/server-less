#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, Res_history

input_report_list, Input_report = create_model("Input_report", {"usrid":string, "room":string, "from_date":date, "to_date":date, "pvilanguages":int})

def hk_rmstat_history_webbl(input_report_list:[Input_report]):

    prepare_cache ([Bediener, Res_history])

    b1_list_list = []
    pvilanguage:int = 0
    lvcarea:string = "hk-statadmin"
    stat_list:List[string] = create_empty_list(10,"")
    bediener = res_history = None

    input_report = ubuff = b1_list = None

    b1_list_list, B1_list = create_model("B1_list", {"datum":date, "zinr":string, "from_stat":string, "to_stat":string, "remark":string, "username":string, "zeit":int})

    Ubuff = create_buffer("Ubuff",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_list, pvilanguage, lvcarea, stat_list, bediener, res_history
        nonlocal ubuff


        nonlocal input_report, ubuff, b1_list
        nonlocal b1_list_list

        return {"b1-list": b1_list_list}

    def disp_it():

        nonlocal b1_list_list, pvilanguage, lvcarea, stat_list, bediener, res_history
        nonlocal ubuff


        nonlocal input_report, ubuff, b1_list
        nonlocal b1_list_list

        if input_report.usrID != "" and input_report.room != "":

            bediener = get_cache (Bediener, {"userinit": [(eq, trim(entry(0, usrid, "-")))]})

            res_history_obj_list = {}
            res_history = Res_history()
            ubuff = Bediener()
            for res_history.datum, res_history.aenderung, res_history.zeit, res_history._recid, ubuff.nr, ubuff._recid, ubuff.username in db_session.query(Res_history.datum, Res_history.aenderung, Res_history.zeit, Res_history._recid, Ubuff.nr, Ubuff._recid, Ubuff.username).join(Ubuff,(Ubuff.nr == Res_history.nr)).filter(
                     (Res_history.datum >= from_date) & (Res_history.datum <= to_date) & (Res_history.action == ("HouseKeeping").lower()) & (num_entries(Res_history.aenderung, "|") > 3) & (Res_history.nr == bediener.nr) & (entry(1, Res_history.aenderung, " ") == input_report.room)).order_by(Res_history.datum, Res_history.zeit).all():
                if res_history_obj_list.get(res_history._recid):
                    continue
                else:
                    res_history_obj_list[res_history._recid] = True


                assign_it()

            return

        elif usrID != "" and input_report.room == "":

            bediener = get_cache (Bediener, {"userinit": [(eq, trim(entry(0, usrid, "-")))]})

            res_history_obj_list = {}
            res_history = Res_history()
            ubuff = Bediener()
            for res_history.datum, res_history.aenderung, res_history.zeit, res_history._recid, ubuff.nr, ubuff._recid, ubuff.username in db_session.query(Res_history.datum, Res_history.aenderung, Res_history.zeit, Res_history._recid, Ubuff.nr, Ubuff._recid, Ubuff.username).join(Ubuff,(Ubuff.nr == Res_history.nr)).filter(
                     (Res_history.datum >= from_date) & (Res_history.datum <= to_date) & (Res_history.action == ("HouseKeeping").lower()) & (num_entries(Res_history.aenderung, "|") > 3) & (Res_history.nr == bediener.nr)).order_by(Res_history.datum, Res_history.zeit).all():
                if res_history_obj_list.get(res_history._recid):
                    continue
                else:
                    res_history_obj_list[res_history._recid] = True


                assign_it()

            return

        elif usrID == "" and input_report.room != "":

            res_history_obj_list = {}
            res_history = Res_history()
            ubuff = Bediener()
            for res_history.datum, res_history.aenderung, res_history.zeit, res_history._recid, ubuff.nr, ubuff._recid, ubuff.username in db_session.query(Res_history.datum, Res_history.aenderung, Res_history.zeit, Res_history._recid, Ubuff.nr, Ubuff._recid, Ubuff.username).join(Ubuff,(Ubuff.nr == Res_history.nr)).filter(
                     (Res_history.datum >= from_date) & (Res_history.datum <= to_date) & (Res_history.action == ("HouseKeeping").lower()) & (num_entries(Res_history.aenderung, "|") > 3) & (entry(1, Res_history.aenderung, " ") == input_report.room)).order_by(Res_history.datum, Res_history.zeit).all():
                if res_history_obj_list.get(res_history._recid):
                    continue
                else:
                    res_history_obj_list[res_history._recid] = True


                assign_it()

            return
        else:

            res_history_obj_list = {}
            res_history = Res_history()
            ubuff = Bediener()
            for res_history.datum, res_history.aenderung, res_history.zeit, res_history._recid, ubuff.nr, ubuff._recid, ubuff.username in db_session.query(Res_history.datum, Res_history.aenderung, Res_history.zeit, Res_history._recid, Ubuff.nr, Ubuff._recid, Ubuff.username).join(Ubuff,(Ubuff.nr == Res_history.nr)).filter(
                     (Res_history.datum >= from_date) & (Res_history.datum <= to_date) & (Res_history.action == ("HouseKeeping").lower()) & (num_entries(Res_history.aenderung, "|") > 3)).order_by(Res_history.datum, Res_history.zeit).all():
                if res_history_obj_list.get(res_history._recid):
                    continue
                else:
                    res_history_obj_list[res_history._recid] = True


                assign_it()

            return


    def assign_it():

        nonlocal b1_list_list, pvilanguage, lvcarea, stat_list, bediener, res_history
        nonlocal ubuff


        nonlocal input_report, ubuff, b1_list
        nonlocal b1_list_list


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.datum = res_history.datum
        b1_list.zinr = entry(1, res_history.aenderung, " ")
        b1_list.from_stat = stat_list[to_int(entry(1, res_history.aenderung, "|")) + 1 - 1]
        b1_list.to_stat = stat_list[to_int(entry(2, res_history.aenderung, "|")) + 1 - 1]
        b1_list.remark = substring(entry(3, res_history.aenderung, "|Reason:") , 7)
        b1_list.zeit = res_history.zeit

        if ubuff:
            b1_list.username = ubuff.username

    input_report = query(input_report_list, filters=(lambda input_report: input_report.from_date != None and input_report.to_date != None), first=True)

    if input_report:
        pvilanguage = input_report.pvILanguages
        stat_list[0] = translateExtended ("Vacant Clean Checked", lvcarea, "")
        stat_list[1] = translateExtended ("Vacant Clean Unchecked", lvcarea, "")
        stat_list[2] = translateExtended ("Vacant Dirty", lvcarea, "")
        stat_list[3] = translateExtended ("Expected Departure", lvcarea, "")
        stat_list[4] = translateExtended ("Occupied Dirty", lvcarea, "")
        stat_list[5] = translateExtended ("Occupied Cleaned", lvcarea, "")
        stat_list[6] = translateExtended ("Out-of-Order", lvcarea, "")
        stat_list[7] = translateExtended ("Off-Market", lvcarea, "")
        stat_list[8] = translateExtended ("Do not Disturb", lvcarea, "")
        stat_list[9] = translateExtended ("Out-of-Service", lvcarea, "")
        disp_it()

    return generate_output()