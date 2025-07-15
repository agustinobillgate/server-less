#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.read_mc_guestbl import read_mc_guestbl
from functions.read_cl_memberbl import read_cl_memberbl
from functions.read_bk_veranbl import read_bk_veranbl
from functions.read_guestbl import read_guestbl
from functions.read_guest_prbl import read_guest_prbl
from functions.read_res_linebl import read_res_linebl
from functions.gcf_mergebl import gcf_mergebl
from models import Mc_guest, Cl_member, Bk_veran, Guest, Guest_pr, Res_line

def merged_guestbl(t_gastnr:int, s_gastnr:int, tg_karteityp:int, user_init:string):
    mess_str = ""
    answer:bool = False
    flag1:bool = False
    flag2:bool = False
    mc_guest = cl_member = bk_veran = guest = guest_pr = res_line = None

    t_mc_guest = t_cl_member = t_bk_veran = gast = t_guest_pr = t_res_line = None

    t_mc_guest_data, T_mc_guest = create_model_like(Mc_guest)
    t_cl_member_data, T_cl_member = create_model_like(Cl_member)
    t_bk_veran_data, T_bk_veran = create_model_like(Bk_veran)
    gast_data, Gast = create_model_like(Guest)
    t_guest_pr_data, T_guest_pr = create_model_like(Guest_pr)
    t_res_line_data, T_res_line = create_model_like(Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_str, answer, flag1, flag2, mc_guest, cl_member, bk_veran, guest, guest_pr, res_line
        nonlocal t_gastnr, s_gastnr, tg_karteityp, user_init


        nonlocal t_mc_guest, t_cl_member, t_bk_veran, gast, t_guest_pr, t_res_line
        nonlocal t_mc_guest_data, t_cl_member_data, t_bk_veran_data, gast_data, t_guest_pr_data, t_res_line_data

        return {"mess_str": mess_str}

    t_mc_guest_data = get_output(read_mc_guestbl(1, t_gastnr, ""))

    t_mc_guest = query(t_mc_guest_data, first=True)

    if t_mc_guest:
        mess_str = "Merging not for t-guest with active membership card."

        return generate_output()
    t_cl_member_data = get_output(read_cl_memberbl(1, t_gastnr))

    t_cl_member = query(t_cl_member_data, first=True)

    if t_cl_member:
        mess_str = "Merging not for club member."

        return generate_output()
    t_bk_veran_data = get_output(read_bk_veranbl(1, t_gastnr, 5, None, None))

    t_bk_veran = query(t_bk_veran_data, first=True)

    if t_bk_veran:
        mess_str = "Merging not allowed: Active banquet reservation exists."

        return generate_output()

    if s_gastnr > 0:

        if s_gastnr == t_gastnr:
            mess_str = "The selected t-guest cards must be different to the first."

            return generate_output()
        gast_data = get_output(read_guestbl(1, s_gastnr, "", ""))

        gast = query(gast_data, first=True)

        if gast.karteityp != tg_karteityp:
            mess_str = "The selected t-guest Card Type must have the same."

            return generate_output()
        t_guest_pr_data = get_output(read_guest_prbl(1, t_gastnr, ""))

        t_guest_pr = query(t_guest_pr_data, first=True)
        flag1 = None != t_guest_pr
        t_guest_pr_data = get_output(read_guest_prbl(1, s_gastnr, ""))

        t_guest_pr = query(t_guest_pr_data, first=True)
        flag2 = None != t_guest_pr

        if flag1 and flag2:
            mess_str = "Contract rates exists, Can not merge the cards."

            return generate_output()
        t_res_line_data = get_output(read_res_linebl(18, None, None, None, None, "", None, None, t_gastnr, None, ""))

        t_res_line = query(t_res_line_data, first=True)

        if t_res_line:
            mess_str = "GCF to be merged still has active reservation(s)!"

            return generate_output()
        get_output(gcf_mergebl(user_init, t_gastnr, s_gastnr, flag1, flag2))
        mess_str = "Merged Successfull"

    return generate_output()