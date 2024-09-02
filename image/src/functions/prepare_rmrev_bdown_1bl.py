from functions.additional_functions import *
import decimal
from datetime import date
import re
from sqlalchemy import func
from models import Htparam, Waehrung, Res_line, Guest_pr, Queasy

def prepare_rmrev_bdown_1bl():
    new_contrate = False
    curr_date = None
    bill_date = None
    price_decimal = 0
    long_digit = False
    foreign_rate = False
    curr_local = ""
    curr_foreign = ""
    exchg_rate = 0
    lnl_filepath = ""
    lnl_prog = ""
    fdate = None
    tdate = None
    htparam = waehrung = res_line = guest_pr = queasy = None

    rline = None

    Rline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_contrate, curr_date, bill_date, price_decimal, long_digit, foreign_rate, curr_local, curr_foreign, exchg_rate, lnl_filepath, lnl_prog, fdate, tdate, htparam, waehrung, res_line, guest_pr, queasy
        nonlocal rline


        nonlocal rline
        return {"new_contrate": new_contrate, "curr_date": curr_date, "bill_date": bill_date, "price_decimal": price_decimal, "long_digit": long_digit, "foreign_rate": foreign_rate, "curr_local": curr_local, "curr_foreign": curr_foreign, "exchg_rate": exchg_rate, "lnl_filepath": lnl_filepath, "lnl_prog": lnl_prog, "fdate": fdate, "tdate": tdate}

    def update_resline():

        nonlocal new_contrate, curr_date, bill_date, price_decimal, long_digit, foreign_rate, curr_local, curr_foreign, exchg_rate, lnl_filepath, lnl_prog, fdate, tdate, htparam, waehrung, res_line, guest_pr, queasy
        nonlocal rline


        nonlocal rline

        found:bool = False
        local_nr:int = 0
        foreign_nr:int = 0
        ct:str = ""
        contcode:str = ""
        Rline = Res_line

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == 1) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.betriebsnr == 0)).first()

        if not res_line:

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 152)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()
        local_nr = waehrungsnr

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            foreign_nr = waehrungsnr

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag == 1) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.betriebsnr == 0)).all():
            found = False

            rline = db_session.query(Rline).filter(
                    (Rline.resnr == res_line.resnr) &  (Rline.reslinnr == res_line.reslinnr)).first()

            if not res_line.adrflag:

                guest_pr = db_session.query(Guest_pr).filter(
                        (Guest_pr.gastnr == res_line.gastnr)).first()

                if guest_pr:
                    contcode = guest_pr.CODE
                    ct = res_line.zimmer_wunsch

                    if re.match(".*\$CODE\$.*",ct):
                        ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                        contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)

                    if res_line.reserve_int != 0:

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 18) &  (Queasy.number1 == res_line.reserve_int)).first()

                        if not queasy or (queasy and queasy.char3 == ""):

                            queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 2) &  (func.lower(Queasy.char1) == (contcode).lower())).first()
                    else:

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 2) &  (func.lower(Queasy.char1) == (contcode).lower())).first()

                    if queasy:

                        if queasy.key == 18:

                            waehrung = db_session.query(Waehrung).filter(
                                    (Waehrung.wabkurz == queasy.char3)).first()
                        else:

                            waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == queasy.number1)).first()

                        if waehrung:
                            found = True
                            rline.betriebsnr = waehrungsnr

            if not found:

                if res_line.adrflag  or not foreign_rate:
                    rline.betriebsnr = local_nr
                else:
                    rline.betriebsnr = foreign_nr

            rline = db_session.query(Rline).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 417)).first()

    if htparam.fchar != "":
        lnl_filepath = htparam.fchar

        if substring(lnl_filepath, len(lnl_filepath) - 1, 1) != "\\":
            lnl_filepath = lnl_filepath + "\\"
        lnl_filepath = lnl_filepath + lnl_prog

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 550)).first()

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    curr_date = htparam.fdate
    bill_date = curr_date
    tdate = curr_date


    fdate = date_mdy(get_month(tdate) , 1, get_year(tdate))

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()
    foreign_rate = htparam.flogical

    if not foreign_rate:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 143)).first()
        foreign_rate = htparam.flogical

    if foreign_rate:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 152)).first()
        curr_local = fchar

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()
        curr_foreign = fchar

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate = waehrung.ankauf / waehrung.einheit
        else:
            exchg_rate = 1
    update_resline()

    return generate_output()