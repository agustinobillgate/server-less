#using conversion tools version: 1.0.0.117

# =============================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fa_op, Bediener, L_lieferant, Mathis, Fa_artikel, Queasy, Htparam, L_op, L_kredit, Ap_journal

op_list_data, Op_list = create_model_like(Fa_op, {"name":string, "location":string})

def fa_stin_btn_gobl(op_list_data, billdate:date, user_init:string, lscheinnr:string, lief_nr:int):

    prepare_cache ([Fa_op, Bediener, L_lieferant, Mathis, Fa_artikel, Queasy, Htparam, L_kredit, Ap_journal])

    created = False
    s_artnr:int = 0
    qty:Decimal = to_decimal("0.0")
    price:Decimal = to_decimal("0.0")
    amount:Decimal = to_decimal("0.0")
    t_amount:Decimal = to_decimal("0.0")
    fa_op = bediener = l_lieferant = mathis = fa_artikel = queasy = htparam = l_op = l_kredit = ap_journal = None

    op_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal created, s_artnr, qty, price, amount, t_amount, fa_op, bediener, l_lieferant, mathis, fa_artikel, queasy, htparam, l_op, l_kredit, ap_journal
        nonlocal billdate, user_init, lscheinnr, lief_nr


        nonlocal op_list

        return {"created": created}

    def create_fa_op():

        nonlocal created, s_artnr, qty, price, amount, t_amount, fa_op, bediener, l_lieferant, mathis, fa_artikel, queasy, htparam, l_op, l_kredit, ap_journal
        nonlocal billdate, user_init, lscheinnr, lief_nr


        nonlocal op_list

        next_date:date = None
        next_mon:int = 0
        next_yr:int = 0

        # mathis = get_cache (Mathis, {"nr": [(eq, s_artnr)]})
        mathis = db_session.query(Mathis).filter(
                 (Mathis.nr == s_artnr)).with_for_update().first()

        if mathis:
            # pass
            mathis.price =  to_decimal(price)
            mathis.supplier = l_lieferant.firma
            mathis.datum = billdate
            # pass
            db_session.refresh(mathis,with_for_update=True)

            # fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, s_artnr)]})
            fa_artikel = db_session.query(Fa_artikel).filter(
                     (Fa_artikel.nr == s_artnr)).with_for_update().first()
            
            if fa_artikel:
                # pass
                fa_artikel.lief_nr = l_lieferant.lief_nr
                fa_artikel.posted = True
                fa_artikel.anzahl = qty
                fa_artikel.warenwert =  to_decimal(amount)
                fa_artikel.book_wert =  to_decimal(amount)

                queasy = get_cache (Queasy, {"key": [(eq, 314)],"number1": [(eq, s_artnr)]})

                if queasy and queasy.date1 != None:
                    next_mon = get_month(queasy.date1) + 1
                    next_yr = get_year(queasy.date1)

                    if next_mon == 13:
                        next_mon = 1
                        next_yr = next_yr + 1
                    next_date = date_mdy(next_mon, 1, next_yr) - timedelta(days=1)

                    htparam = get_cache (Htparam, {"paramnr": [(eq, 880)]})

                    if get_day(queasy.date1) <= htparam.finteger:
                        fa_artikel.next_depn = next_date
                    else:
                        fa_artikel.next_depn = next_date

                    if queasy.date1 < get_current_date():
                        next_mon = get_month(get_current_date()) + 1
                        next_yr = get_year(get_current_date())

                        if next_mon == 13:
                            next_mon = 1
                            next_yr = next_yr + 1
                        next_date = date_mdy(next_mon, 1, next_yr) - timedelta(days=1)
                        fa_artikel.next_depn = next_date
                        queasy.date1 = date_mdy(get_month(get_current_date()) , get_day(queasy.date1) , get_year(get_current_date()))
                else:
                    next_mon = get_month(billdate) + 1
                    next_yr = get_year(billdate)

                    if next_mon == 13:
                        next_mon = 1
                        next_yr = next_yr + 1
                    next_date = date_mdy(next_mon, 1, next_yr) - timedelta(days=1)

                    htparam = get_cache (Htparam, {"paramnr": [(eq, 880)]})

                    if get_day(billdate) <= htparam.finteger:
                        fa_artikel.next_depn = next_date
                    else:
                        next_mon = next_mon + 1

                        if next_mon == 13:
                            next_mon = 1
                            next_yr = next_yr + 1
                        next_date = date_mdy(next_mon, 1, next_yr) - timedelta(days=1)
                        fa_artikel.next_depn = next_date
                # pass
                # pass
                db_session.refresh(fa_artikel,with_for_update=True)
                
            fa_op = Fa_op()
            db_session.add(fa_op)

            fa_op.nr = mathis.nr
            fa_op.opart = 1
            fa_op.datum = billdate
            fa_op.zeit = get_current_time_in_seconds()
            fa_op.anzahl = qty
            fa_op.einzelpreis =  to_decimal(price)
            fa_op.warenwert =  to_decimal(amount)
            fa_op.id = user_init
            fa_op.lscheinnr = lscheinnr
            fa_op.docu_nr = lscheinnr
            fa_op.lief_nr = l_lieferant.lief_nr
            pass
            pass


    def create_ap():

        nonlocal created, s_artnr, qty, price, amount, t_amount, fa_op, bediener, l_lieferant, mathis, fa_artikel, queasy, htparam, l_op, l_kredit, ap_journal
        nonlocal billdate, user_init, lscheinnr, lief_nr


        nonlocal op_list

        l_op1 = None
        L_op1 =  create_buffer("L_op1",L_op)
        l_kredit = L_kredit()
        db_session.add(l_kredit)

        l_kredit.name = lscheinnr
        l_kredit.lief_nr = lief_nr
        l_kredit.lscheinnr = lscheinnr
        l_kredit.rgdatum = billdate
        l_kredit.datum = None
        l_kredit.saldo =  to_decimal(t_amount)
        l_kredit.ziel = 30
        l_kredit.netto =  to_decimal(t_amount)
        l_kredit.bediener_nr = bediener.nr
        l_kredit.betriebsnr = 2
        ap_journal = Ap_journal()
        db_session.add(ap_journal)

        ap_journal.lief_nr = lief_nr
        ap_journal.docu_nr = lscheinnr
        ap_journal.lscheinnr = lscheinnr
        ap_journal.rgdatum = billdate
        ap_journal.saldo =  to_decimal(t_amount)
        ap_journal.netto =  to_decimal(t_amount)
        ap_journal.userinit = bediener.userinit
        ap_journal.zeit = get_current_time_in_seconds()


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})

    if bediener and l_lieferant:

        for op_list in query(op_list_data):
            s_artnr = op_list.nr
            qty =  to_decimal(op_list.anzahl)
            price =  to_decimal(op_list.warenwert) / to_decimal(qty)
            amount =  to_decimal(op_list.warenwert)
            t_amount =  to_decimal(t_amount) + to_decimal(op_list.warenwert)
            create_fa_op()
            created = True

        if lief_nr != 0 and t_amount != 0:
            create_ap()

    return generate_output()
