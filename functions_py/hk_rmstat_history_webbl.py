#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 22/8/2025
# data kosong di .py
# sambil tunggu update, parameter from_date diisi manual.
#------------------------------------------
from functions.additional_functions import *
from sqlalchemy import func
from decimal import Decimal
from datetime import date
from models import Bediener, Res_history
from sqlalchemy import func

input_report_data, Input_report = create_model("Input_report", {"usrid":string, "room":string, "from_date":date, "to_date":date, "pvilanguages":int})

def hk_rmstat_history_webbl(input_report_data:[Input_report]):

    prepare_cache ([Bediener, Res_history])

    b1_list_data = []
    pvilanguage:int = 0
    lvcarea:string = "hk-statadmin"
    stat_list:List[string] = create_empty_list(10,"")
    bediener = res_history = None

    input_report = ubuff = b1_list = None

    b1_list_data, B1_list = create_model("B1_list", {"datum":date, "zinr":string, "from_stat":string, "to_stat":string, "remark":string, "username":string, "zeit":int})

    Ubuff = create_buffer("Ubuff",Bediener)


    db_session = local_storage.db_session

    # Rd, testonly from_date, to_date assign manual

    def generate_output():
        nonlocal b1_list_data, pvilanguage, lvcarea, stat_list, bediener, res_history
        nonlocal ubuff


        nonlocal input_report, ubuff, b1_list
        nonlocal b1_list_data

        return {"b1-list": b1_list_data}

    def disp_it():

        nonlocal b1_list_data, pvilanguage, lvcarea, stat_list, bediener, res_history
        nonlocal ubuff

        nonlocal input_report, ubuff, b1_list
        nonlocal b1_list_data
        # Rd, 22/8/2025, from_date diisi manual
        input_from_date = date(2024,9,24)
        
        if input_report.usrid != "" and input_report.room.strip() != "":
            # Rd 22/8/2025, input_report_data
            # bediener = get_cache (Bediener, {"userinit": [(eq, trim(entry(0, usrid, "-")))]})
            bediener = get_cache (Bediener, {"userinit": [(eq, trim(entry(0, input_report_data.usrid, "-")))]})

            res_history_obj_list = {}
            res_history = Res_history()
            ubuff = Bediener()

            # Rd 22/8/2025, input_report_data
            # for res_history.datum, res_history.aenderung, res_history.zeit, res_history._recid, ubuff.nr, ubuff._recid, ubuff.username in db_session.query(Res_history.datum, Res_history.aenderung, Res_history.zeit, Res_history._recid, Ubuff.nr, Ubuff._recid, Ubuff.username).join(Ubuff,(Ubuff.nr == Res_history.nr)).filter(
            #          (Res_history.datum >= from_date) & (Res_history.datum <= to_date) & (Res_history.action == ("HouseKeeping").lower()) & (num_entries(Res_history.aenderung, "|") > 3) & (Res_history.nr == bediener.nr) & (entry(1, Res_history.aenderung, " ") == input_report.room)).order_by(Res_history.datum, Res_history.zeit).all():
            
            for res_history.datum, res_history.aenderung, res_history.zeit, res_history._recid, ubuff.nr, ubuff._recid, ubuff.username in db_session.query(Res_history.datum, Res_history.aenderung, Res_history.zeit, Res_history._recid, Ubuff.nr, Ubuff._recid, Ubuff.username).join(Ubuff,(Ubuff.nr == Res_history.nr)).filter(
                     (Res_history.datum >= input_from_date) & (Res_history.datum <= input_report.to_date) & (Res_history.action == "HouseKeeping")  & (Res_history.nr == bediener.nr) & (entry(1, Res_history.aenderung, " ") == input_report.room)).order_by(Res_history.datum, Res_history.zeit).all():
                
                if num_entries(res_history.aenderung, "|") > 3:

                    if res_history_obj_list.get(res_history._recid):
                        continue
                    else:
                        res_history_obj_list[res_history._recid] = True

                    assign_it()

            return
        # Rd 22/8/2025, input_report_data
        # elif usrid != "" and input_report.room == "":
        elif input_report.usrid.strip() != "" and input_report.room.strip() == "":
            # Rd 22/8/2025, input_report_data
            # bediener = get_cache (Bediener, {"userinit": [(eq, trim(entry(0, usrid, "-")))]})
            bediener = get_cache (Bediener, {"userinit": [(eq, trim(entry(0, input_report_data.usrid, "-")))]})

            res_history_obj_list = {}
            res_history = Res_history()
            ubuff = Bediener()

            # Rd 22/8/2025, input_report_data
            # for res_history.datum, res_history.aenderung, res_history.zeit, res_history._recid, ubuff.nr, ubuff._recid, ubuff.username in db_session.query(Res_history.datum, Res_history.aenderung, Res_history.zeit, Res_history._recid, Ubuff.nr, Ubuff._recid, Ubuff.username).join(Ubuff,(Ubuff.nr == Res_history.nr)).filter(
            #          (Res_history.datum >= from_date) & (Res_history.datum <= to_date) & (Res_history.action == "HouseKeeping") & (num_entries(Res_history.aenderung, "|") > 3) & (Res_history.nr == bediener.nr)).order_by(Res_history.datum, Res_history.zeit).all():
            for res_history.datum, res_history.aenderung, res_history.zeit, res_history._recid, ubuff.nr, ubuff._recid, ubuff.username in db_session.query(Res_history.datum, Res_history.aenderung, Res_history.zeit, Res_history._recid, Ubuff.nr, Ubuff._recid, Ubuff.username).join(Ubuff,(Ubuff.nr == Res_history.nr)).filter(
                     (Res_history.datum >= input_from_date) & (Res_history.datum <= input_report.to_date) & (Res_history.action == "HouseKeeping")  & (Res_history.nr == bediener.nr)).order_by(Res_history.datum, Res_history.zeit).all():

                if  num_entries(res_history.aenderung, "|") > 3:
                    if res_history_obj_list.get(res_history._recid):
                        continue
                    else:
                        res_history_obj_list[res_history._recid] = True


                    assign_it()

            return

        # Rd 22/8/2025, input_report_data
        # elif usrid != "" and input_report.room == "":
        elif input_report.usrid.strip() == "" and input_report.room.strip() == "":
            res_history_obj_list = {}
            res_history = Res_history()
            ubuff = Bediener()

            # Rd 22/8/2025, input_report_data
            # for res_history.datum, res_history.aenderung, res_history.zeit, res_history._recid, ubuff.nr, ubuff._recid, ubuff.username in db_session.query(Res_history.datum, Res_history.aenderung, Res_history.zeit, Res_history._recid, Ubuff.nr, Ubuff._recid, Ubuff.username).join(Ubuff,(Ubuff.nr == Res_history.nr)).filter(
            #          (Res_history.datum >= from_date) & (Res_history.datum <= to_date) & (Res_history.action == ("HouseKeeping").lower()) & (num_entries(Res_history.aenderung, "|") > 3) & (entry(1, Res_history.aenderung, " ") == input_report.room)).order_by(Res_history.datum, Res_history.zeit).all():

            for res_history, ubuff in db_session.query(Res_history, Ubuff).join(Ubuff,(Ubuff.nr == Res_history.nr)).filter(
                     (Res_history.datum >= input_from_date) & 
                     (Res_history.datum <= input_report.to_date) & 
                     (Res_history.action == "HouseKeeping") 
                    ).order_by(Res_history.datum, Res_history.zeit).all():
                
                if num_entries(res_history.aenderung, "|") > 3:
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

            # Rd 22/8/2025, input_report_data
            # for res_history.datum, res_history.aenderung, res_history.zeit, res_history._recid, ubuff.nr, ubuff._recid, ubuff.username in db_session.query(Res_history.datum, Res_history.aenderung, Res_history.zeit, Res_history._recid, Ubuff.nr, Ubuff._recid, Ubuff.username).join(Ubuff,(Ubuff.nr == Res_history.nr)).filter(
            #          (Res_history.datum >= from_date) & (Res_history.datum <= to_date) & (Res_history.action == ("HouseKeeping").lower()) & (num_entries(Res_history.aenderung, "|") > 3)).order_by(Res_history.datum, Res_history.zeit).all():

            for res_history.datum, res_history.aenderung, res_history.zeit, res_history._recid, ubuff.nr, ubuff._recid, ubuff.username in db_session.query(Res_history.datum, Res_history.aenderung, Res_history.zeit, Res_history._recid, Ubuff.nr, Ubuff._recid, Ubuff.username).join(Ubuff,(Ubuff.nr == Res_history.nr)).filter(
                     (Res_history.datum >= input_from_date) & (Res_history.datum <= input_report.to_date) & (Res_history.action == "HouseKeeping") ).order_by(Res_history.datum, Res_history.zeit).all():
                
                if num_entries(res_history.aenderung, "|") > 3:
                    if res_history_obj_list.get(res_history._recid):
                        continue
                    else:
                        res_history_obj_list[res_history._recid] = True
                    assign_it()

            return


    def assign_it():

        nonlocal b1_list_data, pvilanguage, lvcarea, stat_list, bediener, res_history
        nonlocal ubuff


        nonlocal input_report, ubuff, b1_list
        nonlocal b1_list_data

        b1_list = B1_list()
        b1_list_data.append(b1_list)

        b1_list.datum = res_history.datum
        b1_list.zinr = entry(1, res_history.aenderung, " ")
        b1_list.from_stat = stat_list[to_int(entry(1, res_history.aenderung, "|")) + 1 - 1]
        b1_list.to_stat = stat_list[to_int(entry(2, res_history.aenderung, "|")) + 1 - 1]
        b1_list.remark = entry(1, res_history.aenderung, "|Reason:")
        b1_list.zeit = res_history.zeit

        if ubuff:
            b1_list.username = ubuff.username


    input_report = query(input_report_data, filters=(lambda input_report: date(2024,9,1) is not None and input_report.to_date is not None), first=True)
    if input_report:
        pvilanguage = input_report.pvilanguages
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