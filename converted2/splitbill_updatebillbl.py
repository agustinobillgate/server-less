#using conversion tools version: 1.0.0.117
#---------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bill, Bill_line, Artikel, Guest, Counters, Res_line, Htparam, Billjournal, Debitor, Bediener, Res_history

spbill_list_data, Spbill_list = create_model("Spbill_list", {"selected":bool, "bl_recid":int}, {"selected": True})

def splitbill_updatebillbl(pvilanguage:int, j:int, recid_curr:int, recid_j:int, user_init:string, spbill_list_data:[Spbill_list]):

    prepare_cache ([Bill, Bill_line, Artikel, Guest, Counters, Res_line, Htparam, Billjournal, Debitor, Bediener, Res_history])

    msg_str = ""
    lvcarea:string = "split-bill"
    availbill:bool = False
    bill = bill_line = artikel = guest = counters = res_line = htparam = billjournal = debitor = bediener = res_history = None

    spbill_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, availbill, bill, bill_line, artikel, guest, counters, res_line, htparam, billjournal, debitor, bediener, res_history
        nonlocal pvilanguage, j, recid_curr, recid_j, user_init


        nonlocal spbill_list

        return {"msg_str": msg_str}

    def check_bill_line():

        nonlocal msg_str, lvcarea, availbill, bill, bill_line, artikel, guest, counters, res_line, htparam, billjournal, debitor, bediener, res_history
        nonlocal pvilanguage, j, recid_curr, recid_j, user_init


        nonlocal spbill_list

        bill = get_cache (Bill, {"_recid": [(eq, recid_curr)]})

        if not bill:

            return
        availbill = True

        for spbill_list in query(spbill_list_data, filters=(lambda spbill_list: spbill_list.selected)):

            bill_line = get_cache (Bill_line, {"_recid": [(eq, spbill_list.bl_recid)],"rechnr": [(eq, bill.rechnr)]})

            if not bill_line:
                msg_str = translateExtended ("Bill transfer not possible:", lvcarea, "") + chr_unicode(10) + translateExtended ("One of the bill has been changed, please refresh the screen!", lvcarea, "")
                break


    def update_billine():

        nonlocal msg_str, lvcarea, availbill, bill, bill_line, artikel, guest, counters, res_line, htparam, billjournal, debitor, bediener, res_history
        nonlocal pvilanguage, j, recid_curr, recid_j, user_init


        nonlocal spbill_list

        rechnr:int = 0
        datum:date = None
        replace_it:bool = False
        do_it:bool = False
        billine_datum:date = None
        billi = None
        billj = None
        art1 = None
        bline = None
        gbuff = None
        Billi =  create_buffer("Billi",Bill)
        Billj =  create_buffer("Billj",Bill)
        Art1 =  create_buffer("Art1",Artikel)
        Bline =  create_buffer("Bline",Bill_line)
        Gbuff =  create_buffer("Gbuff",Guest)

        billi = get_cache (Bill, {"_recid": [(eq, recid_curr)]})
        rechnr = billi.rechnr

        billj = get_cache (Bill, {"_recid": [(eq, recid_j)]})

        if billj.rechnr == 0:
            # Rd, 24/11/2025, Update last counter dengan next_counter_for_update
            # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
            counters = db_session.query(Counters).with_for_update().filter(
                     (Counters.counter_no == 3)).first()
            
            counters.counter = counters.counter + 1
            billj.rechnr = counters.counter
            pass
            replace_it = True
        else:

            bline = get_cache (Bill_line, {"rechnr": [(eq, billj.rechnr)]})

            if not bline:
                replace_it = True

        gbuff = get_cache (Guest, {"gastnr": [(eq, billj.gastnr)]})

        for spbill_list in query(spbill_list_data, filters=(lambda spbill_list: spbill_list.selected)):

            bill_line = get_cache (Bill_line, {"_recid": [(eq, spbill_list.bl_recid)],"rechnr": [(eq, rechnr)]})

            if bill_line:

                artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, bill_line.departement)]})

                if artikel and artikel.artart == 2 and gbuff.zahlungsart == 0:
                    msg_str = translateExtended ("Bill transfer not possible:", lvcarea, "") + chr_unicode(10) + translateExtended ("Destination bill does not have C/L account", lvcarea, "")

                    return

        for spbill_list in query(spbill_list_data, filters=(lambda spbill_list: spbill_list.selected)):

            bill_line = get_cache (Bill_line, {"_recid": [(eq, spbill_list.bl_recid)],"rechnr": [(eq, rechnr)]})
            do_it = (None != bill_line)

            if do_it and billj.resnr > 0 and billj.reslinnr > 0 and bill_line.typ > 0 and bill_line.typ != billi.resnr and bill_line.typ != billj.resnr and (billi.gastnr != billj.gastnr):

                res_line = get_cache (Res_line, {"resnr": [(eq, billj.resnr)],"reslinnr": [(eq, billj.parent_nr)]})

                if res_line and res_line.ankunft > bill_line.bill_datum:
                    do_it = False
                    billine_datum = bill_line.bill_datum

            if not do_it:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Bill transfer not possible:", lvcarea, "") + chr_unicode(10) + translateExtended ("Posting date:", lvcarea, "") + " " + to_string(billine_datum) + " " + translateExtended ("BUT Arrival Date of the transferred guest bill is", lvcarea, "") + " " + to_string(res_line.ankunft) + chr_unicode(10)
            else:
                billi.rgdruck = 0
                billj.rgdruck = 0
                bill_line.rechnr = billj.rechnr
                billi.saldo =  to_decimal(billi.saldo) - to_decimal(bill_line.betrag)
                billj.saldo =  to_decimal(billj.saldo) + to_decimal(bill_line.betrag)
                billi.mwst[98] = billi.mwst[98] - bill_line.fremdwbetrag
                billj.mwst[98] = billj.mwst[98] + bill_line.fremdwbetrag

                if bill_line.typ == 0:
                    bill_line.typ = billi.resnr

                if datum == None:
                    datum = bill_line.bill_datum

                elif datum < bill_line.bill_datum:
                    datum = bill_line.bill_datum

                htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = billj.rechnr
                billjournal.artnr = bill_line.artnr
                billjournal.anzahl = 0
                billjournal.betrag =  to_decimal(bill_line.betrag)
                billjournal.fremdwaehrng =  to_decimal(bill_line.fremdwbetrag)
                billjournal.zinr = billj.zinr
                billjournal.departement = bill_line.departement
                billjournal.epreis =  to_decimal(bill_line.epreis)
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_line.bill_datum


                billjournal.bezeich = "*" + to_string(billi.rechnr) + "; " + to_string(htparam.fdate) + " " + translateExtended ("RmNo", lvcarea, "") + " " + billi.zinr
                pass
                pass

                art1 = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, bill_line.departement)]})

                if art1 and (art1.artart == 2 or art1.artart == 7):

                    debitor = get_cache (Debitor, {"artnr": [(eq, art1.artnr)],"rechnr": [(eq, billi.rechnr)],"rgdatum": [(eq, bill_line.bill_datum)],"saldo": [(eq, - bill_line.betrag)],"counter": [(eq, 0)]})

                    if debitor:

                        gbuff = get_cache (Guest, {"gastnr": [(eq, billj.gastnr)]})
                        pass
                        debitor.rechnr = billj.rechnr
                        debitor.gastnr = billj.gastnr
                        debitor.name = gbuff.name


                        pass

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

                if bediener:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = bediener.nr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.aenderung = "OutletNo: " + to_string(bill_line.departement) +\
                            "|" + "ArtNo:" + to_string(bill_line.artnr) +\
                            "|" + "Desc:" + bill_line.bezeich +\
                            "|" + "Amount:" + trim(to_string(bill_line.betrag, "->>>,>>>,>>>,>>9.99"))

                    if billi.resnr != 0 and billi.reslinnr != 0:
                        res_history.aenderung = res_history.aenderung + "|" + "From Room:" + to_string(billi.zinr)

                    elif billi.resnr != 0 and billi.reslinnr == 0:
                        res_history.aenderung = res_history.aenderung + "|" + "From Master Bill"

                    elif billi.resnr == 0 and billi.reslinnr != 0:
                        res_history.aenderung = res_history.aenderung + "|" + "From NonStay Bill"

                    if billj.resnr != 0 and billj.reslinnr != 0:
                        res_history.aenderung = res_history.aenderung + "|" + "To Room:" + to_string(billj.zinr)

                    elif billj.resnr != 0 and billj.reslinnr == 0:
                        res_history.aenderung = res_history.aenderung + "|" + "To Master Bill"

                    elif billj.resnr == 0 and billj.reslinnr != 0:
                        res_history.aenderung = res_history.aenderung + "|" + "To NonStay Bill"
                    res_history.aenderung = res_history.aenderung + "|" + "From Bill:" + to_string(billi.rechnr) + "|" + "To Bill:" + to_string(billj.rechnr)
                    res_history.action = "Transfer Bill F/O"
                    pass
                    pass
            spbill_list_data.remove(spbill_list)

        if datum != None and replace_it:
            billj.datum = datum

        elif billj.datum < datum and datum != None:
            billj.datum = datum
        datum = None

        for bline in db_session.query(Bline).filter(
                 (Bline.rechnr == billi.rechnr)).order_by(Bline._recid).all():

            if datum == None:
                datum = bline.bill_datum

            elif datum < bline.bill_datum:
                datum = bline.bill_datum

        if datum != billi.datum and datum != None:
            billi.datum = datum
        pass
        pass

    check_bill_line()

    if msg_str == "" and availbill:
        update_billine()

    return generate_output()