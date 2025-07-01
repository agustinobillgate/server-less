#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.view_staycostbl import view_staycostbl
from models import Htparam, Res_line, Guest_pr, Zimkateg, Arrangement, Waehrung

def prepare_view_staycostbl(pvilanguage:int, resnr:int, reslinnr:int):

    prepare_cache ([Htparam, Res_line, Guest_pr, Zimkateg, Arrangement, Waehrung])

    ci_date = None
    contcode = ""
    ct = ""
    curr_rmcat = ""
    t_str = ""
    str_arrangement = ""
    kurzbez = ""
    t_res_line_list = []
    output_list_list = []
    new_contrate:bool = False
    lvcarea:string = "view-staycost"
    bonus_array:List[bool] = create_empty_list(999, False)
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    htparam = res_line = guest_pr = zimkateg = arrangement = waehrung = None

    output_list = t_res_line = None

    output_list_list, Output_list = create_model("Output_list", {"flag":int, "str":string, "str1":string})
    t_res_line_list, T_res_line = create_model("T_res_line", {"name":string, "zinr":string, "ankunft":date, "abreise":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, contcode, ct, curr_rmcat, t_str, str_arrangement, kurzbez, t_res_line_list, output_list_list, new_contrate, lvcarea, bonus_array, wd_array, htparam, res_line, guest_pr, zimkateg, arrangement, waehrung
        nonlocal pvilanguage, resnr, reslinnr


        nonlocal output_list, t_res_line
        nonlocal output_list_list, t_res_line_list

        return {"ci_date": ci_date, "contcode": contcode, "ct": ct, "curr_rmcat": curr_rmcat, "t_str": t_str, "str_arrangement": str_arrangement, "kurzbez": kurzbez, "t-res-line": t_res_line_list, "output-list": output_list_list}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    if not res_line:

        return generate_output()
    t_res_line = T_res_line()
    t_res_line_list.append(t_res_line)

    t_res_line.name = res_line.name
    t_res_line.zinr = res_line.zinr
    t_res_line.ankunft = res_line.ankunft
    t_res_line.abreise = res_line.abreise


    contcode = ""

    guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

    if guest_pr:
        contcode = guest_pr.code
        ct = res_line.zimmer_wunsch

        if matches(ct,r"*$CODE$*"):
            ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
            contcode = substring(ct, 0, get_index(ct, ";") - 1)

    if res_line.l_zuordnung[0] != 0:

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.l_zuordnung[0])]})

        if zimkateg:
            curr_rmcat = zimkateg.kurzbez

    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

    if arrangement:
        str_arrangement = arrangement.arrangement

    if str_arrangement != "":
        t_str = translateExtended ("Forecast RoomRev", lvcarea, "") + " " + trim(to_string(res_line.name, "x(30)")) + " " + zimkateg.kurzbez + "/" + arrangement.arrangement
    else:
        t_str = translateExtended ("Forecast RoomRev", lvcarea, "") + " " + trim(to_string(res_line.name, "x(30)")) + " " + zimkateg.kurzbez

    if res_line.betriebsnr != 0:

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

        if waehrung:
            t_str = t_str + "/" + waehrung.wabkurz

    if curr_rmcat != "":
        t_str = t_str + translateExtended (" (Rate Rmcat =", lvcarea, "") + " " + curr_rmcat + ")"

    if zimkateg:
        kurzbez = zimkateg.kurzbez
    output_list_list = get_output(view_staycostbl(pvilanguage, resnr, reslinnr, contcode))

    return generate_output()