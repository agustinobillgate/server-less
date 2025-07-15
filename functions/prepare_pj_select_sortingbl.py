#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Segment, Arrangement, Zimkateg

def prepare_pj_select_sortingbl():

    prepare_cache ([Segment, Arrangement, Zimkateg])

    segm1_list_data = []
    argt_list_data = []
    zikat_list_data = []
    segment = arrangement = zimkateg = None

    segm1_list = argt_list = zikat_list = None

    segm1_list_data, Segm1_list = create_model("Segm1_list", {"selected":bool, "segm":int, "bezeich":string, "bezeich1":string})
    argt_list_data, Argt_list = create_model("Argt_list", {"selected":bool, "argtnr":int, "argt":string, "bezeich":string})
    zikat_list_data, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":string, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal segm1_list_data, argt_list_data, zikat_list_data, segment, arrangement, zimkateg


        nonlocal segm1_list, argt_list, zikat_list
        nonlocal segm1_list_data, argt_list_data, zikat_list_data

        return {"segm1-list": segm1_list_data, "argt-list": argt_list_data, "zikat-list": zikat_list_data}

    def create_segm():

        nonlocal segm1_list_data, argt_list_data, zikat_list_data, segment, arrangement, zimkateg


        nonlocal segm1_list, argt_list, zikat_list
        nonlocal segm1_list_data, argt_list_data, zikat_list_data

        for segment in db_session.query(Segment).filter(
                 (Segment.betriebsnr <= 2)).order_by(Segment.segmentcode).all():
            segm1_list = Segm1_list()
            segm1_list_data.append(segm1_list)

            segm1_list.segm = segment.segmentcode
            segm1_list.bezeich = to_string(segment.segmentcode, ">>9 ") + entry(0, segment.bezeich, "$$0")


            segm1_list.bezeich1 = entry(0, segment.bezeich, "$$0")


    def create_argt():

        nonlocal segm1_list_data, argt_list_data, zikat_list_data, segment, arrangement, zimkateg


        nonlocal segm1_list, argt_list, zikat_list
        nonlocal segm1_list_data, argt_list_data, zikat_list_data

        for arrangement in db_session.query(Arrangement).order_by(Arrangement.arrangement).all():
            argt_list = Argt_list()
            argt_list_data.append(argt_list)

            argt_list.argt = arrangement.arrangement
            argt_list.bezeich = to_string(arrangement.arrangement, "x(5)") + " " +\
                    arrangement.argt_bez


    def create_zikat():

        nonlocal segm1_list_data, argt_list_data, zikat_list_data, segment, arrangement, zimkateg


        nonlocal segm1_list, argt_list, zikat_list
        nonlocal segm1_list_data, argt_list_data, zikat_list_data

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg.kurzbez).all():
            zikat_list = Zikat_list()
            zikat_list_data.append(zikat_list)

            zikat_list.zikatnr = zimkateg.zikatnr
            zikat_list.kurzbez = zimkateg.kurzbez
            zikat_list.bezeich = zimkateg.bezeichnung

    create_segm()
    create_argt()
    create_zikat()

    return generate_output()