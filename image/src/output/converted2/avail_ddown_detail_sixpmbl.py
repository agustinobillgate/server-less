from functions.additional_functions import *
import decimal
from datetime import date
from models import Zimkateg, Res_line, Zimmer, Reservation, Segment, Guest

def avail_ddown_detail_sixpmbl(datum:date):
    rlist_list = []
    zimkateg = res_line = zimmer = reservation = segment = guest = None

    rlist = None

    rlist_list, Rlist = create_model("Rlist", {"resnr":str, "zinr":str, "ankunft":date, "abreise":date, "zimmeranz":int, "resstatus":int, "zipreis":decimal, "erwachs":int, "kind1":int, "gratis":int, "name":str, "rsvname":str, "confirmed":bool, "sleeping":bool, "bezeich":str, "res_status":str}, {"sleeping": True})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rlist_list, zimkateg, res_line, zimmer, reservation, segment, guest
        nonlocal datum


        nonlocal rlist
        nonlocal rlist_list
        return {"rlist": rlist_list}

    def detail_sixpm():

        nonlocal rlist_list, zimkateg, res_line, zimmer, reservation, segment, guest
        nonlocal datum


        nonlocal rlist
        nonlocal rlist_list

        qty:int = 0
        tot_adult:int = 0
        tot_ch:int = 0
        tot_rmrate:int = 0
        do_it:bool = False
        vhp_limited:bool = False

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag == 0) & (Res_line.resstatus == 2) & (Res_line.zikatnr == zimkateg.zikatnr) & (Res_line.ankunft <= datum) & (Res_line.abreise > datum) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                do_it = True

                if res_line.zinr != "":

                    zimmer = db_session.query(Zimmer).filter(
                             (Zimmer.zinr == res_line.zinr)).first()
                    do_it = zimmer.sleeping

                if do_it and vhp_limited:

                    reservation = db_session.query(Reservation).filter(
                             (Reservation.resnr == res_line.resnr)).first()

                    segment = db_session.query(Segment).filter(
                             (Segment.segmentcode == reservation.segmentcode)).first()
                    do_it = None ! == segment and segment.vip_level == 0

                if do_it:
                    rlist = Rlist()
                    rlist_list.append(rlist)

                    rlist.resnr = to_string(res_line.resnr)
                    rlist.name = res_line.name
                    rlist.ankunft = res_line.ankunft
                    rlist.abreise = res_line.abreise
                    rlist.zimmeranz = rlist.zimmeranz
                    rlist.zipreis =  to_decimal(res_line.zipreis)
                    rlist.erwachs = res_line.erwachs
                    rlist.kind1 = res_line.kind1 + res_line.kind2

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == res_line.gastnr)).first()
                rlist.rsvname = guest.name + ", " + guest.anredefirma
                qty = qty + rlist.zimmeranz
                tot_adult = tot_adult + rlist.erwachs
                tot_ch = tot_ch + rlist.kind1
                tot_rmrate = tot_rmrate + rlist.zipreis

        if qty != 0:
            rlist = Rlist()
            rlist_list.append(rlist)

            rlist.rsvname = "T O T A L"
            rlist.ankunft = None
            rlist.abreise = None
            rlist.zimmeranz = qty
            rlist.zipreis =  to_decimal(tot_rmrate)
            rlist.erwachs = tot_adult
            rlist.kind1 = tot_ch


    pass

    detail_sixpm()

    return generate_output()