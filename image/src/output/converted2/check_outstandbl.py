#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Segment, Guestseg, Artikel, Debitor, Htparam

def check_outstandbl(pvilanguage:int, gastnr:int, from_inv:bool):

    prepare_cache ([Guest, Segment, Debitor, Htparam])

    msg_str = ""
    error_flag = True
    pswd_str = ""
    outstand = to_decimal("0.0")
    black_list_flag:bool = False
    lvcarea:string = "reservation"
    guest = segment = guestseg = artikel = debitor = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, error_flag, pswd_str, outstand, black_list_flag, lvcarea, guest, segment, guestseg, artikel, debitor, htparam
        nonlocal pvilanguage, gastnr, from_inv

        return {"msg_str": msg_str, "error_flag": error_flag, "pswd_str": pswd_str, "outstand": outstand}


    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

    guestseg_obj_list = {}
    for guestseg, segment in db_session.query(Guestseg, Segment).join(Segment,(Segment.segmentcode == Guestseg.segmentcode) & (Segment.betriebsnr == 4)).filter(
             (Guestseg.gastnr == guest.gastnr)).order_by(Guestseg._recid).yield_per(100):
        if guestseg_obj_list.get(guestseg._recid):
            continue
        else:
            guestseg_obj_list[guestseg._recid] = True

        if guest.zahlungsart > 0:

            debitor_obj_list = {}
            for debitor, artikel in db_session.query(Debitor, Artikel).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & ((Artikel.artart == 2) | (Artikel.artart == 7))).filter(
                     (Debitor.gastnr == guest.gastnr) & (Debitor.opart <= 1)).order_by(Debitor._recid).all():
                if debitor_obj_list.get(debitor._recid):
                    continue
                else:
                    debitor_obj_list[debitor._recid] = True


                outstand =  to_decimal(outstand) + to_decimal(debitor.saldo)

        black_list_flag = True
        break

    if guest.karteityp >= 1 and guest.kreditlimit > 0 and guest.zahlungsart > 0:

        debitor_obj_list = {}
        for debitor, artikel in db_session.query(Debitor, Artikel).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).filter(
                 (Debitor.gastnr == guest.gastnr) & (Debitor.opart <= 1)).order_by(Debitor._recid).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True


            outstand =  to_decimal(outstand) + to_decimal(debitor.saldo)

        if outstand > guest.kreditlimit:

            if not from_inv:

                if black_list_flag:

                    htparam = get_cache (Htparam, {"paramnr": [(eq, 141)]})

                    if htparam.fchar != "":
                        pswd_str = htparam.fchar
                        msg_str = translateExtended ("Black List:", lvcarea, "") +\
                            " " + entry(0, segment.bezeich, "$$0")


                    else:
                        msg_str = "&Q" + translateExtended ("Black List:", lvcarea, "") + " " + entry(0, segment.bezeich, "$$0") + chr_unicode(10) + translateExtended ("Cancel Booking?", lvcarea, "")
                else:

                    htparam = get_cache (Htparam, {"paramnr": [(eq, 320)]})

                    if htparam.flogical:
                        msg_str = translateExtended ("Credit Limit overdrawn:", lvcarea, "") + " " + trim(to_string(outstand, "->,>>>,>>>,>>>,>>9")) + " >> " + trim(to_string(guest.kreditlimit, "->>>,>>>,>>>,>>9"))

                        htparam = get_cache (Htparam, {"paramnr": [(eq, 141)]})
                        pswd_str = htparam.fchar

                        return generate_output()
                    else:
                        msg_str = "&Q" + translateExtended ("Credit Limit overdrawn:", lvcarea, "") + " " + trim(to_string(outstand, "->,>>>,>>>,>>>,>>9")) + " >> " + trim(to_string(guest.kreditlimit, "->>>,>>>,>>>,>>9")) + chr_unicode(10) + translateExtended ("Cancel creating new reservation?", lvcarea, "")

                        return generate_output()
            else:
                msg_str = translateExtended ("Credit Limit overdrawn:", lvcarea, "") + " " + trim(to_string(outstand, "->,>>>,>>>,>>>,>>9")) + " >> " + trim(to_string(guest.kreditlimit, "->>>,>>>,>>>,>>9"))

                htparam = get_cache (Htparam, {"paramnr": [(eq, 141)]})
                pswd_str = htparam.fchar

                return generate_output()
    error_flag = False

    return generate_output()