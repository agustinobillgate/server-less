# using conversion tools version: 1.0.0.119
"""_yusufwijasena_05/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix python indentation
                    - convert only
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Artikel, Billjournal


def leasing_get_payment_listbl(resno: int):

    prepare_cache([Htparam, Artikel, Billjournal])

    tlist_data = []
    ar_ledger: int = 0
    htparam = artikel = billjournal = None

    tlist = None

    tlist_data, Tlist = create_model(
        "Tlist",
        {
            "artnr": int,
            "art_bez": str,
            "bezeich": str,
            "amount": Decimal,
            "pay_date": date,
            "pay_time": str,
            "rec_id": int,
            "resno": int,
            "art_select": bool,
            "cicilanke": int
        })

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tlist_data, ar_ledger, htparam, artikel, billjournal
        nonlocal resno
        nonlocal tlist
        nonlocal tlist_data

        return {
            "tlist": tlist_data
        }

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 1051)]})

    if htparam:
        ar_ledger = htparam.finteger

    billjournal_obj_list = {}
    billjournal = Billjournal()
    artikel = Artikel()
    for billjournal.artnr, billjournal.bezeich, billjournal.betrag, billjournal.bill_datum, billjournal.zeit, billjournal._recid, billjournal.billin_nr, artikel.bezeich, artikel._recid in db_session.query(Billjournal.artnr, Billjournal.bezeich, Billjournal.betrag, Billjournal.bill_datum, Billjournal.zeit, Billjournal._recid, Billjournal.billin_nr, Artikel.bezeich, Artikel._recid).join(Artikel, (Artikel.artnr == Billjournal.artnr) & (Artikel.departement == Billjournal.departement)).filter(
            (matches(Billjournal.bezeich, "*Payment Leasing #*")) & (Billjournal.betrag < 0) & (Billjournal.artnr != ar_ledger)).order_by(Billjournal._recid).all():
        if billjournal_obj_list.get(billjournal._recid):
            continue
        else:
            billjournal_obj_list[billjournal._recid] = True

        if num_entries(billjournal.bezeich, "#") > 0 and entry(1, billjournal.bezeich, "#") == to_string(resno) + "]":
            tlist = Tlist()
            tlist_data.append(tlist)

            tlist.artnr = billjournal.artnr
            tlist.art_bez = artikel.bezeich
            tlist.bezeich = billjournal.bezeich
            tlist.amount = to_decimal(billjournal.betrag)
            tlist.pay_date = billjournal.bill_datum
            tlist.pay_time = to_string(billjournal.zeit)
            tlist.rec_id = billjournal._recid
            tlist.resno = resno
            tlist.cicilanke = billjournal.billin_nr

    for billjournal in db_session.query(Billjournal).filter(
            (matches(Billjournal.bezeich, "*Cancel Payment Leasing #*")) & (Billjournal.betrag > 0) & (Billjournal.artnr != ar_ledger)).order_by(Billjournal._recid).all():

        if num_entries(billjournal.bezeich, "#") > 0 and entry(1, billjournal.bezeich, "#") == to_string(resno) + "]":
            tlist = query(tlist_data, filters=(lambda tlist: tlist.artnr == billjournal.artnr and tlist.cicilanKe == billjournal.billin_nr and tlist.amount == - billjournal.betrag), first=True)

            if tlist:
                tlist.amount = to_decimal(tlist.amount + billjournal.betrag)

    for tlist in query(tlist_data, filters=(lambda tlist: tlist.amount == 0)):
        tlist_data.remove(tlist)

    return generate_output()
