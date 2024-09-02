from functions.additional_functions import *
import decimal
from functions.htpchar import htpchar
from functions.htplogic import htplogic
from models import Hoteldpt

def prepare_setup_articlebl():
    licstr = ""
    coa_format = ""
    t_hoteldpt_list = []
    licflag:bool = False
    hoteldpt = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal licstr, coa_format, t_hoteldpt_list, licflag, hoteldpt


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list
        return {"licstr": licstr, "coa_format": coa_format, "t-hoteldpt": t_hoteldpt_list}


    coa_format = get_output(htpchar(977))
    licflag = get_output(htplogic(2000))

    if licflag:
        licstr = licstr + "2000;"
    licflag = get_output(htplogic(988))

    if licflag:
        licstr = licstr + "988;"

    for hoteldpt in db_session.query(Hoteldpt).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    return generate_output()