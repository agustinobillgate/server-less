#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel, Waehrung

def get_currencybl(pricetab:bool, rec_id:int, foreign_nr:int, betriebsnr:int, local_nr:int):

    prepare_cache ([Artikel, Waehrung])

    wabkurz = ""
    t_waehrung_data = []
    artikel = waehrung = None

    t_waehrung = art1 = None

    t_waehrung_data, T_waehrung = create_model("T_waehrung", {"wabkurz":string})

    Art1 = create_buffer("Art1",Artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal wabkurz, t_waehrung_data, artikel, waehrung
        nonlocal pricetab, rec_id, foreign_nr, betriebsnr, local_nr
        nonlocal art1


        nonlocal t_waehrung, art1
        nonlocal t_waehrung_data

        return {"wabkurz": wabkurz, "t-waehrung": t_waehrung_data}

    if pricetab:

        art1 = get_cache (Artikel, {"_recid": [(eq, rec_id)]})

        if betriebsnr == 0:
            pass
            art1.betriebsnr = foreign_nr
            pass

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, art1.betriebsnr)]})
        wabkurz = waehrung.wabkurz

        for waehrung in db_session.query(Waehrung).filter(
                     (Waehrung.waehrungsnr != art1.betriebsnr) & (Waehrung.ankauf > 0)).order_by(Waehrung.wabkurz).all():
            t_waehrung = T_waehrung()
            t_waehrung_data.append(t_waehrung)

            t_waehrung.wabkurz = waehrung.wabkurz


    else:

        if betriebsnr != 0:

            art1 = get_cache (Artikel, {"_recid": [(eq, rec_id)]})
            art1.betriebsnr = 0
            pass

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, local_nr)]})
        wabkurz = waehrung.wabkurz

        for waehrung in db_session.query(Waehrung).filter(
                     (Waehrung.waehrungsnr != local_nr) & (Waehrung.ankauf > 0)).order_by(Waehrung.wabkurz).all():
            t_waehrung = T_waehrung()
            t_waehrung_data.append(t_waehrung)

            t_waehrung.wabkurz = waehrung.wabkurz

    return generate_output()