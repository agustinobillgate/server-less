from functions.additional_functions import *
import decimal
from models import Queasy, H_artikel

def prepare_officer_admin_webbl():
    compli_dept = 0
    t_queasy_list = []
    str:str = ""
    queasy = h_artikel = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model_like(Queasy, {"rec_id":int, "char4":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal compli_dept, t_queasy_list, str, queasy, h_artikel


        nonlocal t_queasy
        nonlocal t_queasy_list
        return {"compli_dept": compli_dept, "t-queasy": t_queasy_list}

    def get_compli_dept():

        nonlocal compli_dept, t_queasy_list, str, queasy, h_artikel


        nonlocal t_queasy
        nonlocal t_queasy_list

        for h_artikel in db_session.query(H_artikel).filter(
                (H_artikel.artart == 11)).all():
            compli_dept = h_artikel.departement

            return


    get_compli_dept()

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 105)).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)
        t_queasy.rec_id = queasy._recid
        str = entry(num_entries(queasy.char3, "&") - 1 - 1, queasy.char3, "&")
        t_queasy.char3 = substring(queasy.char3, 0, len(queasy.char3) - len(str) - 2)


        t_queasy.char4 = trim(str)

    return generate_output()