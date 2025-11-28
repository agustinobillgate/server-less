#using conversion tools version: 1.0.0.117

# =============================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fa_op, Fa_order, Mathis, Fa_artikel, Queasy, Htparam, Fa_ordheader, Bediener, L_kredit, Ap_journal

op_list_data, Op_list = create_model_like(Fa_op, {"counter":int})

def fa_recpo_btn_gobl(op_list_data, docu_nr:string, billdate:date, user_init:string, supplier_nr:int, supp_name:string, del_note:string, order_nr:string):

    prepare_cache ([Fa_op, Fa_order, Mathis, Fa_artikel, Queasy, Htparam, Fa_ordheader, Bediener, L_kredit, Ap_journal])

    allowclose = True
    art_nr:int = 0
    qty:int = 0
    price:Decimal = to_decimal("0.0")
    amount:Decimal = to_decimal("0.0")
    t_amount:Decimal = to_decimal("0.0")
    fa_op = fa_order = mathis = fa_artikel = queasy = htparam = fa_ordheader = bediener = l_kredit = ap_journal = None

    op_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal allowclose, art_nr, qty, price, amount, t_amount, fa_op, fa_order, mathis, fa_artikel, queasy, htparam, fa_ordheader, bediener, l_kredit, ap_journal
        nonlocal docu_nr, billdate, user_init, supplier_nr, supp_name, del_note, order_nr


        nonlocal op_list

        return {"allowclose": allowclose}

    def create_fa_op():

        nonlocal allowclose, art_nr, qty, price, amount, t_amount, fa_op, fa_order, mathis, fa_artikel, queasy, htparam, fa_ordheader, bediener, l_kredit, ap_journal
        nonlocal docu_nr, billdate, user_init, supplier_nr, supp_name, del_note, order_nr


        nonlocal op_list

        next_date:date = None
        next_mon:int = 0
        next_yr:int = 0

        # mathis = get_cache (Mathis, {"nr": [(eq, art_nr)]})
        mathis = db_session.query(Mathis).filter(
                 (Mathis.nr == art_nr) & (Mathis.flag == 1)).with_for_update().first()

        if mathis:
            # pass
            mathis.price =  to_decimal(price)
            mathis.supplier = supp_name
            mathis.datum = billdate
            # pass
            db_session.refresh(mathis,with_for_update=True)

            # fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, art_nr)]})
            fa_artikel = db_session.query(Fa_artikel).filter(
                     (Fa_artikel.nr == art_nr)).with_for_update().first()

            if fa_artikel:
                pass
                fa_artikel.lief_nr = supplier_nr
                fa_artikel.posted = True
                fa_artikel.anzahl = qty
                fa_artikel.warenwert =  to_decimal(amount)
                fa_artikel.book_wert =  to_decimal(amount)

                # queasy = get_cache (Queasy, {"key": [(eq, 314)],"number1": [(eq, art_nr)]})
                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 314) & (Queasy.number1 == art_nr)).with_for_update().first()

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
                    pass
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
                pass
                pass
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
            fa_op.lscheinnr = del_note
            fa_op.docu_nr = order_nr
            fa_op.lief_nr = supplier_nr
            fa_op.loeschflag = 0


            pass
            pass


    def close_po():

        nonlocal allowclose, art_nr, qty, price, amount, t_amount, fa_op, fa_order, mathis, fa_artikel, queasy, htparam, fa_ordheader, bediener, l_kredit, ap_journal
        nonlocal docu_nr, billdate, user_init, supplier_nr, supp_name, del_note, order_nr


        nonlocal op_list

        for fa_order in db_session.query(Fa_order).filter(
                 (Fa_order.order_nr == (order_nr).lower())).order_by(Fa_order._recid).all():

            if allowclose :

                if fa_order.order_qty == fa_order.delivered_qty:
                    allowclose = True
                else:
                    allowclose = False
            else:
                allowclose = False

        if allowclose :

            # fa_ordheader = get_cache (Fa_ordheader, {"order_nr": [(eq, order_nr)]})
            fa_ordheader = db_session.query(Fa_ordheader).filter(
                     (Fa_ordheader.order_nr == order_nr)).with_for_update().first()

            if fa_ordheader:
                fa_ordheader.activeflag = 1
                fa_ordheader.close_by = user_init
                fa_ordheader.close_date = billdate
                fa_ordheader.close_time = get_current_time_in_seconds()


            pass


    def create_ap():

        nonlocal allowclose, art_nr, qty, price, amount, t_amount, fa_op, fa_order, mathis, fa_artikel, queasy, htparam, fa_ordheader, bediener, l_kredit, ap_journal
        nonlocal docu_nr, billdate, user_init, supplier_nr, supp_name, del_note, order_nr


        nonlocal op_list

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
        l_kredit = L_kredit()
        db_session.add(l_kredit)

        l_kredit.name = order_nr
        l_kredit.lief_nr = supplier_nr
        l_kredit.lscheinnr = del_note
        l_kredit.rgdatum = billdate
        l_kredit.datum = None
        l_kredit.saldo =  to_decimal(t_amount)
        l_kredit.ziel = 30
        l_kredit.netto =  to_decimal(t_amount)
        l_kredit.bediener_nr = bediener.nr
        l_kredit.betriebsnr = 2


        ap_journal = Ap_journal()
        db_session.add(ap_journal)

        ap_journal.lief_nr = supplier_nr
        ap_journal.docu_nr = order_nr
        ap_journal.lscheinnr = del_note
        ap_journal.rgdatum = billdate
        ap_journal.saldo =  to_decimal(t_amount)
        ap_journal.netto =  to_decimal(t_amount)
        ap_journal.userinit = bediener.userinit
        ap_journal.zeit = get_current_time_in_seconds()

    t_amount =  to_decimal("0")

    for op_list in query(op_list_data):
        art_nr = op_list.nr
        qty = op_list.anzahl
        price =  to_decimal(op_list.einzelpreis)
        amount =  to_decimal(op_list.warenwert)
        t_amount =  to_decimal(t_amount) + to_decimal(op_list.warenwert)


        create_fa_op()

        # fa_order = get_cache (Fa_order, {"order_nr": [(eq, docu_nr)],"fa_nr": [(eq, op_list.nr)],"fa_pos": [(eq, op_list.counter)]})
        fa_order = db_session.query(Fa_order).filter(
                 (Fa_order.order_nr == docu_nr) & (Fa_order.fa_nr == op_list.nr) & (Fa_order.fa_pos == op_list.counter)).with_for_update().first()

        if fa_order:
            # pass
            fa_order.delivered_qty = fa_order.delivered_qty + qty
            fa_order.delivered_date = billdate
            fa_order.delivered_price =  to_decimal(op_list.einzelpreis)
            fa_order.delivered_amount =  to_decimal(fa_order.delivered_amount) + to_decimal(op_list.warenwert)
            fa_order.last_id = user_init
            # pass
            db_session.refresh(fa_order,with_for_update=True)
    close_po()

    if supplier_nr != 0 and t_amount != 0:
        create_ap()

    return generate_output()
