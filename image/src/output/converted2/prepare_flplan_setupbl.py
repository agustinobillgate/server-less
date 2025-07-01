#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Htparam

def prepare_flplan_setupbl(location:int, floor:int):

    prepare_cache ([Htparam])

    f_char = ""
    t_queasy_list = []
    queasy = htparam = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_char, t_queasy_list, queasy, htparam
        nonlocal location, floor


        nonlocal t_queasy
        nonlocal t_queasy_list

        return {"f_char": f_char, "t-queasy": t_queasy_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 571)]})

    if htparam.feldtyp == 5 and htparam.fchar != "":
        f_char = htparam.fchar

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 25) & (Queasy.number1 == location) & (Queasy.number2 == floor)).order_by(Queasy.char1).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)

    return generate_output()