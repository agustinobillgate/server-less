#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Res_line, Arrangement, Argt_line, Artikel, Mealcoup

def mk_mcoupon(resnr:int, zinr:string):

    prepare_cache ([Htparam, Res_line, Arrangement, Argt_line, Artikel, Mealcoup])

    anzahl:int = 0
    eknr:int = 0
    i:int = 0
    depart:date = None
    gname:string = ""
    htparam = res_line = arrangement = argt_line = artikel = mealcoup = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal anzahl, eknr, i, depart, gname, htparam, res_line, arrangement, argt_line, artikel, mealcoup
        nonlocal resnr, zinr

        return {}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 274)]})

    if not htparam.flogical:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 273)]})
    eknr = htparam.finteger

    if eknr == 0:

        return generate_output()
    anzahl = 0

    for res_line in db_session.query(Res_line).filter(
             (Res_line.resnr == resnr) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12)).order_by(Res_line._recid).all():
        depart = res_line.abreise

        if res_line.resstatus == 6:
            gname = res_line.name

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line._recid).all():

            artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})

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