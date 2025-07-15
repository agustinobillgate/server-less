#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.res_zimkateg0bl import res_zimkateg0bl
from models import Paramtext, Zimkateg

def prepare_res_zimkateg0bl():

    prepare_cache ([Paramtext, Zimkateg])

    rmcat_list_data = []
    anz_setup:int = 0
    paramtext = zimkateg = None

    t_paramtext = rmcat_list = None

    t_paramtext_data, T_paramtext = create_model_like(Paramtext)
    rmcat_list_data, Rmcat_list = create_model("Rmcat_list", {"zikatnr":int, "kurzbez":string, "bezeich":string, "kurzbez1":string, "setup":string, "nr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmcat_list_data, anz_setup, paramtext, zimkateg


        nonlocal t_paramtext, rmcat_list
        nonlocal t_paramtext_data, rmcat_list_data

        return {"rmcat-list": rmcat_list_data}

    def get_bedsetup():

        nonlocal rmcat_list_data, anz_setup, paramtext, zimkateg


        nonlocal t_paramtext, rmcat_list
        nonlocal t_paramtext_data, rmcat_list_data

        for paramtext in db_session.query(Paramtext).filter(
                 (Paramtext.txtnr >= 9201) & (Paramtext.txtnr <= 9299)).order_by(Paramtext.txtnr).all():

            if paramtext.notes != "":
                anz_setup = anz_setup + 1


    def create_rmcat_list():

        nonlocal rmcat_list_data, anz_setup, paramtext, zimkateg


        nonlocal t_paramtext, rmcat_list
        nonlocal t_paramtext_data, rmcat_list_data

        if anz_setup > 0:
            rmcat_list_data = get_output(res_zimkateg0bl())
        else:

            for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
                rmcat_list = Rmcat_list()
                rmcat_list_data.append(rmcat_list)

                rmcat_list.zikatnr = zimkateg.zikatnr
                rmcat_list.kurzbez = zimkateg.kurzbez
                rmcat_list.kurzbez1 = zimkateg.kurzbez
                rmcat_list.bezeich = zimkateg.bezeichnung


    get_bedsetup()
    create_rmcat_list()

    return generate_output()