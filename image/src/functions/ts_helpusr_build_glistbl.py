from functions.additional_functions import *
import decimal
from models import Htparam, Kellner

def ts_helpusr_build_glistbl(dept:int):
    curr_num = 0
    max_gpos = 0
    p1079 = False
    grp_list_list = []
    htparam = kellner = None

    grp_list = None

    grp_list_list, Grp_list = create_model("Grp_list", {"pos":int, "num":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_num, max_gpos, p1079, grp_list_list, htparam, kellner


        nonlocal grp_list
        nonlocal grp_list_list
        return {"curr_num": curr_num, "max_gpos": max_gpos, "p1079": p1079, "grp-list": grp_list_list}

    def build_glist():

        nonlocal curr_num, max_gpos, p1079, grp_list_list, htparam, kellner


        nonlocal grp_list
        nonlocal grp_list_list

        i:int = 0

        for kellner in db_session.query(Kellner).filter(
                (Kellner.departement == dept)).all():
            i = i + 1
            grp_list = Grp_list()
            grp_list_list.append(grp_list)

            grp_list.pos = i
            grp_list.num = kellner_nr
            grp_list.bezeich = kellnername

            if i == 1:
                curr_num = kellner_nr
        max_gpos = i


    build_glist()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1079)).first()
    p1079 = htparam.flogical

    return generate_output()