from functions.additional_functions import *
import decimal
from datetime import date
from models import Fa_artikel, Mathis, Htparam, Fa_kateg

def fa_canceldepnbl(datum:date):
    do_it = False
    last_date:date = None
    depn_value:decimal = 0
    old_book_wert:decimal = 0
    fa_artikel = mathis = htparam = fa_kateg = None

    fabuff = None

    Fabuff = Fa_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, last_date, depn_value, old_book_wert, fa_artikel, mathis, htparam, fa_kateg
        nonlocal fabuff


        nonlocal fabuff
        return {"do_it": do_it}

    def get_depn_value():

        nonlocal do_it, last_date, depn_value, old_book_wert, fa_artikel, mathis, htparam, fa_kateg
        nonlocal fabuff


        nonlocal fabuff

        tot_anz:int = 0
        num:int = 0
        old_book_wert = 0

        fa_kateg = db_session.query(Fa_kateg).filter(
                (Fa_kateg.katnr == fa_artikel.katnr)).first()

        if fa_kateg.methode == 0:
            old_book_wert = fa_artikel.warenwert
            for num in range(1,(fa_artikel.anz_depn - 1)  + 1) :
                tot_anz = fa_kateg.nutzjahr * 12 - (num - 1)
                old_book_wert = old_book_wert - (old_book_wert / tot_anz)


    fa_artikel_obj_list = []
    for fa_artikel, mathis in db_session.query(Fa_artikel, Mathis).join(Mathis,(Mathis.nr == Fa_artikel.nr)).filter(
            (Fa_artikel.last_depn == datum) &  (Fa_artikel.loeschflag == 0)).all():
        if fa_artikel._recid in fa_artikel_obj_list:
            continue
        else:
            fa_artikel_obj_list.append(fa_artikel._recid)


        last_date = date_mdy(get_month(datum) , 1, get_year(datum)) - 1
        depn_value = 0

        if fa_artikel.anz_depn >= 1:
            get_depn_value()

        if old_book_wert != 0:
            do_it = True

            fabuff = db_session.query(Fabuff).filter(
                    (Fabuff._recid == fa_artikel._recid)).first()

            if fa_artikel.anz_depn == 1:
                fabuff.anz_depn = 0
                fabuff.depn_wert = 0
                fabuff.next_depn = datum
                fabuff.last_depn = None
                fabuff.book_wert = fabuff.warenwert


            else:
                fabuff.depn_wert = fabuff.warenwert - old_book_wert
                fabuff.book_wert = old_book_wert
                fabuff.anz_depn = fabuff.anz_depn - 1
                fabuff.last_depn = last_date
                fabuff.next_depn = datum

            if fabuff.first_depn == datum:
                fabuff.first_depn = None

            fabuff = db_session.query(Fabuff).first()

    if do_it:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 881)).first()
        htparam.fdate = last_date

        htparam = db_session.query(Htparam).first()

    return generate_output()