#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_cost

scost_data, Scost = create_model_like(Eg_cost)

def eg_daily_btn_okframe2bl(scost_data:[Scost], blframe:int, a1:date, b1:date, intres:int):
    eg_cost = None

    scost = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_cost
        nonlocal blframe, a1, b1, intres


        nonlocal scost

        return {}

    if blframe == 0:

        for eg_cost in db_session.query(Eg_cost).filter(
                 (Eg_cost.datum >= a1) & (Eg_cost.datum <= b1) & (Eg_cost.resource_nr == intres)).with_for_update().order_by(Eg_cost._recid).all():
            db_session.delete(eg_cost)

        for scost in query(scost_data):
            eg_cost = Eg_cost()
            db_session.add(eg_cost)

            eg_cost.datum = scost.datum
            eg_cost.resource_nr = scost.resource_nr
            eg_cost.usage = scost.usage
            eg_cost.price =  to_decimal(scost.price)
            eg_cost.cost =  to_decimal(scost.usage) * to_decimal(scost.price)
            eg_cost.year = get_year(get_current_date())


    else:

        for eg_cost in db_session.query(Eg_cost).filter(
                 (Eg_cost.datum >= a1) & (Eg_cost.datum <= b1) & (Eg_cost.resource_nr == intres)).with_for_update().order_by(Eg_cost._recid).all():
            db_session.delete(eg_cost)

        for scost in query(scost_data):
            eg_cost = Eg_cost()
            db_session.add(eg_cost)

            eg_cost.datum = scost.datum
            eg_cost.resource_nr = scost.resource_nr
            eg_cost.usage = scost.usage
            eg_cost.price =  to_decimal(scost.price)
            eg_cost.cost =  to_decimal(scost.usage) * to_decimal(scost.price)
            eg_cost.year = get_year(get_current_date())

    return generate_output()