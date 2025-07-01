#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Htparam, Segment, Arrangement, Artikel, Argt_line

def ratecode_admin_check_argt_betragbl(roomrate:Decimal, argt_num:int, tb1char3:string, adult:int, adult_str:string):

    prepare_cache ([Htparam, Arrangement, Artikel, Argt_line])

    error_msg = ""
    argt_betrag:Decimal = to_decimal("0.0")
    bfast_art:int = 0
    lunch_art:int = 0
    dinner_art:int = 0
    lundin_art:int = 0
    next_step:bool = False
    segmbez:string = ""
    loopi:int = 0
    loopqty:int = 0
    htparam = segment = arrangement = artikel = argt_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_msg, argt_betrag, bfast_art, lunch_art, dinner_art, lundin_art, next_step, segmbez, loopi, loopqty, htparam, segment, arrangement, artikel, argt_line
        nonlocal roomrate, argt_num, tb1char3, adult, adult_str

        return {"error_msg": error_msg}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 125)]})
    bfast_art = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 227)]})
    lunch_art = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 228)]})
    dinner_art = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 229)]})
    lundin_art = htparam.finteger

    if matches(tb1char3,r"*;*"):
        segmbez = entry(0, tb1char3, ";")
    else:
        segmbez = tb1char3

    segment = db_session.query(Segment).filter(
             (Segment.bezeich == (segmbez).lower()) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2)) & (not_(matches(Segment.bezeich,("*$$0*"))))).first()

    if segment:

        return generate_output()

    arrangement = get_cache (Arrangement, {"argtnr": [(eq, argt_num)]})

    if not arrangement:
        error_msg = "Arrangement not found."

        return generate_output()

    if matches(adult_str,r"*,*"):
        for loopi in range(1,num_entries(adult_str, ",")  + 1) :
            loopqty = to_int(entry(loopi - 1, adult_str, ","))

            argt_line_obj_list = {}
            argt_line = Argt_line()
            artikel = Artikel()
            for argt_line.betrag, argt_line._recid, artikel.umsatzart, artikel.zwkum, artikel._recid in db_session.query(Argt_line.betrag, Argt_line._recid, Artikel.umsatzart, Artikel.zwkum, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == Argt_line.departement)).filter(
                     (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2) & (Argt_line.kind1)).order_by(Argt_line._recid).all():
                if argt_line_obj_list.get(argt_line._recid):
                    continue
                else:
                    argt_line_obj_list[argt_line._recid] = True

                if argt_line.betrag > 0:
                    argt_betrag =  to_decimal(argt_line.betrag) * to_decimal(loopqty)
                else:
                    argt_betrag =  to_decimal(roomrate) * to_decimal(- to_decimal(argt_line.betrag) / to_decimal(100)) * to_decimal(loopqty)

                if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                    roomrate =  to_decimal(roomrate) - to_decimal(argt_betrag)

                elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                    roomrate =  to_decimal(roomrate) - to_decimal(argt_betrag)

                elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                    roomrate =  to_decimal(roomrate) - to_decimal(argt_betrag)

                elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                    roomrate =  to_decimal(roomrate) - to_decimal(argt_betrag)
                else:
                    roomrate =  to_decimal(roomrate) - to_decimal(argt_betrag)

            if roomrate < 0:
                error_msg = "Breakdown arrangement line and this roomrate is unbalance." + chr_unicode(10) + "Please check again."

                return generate_output()
    else:

        if adult == 0:
            adult = to_int(adult_str)

        argt_line_obj_list = {}
        argt_line = Argt_line()
        artikel = Artikel()
        for argt_line.betrag, argt_line._recid, artikel.umsatzart, artikel.zwkum, artikel._recid in db_session.query(Argt_line.betrag, Argt_line._recid, Artikel.umsatzart, Artikel.zwkum, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == Argt_line.departement)).filter(
                 (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2) & (Argt_line.kind1)).order_by(Argt_line._recid).all():
            if argt_line_obj_list.get(argt_line._recid):
                continue
            else:
                argt_line_obj_list[argt_line._recid] = True

            if argt_line.betrag > 0:
                argt_betrag =  to_decimal(argt_line.betrag) * to_decimal(adult)
            else:
                argt_betrag =  to_decimal(roomrate) * to_decimal(- to_decimal(argt_line.betrag) / to_decimal(100)) * to_decimal(adult)

            if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                roomrate =  to_decimal(roomrate) - to_decimal(argt_betrag)

            elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                roomrate =  to_decimal(roomrate) - to_decimal(argt_betrag)

            elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                roomrate =  to_decimal(roomrate) - to_decimal(argt_betrag)

            elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                roomrate =  to_decimal(roomrate) - to_decimal(argt_betrag)
            else:
                roomrate =  to_decimal(roomrate) - to_decimal(argt_betrag)

        if roomrate < 0:
            error_msg = "Breakdown arrangement line and this roomrate is unbalance." + chr_unicode(10) + "Please check again."

            return generate_output()

    return generate_output()