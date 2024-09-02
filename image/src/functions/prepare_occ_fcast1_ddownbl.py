from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import Segment, Arrangement, Zimkateg

def prepare_occ_fcast1_ddownbl():
    ci_date = None
    segm_list_list = []
    argt_list_list = []
    zikat_list_list = []
    vhp_limited:bool = False
    segment = arrangement = zimkateg = None

    segm_list = argt_list = zikat_list = None

    segm_list_list, Segm_list = create_model("Segm_list", {"selected":bool, "segm":int, "bezeich":str})
    argt_list_list, Argt_list = create_model("Argt_list", {"selected":bool, "argtnr":int, "argt":str, "bezeich":str})
    zikat_list_list, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, segm_list_list, argt_list_list, zikat_list_list, vhp_limited, segment, arrangement, zimkateg


        nonlocal segm_list, argt_list, zikat_list
        nonlocal segm_list_list, argt_list_list, zikat_list_list
        return {"ci_date": ci_date, "segm-list": segm_list_list, "argt-list": argt_list_list, "zikat-list": zikat_list_list}

    def create_segm():

        nonlocal ci_date, segm_list_list, argt_list_list, zikat_list_list, vhp_limited, segment, arrangement, zimkateg


        nonlocal segm_list, argt_list, zikat_list
        nonlocal segm_list_list, argt_list_list, zikat_list_list

        for segment in db_session.query(Segment).filter(
                (Segment.betriebsnr <= 2)).all():

            if not vhp_limited or (vhp_limited and segment.vip_level == 0):
                segm_list = Segm_list()
                segm_list_list.append(segm_list)

                segm_list.segm = segmentcode
                segm_list.bezeich = to_string(segmentcode, ">>9 ") + entry(0, segment.bezeich, "$$0")

    def create_argt():

        nonlocal ci_date, segm_list_list, argt_list_list, zikat_list_list, vhp_limited, segment, arrangement, zimkateg


        nonlocal segm_list, argt_list, zikat_list
        nonlocal segm_list_list, argt_list_list, zikat_list_list

        for arrangement in db_session.query(Arrangement).all():
            argt_list = Argt_list()
            argt_list_list.append(argt_list)

            argt_list.argt = arrangement
            argt_list.bezeich = to_string(arrangement, "x(5)") + " " +\
                    arrangement.argt_bez

    def create_zikat():

        nonlocal ci_date, segm_list_list, argt_list_list, zikat_list_list, vhp_limited, segment, arrangement, zimkateg


        nonlocal segm_list, argt_list, zikat_list
        nonlocal segm_list_list, argt_list_list, zikat_list_list

        for zimkateg in db_session.query(Zimkateg).all():
            zikat_list = Zikat_list()
            zikat_list_list.append(zikat_list)

            zikat_list.zikatnr = zimkateg.zikatnr
            zikat_list.bezeich = zimkateg.bezeich

    pass

    ci_date = get_output(htpdate(87))
    create_segm()
    create_argt()
    create_zikat()

    return generate_output()