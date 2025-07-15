#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.read_paramtextbl import read_paramtextbl
from models import Paramtext

def pj_depart_bed_setup_webbl():
    setup_list_data = []
    p_text:string = ""
    paramtext = None

    t_paramtext = setup_list = None

    t_paramtext_data, T_paramtext = create_model_like(Paramtext)
    setup_list_data, Setup_list = create_model("Setup_list", {"nr":int, "char":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal setup_list_data, p_text, paramtext


        nonlocal t_paramtext, setup_list
        nonlocal t_paramtext_data, setup_list_data

        return {"setup-list": setup_list_data}

    setup_list = Setup_list()
    setup_list_data.append(setup_list)

    setup_list.nr = 1
    setup_list.char = " "
    p_text, t_paramtext_data = get_output(read_paramtextbl(3, 9201))

    for t_paramtext in query(t_paramtext_data):
        setup_list = Setup_list()
        setup_list_data.append(setup_list)

        setup_list.nr = t_paramtext.txtnr - 9199
        setup_list.char = substring(t_paramtext.notes, 0, 1)

    return generate_output()