from functions.additional_functions import *
import decimal
from datetime import date
import re
from functions.view_staycostbl import view_staycostbl
from models import Htparam, Res_line, Guest_pr, Zimkateg, Arrangement, Waehrung

def prepare_view_staycostbl(pvilanguage:int, resnr:int, reslinnr:int):
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
    lvcarea:str = "view_staycost"
    bonus_array:[bool] = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    wd_array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    htparam = res_line = guest_pr = zimkateg = arrangement = waehrung = None

    output_list = t_res_line = None

    output_list_list, Output_list = create_model("Output_list", {"flag":int, "str":str, "str1":str})
    t_res_line_list, T_res_line = create_model("T_res_line", {"name":str, "zinr":str, "ankunft":date, "abreise":date})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, contcode, ct, curr_rmcat, t_str, str_arrangement, kurzbez, t_res_line_list, output_list_list, new_contrate, lvcarea, bonus_array, wd_array, htparam, res_line, guest_pr, zimkateg, arrangement, waehrung


        nonlocal output_list, t_res_line
        nonlocal output_list_list, t_res_line_list
        return {"ci_date": ci_date, "contcode": contcode, "ct": ct, "curr_rmcat": curr_rmcat, "t_str": t_str, "str_arrangement": str_arrangement, "kurzbez": kurzbez, "t-res-line": t_res_line_list, "output-list": output_list_list}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 550)).first()

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()
    t_res_line = T_res_line()
    t_res_line_list.append(t_res_line)

    t_res_line.name = res_line.name
    t_res_line.zinr = res_line.zinr
    t_res_line.ankunft = res_line.ankunft
    t_res_line.abreise = res_line.abreise


    contcode = ""

    guest_pr = db_session.query(Guest_pr).filter(
            (Guest_pr.gastnr == res_line.gastnr)).first()

    if guest_pr:
        contcode = guest_pr.CODE
        ct = res_line.zimmer_wunsch

        if re.match(".*\$CODE\$.*",ct):
            ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
            contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)

    if res_line.l_zuordnung[0] != 0:

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == res_line.l_zuordnung[0])).first()
        curr_rmcat = zimkateg.kurzbez

    zimkateg = db_session.query(Zimkateg).filter(
            (Zimkateg.zikatnr == res_line.zikatnr)).first()

    arrangement = db_session.query(Arrangement).filter(
            (Arrangement == res_line.arrangement)).first()
    str_arrangement = arrangement
    t_str = translateExtended ("Forecast RoomRev", lvcarea, "") + " " + trim(to_string(res_line.name, "x(30)")) + " " + zimkateg.kurzbez + "/" + arrangement

    if res_line.betriebsnr != 0:

        waehrung = db_session.query(Waehrung).filter(
                (Waehrungsnr == res_line.betriebsnr)).first()
        t_str = t_str + "/" + waehrung.wabkurz

    if curr_rmcat != "":
        t_str = t_str + translateExtended (" (Rate Rmcat  == ", lvcarea, "") + " " + curr_rmcat + ")"
    kurzbez = zimkateg.kurzbez
    output_list_list = get_output(view_staycostbl(pvilanguage, resnr, reslinnr, contcode))

    return generate_output()