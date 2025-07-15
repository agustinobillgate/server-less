#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Kontline, Zimkateg

def update_global_allotment_rmtypebl(currcode:string):

    prepare_cache ([Kontline, Zimkateg])

    rmcat_list_data = []
    kontline = zimkateg = None

    rmcat_list = None

    rmcat_list_data, Rmcat_list = create_model("Rmcat_list", {"rmcat":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmcat_list_data, kontline, zimkateg
        nonlocal currcode


        nonlocal rmcat_list
        nonlocal rmcat_list_data

        return {"rmcat-list": rmcat_list_data}

    def create_rmtype_list():

        nonlocal rmcat_list_data, kontline, zimkateg
        nonlocal currcode


        nonlocal rmcat_list
        nonlocal rmcat_list_data

        i:int = 0

        for kontline in db_session.query(Kontline).filter(
                 (Kontline.kontcode == (currcode).lower()) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).yield_per(100):

            if kontline.zikatnr == 0:

                for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():

                    rmcat_list = query(rmcat_list_data, filters=(lambda rmcat_list: rmcat_list.rmcat == zimkateg.kurzbez), first=True)

                    if not rmcat_list:
                        rmcat_list = Rmcat_list()
                        rmcat_list_data.append(rmcat_list)

                        rmcat_list.rmcat = zimkateg.kurzbez


                break
            else:

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, kontline.zikatnr)]})

                rmcat_list = query(rmcat_list_data, filters=(lambda rmcat_list: rmcat_list.rmcat == zimkateg.kurzbez), first=True)

                if not rmcat_list:
                    rmcat_list = Rmcat_list()
                    rmcat_list_data.append(rmcat_list)

                    rmcat_list.rmcat = zimkateg.kurzbez

    create_rmtype_list()

    return generate_output()