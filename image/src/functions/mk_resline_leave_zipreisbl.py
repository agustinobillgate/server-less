from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Arrangement, Waehrung, Katpreis

def mk_resline_leave_zipreisbl(from_date:date, to_date:date, r_arrangement:str, r_betriebsnr:int, local_nr:int, price_decimal:int, rmcat:int):
    wrong_price = False
    exrate1 = 0
    exrate2 = 0
    t_list_list = []
    datum:date = None
    tol_value:decimal = 0
    wd_array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    htparam = arrangement = waehrung = katpreis = None

    t_list = htp1 = None

    t_list_list, T_list = create_model("T_list", {"datum":date, "avail_katpreis":bool})

    Htp1 = Htparam

    db_session = local_storage.db_session

    def generate_output():
        nonlocal wrong_price, exrate1, exrate2, t_list_list, datum, tol_value, wd_array, htparam, arrangement, waehrung, katpreis
        nonlocal htp1


        nonlocal t_list, htp1
        nonlocal t_list_list
        return {"wrong_price": wrong_price, "exrate1": exrate1, "exrate2": exrate2, "t-list": t_list_list}

    arrangement = db_session.query(Arrangement).filter(
            (func.lower(Arrangement) == (r_arrangement).lower())).first()

    if not arrangement:
        wrong_price = True

        return generate_output()

    htp1 = db_session.query(Htp1).filter(
            (Htp1.paramnr == 145)).first()

    if r_betriebsnr == local_nr and (price_decimal == 0):
        tol_value = htp1.finteger * 10

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if waehrung:
        exrate1 = waehrung.ankauf / waehrung.einheit

    waehrung = db_session.query(Waehrung).filter(
            (Waehrungsnr == r_betriebsnr)).first()

    if waehrung:
        exrate2 = waehrung.ankauf / waehrung.einheit
    for datum in range(from_date,to_date + 1) :

        katpreis = db_session.query(Katpreis).filter(
                (Katpreis.zikatnr == rmcat) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= datum) &  (Katpreis.endperiode >= datum) &  (Katpreis.betriebsnr == wd_array[get_weekday(datum) - 1])).first()

        if not katpreis:

            katpreis = db_session.query(Katpreis).filter(
                    (Katpreis.zikatnr == rmcat) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= datum) &  (Katpreis.endperiode >= datum) &  (Katpreis.betriebsnr == 0)).first()
        t_list = T_list()
        t_list_list.append(t_list)

        t_list.datum = datum
        t_list.avail_katpreis = None != katpreis

    return generate_output()