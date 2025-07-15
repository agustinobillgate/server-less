#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Mathis

t_mathis_data, T_mathis = create_model_like(Mathis, {"remain_budget":Decimal, "init_budget":Decimal})

def fa_mkpo_check_mathis_webbl(art_nr:int, order_date:date, t_mathis_data:[T_mathis]):
    avail_mathis = True
    mtd_budget:Decimal = to_decimal("0.0")
    mtd_balance:Decimal = to_decimal("0.0")
    t_warenwert:Decimal = to_decimal("0.0")
    remain_budget:Decimal = to_decimal("0.0")
    grup_nr:Decimal = to_decimal("0.0")
    mathis = None

    t_mathis = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_mathis, mtd_budget, mtd_balance, t_warenwert, remain_budget, grup_nr, mathis
        nonlocal art_nr, order_date


        nonlocal t_mathis

        return {"avail_mathis": avail_mathis, "t-mathis": t_mathis_data}

    mathis = get_cache (Mathis, {"nr": [(eq, art_nr)]})

    if not mathis:
        avail_mathis = False

    for mathis in db_session.query(Mathis).filter(
             (Mathis.nr == art_nr)).order_by(Mathis._recid).all():
        t_mathis = T_mathis()
        t_mathis_data.append(t_mathis)

        buffer_copy(mathis, t_mathis)

    return generate_output()