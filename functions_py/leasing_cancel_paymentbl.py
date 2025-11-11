# using conversion tools version: 1.0.0.119
"""_yusufwijasena_04/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix var decklaration
                    - fix python indentation
                    - changed string to str
                    - fix ("string").lower()
                    - use f"string"
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Artikel, Queasy, Reslin_queasy, Htparam, Bediener, Res_history, Res_line, Debitor, Guest, Billjournal, Umsatz

tlist_data, Tlist = create_model(
    "Tlist",
    {
        "artnr": int,
        "art_bez": str,
        "bezeich": str,
        "amount": Decimal,
        "pay_date": date,
        "pay_time": str,
        "rec_id": int,
        "resno": int,
        "art_select": bool,
        "cicilanke": int
    })


def leasing_cancel_paymentbl(tlist_data: Tlist, qrecid: int, user_init: str):

    prepare_cache([Artikel, Queasy, Reslin_queasy, Htparam, Bediener,Res_history, Res_line, Guest, Billjournal, Umsatz])

    success = False
    pay_amount = to_decimal("0.0")
    bill_date: date = None
    pinvoice_no = ""
    artikel_no: int = 0
    ar_ledger: int = 0
    v_cicilanke: int = 0
    artikel = queasy = reslin_queasy = htparam = bediener = res_history = res_line = debitor = guest = billjournal = umsatz = None
    tlist = bart = tqueasy = treslin = None

    Bart = create_buffer("Bart", Artikel)
    Tqueasy = create_buffer("Tqueasy", Queasy)
    Treslin = create_buffer("Treslin", Reslin_queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success, pay_amount, bill_date, pinvoice_no, artikel_no, ar_ledger, v_cicilanke, artikel, queasy, reslin_queasy, htparam, bediener, res_history, res_line, debitor, guest, billjournal, umsatz
        nonlocal qrecid, user_init
        nonlocal bart, tqueasy, treslin
        nonlocal tlist, bart, tqueasy, treslin

        return {
            "success": success
        }

    def create_log():
        nonlocal success, pay_amount, bill_date, pinvoice_no, artikel_no, ar_ledger, v_cicilanke, artikel, queasy, reslin_queasy, htparam, bediener, res_history, res_line, debitor, guest, billjournal, umsatz
        nonlocal qrecid, user_init
        nonlocal bart, tqueasy, treslin
        nonlocal tlist, bart, tqueasy, treslin

        bediener = get_cache(
            Bediener, {"userinit": [(eq, user_init)]})
        res_history = Res_history()

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        # res_history.aenderung = "Cancel Payment - Reservation no : " + \
        #     to_string(queasy.number1) + " Amount : " + to_string(pay_amount)
        res_history.aenderung = f"Cancel Payment - Reservation no : {queasy.number1} Amount : {pay_amount}"
        res_history.action = "Service Apartment"

        db_session.add(res_history)

        treslin = Reslin_queasy()

        treslin.key = "ResChanges"
        treslin.resnr = queasy.number1
        treslin.reslinnr = queasy.number2
        treslin.date2 = get_current_date()
        treslin.number2 = get_current_time_in_seconds()

        db_session.add(treslin)

        res_line = get_cache(
            Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

        if res_line:
            treslin.char3 = to_string(res_line.ankunft) + ";" +\
                to_string(res_line.ankunft) + ";" +\
                to_string(res_line.abreise) + ";" +\
                to_string(res_line.abreise) + ";" +\
                to_string(res_line.zimmeranz) + ";" +\
                to_string(res_line.zimmeranz) + ";" +\
                to_string(res_line.erwachs) + ";" +\
                to_string(res_line.erwachs) + ";" +\
                to_string(res_line.kind1) + ";" +\
                to_string(res_line.kind1) + ";" +\
                to_string(res_line.gratis) + ";" +\
                to_string(res_line.gratis) + ";" +\
                to_string(res_line.zikatnr) + ";" +\
                to_string(res_line.zikatnr) + ";" +\
                to_string(res_line.zinr) + ";" +\
                to_string(res_line.zinr) + ";" +\
                to_string(res_line.arrangement) + ";" +\
                to_string(res_line.arrangement) + ";" +\
                to_string(res_line.zipreis) + ";" +\
                to_string(res_line.zipreis) + ";" +\
                " " + ";" +\
                to_string(user_init) + ";" +\
                to_string(get_current_date()) + ";" +\
                to_string(get_current_time_in_seconds()) + ";" +\
                to_string("Service Apartement - Cancel Payment : ") + ";" +\
                to_string(res_line.resnr) + " Amount : " + to_string(pay_amount) + ";" +\
                to_string("NO", "x(3)") + ";" +\
                to_string("NO", "x(3)") + ";"

    def create_ar():
        nonlocal success, pay_amount, bill_date, pinvoice_no, artikel_no, ar_ledger, v_cicilanke, artikel, queasy, reslin_queasy, htparam, bediener, res_history, res_line, debitor, guest, billjournal, umsatz
        nonlocal qrecid, user_init
        nonlocal bart, tqueasy, treslin
        nonlocal tlist, bart, tqueasy, treslin

        bdebt = None
        Bdebt = create_buffer("Bdebt", Debitor)

        debitor = get_cache(
            Debitor, {"vesrcod": [(eq, pinvoice_no)], "zahlkonto": [(eq, 0)]})

        if debitor:
            bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})

            bart = db_session.query(Bart).filter(
                (Bart.artnr == artikel_no) & (Bart.departement == 0) & ((Bart.artart == 2) | (Bart.artart == 7))).first()

            if bart:
                bdebt = Debitor()

                bdebt.artnr = artikel_no
                bdebt.rechnr = to_int(pinvoice_no)
                bdebt.rgdatum = bill_date
                bdebt.saldo = - to_decimal(pay_amount)
                bdebt.vesrdep = - to_decimal(pay_amount)
                bdebt.bediener_nr = bediener.nr
                bdebt.vesrdat = get_current_date()
                bdebt.transzeit = get_current_time_in_seconds()
                # bdebt.vesrcod = pinvoice_no + "|CANCEL PAYMENT DEPOSIT"
                bdebt.vesrcod = f"{pinvoice_no}|CANCEL PAYMENT DEPOSIT"

                db_session.add(bdebt)

                res_line = get_cache(
                    Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

                if res_line:
                    guest = get_cache(
                        Guest, {"gastnr": [(eq, res_line.gastnr)]})

                    if guest:
                        bdebt.name = guest.name
                        bdebt.gastnr = res_line.gastnr
                        bdebt.gastnrmember = res_line.gastnrmember

            bdebt = Debitor()

            bdebt.artnr = ar_ledger
            bdebt.rechnr = to_int(pinvoice_no)
            bdebt.rgdatum = bill_date
            bdebt.saldo = to_decimal(pay_amount)
            bdebt.vesrdep = to_decimal(pay_amount)
            bdebt.bediener_nr = bediener.nr
            bdebt.vesrdat = get_current_date()
            bdebt.transzeit = get_current_time_in_seconds()
            # bdebt.vesrcod = pinvoice_no + "|VOID CANCEL PAYMENT DEPOSIT"
            bdebt.vesrcod = f"{pinvoice_no}|VOID CANCEL PAYMENT DEPOSIT"

            db_session.add(bdebt)

            res_line = get_cache(
                Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

            if res_line:
                guest = get_cache(Guest, {"gastnr": [(eq, res_line.gastnr)]})

                if guest:
                    bdebt.name = guest.name
                    bdebt.gastnr = res_line.gastnr
                    bdebt.gastnrmember = res_line.gastnrmember

    def create_turnover():
        nonlocal success, pay_amount, bill_date, pinvoice_no, artikel_no, ar_ledger, v_cicilanke, artikel, queasy, reslin_queasy, htparam, bediener, res_history, res_line, debitor, guest, billjournal, umsatz
        nonlocal qrecid, user_init
        nonlocal bart, tqueasy, treslin
        nonlocal tlist, bart, tqueasy, treslin

        artikel = get_cache(
            Artikel, {"artnr": [(eq, ar_ledger)], "departement": [(eq, 0)]})

        if not artikel:
            return
        billjournal = Billjournal()

        billjournal.artnr = artikel.artnr
        billjournal.anzahl = 1
        billjournal.fremdwaehrng = - to_decimal(pay_amount)
        billjournal.betrag = - to_decimal(pay_amount)
        # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + pinvoice_no + \
        #     "[CANCEL Payment Leasing #" + to_string(queasy.number1) + "]"
        billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {pinvoice_no}[CANCEL Payment Leasing #{queasy.number1}]"
        billjournal.epreis = to_decimal("0")
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.billjou_ref = artikel.artnr
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date
        billjournal.kassabuch_nr = qrecid

        db_session.add(billjournal)

        if v_cicilanke != 0:
            billjournal.billin_nr = v_cicilanke

        umsatz = get_cache(
            Umsatz, {"artnr": [(eq, ar_ledger)], "departement": [(eq, 0)], "datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = ar_ledger
            umsatz.datum = bill_date

        umsatz.anzahl = umsatz.anzahl - 1
        umsatz.betrag = to_decimal(umsatz.betrag - pay_amount)

        artikel = get_cache(
            Artikel, {"artnr": [(eq, artikel_no)], "departement": [(eq, 0)]})

        if not artikel:
            return
        billjournal = Billjournal()

        billjournal.artnr = artikel.artnr
        billjournal.anzahl = 1
        billjournal.fremdwaehrng = to_decimal(pay_amount)
        billjournal.betrag = to_decimal(pay_amount)
        # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + pinvoice_no + \
        #     "[CANCEL Payment Leasing #" + to_string(queasy.number1) + "]"
        billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {pinvoice_no}[CANCEL Payment Leasing #{queasy.number1}]"
        billjournal.epreis = to_decimal("0")
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.billjou_ref = queasy.number1
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date
        billjournal.kassabuch_nr = qrecid

        db_session.add(billjournal)

        if v_cicilanke != 0:
            billjournal.billin_nr = v_cicilanke

        umsatz = get_cache(
            Umsatz, {"artnr": [(eq, artikel.artnr)], "departement": [(eq, 0)], "datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()

            umsatz.artnr = artikel.artnr
            umsatz.datum = bill_date

            db_session.add(umsatz)

        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag = to_decimal(umsatz.betrag + pay_amount)

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date = htparam.fdate

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 1051)]})

    if htparam:
        ar_ledger = htparam.finteger

    for tlist in query(tlist_data, filters=(lambda tlist: tlist.art_select)):
        queasy = get_cache(
            Queasy, {"key": [(eq, 329)], "_recid": [(eq, qrecid)]})

        if queasy:
            pay_amount = - to_decimal(tlist.amount)
            pinvoice_no = queasy.char2
            artikel_no = tlist.artnr
            v_cicilanke = tlist.cicilanKe

            artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == tlist.artnr) & (Artikel.departement == 0) & ((Artikel.artart == 2) | (Artikel.artart == 7) | (Artikel.artart == 6))).first()

            if artikel:
                if artikel.artart == 2 or artikel.artart == 7:
                    create_ar()
            create_turnover()
            queasy.deci2 = to_decimal(queasy.deci2) - to_decimal(pay_amount)

            if queasy.deci2 == 0:
                queasy.logi2 = False

            reslin_queasy = get_cache(
                Reslin_queasy, {"key": [(eq, "actual-invoice")], "resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)], "betriebsnr": [(eq, qrecid)], "number1": [(eq, v_cicilanke)], "logi3": [(eq, True)]})

            if reslin_queasy:
                reslin_queasy.logi3 = False
                
            create_log()
            success = True

    return generate_output()
