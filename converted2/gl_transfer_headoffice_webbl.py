#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.read_htparambl import read_htparambl
from functions.gl_transf_headoffice1bl import gl_transf_headoffice1bl
from functions.gl_transf_headoffice11bl import gl_transf_headoffice11bl
from models import Htparam, Gl_jouhdr, Gl_journal

def gl_transfer_headoffice_webbl(close_month:date, close_year:date, user_init:string, language_code:int):
    msg_str = ""
    success_flag = False
    htparam = gl_jouhdr = gl_journal = None

    t_htparam = t_gl_jouhdr = t_gl_journal = None

    t_htparam_data, T_htparam = create_model_like(Htparam)
    t_gl_jouhdr_data, T_gl_jouhdr = create_model_like(Gl_jouhdr)
    t_gl_journal_data, T_gl_journal = create_model_like(Gl_journal)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, success_flag, htparam, gl_jouhdr, gl_journal
        nonlocal close_month, close_year, user_init, language_code


        nonlocal t_htparam, t_gl_jouhdr, t_gl_journal
        nonlocal t_htparam_data, t_gl_jouhdr_data, t_gl_journal_data

        return {"msg_str": msg_str, "success_flag": success_flag}


    t_htparam_data = get_output(read_htparambl(3, 2843, 38))

    t_htparam = query(t_htparam_data, first=True)

    if not t_htparam:
        msg_str = "Param No [2843] was not available."

        return generate_output()

    if t_htparam and t_htparam.fchar == "":
        msg_str = "Param No [2843] is empty value."

        return generate_output()

    if not matches(t_htparam.fchar,r"*:*"):
        msg_str = "Wrong Head Office IP:Port format" + " " + t_htparam.fchar

        return generate_output()

    if num_entries(t_htparam.fchar, ":") == 2:
        success_flag, msg_str = get_output(gl_transf_headoffice1bl(language_code, close_month))

    elif num_entries(t_htparam.fchar, ":") == 3:
        success_flag, msg_str = get_output(gl_transf_headoffice11bl(language_code, close_month, close_year))

    return generate_output()