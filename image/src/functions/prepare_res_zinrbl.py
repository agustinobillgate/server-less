from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from functions.read_zimkategbl import read_zimkategbl
from functions.read_res_linebl import read_res_linebl
from functions.read_paramtextbl import read_paramtextbl
from functions.read_zimmerbl import read_zimmerbl
from functions.res_zinrbl import res_zinrbl
from models import Zimkateg, Paramtext, Res_line, Zimmer

def prepare_res_zinrbl(c_rmcat:str, resnr:int, reslinnr:int, i_setup:int, sharer:bool, ankunft1:date, abreise1:date):
    ci_date = None
    t_paramtext1_list = []
    t_paramtext2_list = []
    t_paramtext3_list = []
    t_zimkateg_list = []
    t_res_line_list = []
    zimkateg1_list = []
    htl_feature_list = []
    room_list_list = []
    p_text:str = ""
    int_tzimkategzikatnr:int = 0
    zimkateg = paramtext = res_line = zimmer = None

    t_zimkateg = t_paramtext1 = t_paramtext2 = t_paramtext3 = t_res_line = t_zimmer = zimkateg1 = res_line1 = htl_feature = room_list = None

    t_zimkateg_list, T_zimkateg = create_model_like(Zimkateg)
    t_paramtext1_list, T_paramtext1 = create_model_like(Paramtext)
    t_paramtext2_list, T_paramtext2 = create_model_like(Paramtext)
    t_paramtext3_list, T_paramtext3 = create_model_like(Paramtext)
    t_res_line_list, T_res_line = create_model_like(Res_line)
    t_zimmer_list, T_zimmer = create_model_like(Zimmer)
    zimkateg1_list, Zimkateg1 = create_model_like(Zimkateg)
    res_line1_list, Res_line1 = create_model_like(Res_line)
    htl_feature_list, Htl_feature = create_model("Htl_feature", {"s":str, "flag":int}, {"flag": 1})
    room_list_list, Room_list = create_model("Room_list", {"i":int, "flag":bool, "sleeping":bool, "feature":str, "himmelsr":str, "build":str, "zikennz":str, "build_flag":str, "zistat":str, "infochar":str, "zinr":str, "bezeich":str, "etage":int, "outlook":str, "setup":str, "name":str, "comment":str, "verbindung1":str, "verbindung2":str, "infonum":int, "prioritaet":int, "recid1":int, "recid2":int, "infostr":str}, {"flag": True, "sleeping": True})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, t_paramtext1_list, t_paramtext2_list, t_paramtext3_list, t_zimkateg_list, t_res_line_list, zimkateg1_list, htl_feature_list, room_list_list, p_text, int_tzimkategzikatnr, zimkateg, paramtext, res_line, zimmer


        nonlocal t_zimkateg, t_paramtext1, t_paramtext2, t_paramtext3, t_res_line, t_zimmer, zimkateg1, res_line1, htl_feature, room_list
        nonlocal t_zimkateg_list, t_paramtext1_list, t_paramtext2_list, t_paramtext3_list, t_res_line_list, t_zimmer_list, zimkateg1_list, res_line1_list, htl_feature_list, room_list_list
        return {"ci_date": ci_date, "t-paramtext1": t_paramtext1_list, "t-paramtext2": t_paramtext2_list, "t-paramtext3": t_paramtext3_list, "t-zimkateg": t_zimkateg_list, "t-res-line": t_res_line_list, "zimkateg1": zimkateg1_list, "htl-feature": htl_feature_list, "room-list": room_list_list}

    ci_date = get_output(htpdate(87))
    t_zimkateg_list = get_output(read_zimkategbl(2, None, c_rmcat))

    t_zimkateg = query(t_zimkateg_list, first=True)

    if t_zimkateg:
        int_tzimkategzikatnr = t_zimkateg.zikatnr
    t_res_line_list = get_output(read_res_linebl(1, resnr, reslinnr, None, None, None, None, None, None, None, None))

    t_res_line = query(t_res_line_list, first=True)
    zimkateg1_list = get_output(read_zimkategbl(3, None, None))
    p_text, t_paramtext1_list = get_output(read_paramtextbl(3, 9201))
    p_text, t_paramtext2_list = get_output(read_paramtextbl(3, 230))

    if i_setup > 0:
        p_text, t_paramtext3_list = get_output(read_paramtextbl(2, (i_setup + 9200)))

    if sharer:
        res_line1_list = get_output(read_res_linebl(4, resnr, None, None, None, None, None, None, None, None, None))

        for res_line1 in query(res_line1_list, filters=(lambda res_line1 :res_line1.zinr != "" and res_line1.resstatus <= 6)):

            if res_line1.ankunft <= ankunft1 and res_line1.abreise >= abreise1:
                t_zimmer_list = get_output(read_zimmerbl(1, res_line1.zinr, None, None))

                t_zimmer = query(t_zimmer_list, first=True)


                if t_zimmer.zikatnr == int_tzimkategzikatnr:

                    if t_zimmer.setup > 0:

                        paramtext = db_session.query(Paramtext).filter(
                                (Paramtext.txtnr == (t_zimmer.setup + 9200))).first()
                    room_list = Room_list()
                    room_list_list.append(room_list)

                    room_list.zinr = t_zimmer.zinr
                    room_list.prioritaet = t_zimmer.prioritaet
                    room_list.name = res_line1.name

                    if paramtext:
                        room_list.setup = paramtext.ptexte


    else:
        room_list_list, htl_feature_list = get_output(res_zinrbl(1, resnr, reslinnr, int_tzimkategzikatnr, ankunft1, abreise1))

    return generate_output()