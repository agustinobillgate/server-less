#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Brief, Parameters

def main_gl_mi_reportbl(reportnr:int):
    avail_parameters = False
    t_brief_data = []
    brief = parameters = None

    t_brief = None

    t_brief_data, T_brief = create_model_like(Brief)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_parameters, t_brief_data, brief, parameters
        nonlocal reportnr


        nonlocal t_brief
        nonlocal t_brief_data

        return {"avail_parameters": avail_parameters, "t-brief": t_brief_data}

    brief = get_cache (Brief, {"briefnr": [(eq, reportnr)]})
    t_brief = T_brief()
    t_brief_data.append(t_brief)

    buffer_copy(brief, t_brief)

    parameters = get_cache (Parameters, {"progname": [(eq, "gl-macro")],"section": [(eq, to_string(reportnr))]})

    if parameters:
        avail_parameters = True

    return generate_output()