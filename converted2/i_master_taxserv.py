#using conversion tools version: 1.0.0.20

from functions.additional_functions import *
import decimal
from functions.argt_betrag import argt_betrag
from models import Artikel, Bill, Htparam, Res_line, Argt_line, Billjournal, Umsatz, Bill_line

def i_master_taxserv():
    artikel = bill = htparam = res_line = argt_line = billjournal = umsatz = bill_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal artikel, bill, htparam, res_line, argt_line, billjournal, umsatz, bill_line

        return {}

    def master_taxserv(recid_mbill:int, currzeit:int):

        nonlocal artikel, bill, htparam, res_line, argt_line, billjournal, umsatz, bill_line

        service:decimal = to_decimal("0.0")
        vat:decimal = to_decimal("0.0")
        service_foreign:decimal = to_decimal("0.0")
        vat_foreign:decimal = to_decimal("0.0")
        argt_betrag0:decimal = to_decimal("0.0")
        argt_betrag:decimal = to_decimal("0.0")
        rest_betrag:decimal = to_decimal("0.0")
        frate:decimal = to_decimal("0.0")
        p_sign:int = 1
        qty1:int = 0
        rm_vat:bool = False
        rm_serv:bool = False
        post_it:bool = False
        artikel1 = None
        mbill = None
        Artikel1 =  create_buffer("Artikel1",Artikel)
        Mbill =  create_buffer("Mbill",Bill)

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 127)).first()
        rm_vat = not htparam.flogical

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 128)).first()
        rm_serv = not htparam.flogical

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.parent_nr)).first()

        if res_line.adrflag:
            frate =  to_decimal("1")

        elif res_line.reserve_dec != 0:
            frate =  to_decimal(res_line.reserve_dec)
        else:
            frate =  to_decimal(exchg_rate)

        mbill = db_session.query(Mbill).filter(
                 (Mbill._recid == recid_mbill)).first()
        rest_betrag =  to_decimal(amount)

        if amount < 0:
            p_sign = -1

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():
            post_it = False
            argt_betrag0, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
            argt_betrag = to_decimal(round(argt_betrag0 * ex_rate , price_decimal))

            artikel1 = db_session.query(Artikel1).filter(
                     (Artikel1.artnr == argt_line.argt_artnr) & (Artikel1.departement == argt_line.departement)).first()

            if argt_line.fakt_modus == 1:
                post_it = True

            elif argt_line.fakt_modus == 2:

                billjournal = db_session.query(Billjournal).filter(
                         (Billjournal.rechnr == bill.rechnr) & (Billjournal.artnr == artikel1.artnr) & (Billjournal.betrag == argt_betrag) & (Billjournal.departement == artikel1.departement)).first()

                if not billjournal:
                    post_it = True

            elif argt_line.fakt_modus == 3:

                if (res_line.ankunft + 1) == bill_date:
                    post_it = True

            elif argt_line.fakt_modus == 4:

                if get_day(bill_date) == 1:
                    post_it = True

            elif argt_line.fakt_modus == 5:

                if get_day(bill_date + 1) == 1:
                    post_it = True

            if post_it and argt_betrag != 0:

                if argt_line.vt_percnt == 0:

                    if argt_line.betriebsnr == 0:
                        qty1 = res_line.erwachs * p_sign
                    else:
                        qty1 = argt_line.betriebsnr * p_sign

                elif argt_line.vt_percnt == 1:

                    if argt_line.betriebsnr == 0:
                        qty1 = res_line.kind1 * p_sign
                    else:
                        qty1 = argt_line.betriebsnr * p_sign

                if argt_line.vt_percnt == 2:

                    if argt_line.betriebsnr == 0:
                        qty1 = res_line.kind2 * p_sign
                    else:
                        qty1 = argt_line.betriebsnr * p_sign
                rest_betrag =  to_decimal(rest_betrag) - to_decimal(argt_betrag) * to_decimal(p_sign)

                artikel1 = db_session.query(Artikel1).filter(
                         (Artikel1.artnr == argt_line.argt_artnr) & (Artikel1.departement == argt_line.departement)).first()

                umsatz = db_session.query(Umsatz).filter(
                         (Umsatz.artnr == artikel1.artnr) & (Umsatz.departement == artikel1.departement) & (Umsatz.datum == bill_date)).first()

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement
                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(argt_betrag) * to_decimal(p_sign)
                umsatz.anzahl = umsatz.anzahl + qty1
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty1
                billjournal.fremdwaehrng =  to_decimal(argt_betrag0) * to_decimal(p_sign)
                billjournal.betrag =  to_decimal(argt_betrag) * to_decimal(p_sign)
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = res_line.zinr
                billjournal.departement = artikel1.departement
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = currzeit
                billjournal.userinit = userinit
                billjournal.bill_datum = bill_date
                pass

        artikel1 = db_session.query(Artikel1).filter(
                 (Artikel1.artnr == arrangement.artnr_logis) & (Artikel1.departement == curr_department)).first()

        umsatz = db_session.query(Umsatz).filter(
                 (Umsatz.artnr == artikel1.artnr) & (Umsatz.departement == artikel1.departement) & (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel1.artnr
            umsatz.datum = bill_date
            umsatz.departement = artikel1.departement
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(rest_betrag)
        umsatz.anzahl = umsatz.anzahl + qty
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = mbill.rechnr
        billjournal.artnr = artikel1.artnr
        billjournal.anzahl = qty
        billjournal.fremdwaehrng = to_decimal(round(rest_betrag / exchg_rate , 2))
        billjournal.betrag =  to_decimal(rest_betrag)
        billjournal.bezeich = artikel1.bezeich
        billjournal.zinr = curr_room
        billjournal.departement = artikel1.departement
        billjournal.epreis =  to_decimal("0")
        billjournal.zeit = currzeit
        billjournal.stornogrund = cancel_str
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date
        pass

        if rm_serv and artikel.service_code != 0:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == artikel.service_code)).first()

            if htparam and htparam.fdecimal != 0:
                service =  to_decimal(htparam.fdecimal)

                htparam = db_session.query(Htparam).filter(
                         (Htparam.paramnr == 133)).first()

                artikel1 = db_session.query(Artikel1).filter(
                         (Artikel1.artnr == htparam.finteger) & (Artikel1.departement == curr_department)).first()
                service =  to_decimal(service) * to_decimal(price) / to_decimal("100")
                service_foreign = to_decimal(round(service , 2) * qty)

                if double_currency:
                    service = to_decimal(round(service * exchg_rate , price_decimal) * qty)
                else:
                    service = to_decimal(round(service , price_decimal) * qty)

                if artikel1.umsatzart == 1:
                    bill.logisumsatz =  to_decimal(bill.logisumsatz) + to_decimal(service)

                elif artikel1.umsatzart == 2:
                    bill.argtumsatz =  to_decimal(bill.argtumsatz) + to_decimal(service)

                elif artikel1.umsatzart == 3:
                    bill.f_b_umsatz =  to_decimal(bill.f_b_umsatz) + to_decimal(service)

                elif artikel1.umsatzart == 4:
                    bill.sonst_umsatz =  to_decimal(bill.sonst_umsatz) + to_decimal(service)

                if artikel1.umsatzart >= 1 and artikel1.umsatzart <= 4:
                    bill.gesamtumsatz =  to_decimal(bill.gesamtumsatz) + to_decimal(service)
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = mbill.rechnr
                bill_line.artnr = artikel1.artnr
                bill_line.bezeich = artikel1.bezeich
                bill_line.anzahl = qty
                bill_line.fremdwbetrag =  to_decimal(service_foreign)
                bill_line.betrag =  to_decimal(service)
                bill_line.zinr = curr_room
                bill_line.departement = artikel1.departement
                bill_line.epreis =  to_decimal("0")
                bill_line.zeit = currzeit + 1
                bill_line.userinit = user_init
                bill_line.arrangement = res_line.arrangement
                bill_line.bill_datum = bill_date

                umsatz = db_session.query(Umsatz).filter(
                         (Umsatz.artnr == artikel1.artnr) & (Umsatz.departement == curr_department) & (Umsatz.datum == bill_date)).first()

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement
                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(service)
                umsatz.anzahl = umsatz.anzahl + qty
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = mbill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty
                billjournal.fremdwaehrng =  to_decimal(service_foreign)
                billjournal.betrag =  to_decimal(service)
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = curr_room
                billjournal.departement = artikel1.departement
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = currzeit + 1
                billjournal.stornogrund = cancel_str
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date
                pass

        if rm_vat and artikel.mwst_code != 0:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == artikel.mwst_code)).first()

            if htparam and htparam.fdecimal != 0:
                vat =  to_decimal(htparam.fdecimal)

                if (service * qty) < 0:
                    service =  - to_decimal(service)

                htparam = db_session.query(Htparam).filter(
                         (Htparam.paramnr == 132)).first()

                artikel1 = db_session.query(Artikel1).filter(
                         (Artikel1.artnr == htparam.finteger) & (Artikel1.departement == curr_department)).first()

                htparam = db_session.query(Htparam).filter(
                         (Htparam.paramnr == 479)).first()

                if htparam.flogical:
                    vat =  to_decimal(vat) * to_decimal((price) + to_decimal(service_foreign) / to_decimal(qty)) / to_decimal("100")
                else:
                    vat =  to_decimal(vat) * to_decimal(price) / to_decimal("100")
                vat_foreign = to_decimal(round(vat , 2) * qty)

                if double_currency:
                    vat = to_decimal(round(vat * exchg_rate , price_decimal) * qty)
                else:
                    vat = to_decimal(round(vat , price_decimal) * qty)

                if artikel1.umsatzart == 1:
                    mbill.logisumsatz =  to_decimal(mbill.logisumsatz) + to_decimal(vat)

                elif artikel1.umsatzart == 2:
                    mbill.argtumsatz =  to_decimal(mbill.argtumsatz) + to_decimal(vat)

                elif artikel1.umsatzart == 3:
                    mbill.f_b_umsatz =  to_decimal(mbill.f_b_umsatz) + to_decimal(vat)

                elif artikel1.umsatzart == 4:
                    mbill.sonst_umsatz =  to_decimal(mbill.sonst_umsatz) + to_decimal(vat)

                if artikel1.umsatzart >= 1 and artikel1.umsatzart <= 4:
                    mbill.gesamtumsatz =  to_decimal(mbill.gesamtumsatz) + to_decimal(vat)
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = mbill.rechnr
                bill_line.artnr = artikel1.artnr
                bill_line.bezeich = artikel1.bezeich
                bill_line.anzahl = qty
                bill_line.fremdwbetrag =  to_decimal(vat_foreign)
                bill_line.betrag =  to_decimal(vat)
                bill_line.zinr = curr_room
                bill_line.departement = artikel1.departement
                bill_line.epreis =  to_decimal("0")
                bill_line.zeit = currzeit + 2
                bill_line.userinit = user_init
                bill_line.arrangement = res_line.arrangement
                bill_line.bill_datum = bill_date

                umsatz = db_session.query(Umsatz).filter(
                         (Umsatz.artnr == artikel1.artnr) & (Umsatz.departement == curr_department) & (Umsatz.datum == bill_date)).first()

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement
                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(vat)
                umsatz.anzahl = umsatz.anzahl + qty
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = mbill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty
                billjournal.fremdwaehrng =  to_decimal(vat_foreign)
                billjournal.betrag =  to_decimal(vat)
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = curr_room
                billjournal.departement = artikel1.departement
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = currzeit + 2
                billjournal.stornogrund = cancel_str
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date
                pass
        mbill.saldo =  to_decimal(mbill.saldo) + to_decimal(vat) + to_decimal(service)
        mbill.mwst[98] = mbill.mwst[98] + vat_foreign + service_foreign