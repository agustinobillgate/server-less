from functions.additional_functions import *
import decimal
from datetime import date
from models import Artikel, Billjournal, Segmentstat, Genstat

def correct_statistic_btn_dispbl(lodg_artnr:int, date1:date):
    flag = 0
    slist_list = []
    vat:decimal = 0
    service:decimal = 0
    d:decimal = 0
    artikel = billjournal = segmentstat = genstat = None

    slist = None

    slist_list, Slist = create_model("Slist", {"bjournal":decimal, "genstat":decimal, "paxgenstat":int, "segmstat":decimal, "paxsegm":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, slist_list, vat, service, d, artikel, billjournal, segmentstat, genstat


        nonlocal slist
        nonlocal slist_list
        return {"flag": flag, "slist": slist_list}

    artikel = db_session.query(Artikel).filter(
            (Artikel.artnr == lodg_artnr) &  (Artikel.departement == 0)).first()

    if not artikel:
        flag = 1

        return generate_output()
    else:
        service = 0
        vat = 0


        slist_list.clear()
        slist = Slist()
        slist_list.append(slist)


        for billjournal in db_session.query(Billjournal).filter(
                (Billjournal.bill_datum == date1) &  (Billjournal.departement == 0) &  (Billjournal.artnr == lodg_artnr)).all():
            d = billjournal.betrag / (1 + vat + service)
            slist.bjournal = slist.bjournal + d

        for segmentstat in db_session.query(Segmentstat).filter(
                (Segmentstat.datum == date1)).all():
            slist.segmstat = slist.segmstat + segmentstat.logis
            slist.paxsegm = slist.paxsegm + segmentstat.persanz +\
                    segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis

        for genstat in db_session.query(Genstat).filter(
                (Genstat.datum == date1) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
            slist.genstat = slist.genstat + genstat.logis
            slist.paxgenstat = slist.paxgenstat +\
                    genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 +\
                    genstat.kind3


        flag = 2

        return generate_output()