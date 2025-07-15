#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Waehrung

def read_waehrungbl(case_type:int, currencyno:int, currbez:string):
    t_waehrung_data = []
    waehrung = None

    t_waehrung = None

    t_waehrung_data, T_waehrung = create_model_like(Waehrung)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_waehrung_data, waehrung
        nonlocal case_type, currencyno, currbez


        nonlocal t_waehrung
        nonlocal t_waehrung_data

        return {"t-waehrung": t_waehrung_data}

    if case_type == 1:

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, currencyno)]})

        if waehrung:
            t_waehrung = T_waehrung()
            t_waehrung_data.append(t_waehrung)

            buffer_copy(waehrung, t_waehrung)
    elif case_type == 2:

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, currbez)]})

        if waehrung:
            t_waehrung = T_waehrung()
            t_waehrung_data.append(t_waehrung)

            buffer_copy(waehrung, t_waehrung)
    elif case_type == 3:

        for waehrung in db_session.query(Waehrung).filter(
                 (Waehrung.betriebsnr == 0)).order_by(Waehrung.bezeich).all():
            t_waehrung = T_waehrung()
            t_waehrung_data.append(t_waehrung)

            buffer_copy(waehrung, t_waehrung)

    elif case_type == 4:

        waehrung = get_cache (Waehrung, {"bezeich": [(eq, currbez)]})

        if waehrung:
            t_waehrung = T_waehrung()
            t_waehrung_data.append(t_waehrung)

            buffer_copy(waehrung, t_waehrung)
    elif case_type == 5:

        for waehrung in db_session.query(Waehrung).filter(
                 (Waehrung.waehrungsnr != currencyno) & (Waehrung.betriebsnr == 0)).order_by(Waehrung.bezeich).all():
            t_waehrung = T_waehrung()
            t_waehrung_data.append(t_waehrung)

            buffer_copy(waehrung, t_waehrung)
    elif case_type == 6:

        for waehrung in db_session.query(Waehrung).filter(
                 (Waehrung.betriebsnr == 0) & (Waehrung.ankauf > 0) & (Waehrung.wabkurz != currbez)).order_by(Waehrung.bezeich).all():
            t_waehrung = T_waehrung()
            t_waehrung_data.append(t_waehrung)

            buffer_copy(waehrung, t_waehrung)
    elif case_type == 7:

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, currencyno)],"ankauf": [(ne, 0)]})

        if waehrung:
            t_waehrung = T_waehrung()
            t_waehrung_data.append(t_waehrung)

            buffer_copy(waehrung, t_waehrung)
    elif case_type == 8:

        for waehrung in db_session.query(Waehrung).order_by(Waehrung._recid).all():
            t_waehrung = T_waehrung()
            t_waehrung_data.append(t_waehrung)

            buffer_copy(waehrung, t_waehrung)

    elif case_type == 9:

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(ne, currencyno)],"wabkurz": [(eq, currbez)]})

        if waehrung:
            t_waehrung = T_waehrung()
            t_waehrung_data.append(t_waehrung)

            buffer_copy(waehrung, t_waehrung)

    return generate_output()