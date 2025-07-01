#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zimmer, Outorder

def avail_ddown_ooo_roombl(curr_zikat:int, datum:date):

    prepare_cache ([Zimmer, Outorder])

    rlist_list = []
    zimmer = outorder = None

    rlist = None

    rlist_list, Rlist = create_model("Rlist", {"resnr":string, "zinr":string, "ankunft":date, "abreise":date, "zimmeranz":int, "resstatus":int, "zipreis":Decimal, "erwachs":int, "kind1":int, "gratis":int, "name":string, "rsvname":string, "confirmed":bool, "sleeping":bool, "bezeich":string, "res_status":string}, {"sleeping": True})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rlist_list, zimmer, outorder
        nonlocal curr_zikat, datum


        nonlocal rlist
        nonlocal rlist_list

        return {"rlist": rlist_list}

    def ooo_room():

        nonlocal rlist_list, zimmer, outorder
        nonlocal curr_zikat, datum


        nonlocal rlist
        nonlocal rlist_list

        tot:int = 0

        if curr_zikat == 0:

            outorder_obj_list = {}
            outorder = Outorder()
            zimmer = Zimmer()
            for outorder.zinr, outorder.gespgrund, outorder.gespende, outorder.gespstart, outorder._recid, zimmer.bezeich, zimmer._recid in db_session.query(Outorder.zinr, Outorder.gespgrund, Outorder.gespende, Outorder.gespstart, Outorder._recid, Zimmer.bezeich, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).filter(
                     (Outorder.gespstart <= datum) & (Outorder.gespende >= datum) & (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
                if outorder_obj_list.get(outorder._recid):
                    continue
                else:
                    outorder_obj_list[outorder._recid] = True


                rlist = Rlist()
                rlist_list.append(rlist)

                rlist.zimmeranz = 1
                rlist.zinr = outorder.zinr
                rlist.name = outorder.gespgrund
                rlist.abreise = outorder.gespende
                rlist.ankunft = outorder.gespstart
                rlist.bezeich = zimmer.bezeich


                tot = tot + rlist.zimmeranz


        else:

            outorder_obj_list = {}
            outorder = Outorder()
            zimmer = Zimmer()
            for outorder.zinr, outorder.gespgrund, outorder.gespende, outorder.gespstart, outorder._recid, zimmer.bezeich, zimmer._recid in db_session.query(Outorder.zinr, Outorder.gespgrund, Outorder.gespende, Outorder.gespstart, Outorder._recid, Zimmer.bezeich, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping) & (Zimmer.zikatnr == curr_zikat)).filter(
                     (Outorder.gespstart <= datum) & (Outorder.gespende >= datum) & (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
                if outorder_obj_list.get(outorder._recid):
                    continue
                else:
                    outorder_obj_list[outorder._recid] = True


                rlist = Rlist()
                rlist_list.append(rlist)

                rlist.zimmeranz = 1
                rlist.zinr = outorder.zinr
                rlist.name = outorder.gespgrund
                rlist.abreise = outorder.gespende
                rlist.ankunft = outorder.gespstart
                rlist.bezeich = zimmer.bezeich


                tot = tot + 1

        if tot != 0:
            rlist = Rlist()
            rlist_list.append(rlist)

            rlist.name = "TOTAL"
            rlist.zimmeranz = tot
            rlist.abreise = None
            rlist.ankunft = None


    ooo_room()

    return generate_output()