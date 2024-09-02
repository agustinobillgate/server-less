from functions.additional_functions import *
import decimal
from datetime import date
from models import Res_line, Guest, Waehrung

def res_voucherbl(fr_date:date, to_date:date):
    r_list_list = []
    res_line = guest = waehrung = None

    r_list = None

    r_list_list, R_list = create_model_like(Res_line, {"rsvname":str, "voucher":str, "currency":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal r_list_list, res_line, guest, waehrung


        nonlocal r_list
        nonlocal r_list_list
        return {"r-list": r_list_list}

    def disp_it():

        nonlocal r_list_list, res_line, guest, waehrung


        nonlocal r_list
        nonlocal r_list_list

        i:int = 0
        str:str = ""
        r_list_list.clear()

        for res_line in db_session.query(Res_line).filter(
                (Res_line.ankunft >= fr_date) &  (Res_line.ankunft <= to_date) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != 99) &  (Res_line.zimmer_wunsch.op("~")(".*Voucher.*"))).all():
            r_list = R_list()
            r_list_list.append(r_list)

            buffer_copy(res_line, r_list)

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnr)).first()
            r_list.rsvName = guest.name + "," + guest.anredefirma

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == res_line.betriebsnr)).first()

            if waehrung:
                r_list.currency = waehrung.wabkurz
            for i in range(1,num_entries(r_list.zimmer_wunsch, ";") - 1 + 1) :
                str = entry(i - 1, r_list.zimmer_wunsch, ";")

                if substring(str, 0, 7) == "voucher":
                    r_list.voucher = substring(str, 7)
                    i = 9999


    disp_it()

    return generate_output()