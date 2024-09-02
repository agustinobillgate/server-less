from functions.additional_functions import *
import decimal
from models import Segment, Arrangement, Zimkateg

def prepare_avail_select_sortingbl():
    segm1_list_list = []
    argt_list_list = []
    zikat_list_list = []
    segment = arrangement = zimkateg = None

    segm1_list = argt_list = zikat_list = None

    segm1_list_list, Segm1_list = create_model("Segm1_list", {"selected":bool, "segm":int, "bezeich":str, "bezeich1":str})
    argt_list_list, Argt_list = create_model("Argt_list", {"selected":bool, "argtnr":int, "argt":str, "bezeich":str})
    zikat_list_list, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":str, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal segm1_list_list, argt_list_list, zikat_list_list, segment, arrangement, zimkateg


        nonlocal segm1_list, argt_list, zikat_list
        nonlocal segm1_list_list, argt_list_list, zikat_list_list
        return {"segm1-list": segm1_list_list, "argt-list": argt_list_list, "zikat-list": zikat_list_list}

    def create_segm():

        nonlocal segm1_list_list, argt_list_list, zikat_list_list, segment, arrangement, zimkateg


        nonlocal segm1_list, argt_list, zikat_list
        nonlocal segm1_list_list, argt_list_list, zikat_list_list

        for segment in db_session.query(Segment).filter(
                (Segment.betriebsnr <= 2)).all():
            segm1_list = Segm1_list()
            segm1_list_list.append(segm1_list)

            segm1_list.segm = segmentcode
            segm1_list.bezeich = to_string(segmentcode, ">>9 ") + entry(0, segment.bezeich, "$$0")


            segm1_list.bezeich1 = entry(0, segment.bezeich, "$$0")

    def create_argt():

        nonlocal segm1_list_list, argt_list_list, zikat_list_list, segment, arrangement, zimkateg


        nonlocal segm1_list, argt_list, zikat_list
        nonlocal segm1_list_list, argt_list_list, zikat_list_list

        for arrangement in db_session.query(Arrangement).all():
            argt_list = Argt_list()
            argt_list_list.append(argt_list)

            argt_list.argt = arrangement
            argt_list.bezeich = to_string(arrangement, "x(5)") + " " +\
                    arrangement.argt_bez

    def create_zikat():

        nonlocal segm1_list_list, argt_list_list, zikat_list_list, segment, arrangement, zimkateg


        nonlocal segm1_list, argt_list, zikat_list
        nonlocal segm1_list_list, argt_list_list, zikat_list_list

        for zimkateg in db_session.query(Zimkateg).all():
            zikat_list = Zikat_list()
            zikat_list_list.append(zikat_list)

            zikat_list.zikatnr = zimkateg.zikatnr
            zikat_list.kurzbez = zimkateg.kurzbez
            zikat_list.bezeich = zimkateg.bezeich


    create_segm()
    create_argt()
    create_zikat()

    return generate_output()