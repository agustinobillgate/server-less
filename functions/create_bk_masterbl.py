#using conversion tools version: 1.0.0.27

from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.create_bk_roombl import create_bk_roombl
from models import Bediener, Res_history

t_bk_master_list, T_bk_master = create_model("T_bk_master", {"resnr":int, "gastnr":int, "name":str, "startdate":date, "enddate":date, "resstatus":int, "market_nr":int, "source_nr":int, "sales_nr":int, "restype":int, "origins":int, "sob":int, "catering_flag":bool, "room_flag":bool, "cancel_flag":[bool,2], "cancel_type":str, "cancel_reason":str, "cancel_destination":str, "cancel_property":str, "res_character":[str,9], "res_int":[int,9], "res_dec":[decimal,9], "block_id":str, "block_code":str, "reservation_method":str, "rooming_list_due":date, "arrival_time":int, "departure_time":int, "payment":str, "cancel_penalty":decimal})
t_bk_room_list, T_bk_room = create_model("T_bk_room", {"resnr":int, "resttype":int, "pax":int, "cutoffdate":date, "followupdate":date, "depositduedate":date, "salesid":str, "res_char":[str,9], "res_int":[int,9], "res_dec":[decimal,9], "block_id":str, "block_code":str, "trace_code":str, "ratecode":str, "cutoffdays":int, "fo_resnr":int, "fo_reslinne":int, "ankunft":date, "abreise":date, "cancellation_no":str, "reason":str, "comments":str, "destination":str, "property":str, "cancel_penalty":decimal})
t_bk_catering_list, T_bk_catering = create_model("T_bk_catering", {"block_id":str, "attendees":int, "guaranteedflag":bool, "info":str, "cutoff_date":date, "deposit_due":date, "function_name":str, "contract_no":str, "sales_nr":int, "str_status":str, "cancellation_no":str, "reason":str, "comments":str, "amounpax":decimal, "totalamount":decimal})

def create_bk_masterbl(casetype:int, name:str, user_init:str, t_bk_master_list:[T_bk_master], t_bk_room_list:[T_bk_room], t_bk_catering_list:[T_bk_catering]):
    resnr:int = 0
    bk_count:int = 0
    oristr:str = ""
    chgstr:str = ""
    bediener = res_history = None

    t_bk_master = t_bk_room = t_bk_catering = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal resnr, bk_count, oristr, chgstr, bediener, res_history
        nonlocal casetype, name, user_init


        nonlocal t_bk_master, t_bk_room, t_bk_catering

        return {}


    bk_count = 0

    bk_master = db_session.query(Bk_master).order_by(Bk_master._recid.desc()).first()

    if bk_master:
        bk_count = bk_master.resnr + 1
    else:
        bk_count = 1

    if casetype == 1:

        t_bk_master = query(t_bk_master_list, first=True)

        if t_bk_master:

            bk_master = db_session.query(Bk_master).filter(
                     (Bk_master.block_id == t_bk_master.block_id)).first()

            if not bk_master:
                bk_master = Bk_master()
                bk_master_list.append(bk_master)

                bk_master.block_id = t_bk_master.block_id
                bk_master.block_code = t_bk_master.block_code
                bk_master.resnr = bk_count
                bk_master.gastnr = t_bk_master.gastnr
                bk_master.name = name
                bk_master.startdate = t_bk_master.startdate
                bk_master.enddate = t_bk_master.enddate
                bk_master.resstatus = t_bk_master.resstatus
                bk_master.market_nr = t_bk_master.market_nr
                bk_master.source_nr = t_bk_master.source_nr
                bk_master.sales_nr = t_bk_master.sales_nr
                bk_master.restype = t_bk_master.restype
                bk_master.origins = t_bk_master.origins
                bk_master.catering_flag = t_bk_master.catering_flag
                bk_master.reservation_method = t_bk_master.reservation_method
                bk_master.rooming_list_due = t_bk_master.rooming_list_due
                bk_master.arrival_time = t_bk_master.arrival_time
                bk_master.departure_time = t_bk_master.departure_time
                bk_master.payment = t_bk_master.payment

                t_bk_room = query(t_bk_room_list, first=True)

                if t_bk_room:
                    t_bk_room.resnr = bk_count
                    t_bk_room.block_id = t_bk_master.block_id


                    pass

                bediener = db_session.query(Bediener).filter(
                         (func.lower(Bediener.userinit) == (user_init).lower())).first()

                if bediener:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = bediener.nr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.action = "Banquet"
                    res_history.aenderung = "Create Master Plan With Block ID " + t_bk_master.block_id


                get_output(create_bk_roombl(1, t_bk_room_list))
            else:
                chgstr = ""
                oristr = ""
                resnr = bk_master.resnr

                if bk_master.gastnr != t_bk_master.gastnr:
                    oristr = to_string(bk_master.gastnr) + ";"
                    chgstr = to_string(t_bk_master.gastnr) + ";"

                elif bk_master.startdate != t_bk_master.startdate:
                    oristr = oristr + to_string(bk_master.startdate, "99/99/9999") + ";"
                    chgstr = chgstr + to_string(t_bk_master.startdate, "99/99/9999") + ";"

                elif bk_master.enddate != t_bk_master.enddate:
                    oristr = oristr + to_string(bk_master.enddate, "99/99/9999") + ";"
                    chgstr = chgstr + to_string(t_bk_master.enddate, "99/99/9999") + ";"

                elif bk_master.resstatus != t_bk_master.resstatus:
                    oristr = oristr + to_string(bk_master.resstatus) + ";"
                    chgstr = chgstr + to_string(t_bk_master.resstatus) + ";"

                elif bk_master.market_nr != t_bk_master.market_nr:
                    oristr = oristr + to_string(bk_master.market_nr) + ";"
                    chgstr = chgstr + to_string(t_bk_master.market_nr) + ";"

                elif bk_master.source_nr != t_bk_master.source_nr:
                    oristr = oristr + to_string(bk_master.source_nr) + ";"
                    chgstr = chgstr + to_string(t_bk_master.source_nr) + ";"

                elif bk_master.sales_nr != t_bk_master.sales_nr:
                    oristr = oristr + to_string(bk_master.sales_nr) + ";"
                    chgstr = chgstr + to_string(t_bk_master.sales_nr) + ";"

                elif bk_master.restype != t_bk_master.restype:
                    oristr = oristr + to_string(bk_master.restype) + ";"
                    chgstr = chgstr + to_string(t_bk_master.restype) + ";"

                elif bk_master.origins != t_bk_master.origins:
                    oristr = oristr + to_string(bk_master.origins) + ";"
                    chgstr = chgstr + to_string(t_bk_master.origins) + ";"

                elif bk_master.catering_flag != t_bk_master.catering_flag:
                    oristr = oristr + to_string(bk_master.catering_flag) + ";"
                    chgstr = chgstr + to_string(t_bk_master.catering_flag) + ";"


                bk_master.gastnr = t_bk_master.gastnr
                bk_master.name = name
                bk_master.startdate = t_bk_master.startdate
                bk_master.enddate = t_bk_master.enddate
                bk_master.resstatus = t_bk_master.resstatus
                bk_master.market_nr = t_bk_master.market_nr
                bk_master.source_nr = t_bk_master.source_nr
                bk_master.sales_nr = t_bk_master.sales_nr
                bk_master.restype = t_bk_master.restype
                bk_master.origins = t_bk_master.origins
                bk_master.catering_flag = t_bk_master.catering_flag
                bk_master.reservation_method = t_bk_master.reservation_method
                bk_master.rooming_list_due = t_bk_master.rooming_list_due
                bk_master.arrival_time = t_bk_master.arrival_time
                bk_master.departure_time = t_bk_master.departure_time
                bk_master.payment = t_bk_master.payment

                t_bk_room = query(t_bk_room_list, first=True)

                if t_bk_room:
                    t_bk_room.resnr = resnr


                    pass
                get_output(create_bk_roombl(1, t_bk_room_list))

        t_bk_catering = query(t_bk_catering_list, first=True)

        if t_bk_catering:

            bk_catering = db_session.query(Bk_catering).filter(
                     (Bk_catering.block_id == t_bk_catering.block_id)).first()

            if not bk_catering:
                bk_catering = Bk_catering()
                bk_catering_list.append(bk_catering)

                buffer_copy(t_bk_catering, bk_catering)
                pass
            else:
                buffer_copy(t_bk_catering, bk_catering)
                pass

    return generate_output()