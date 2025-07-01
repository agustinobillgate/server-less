#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.htpint import htpint
from functions.black_vip_listbl import black_vip_listbl
from models import Guest, Master, Htparam

def mk_resline_entry_guestnamebl(pvilanguage:int, gastno:int, gcfmember:int, reslin_list_active_flag:int, master_exist:bool):

    prepare_cache ([Guest])

    guestname = ""
    msg_str = ""
    msg_str1 = ""
    answer = False
    ind_gastnr:int = 0
    wig_gastnr:int = 0
    lvcarea:string = "mk-resline"
    guest = master = htparam = None

    member1 = mbuff = None

    Member1 = create_buffer("Member1",Guest)
    Mbuff = create_buffer("Mbuff",Master)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guestname, msg_str, msg_str1, answer, ind_gastnr, wig_gastnr, lvcarea, guest, master, htparam
        nonlocal pvilanguage, gastno, gcfmember, reslin_list_active_flag, master_exist
        nonlocal member1, mbuff


        nonlocal member1, mbuff

        return {"guestname": guestname, "msg_str": msg_str, "msg_str1": msg_str1, "answer": answer}

    wig_gastnr = get_output(htpint(109))
    ind_gastnr = get_output(htpint(123))

    member1 = get_cache (Guest, {"gastnr": [(eq, gcfmember)]})
    guestname = member1.name + ", " + member1.vorname1 + " " + member1.anrede1

    if member1.karteityp == 0:
        msg_str = get_output(black_vip_listbl(pvilanguage, gcfmember))

    if (gastno == wig_gastnr) or (gastno == ind_gastnr):
        answer = True
    else:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 76)]})

        if htparam.flogical or master_exist:
            msg_str1 = "&Q" + translateExtended ("Use the same guest name for Bill Receiver?", lvcarea, "")

    return generate_output()