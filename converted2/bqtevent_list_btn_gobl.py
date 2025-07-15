#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Bk_veran, Bk_func

def bqtevent_list_btn_gobl(from_date:date, to_date:date):

    prepare_cache ([Bk_func])

    output_list_data = []
    guest = bk_veran = bk_func = None

    output_list = None

    output_list_data, Output_list = create_model("Output_list", {"resstatus":string, "compname":string, "event":string, "pax":string, "venue":string, "booker":string, "date":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, guest, bk_veran, bk_func
        nonlocal from_date, to_date


        nonlocal output_list
        nonlocal output_list_data

        return {"output-list": output_list_data}

    def event_list():

        nonlocal output_list_data, guest, bk_veran, bk_func
        nonlocal from_date, to_date


        nonlocal output_list
        nonlocal output_list_data

        gast = None
        resstatus:string = ""
        str_len:int = 0
        Gast =  create_buffer("Gast",Guest)
        output_list_data.clear()

        bk_func_obj_list = {}
        for bk_func, bk_veran in db_session.query(Bk_func, Bk_veran).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).filter(
                 (Bk_func.bis_datum >= from_date) & (Bk_func.bis_datum <= to_date) & (Bk_func.resstatus <= 3)).order_by(Bk_func.bis_datum).all():
            if bk_func_obj_list.get(bk_func._recid):
                continue
            else:
                bk_func_obj_list[bk_func._recid] = True


            output_list = Output_list()
            output_list_data.append(output_list)


            if bk_func.resstatus == 1:
                output_list.resstatus = "F"

            elif bk_func.resstatus == 2:
                output_list.resstatus = "T"

            elif bk_func.resstatus == 3:
                output_list.resstatus = "W"
            output_list.compname = bk_func.adurch
            output_list.event = bk_func.zweck[0]
            output_list.pax = to_string(bk_func.rpersonen[0])
            output_list.venue = bk_func.raeume[0]
            output_list.booker = bk_func.v_kontaktperson[0]
            output_list.date = bk_func.datum

    event_list()

    return generate_output()