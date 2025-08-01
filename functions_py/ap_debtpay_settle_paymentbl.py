#using conversion tools version: 1.0.0.27
#----------------------------------------
# Rd, 1/8/2025
# if available l_kredit1
#----------------------------------------

from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_lieferant, L_kredit, Htparam, Bediener, Counters, Umsatz, Ap_journal, L_order

pay_list_list, Pay_list = create_model("Pay_list", {"dummy":str, "artnr":int, "bezeich":str, "proz":decimal, "betrag":decimal})
age_list_list, Age_list = create_model("Age_list", {"selected":bool, "ap_recid":int, "counter":int, "docu_nr":str, "rechnr":int, "lief_nr":int, "lscheinnr":str, "supplier":str, "rgdatum":date, "rabatt":decimal, "rabattbetrag":decimal, "ziel":date, "netto":decimal, "user_init":str, "debt":decimal, "credit":decimal, "bemerk":str, "tot_debt":decimal, "rec_id":int, "resname":str, "comments":str, "fibukonto":str, "t_bezeich":str, "debt2":decimal, "recv_date":date})

def ap_debtpay_settle_paymentbl(pay_list_list:[Pay_list], age_list_list:[Age_list], user_init:str, outstand:decimal, outstand1:decimal, rundung:int, pay_date:date, remark:str):
    t_l_lieferant_list = []
    l_lieferant = l_kredit = htparam = bediener = counters = umsatz = ap_journal = l_order = None

    pay_list = age_list = t_l_lieferant = None

    t_l_lieferant_list, T_l_lieferant = create_model("T_l_lieferant", {"telefon":str, "fax":str, "adresse1":str, "notizen_1":str, "lief_nr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_lieferant_list, l_lieferant, l_kredit, htparam, bediener, counters, umsatz, ap_journal, l_order
        nonlocal user_init, outstand, outstand1, rundung, pay_date, remark


        nonlocal pay_list, age_list, t_l_lieferant
        nonlocal t_l_lieferant_list

        return {"pay-list": pay_list_list, "age-list": age_list_list, "t-l-lieferant": t_l_lieferant_list}

    def settle_payment():

        nonlocal t_l_lieferant_list, l_lieferant, l_kredit, htparam, bediener, counters, umsatz, ap_journal, l_order
        nonlocal user_init, outstand, outstand1, rundung, pay_date, remark


        nonlocal pay_list, age_list, t_l_lieferant
        nonlocal t_l_lieferant_list

        saldo_i:decimal = to_decimal("0.0")
        bill_date:date = None
        count:int = 0
        anzahl:int = 0
        supplier:str = ""
        pay_amount:decimal = to_decimal("0.0")
        payment1:decimal = to_decimal("0.0")
        l_kredit1 = None
        L_kredit1 =  create_buffer("L_kredit1",L_kredit)

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate

        bediener = db_session.query(Bediener).filter(
                 (func.lower(Bediener.userinit) == (user_init).lower())).first()

        for age_list in query(age_list_list, filters=(lambda age_list: age_list.selected)):

            l_kredit1 = db_session.query(L_kredit1).filter(
                     (L_kredit1.opart == 0) & (L_kredit1.lief_nr == age_list.lief_nr) & 
                     (L_kredit1.name == age_list.docu_nr) & (L_kredit1.lscheinnr == age_list.lscheinnr) & 
                     (L_kredit1.rgdatum == age_list.rgdatum) & (L_kredit1.saldo == age_list.debt)).first()

            # Rd 1/8/2025
            # if available
            # l_lieferant = db_session.query(L_lieferant).filter(
            #          (L_lieferant.lief_nr == l_kredit1.lief_nr)).first()

            if l_kredit1 is None:
                continue

            l_lieferant = db_session.query(L_lieferant).filter(
                     (L_lieferant.lief_nr == l_kredit1.lief_nr)).first()

            supplier = l_lieferant.firma
            saldo_i =  to_decimal(age_list.tot_debt)
            payment1 =  - to_decimal(saldo_i)

            if outstand == 0:
                l_kredit1.opart = 2
                del_po(l_kredit1._recid, l_kredit1.lscheinnr)
            l_kredit1.datum = pay_date

            if num_entries(l_kredit1.bemerk, ";") > 1:
                l_kredit1.bemerk = entry(0, l_kredit1.bemerk, ";", remark)
            else:
                l_kredit1.bemerk = remark
            count = l_kredit1.counter

            if count == 0:

                counters = db_session.query(Counters).filter(
                         (Counters.counter_no == 24)).first()

                if not counters:
                    counters = Counters()
                    db_session.add(counters)

                    counters.counter_no = 24
                    counters.counter_bez = "Accounts Payable"
                counters.counter = counters.counter + 1
                l_kredit1.counter = counters.counter
                count = l_kredit1.counter
                pass

            elif count != 0 and outstand == 0:

                for l_kredit in db_session.query(L_kredit).filter(
                         (L_kredit.opart >= 1) & (L_kredit.counter == count) & (L_kredit.name == age_list.docu_nr) & (L_kredit.zahlkonto > 0) & (L_kredit.lief_nr == age_list.lief_nr)).order_by(L_kredit._recid).all():
                    l_kredit.opart = 2
                    payment1 =  to_decimal(payment1) - to_decimal(l_kredit.saldo)
                    pass

            for pay_list in query(pay_list_list):

                if pay_list.proz == 100:
                    pay_amount =  - to_decimal(saldo_i)
                else:
                    pay_amount =  to_decimal(saldo_i) / to_decimal(outstand1) * to_decimal(pay_list.betrag)

                    if outstand == 0:

                        if round (payment1 - pay_amount, rundung) == 0:
                            pay_amount =  to_decimal(payment1)

                if age_list.tot_debt != 0:
                    l_kredit = L_kredit()
                    db_session.add(l_kredit)

                    l_kredit.lief_nr = age_list.lief_nr

                    if outstand != 0:
                        l_kredit.opart = 1
                    else:
                        l_kredit.opart = 2
                    l_kredit.name = age_list.docu_nr
                    l_kredit.rechnr = age_list.rechnr
                    l_kredit.lief_nr = age_list.lief_nr
                    l_kredit.lscheinnr = age_list.lscheinnr
                    l_kredit.saldo =  to_decimal(pay_amount)
                    l_kredit.rabatt =  to_decimal(age_list.rabatt)
                    l_kredit.rabattbetrag =  to_decimal(age_list.rabattbetrag)
                    l_kredit.netto =  to_decimal(age_list.netto)
                    l_kredit.zahlkonto = pay_list.artnr
                    l_kredit.counter = count
                    l_kredit.rgdatum = pay_date
                    l_kredit.bediener_nr = bediener.nr

                    if num_entries(l_kredit.bemerk, ";") > 1:
                        l_kredit.bemerk = entry(0, l_kredit.bemerk, ";", remark)
                    else:
                        l_kredit.bemerk = remark
                    l_kredit1.skontobetrag =  to_decimal(l_kredit1.skontobetrag) + to_decimal(l_kredit.saldo)

                    umsatz = db_session.query(Umsatz).filter(
                             (Umsatz.departement == 0) & (Umsatz.artnr == pay_list.artnr) & (Umsatz.datum == pay_date)).first()

                    if not umsatz:
                        umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.datum = pay_date
                    umsatz.artnr = pay_list.artnr
                    umsatz.anzahl = umsatz.anzahl + 1
                    umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(l_kredit.saldo)
                    pass
                    ap_journal = Ap_journal()
                    db_session.add(ap_journal)

                    ap_journal.lief_nr = age_list.lief_nr
                    ap_journal.docu_nr = age_list.docu_nr
                    ap_journal.lscheinnr = age_list.lscheinnr
                    ap_journal.rgdatum = pay_date
                    ap_journal.saldo =  to_decimal(l_kredit.saldo)
                    ap_journal.netto =  to_decimal(l_kredit.netto)
                    ap_journal.zahlkonto = l_kredit.zahlkonto
                    ap_journal.userinit = bediener.userinit
                    ap_journal.zeit = get_current_time_in_seconds()


    def del_po(ap_recid:int, docu_nr:str):

        nonlocal t_l_lieferant_list, l_lieferant, l_kredit, htparam, bediener, counters, umsatz, ap_journal, l_order
        nonlocal user_init, outstand, outstand1, rundung, pay_date, remark


        nonlocal pay_list, age_list, t_l_lieferant
        nonlocal t_l_lieferant_list

        l_od = None
        l_ap = None
        L_od =  create_buffer("L_od",L_order)
        L_ap =  create_buffer("L_ap",L_kredit)

        l_od = db_session.query(L_od).filter(
                 (func.lower(L_od.docu_nr) == (docu_nr).lower()) & (L_od.pos == 0)).first()

        if not l_od:

            return

        if l_od.loeschflag == 0:

            return

        l_ap = db_session.query(L_ap).filter(
                 (func.lower(L_ap.lscheinnr) == (docu_nr).lower()) & (L_ap.opart == 0) & (L_ap._recid != ap_recid)).first()

        if l_ap:

            return

        bediener = db_session.query(Bediener).filter(
                 (func.lower(Bediener.userinit) == (user_init).lower())).first()
        l_od.loeschflag = 2
        l_od.lieferdatum_eff = pay_date
        l_od.lief_fax[2] = bediener.username

        for l_od in db_session.query(L_od).filter(
                 (func.lower(L_od.docu_nr) == (docu_nr).lower()) & (L_od.pos > 0) & (L_od.loeschflag == 0)).order_by(L_od._recid).all():
            l_od.loeschflag = 2
            l_od.lieferdatum = pay_date
            l_od.lief_fax[1] = bediener.username
            pass

    settle_payment()

    for age_list in query(age_list_list):

        l_lieferant = db_session.query(L_lieferant).filter(
                 (L_lieferant.lief_nr == age_list.lief_nr)).first()

        if l_lieferant:

            t_l_lieferant = query(t_l_lieferant_list, filters=(lambda t_l_lieferant: t_l_lieferant.lief_nr == l_lieferant.lief_nr), first=True)

            if not t_l_lieferant:
                t_l_lieferant = T_l_lieferant()
                t_l_lieferant_list.append(t_l_lieferant)

                t_l_lieferant.telefon = l_lieferant.telefon
                t_l_lieferant.fax = l_lieferant.fax
                t_l_lieferant.adresse1 = l_lieferant.adresse1
                t_l_lieferant.notizen_1 = l_lieferant.notizen[0]
                t_l_lieferant.lief_nr = l_lieferant.lief_nr

    return generate_output()