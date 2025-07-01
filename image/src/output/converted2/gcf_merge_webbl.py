#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.read_mc_guestbl import read_mc_guestbl
from functions.read_cl_memberbl import read_cl_memberbl
from functions.read_bk_veranbl import read_bk_veranbl
from functions.read_guest_prbl import read_guest_prbl
from functions.gcf_mergebl import gcf_mergebl
from models import Mc_guest, Cl_member, Bk_veran, Guest_pr

tlist_list, Tlist = create_model("Tlist", {"gastno":int})

def gcf_merge_webbl(pvilanguage:int, userinit:string, bgastno:int, tlist_list:[Tlist]):
    success_flag = False
    msg_str = ""
    doit:bool = False
    flag1:bool = False
    flag2:bool = False
    lvcarea:string = "gcf-merge-web"
    mc_guest = cl_member = bk_veran = guest_pr = None

    tlist = t_mc_guest = t_cl_member = t_bk_veran = t_guest_pr = None

    t_mc_guest_list, T_mc_guest = create_model_like(Mc_guest)
    t_cl_member_list, T_cl_member = create_model_like(Cl_member)
    t_bk_veran_list, T_bk_veran = create_model_like(Bk_veran)
    t_guest_pr_list, T_guest_pr = create_model_like(Guest_pr)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, msg_str, doit, flag1, flag2, lvcarea, mc_guest, cl_member, bk_veran, guest_pr
        nonlocal pvilanguage, userinit, bgastno


        nonlocal tlist, t_mc_guest, t_cl_member, t_bk_veran, t_guest_pr
        nonlocal t_mc_guest_list, t_cl_member_list, t_bk_veran_list, t_guest_pr_list

        return {"success_flag": success_flag, "msg_str": msg_str}

    for tlist in query(tlist_list):
        doit = True


        t_mc_guest_list = get_output(read_mc_guestbl(1, tlist.gastno, ""))

        t_mc_guest = query(t_mc_guest_list, first=True)

        if t_mc_guest:
            doit = False
            msg_str = translateExtended ("Merging not for t-guest with active membership card.", lvcarea, "")

        if doit:
            t_cl_member_list = get_output(read_cl_memberbl(1, tlist.gastno))

            t_cl_member = query(t_cl_member_list, first=True)

            if t_cl_member:
                doit = False
                msg_str = translateExtended ("Merging not for club member.", lvcarea, "")

        if doit:
            t_bk_veran_list = get_output(read_bk_veranbl(1, tlist.gastno, 5, None, None))

            t_bk_veran = query(t_bk_veran_list, first=True)

            if t_bk_veran:
                doit = False
                msg_str = translateExtended ("Merging not allowed: Active banquet reservation exists.", lvcarea, "")

        if doit:
            t_guest_pr_list = get_output(read_guest_prbl(1, tlist.gastno, ""))

            t_guest_pr = query(t_guest_pr_list, first=True)
            flag1 = None != t_guest_pr
            t_guest_pr_list = get_output(read_guest_prbl(1, bgastno, ""))

            t_guest_pr = query(t_guest_pr_list, first=True)
            flag2 = None != t_guest_pr

            if flag1 and flag2:
                doit = False
                msg_str = translateExtended ("Contract rates exists, Can not merge the cards.", lvcarea, "")

        if doit == False:
            break

        if doit:
            get_output(gcf_mergebl(userinit, tlist.gastno, bgastno, flag1, flag2))
            success_flag = True

    return generate_output()