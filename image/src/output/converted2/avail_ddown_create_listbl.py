#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Zimmer, Guest, Zimkateg

def avail_ddown_create_listbl(pvilanguage:int, curr_zikat:int, datum:date):

    prepare_cache ([Res_line, Guest, Zimkateg])

    rlist_list = []
    lvcarea:string = "availability_ddownUI"
    stat_list:List[string] = create_empty_list(13,"")
    res_line = zimmer = guest = zimkateg = None

    rlist = None

    rlist_list, Rlist = create_model("Rlist", {"resnr":string, "zinr":string, "ankunft":date, "abreise":date, "zimmeranz":int, "resstatus":int, "zipreis":Decimal, "erwachs":int, "kind1":int, "gratis":int, "name":string, "rsvname":string, "confirmed":bool, "sleeping":bool, "bezeich":string, "res_status":string}, {"sleeping": True})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rlist_list, lvcarea, stat_list, res_line, zimmer, guest, zimkateg
        nonlocal pvilanguage, curr_zikat, datum


        nonlocal rlist
        nonlocal rlist_list

        return {"rlist": rlist_list}

    def create_list():

        nonlocal rlist_list, lvcarea, stat_list, res_line, zimmer, guest, zimkateg
        nonlocal pvilanguage, curr_zikat, datum


        nonlocal rlist
        nonlocal rlist_list

        do_it:bool = False
        rbuff = None
        tot_pax:int = 0
        tot_adult:int = 0
        tot_ch1:int = 0
        tot_ch2:int = 0
        tot_compli:int = 0
        tot_nights:int = 0
        tot_qty:Decimal = to_decimal("0.0")
        Rbuff =  create_buffer("Rbuff",Res_line)
        rlist_list.clear()
        tot_pax = 0
        tot_adult = 0
        tot_ch1 = 0
        tot_compli = 0
        tot_qty =  to_decimal("0")

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag <= 1) & (Res_line.resstatus != 12) & (Res_line.zikatnr == curr_zikat) & not_ (Res_line.ankunft > datum) & not_ (Res_line.abreise <= datum) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.kontakt_nr).all():
            rlist = Rlist()
            rlist_list.append(rlist)

            rlist.resnr = to_string(res_line.resnr)
            rlist.zinr = res_line.zinr
            rlist.name = res_line.name
            rlist.ankunft = res_line.ankunft
            rlist.abreise = res_line.abreise
            rlist.zimmeranz = res_line.zimmeranz
            rlist.zipreis =  to_decimal(res_line.zipreis)
            rlist.erwachs = res_line.erwachs
            rlist.kind1 = res_line.kind1
            rlist.gratis = res_line.gratis
            rlist.res_status = stat_list[res_line.resstatus - 1]


            if res_line.zinr != "":

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                if zimmer and not zimmer.sleeping:
                    rlist.sleeping = False

            if res_line.resstatus == 11 or res_line.resstatus == 13:

                rbuff = get_cache (Res_line, {"resnr": [(eq, to_int(res_line.resnr))],"reslinnr": [(eq, res_line.kontakt_nr)]})

                if rbuff:
                    rlist.confirmed = (rbuff.resstatus <= 2 or rbuff.resstatus == 5 or rbuff.resstatus == 6)
                else:
                    rlist.confirmed = True

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
            rlist.rsvname = guest.name + ", " + guest.anredefirma

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

            if zimkateg:
                rlist.bezeich = zimkateg.bezeichnung
            tot_pax = tot_pax + res_line.zimmeranz
            tot_adult = tot_adult + (res_line.erwachs * res_line.zimmeranz)
            tot_ch1 = tot_ch1 + (res_line.kind1 * res_line.zimmeranz)
            tot_compli = tot_compli + (res_line.gratis * res_line.zimmeranz)
            tot_qty =  to_decimal(tot_qty) + to_decimal(res_line.zipreis)

        if tot_pax != 0:
            rlist = Rlist()
            rlist_list.append(rlist)

            rlist.rsvname = "T O T A L"
            rlist.zimmeranz = tot_pax
            rlist.ankunft = None
            rlist.abreise = None
            rlist.erwachs = tot_adult
            rlist.kind1 = tot_ch1
            rlist.gratis = tot_compli
            rlist.zipreis =  to_decimal(tot_qty)


    stat_list[0] = translateExtended ("Guaranted", lvcarea, "")
    stat_list[1] = translateExtended ("6 PM", lvcarea, "")
    stat_list[2] = translateExtended ("Tentative", lvcarea, "")
    stat_list[3] = translateExtended ("WaitList", lvcarea, "")
    stat_list[4] = translateExtended ("OralConform", lvcarea, "")
    stat_list[5] = translateExtended ("Inhouse", lvcarea, "")
    stat_list[6] = ""
    stat_list[7] = translateExtended ("Departed", lvcarea, "")
    stat_list[8] = translateExtended ("Cancelled", lvcarea, "")
    stat_list[9] = translateExtended ("NoShow", lvcarea, "")
    stat_list[10] = translateExtended ("ShareRes", lvcarea, "")
    stat_list[11] = translateExtended ("Extra Bill", lvcarea, "")
    stat_list[12] = translateExtended ("RmSharer", lvcarea, "")
    create_list()

    return generate_output()