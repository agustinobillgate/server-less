#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Kellner

def ts_helpusr_build_glistbl(dept:int):

    prepare_cache ([Htparam, Kellner])

    curr_num = 0
    max_gpos = 0
    p1079 = False
    grp_list_data = []
    htparam = kellner = None

    grp_list = None

    grp_list_data, Grp_list = create_model("Grp_list", {"pos":int, "num":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_num, max_gpos, p1079, grp_list_data, htparam, kellner
        nonlocal dept


        nonlocal grp_list
        nonlocal grp_list_data

        return {"curr_num": curr_num, "max_gpos": max_gpos, "p1079": p1079, "grp-list": grp_list_data}

    def build_glist():

        nonlocal curr_num, max_gpos, p1079, grp_list_data, htparam, kellner
        nonlocal dept


        nonlocal grp_list
        nonlocal grp_list_data

        i:int = 0

        for kellner in db_session.query(Kellner).filter(
                 (Kellner.departement == dept)).order_by(Kellner.kellnername).all():
            i = i + 1
            grp_list = Grp_list()
            grp_list_data.append(grp_list)

            grp_list.pos = i
            grp_list.num = kellner.kellner_nr
            grp_list.bezeich = kellner.kellnername

            if i == 1:
                curr_num = kellner.kellner_nr
        max_gpos = i

    build_glist()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1079)]})
    p1079 = htparam.flogical

    return generate_output()