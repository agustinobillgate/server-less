#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Htparam

def read_queasybl(case_type:int, intkey:int, inpint1:int, inpchar1:string):

    prepare_cache ([Htparam])

    t_queasy_list = []
    i:int = 0
    j:int = 0
    sumuser:int = 0
    sumappr:int = 0
    p_786:string = ""
    queasy = htparam = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_list, i, j, sumuser, sumappr, p_786, queasy, htparam
        nonlocal case_type, intkey, inpint1, inpchar1


        nonlocal t_queasy
        nonlocal t_queasy_list

        return {"t-queasy": t_queasy_list}

    if case_type == 1:

        queasy = get_cache (Queasy, {"key": [(eq, intkey)],"number1": [(eq, inpint1)]})

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 2:

        queasy = get_cache (Queasy, {"key": [(eq, intkey)],"char1": [(eq, inpchar1)]})

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 3:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == intkey)).order_by(Queasy.char1).all():
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)

    elif case_type == 4:

        queasy = get_cache (Queasy, {"key": [(eq, intkey)],"char1": [(eq, inpchar1)]})

        if not queasy:

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == intkey) & (substring(Queasy.char1, 0, length(inpchar1)) == inpchar1)).first()

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 5:

        queasy = get_cache (Queasy, {"key": [(eq, intkey)]})

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 6:

        queasy = get_cache (Queasy, {"key": [(eq, intkey)],"char3": [(ne, "")]})

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 7:

        queasy = get_cache (Queasy, {"key": [(eq, intkey)],"number1": [(eq, inpint1)]})

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 8:

        queasy = get_cache (Queasy, {"key": [(eq, intkey)],"number1": [(eq, inpint1)],"char1": [(eq, inpchar1)]})

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 9:

        queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, intkey)],"char3": [(ne, "")]})

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 10:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == intkey) & (Queasy.number3 == inpint1)).order_by(Queasy._recid).all():
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 11:

        queasy = get_cache (Queasy, {"_recid": [(eq, intkey)]})

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 12:

        queasy = get_cache (Queasy, {"number1": [(eq, inpint1)],"number2": [(eq, 0)],"deci2": [(eq, 0)],"key": [(eq, intkey)]})

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 13:

        queasy = get_cache (Queasy, {"key": [(eq, intkey)],"number1": [(ne, inpint1)],"char3": [(eq, inpchar1)]})

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 14:

        queasy = get_cache (Queasy, {"key": [(eq, 25)],"number1": [(eq, intkey)],"number2": [(eq, inpint1)],"char3": [(eq, inpchar1)]})

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 15:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

        if inpint1 == 0:

            queasy = get_cache (Queasy, {"key": [(eq, 37)],"betriebsnr": [(eq, intkey)],"date1": [(eq, htparam.fdate)],"logi1": [(eq, true)],"char1": [(eq, "micros")]})
        else:

            queasy = get_cache (Queasy, {"key": [(eq, 37)],"betriebsnr": [(eq, intkey)],"date1": [(eq, htparam.fdate)],"logi1": [(eq, true)],"char1": [(eq, "micros")],"number1": [(eq, inpint1)]})

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
            pass
    elif case_type == 16:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 37) & (Queasy.betriebsnr == intkey) & (Queasy.date1 == htparam.fdate) & (Queasy.logi1) & (Queasy.char1 == ("micros").lower()) & (Queasy.number1 > inpint1)).order_by(Queasy._recid).all():
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
            pass

    return generate_output()