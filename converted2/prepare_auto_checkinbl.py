#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Reservation, Guest, Artikel, Debitor, Htparam, Res_line

def prepare_auto_checkinbl(pvilanguage:int, resnr:int):

    prepare_cache ([Reservation, Guest, Debitor, Htparam, Res_line])

    f_tittle = ""
    msg_str = ""
    msg_str1 = ""
    f_char = ""
    guest_gastnr = 0
    guest_kreditlimit = to_decimal("0.0")
    outstand = to_decimal("0.0")
    f_logical = False
    res_list_data = []
    lvcarea:string = "prepare-auto-checkin"
    ci_date:date = None
    reservation = guest = artikel = debitor = htparam = res_line = None

    res_list = None

    res_list_data, Res_list = create_model("Res_list", {"gastnr":int, "zinr":string, "name":string, "resnr":int, "reslinnr":int, "activeflag":int, "resstatus":int, "sysdate":date, "zeit":int, "selflag":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_tittle, msg_str, msg_str1, f_char, guest_gastnr, guest_kreditlimit, outstand, f_logical, res_list_data, lvcarea, ci_date, reservation, guest, artikel, debitor, htparam, res_line
        nonlocal pvilanguage, resnr


        nonlocal res_list
        nonlocal res_list_data

        return {"f_tittle": f_tittle, "msg_str": msg_str, "msg_str1": msg_str1, "f_char": f_char, "guest_gastnr": guest_gastnr, "guest_kreditlimit": guest_kreditlimit, "outstand": outstand, "f_logical": f_logical, "res-list": res_list_data}

    def create_list():

        nonlocal f_tittle, msg_str, msg_str1, f_char, guest_gastnr, guest_kreditlimit, outstand, f_logical, res_list_data, lvcarea, ci_date, reservation, guest, artikel, debitor, htparam, res_line
        nonlocal pvilanguage, resnr


        nonlocal res_list
        nonlocal res_list_data

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == resnr) & (Res_line.active_flag == 0) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.ankunft == ci_date)).order_by(Res_line.zinr, Res_line.resstatus).all():
            res_list = Res_list()
            res_list_data.append(res_list)

            res_list.gastnr = res_line.gastnr
            res_list.name = res_line.name
            res_list.zinr = res_line.zinr
            res_list.resnr = res_line.resnr
            res_list.reslinnr = res_line.reslinnr
            res_list.activeflag = res_line.active_flag
            res_list.resstatus = res_line.resstatus
            res_list.sysdate = get_current_date()
            res_list.zeit = get_current_time_in_seconds()


    reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})

    if (reservation.depositgef - reservation.depositbez - reservation.depositbez2) > 0:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Deposit not yet settled, check-in not possible", lvcarea, "")

        return generate_output()

    guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

    if guest.karteityp >= 1 and guest.kreditlimit > 0 and guest.zahlungsart > 0:
        outstand =  to_decimal("0")

        debitor_obj_list = {}
        for debitor, artikel in db_session.query(Debitor, Artikel).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).filter(
                 (Debitor.gastnr == guest.gastnr) & (Debitor.opart <= 1)).order_by(Debitor._recid).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True


            outstand =  to_decimal(outstand) + to_decimal(debitor.saldo)

        if outstand > guest.kreditlimit:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 320)]})

            if htparam.flogical:
                f_logical = True
                msg_str1 = msg_str1 + chr_unicode(2) + translateExtended ("Credit Limit overdrawn: ", lvcarea, "") + trim(to_string(outstand, "->,>>>,>>>,>>>,>>9")) + trim(to_string(guest.kreditlimit, "->>>,>>>,>>>,>>9"))

                htparam = get_cache (Htparam, {"paramnr": [(eq, 141)]})
                f_char = htparam.fchar

                if htparam.fchar != "":
                    guest_gastnr = guest.gastnr
                    guest_kreditlimit =  to_decimal(guest.kreditlimit)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})
    f_tittle = translateExtended ("Automatic Checkin for :", lvcarea, "") + reservation.name
    create_list()

    return generate_output()