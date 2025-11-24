#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.create_newbill import create_newbill
from models import Bill, Parameters, Res_line, Htparam, Artikel, Waehrung, Counters, Bill_line, Umsatz, Billjournal, Master, Mast_art

def bookcall(zinr:string, calldate:date, calltime:int, destination:string, duration:int, rufnummer:string, amount:Decimal):

    prepare_cache ([Bill, Parameters, Res_line, Htparam, Artikel, Waehrung, Counters, Bill_line, Umsatz, Billjournal, Master])

    success = False
    rechnr = 0
    versioninfo:string = "@(#) BookCall.p 1.0.2 Sindata 2003/11/17"
    bil_recid:int = 0
    epreis:Decimal = to_decimal("0.0")
    artnr:int = 0
    resnr:int = 0
    billno:int = 0
    master_flag:bool = False
    bill_date:date = None
    user_init:string = ""
    bookflag:int = 0
    foreign_rate:bool = False
    double_currency:bool = False
    exchg_rate:Decimal = 1
    amount_foreign:Decimal = to_decimal("0.0")
    price_decimal:int = 0
    calls_type:int = 0
    bill = parameters = res_line = htparam = artikel = waehrung = counters = bill_line = umsatz = billjournal = master = mast_art = None

    bill1 = prefix_list = None

    prefix_list_data, Prefix_list = create_model("Prefix_list", {"prefix":string, "codelan":int})

    Bill1 = create_buffer("Bill1",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success, rechnr, versioninfo, bil_recid, epreis, artnr, resnr, billno, master_flag, bill_date, user_init, bookflag, foreign_rate, double_currency, exchg_rate, amount_foreign, price_decimal, calls_type, bill, parameters, res_line, htparam, artikel, waehrung, counters, bill_line, umsatz, billjournal, master, mast_art
        nonlocal zinr, calldate, calltime, destination, duration, rufnummer, amount
        nonlocal bill1


        nonlocal bill1, prefix_list
        nonlocal prefix_list_data

        return {"success": success, "rechnr": rechnr}

    def update_masterbill():

        nonlocal success, rechnr, versioninfo, bil_recid, epreis, artnr, resnr, billno, master_flag, bill_date, user_init, bookflag, foreign_rate, double_currency, exchg_rate, amount_foreign, price_decimal, calls_type, bill, parameters, res_line, htparam, artikel, waehrung, counters, bill_line, umsatz, billjournal, master, mast_art
        nonlocal zinr, calldate, calltime, destination, duration, rufnummer, amount
        nonlocal bill1


        nonlocal bill1, prefix_list
        nonlocal prefix_list_data

        master_flag = False
        bookflag = 0
        mbill = None
        resline = None

        def generate_inner_output():
            return (master_flag, bookflag)

        Mbill =  create_buffer("Mbill",Bill)
        Resline =  create_buffer("Resline",Res_line)

        master = get_cache (Master, {"resnr": [(eq, resnr)],"active": [(eq, true)],"flag": [(eq, 0)]})

        if not master:

            return generate_inner_output()

        if master.umsatzart[3] :
            master_flag = True
            else:

                mast_art = get_cache (Mast_art, {"resnr": [(eq, master.resnr)],"departement": [(eq, artikel.departement)],"artnr": [(eq, artikel.artnr)]})
                master_flag = (None != mast_art)

        if master_flag:

            mbill = get_cache (Bill, {"resnr": [(eq, resnr)],"reslinnr": [(eq, 0)]})

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

                counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                counters.counter = counters.counter + 1
                mbill.rechnr = counters.counter
                pass
                pass
                master.rechnr = mbill.rechnr
                pass
            rechnr = mbill.rechnr
            bill_line = Bill_line()
            db_session.add(bill_line)

            bill_line.rechnr = mbill.rechnr
            bill_line.artnr = artnr
            bill_line.bezeich = artikel.bezeich + " - " +\
                    substring(rufnummer, 0, length(rufnummer))
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


            pass

            umsatz = get_cache (Umsatz, {"artnr": [(eq, artnr)],"departement": [(eq, artikel.departement)],"datum": [(eq, bill_date)]})

            if not umsatz:
                umsatz = Umsatz()
                db_session.add(umsatz)

                umsatz.artnr = artnr
                umsatz.datum = bill_date
                umsatz.departement = artikel.departement


            umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
            umsatz.anzahl = umsatz.anzahl + 1


            pass
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


            pass
            pass
            bookflag = 1
            success = True

        return generate_inner_output()


    for parameters in db_session.query(Parameters).filter(
             (Parameters.progname == ("interface").lower()) & (Parameters.section == ("prefix").lower())).order_by(Parameters._recid).all():

        if substring(parameters.vstring, 1, 1) != ("0").lower() :

            prefix_list = query(prefix_list_data, filters=(lambda prefix_list: prefix_list.prefix == parameters.vstring), first=True)

            if not prefix_list:
                prefix_list = Prefix_list()
                prefix_list_data.append(prefix_list)

                prefix_list.prefix = parameters.vstring
                prefix_list.codelan = length(parameters.vstring)

    if zinr == "":

        return generate_output()

    if substring(rufnummer, 0, 2) == ("00").lower() :
        calls_type = 2

    elif substring(rufnummer, 0, 1) == ("0").lower() :
        calls_type = 1

        prefix_list = query(prefix_list_data, filters=(lambda prefix_list: prefix_list.prefix == substring(rufnummer, 0, length(prefix_list.prefix))), first=True)

        if prefix_list:
            calls_type = 2

    res_line = get_cache (Res_line, {"resstatus": [(eq, 6)],"zinr": [(eq, zinr)]})

    if not res_line:

        res_line = get_cache (Res_line, {"resstatus": [(eq, 13)],"zinr": [(eq, zinr)]})

        if not res_line:

            return generate_output()
    resnr = res_line.resnr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 113)]})
    artnr = htparam.finteger

    artikel = get_cache (Artikel, {"artnr": [(eq, artnr),(ne, 0)],"departement": [(eq, 0)]})

    if not artikel:

        return generate_output()

    if calls_type == 1:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 114)]})

        artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger),(ne, 0)],"departement": [(eq, 0)],"artart": [(eq, 0)]})

        if artikel:
            artnr = htparam.finteger

    elif calls_type == 2:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 115)]})

        artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger),(ne, 0)],"departement": [(eq, 0)],"artart": [(eq, 0)]})

        if artikel:
            artnr = htparam.finteger
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 114)]})

            artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger),(ne, 0)],"departement": [(eq, 0)],"artart": [(eq, 0)]})

            if artikel:
                artnr = htparam.finteger

    bill1 = get_cache (Bill, {"zinr": [(eq, res_line.zinr)],"reslinnr": [(eq, res_line.reslinnr)],"resnr": [(eq, res_line.resnr)]})

    if not bill1:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 335)]})
    billno = htparam.finteger

    if billno == 0:
        billno = 1

    if billno > 2:
        billno = 2

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

    if htparam.flogical:
        bill_date = bill_date + timedelta(days=1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 317)]})
    user_init = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 559)]})

    if htparam.flogical and length(rufnummer) > 3:
        rufnummer = substring(rufnummer, 0, length(rufnummer) - 3) + "xxx"

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical
    pass

    if artikel.pricetab and artikel.betriebsnr != 0:

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)],"ankauf": [(ne, 0)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    elif foreign_rate or double_currency:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

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

                bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})
        else:

            bill = get_cache (Bill, {"_recid": [(eq, bill1._recid)]})
        bill.sonst_umsatz =  to_decimal(bill.sonst_umsatz) + to_decimal(amount)
        bill.gesamtumsatz =  to_decimal(bill.gesamtumsatz) + to_decimal(amount)
        bill.rgdruck = 0
        bill.saldo =  to_decimal(bill.saldo) + to_decimal(amount)
        bill.mwst[98] = bill.mwst[98] + amount_foreign
        bill.datum = bill_date

        if bill.rechnr == 0:

            counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
            counters.counter = counters.counter + 1
            bill.rechnr = counters.counter
            pass
        bill_line = Bill_line()
        db_session.add(bill_line)

        bill_line.rechnr = bill.rechnr
        bill_line.artnr = artnr
        bill_line.bezeich = artikel.bezeich + " - " + substring(rufnummer, 0, length(rufnummer))
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
        pass

        umsatz = get_cache (Umsatz, {"artnr": [(eq, artnr)],"departement": [(eq, 0)],"datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artnr
            umsatz.datum = bill_date
            umsatz.departement = 0
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
        umsatz.anzahl = umsatz.anzahl + 1
        pass
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
        pass
        pass
        success = True
        rechnr = bill.rechnr

    return generate_output()