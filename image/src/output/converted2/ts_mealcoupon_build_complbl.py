#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel

def ts_mealcoupon_build_complbl(dept:int):

    prepare_cache ([H_artikel])

    max_gpos = 0
    grp_compl_list = []
    curr_num:int = 0
    h_artikel = None

    grp_compl = None

    grp_compl_list, Grp_compl = create_model("Grp_compl", {"pos":int, "num":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal max_gpos, grp_compl_list, curr_num, h_artikel
        nonlocal dept


        nonlocal grp_compl
        nonlocal grp_compl_list

        return {"max_gpos": max_gpos, "grp-compl": grp_compl_list}

    def build_compl():

        nonlocal max_gpos, grp_compl_list, curr_num, h_artikel
        nonlocal dept


        nonlocal grp_compl
        nonlocal grp_compl_list

        i:int = 0

        for h_artikel in db_session.query(H_artikel).filter(
                 (H_artikel.departement == dept) & (H_artikel.artart == 12) & (H_artikel.activeflag)).order_by(H_artikel.bezeich).all():
            i = i + 1
            grp_compl = Grp_compl()
            grp_compl_list.append(grp_compl)

            grp_compl.pos = i
            grp_compl.num = h_artikel.artnr
            grp_compl.bezeich = h_artikel.bezeich

            if i == 1:
                curr_num = h_artikel.artnr
        max_gpos = i

    build_compl()

    return generate_output()