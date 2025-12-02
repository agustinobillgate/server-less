#using conversion tools version: 1.0.0.117
#----------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#----------------------------------------

# ==================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# ==================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Mathis, Fa_artikel, Htparam, Fa_op, Counters
from functions.next_counter_for_update import next_counter_for_update

def fa_move_move_itbl(location_str:string, qty:int, user_init:string, artnr:int):

    prepare_cache ([Mathis, Fa_artikel, Htparam, Fa_op, Counters])

    anz1 = 0
    anz2 = 0
    mathis = fa_artikel = htparam = fa_op = counters = None

    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""
    location_str = location_str.strip()

    def generate_output():
        nonlocal anz1, anz2, mathis, fa_artikel, htparam, fa_op, counters
        nonlocal location_str, qty, user_init, artnr

        return {"anz1": anz1, "anz2": anz2}

    def move_it():

        nonlocal anz1, anz2, mathis, fa_artikel, htparam, fa_op, counters
        nonlocal location_str, qty, user_init, artnr

        fabuff = None
        mabuff = None
        found:bool = False
        billdate:date = None
        Fabuff =  create_buffer("Fabuff",Fa_artikel)
        Mabuff =  create_buffer("Mabuff",Mathis)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})

        if htparam:
            billdate = htparam.fdate

        for mabuff in db_session.query(Mabuff).filter(
                 (Mabuff.name == mathis.name) & (Mabuff.location != mathis.location) & (Mabuff.asset == mathis.asset) & (Mabuff.location == (location_str).lower())).order_by(Mabuff._recid).yield_per(100):

            fabuff = get_cache (Fa_artikel, {"nr": [(eq, mabuff.nr)]})

            if fabuff.katnr == fa_artikel.katnr and fabuff.gnr == fa_artikel.gnr and fabuff.subgrp == fa_artikel.subgrp and fabuff.anz_depn == fa_artikel.anz_dep and fabuff.loeschflag == 0 and fabuff._recid != fa_artikel._recid:
                found = True
                break

        if found:
            fa_op = Fa_op()
            db_session.add(fa_op)

            fa_op.nr = mathis.nr
            fa_op.opart = 2
            fa_op.datum = billdate
            fa_op.zeit = get_current_time_in_seconds()
            fa_op.anzahl = qty
            fa_op.einzelpreis =  to_decimal(fa_artikel.book_wert) / to_decimal(fa_artikel.anzahl)
            fa_op.warenwert =  to_decimal(fa_op.einzelpreis) * to_decimal(qty)
            fa_op.id = user_init
            fa_op.docu_nr = mathis.name + ";;" +\
                    mathis.location + ";;" +\
                    location_str + ";;" +\
                    "YES" + ";;" +\
                    to_string(get_year(get_current_date())) + to_string(get_month(get_current_date()) , "99") +\
                    to_string(get_day(get_current_date()) , "99") + ";;"


            pass
            pass
            pass
            pass

            if fa_artikel.anzahl == qty:
                fabuff.warenwert =  to_decimal(fabuff.warenwert) + to_decimal(fa_artikel.warenwert)
                fabuff.book_wert =  to_decimal(fabuff.book_wert) + to_decimal(fa_artikel.book_wert)
                fabuff.depn_wert =  to_decimal(fabuff.depn_wert) + to_decimal(fa_artikel.depn_wert)
                fabuff.anzahl = fabuff.anzahl + qty
                fabuff.anz100 = fabuff.anzahl + qty
                fabuff.cid = user_init
                fabuff.changed = get_current_date()
                fa_artikel.loeschflag = 1
                fa_artikel.deleted = get_current_date()


            else:
                fabuff.warenwert =  to_decimal(fabuff.warenwert) +\
                        fa_artikel.warenwert * to_decimal(qty) / to_decimal(fa_artikel.anzahl)
                fabuff.book_wert =  to_decimal(fabuff.book_wert) +\
                        fa_artikel.book_wert * to_decimal(qty) / to_decimal(fa_artikel.anzahl)
                fabuff.depn_wert =  to_decimal(fabuff.depn_wert) +\
                        fa_artikel.depn_wert * to_decimal(qty) / to_decimal(fa_artikel.anzahl)
                fabuff.anzahl = fabuff.anzahl + qty
                fabuff.anz100 = fabuff.anzahl + qty


                fa_artikel.warenwert =  to_decimal(fa_artikel.warenwert) *\
                        (1 - to_decimal(qty) / to_decimal(fa_artikel.anzahl) )
                fa_artikel.book_wert =  to_decimal(fa_artikel.book_wert) *\
                        (1 - to_decimal(qty) / to_decimal(fa_artikel.anzahl) )
                fa_artikel.depn_wert =  to_decimal(fa_artikel.depn_wert) *\
                        (1 - to_decimal(qty) / to_decimal(fa_artikel.anzahl) )
                fa_artikel.anzahl = fa_artikel.anzahl - qty
                fa_artikel.anz100 = fa_artikel.anzahl - qty


                pass
            anz1 = 11
            anz2 = 22


        else:
            fa_op = Fa_op()
            db_session.add(fa_op)

            fa_op.nr = mathis.nr
            fa_op.opart = 2
            fa_op.datum = billdate
            fa_op.zeit = get_current_time_in_seconds()
            fa_op.anzahl = qty
            fa_op.einzelpreis =  to_decimal(fa_artikel.book_wert) / to_decimal(fa_artikel.anzahl)
            fa_op.warenwert =  to_decimal(fa_op.einzelpreis) * to_decimal(qty)
            fa_op.id = user_init
            fa_op.docu_nr = mathis.name + ";;" +\
                    mathis.location + ";;" +\
                    location_str + ";;" +\
                    "NO" + ";;" +\
                    to_string(get_year(get_current_date())) + to_string(get_month(get_current_date()) , "99") +\
                    to_string(get_day(get_current_date()) , "99") + ";;"


            pass
            pass

            if fa_artikel.anzahl == qty:
                # pass
                mathis.location = location_str
                db_session.refresh(mathis,with_for_update=True)
                # pass
            else:

                # counters = get_cache (Counters, {"counter_no": [(eq, 17)]})
                counters = db_session.query(Counters).filter(Counters.counter_no == 17).with_for_update().first()
                counters.counter = counters.counter + 1
                mabuff = Mathis()
                db_session.add(mabuff)

                buffer_copy(mathis, mabuff,except_fields=["mathis.nr"])
                mabuff.nr = counters.counter


                mabuff.location = location_str


                pass
                fabuff = Fa_artikel()
                db_session.add(fabuff)

                buffer_copy(fa_artikel, fabuff,except_fields=["fa_artikel.nr"])
                # fabuff.nr = counters.counter
                fabuff.nr = last_count
                
                fabuff.anzahl = qty
                fabuff.anz100 = qty
                fabuff.warenwert =  to_decimal(fa_artikel.warenwert) * to_decimal(qty) / to_decimal(fa_artikel.anzahl)
                fabuff.book_wert =  to_decimal(fa_artikel.book_wert) * to_decimal(qty) / to_decimal(fa_artikel.anzahl)
                fabuff.depn_wert =  to_decimal(fa_artikel.depn_wert) * to_decimal(qty) / to_decimal(fa_artikel.anzahl)


                pass
                pass
                fa_artikel.warenwert =  to_decimal(fa_artikel.warenwert) *\
                        (1 - to_decimal(qty) / to_decimal(fa_artikel.anzahl) )
                fa_artikel.book_wert =  to_decimal(fa_artikel.book_wert) *\
                        (1 - to_decimal(qty) / to_decimal(fa_artikel.anzahl) )
                fa_artikel.depn_wert =  to_decimal(fa_artikel.depn_wert) *\
                        (1 - to_decimal(qty) / to_decimal(fa_artikel.anzahl) )
                fa_artikel.anzahl = fa_artikel.anzahl - qty
                fa_artikel.anz100 = fa_artikel.anzahl - qty
                fa_artikel.cid = user_init
                fa_artikel.changed = get_current_date()


                # pass
                db_session.refresh(fa_artikel,with_for_update=True)

#     mathis = get_cache (Mathis, {"nr": [(eq, artnr)]})
        mathis = db_session.query(Mathis).filter(Mathis.nr == artnr).with_for_update().first()

    if mathis:

        # fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, artnr)]})
        fa_artikel = db_session.query(Fa_artikel).filter(Fa_artikel.nr == artnr).with_for_update().first()

        if fa_artikel:
            move_it()

    return generate_output()