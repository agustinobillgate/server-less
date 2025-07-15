#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

t_push_list_data, T_push_list = create_model("T_push_list", {"rcodevhp":string, "rcodebe":string, "rmtypevhp":string, "rmtypebe":string, "argtvhp":string, "flag":int})

def bookengine_ratecodepull_btn_exitbl(t_push_list_data:[T_push_list], bookengid:int):

    prepare_cache ([Queasy])

    str:string = ""
    queasy = None

    t_push_list = bufq = None

    Bufq = create_buffer("Bufq",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str, queasy
        nonlocal bookengid
        nonlocal bufq


        nonlocal t_push_list, bufq

        return {}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 163) & (Queasy.number1 == bookengid)).order_by(Queasy._recid).all():
        db_session.delete(queasy)

    for t_push_list in query(t_push_list_data):
        str = t_push_list.rcodevhp + ";" + t_push_list.rcodebe + ";" + t_push_list.rmtypevhp + ";" + t_push_list.rmtypebe + ";" + t_push_list.argtvhp
        bufq = Queasy()
        db_session.add(bufq)

        bufq.key = 163
        bufq.number1 = bookengid
        bufq.char1 = str


        pass

    return generate_output()