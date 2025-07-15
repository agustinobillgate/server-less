#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Reservation, Segment, Zimmer, Guest

def avail_ddown_detail_occupiedbl(datum:date):

    prepare_cache ([Res_line, Reservation, Guest])

    rlist_data = []
    res_line = reservation = segment = zimmer = guest = None

    rlist = None

    rlist_data, Rlist = create_model("Rlist", {"resnr":string, "zinr":string, "ankunft":date, "abreise":date, "zimmeranz":int, "resstatus":int, "zipreis":Decimal, "erwachs":int, "kind1":int, "gratis":int, "name":string, "rsvname":string, "confirmed":bool, "sleeping":bool, "bezeich":string, "res_status":string}, {"sleeping": True})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rlist_data, res_line, reservation, segment, zimmer, guest
        nonlocal datum


        nonlocal rlist
        nonlocal rlist_data

        return {"rlist": rlist_data}

    def detail_occupied():

        nonlocal rlist_data, res_line, reservation, segment, zimmer, guest
        nonlocal datum


        nonlocal rlist
        nonlocal rlist_data

        qty:int = 0
        tot_adult:int = 0
        tot_ch:int = 0
        tot_rmrate:int = 0
        do_it:bool = False
        vhp_limited:bool = False

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resstatus == 6) & (Res_line.active_flag == 1) & (Res_line.abreise > datum) & (Res_line.active_flag == 1) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

            if not vhp_limited:
                do_it = True
            else:

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                do_it = None != segment and segment.vip_level == 0

            if do_it:

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                if zimmer.sleeping:
                    rlist = Rlist()
                    rlist_data.append(rlist)

                    rlist.resnr = to_string(res_line.resnr)
                    rlist.name = res_line.name
                    rlist.ankunft = res_line.ankunft
                    rlist.abreise = res_line.abreise
                    rlist.zimmeranz = rlist.zimmeranz
                    rlist.zipreis =  to_decimal(res_line.zipreis)
                    rlist.erwachs = res_line.erwachs
                    rlist.kind1 = res_line.kind1 + res_line.kind2

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                rlist.rsvname = guest.name + ", " + guest.anredefirma
                qty = qty + rlist.zimmeranz
                tot_adult = tot_adult + rlist.erwachs
                tot_ch = tot_ch + rlist.kind1
                tot_rmrate = tot_rmrate + rlist.zipreis

        if qty != 0:
            rlist = Rlist()
            rlist_data.append(rlist)

            rlist.rsvname = "T O T A L"
            rlist.ankunft = None
            rlist.abreise = None
            rlist.zimmeranz = qty
            rlist.zipreis =  to_decimal(tot_rmrate)
            rlist.erwachs = tot_adult
            rlist.kind1 = tot_ch


    detail_occupied()

    return generate_output()