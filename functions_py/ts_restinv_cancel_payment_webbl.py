#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_bill, H_bill_line, H_artikel, Hoteldpt, Res_line, H_journal, H_umsatz, Umsatz, Artikel, Guest, Debitor, Htparam, Waehrung, Bediener, Billjournal
from sqlalchemy.orm import flag_modified

t_payload_list_data, T_payload_list = create_model("T_payload_list", {"hbill_recid":int, "hbline_recid":int, "bill_number":int, "art_number":int, "dept_number":int, "bill_date":date, "curr_waiter":int, "user_init":string, "cancel_reason":string})

def ts_restinv_cancel_payment_webbl(t_payload_list_data:[T_payload_list]):

    prepare_cache ([H_artikel, Hoteldpt, Res_line, H_journal, H_umsatz, Umsatz, Artikel, Guest, Htparam, Waehrung, Bediener, Billjournal])

    output_response_data = []
    t_h_bill_data = []
    zeit:int = 0
    h_artart:int = 0
    h_artnrfront:int = 0
    fo_artno:int = 0
    guest_member:int = 0
    curr_room:string = ""
    guest_name:string = ""
    dept_name:string = ""
    h_bill = h_bill_line = h_artikel = hoteldpt = res_line = h_journal = h_umsatz = umsatz = artikel = guest = debitor = htparam = waehrung = bediener = billjournal = None

    t_h_bill = b_list = t_payload_list = output_response = None

    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    b_list_data, B_list = create_model_like(H_bill_line, {"rec_id":int})
    output_response_data, Output_response = create_model("Output_response", {"success_flag":bool, "error_message":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_response_data, t_h_bill_data, zeit, h_artart, h_artnrfront, fo_artno, guest_member, curr_room, guest_name, dept_name, h_bill, h_bill_line, h_artikel, hoteldpt, res_line, h_journal, h_umsatz, umsatz, artikel, guest, debitor, htparam, waehrung, bediener, billjournal


        nonlocal t_h_bill, b_list, t_payload_list, output_response
        nonlocal t_h_bill_data, b_list_data, output_response_data

        return {"output-response": output_response_data, "t-h-bill": t_h_bill_data}

    def inv_ar(curr_art:int, curr_dept:int, zinr:string, gastnr:int, gastnrmember:int, rechnr:int, saldo:Decimal, saldo_foreign:Decimal, bill_date:date, billname:string, userinit:string, voucher_nr:string):

        nonlocal output_response_data, t_h_bill_data, zeit, h_artart, h_artnrfront, fo_artno, guest_member, curr_room, guest_name, dept_name, h_bill, h_bill_line, h_artikel, hoteldpt, res_line, h_journal, h_umsatz, umsatz, artikel, guest, debitor, htparam, waehrung, bediener, billjournal
        nonlocal t_h_bill, b_list, t_payload_list, output_response
        nonlocal t_h_bill_data, b_list_data, output_response_data

        exchg_rate:Decimal = 1
        foreign_rate:bool = False
        double_currency:bool = False
        ar_license:bool = False
        debt = None
        Debt =  create_buffer("Debt",Debitor)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})

        if htparam:
            foreign_rate = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})

        if htparam:
            double_currency = htparam.flogical

        if foreign_rate:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

            if htparam:

                waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

                if waehrung:
                    exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        if exchg_rate != 1:
            saldo_foreign = to_decimal(round(saldo / exchg_rate , 2))

        bediener = get_cache (Bediener, {"userinit": [(eq, userinit)]})

        htparam = get_cache (Htparam, {"paramnr": [(eq, 997)]})

        if htparam:
            ar_license = htparam.flogical

        artikel = get_cache (Artikel, {"departement": [(eq, 0)],"artnr": [(eq, curr_art)]})

        guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

        if guest:
            billname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

        debt = db_session.query(Debt).filter(
                 (Debt.artnr == curr_art) & (Debt.rechnr == rechnr) & (Debt.opart == 0) & (Debt.betriebsnr == curr_dept) & 
                 (Debt.rgdatum == bill_date) & (Debt.counter == 0) & (Debt.saldo == saldo)).with_for_update().first()

        if debt:
            pass
            db_session.delete(debt)

            # umsatz = get_cache (Umsatz, {"departement": [(eq, 0)],"artnr": [(eq, curr_art)],"datum": [(eq, bill_date)]})
            umsatz = db_session.query(Umsatz).filter(
                     (Umsatz.departement == 0) & (Umsatz.artnr == curr_art) & (Umsatz.datum == bill_date)).with_for_update().first()
            

            if umsatz:
                umsatz.anzahl = umsatz.anzahl - 1
                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(saldo)
                
            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = rechnr
            billjournal.bill_datum = bill_date
            billjournal.artnr = curr_art
            billjournal.betriebsnr = curr_dept
            billjournal.anzahl = 1
            billjournal.betrag =  to_decimal(saldo)
            billjournal.zinr = zinr
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.userinit = userinit

            if double_currency:
                billjournal.fremdwaehrng =  to_decimal(saldo_foreign)

            if artikel:
                billjournal.bezeich = artikel.bezeich

            if bediener:
                billjournal.bediener_nr = bediener.nr
            pass

            return

        if ar_license:

            if voucher_nr != "":
                voucher_nr = "/" + voucher_nr
            debitor = Debitor()
            db_session.add(debitor)

            debitor.artnr = curr_art
            debitor.betrieb_gastmem = artikel.betriebsnr
            debitor.betriebsnr = curr_dept
            debitor.zinr = zinr
            debitor.gastnr = gastnr
            debitor.gastnrmember = gastnrmember
            debitor.rechnr = rechnr
            debitor.saldo =  - to_decimal(saldo)
            debitor.transzeit = get_current_time_in_seconds()
            debitor.rgdatum = bill_date
            debitor.bediener_nr = bediener.nr
            debitor.name = billname
            debitor.vesrcod = dept_name + voucher_nr

            if double_currency or foreign_rate:
                debitor.vesrdep =  - to_decimal(saldo_foreign)

            if artikel:
                debitor.betrieb_gastmem = artikel.betriebsnr

            if bediener:
                debitor.bediener_nr = bediener.nr
            pass

        # umsatz = get_cache (Umsatz, {"departement": [(eq, 0)],"artnr": [(eq, curr_art)],"datum": [(eq, bill_date)]})
        umsatz = db_session.query(Umsatz).filter(
                 (Umsatz.departement == 0) & (Umsatz.artnr == curr_art) & (Umsatz.datum == bill_date)).with_for_update().first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = curr_art
            umsatz.datum = bill_date
        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(saldo)


        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = rechnr
        billjournal.bill_datum = bill_date
        billjournal.artnr = curr_art
        billjournal.betriebsnr = curr_dept
        billjournal.anzahl = 1
        billjournal.betrag =  to_decimal(saldo)
        billjournal.bezeich = artikel.bezeich
        billjournal.zinr = zinr
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.bediener_nr = bediener.nr
        billjournal.userinit = userinit

        if double_currency:
            billjournal.fremdwaehrng =  to_decimal(saldo_foreign)

        if artikel:
            billjournal.bezeich = artikel.bezeich

        if bediener:
            billjournal.bediener_nr = bediener.nr
        pass

    t_payload_list = query(t_payload_list_data, first=True)

    if not t_payload_list:

        return generate_output()
    output_response = Output_response()
    output_response_data.append(output_response)


    h_artikel = get_cache (H_artikel, {"artnr": [(eq, t_payload_list.art_number)],"departement": [(eq, t_payload_list.dept_number)]})

    if h_artikel:

        if h_artikel.artart == 0:
            output_response.error_message = "Select payment article only."

            return generate_output()
        h_artart = h_artikel.artart
        h_artnrfront = h_artikel.artnrfront

    h_bill_line = get_cache (H_bill_line, {"_recid": [(eq, H_bill_line._recid)],"rechnr": [(eq, t_payload_list.bill_number)],"departement": [(eq, t_payload_list.dept_number)]})

    if h_bill_line:
        b_list = B_list()
        b_list_data.append(b_list)

        buffer_copy(h_bill_line, b_list)

        if t_payload_list.cancel_reason != None and t_payload_list.cancel_reason != "":
            b_list.bezeich = to_string(h_bill_line.bezeich, "x(24)") + t_payload_list.cancel_reason
        b_list.anzahl = - h_bill_line.anzahl
        b_list.betrag =  - to_decimal(h_bill_line.betrag)
        b_list.nettobetrag =  - to_decimal(h_bill_line.nettobetrag)
        b_list.fremdwbetrag =  - to_decimal(h_bill_line.fremdwbetrag)

    b_list = query(b_list_data, first=True)

    if not b_list:

        return generate_output()
    zeit = get_current_time_in_seconds()

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, t_payload_list.dept_number)]})

    if hoteldpt:
        dept_name = hoteldpt.depart

    # h_bill = get_cache (H_bill, {"_recid": [(eq, t_payload_list.hbill_recid)]})
    h_bill = db_session.query(H_bill).filter(
                 (H_bill._recid == t_payload_list.hbill_recid)).with_for_update().first()

    if h_bill:
        pass
        h_bill.saldo =  to_decimal(h_bill.saldo) + to_decimal(b_list.betrag)
        h_bill.mwst[98] = h_bill.mwst[98] + b_list.betrag
        pass

        if h_bill.resnr > 0 and h_bill.reslinnr > 0:

            res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

            if res_line:
                guest_member = res_line.gastnrmember
                curr_room = res_line.zinr

        elif h_bill.resnr > 0:
            guest_member = h_bill.resnr
        pass
    h_bill_line = H_bill_line()
    db_session.add(h_bill_line)
    flag_modified(h_bill, "mwst")

    h_bill_line.rechnr = b_list.rechnr
    h_bill_line.artnr = b_list.artnr
    h_bill_line.bezeich = b_list.bezeich
    h_bill_line.anzahl = b_list.anzahl
    h_bill_line.nettobetrag =  to_decimal(b_list.nettobetrag)
    h_bill_line.fremdwbetrag =  to_decimal(b_list.fremdwbetrag)
    h_bill_line.betrag =  to_decimal(b_list.betrag)
    h_bill_line.tischnr = b_list.tischnr
    h_bill_line.departement = b_list.departement
    h_bill_line.epreis =  to_decimal("0")
    h_bill_line.zeit = zeit
    h_bill_line.bill_datum = t_payload_list.bill_date
    h_bill_line.sysdate = get_current_date()
    h_bill_line.waehrungsnr = b_list.waehrungsnr


    h_journal = H_journal()
    db_session.add(h_journal)

    h_journal.rechnr = b_list.rechnr
    h_journal.artnr = b_list.artnr
    h_journal.anzahl = b_list.anzahl
    h_journal.fremdwaehrng =  to_decimal(b_list.fremdwbetrag)
    h_journal.betrag =  to_decimal(b_list.betrag)
    h_journal.bezeich = b_list.bezeich
    h_journal.tischnr = b_list.tischnr
    h_journal.departement = b_list.departement
    h_journal.epreis =  to_decimal("0")
    h_journal.zeit = zeit
    h_journal.stornogrund = t_payload_list.cancel_reason
    h_journal.aendertext = ""
    h_journal.kellner_nr = to_int(t_payload_list.user_init)
    h_journal.bill_datum = t_payload_list.bill_date
    h_journal.sysdate = get_current_date()
    h_journal.wabkurz = ""
    h_journal.artart = h_artart
    h_journal.artnrfront = h_artnrfront


    if t_payload_list.art_number != 0:

        # h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, t_payload_list.art_number)],"departement": [(eq, t_payload_list.dept_number)],"datum": [(eq, t_payload_list.bill_date)]})
        h_umsatz = db_session.query(H_umsatz).filter(
                 (H_umsatz.artnr == t_payload_list.art_number) & (H_umsatz.departement == t_payload_list.dept_number) & 
                 (H_umsatz.datum == t_payload_list.bill_date)).with_for_update().first()
        if not h_umsatz:
            h_umsatz = H_umsatz()
            db_session.add(h_umsatz)

            h_umsatz.artnr = t_payload_list.art_number
            h_umsatz.datum = t_payload_list.bill_date
            h_umsatz.departement = t_payload_list.dept_number


        h_umsatz.betrag =  to_decimal(h_umsatz.betrag) + to_decimal(b_list.betrag)
        h_umsatz.anzahl = h_umsatz.anzahl + b_list.anzahl



    if h_artart == 6:

        # umsatz = get_cache (Umsatz, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, 0)],"datum": [(eq, t_payload_list.bill_date)]})
        umsatz = db_session.query(Umsatz).filter(
                 (Umsatz.artnr == h_artikel.artnrfront) & (Umsatz.departement == 0) & (Umsatz.datum == t_payload_list.bill_date)).with_for_update().first()

        if umsatz:
            pass
        else:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = h_artikel.artnrfront
            umsatz.datum = h_artikel.bill_date
            umsatz.departement = 0


        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(b_list.betrag)
        umsatz.anzahl = umsatz.anzahl + b_list.anzahl



    if h_artart == 2 or h_artart == 7:

        artikel = get_cache (Artikel, {"artnr": [(eq, h_artnrfront)],"departement": [(eq, 0)]})

        if artikel:
            fo_artno = artikel.artnr

        if guest_member != 0:

            guest = get_cache (Guest, {"gastnr": [(eq, guest_member)]})

            if guest:
                guest_name = guest.name
        inv_ar(fo_artno, t_payload_list.dept_number, curr_room, guest_member, guest_member, t_payload_list.bill_number, b_list.betrag, b_list.fremdwbetrag, t_payload_list.bill_date, guest_name, user_init, "")

    h_bill = get_cache (H_bill, {"_recid": [(eq, t_payload_list.hbill_recid)]})

    if h_bill:
        t_h_bill = T_h_bill()
        t_h_bill_data.append(t_h_bill)

        buffer_copy(h_bill, t_h_bill)
        t_h_bill.rec_id = h_bill._recid


    success_flag = True

    return generate_output()