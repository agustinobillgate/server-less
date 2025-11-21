#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Zimkateg, Arrangement, Katpreis

def prepare_rmcat_ratebl():

    prepare_cache ([Arrangement, Katpreis])

    q1_list_data = []
    t_zimkateg_data = []
    t_arrangement_data = []
    zimkateg = arrangement = katpreis = None

    t_arrangement = t_zimkateg = q1_list = None

    t_arrangement_data, T_arrangement = create_model("T_arrangement", {"arrangement":string, "argtnr":int})
    t_zimkateg_data, T_zimkateg = create_model_like(Zimkateg)
    q1_list_data, Q1_list = create_model("Q1_list", {"betriebsnr":int, "kurzbez":string, "arrangement":string, "startperiode":date, "endperiode":date, "perspreis1":Decimal, "perspreis2":Decimal, "perspreis3":Decimal, "perspreis4":Decimal, "kindpreis1":Decimal, "kindpreis2":Decimal, "zikatnr":int, "argtnr":int, "katpreis_recid":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_data, t_zimkateg_data, t_arrangement_data, zimkateg, arrangement, katpreis


        nonlocal t_arrangement, t_zimkateg, q1_list
        nonlocal t_arrangement_data, t_zimkateg_data, q1_list_data

        return {"q1-list": q1_list_data, "t-zimkateg": t_zimkateg_data, "t-arrangement": t_arrangement_data}

    katpreis_obj_list = {}
    for katpreis, zimkateg, arrangement in db_session.query(Katpreis, Zimkateg, Arrangement).join(Zimkateg,(Zimkateg.zikatnr == Katpreis.zikatnr)).join(Arrangement,(Arrangement.argtnr == Katpreis.argtnr)).filter(
             (Katpreis.betriebsnr >= 0)).order_by(Katpreis.zikatnr, Katpreis.argtnr, Katpreis.startperiode).all():
        if katpreis_obj_list.get(katpreis._recid):
            continue
        else:
            katpreis_obj_list[katpreis._recid] = True


        q1_list = Q1_list()
        q1_list_data.append(q1_list)

        q1_list.zikatnr = zimkateg.zikatnr
        q1_list.betriebsnr = katpreis.betriebsnr
        q1_list.kurzbez = zimkateg.kurzbez
        q1_list.arrangement = arrangement.arrangement
        q1_list.startperiode = katpreis.startperiode
        q1_list.endperiode = katpreis.endperiode
        q1_list.perspreis1 = to_decimal(katpreis.perspreis[0])
        q1_list.perspreis2 = to_decimal(katpreis.perspreis[1])
        q1_list.perspreis3 = to_decimal(katpreis.perspreis[2])
        q1_list.perspreis4 = to_decimal(katpreis.perspreis[3])
        q1_list.kindpreis1 = to_decimal(katpreis.kindpreis[0])
        q1_list.kindpreis2 = to_decimal(katpreis.kindpreis[1])
        q1_list.argtnr = katpreis.argtnr
        q1_list.katpreis_recid = katpreis._recid

    for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
        t_zimkateg = T_zimkateg()
        t_zimkateg_data.append(t_zimkateg)

        buffer_copy(zimkateg, t_zimkateg)

    for arrangement in db_session.query(Arrangement).order_by(Arrangement._recid).all():
        t_arrangement = T_arrangement()
        t_arrangement_data.append(t_arrangement)

        t_arrangement.arrangement = arrangement.arrangement
        t_arrangement.argtnr = arrangement.argtnr

    return generate_output()