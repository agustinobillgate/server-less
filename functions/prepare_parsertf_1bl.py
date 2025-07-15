#using conversion tools version: 1.0.0.105

from functions.additional_functions import *
from decimal import Decimal
from functions.htpchar import htpchar
from models import Res_line, Reservation, Guest, Bill, Akt_kont, Zimkateg, Htparam, Bediener, Brief, Arrangement

def prepare_parsertf_1bl(user_init:string, gastnr:int, resnr:int, reslinnr:int, briefnr:int, rechnr:int):

    prepare_cache ([Res_line, Htparam, Brief, Arrangement])

    gastnr_ind = 0
    gastnr_wi = 0
    f_gastnr = False
    f_resnr = False
    f_resline = False
    f_bill = False
    infile = ""
    outfile = ""
    keychar = ""
    p_400 = ""
    p_405 = ""
    htp_list_list = []
    t_res_line_list = []
    t_reservation_list = []
    t_guest_list = []
    t_bill_list = []
    t_akt_kont_list = []
    t_zimkateg_list = []
    res_line = reservation = guest = bill = akt_kont = zimkateg = htparam = bediener = brief = arrangement = None

    t_res_line = t_reservation = t_guest = t_bill = t_akt_kont = t_zimkateg = htp_list = gmember = resbuff = None

    t_res_line_list, T_res_line = create_model_like(Res_line, {"argt_bezeich":string})
    t_reservation_list, T_reservation = create_model_like(Reservation)
    t_guest_list, T_guest = create_model_like(Guest)
    t_bill_list, T_bill = create_model_like(Bill)
    t_akt_kont_list, T_akt_kont = create_model_like(Akt_kont)
    t_zimkateg_list, T_zimkateg = create_model_like(Zimkateg)
    htp_list_list, Htp_list = create_model("Htp_list", {"paramnr":int, "fchar":string})

    Gmember = create_buffer("Gmember",Guest)
    Resbuff = create_buffer("Resbuff",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gastnr_ind, gastnr_wi, f_gastnr, f_resnr, f_resline, f_bill, infile, outfile, keychar, p_400, p_405, htp_list_list, t_res_line_list, t_reservation_list, t_guest_list, t_bill_list, t_akt_kont_list, t_zimkateg_list, res_line, reservation, guest, bill, akt_kont, zimkateg, htparam, bediener, brief, arrangement
        nonlocal user_init, gastnr, resnr, reslinnr, briefnr, rechnr
        nonlocal gmember, resbuff


        nonlocal t_res_line, t_reservation, t_guest, t_bill, t_akt_kont, t_zimkateg, htp_list, gmember, resbuff
        nonlocal t_res_line_list, t_reservation_list, t_guest_list, t_bill_list, t_akt_kont_list, t_zimkateg_list, htp_list_list

        return {"gastnr_ind": gastnr_ind, "gastnr_wi": gastnr_wi, "f_gastnr": f_gastnr, "f_resnr": f_resnr, "f_resline": f_resline, "f_bill": f_bill, "infile": infile, "outfile": outfile, "keychar": keychar, "p_400": p_400, "p_405": p_405, "htp-list": htp_list_list, "t-res-line": t_res_line_list, "t-reservation": t_reservation_list, "t-guest": t_guest_list, "t-bill": t_bill_list, "t-akt-kont": t_akt_kont_list, "t-zimkateg": t_zimkateg_list}

    def fill_list():

        nonlocal gastnr_ind, gastnr_wi, f_gastnr, f_resnr, f_resline, f_bill, infile, outfile, keychar, p_400, p_405, htp_list_list, t_res_line_list, t_reservation_list, t_guest_list, t_bill_list, t_akt_kont_list, t_zimkateg_list, res_line, reservation, guest, bill, akt_kont, zimkateg, htparam, bediener, brief, arrangement
        nonlocal user_init, gastnr, resnr, reslinnr, briefnr, rechnr
        nonlocal gmember, resbuff


        nonlocal t_res_line, t_reservation, t_guest, t_bill, t_akt_kont, t_zimkateg, htp_list, gmember, resbuff
        nonlocal t_res_line_list, t_reservation_list, t_guest_list, t_bill_list, t_akt_kont_list, t_zimkateg_list, htp_list_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 600)]})
        keychar = htparam.fchar

        for htparam in db_session.query(Htparam).filter(
                 (Htparam.paramgruppe == 17)).order_by(length(Htparam.fchar).desc()).all():
            htp_list = Htp_list()
            htp_list_list.append(htp_list)

            htp_list.paramnr = htparam.paramnr
            htp_list.fchar = keychar + htparam.fchar

    p_400 = get_output(htpchar(400))
    p_405 = get_output(htpchar(405))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 109)]})
    gastnr_wi = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 123)]})
    gastnr_ind = htparam.finteger

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

    if guest:
        f_gastnr = True

    reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})

    if reservation:
        f_resnr = True
        t_reservation = T_reservation()
        t_reservation_list.append(t_reservation)

        buffer_copy(reservation, t_reservation)

    if reslinnr > 0:

        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"resstatus": [(le, 6)]})

    if res_line:

        gmember = db_session.query(Gmember).filter(
                 (Gmember.gastnr == res_line.gastnrmember)).first()
        f_resline = True

        for resbuff in db_session.query(Resbuff).filter(
                 (Resbuff.resnr == resnr)).order_by(Resbuff._recid).all():

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, resbuff.zikatnr)]})

            if zimkateg:

                t_zimkateg = query(t_zimkateg_list, filters=(lambda t_zimkateg: t_zimkateg.zikatnr == zimkateg.zikatnr), first=True)

                if not t_zimkateg:
                    t_zimkateg = T_zimkateg()
                    t_zimkateg_list.append(t_zimkateg)

                    buffer_copy(zimkateg, t_zimkateg)

    bill = get_cache (Bill, {"rechnr": [(eq, rechnr)]})

    if bill:
        f_bill = True
        t_bill = T_bill()
        t_bill_list.append(t_bill)

        buffer_copy(bill, t_bill)

    brief = get_cache (Brief, {"briefnr": [(eq, briefnr)]})
    infile = entry(0, brief.fname, ";")
    outfile = "CONF" + to_string(resnr) + ".rtf"

    htparam = get_cache (Htparam, {"paramnr": [(eq, 430)]})

    if htparam.fchar != "":

        if substring(htparam.fchar, length(htparam.fchar) - 1, 1) != ("\\").lower()  and substring(htparam.fchar, length(htparam.fchar) - 1, 1) != ("/").lower() :
            outfile = htparam.fchar + "\\" + outfile
        else:
            outfile = htparam.fchar + outfile
    else:
        outfile = ".\\" + outfile

    for res_line in db_session.query(Res_line).filter(
             (Res_line.resnr == resnr) & ((Res_line.resstatus <= 6) | (Res_line.resstatus == 11) | (Res_line.resstatus == 13))).order_by(Res_line._recid).all():
        t_res_line = T_res_line()
        t_res_line_list.append(t_res_line)

        buffer_copy(res_line, t_res_line)

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

        if arrangement:
            t_res_line.argt_bezeich = arrangement.argt_bez

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

        t_guest = query(t_guest_list, filters=(lambda t_guest: t_guest.gastnr == guest.gastnr), first=True)

        if not t_guest:
            t_guest = T_guest()
            t_guest_list.append(t_guest)

            buffer_copy(guest, t_guest)

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        t_guest = query(t_guest_list, filters=(lambda t_guest: t_guest.gastnr == guest.gastnr), first=True)

        if not t_guest:
            t_guest = T_guest()
            t_guest_list.append(t_guest)

            buffer_copy(guest, t_guest)

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})

        t_guest = query(t_guest_list, filters=(lambda t_guest: t_guest.gastnr == guest.gastnr), first=True)

        if not t_guest:
            t_guest = T_guest()
            t_guest_list.append(t_guest)

            buffer_copy(guest, t_guest)

    for t_guest in query(t_guest_list):

        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, t_guest.gastnr)],"hauptkontakt": [(eq, True)]})

        if akt_kont:
            t_akt_kont = T_akt_kont()
            t_akt_kont_list.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    fill_list()

    return generate_output()