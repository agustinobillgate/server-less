#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Exrate, Waehrung

def fo_invoice_calculate_amountbl(transdate:date, a_betriebsnr:int):
    t_exrate_data = []
    t_waehrung_data = []
    exrate = waehrung = None

    t_exrate = t_waehrung = None

    t_exrate_data, T_exrate = create_model_like(Exrate)
    t_waehrung_data, T_waehrung = create_model_like(Waehrung)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_exrate_data, t_waehrung_data, exrate, waehrung
        nonlocal transdate, a_betriebsnr


        nonlocal t_exrate, t_waehrung
        nonlocal t_exrate_data, t_waehrung_data

        return {"t-exrate": t_exrate_data, "t-waehrung": t_waehrung_data}


    for exrate in db_session.query(Exrate).filter(
             (Exrate.artnr == a_betriebsnr) & (Exrate.datum == transdate)).order_by(Exrate._recid).all():
        t_exrate = T_exrate()
        t_exrate_data.append(t_exrate)

        buffer_copy(exrate, t_exrate)

    for waehrung in db_session.query(Waehrung).filter(
             (Waehrung.waehrungsnr == a_betriebsnr) & (Waehrung.ankauf != 0)).order_by(Waehrung._recid).all():
        t_waehrung = T_waehrung()
        t_waehrung_data.append(t_waehrung)

        buffer_copy(waehrung, t_waehrung)

    return generate_output()