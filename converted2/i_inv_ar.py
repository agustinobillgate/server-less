#using conversion tools version: 1.0.0.20

from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Debitor, Reservation, Res_line, Bill, Bill_line, Guest, Htparam, Bediener

def i_inv_ar():
    debitor = reservation = res_line = bill = bill_line = guest = htparam = bediener = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal debitor, reservation, res_line, bill, bill_line, guest, htparam, bediener

        return {}

    def inv_ar(curr_art:int, zinr:str, gastnr:int, gastnrmember:int, rechnr:int, saldo:decimal, saldo_foreign:decimal, bill_date:date, billname:str, userinit:str, voucher_nr:str):

        nonlocal debitor, reservation, res_line, bill, bill_line, guest, htparam, bediener

        comment:str = ""
        verstat:int = 0
        fsaldo:decimal = to_decimal("0.0")
        lsaldo:decimal = to_decimal("0.0")
        foreign_rate:bool = False
        currency_nr:int = 0
        double_currency:bool = False
        debt = None
        debt1 = None
        main_res = None
        resline = None
        bill1 = None
        bline = None
        guest1 = None
        Debt =  create_buffer("Debt",Debitor)
        Debt1 =  create_buffer("Debt1",Debitor)
        Main_res =  create_buffer("Main_res",Reservation)
        Resline =  create_buffer("Resline",Res_line)
        Bill1 =  create_buffer("Bill1",Bill)
        Bline =  create_buffer("Bline",Bill_line)
        Guest1 =  create_buffer("Guest1",Guest)

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 143)).first()
        foreign_rate = htparam.flogical

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 240)).first()
        double_currency = htparam.flogical

        bediener = db_session.query(Bediener).filter(
                 (func.lower(Bediener.userinit) == (userinit).lower())).first()

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 997)).first()

        if not htparam.flogical:

            return

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == gastnr)).first()
        billname = to_string(guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma, "x(36)")

        debt = db_session.query(Debt).filter(
                 (Debt.artnr == curr_art) & (Debt.rechnr == rechnr) & (Debt.opart == 0) & (Debt.rgdatum == bill_date) & (Debt.counter == 0) & (Debt.saldo == saldo)).first()

        if debt:

            debt1 = db_session.query(Debt1).filter(
                     (Debt1._recid == debt._recid)).first()

            if debt1:
                db_session.delete(debt1)
                pass

                return
            else:
                debt1 = Debitor()
                db_session.add(debt1)

                buffer_copy(debt, debt1)
                debt1.saldo =  - to_decimal(debt1.saldo)
                debt1.bediener_nr = bediener.nr
                debt1.transzeit = get_current_time_in_seconds()


                pass

                return

        bill1 = db_session.query(Bill1).filter(
                 (Bill1.rechnr == rechnr)).first()

        if bill1 and bill1.resnr != 0:

            resline = db_session.query(Resline).filter(
                     (Resline.resnr == bill1.resnr) & (Resline.active_flag <= 2) & (Resline.resstatus <= 8) & (Resline.zipreis != 0)).first()

            if not resline:

                resline = db_session.query(Resline).filter(
                         (Resline.resnr == bill1.resnr) & (Resline.active_flag <= 2) & (Resline.resstatus <= 8)).first()

            if resline:
                currency_nr = resline.betriebsnr

            main_res = db_session.query(Main_res).filter(
                     (Main_res.resnr == bill1.resnr)).first()

            if main_res:
                comment = main_res.groupname

            if comment == "" and gastnrmember != gastnr:

                guest1 = db_session.query(Guest1).filter(
                         (Guest1.gastnr == gastnrmember)).first()

                if guest1:
                    comment = to_string(guest1.name + "," + guest1.vorname1, "x(20)")

                    if resline:
                        comment = comment + " " + to_string(resline.ankunft) + "-" + to_string(resline.abreise)

            if bill1.reslinnr == 0:
                verstat = 1

            if main_res and main_res.insurance:

                resline = db_session.query(Resline).filter(
                         (Resline.resnr == main_res.resnr) & (Resline.reserve_dec != 0) & (Resline.reserve_dec != 1)).first()

                if resline:
                    saldo_foreign =  to_decimal(saldo) / to_decimal(resline.reserve_dec)

        elif bill1 and bill1.resnr == 0:
            comment = bill1.bilname
        debitor = Debitor()
        db_session.add(debitor)

        debitor.artnr = curr_art
        debitor.betrieb_gastmem = currency_nr
        debitor.zinr = zinr
        debitor.gastnr = gastnr
        debitor.gastnrmember = gastnrmember
        debitor.rechnr = rechnr
        debitor.saldo =  - to_decimal(saldo)
        debitor.transzeit = get_current_time_in_seconds()
        debitor.rgdatum = bill_date
        debitor.bediener_nr = bediener.nr
        debitor.name = billname
        debitor.vesrcod = comment
        debitor.verstat = verstat

        if double_currency or foreign_rate:
            debitor.vesrdep =  - to_decimal(saldo_foreign)

        if voucher_nr != "":

            if comment != "":
                debitor.vesrcod = voucher_nr + ";" + debitor.vesrcod


            else:
                debitor.vesrcod = voucher_nr


        pass