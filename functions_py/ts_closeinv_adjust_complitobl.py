#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import H_bill, Artikel, H_bill_line, H_artikel, Kellner, Htparam, H_umsatz, Umsatz, Arrangement, Argt_line, Billjournal, H_journal, H_compli
from sqlalchemy_orm import flag_modified

def ts_closeinv_adjust_complitobl(rec_h_bill:int, p_sign:int, p_artnr:int, h_artart:int, curr_dept:int, pay_type:int, 
                                  double_currency:bool, exchg_rate:Decimal, price_decimal:int, user_init:string):

    prepare_cache ([Artikel, H_artikel, Htparam, H_umsatz, Umsatz, Arrangement, Argt_line, Billjournal, H_journal, H_compli])

    balance_foreign = to_decimal("0.0")
    balance = to_decimal("0.0")
    t_h_bill_data = []
    h_bill = artikel = h_bill_line = h_artikel = kellner = htparam = h_umsatz = umsatz = arrangement = argt_line = billjournal = h_journal = h_compli = None

    t_h_bill = None

    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal balance_foreign, balance, t_h_bill_data, h_bill, artikel, h_bill_line, h_artikel, kellner, htparam, h_umsatz, umsatz, arrangement, argt_line, billjournal, h_journal, h_compli
        nonlocal rec_h_bill, p_sign, p_artnr, h_artart, curr_dept, pay_type, double_currency, exchg_rate, price_decimal, user_init


        nonlocal t_h_bill
        nonlocal t_h_bill_data

        return {"balance_foreign": balance_foreign, "balance": balance, "t-h-bill": t_h_bill_data}

    def adjust_complito():

        nonlocal balance_foreign, balance, t_h_bill_data, h_bill, artikel, h_bill_line, h_artikel, kellner, htparam, h_umsatz, umsatz, arrangement, argt_line, billjournal, h_journal, h_compli
        nonlocal rec_h_bill, p_sign, p_artnr, h_artart, curr_dept, pay_type, double_currency, exchg_rate, price_decimal, user_init


        nonlocal t_h_bill
        nonlocal t_h_bill_data

        rest_betrag:Decimal = to_decimal("0.0")
        argt_betrag:Decimal = to_decimal("0.0")
        h_mwst:Decimal = to_decimal("0.0")
        h_service:Decimal = to_decimal("0.0")
        h_mwst_foreign:Decimal = to_decimal("0.0")
        h_service_foreign:Decimal = to_decimal("0.0")
        epreis:Decimal = to_decimal("0.0")
        amount:Decimal = to_decimal("0.0")
        amount_foreign:Decimal = to_decimal("0.0")
        cost:Decimal = to_decimal("0.0")
        f_cost:Decimal = to_decimal("0.0")
        b_cost:Decimal = to_decimal("0.0")
        f_eknr:int = 0
        b_eknr:int = 0
        f_disc:int = 0
        b_disc:int = 0
        o_disc:int = 0
        artikel1 = None
        h_bline = None
        h_art = None
        fr_art = None
        kellner1 = None
        kellne1 = None
        Artikel1 =  create_buffer("Artikel1",Artikel)
        H_bline =  create_buffer("H_bline",H_bill_line)
        H_art =  create_buffer("H_art",H_artikel)
        Fr_art =  create_buffer("Fr_art",Artikel)
        Kellner1 =  create_buffer("Kellner1",Kellner)
        Kellne1 =  create_buffer("Kellne1",Kellner)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
        f_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
        b_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})
        f_disc = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})
        b_disc = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})
        o_disc = htparam.finteger

        h_bline = db_session.query(H_bline).filter(
                 (H_bline.rechnr == h_bill.rechnr) & (H_bline.departement == curr_dept)).first()
        while None != h_bline:

            h_art = get_cache (H_artikel, {"artnr": [(eq, h_bline.artnr)],"departement": [(eq, h_bline.departement)]})

            if h_art and h_art.artart == 0:
                h_service =  to_decimal("0")
                h_mwst =  to_decimal("0")
                h_service_foreign =  to_decimal("0")
                h_mwst_foreign =  to_decimal("0")
                amount =  to_decimal("0")
                amount_foreign =  to_decimal("0")

                # h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_art.artnr)],"departement": [(eq, h_art.departement)],"datum": [(eq, h_bline.bill_datum)]})
                h_umsatz = db_session.query(H_umsatz).filter(
                             (H_umsatz.artnr == h_art.artnr) & (H_umsatz.departement == h_art.departement) & (H_umsatz.datum == h_bline.bill_datum)).with_for_update().first()

                if h_umsatz and pay_type == 5:
                    h_umsatz.betrag =  to_decimal(h_umsatz.betrag) - to_decimal(p_sign) * to_decimal(h_bline.betrag)
                    h_umsatz.anzahl = h_umsatz.anzahl - p_sign * h_bline.anzahl
                    pass

                # umsatz = get_cache (Umsatz, {"artnr": [(eq, h_art.artnrfront)],"departement": [(eq, h_art.departement)],"datum": [(eq, h_bline.bill_datum)]})
                umsatz = db_session.query(Umsatz).filter(
                             (Umsatz.artnr == h_art.artnrfront) & (Umsatz.departement == h_art.departement) & (Umsatz.datum == h_bline.bill_datum)).with_for_update().first()

                if umsatz:
                    umsatz.betrag =  to_decimal(umsatz.betrag) - to_decimal(p_sign) * to_decimal(h_bline.betrag)
                    umsatz.anzahl = umsatz.anzahl - p_sign * h_bline.anzahl
                    pass

                artikel = get_cache (Artikel, {"artnr": [(eq, umsatz.artnr)],"departement": [(eq, umsatz.departement)]})

                if artikel.artart == 9:
                    amount =  to_decimal(p_sign) * to_decimal(h_bline.betrag)
                    rest_betrag =  to_decimal(amount)

                    arrangement = get_cache (Arrangement, {"argtnr": [(eq, artikel.artgrp)]})

                    for argt_line in db_session.query(Argt_line).filter(
                             (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line._recid).all():

                        if argt_line.betrag != 0:
                            argt_betrag =  to_decimal(p_sign) * to_decimal(argt_line.betrag) * to_decimal(h_bline.anzahl)

                            if double_currency or artikel.pricetab:
                                argt_betrag = to_decimal(round(argt_betrag * exchg_rate , price_decimal))
                        else:
                            argt_betrag =  to_decimal(amount) * to_decimal(argt_line.vt_percnt) / to_decimal("100")
                            argt_betrag = to_decimal(round(argt_betrag , price_decimal))


                        rest_betrag =  to_decimal(rest_betrag) - to_decimal(argt_betrag)

                        artikel1 = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})

                        # umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, h_bline.bill_datum)]})
                        umsatz = db_session.query(Umsatz).filter(
                                     (Umsatz.artnr == artikel1.artnr) & (Umsatz.departement == artikel1.departement) & (Umsatz.datum == h_bline.bill_datum)).with_for_update().first()

                        if not umsatz:
                            umsatz = Umsatz()
                            db_session.add(umsatz)

                            umsatz.artnr = artikel1.artnr
                            umsatz.datum = h_bline.bill_datum
                            umsatz.departement = artikel1.departement


                        umsatz.betrag =  to_decimal(umsatz.betrag) - to_decimal(argt_betrag)
                        umsatz.anzahl = umsatz.anzahl - p_sign * h_bline.anzahl


                        pass
                        billjournal = Billjournal()
                        db_session.add(billjournal)

                        billjournal.rechnr = h_bline.rechnr
                        billjournal.artnr = artikel1.artnr
                        billjournal.anzahl = - p_sign * h_bline.anzahl
                        billjournal.betrag =  - to_decimal(argt_betrag)
                        billjournal.bezeich = artikel1.bezeich +\
                                "<" + to_string(h_bline.departement, "99") + ">"
                        billjournal.departement = artikel1.departement
                        billjournal.epreis =  to_decimal("0")
                        billjournal.zeit = get_current_time_in_seconds()
                        billjournal.userinit = user_init
                        billjournal.bill_datum = h_bline.bill_datum


                        pass

                    artikel1 = get_cache (Artikel, {"artnr": [(eq, arrangement.artnr_logis)],"departement": [(eq, arrangement.intervall)]})

                    # umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, h_bline.bill_datum)]})
                    umsatz = db_session.query(Umsatz).filter(
                                 (Umsatz.artnr == artikel1.artnr) & (Umsatz.departement == artikel1.departement) & (Umsatz.datum == h_bline.bill_datum)).with_for_update().first()

                    if not umsatz:
                        umsatz = Umsatz()
                        db_session.add(umsatz)

                        umsatz.artnr = artikel1.artnr
                        umsatz.datum = h_bline.bill_datum
                        umsatz.departement = artikel1.departement


                    umsatz.betrag =  to_decimal(umsatz.betrag) - to_decimal(rest_betrag)
                    umsatz.anzahl = umsatz.anzahl - p_sign * h_bline.anzahl


                    pass
                    billjournal = Billjournal()
                    db_session.add(billjournal)

                    billjournal.rechnr = h_bline.rechnr
                    billjournal.artnr = artikel1.artnr
                    billjournal.anzahl = - p_sign * h_bline.anzahl
                    billjournal.betrag =  - to_decimal(rest_betrag)
                    billjournal.bezeich = artikel1.bezeich +\
                            "<" + to_string(h_bline.departement, "99") + ">"
                    billjournal.departement = artikel1.departement
                    billjournal.epreis =  to_decimal("0")
                    billjournal.zeit = get_current_time_in_seconds()
                    billjournal.userinit = user_init
                    billjournal.bill_datum = h_bline.bill_datum


                    pass

                if h_bline.artnr != f_disc and h_bline.artnr != b_disc and h_bline.artnr != o_disc:

                    # h_journal = get_cache (H_journal, {"bill_datum": [(eq, h_bline.bill_datum)],"zeit": [(eq, h_bline.zeit)],"sysdate": [(eq, h_bline.sysdate)],"artnr": [(eq, h_bline.artnr)],"departement": [(eq, h_bline.departement)]})
                    h_journal = db_session.query(H_journal).filter(
                                 (H_journal.bill_datum == h_bline.bill_datum) & (H_journal.zeit == h_bline.zeit) & 
                                 (H_journal.sysdate == h_bline.sysdate) & (H_journal.artnr == h_bline.artnr) & 
                                 (H_journal.departement == h_bline.departement)).with_for_update().first()
                    
                    h_journal.fremdwaehrng =  to_decimal(h_bline.fremdwbetrag)
                    h_journal.betrag =  to_decimal(h_bline.betrag)
                    pass
                pass
                h_bill.gesamtumsatz =  to_decimal(h_bill.gesamtumsatz) - to_decimal(p_sign) * to_decimal(h_bline.betrag)
                h_bill.mwst[98] = h_bill.mwst[98] - p_sign * (h_service_foreign + h_mwst_foreign) * h_bline.anzahl
                h_bill.saldo =  to_decimal(h_bill.saldo) - to_decimal(p_sign) * to_decimal((h_service) + to_decimal(h_mwst)) * to_decimal(h_bline.anzahl)
                pass
                balance_foreign =  to_decimal(h_bill.mwst[98])
                balance =  to_decimal(h_bill.saldo)

                if h_artart == 11:
                    h_compli = H_compli()
                    db_session.add(h_compli)

                    h_compli.datum = h_bline.bill_datum
                    h_compli.departement = h_bline.departement
                    h_compli.rechnr = h_bline.rechnr
                    h_compli.artnr = h_bline.artnr
                    h_compli.anzahl = p_sign * h_bline.anzahl
                    h_compli.epreis =  to_decimal(h_bline.epreis)
                    h_compli.p_artnr = p_artnr
                    pass

            curr_recid = h_bline._recid
            h_bline = db_session.query(H_bline).filter(
                     (H_bline.rechnr == h_bill.rechnr) & (H_bline.departement == curr_dept) & (H_bline._recid > curr_recid)).first()
            flag_modified(h_bill, "mwst")

    # h_bill = get_cache (H_bill, {"_recid": [(eq, rec_h_bill)]})
    h_bill = db_session.query(H_bill).filter(
             (H_bill._recid == rec_h_bill)).with_for_update().first()
    adjust_complito()

    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_h_bill)]})
    t_h_bill = T_h_bill()
    t_h_bill_data.append(t_h_bill)

    buffer_copy(h_bill, t_h_bill)
    t_h_bill.rec_id = h_bill._recid

    return generate_output()