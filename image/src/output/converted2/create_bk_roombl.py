#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date

t_bk_room_list, T_bk_room = create_model("T_bk_room", {"resnr":int, "resttype":int, "pax":int, "cutoffdate":date, "followupdate":date, "depositduedate":date, "salesid":string, "res_char":[string,9], "res_int":[int,9], "res_dec":[Decimal,9], "block_id":string, "block_code":string, "trace_code":string, "ratecode":string, "cutoffdays":int, "fo_resnr":int, "fo_reslinne":int, "ankunft":date, "abreise":date, "cancellation_no":string, "reason":string, "comments":string, "destination":string, "property":string, "cancel_penalty":Decimal})

def create_bk_roombl(casetype:int, t_bk_room_list:[T_bk_room]):


    t_bk_room = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal casetype


        nonlocal t_bk_room

        return {}

    if casetype == 1:

        t_bk_room = query(t_bk_room_list, first=True)

        if t_bk_room:

            bk_room = db_session.query(Bk_room).filter(
                     (Bk_room.resnr == t_bk_room.resnr)).first()

            if not bk_room:
                bk_room = Bk_room()
                bk_room_list.append(bk_room)

                bk_room.resnr = t_bk_room.resnr
                bk_room.block_code = t_bk_room.block_code
                bk_room.block_id = t_bk_room.block_id
                bk_room.resttype = t_bk_room.resttype
                bk_room.pax = t_bk_room.pax
                bk_room.ratecode = t_bk_room.ratecode
                bk_room.cutoffdate = t_bk_room.cutoffdate
                bk_room.followupdate = t_bk_room.followupdate
                bk_room.depositduedate = t_bk_room.depositduedate
                bk_room.trace_code = t_bk_room.trace_code
                bk_room.cutoffdays = t_bk_room.cutoffdays
                bk_room.salesid = t_bk_room.salesID
                bk_room.cancellation_no = t_bk_room.cancellation_no
                bk_room.reason = t_bk_room.reason
                bk_room.comments = t_bk_room.comments
                bk_room.destination = t_bk_room.destination
                bk_room.property = t_bk_room.property
                bk_room.cancel_penalty = t_bk_room.cancel_penalty


            else:
                bk_room.resttype = t_bk_room.resttype
                bk_room.pax = t_bk_room.pax
                bk_room.ratecode = t_bk_room.ratecode
                bk_room.cutoffdate = t_bk_room.cutoffdate
                bk_room.followupdate = t_bk_room.followupdate
                bk_room.depositduedate = t_bk_room.depositduedate
                bk_room.trace_code = t_bk_room.trace_code
                bk_room.cutoffdays = t_bk_room.cutoffdays
                bk_room.salesid = t_bk_room.salesID
                bk_room.cancellation_no = t_bk_room.cancellation_no
                bk_room.reason = t_bk_room.reason
                bk_room.comments = t_bk_room.comments
                bk_room.destination = t_bk_room.destination
                bk_room.property = t_bk_room.property
                bk_room.cancel_penalty = t_bk_room.cancel_penalty

    return generate_output()