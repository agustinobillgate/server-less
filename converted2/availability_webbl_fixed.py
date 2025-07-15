#using conversion tools version: 1.0.0.113

from functions.additional_functions import *
from decimal import Decimal
from datetime import date, timedelta
from models import Res_line, Zimkateg, Htparam, Artikel, Fixleist, Arrangement, Reslin_queasy, Paramtext, Zimmer, Kontline, Outorder, Guest

zikat_list_list, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":string, "bezeich":string})

def availability_webbl(pvilanguage:int, printer_nr:int, call_from:int, txt_file:string, curr_date:date, to_date:date, incl_tentative:bool, zikat_list_list:[Zikat_list]):

    prepare_cache ([Zimkateg, Htparam, Artikel, Fixleist, Arrangement, Reslin_queasy, Paramtext, Zimmer, Kontline, Outorder])

    msg_str = ""
    room_list_list = []
    sum_list_list = []
    lnldelimeter:string = ""
    ttl_room:List[int] = create_empty_list(32,0)
    occ_room:List[int] = create_empty_list(32,0)
    ooo_room:List[int] = create_empty_list(32,0)
    anz_setup:int = 0
    tot_room:int = 0
    isetup_array:List[int] = create_empty_list(99,0)
    csetup_array:List[string] = create_empty_list(99,"")
    ci_date:date = None
    datum:date = None
    week_list:List[string] = [" Mon ", " Tue ", " Wed ", " Thu ", " Fri ", " Sat ", " Sun "]
    i:int = 0
    j:int = 0
    curr_day:int = 0
    tmp_date:date = None
    lvcarea:string = "availability1"
    res_line = zimkateg = htparam = artikel = fixleist = arrangement = reslin_queasy = paramtext = zimmer = kontline = outorder = guest = None

    rmcat_list = room_list = sum_list = tmp_resline = tmp_extra = temp_art = zikat_list = zkbuff = rlist = None

    rmcat_list_list, Rmcat_list = create_model("Rmcat_list", {"zikatnr":int, "kurzbez":string, "kurzbez1":string, "bezeich":string, "setup":string, "haupt":bool, "anzahl":int, "nr":int, "glores":bool})
    room_list_list, Room_list = create_model("Room_list", {"flag":string, "setup":int, "haupt":bool, "zikatnr":int, "bezeich":string, "room":[Decimal,32], "coom":[string,32], "glores":bool})
    sum_list_list, Sum_list = create_model("Sum_list", {"bezeich":string, "summe":[string,32]})
    tmp_resline_list, Tmp_resline = create_model_like(Res_line)
    tmp_extra_list, Tmp_extra = create_model("Tmp_extra", {"art":int, "typ_pos":string, "pos_from":string, "cdate":date, "room":string, "qty":int})
    temp_art_list, Temp_art = create_model("Temp_art", {"art_nr":int, "art_nm":string})

    Zkbuff = create_buffer("Zkbuff",Zimkateg)


    db_session = local_storage.db_session

    # ... (rest of the functions remain unchanged)

    tmp_date = curr_date - timedelta(days=1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    if htparam:
        ci_date = htparam.fdate
        days_diff = (to_date - curr_date).days
        for i in range(1, days_diff + 1):
            ttl_room[i - 1] = 0
            occ_room[i - 1] = 0
            ooo_room[i - 1] = 0

        get_bedsetup()
        create_rmcat_list()
        count_rmcateg()
        create_browse()
        calc_extra(curr_date)

        return generate_output()
    else:
        return {"msg_str": "Htparam with paramnr 87 not found", "room-list": [], "sum-list": []}
