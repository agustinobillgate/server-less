#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Segment, Arrangement, Zimkateg

def prepare_occ_fcast1_ddownbl():

    prepare_cache ([Segment, Arrangement, Zimkateg])

    ci_date = None
    segm_list_data = []
    argt_list_data = []
    zikat_list_data = []
    vhp_limited:bool = False
    segment = arrangement = zimkateg = None

    segm_list = argt_list = zikat_list = None

    segm_list_data, Segm_list = create_model("Segm_list", {"selected":bool, "segm":int, "bezeich":string})
    argt_list_data, Argt_list = create_model("Argt_list", {"selected":bool, "argtnr":int, "argt":string, "bezeich":string})
    zikat_list_data, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, segm_list_data, argt_list_data, zikat_list_data, vhp_limited, segment, arrangement, zimkateg


        nonlocal segm_list, argt_list, zikat_list
        nonlocal segm_list_data, argt_list_data, zikat_list_data

        return {"ci_date": ci_date, "segm-list": segm_list_data, "argt-list": argt_list_data, "zikat-list": zikat_list_data}

    def create_segm():

        nonlocal ci_date, segm_list_data, argt_list_data, zikat_list_data, vhp_limited, segment, arrangement, zimkateg


        nonlocal segm_list, argt_list, zikat_list
        nonlocal segm_list_data, argt_list_data, zikat_list_data

        for segment in db_session.query(Segment).filter(
                 (Segment.betriebsnr <= 2)).order_by(Segment.segmentcode).all():

            if not vhp_limited or (vhp_limited and segment.vip_level == 0):
                segm_list = Segm_list()
                segm_list_data.append(segm_list)

                segm_list.segm = segment.segmentcode
                segm_list.bezeich = to_string(segmentcode, ">>9 ") + entry(0, segment.bezeich, "$$0")


    def create_argt():

        nonlocal ci_date, segm_list_data, argt_list_data, zikat_list_data, vhp_limited, segment, arrangement, zimkateg


        nonlocal segm_list, argt_list, zikat_list
        nonlocal segm_list_data, argt_list_data, zikat_list_data

        for arrangement in db_session.query(Arrangement).order_by(Arrangement.arrangement).all():
            argt_list = Argt_list()
            argt_list_data.append(argt_list)

            argt_list.argt = arrangement.arrangement
            argt_list.bezeich = to_string(arrangement.arrangement, "x(5)") + " " +\
                    arrangement.argt_bez


    def create_zikat():

        nonlocal ci_date, segm_list_data, argt_list_data, zikat_list_data, vhp_limited, segment, arrangement, zimkateg


        nonlocal segm_list, argt_list, zikat_list
        nonlocal segm_list_data, argt_list_data, zikat_list_data

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg.bezeich).all():
            zikat_list = Zikat_list()
            zikat_list_data.append(zikat_list)

            zikat_list.zikatnr = zimkateg.zikatnr
            zikat_list.bezeich = zimkateg.bezeichnung


    ci_date = get_output(htpdate(87))
    create_segm()
    create_argt()
    create_zikat()

    return generate_output()