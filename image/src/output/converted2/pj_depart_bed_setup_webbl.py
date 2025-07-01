#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.read_paramtextbl import read_paramtextbl
from models import Paramtext

def pj_depart_bed_setup_webbl():
    setup_list_list = []
    p_text:string = ""
    paramtext = None

    t_paramtext = setup_list = None

    t_paramtext_list, T_paramtext = create_model_like(Paramtext)
    setup_list_list, Setup_list = create_model("Setup_list", {"nr":int, "char":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal setup_list_list, p_text, paramtext


        nonlocal t_paramtext, setup_list
        nonlocal t_paramtext_list, setup_list_list

        return {"setup-list": setup_list_list}

    setup_list = Setup_list()
    setup_list_list.append(setup_list)

    setup_list.nr = 1
    setup_list.char = " "
    p_text, t_paramtext_list = get_output(read_paramtextbl(3, 9201))

    for t_paramtext in query(t_paramtext_list):
        setup_list = Setup_list()
        setup_list_list.append(setup_list)

        setup_list.nr = t_paramtext.txtnr - 9199
        setup_list.char = substring(t_paramtext.notes, 0, 1)

    return generate_output()