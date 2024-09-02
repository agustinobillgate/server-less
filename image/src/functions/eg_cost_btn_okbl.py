from functions.additional_functions import *
import decimal
from datetime import date
from models import Eg_cost

def eg_cost_btn_okbl(case_type:int, scost:[Scost], blframe:int, fdate1:date, tdate1:date, intres:int, intres4:int, fyear1:int, rmonth:int, fusage:int, fprice:decimal, fval:decimal):
    eg_cost = None

    scost = None

    scost_list, Scost = create_model_like(Eg_cost, {"strmonth":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_cost


        nonlocal scost
        nonlocal scost_list
        return {}

    if case_type == 1:

        if blframe == 0:

            for eg_cost in db_session.query(Eg_cost).filter(
                    (Eg_cost.datum >= fdate1) &  (Eg_cost.datum <= tdate1) &  (Eg_cost.resource_nr == intres)).all():
                db_session.delete(eg_cost)

            for scost in query(scost_list):
                eg_cost = Eg_cost()
                db_session.add(eg_cost)

                eg_cost.datum = scost.datum
                eg_cost.resource_nr = scost.resource_nr
                eg_cost.usage = scost.usage
                eg_cost.price = scost.price
                eg_cost.cost = scost.usage * scost.price


        else:

            for eg_cost in db_session.query(Eg_cost).filter(
                    (Eg_cost.datum >= fdate1) &  (Eg_cost.datum <= tdate1) &  (Eg_cost.resource_nr == intres4)).all():
                db_session.delete(eg_cost)

            for scost in query(scost_list):
                eg_cost = Eg_cost()
                db_session.add(eg_cost)

                eg_cost.datum = scost.datum
                eg_cost.resource_nr = scost.resource_nr
                eg_cost.usage = scost.usage
                eg_cost.price = scost.price
                eg_cost.cost = scost.usage * scost.price

    if case_type == 2:

        eg_cost = db_session.query(Eg_cost).filter(
                (Eg_cost.YEAR == fyear1) &  (Eg_cost.MONTH == rmonth) &  (Eg_cost.resource_nr == intres4)).first()

        if eg_cost:
            eg_cost.YEAR = fyear1
            eg_cost.MONTH = rmonth
            eg_cost.resource_nr = intres4
            eg_cost.usage = fusage
            eg_cost.price = fprice
            eg_cost.cost = fval


        else:
            eg_cost = Eg_cost()
            db_session.add(eg_cost)

            eg_cost.YEAR = fyear1
            eg_cost.MONTH = rmonth
            eg_cost.resource_nr = intres4
            eg_cost.usage = fusage
            eg_cost.price = fprice
            eg_cost.cost = fval

    return generate_output()