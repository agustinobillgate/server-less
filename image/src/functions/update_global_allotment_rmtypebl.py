from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Kontline, Zimkateg

def update_global_allotment_rmtypebl(currcode:str):
    rmcat_list_list = []
    kontline = zimkateg = None

    rmcat_list = None

    rmcat_list_list, Rmcat_list = create_model("Rmcat_list", {"rmcat":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmcat_list_list, kontline, zimkateg


        nonlocal rmcat_list
        nonlocal rmcat_list_list
        return {"rmcat-list": rmcat_list_list}

    def create_rmtype_list():

        nonlocal rmcat_list_list, kontline, zimkateg


        nonlocal rmcat_list
        nonlocal rmcat_list_list

        i:int = 0

        for kontline in db_session.query(Kontline).filter(
                (func.lower(Kontline.kontcode) == (currcode).lower()) &  (Kontline.kontstat == 1)).all():

            if kontline.zikatnr == 0:

                for zimkateg in db_session.query(Zimkateg).all():

                    rmcat_list = query(rmcat_list_list, filters=(lambda rmcat_list :rmcat_list.rmcat == zimkateg.kurzbez), first=True)

                    if not rmcat_list:
                        rmcat_list = Rmcat_list()
                        rmcat_list_list.append(rmcat_list)

                        rmcat_list.rmcat = zimkateg.kurzbez


                break
            else:

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == kontline.zikatnr)).first()

                rmcat_list = query(rmcat_list_list, filters=(lambda rmcat_list :rmcat_list.rmcat == zimkateg.kurzbez), first=True)

                if not rmcat_list:
                    rmcat_list = Rmcat_list()
                    rmcat_list_list.append(rmcat_list)

                    rmcat_list.rmcat = zimkateg.kurzbez


    create_rmtype_list()

    return generate_output()