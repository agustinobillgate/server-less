from functions.additional_functions import *
import decimal
from datetime import date
from models import Res_line, Reservation, Segment, Zimmer, Guest

def avail_ddown_detail_occupiedbl(datum:date):
    rlist_list = []
    res_line = reservation = segment = zimmer = guest = None

    rlist = None

    rlist_list, Rlist = create_model("Rlist", {"resnr":str, "zinr":str, "ankunft":date, "abreise":date, "zimmeranz":int, "resstatus":int, "zipreis":decimal, "erwachs":int, "kind1":int, "gratis":int, "name":str, "rsvname":str, "confirmed":bool, "sleeping":bool, "bezeich":str, "res_status":str}, {"sleeping": True})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rlist_list, res_line, reservation, segment, zimmer, guest


        nonlocal rlist
        nonlocal rlist_list
        return {"rlist": rlist_list}

    def detail_occupied():

        nonlocal rlist_list, res_line, reservation, segment, zimmer, guest


        nonlocal rlist
        nonlocal rlist_list

        qty:int = 0
        tot_adult:int = 0
        tot_ch:int = 0
        tot_rmrate:int = 0
        do_it:bool = False
        vhp_limited:bool = False

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resstatus == 6) &  (Res_line.active_flag == 1) &  (Res_line.abreise > datum) &  (Res_line.active_flag == 1) &  (Res_line.l_zuordnung[2] == 0)).all():

            if not vhp_limited:
                do_it = True
            else:

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == res_line.resnr)).first()

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == reservation.segmentcode)).first()
                do_it = None != segment and segment.vip_level == 0

            if do_it:

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == res_line.zinr)).first()

                if zimmer.sleeping:
                    rlist = Rlist()
                    rlist_list.append(rlist)

                    rlist.resnr = to_string(res_line.resnr)
                    rlist.name = res_line.name
                    rlist.ankunft = res_line.ankunft
                    rlist.abreise = res_line.abreise
                    rlist.zimmeranz = rlist.zimmeranz
                    rlist.zipreis = res_line.zipreis
                    rlist.erwachs = res_line.erwachs
                    rlist.kind1 = res_line.kind1 + res_line.kind2

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnr)).first()
                rlist.rsvName = guest.name + ", " + guest.anredefirma
                qty = qty + rlist.zimmeranz
                tot_adult = tot_adult + rlist.erwachs
                tot_ch = tot_ch + rlist.kind1
                tot_rmrate = tot_rmrate + rlist.zipreis

        if qty != 0:
            rlist = Rlist()
            rlist_list.append(rlist)

            rlist.rsvName = "T O T A L"
            rlist.ankunft = None
            rlist.abreise = None
            rlist.zimmeranz = qty
            rlist.zipreis = tot_rmrate
            rlist.erwachs = tot_adult
            rlist.kind1 = tot_ch

    pass

    detail_occupied()

    return generate_output()