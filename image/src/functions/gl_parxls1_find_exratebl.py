from functions.additional_functions import *
import decimal
from datetime import date
from models import Exrate, Htparam, Waehrung

def gl_parxls1_find_exratebl(curr_date:date, foreign_flag:bool):
    exrate_betrag = 0
    frate = 0
    exrate = htparam = waehrung = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal exrate_betrag, frate, exrate, htparam, waehrung


        return {"exrate_betrag": exrate_betrag, "frate": frate}

    def find_exrate():

        nonlocal exrate_betrag, frate, exrate, htparam, waehrung

        foreign_nr:int = 0

        if foreign_flag:

            exrate = db_session.query(Exrate).filter(
                    (Exrate.artnr == 99999) &  (Exrate.datum == curr_date)).first()

            if exrate:

                return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        if htparam.fchar != "":

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrung.wabkurz == htparam.fchar)).first()

            if waehrung:
                foreign_nr = waehrungsnr

        if foreign_nr != 0:

            exrate = db_session.query(Exrate).filter(
                    (Exrate.artnr == foreign_nr) &  (Exrate.datum == curr_date)).first()
        else:

            exrate = db_session.query(Exrate).filter(
                    (Exrate.datum == curr_date)).first()

        if exrate:
            exrate_betrag = exrate.betrag

    find_exrate()

    if exrate:
        frate = exrate.betrag

    return generate_output()