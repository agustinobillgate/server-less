from functions.additional_functions import *
import decimal
from datetime import date
from models import Exrate, Htparam, Waehrung

def gl_parxls1_find_exratebl(curr_date:date, foreign_flag:bool):
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

            exrate = db_session.query(Exrate).filter(
                     (Exrate.artnr == 99999) & (Exrate.datum == curr_date)).first()

            if exrate:

                return

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 144)).first()

        if htparam.fchar != "":

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.wabkurz == htparam.fchar)).first()

            if waehrung:
                foreign_nr = waehrung.waehrungsnr

        if foreign_nr != 0:

            exrate = db_session.query(Exrate).filter(
                     (Exrate.artnr == foreign_nr) & (Exrate.datum == curr_date)).first()
        else:

            exrate = db_session.query(Exrate).filter(
                     (Exrate.datum == curr_date)).first()

        if exrate:
            exrate_betrag =  to_decimal(exrate.betrag)


    find_exrate()

    if exrate:
        frate =  to_decimal(exrate.betrag)

    return generate_output()