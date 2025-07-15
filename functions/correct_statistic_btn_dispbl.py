#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Artikel, Billjournal, Segmentstat, Genstat

def correct_statistic_btn_dispbl(lodg_artnr:int, date1:date):

    prepare_cache ([Billjournal, Segmentstat, Genstat])

    flag = 0
    slist_data = []
    vat:Decimal = to_decimal("0.0")
    service:Decimal = to_decimal("0.0")
    d:Decimal = to_decimal("0.0")
    artikel = billjournal = segmentstat = genstat = None

    slist = None

    slist_data, Slist = create_model("Slist", {"bjournal":Decimal, "genstat":Decimal, "paxgenstat":int, "segmstat":Decimal, "paxsegm":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, slist_data, vat, service, d, artikel, billjournal, segmentstat, genstat
        nonlocal lodg_artnr, date1


        nonlocal slist
        nonlocal slist_data

        return {"flag": flag, "slist": slist_data}

    artikel = get_cache (Artikel, {"artnr": [(eq, lodg_artnr)],"departement": [(eq, 0)]})

    if not artikel:
        flag = 1

        return generate_output()
    else:
        service =  to_decimal("0")
        vat =  to_decimal("0")


        slist_data.clear()
        slist = Slist()
        slist_data.append(slist)


        for billjournal in db_session.query(Billjournal).filter(
                 (Billjournal.bill_datum == date1) & (Billjournal.departement == 0) & (Billjournal.artnr == lodg_artnr)).order_by(Billjournal._recid).all():
            d =  to_decimal(billjournal.betrag) / to_decimal((1) + to_decimal(vat) + to_decimal(service))
            slist.bjournal =  to_decimal(slist.bjournal) + to_decimal(d)

        for segmentstat in db_session.query(Segmentstat).filter(
                 (Segmentstat.datum == date1)).order_by(Segmentstat._recid).all():
            slist.segmstat =  to_decimal(slist.segmstat) + to_decimal(segmentstat.logis)
            slist.paxsegm = slist.paxsegm + segmentstat.persanz +\
                    segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.datum == date1) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
            slist.genstat =  to_decimal(slist.genstat) + to_decimal(genstat.logis)
            slist.paxgenstat = slist.paxgenstat +\
                    genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 +\
                    genstat.kind3


        flag = 2

        return generate_output()

    return generate_output()