#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Waehrung, Exrate

def read_exrate_webbl(currencyno:int, from_date:date, to_date:date):

    prepare_cache ([Waehrung, Exrate])

    avg_rate = to_decimal("0.0")
    waehrung_his_list = []
    days:int = 0
    tot_betrag:Decimal = to_decimal("0.0")
    waehrung = exrate = None

    waehrung_his = None

    waehrung_his_list, Waehrung_his = create_model("Waehrung_his", {"waehrungsnr":int, "wabkurz":string, "bezeich":string, "betrag":Decimal, "datum":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avg_rate, waehrung_his_list, days, tot_betrag, waehrung, exrate
        nonlocal currencyno, from_date, to_date


        nonlocal waehrung_his
        nonlocal waehrung_his_list

        return {"avg_rate": avg_rate, "waehrung-his": waehrung_his_list}

    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, currencyno)]})

    if waehrung:

        for exrate in db_session.query(Exrate).filter(
                 (Exrate.artnr == waehrung.waehrungsnr) & (Exrate.datum >= from_date) & (Exrate.datum <= to_date)).order_by(Exrate.datum, Exrate.betrag).all():

            waehrung_his = query(waehrung_his_list, filters=(lambda waehrung_his: waehrung_his.betrag == exrate.betrag), first=True)

            if not waehrung_his:
                waehrung_his = Waehrung_his()
                waehrung_his_list.append(waehrung_his)

                days = days + 1
                tot_betrag =  to_decimal(tot_betrag) + to_decimal(exrate.betrag)
                waehrung_his.waehrungsnr = waehrung.waehrungsnr
                waehrung_his.wabkurz = waehrung.wabkurz
                waehrung_his.bezeich = waehrung.bezeich
                waehrung_his.betrag =  to_decimal(exrate.betrag)
                waehrung_his.datum = exrate.datum


    avg_rate =  to_decimal(tot_betrag) / to_decimal(days)

    return generate_output()