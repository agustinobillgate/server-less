#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.move_resmemberbl import move_resmemberbl
from functions.read_zimkategbl import read_zimkategbl
from models import Res_line, Zimkateg

def move_resmember1bl(pvilanguage:int, resno:int, sorttype:int):
    r_list_data = []
    tlist_data = []
    lvcarea:string = "move-resmember"
    stat_list:List[string] = create_empty_list(14,"")
    done:bool = False
    res_line = zimkateg = None

    r_list = tlist = t_zimkateg = buf_r_list = None

    r_list_data, R_list = create_model_like(Res_line, {"select_flag":bool})
    tlist_data, Tlist = create_model("Tlist", {"select_flag":bool, "name":string, "ankunft":date, "abreise":date, "zinr":string, "kurzbez":string, "zipreis":Decimal, "arrangement":string, "erwachs":int, "gratis":int, "kind1":int, "kind2":int, "resstatus":string, "zimmeranz":int, "anztage":int})
    t_zimkateg_data, T_zimkateg = create_model_like(Zimkateg)
    buf_r_list_data, Buf_r_list = create_model_like(R_list)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal r_list_data, tlist_data, lvcarea, stat_list, done, res_line, zimkateg
        nonlocal pvilanguage, resno, sorttype


        nonlocal r_list, tlist, t_zimkateg, buf_r_list
        nonlocal r_list_data, tlist_data, t_zimkateg_data, buf_r_list_data

        return {"r-list": r_list_data, "tlist": tlist_data}

    stat_list[0] = translateExtended ("Guaranted", lvcarea, "")
    stat_list[1] = translateExtended ("6 PM", lvcarea, "")
    stat_list[2] = translateExtended ("Tentative", lvcarea, "")
    stat_list[3] = translateExtended ("WaitList", lvcarea, "")
    stat_list[4] = translateExtended ("VerbalConfirm", lvcarea, "")
    stat_list[5] = translateExtended ("Inhouse", lvcarea, "")
    stat_list[6] = ""
    stat_list[7] = translateExtended ("Departed", lvcarea, "")
    stat_list[8] = translateExtended ("Cancelled", lvcarea, "")
    stat_list[9] = translateExtended ("NoShow", lvcarea, "")
    stat_list[10] = translateExtended ("ShareRes", lvcarea, "")
    stat_list[11] = translateExtended ("AccGuest", lvcarea, "")
    stat_list[12] = translateExtended ("RmSharer", lvcarea, "")
    stat_list[13] = translateExtended ("AccGuest", lvcarea, "")
    done, r_list_data = get_output(move_resmemberbl(1, resno, sorttype, None, buf_r_list_data))
    t_zimkateg_data = get_output(read_zimkategbl(4, None, ""))

    for r_list in query(r_list_data, sort_by=[("zinr",False),("kontakt_nr",False),("resstatus",False)]):
        t_zimkateg = query(t_zimkateg_data, (lambda t_zimkateg: t_zimkateg.zikatnr == r_list.zikatnr), first=True)
        if not t_zimkateg:
            continue

        tlist = Tlist()
        tlist_data.append(tlist)

        tlist.select_flag = r_list.select_flag
        tlist.name = r_list.name
        tlist.ankunft = r_list.ankunft
        tlist.abreise = r_list.abreise
        tlist.zinr = r_list.zinr
        tlist.kurzbez = t_zimkateg.kurzbez
        tlist.zipreis =  to_decimal(r_list.zipreis)
        tlist.arrangement = r_list.arrangement
        tlist.erwachs = r_list.erwachs
        tlist.gratis = r_list.gratis
        tlist.kind1 = r_list.kind1
        tlist.kind2 = r_list.kind2
        tlist.resstatus = stat_list[r_list.resstatus + r_list.l_zuordnung[3 - 1]]
        tlist.zimmeranz = r_list.zimmeranz
        tlist.anztage = r_list.anztage

    return generate_output()