from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Katpreis, Arrangement, Htparam, Waehrung

def mk_resline_discounted_ratebl(res_mode:str, r_arrangement:str, r_betriebsnr:int, r_ankunft:date, r_zikatnr:int, r_erwachs:int, r_kind1:int, r_kind2:int, ci_date:date):
    exrate1 = 0
    exrate2 = 0
    t_katpreis_list = []
    datum:date = None
    wd_array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    katpreis = arrangement = htparam = waehrung = None

    t_katpreis = None

    t_katpreis_list, T_katpreis = create_model_like(Katpreis)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal exrate1, exrate2, t_katpreis_list, datum, wd_array, katpreis, arrangement, htparam, waehrung


        nonlocal t_katpreis
        nonlocal t_katpreis_list
        return {"exrate1": exrate1, "exrate2": exrate2, "t-katpreis": t_katpreis_list}

    arrangement = db_session.query(Arrangement).filter(
            (func.lower(Arrangement) == (r_arrangement).lower())).first()

    if not arrangement:

        return generate_output()

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
    datum = r_ankunft

    if res_mode.lower()  == "inhouse":
        datum = ci_date

    katpreis = db_session.query(Katpreis).filter(
            (Katpreis.zikatnr == r_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= datum) &  (Katpreis.endperiode >= datum) &  (Katpreis.betriebsnr == wd_array[get_weekday(datum) - 1])).first()

    if not katpreis:

        katpreis = db_session.query(Katpreis).filter(
                (Katpreis.zikatnr == r_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= datum) &  (Katpreis.endperiode >= datum) &  (Katpreis.betriebsnr == 0)).first()

    if not katpreis:

        return generate_output()
    else:
        t_katpreis = T_katpreis()
        t_katpreis_list.append(t_katpreis)

        buffer_copy(katpreis, t_katpreis)

    return generate_output()