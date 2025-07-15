#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Exrate, Htparam, Waehrung

def gl_parxls1_find_exratebl(curr_date:date, foreign_flag:bool):

    prepare_cache ([Exrate, Htparam, Waehrung])

    exrate_betrag = to_decimal("0.0")
    frate = to_decimal("0.0")
    exrate = htparam = waehrung = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal exrate_betrag, frate, exrate, htparam, waehrung
        nonlocal curr_date, foreign_flag

        return {"exrate_betrag": exrate_betrag, "frate": frate}

    def find_exrate():

        nonlocal exrate_betrag, frate, exrate, htparam, waehrung
        nonlocal curr_date, foreign_flag

        foreign_nr:int = 0

        if foreign_flag:

            exrate = get_cache (Exrate, {"artnr": [(eq, 99999)],"datum": [(eq, curr_date)]})

            if exrate:

                return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        if htparam.fchar != "":

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

            if waehrung:
                foreign_nr = waehrung.waehrungsnr

        if foreign_nr != 0:

            exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, curr_date)]})
        else:

            exrate = get_cache (Exrate, {"datum": [(eq, curr_date)]})

        if exrate:
            exrate_betrag =  to_decimal(exrate.betrag)


    find_exrate()

    if exrate:
        frate =  to_decimal(exrate.betrag)

    return generate_output()