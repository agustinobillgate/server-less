from functions.additional_functions import *
import decimal
from models import Queasy

t_push_list_list, T_push_list = create_model("T_push_list", {"rcodevhp":str, "rcodebe":str, "rmtypevhp":str, "rmtypebe":str, "argtvhp":str, "flag":int})

def bookengine_ratecodepush_btn_exitbl(t_push_list_list:[T_push_list], bookengid:int):
    str:str = ""
    queasy = None

    t_push_list = bufq = None

    Bufq = create_buffer("Bufq",Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str, queasy
        nonlocal bookengid
        nonlocal bufq


        nonlocal t_push_list, bufq
        nonlocal t_push_list_list
        return {}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 161) & (Queasy.number1 == bookengid)).order_by(Queasy._recid).all():
        db_session.delete(queasy)

    for t_push_list in query(t_push_list_list):
        str = t_push_list.rcodeVHP + ";" + t_push_list.rcodeBE + ";" + t_push_list.rmtypeVHP + ";" + t_push_list.rmtypeBE + ";" + t_push_list.argtVHP
        bufq = Bufq()
        db_session.add(bufq)

        bufq.key = 161
        bufq.number1 = bookengid
        bufq.char1 = str


        pass

    return generate_output()