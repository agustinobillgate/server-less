#using conversion tools version: 1.0.0.118

#------------------------------------------
# Rulita, 25/08/2025
# Issue : Req nput param from UI beda dgn BL
# Recompile
#------------------------------------------


from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Mc_aclub

def accor_dailyaclubbl(curr_date:date):
    aclub_daily_data = []
    mc_aclub = None

    aclub_daily = None

    aclub_daily_data, Aclub_daily = create_model("Aclub_daily", {"key":int, "cardnum":string, "sysdate":date, "zeit":int, "billdatum":date, "billtype":int, "rechnr":int, "artnr":int, "departement":int, "betrag":Decimal, "nettobetrag":Decimal, "incl_flag":int, "bemerk":string, "resnr":int, "reslinnr":int, "vat":Decimal, "service":Decimal, "num1":int, "num2":int, "num3":int, "num4":int, "num5":int, "deci1":Decimal, "deci2":Decimal, "deci3":Decimal, "deci4":Decimal, "deci5":Decimal, "logi1":bool, "logi2":bool, "logi3":bool, "char1":string, "char2":string, "char3":string, "char4":string, "char5":string, "date1":date, "date2":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal aclub_daily_data, mc_aclub
        nonlocal curr_date


        nonlocal aclub_daily
        nonlocal aclub_daily_data

        return {"aclub-daily": aclub_daily_data}

    for mc_aclub in db_session.query(Mc_aclub).filter(
             (Mc_aclub.billdatum == curr_date)).order_by(Mc_aclub._recid).all():
        aclub_daily = Aclub_daily()
        aclub_daily_data.append(aclub_daily)

        buffer_copy(mc_aclub, aclub_daily)

    return generate_output()