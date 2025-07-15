#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Mc_aclub

def accor_dailyaclubbl(fdate:date, tdate:date):
    aclub_daily_data = []
    nomor:int = 0
    mc_aclub = None

    aclub_daily = None

    aclub_daily_data, Aclub_daily = create_model_like(Mc_aclub, {"count_no":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal aclub_daily_data, nomor, mc_aclub
        nonlocal fdate, tdate


        nonlocal aclub_daily
        nonlocal aclub_daily_data

        return {"aclub-daily": aclub_daily_data}

    for mc_aclub in db_session.query(Mc_aclub).filter(
             (Mc_aclub.billdatum >= fdate) & (Mc_aclub.billdatum <= tdate) & ((Mc_aclub.key == 2) | (Mc_aclub.key == 1))).order_by(Mc_aclub._recid).all():
        aclub_daily = Aclub_daily()
        aclub_daily_data.append(aclub_daily)

        buffer_copy(mc_aclub, aclub_daily)
        nomor = nomor + 1
        aclub_daily.count_no = nomor

    return generate_output()