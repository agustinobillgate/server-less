from functions.additional_functions import *
import decimal
from datetime import date
from models import Exrate, Waehrung

def fo_invoice_calculate_amountbl(transdate:date, a_betriebsnr:int):
    t_exrate_list = []
    t_waehrung_list = []
    exrate = waehrung = None

    t_exrate = t_waehrung = None

    t_exrate_list, T_exrate = create_model_like(Exrate)
    t_waehrung_list, T_waehrung = create_model_like(Waehrung)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_exrate_list, t_waehrung_list, exrate, waehrung


        nonlocal t_exrate, t_waehrung
        nonlocal t_exrate_list, t_waehrung_list
        return {"t-exrate": t_exrate_list, "t-waehrung": t_waehrung_list}


    for exrate in db_session.query(Exrate).filter(
            (Exrate.artnr == a_betriebsnr) &  (Exrate.datum == transdate)).all():
        t_exrate = T_exrate()
        t_exrate_list.append(t_exrate)

        buffer_copy(exrate, t_exrate)

    for waehrung in db_session.query(Waehrung).filter(
            (Waehrungsnr == a_betriebsnr) &  (Waehrung.ankauf != 0)).all():
        t_waehrung = T_waehrung()
        t_waehrung_list.append(t_waehrung)

        buffer_copy(waehrung, t_waehrung)

    return generate_output()