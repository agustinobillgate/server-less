from functions.additional_functions import *
import decimal
from datetime import date
from models import Res_line, Zimmer, Guest, Zimkateg

def avail_ddown_create_listbl(pvilanguage:int, curr_zikat:int, datum:date):
    rlist_list = []
    lvcarea:str = "availability__ddownUI"
    stat_list:[str] = ["", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    res_line = zimmer = guest = zimkateg = None

    rlist = rbuff = None

    rlist_list, Rlist = create_model("Rlist", {"resnr":str, "zinr":str, "ankunft":date, "abreise":date, "zimmeranz":int, "resstatus":int, "zipreis":decimal, "erwachs":int, "kind1":int, "gratis":int, "name":str, "rsvname":str, "confirmed":bool, "sleeping":bool, "bezeich":str, "res_status":str}, {"sleeping": True})

    Rbuff = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rlist_list, lvcarea, stat_list, res_line, zimmer, guest, zimkateg
        nonlocal rbuff


        nonlocal rlist, rbuff
        nonlocal rlist_list
        return {"rlist": rlist_list}

    def create_list():

        nonlocal rlist_list, lvcarea, stat_list, res_line, zimmer, guest, zimkateg
        nonlocal rbuff


        nonlocal rlist, rbuff
        nonlocal rlist_list

        do_it:bool = False
        tot_pax:int = 0
        tot_adult:int = 0
        tot_ch1:int = 0
        tot_ch2:int = 0
        tot_compli:int = 0
        tot_nights:int = 0
        tot_qty:decimal = 0
        Rbuff = Res_line
        rlist_list.clear()
        tot_pax = 0
        tot_adult = 0
        tot_ch1 = 0
        tot_compli = 0
        tot_qty = 0

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag <= 1) &  (Res_line.resstatus != 12) &  (Res_line.zikatnr == curr_zikat) &  (not Res_line.ankunft > datum) &  (not Res_line.abreise <= datum) &  (Res_line.l_zuordnung[2] == 0)).all():
            rlist = Rlist()
            rlist_list.append(rlist)

            rlist.resnr = to_string(res_line.resnr)
            rlist.zinr = res_line.zinr
            rlist.name = res_line.name
            rlist.ankunft = res_line.ankunft
            rlist.abreise = res_line.abreise
            rlist.zimmeranz = res_line.zimmeranz
            rlist.zipreis = res_line.zipreis
            rlist.erwachs = res_line.erwachs
            rlist.kind1 = res_line.kind1
            rlist.gratis = res_line.gratis
            rlist.res_status = stat_list[res_line.resstatus - 1]


            pass

            if res_line.zinr != "":

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == res_line.zinr)).first()

                if zimmer and not zimmer.sleeping:
                    rlist.sleeping = False

            if res_line.resstatus == 11 or res_line.resstatus == 13:

                rbuff = db_session.query(Rbuff).filter(
                        (Rbuff.resnr == to_int(res_line.resnr)) &  (Rbuff.reslinnr == res_line.kontakt_nr)).first()

                if rbuff:
                    rlist.confirmed = (rbuff.resstatus <= 2 or rbuff.resstatus == 5 or rbuff.resstatus == 6)
                else:
                    rlist.confirmed = True

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnr)).first()
            rlist.rsvName = guest.name + ", " + guest.anredefirma

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == res_line.zikatnr)).first()

            if zimkateg:
                rlist.bezeich = zimkateg.bezeich
            tot_pax = tot_pax + res_line.zimmeranz
            tot_adult = tot_adult + (res_line.erwachs * res_line.zimmeranz)
            tot_ch1 = tot_ch1 + (res_line.kind1 * res_line.zimmeranz)
            tot_compli = tot_compli + (res_line.gratis * res_line.zimmeranz)
            tot_qty = tot_qty + res_line.zipreis

        if tot_pax != 0:
            rlist = Rlist()
            rlist_list.append(rlist)

            rlist.rsvName = "T O T A L"
            rlist.zimmeranz = tot_pax
            rlist.ankunft = None
            rlist.abreise = None
            rlist.erwachs = tot_adult
            rlist.kind1 = tot_ch1
            rlist.gratis = tot_compli
            rlist.zipreis = tot_qty

    pass

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