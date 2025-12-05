#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 09-10-2025
# Tiket ID : 8CF423 | Recompile Program
# Rd, 01/12/2025, with_for_update added
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_bill, H_bill_line, H_artikel, Htparam, Kellne1, H_umsatz, H_journal, Umsatz, Queasy, Guest, Artikel, Debitor, Waehrung, Bediener, Billjournal
from sqlalchemy.orm.attributes import flag_modified

input_list_data, Input_list = create_model("Input_list", {"mc_str":string})

def ts_closeinv_update_bill_webbl(amount:Decimal, amount_foreign:Decimal, balance:Decimal, rec_bill_guest:int, 
                                  foreign_rate:bool, curr_dept:int, rec_h_artikel:int, rec_h_bill:int, h_artart:int, h_artnrfront:int, 
                                  unit_price:Decimal, double_currency:bool, exchg_rate:Decimal, price_decimal:int, qty:int, kreditlimit:Decimal, 
                                  billart:int, description:string, change_str:string, nett_amount:Decimal, tischnr:int, price:Decimal, 
                                  bill_date:date, b_list_departement:int, avail_b_list:bool, cc_comment:string, b_list_waehrungsnr:int, 
                                  hoga_card:string, cancel_str:string, req_str:string, curr_waiter:int, pay_type:int, transfer_zinr:string, 
                                  curr_room:string, user_init:string, deptname:string, input_list_data:[Input_list]):

    prepare_cache ([H_bill_line, H_artikel, Htparam, H_umsatz, H_journal, Umsatz, Queasy, Guest, Artikel, Waehrung, Bediener, Billjournal])

    service_foreign = to_decimal("0.0")
    mwst_foreign = to_decimal("0.0")
    service = to_decimal("0.0")
    mwst = to_decimal("0.0")
    bcol = 2
    balance_foreign = to_decimal("0.0")
    closed = False
    t_h_bill_data = []
    h_service:Decimal = to_decimal("0.0")
    h_service_foreign:Decimal = to_decimal("0.0")
    h_mwst:Decimal = to_decimal("0.0")
    h_mwst_foreign:Decimal = to_decimal("0.0")
    sysdate:date = None
    zeit:int = 0
    nett_compli:Decimal = to_decimal("0.0")
    mc_str:string = ""
    h_bill = h_bill_line = h_artikel = htparam = kellne1 = h_umsatz = h_journal = umsatz = queasy = guest = artikel = debitor = waehrung = bediener = billjournal = None

    t_h_bill = input_list = hbline = hartikel = bill_guest = None

    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    Hbline = create_buffer("Hbline",H_bill_line)
    Hartikel = create_buffer("Hartikel",H_artikel)
    Bill_guest = create_buffer("Bill_guest",Guest)

    db_session = local_storage.db_session
    description = description.strip()
    change_str = change_str.strip()
    cc_comment = cc_comment.strip()
    hoga_card = hoga_card.strip()
    cancel_str = cancel_str.strip()
    req_str = req_str.strip()
    transfer_zinr = transfer_zinr.strip()
    curr_room = curr_room.strip()
    deptname = deptname.strip()

    def generate_output():
        nonlocal service_foreign, mwst_foreign, service, mwst, bcol, balance_foreign, closed, t_h_bill_data, h_service, h_service_foreign, h_mwst, h_mwst_foreign, sysdate, zeit, nett_compli, mc_str, h_bill, h_bill_line, h_artikel, htparam, kellne1, h_umsatz, h_journal, umsatz, queasy, guest, artikel, debitor, waehrung, bediener, billjournal
        nonlocal amount, amount_foreign, balance, rec_bill_guest, foreign_rate, curr_dept, rec_h_artikel, rec_h_bill, h_artart, h_artnrfront, unit_price, double_currency, exchg_rate, price_decimal, qty, kreditlimit, billart, description, change_str, nett_amount, tischnr, price, bill_date, b_list_departement, avail_b_list, cc_comment, b_list_waehrungsnr, hoga_card, cancel_str, req_str, curr_waiter, pay_type, transfer_zinr, curr_room, user_init, deptname
        nonlocal hbline, hartikel, bill_guest


        nonlocal t_h_bill, input_list, hbline, hartikel, bill_guest
        nonlocal t_h_bill_data

        return {"amount": amount, "amount_foreign": amount_foreign, "balance": balance, "service_foreign": service_foreign, "mwst_foreign": mwst_foreign, "service": service, "mwst": mwst, "bcol": bcol, "balance_foreign": balance_foreign, "closed": closed, "t-h-bill": t_h_bill_data}

    def inv_ar(curr_art:int, curr_dept:int, zinr:string, gastnr:int, gastnrmember:int, rechnr:int, saldo:Decimal, saldo_foreign:Decimal, bill_date:date, billname:string, userinit:string, voucher_nr:string):

        nonlocal service_foreign, mwst_foreign, service, mwst, bcol, balance_foreign, closed, t_h_bill_data, h_service, h_service_foreign, h_mwst, h_mwst_foreign, sysdate, zeit, nett_compli, mc_str, h_bill, h_bill_line, h_artikel, htparam, kellne1, h_umsatz, h_journal, umsatz, queasy, guest, artikel, debitor, waehrung, bediener, billjournal
        nonlocal amount, amount_foreign, balance, rec_bill_guest, rec_h_artikel, rec_h_bill, h_artart, h_artnrfront, unit_price, price_decimal, qty, kreditlimit, billart, description, change_str, nett_amount, tischnr, price, b_list_departement, avail_b_list, cc_comment, b_list_waehrungsnr, hoga_card, cancel_str, req_str, curr_waiter, pay_type, transfer_zinr, curr_room, user_init, deptname
        nonlocal hbline, hartikel, bill_guest


        nonlocal t_h_bill, input_list, hbline, hartikel, bill_guest
        nonlocal t_h_bill_data

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

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

            if waehrung:
                exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        if exchg_rate != 1:
            saldo_foreign = to_decimal(round(saldo / exchg_rate , 2))

        bediener = get_cache (Bediener, {"userinit": [(eq, userinit)]})

        htparam = get_cache (Htparam, {"paramnr": [(eq, 997)]})
        ar_license = htparam.flogical

        artikel = get_cache (Artikel, {"departement": [(eq, 0)],"artnr": [(eq, curr_art)]})

        guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})
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

            if double_currency:
                billjournal.fremdwaehrng =  to_decimal(saldo_foreign)
            billjournal.bezeich = artikel.bezeich
            billjournal.zinr = zinr
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.bediener_nr = bediener.nr
            billjournal.userinit = userinit
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
            debitor.vesrcod = deptname + voucher_nr

            if double_currency or foreign_rate:
                debitor.vesrdep =  - to_decimal(saldo_foreign)
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

        if double_currency:
            billjournal.fremdwaehrng =  to_decimal(saldo_foreign)
        billjournal.bezeich = artikel.bezeich
        billjournal.zinr = zinr
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.bediener_nr = bediener.nr
        billjournal.userinit = userinit
        pass

    input_list = query(input_list_data, first=True)

    if input_list and mc_str != None:
        mc_str = input_list.mc_str
    else:
        mc_str = ""

    h_artikel = get_cache (H_artikel, {"_recid": [(eq, rec_h_artikel)]})

    if h_artikel:

        if (rec_h_artikel == rec_h_bill and h_artikel.departement == curr_dept) or rec_h_artikel != rec_h_bill:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 135)]})

            if not htparam.flogical and h_artart == 0 and h_artikel.service_code != 0:

                htparam = get_cache (Htparam, {"paramnr": [(eq, h_artikel.service_code)]})

                if htparam.fdecimal != 0:
                    h_service =  to_decimal(unit_price) * to_decimal(htparam.fdecimal) / to_decimal("100")
                    h_service_foreign = to_decimal(round(h_service , 2))

                    if double_currency:
                        h_service = to_decimal(round(h_service * exchg_rate , price_decimal))
                    else:
                        h_service = to_decimal(round(h_service , price_decimal))
                    service =  to_decimal(service) + to_decimal(h_service) * to_decimal(qty)
                    service_foreign =  to_decimal(service_foreign) + to_decimal(h_service_foreign) * to_decimal(qty)

            htparam = get_cache (Htparam, {"paramnr": [(eq, 134)]})

            if not htparam.flogical and h_artart == 0 and h_artikel.mwst_code != 0:

                htparam = get_cache (Htparam, {"paramnr": [(eq, h_artikel.mwst_code)]})

                if htparam.fdecimal != 0:
                    h_mwst =  to_decimal(htparam.fdecimal)

                    htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})

                    if htparam.flogical:
                        h_mwst =  to_decimal(h_mwst) * to_decimal((unit_price) + to_decimal(h_service_foreign)) / to_decimal("100")
                    else:
                        h_mwst =  to_decimal(h_mwst) * to_decimal(unit_price) / to_decimal("100")
                    h_mwst_foreign = to_decimal(round(h_mwst , 2))

                    if double_currency:
                        h_mwst = to_decimal(round(h_mwst * exchg_rate , price_decimal))
                    else:
                        h_mwst = to_decimal(round(h_mwst , price_decimal))
                    mwst =  to_decimal(mwst) + to_decimal(h_mwst) * to_decimal(qty)
                    mwst_foreign =  to_decimal(mwst_foreign) + to_decimal(h_mwst_foreign) * to_decimal(qty)
    amount =  to_decimal(amount) + to_decimal((h_service) + to_decimal(h_mwst)) * to_decimal(qty)
    amount_foreign =  to_decimal(amount_foreign) + to_decimal((h_service_foreign) + to_decimal(h_mwst_foreign)) * to_decimal(qty)

    # h_bill = get_cache (H_bill, {"_recid": [(eq, rec_h_bill)]})
    h_bill = db_session.query(H_bill).filter(
                 (H_bill._recid == rec_h_bill)).with_for_update().first()

    if h_bill:
        pass

        kellne1 = get_cache (Kellne1, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, curr_dept)]})

        if h_artart == 0:
            h_bill.gesamtumsatz =  to_decimal(h_bill.gesamtumsatz) + to_decimal(amount)
        balance =  to_decimal(balance) + to_decimal(amount)

        if balance <= kreditlimit:
            bcol = 2
        h_bill.saldo =  to_decimal(h_bill.saldo) + to_decimal(amount)
        h_bill.mwst[98] = h_bill.mwst[98] + amount_foreign
        balance =  to_decimal(h_bill.saldo)
        balance_foreign =  to_decimal(h_bill.mwst[98])
        flag_modified(h_bill, "mwst")
        if balance != 0:
            h_bill.rgdruck = 0

        if balance <= kreditlimit:
            bcol = 2
        sysdate = get_current_date()
        zeit = get_current_time_in_seconds()
        h_bill_line = H_bill_line()
        db_session.add(h_bill_line)

        h_bill_line.rechnr = h_bill.rechnr
        h_bill_line.artnr = billart
        h_bill_line.bezeich = description + change_str
        h_bill_line.anzahl = qty
        h_bill_line.nettobetrag =  to_decimal(nett_amount)
        h_bill_line.fremdwbetrag =  to_decimal(amount_foreign)
        h_bill_line.betrag =  to_decimal(amount)
        h_bill_line.tischnr = tischnr
        h_bill_line.departement = curr_dept
        h_bill_line.epreis =  to_decimal(price)
        h_bill_line.zeit = zeit
        h_bill_line.bill_datum = bill_date
        h_bill_line.sysdate = sysdate

        if avail_b_list and b_list_departement < 999:
            h_bill_line.bezeich = h_bill_line.bezeich + cc_comment

        if avail_b_list:
            h_bill_line.waehrungsnr = b_list_waehrungsnr

        if substring(description, 0, 5) == ("RmNo ").lower()  or substring(description, 0, 5) == ("Card ").lower() :
            h_bill_line.segmentcode = to_int(substring(hoga_card, 0, 9))
        pass

        if billart != 0:

            # h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, billart)],"departement": [(eq, curr_dept)],"datum": [(eq, bill_date)]})
            h_umsatz = db_session.query(H_umsatz).filter(
                     (H_umsatz.artnr == billart) & (H_umsatz.departement == curr_dept) & (H_umsatz.datum == bill_date)).with_for_update().first()

            if not h_umsatz:
                h_umsatz = H_umsatz()
                db_session.add(h_umsatz)

                h_umsatz.artnr = billart
                h_umsatz.datum = bill_date
                h_umsatz.departement = curr_dept


            h_umsatz.betrag =  to_decimal(h_umsatz.betrag) + to_decimal(amount)
            h_umsatz.anzahl = h_umsatz.anzahl + qty


            pass
        h_journal = H_journal()
        db_session.add(h_journal)

        h_journal.rechnr = h_bill.rechnr
        h_journal.artnr = billart
        h_journal.anzahl = qty
        h_journal.fremdwaehrng =  to_decimal(amount_foreign)

        if h_artikel:
            h_journal.artart = h_artikel.artart

        if h_artart == 6 and h_artikel:
            h_journal.betrag =  to_decimal(amount)

            # umsatz = get_cache (Umsatz, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, 0)],"datum": [(eq, bill_date)]})
            umsatz = db_session.query(Umsatz).filter(
                     (Umsatz.artnr == h_artikel.artnrfront) & (Umsatz.departement == 0) & (Umsatz.datum == bill_date)).with_for_update().first()

            if umsatz:
                pass
            else:
                umsatz = Umsatz()
                db_session.add(umsatz)

                umsatz.artnr = h_artikel.artnrfront
                umsatz.datum = bill_date
                umsatz.departement = 0


            umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
            umsatz.anzahl = umsatz.anzahl + qty


            pass
        else:
            h_journal.betrag =  to_decimal(amount)
        h_journal.bezeich = description + change_str
        h_journal.tischnr = tischnr
        h_journal.departement = curr_dept
        h_journal.epreis =  to_decimal(price)
        h_journal.zeit = zeit
        h_journal.stornogrund = cancel_str
        h_journal.aendertext = req_str
        h_journal.kellner_nr = to_int(user_init)
        h_journal.bill_datum = bill_date
        h_journal.sysdate = sysdate
        h_journal.artnrfront = h_artnrfront

        if avail_b_list and b_list_departement < 999:
            h_journal.bezeich = h_journal.bezeich + cc_comment

        if billart == 0:
            h_journal.artart = 0
        else:
            h_journal.artart = h_artart

        if pay_type == 2:
            h_journal.zinr = transfer_zinr

        if h_artart == 11:
            h_journal.aendertext = h_bill.bilname
            h_journal.segmentcode = billart

            if mc_str != " ":
                nett_compli =  to_decimal("0")

                hbline_obj_list = {}
                hbline = H_bill_line()
                hartikel = H_artikel()
                for hbline.bezeich, hbline.rechnr, hbline.artnr, hbline.anzahl, hbline.nettobetrag, hbline.fremdwbetrag, hbline.betrag, hbline.tischnr, hbline.departement, hbline.epreis, hbline.zeit, hbline.bill_datum, hbline.sysdate, hbline.waehrungsnr, hbline.segmentcode, hbline._recid, hartikel.departement, hartikel.service_code, hartikel.mwst_code, hartikel.artart, hartikel.artnrfront, hartikel._recid in db_session.query(Hbline.bezeich, Hbline.rechnr, Hbline.artnr, Hbline.anzahl, Hbline.nettobetrag, Hbline.fremdwbetrag, Hbline.betrag, Hbline.tischnr, Hbline.departement, Hbline.epreis, Hbline.zeit, Hbline.bill_datum, Hbline.sysdate, Hbline.waehrungsnr, Hbline.segmentcode, Hbline._recid, Hartikel.departement, Hartikel.service_code, Hartikel.mwst_code, Hartikel.artart, Hartikel.artnrfront, Hartikel._recid).join(Hartikel,(Hartikel.artnr == Hbline.artnr) & (Hartikel.departement == Hbline.departement) & (Hartikel.artart == 0)).filter(
                             (Hbline.departement == h_bill.departement) & (Hbline.rechnr == h_bill.rechnr) & (Hbline.betrag != 0)).order_by(Hbline._recid).all():
                    if hbline_obj_list.get(hbline._recid):
                        continue
                    else:
                        hbline_obj_list[hbline._recid] = True


                    nett_compli =  to_decimal(nett_compli) + to_decimal((hbline.anzahl) * to_decimal(hbline.epreis))

                # queasy = get_cache (Queasy, {"key": [(eq, 197)],"char1": [(eq, mc_str)],"date1": [(eq, bill_date)],"number1": [(eq, billart)]})
                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 197) & (Queasy.char1 == mc_str) & (Queasy.date1 == bill_date) & (Queasy.number1 == billart)).with_for_update().first()

                if not queasy:
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 197
                    queasy.char1 = mc_str
                    queasy.date1 = bill_date
                    queasy.deci1 =  to_decimal(nett_compli)
                    queasy.number1 = billart


                else:
                    pass
                    queasy.deci1 =  to_decimal(queasy.deci1) + to_decimal(nett_compli)


                    pass
                    pass
        pass
        change_str = ""
        closed = False

        if h_artart == 2 or h_artart == 7 and h_artikel:

            bill_guest = get_cache (Guest, {"_recid": [(eq, rec_bill_guest)]})

            artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, 0)]})

            if foreign_rate and not double_currency:
                amount_foreign =  to_decimal(amount) / to_decimal(exchg_rate)

            if b_list_departement == 999:
                inv_ar(artikel.artnr, curr_dept, curr_room, bill_guest.gastnr, bill_guest.gastnr, h_bill.rechnr, amount, amount_foreign, bill_date, bill_guest.name, user_init, "")
            else:
                inv_ar(artikel.artnr, curr_dept, curr_room, bill_guest.gastnr, bill_guest.gastnr, h_bill.rechnr, amount, amount_foreign, bill_date, bill_guest.name, user_init, cc_comment)

        if h_artart == 2 or h_artart == 7 or h_artart == 11 or h_artart == 12:

            if balance == 0:
                closed = True
                pass
                h_bill.flag = 1
                pass
        pass
        t_h_bill = T_h_bill()
        t_h_bill_data.append(t_h_bill)

        buffer_copy(h_bill, t_h_bill)
        t_h_bill.rec_id = h_bill._recid

    return generate_output()