from functions.additional_functions import *
import decimal
from models import Paramtext, Zimkateg, Zimmer

def res_zimkateg0bl():
    rmcat_list_list = []
    i:int = 0
    anz_setup:int = 0
    isetup_array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    paramtext = zimkateg = zimmer = None

    rmcat_list = None

    rmcat_list_list, Rmcat_list = create_model("Rmcat_list", {"zikatnr":int, "kurzbez":str, "bezeich":str, "kurzbez1":str, "setup":str, "nr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmcat_list_list, i, anz_setup, isetup_array, paramtext, zimkateg, zimmer


        nonlocal rmcat_list
        nonlocal rmcat_list_list
        return {"rmcat-list": rmcat_list_list}

    for paramtext in db_session.query(Paramtext).filter(
            (Paramtext.txtnr >= 9201) &  (Paramtext.txtnr <= 9299)).all():

        if paramtext.notes != "":
            anz_setup = anz_setup + 1
            isetup_array[anz_setup - 1] = paramtext.txtnr - 9200

    for zimkateg in db_session.query(Zimkateg).all():

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zikatnr == zimkateg.zikatnr) &  (Zimmer.setup == 0)).first()

        if zimmer:
            rmcat_list = Rmcat_list()
            rmcat_list_list.append(rmcat_list)

            buffer_copy(zimkateg, rmcat_list)
        for i in range(1,anz_setup + 1) :

            paramtext = db_session.query(Paramtext).filter(
                    (Paramtext.txtnr == (isetup_array[i - 1] + 9200))).first()

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zikatnr == zimkateg.zikatnr) &  (Zimmer.setup == isetup_array[i - 1])).first()

            if zimmer:
                rmcat_list = Rmcat_list()
                rmcat_list_list.append(rmcat_list)

                rmcat_list.zikatnr = zimkateg.zikatnr
                rmcat_list.kurzbez = zimkateg.kurzbez
                rmcat_list.kurzbez1 = zimkateg.bezeichnung
                rmcat_list.bezeich = zimkateg.bezeichnung
                rmcat_list.kurzbez1 = zimkateg.kurzbez +\
                        substring(paramtext.notes, 0, 1)
                rmcat_list.setup = paramtext.ptexte
                rmcat_list.nr = i

    return generate_output()