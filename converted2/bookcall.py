from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.create_newbill import create_newbill
from models import Bill, Parameters, Res_line, Htparam, Artikel, Waehrung, Counters, Bill_line, Umsatz, Billjournal, Master, Mast_art

def bookcall(zinr:str, calldate:date, calltime:int, destination:str, duration:int, rufnummer:str, amount:decimal):
    success = False
    rechnr = 0
    versioninfo:str = "@(#) BookCall.p 1.0.2 Sindata 2003/11/17"
    bil_recid:int = 0
    epreis:decimal = to_decimal("0.0")
    artnr:int = 0
    resnr:int = 0
    billno:int = 0
    master_flag:bool = False
    bill_date:date = None
    user_init:str = ""
    bookflag:int = 0
    foreign_rate:bool = False
    double_currency:bool = False
    exchg_rate:decimal = 1
    amount_foreign:decimal = to_decimal("0.0")
    price_decimal:int = 0
    calls_type:int = 0
    bill = parameters = res_line = htparam = artikel = waehrung = counters = bill_line = umsatz = billjournal = master = mast_art = None

    bill1 = prefix_list = None

    prefix_list_list, Prefix_list = create_model("Prefix_list", {"prefix":str, "codelan":int})

    Bill1 = create_buffer("Bill1",Bill)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success, rechnr, versioninfo, bil_recid, epreis, artnr, resnr, billno, master_flag, bill_date, user_init, bookflag, foreign_rate, double_currency, exchg_rate, amount_foreign, price_decimal, calls_type, bill, parameters, res_line, htparam, artikel, waehrung, counters, bill_line, umsatz, billjournal, master, mast_art
        nonlocal zinr, calldate, calltime, destination, duration, rufnummer, amount
        nonlocal bill1


        nonlocal bill1, prefix_list
        nonlocal prefix_list_list

        return {"success": success, "rechnr": rechnr}

    def update_masterbill():

        nonlocal success, rechnr, versioninfo, bil_recid, epreis, artnr, resnr, billno, master_flag, bill_date, user_init, bookflag, foreign_rate, double_currency, exchg_rate, amount_foreign, price_decimal, calls_type, bill, parameters, res_line, htparam, artikel, waehrung, counters, bill_line, umsatz, billjournal, master, mast_art
        nonlocal zinr, calldate, calltime, destination, duration, rufnummer, amount
        nonlocal bill1


        nonlocal bill1, prefix_list
        nonlocal prefix_list_list

        master_flag = None
        bookflag = None
        mbill = None
        resline = None

        def generate_inner_output():
            return (master_flag, bookflag)

        Mbill =  create_buffer("Mbill",Bill)
        Resline =  create_buffer("Resline",Res_line)

        master = db_session.query(Master).filter(
                 (Master.resnr == resnr) & (Master.active) & (Master.flag == 0)).first()

        if not master:

            return generate_inner_output()

        if master.umsatzart[3] :
            master_flag = True
        else:

            mast_art = db_session.query(Mast_art).filter(
                     (Mast_art.resnr == master.resnr) & (Mast_art.departement == artikel.departement) & (Mast_art.artnr == artikel.artnr)).first()
            master_flag = (None != mast_art)

        if master_flag:

            mbill = db_session.query(Mbill).filter(
                     (Mbill.resnr == resnr) & (Mbill.reslinnr == 0)).first()

            if not mbill:
                master_flag = False

                return generate_inner_output()
            mbill.sonst_umsatz =  to_decimal(mbill.sonst_umsatz) + to_decimal(amount)
            mbill.gesamtumsatz =  to_decimal(mbill.gesamtumsatz) + to_decimal(amount)
            mbill.rgdruck = 0
            mbill.saldo =  to_decimal(mbill.saldo) + to_decimal(amount)
            mbill.mwst[98] = mbill.mwst[98] + amount_foreign
            mbill.datum = bill_date

            if mbill.rechnr == 0:

                counters = db_session.query(Counters).filter(
                         (Counters.counter_no == 3)).first()
                counters.counter = counters.counter + 1
                mbill.rechnr = counters.counter
                master.rechnr = mbill.rechnr
            rechnr = mbill.rechnr
            bill_line = Bill_line()
            db_session.add(bill_line)

            bill_line.rechnr = mbill.rechnr
            bill_line.artnr = artnr
            bill_line.bezeich = artikel.bezeich + " - " +\
                    substring(rufnummer, 0, len(rufnummer))
            bill_line.anzahl = 1
            bill_line.betrag =  to_decimal(amount)
            bill_line.fremdwbetrag =  to_decimal(amount_foreign)
            bill_line.zinr = zinr
            bill_line.departement = artikel.departement
            bill_line.epreis =  to_decimal(epreis)
            bill_line.zeit = get_current_time_in_seconds()
            bill_line.userinit = user_init
            bill_line.arrangement = res_line.arrangement
            bill_line.bill_datum = bill_date
            bill_line.origin_id = "CALLS " + to_string(calldate) + ";" +\
                    to_string(calltime, "HH:MM") + ";" + rufnummer + ";" +\
                    destination + ";" + to_string(duration, "HH:MM:SS") + ";"

            umsatz = db_session.query(Umsatz).filter(
                     (Umsatz.artnr == artnr) & (Umsatz.departement == artikel.departement) & (Umsatz.datum == bill_date)).first()

            if not umsatz:
                umsatz = Umsatz()
                db_session.add(umsatz)

                umsatz.artnr = artnr
                umsatz.datum = bill_date
                umsatz.departement = artikel.departement


            umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
            umsatz.anzahl = umsatz.anzahl + 1


            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = mbill.rechnr
            billjournal.artnr = artnr
            billjournal.anzahl = 1
            billjournal.betrag =  to_decimal(amount)
            billjournal.fremdwaehrng =  to_decimal(amount_foreign)
            billjournal.bezeich = artikel.bezeich
            billjournal.zinr = zinr
            billjournal.departement = artikel.departement
            billjournal.epreis =  to_decimal(epreis)
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_date


            bookflag = 1
            success = True

        return generate_inner_output()


    for parameters in db_session.query(Parameters).filter(
             (func.lower(Parameters.progname) == ("interface").lower()) & (func.lower(Parameters.section) == ("prefix").lower())).order_by(Parameters._recid).all():

        if substring(parameters.vstring, 1, 1) != ("0").lower() :

            prefix_list = query(prefix_list_list, filters=(lambda prefix_list: prefix_list.prefix == parameters.vstring), first=True)

            if not prefix_list:
                prefix_list = Prefix_list()
                prefix_list_list.append(prefix_list)

                prefix_list.prefix = parameters.vstring
                prefix_list.codelan = len(parameters.vstring)

    if zinr == "":

        return generate_output()

    if substring(rufnummer, 0, 2) == ("00").lower() :
        calls_type = 2

    elif substring(rufnummer, 0, 1) == ("0").lower() :
        calls_type = 1

        prefix_list = query(prefix_list_list, filters=(lambda prefix_list: prefix_list.prefix == substring(rufnummer, 0, len(prefix_list.prefix))), first=True)

        if prefix_list:
            calls_type = 2

    res_line = db_session.query(Res_line).filter(
             (Res_line.resstatus == 6) & (func.lower(Res_line.zinr) == (zinr).lower())).first()

    if not res_line:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resstatus == 13) & (func.lower(Res_line.zinr) == (zinr).lower())).first()

        if not res_line:

            return generate_output()
    resnr = res_line.resnr

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 113)).first()
    artnr = htparam.finteger

    artikel = db_session.query(Artikel).filter(
             (Artikel.artnr == artnr) & (Artikel.departement == 0) & (Artikel.artnr != 0)).first()

    if not artikel:

        return generate_output()

    if calls_type == 1:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 114)).first()

        artikel = db_session.query(Artikel).filter(
                 (Artikel.artnr == htparam.finteger) & (Artikel.departement == 0) & (Artikel.artart == 0) & (Artikel.artnr != 0)).first()

        if artikel:
            artnr = htparam.finteger

    elif calls_type == 2:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 115)).first()

        artikel = db_session.query(Artikel).filter(
                 (Artikel.artnr == htparam.finteger) & (Artikel.departement == 0) & (Artikel.artart == 0) & (Artikel.artnr != 0)).first()

        if artikel:
            artnr = htparam.finteger
        else:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 114)).first()

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == htparam.finteger) & (Artikel.departement == 0) & (Artikel.artart == 0) & (Artikel.artnr != 0)).first()

            if artikel:
                artnr = htparam.finteger

    bill1 = db_session.query(Bill1).filter(
             (Bill1.zinr == res_line.zinr) & (Bill1.reslinnr == res_line.reslinnr) & (Bill1.resnr == res_line.resnr)).first()

    if not bill1:

        return generate_output()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 335)).first()
    billno = htparam.finteger

    if billno == 0:
        billno = 1

    if billno > 2:
        billno = 2

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 253)).first()

    if htparam.flogical:
        bill_date = bill_date + timedelta(days=1)

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 317)).first()
    user_init = htparam.fchar

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 559)).first()

    if htparam.flogical and len(rufnummer) > 3:
        rufnummer = substring(rufnummer, 0, len(rufnummer) - 3) + "xxx"

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 143)).first()
    foreign_rate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 240)).first()
    double_currency = htparam.flogical
    pass

    if artikel.pricetab and artikel.betriebsnr != 0:

        waehrung = db_session.query(Waehrung).filter(
                 (Waehrung.waehrungsnr == artikel.betriebsnr) & (Waehrung.ankauf != 0)).first()

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    elif foreign_rate or double_currency:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                 (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    if (artikel.pricetab and artikel.betriebsnr != 0) or double_currency:
        amount_foreign =  to_decimal(amount)
        amount =  to_decimal(amount) * to_decimal(exchg_rate)


    else:
        amount_foreign =  to_decimal(amount) / to_decimal(exchg_rate)
    amount = to_decimal(round(amount , price_decimal))
    master_flag, bookflag = update_masterbill()

    if bookflag > 0:

        return generate_output()

    if not master_flag:

        if billno > 1:
            FIND bill WHERE bill.resnr = bill1.resnr and bill.parent_nr == bill1.parent_nr and bill.billnr == billno and bill.flag == 0 and bill.zinr == bill1.zinr

            if not bill:
                bil_recid = get_output(create_newbill(res_line._recid, bill1.parent_nr, billno))

                bill = db_session.query(Bill).filter(
                         (Bill._recid == bil_recid)).first()
        else:

            bill = db_session.query(Bill).filter(
                     (Bill._recid == bill1._recid)).first()
        bill.sonst_umsatz =  to_decimal(bill.sonst_umsatz) + to_decimal(amount)
        bill.gesamtumsatz =  to_decimal(bill.gesamtumsatz) + to_decimal(amount)
        bill.rgdruck = 0
        bill.saldo =  to_decimal(bill.saldo) + to_decimal(amount)
        bill.mwst[98] = bill.mwst[98] + amount_foreign
        bill.datum = bill_date

        if bill.rechnr == 0:

            counters = db_session.query(Counters).filter(
                     (Counters.counter_no == 3)).first()
            counters.counter = counters.counter + 1
            bill.rechnr = counters.counter
        bill_line = Bill_line()
        db_session.add(bill_line)

        bill_line.rechnr = bill.rechnr
        bill_line.artnr = artnr
        bill_line.bezeich = artikel.bezeich + " - " + substring(rufnummer, 0, len(rufnummer))
        bill_line.anzahl = 1
        bill_line.betrag =  to_decimal(amount)
        bill_line.fremdwbetrag =  to_decimal(amount_foreign)
        bill_line.zinr = zinr
        bill_line.departement = artikel.departement
        bill_line.epreis =  to_decimal(epreis)
        bill_line.zeit = get_current_time_in_seconds()
        bill_line.userinit = user_init
        bill_line.arrangement = res_line.arrangement
        bill_line.bill_datum = bill_date
        bill_line.origin_id = "CALLS " + to_string(calldate) + ";" + to_string(calltime, "HH:MM") + ";" + rufnummer + ";" + destination + ";" + to_string(duration, "HH:MM:SS") + ";"

        umsatz = db_session.query(Umsatz).filter(
                 (Umsatz.artnr == artnr) & (Umsatz.departement == 0) & (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artnr
            umsatz.datum = bill_date
            umsatz.departement = 0
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
        umsatz.anzahl = umsatz.anzahl + 1
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill.rechnr
        billjournal.artnr = artnr
        billjournal.anzahl = 1
        billjournal.betrag =  to_decimal(amount)
        billjournal.fremdwaehrng =  to_decimal(amount_foreign)
        billjournal.bezeich = artikel.bezeich
        billjournal.zinr = zinr
        billjournal.departement = artikel.departement
        billjournal.epreis =  to_decimal(epreis)
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date
        success = True
        rechnr = bill.rechnr

    return generate_output()