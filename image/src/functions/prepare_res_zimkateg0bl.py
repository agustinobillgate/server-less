from functions.additional_functions import *
import decimal
from functions.res_zimkateg0bl import res_zimkateg0bl
from models import Paramtext, Zimkateg

def prepare_res_zimkateg0bl():
    rmcat_list_list = []
    anz_setup:int = 0
    paramtext = zimkateg = None

    t_paramtext = rmcat_list = None

    t_paramtext_list, T_paramtext = create_model_like(Paramtext)
    rmcat_list_list, Rmcat_list = create_model("Rmcat_list", {"zikatnr":int, "kurzbez":str, "bezeich":str, "kurzbez1":str, "setup":str, "nr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmcat_list_list, anz_setup, paramtext, zimkateg


        nonlocal t_paramtext, rmcat_list
        nonlocal t_paramtext_list, rmcat_list_list
        return {"rmcat-list": rmcat_list_list}

    def get_bedsetup():

        nonlocal rmcat_list_list, anz_setup, paramtext, zimkateg


        nonlocal t_paramtext, rmcat_list
        nonlocal t_paramtext_list, rmcat_list_list

        for paramtext in db_session.query(Paramtext).filter(
                (Paramtext.txtnr >= 9201) &  (Paramtext.txtnr <= 9299)).all():

            if paramtext.notes != "":
                anz_setup = anz_setup + 1

    def create_rmcat_list():

        nonlocal rmcat_list_list, anz_setup, paramtext, zimkateg


        nonlocal t_paramtext, rmcat_list
        nonlocal t_paramtext_list, rmcat_list_list

        if anz_setup > 0:
            rmcat_list_list = get_output(res_zimkateg0bl())
        else:

            for zimkateg in db_session.query(Zimkateg).all():
                rmcat_list = Rmcat_list()
                rmcat_list_list.append(rmcat_list)

                rmcat_list.zikatnr = zimkateg.zikatnr
                rmcat_list.kurzbez = zimkateg.kurzbez
                rmcat_list.kurzbez1 = zimkateg.kurzbez
                rmcat_list.bezeich = zimkateg.bezeichnung

    get_bedsetup()
    create_rmcat_list()

    return generate_output()