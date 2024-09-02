from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Res_line, Arrangement, Argt_line, Artikel, Mealcoup

def mk_mcoupon(resnr:int, zinr:str):
    anzahl:int = 0
    eknr:int = 0
    i:int = 0
    depart:date = None
    gname:str = ""
    htparam = res_line = arrangement = argt_line = artikel = mealcoup = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal anzahl, eknr, i, depart, gname, htparam, res_line, arrangement, argt_line, artikel, mealcoup


        return {}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 274)).first()

    if not htparam.flogical:

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 273)).first()
    eknr = finteger

    if eknr == 0:

        return generate_output()
    anzahl = 0

    for res_line in db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.resstatus != 8) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12)).all():
        depart = res_line.abreise

        if res_line.resstatus == 6:
            gname = res_line.name

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement == res_line.arrangement)).first()

        for argt_line in db_session.query(Argt_line).filter(
                (Argt_line.argtnr == arrangement.argtnr)).all():

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == argt_line.argt_artnr) &  (Artikel.departement == argt_line.departement)).first()

            if artikel and artikel.endkum == eknr:
                anzahl = anzahl + (res_line.erwachs + res_line.kind1 + res_line.gratis) * (res_line.abreise - res_line.ankunft)

    if anzahl > 0:
        mealcoup = Mealcoup()
        db_session.add(mealcoup)

        mealcoup.resnr = resnr
        mealcoup.zinr = zinr
        mealcoup.name = gname
        mealcoup.anzahl = anzahl
        mealcoup.abreise = depart

    return generate_output()