#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Guest, Artikel, Debitor, Segment, Guestseg, Htparam

def mkres_gname_btn_nextbl(inp_gastnr:int):

    prepare_cache ([Guest, Debitor, Segment, Htparam])

    error_code = 0
    blacklist_code = ""
    block_rsv = False
    pswd_str = ""
    cr_limit = to_decimal("0.0")
    outstand = to_decimal("0.0")
    ratecode_exist:bool = False
    bill_date:date = None
    guest = artikel = debitor = segment = guestseg = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_code, blacklist_code, block_rsv, pswd_str, cr_limit, outstand, ratecode_exist, bill_date, guest, artikel, debitor, segment, guestseg, htparam
        nonlocal inp_gastnr

        return {"error_code": error_code, "blacklist_code": blacklist_code, "block_rsv": block_rsv, "pswd_str": pswd_str, "cr_limit": cr_limit, "outstand": outstand}

    bill_date = get_output(htpdate(110))

    guest = get_cache (Guest, {"gastnr": [(eq, inp_gastnr)]})
    cr_limit =  to_decimal(guest.kreditlimit)

    if guest.karteityp >= 1 and guest.zahlungsart > 0:

        debitor_obj_list = {}
        for debitor, artikel in db_session.query(Debitor, Artikel).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & ((Artikel.artart == 2) | (Artikel.artart == 7))).filter(
                 (Debitor.gastnr == guest.gastnr) & (Debitor.opart <= 1)).order_by(Debitor._recid).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True


            outstand =  to_decimal(outstand) + to_decimal(debitor.saldo)


    guestseg_obj_list = {}
    for guestseg, segment in db_session.query(Guestseg, Segment).join(Segment,(Segment.segmentcode == Guestseg.segmentcode) & (Segment.betriebsnr == 4)).filter(
             (Guestseg.gastnr == inp_gastnr)).order_by(Guestseg._recid).yield_per(100):
        if guestseg_obj_list.get(guestseg._recid):
            continue
        else:
            guestseg_obj_list[guestseg._recid] = True


        error_code = 1
        blacklist_code = entry(0, segment.bezeich, "$$0")


        break

    if outstand > guest.kreditlimit and guest.kreditlimit > 0:
        error_code = error_code + 2

    htparam = get_cache (Htparam, {"paramnr": [(eq, 320)]})
    block_rsv = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 141)]})
    pswd_str = htparam.fchar

    return generate_output()