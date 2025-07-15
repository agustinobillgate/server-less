#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Hoteldpt, H_umsatz, Fbstat

def correct_cover_deptbl(dept1:int, datum:date):

    prepare_cache ([Hoteldpt, H_umsatz, Fbstat])

    dept = 0
    deptname = ""
    fpax = 0
    bpax = 0
    pax = 0
    orig_fpax = 0
    orig_bpax = 0
    orig_pax = 0
    avail_h_umsatz = False
    cover:int = 0
    hoteldpt = h_umsatz = fbstat = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal dept, deptname, fpax, bpax, pax, orig_fpax, orig_bpax, orig_pax, avail_h_umsatz, cover, hoteldpt, h_umsatz, fbstat
        nonlocal dept1, datum

        return {"dept": dept, "deptname": deptname, "fpax": fpax, "bpax": bpax, "pax": pax, "orig_fpax": orig_fpax, "orig_bpax": orig_bpax, "orig_pax": orig_pax, "avail_h_umsatz": avail_h_umsatz}


    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept1)]})

    if hoteldpt:
        dept = dept1
        deptname = hoteldpt.depart


    fpax = 0
    bpax = 0
    pax = 0
    orig_fpax = 0
    orig_bpax = 0
    orig_pax = 0

    h_umsatz = get_cache (H_umsatz, {"datum": [(eq, datum)],"departement": [(eq, dept)],"betriebsnr": [(eq, dept)]})

    if h_umsatz:
        avail_h_umsatz = True

        for fbstat in db_session.query(Fbstat).filter(
                 (Fbstat.datum == datum) & (Fbstat.departement == dept)).order_by(Fbstat._recid).all():
            cover = cover + fbstat.food_wpax[0] + fbstat.food_wpax[1] + fbstat.food_wpax[2] + fbstat.food_wpax[3] + fbstat.bev_wpax[0] + fbstat.bev_wpax[1] + fbstat.bev_wpax[2] + fbstat.bev_wpax[3] + fbstat.other_wpax[0] + fbstat.other_wpax[1] + fbstat.other_wpax[2] + fbstat.other_wpax[3]
        pax = cover
        fpax = h_umsatz.betrag
        bpax = h_umsatz.nettobetrag
        orig_fpax = fpax
        orig_bpax = bpax
        orig_pax = pax

    return generate_output()