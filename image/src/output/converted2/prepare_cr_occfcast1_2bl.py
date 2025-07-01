#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam, Paramtext, Segment, Arrangement, Zimkateg

def prepare_cr_occfcast1_2bl(pvilanguage:int, vhp_limited:bool):

    prepare_cache ([Htparam, Paramtext, Segment, Arrangement, Zimkateg])

    curr_date = None
    segm_list_list = []
    argt_list_list = []
    zikat_list_list = []
    t_buff_queasy_list = []
    outlook_list_list = []
    local_curr = ""
    lvcarea:string = "occ-fcast1"
    queasy = htparam = paramtext = segment = arrangement = zimkateg = None

    t_buff_queasy = segm_list = argt_list = zikat_list = outlook_list = buff_queasy = None

    t_buff_queasy_list, T_buff_queasy = create_model_like(Queasy)
    segm_list_list, Segm_list = create_model("Segm_list", {"selected":bool, "segm":int, "bezeich":string})
    argt_list_list, Argt_list = create_model("Argt_list", {"selected":bool, "argtnr":int, "argt":string, "bezeich":string})
    zikat_list_list, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "bezeich":string})
    outlook_list_list, Outlook_list = create_model("Outlook_list", {"selected":bool, "outlook_nr":int, "bezeich":string})

    Buff_queasy = create_buffer("Buff_queasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_date, segm_list_list, argt_list_list, zikat_list_list, t_buff_queasy_list, outlook_list_list, local_curr, lvcarea, queasy, htparam, paramtext, segment, arrangement, zimkateg
        nonlocal pvilanguage, vhp_limited
        nonlocal buff_queasy


        nonlocal t_buff_queasy, segm_list, argt_list, zikat_list, outlook_list, buff_queasy
        nonlocal t_buff_queasy_list, segm_list_list, argt_list_list, zikat_list_list, outlook_list_list

        return {"curr_date": curr_date, "segm-list": segm_list_list, "argt-list": argt_list_list, "zikat-list": zikat_list_list, "t-buff-queasy": t_buff_queasy_list, "outlook-list": outlook_list_list, "local_curr": local_curr}

    def create_outlook():

        nonlocal curr_date, segm_list_list, argt_list_list, zikat_list_list, t_buff_queasy_list, outlook_list_list, local_curr, lvcarea, queasy, htparam, paramtext, segment, arrangement, zimkateg
        nonlocal pvilanguage, vhp_limited
        nonlocal buff_queasy


        nonlocal t_buff_queasy, segm_list, argt_list, zikat_list, outlook_list, buff_queasy
        nonlocal t_buff_queasy_list, segm_list_list, argt_list_list, zikat_list_list, outlook_list_list

        for paramtext in db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == 230)).order_by(Paramtext._recid).all():
            outlook_list = Outlook_list()
            outlook_list_list.append(outlook_list)

            outlook_list.outlook_nr = paramtext.sprachcode
            outlook_list.bezeich = paramtext.ptexte


    def create_segm():

        nonlocal curr_date, segm_list_list, argt_list_list, zikat_list_list, t_buff_queasy_list, outlook_list_list, local_curr, lvcarea, queasy, htparam, paramtext, segment, arrangement, zimkateg
        nonlocal pvilanguage, vhp_limited
        nonlocal buff_queasy


        nonlocal t_buff_queasy, segm_list, argt_list, zikat_list, outlook_list, buff_queasy
        nonlocal t_buff_queasy_list, segm_list_list, argt_list_list, zikat_list_list, outlook_list_list

        for segment in db_session.query(Segment).filter(
                 (Segment.betriebsnr <= 2) & (num_entries(Segment.bezeich, "$$0") == 1)).order_by(Segment.segmentcode).all():

            if not vhp_limited or (vhp_limited and segment.vip_level == 0):
                segm_list = Segm_list()
                segm_list_list.append(segm_list)

                segm_list.segm = segment.segmentcode
                segm_list.bezeich = to_string(segment.segmentcode, ">>9 ") + entry(0, segment.bezeich, "$$0")


    def create_argt():

        nonlocal curr_date, segm_list_list, argt_list_list, zikat_list_list, t_buff_queasy_list, outlook_list_list, local_curr, lvcarea, queasy, htparam, paramtext, segment, arrangement, zimkateg
        nonlocal pvilanguage, vhp_limited
        nonlocal buff_queasy


        nonlocal t_buff_queasy, segm_list, argt_list, zikat_list, outlook_list, buff_queasy
        nonlocal t_buff_queasy_list, segm_list_list, argt_list_list, zikat_list_list, outlook_list_list

        for arrangement in db_session.query(Arrangement).filter(
                 (Arrangement.weeksplit == False)).order_by(Arrangement.arrangement).all():
            argt_list = Argt_list()
            argt_list_list.append(argt_list)

            argt_list.argt = arrangement.arrangement
            argt_list.bezeich = to_string(arrangement.arrangement, "x(5)") + " " +\
                    arrangement.argt_bez


    def create_zikat():

        nonlocal curr_date, segm_list_list, argt_list_list, zikat_list_list, t_buff_queasy_list, outlook_list_list, local_curr, lvcarea, queasy, htparam, paramtext, segment, arrangement, zimkateg
        nonlocal pvilanguage, vhp_limited
        nonlocal buff_queasy


        nonlocal t_buff_queasy, segm_list, argt_list, zikat_list, outlook_list, buff_queasy
        nonlocal t_buff_queasy_list, segm_list_list, argt_list_list, zikat_list_list, outlook_list_list

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg.bezeichnung).all():
            zikat_list = Zikat_list()
            zikat_list_list.append(zikat_list)

            zikat_list.zikatnr = zimkateg.zikatnr
            zikat_list.bezeich = zimkateg.bezeichnung


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    curr_date = htparam.fdate

    buff_queasy = db_session.query(Buff_queasy).filter(
             (Buff_queasy.key == 140) & (Buff_queasy.char1 == lvcarea)).first()

    if buff_queasy:
        t_buff_queasy = T_buff_queasy()
        t_buff_queasy_list.append(t_buff_queasy)

        buffer_copy(buff_queasy, t_buff_queasy)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})
    local_curr = htparam.fchar


    create_segm()
    create_argt()
    create_zikat()
    create_outlook()

    return generate_output()