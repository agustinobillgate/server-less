#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_cost

scost_data, Scost = create_model_like(Eg_cost, {"strmonth":string})

def eg_cost_btn_okbl(case_type:int, scost_data:[Scost], blframe:int, fdate1:date, tdate1:date, intres:int, intres4:int, fyear1:int, rmonth:int, fusage:int, fprice:Decimal, fval:Decimal):
    eg_cost = None

    scost = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_cost
        nonlocal case_type, blframe, fdate1, tdate1, intres, intres4, fyear1, rmonth, fusage, fprice, fval


        nonlocal scost

        return {}

    if case_type == 1:

        if blframe == 0:

            for eg_cost in db_session.query(Eg_cost).filter(
                     (Eg_cost.datum >= fdate1) & (Eg_cost.datum <= tdate1) & (Eg_cost.resource_nr == intres)).with_for_update().order_by(Eg_cost._recid).all():
                db_session.delete(eg_cost)

            for scost in query(scost_data):
                eg_cost = Eg_cost()
                db_session.add(eg_cost)

                eg_cost.datum = scost.datum
                eg_cost.resource_nr = scost.resource_nr
                eg_cost.usage = scost.usage
                eg_cost.price =  to_decimal(scost.price)
                eg_cost.cost =  to_decimal(scost.usage) * to_decimal(scost.price)


        else:

            for eg_cost in db_session.query(Eg_cost).filter(
                     (Eg_cost.datum >= fdate1) & (Eg_cost.datum <= tdate1) & (Eg_cost.resource_nr == intres4)).with_for_update().order_by(Eg_cost._recid).all():
                db_session.delete(eg_cost)

            for scost in query(scost_data):
                eg_cost = Eg_cost()
                db_session.add(eg_cost)

                eg_cost.datum = scost.datum
                eg_cost.resource_nr = scost.resource_nr
                eg_cost.usage = scost.usage
                eg_cost.price =  to_decimal(scost.price)
                eg_cost.cost =  to_decimal(scost.usage) * to_decimal(scost.price)

    if case_type == 2:

        eg_cost = get_cache (Eg_cost, {"year": [(eq, fyear1)],"month": [(eq, rmonth)],"resource_nr": [(eq, intres4)]})

        if eg_cost:
            eg_cost.year = fyear1
            eg_cost.month = rmonth
            eg_cost.resource_nr = intres4
            eg_cost.usage = fusage
            eg_cost.price =  to_decimal(fprice)
            eg_cost.cost =  to_decimal(fval)


        else:
            eg_cost = Eg_cost()
            db_session.add(eg_cost)

            eg_cost.year = fyear1
            eg_cost.month = rmonth
            eg_cost.resource_nr = intres4
            eg_cost.usage = fusage
            eg_cost.price =  to_decimal(fprice)
            eg_cost.cost =  to_decimal(fval)

    return generate_output()