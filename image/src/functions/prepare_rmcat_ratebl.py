from functions.additional_functions import *
import decimal
from models import Zimkateg, Arrangement, Katpreis

def prepare_rmcat_ratebl():
    q1_list_list = []
    t_zimkateg_list = []
    t_arrangement_list = []
    zimkateg = arrangement = katpreis = None

    t_arrangement = t_zimkateg = q1_list = None

    t_arrangement_list, T_arrangement = create_model("T_arrangement", {"arrangement":str, "argtnr":int})
    t_zimkateg_list, T_zimkateg = create_model_like(Zimkateg)
    q1_list_list, Q1_list = create_model("Q1_list", {"betriebsnr":int, "kurzbez":str, "arrangement":str, "startperiode":date, "endperiode":date, "perspreis1":decimal, "perspreis2":decimal, "perspreis3":decimal, "perspreis4":decimal, "kindpreis1":decimal, "kindpreis2":decimal, "zikatnr":int, "argtnr":int, "katpreis_recid":int})


    db_session = local_storage.db_session
    result = db_session.execute(sa.text("SELECT current_schema();"))
    current_schema = result.scalar()
    print("Current Schema:", current_schema)

    def generate_output():
        nonlocal q1_list_list, t_zimkateg_list, t_arrangement_list, zimkateg, arrangement, katpreis


        nonlocal t_arrangement, t_zimkateg, q1_list
        nonlocal t_arrangement_list, t_zimkateg_list, q1_list_list
        return {"q1_list": q1_list_list, "t-zimkateg": t_zimkateg_list, "t-arrangement": t_arrangement_list}

    katpreis_obj_list = []
    for katpreis, zimkateg, arrangement in db_session.query(Katpreis, Zimkateg, Arrangement).join(Zimkateg,(Zimkateg.zikatnr == Katpreis.zikatnr)).join(Arrangement,(Arrangement.argtnr == Katpreis.argtnr)).filter(
            (Katpreis.betriebsnr >= 0)).all():
        if katpreis._recid in katpreis_obj_list:
            continue
        else:
            katpreis_obj_list.append(katpreis._recid)


        q1_list = Q1_list()
        

        q1_list.zikatnr = zimkateg.zikatnr
        q1_list.betriebsnr = katpreis.betriebsnr
        q1_list.kurzbez = zimkateg.kurzbez
        q1_list.arrangement = arrangement.arrangement
        q1_list.startperiode = katpreis.startperiode
        q1_list.endperiode = katpreis.endperiode
        q1_list.perspreis1 = katpreis.perspreis[0]
        q1_list.perspreis2 = katpreis.perspreis[1]
        q1_list.perspreis3 = katpreis.perspreis[2]
        q1_list.perspreis4 = katpreis.perspreis[3]
        q1_list.kindpreis1 = katpreis.kindpreis[0]
        q1_list.kindpreis2 = katpreis.kindpreis[1]
        q1_list.katpreis_recid = katpreis._recid
        q1_list_list.append(q1_list)

    for zimkateg in db_session.query(Zimkateg).all():
        t_zimkateg = T_zimkateg()
        t_zimkateg_list.append(t_zimkateg)

        buffer_copy(zimkateg, t_zimkateg)

    for arrangement in db_session.query(Arrangement).all():
        t_arrangement = T_arrangement()
        t_arrangement_list.append(t_arrangement)

        t_arrangement = arrangement
        t_arrangement.argtnr = arrangement.argtnr

    return generate_output()