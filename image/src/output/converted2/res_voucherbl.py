#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Guest, Waehrung

def res_voucherbl(fr_date:date, to_date:date):

    prepare_cache ([Guest, Waehrung])

    r_list_list = []
    res_line = guest = waehrung = None

    r_list = None

    r_list_list, R_list = create_model_like(Res_line, {"rsvname":string, "voucher":string, "currency":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal r_list_list, res_line, guest, waehrung
        nonlocal fr_date, to_date


        nonlocal r_list
        nonlocal r_list_list

        return {"r-list": r_list_list}

    def disp_it():

        nonlocal r_list_list, res_line, guest, waehrung
        nonlocal fr_date, to_date


        nonlocal r_list
        nonlocal r_list_list

        i:int = 0
        str:string = ""
        r_list_list.clear()

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.ankunft >= fr_date) & (Res_line.ankunft <= to_date) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (matches(Res_line.zimmer_wunsch,("*Voucher*")))).order_by(Res_line._recid).all():
            r_list = R_list()
            r_list_list.append(r_list)

            buffer_copy(res_line, r_list)

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
            r_list.rsvname = guest.name + "," + guest.anredefirma

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

            if waehrung:
                r_list.currency = waehrung.wabkurz
            for i in range(1,num_entries(r_list.zimmer_wunsch, ";") - 1 + 1) :
                str = entry(i - 1, r_list.zimmer_wunsch, ";")

                if substring(str, 0, 7) == ("voucher").lower() :
                    r_list.voucher = substring(str, 7)
                    i = 9999

    disp_it()

    return generate_output()