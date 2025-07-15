from functions.additional_functions import *
import decimal
from functions.htpint import htpint
from models import Guest, Artikel, Debitor, Htparam

def mk_resline_chg_gname_1bl(pvilanguage:int, guestnr:int, gastnr:int):
    guestname = ""
    ind_flag = False
    msg_str = ""
    t_guest_list = []
    ind_gastnr:int = 0
    wig_gastnr:int = 0
    outstand:decimal = to_decimal("0.0")
    guest_kreditlimit:decimal = to_decimal("0.0")
    enter_passwd1:bool = False
    enter_passwd2:bool = False
    htparam_fchar1:str = ""
    lvcarea:str = "mk-resline"
    guest = artikel = debitor = htparam = None

    t_guest = None

    t_guest_list, T_guest = create_model_like(Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guestname, ind_flag, msg_str, t_guest_list, ind_gastnr, wig_gastnr, outstand, guest_kreditlimit, enter_passwd1, enter_passwd2, htparam_fchar1, lvcarea, guest, artikel, debitor, htparam
        nonlocal pvilanguage, guestnr, gastnr


        nonlocal t_guest
        nonlocal t_guest_list
        return {"guestname": guestname, "ind_flag": ind_flag, "msg_str": msg_str, "t-guest": t_guest_list}

    guest = db_session.query(Guest).filter(
             (Guest.gastnr == guestnr)).first()
    guestname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

    if guest.kreditlimit > 0:

        debitor_obj_list = []
        for debitor, artikel in db_session.query(Debitor, Artikel).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).filter(
                 (Debitor.gastnr == guest.gastnr) & (Debitor.opart <= 1)).order_by(Debitor._recid).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)


            outstand =  to_decimal(outstand) + to_decimal(debitor.saldo)

        if outstand > guest.kreditlimit:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 320)).first()

            if htparam.flogical:
                msg_str = msg_str + chr(2) + "&M" + translateExtended ("Over Credit Limit:", lvcarea, "") + " " + trim(to_string(outstand, "->,>>>,>>>,>>>,>>9")) + trim(to_string(guest.kreditlimit, "->>>,>>>,>>>,>>9"))

                htparam = db_session.query(Htparam).filter(
                         (Htparam.paramnr == 141)).first()

                if htparam.fchar != "":
                    enter_passwd2 = True
                    htparam_fchar1 = htparam.fchar
                    guest_kreditlimit =  to_decimal(guest.kreditlimit)

    guest = db_session.query(Guest).filter(
             (Guest.gastnr == gastnr)).first()
    t_guest = T_guest()
    t_guest_list.append(t_guest)

    buffer_copy(guest, t_guest)
    wig_gastnr = get_output(htpint(109))
    ind_gastnr = get_output(htpint(123))

    if (guest.gastnr == wig_gastnr) or (guest.gastnr == ind_gastnr):
        ind_flag = True

    return generate_output()