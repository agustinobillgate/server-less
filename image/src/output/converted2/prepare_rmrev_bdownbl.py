#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Waehrung, Res_line, Guest_pr, Queasy

def prepare_rmrev_bdownbl():

    prepare_cache ([Htparam, Waehrung, Res_line, Guest_pr, Queasy])

    new_contrate = False
    curr_date = None
    bill_date = None
    price_decimal = 0
    long_digit = False
    foreign_rate = False
    curr_local = ""
    curr_foreign = ""
    exchg_rate = 1
    lnl_filepath = "\\vhp\\LnL\\"
    lnl_prog = "rmrev-bdown.lst"
    htparam = waehrung = res_line = guest_pr = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_contrate, curr_date, bill_date, price_decimal, long_digit, foreign_rate, curr_local, curr_foreign, exchg_rate, lnl_filepath, lnl_prog, htparam, waehrung, res_line, guest_pr, queasy

        return {"new_contrate": new_contrate, "curr_date": curr_date, "bill_date": bill_date, "price_decimal": price_decimal, "long_digit": long_digit, "foreign_rate": foreign_rate, "curr_local": curr_local, "curr_foreign": curr_foreign, "exchg_rate": exchg_rate, "lnl_filepath": lnl_filepath, "lnl_prog": lnl_prog}

    def update_resline():

        nonlocal new_contrate, curr_date, bill_date, price_decimal, long_digit, foreign_rate, curr_local, curr_foreign, exchg_rate, lnl_filepath, lnl_prog, htparam, waehrung, res_line, guest_pr, queasy

        found:bool = False
        local_nr:int = 0
        foreign_nr:int = 0
        ct:string = ""
        contcode:string = ""
        rline = None
        Rline =  create_buffer("Rline",Res_line)

        res_line = db_session.query(Res_line).filter(
                 (Res_line.active_flag == 1) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.betriebsnr == 0)).first()

        if not res_line:

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})
        local_nr = waehrung.waehrungsnr

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            foreign_nr = waehrung.waehrungsnr

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 1) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.betriebsnr == 0)).order_by(Res_line._recid).all():
            found = False

            rline = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

            if not res_line.adrflag:

                guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

                if guest_pr:
                    contcode = guest_pr.code
                    ct = res_line.zimmer_wunsch

                    if matches(ct,r"*$CODE$*"):
                        ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                        contcode = substring(ct, 0, get_index(ct, ";") - 1)

                    if res_line.reserve_int != 0:

                        queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

                        if not queasy or (queasy and queasy.char3 == ""):

                            queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, contcode)]})
                    else:

                        queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, contcode)]})

                    if queasy:

                        if queasy.key == 18:

                            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, queasy.char3)]})
                        else:

                            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, queasy.number1)]})

                        if waehrung:
                            found = True
                            rline.betriebsnr = waehrung.waehrungsnr

            if not found:

                if res_line.adrflag  or not foreign_rate:
                    rline.betriebsnr = local_nr
                else:
                    rline.betriebsnr = foreign_nr
            pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 417)]})

    if htparam.fchar != "":
        lnl_filepath = htparam.fchar

        if substring(lnl_filepath, length(lnl_filepath) - 1, 1) != ("\\").lower() :
            lnl_filepath = lnl_filepath + "\\"
        lnl_filepath = lnl_filepath + lnl_prog

    htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    curr_date = htparam.fdate
    bill_date = curr_date

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    foreign_rate = htparam.flogical

    if not foreign_rate:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
        foreign_rate = htparam.flogical

    if foreign_rate:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})
        curr_local = htparam.fchar

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})
        curr_foreign = htparam.fchar

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        else:
            exchg_rate =  to_decimal("1")
    update_resline()

    return generate_output()