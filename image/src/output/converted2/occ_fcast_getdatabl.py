#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.cr_occfcast1_2bl import cr_occfcast1_2bl
from functions.cr_occfcast1_1lybl import cr_occfcast1_1lybl

segm_list_list, Segm_list = create_model("Segm_list", {"selected":bool, "segm":int, "bezeich":string})
argt_list_list, Argt_list = create_model("Argt_list", {"selected":bool, "argtnr":int, "argt":string, "bezeich":string})
zikat_list_list, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "bezeich":string})
outlook_list_list, Outlook_list = create_model("Outlook_list", {"selected":bool, "outlook_nr":int, "bezeich":string})

def occ_fcast_getdatabl(language_code:int, from_date:date, to_date:date, flag_i:int, all_segm:bool, all_argt:bool, all_zikat:bool, mi_lessooo:bool, mi_incltent:bool, rev_typ:int, mi_exclcomp:bool, all_outlook:bool, mi_lastyr:bool, segm_list_list:[Segm_list], argt_list_list:[Argt_list], zikat_list_list:[Zikat_list], outlook_list_list:[Outlook_list]):
    msg_str = ""
    room_list_list = []
    vhp_limited:bool = False

    room_list = segm_list = argt_list = zikat_list = outlook_list = None

    room_list_list, Room_list = create_model("Room_list", {"wd":int, "datum":date, "bezeich":string, "room":[Decimal,17], "coom":[string,17], "k_pax":int, "t_pax":int, "lodg":[Decimal,7], "avrglodg":Decimal, "avrglodg2":Decimal, "avrgrmrev":Decimal, "avrgrmrev2":Decimal, "others":[Decimal,8], "ly_fcast":string, "ly_actual":string, "ly_avlodge":string, "room_exccomp":int, "room_comp":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, room_list_list, vhp_limited
        nonlocal language_code, from_date, to_date, flag_i, all_segm, all_argt, all_zikat, mi_lessooo, mi_incltent, rev_typ, mi_exclcomp, all_outlook, mi_lastyr


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list
        nonlocal room_list_list

        return {"msg_str": msg_str, "room-list": room_list_list}

    if to_date < from_date:
        msg_str = "ToDate can not be earlier THEN FromDate."

        return generate_output()
    room_list_list = get_output(cr_occfcast1_2bl(segm_list_list, argt_list_list, zikat_list_list, outlook_list_list, language_code, 0, flag_i, from_date, to_date, all_segm, all_argt, all_zikat, mi_lessooo, mi_incltent, rev_typ, vhp_limited, mi_exclcomp, all_outlook))

    if mi_lastyr:
        room_list_list = get_output(cr_occfcast1_1lybl(from_date, to_date, all_segm, all_argt, all_zikat, room_list_list, segm_list_list, argt_list_list, zikat_list_list))

    return generate_output()