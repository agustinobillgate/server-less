#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Kontline, Zimmer

def avail_ddown_detail_allotmentbl(curr_zikat:int, datum:date):

    prepare_cache ([Kontline, Zimmer])

    rlist_data = []
    kontline = zimmer = None

    rlist = None

    rlist_data, Rlist = create_model("Rlist", {"resnr":string, "zinr":string, "ankunft":date, "abreise":date, "zimmeranz":int, "resstatus":int, "zipreis":Decimal, "erwachs":int, "kind1":int, "gratis":int, "name":string, "rsvname":string, "confirmed":bool, "sleeping":bool, "bezeich":string, "res_status":string}, {"sleeping": True})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rlist_data, kontline, zimmer
        nonlocal curr_zikat, datum


        nonlocal rlist
        nonlocal rlist_data

        return {"rlist": rlist_data}

    def detail_allotments():

        nonlocal rlist_data, kontline, zimmer
        nonlocal curr_zikat, datum


        nonlocal rlist
        nonlocal rlist_data

        if curr_zikat == 0:

            for kontline in db_session.query(Kontline).filter(
                     (Kontline.betriebsnr == 1) & (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():

                zimmer = db_session.query(Zimmer).filter(
                         (Zimmer.zikatnr == kontline.zikatnr) & (Zimmer.sleeping)).first()
                rlist = Rlist()
                rlist_data.append(rlist)

                rlist.zimmeranz = kontline.zimmeranz + 1
                rlist.zinr = zimmer.zinr
                rlist.name = outorder.gespgrund
                rlist.abreise = kontline.abreise
                rlist.ankunft = kontline.ankunft
                rlist.bezeich = zimmer.bezeich


        else:

            for kontline in db_session.query(Kontline).filter(
                     (Kontline.betriebsnr == 1) & (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.zikatnr == curr_zikat) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():

                zimmer = db_session.query(Zimmer).filter(
                         (Zimmer.zikatnr == kontline.zikatnr) & (Zimmer.sleeping)).first()
                rlist = Rlist()
                rlist_data.append(rlist)

                rlist.zimmeranz = kontline.zimmeranz + 1
                rlist.zinr = zimmer.zinr
                rlist.name = outorder.gespgrund
                rlist.abreise = kontline.abreise
                rlist.ankunft = kontline.ankunft
                rlist.bezeich = zimmer.bezeich

    detail_allotments()

    return generate_output()