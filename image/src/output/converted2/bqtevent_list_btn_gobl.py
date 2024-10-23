from functions.additional_functions import *
import decimal
from datetime import date
from models import Guest, Bk_veran, Bk_func

def bqtevent_list_btn_gobl(from_date:date, to_date:date):
    output_list_list = []
    guest = bk_veran = bk_func = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"resstatus":str, "compname":str, "event":str, "pax":str, "venue":str, "booker":str, "date":date})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, guest, bk_veran, bk_func
        nonlocal from_date, to_date


        nonlocal output_list
        nonlocal output_list_list
        return {"output-list": output_list_list}

    def event_list():

        nonlocal output_list_list, guest, bk_veran, bk_func
        nonlocal from_date, to_date


        nonlocal output_list
        nonlocal output_list_list

        gast = None
        resstatus:str = ""
        str_len:int = 0
        Gast =  create_buffer("Gast",Guest)
        output_list_list.clear()

        bk_func_obj_list = []
        for bk_func, bk_veran in db_session.query(Bk_func, Bk_veran).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).filter(
                 (Bk_func.bis_datum >= from_date) & (Bk_func.bis_datum <= to_date) & (Bk_func.resstatus <= 3)).order_by(Bk_func.bis_datum).all():
            if bk_func._recid in bk_func_obj_list:
                continue
            else:
                bk_func_obj_list.append(bk_func._recid)


            output_list = Output_list()
            output_list_list.append(output_list)


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