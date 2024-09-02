from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Fa_op, Bediener, L_lieferant, Mathis, Fa_artikel, Htparam, L_op, L_kredit, Ap_journal

def fa_stin_btn_gobl(op_list:[Op_list], billdate:date, user_init:str, lscheinnr:str, lief_nr:int):
    created = False
    s_artnr:int = 0
    qty:decimal = 0
    price:decimal = 0
    amount:decimal = 0
    t_amount:decimal = 0
    fa_op = bediener = l_lieferant = mathis = fa_artikel = htparam = l_op = l_kredit = ap_journal = None

    op_list = l_op1 = None

    op_list_list, Op_list = create_model_like(Fa_op, {"name":str, "location":str})

    L_op1 = L_op

    db_session = local_storage.db_session

    def generate_output():
        nonlocal created, s_artnr, qty, price, amount, t_amount, fa_op, bediener, l_lieferant, mathis, fa_artikel, htparam, l_op, l_kredit, ap_journal
        nonlocal l_op1


        nonlocal op_list, l_op1
        nonlocal op_list_list
        return {"created": created}

    def create_fa_op():

        nonlocal created, s_artnr, qty, price, amount, t_amount, fa_op, bediener, l_lieferant, mathis, fa_artikel, htparam, l_op, l_kredit, ap_journal
        nonlocal l_op1


        nonlocal op_list, l_op1
        nonlocal op_list_list

        next_date:date = None
        next_mon:int = 0
        next_yr:int = 0

        mathis = db_session.query(Mathis).filter(
                    (Mathis.nr == s_artnr)).first()
        mathis.price = price
        mathis.supplier = l_lieferant.firma
        mathis.datum = billdate

        mathis = db_session.query(Mathis).first()

        fa_artikel = db_session.query(Fa_artikel).filter(
                    (Fa_artikel.nr == s_artnr)).first()
        fa_artikel.lief_nr = l_lieferant.lief_nr
        fa_artikel.posted = True
        fa_artikel.anzahl = qty
        fa_artikel.warenwert = amount
        fa_artikel.book_wert = amount
        next_mon = get_month(billdate) + 1
        next_yr = get_year(billdate)

        if next_mon == 13:
            next_mon = 1
            next_yr = next_yr + 1
        next_date = date_mdy(next_mon, 1, next_yr) - 1

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 880)).first()

        if get_day(billdate) <= htparam.finteger:
            fa_artikel.next_depn = next_date
        else:
            next_mon = next_mon + 1

            if next_mon == 13:
                next_mon = 1
                next_yr = next_yr + 1
            next_date = date_mdy(next_mon, 1, next_yr) - 1
            fa_artikel.next_depn = next_date

        fa_artikel = db_session.query(Fa_artikel).first()
        fa_op = Fa_op()
        db_session.add(fa_op)

        fa_op.nr = mathis.nr
        fa_op.opart = 1
        fa_op.datum = billdate
        fa_op.zeit = get_current_time_in_seconds()
        fa_op.anzahl = qty
        fa_op.einzelpreis = price
        fa_op.warenwert = amount
        fa_op.id = user_init
        fa_op.lscheinnr = lscheinnr
        fa_op.docu_nr = lscheinnr
        fa_op.lief_nr = l_lieferant.lief_nr

    def create_ap():

        nonlocal created, s_artnr, qty, price, amount, t_amount, fa_op, bediener, l_lieferant, mathis, fa_artikel, htparam, l_op, l_kredit, ap_journal
        nonlocal l_op1


        nonlocal op_list, l_op1
        nonlocal op_list_list


        L_op1 = L_op
        l_kredit = L_kredit()
        db_session.add(l_kredit)

        l_kredit.name = lscheinnr
        l_kredit.lief_nr = lief_nr
        l_kredit.lscheinnr = lscheinnr
        l_kredit.rgdatum = billdate
        l_kredit.datum = None
        l_kredit.saldo = t_amount
        l_kredit.ziel = 30
        l_kredit.netto = t_amount
        l_kredit.bediener_nr = bediener.nr
        l_kredit.betriebsnr = 2
        ap_journal = Ap_journal()
        db_session.add(ap_journal)

        ap_journal.lief_nr = lief_nr
        ap_journal.docu_nr = lscheinnr
        ap_journal.lscheinnr = lscheinnr
        ap_journal.rgdatum = billdate
        ap_journal.saldo = t_amount
        ap_journal.netto = t_amount
        ap_journal.userinit = bediener.userinit
        ap_journal.zeit = get_current_time_in_seconds()

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == lief_nr)).first()

    for op_list in query(op_list_list):
        s_artnr = op_list.nr
        qty = op_list.anzahl
        price = op_list.warenwert / qty
        amount = op_list.warenwert
        t_amount = t_amount + op_list.warenwert
        create_fa_op()
        created = True

    if lief_nr != 0 and t_amount != 0:
        create_ap()

    return generate_output()