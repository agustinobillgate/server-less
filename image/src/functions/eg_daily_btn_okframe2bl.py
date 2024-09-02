from functions.additional_functions import *
import decimal
from datetime import date
from models import Eg_cost

def eg_daily_btn_okframe2bl(scost:[Scost], blframe:int, a1:date, b1:date, intres:int):
    eg_cost = None

    scost = None

    scost_list, Scost = create_model_like(Eg_cost)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_cost


        nonlocal scost
        nonlocal scost_list
        return {}

    if blframe == 0:

        for eg_cost in db_session.query(Eg_cost).filter(
                (Eg_cost.datum >= a1) &  (Eg_cost.datum <= b1) &  (Eg_cost.resource_nr == intres)).all():
            db_session.delete(eg_cost)

        for scost in query(scost_list):
            eg_cost = Eg_cost()
            db_session.add(eg_cost)

            eg_cost.datum = scost.datum
            eg_cost.resource_nr = scost.resource_nr
            eg_cost.usage = scost.usage
            eg_cost.price = scost.price
            eg_cost.cost = scost.usage * scost.price
            eg_cost.YEAR = get_year(get_current_date())


    else:

        for eg_cost in db_session.query(Eg_cost).filter(
                (Eg_cost.datum >= a1) &  (Eg_cost.datum <= b1) &  (Eg_cost.resource_nr == intres)).all():
            db_session.delete(eg_cost)

        for scost in query(scost_list):
            eg_cost = Eg_cost()
            db_session.add(eg_cost)

            eg_cost.datum = scost.datum
            eg_cost.resource_nr = scost.resource_nr
            eg_cost.usage = scost.usage
            eg_cost.price = scost.price
            eg_cost.cost = scost.usage * scost.price
            eg_cost.YEAR = get_year(get_current_date())

    return generate_output()