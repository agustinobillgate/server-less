from functions.additional_functions import *
import decimal
from models import Artikel, Waehrung

def get_currencybl(pricetab:bool, rec_id:int, foreign_nr:int, betriebsnr:int, local_nr:int):
    wabkurz = ""
    t_waehrung_list = []
    artikel = waehrung = None

    t_waehrung = art1 = None

    t_waehrung_list, T_waehrung = create_model("T_waehrung", {"wabkurz":str})

    Art1 = create_buffer("Art1",Artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal wabkurz, t_waehrung_list, artikel, waehrung
        nonlocal pricetab, rec_id, foreign_nr, betriebsnr, local_nr
        nonlocal art1


        nonlocal t_waehrung, art1
        nonlocal t_waehrung_list
        return {"wabkurz": wabkurz, "t-waehrung": t_waehrung_list}

    if pricetab:

        art1 = db_session.query(Art1).filter(
                 (Art1._recid == rec_id)).first()

        if betriebsnr == 0:
            art1.betriebsnr = foreign_nr

        waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.waehrungsnr == art1.betriebsnr)).first()
        wabkurz = waehrung.wabkurz

        for waehrung in db_session.query(Waehrung).filter(
                     (Waehrung.waehrungsnr != art1.betriebsnr) & (Waehrung.ankauf > 0)).order_by(Waehrung.wabkurz).all():
            t_waehrung = T_waehrung()
            t_waehrung_list.append(t_waehrung)

            t_waehrung.wabkurz = waehrung.wabkurz


    else:

        if betriebsnr != 0:

            art1 = db_session.query(Art1).filter(
                     (Art1._recid == rec_id)).first()
            art1.betriebsnr = 0

        waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.waehrungsnr == local_nr)).first()
        wabkurz = waehrung.wabkurz

        for waehrung in db_session.query(Waehrung).filter(
                     (Waehrung.waehrungsnr != local_nr) & (Waehrung.ankauf > 0)).order_by(Waehrung.wabkurz).all():
            t_waehrung = T_waehrung()
            t_waehrung_list.append(t_waehrung)

            t_waehrung.wabkurz = waehrung.wabkurz

    return generate_output()