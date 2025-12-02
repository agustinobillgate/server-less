#using conversion tools version: 1.0.0.117

# ==================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# ==================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fa_artikel, Queasy, Mathis, Htparam, Fa_kateg

def fa_canceldepnbl(datum:date):

    prepare_cache ([Fa_artikel, Htparam, Fa_kateg])

    do_it = False
    last_date:date = None
    depn_value:Decimal = to_decimal("0.0")
    old_book_wert:Decimal = to_decimal("0.0")
    fa_artikel = queasy = mathis = htparam = fa_kateg = None

    fabuff = queasy_buff = None

    Fabuff = create_buffer("Fabuff",Fa_artikel)
    Queasy_buff = create_buffer("Queasy_buff",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, last_date, depn_value, old_book_wert, fa_artikel, queasy, mathis, htparam, fa_kateg
        nonlocal datum
        nonlocal fabuff, queasy_buff


        nonlocal fabuff, queasy_buff

        return {"do_it": do_it}

    def get_depn_value():

        nonlocal do_it, last_date, depn_value, old_book_wert, fa_artikel, queasy, mathis, htparam, fa_kateg
        nonlocal datum
        nonlocal fabuff, queasy_buff


        nonlocal fabuff, queasy_buff

        tot_anz:int = 0
        num:int = 0
        old_book_wert =  to_decimal("0")

        fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

        if fa_kateg.methode == 0:
            old_book_wert =  to_decimal(fa_artikel.warenwert)
            for num in range(1,(fa_artikel.anz_depn - 1)  + 1) :
                tot_anz = fa_kateg.nutzjahr * 12 - (num - 1)
                old_book_wert =  to_decimal(old_book_wert) - (to_decimal(old_book_wert) / to_decimal(tot_anz))

    fa_artikel_obj_list = {}
    for fa_artikel, mathis in db_session.query(Fa_artikel, Mathis).join(Mathis,(Mathis.nr == Fa_artikel.nr)).filter(
             (Fa_artikel.last_depn == datum) & (Fa_artikel.loeschflag == 0)).order_by(Mathis.name).all():
        if fa_artikel_obj_list.get(fa_artikel._recid):
            continue
        else:
            fa_artikel_obj_list[fa_artikel._recid] = True


        last_date = date_mdy(get_month(datum) , 1, get_year(datum)) - timedelta(days=1)
        depn_value =  to_decimal("0")

        if fa_artikel.anz_depn >= 1:
            get_depn_value()

        if old_book_wert != 0:
            do_it = True

            fabuff = get_cache (Fa_artikel, {"_recid": [(eq, fa_artikel._recid)]})

            if fa_artikel.anz_depn == 1:
                fabuff.anz_depn = 0
                fabuff.depn_wert =  to_decimal("0")
                fabuff.next_depn = datum
                fabuff.last_depn = None
                fabuff.book_wert =  to_decimal(fabuff.warenwert)


            else:
                fabuff.depn_wert =  to_decimal(fabuff.warenwert) - to_decimal(old_book_wert)
                fabuff.book_wert =  to_decimal(old_book_wert)
                fabuff.anz_depn = fabuff.anz_depn - 1
                fabuff.last_depn = last_date
                fabuff.next_depn = datum

            if fabuff.first_depn == datum:
                fabuff.first_depn = None
            pass

    if do_it:

        # htparam = get_cache (Htparam, {"paramnr": [(eq, 881)]})
        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 881)).with_for_update().first()
        htparam.fdate = last_date
        db_session.refresh(htparam,with_for_update=True)

        # pass

        queasy = get_cache (Queasy, {"key": [(eq, 348)],"date1": [(eq, datum)]})

        if queasy:

            for queasy_buff in db_session.query(Queasy_buff).filter(
                     (Queasy_buff.key == 348) & (Queasy_buff.date1 == datum)).order_by(Queasy_buff._recid).all():
                db_session.delete(queasy_buff)

    return generate_output()
