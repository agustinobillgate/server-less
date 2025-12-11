# using conversion tools version: 1.0.0.119
"""_yusufwijasena_17/11/2025

    Ticket ID: 20FD2B
        _remark_:   - only converted to python
"""

# ===========================================
# Rulita, 11-12-2025
# - Added with_for_update before delete query
# ===========================================

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill_line, H_artikel, H_bill, H_mjourn


def ts_splitbill_split_bill_webbl(rec_id: int, dept: int, price_decimal: int):

    prepare_cache([H_artikel, H_bill, H_mjourn])

    t_h_bill_line_data = []
    h_bill_line = h_artikel = h_bill = h_mjourn = None

    t_h_bill_line = art_list = h_artikel_buff = None

    t_h_bill_line_data, T_h_bill_line = create_model_like(
        H_bill_line,
        {
            "rec_id": int,
            "menu_flag": int,
            "sub_menu_bezeich": str,
            "sub_menu_betriebsnr": int,
            "sub_menu_qty": int
        })
    art_list_data, Art_list = create_model_like(

        H_bill_line,
        {
            "rec_id": int
        })

    H_artikel_buff = create_buffer("H_artikel_buff", H_artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_bill_line_data, h_bill_line, h_artikel, h_bill, h_mjourn
        nonlocal rec_id, dept, price_decimal
        nonlocal h_artikel_buff
        nonlocal t_h_bill_line, art_list, h_artikel_buff
        nonlocal t_h_bill_line_data, art_list_data

        return {
            "t-h-bill-line": t_h_bill_line_data
        }

    def split_bill():
        nonlocal t_h_bill_line_data, h_bill_line, h_artikel, h_bill, h_mjourn
        nonlocal rec_id, dept, price_decimal
        nonlocal h_artikel_buff
        nonlocal t_h_bill_line, art_list, h_artikel_buff
        nonlocal t_h_bill_line_data, art_list_data

        h_artart: int = 0
        i: int = 0
        amount: Decimal = to_decimal("0.0")
        splitamount: Decimal = to_decimal("0.0")
        pos_anz: int = 0
        rec_id_h_bill_line: int = 0
        h_mjourn_buff = None
        rqst_str: string = ""
        counter: int = 0
        H_mjourn_buff = create_buffer("H_mjourn_buff", H_mjourn)

        for h_bill_line in db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == dept)).order_by(H_bill_line._recid).all():
            if h_bill_line.waehrungsnr != 0:
                continue
            rec_id_h_bill_line = h_bill_line._recid

            if h_bill_line.artnr != 0:
                h_artikel = get_cache(
                    H_artikel, {"artnr": [(eq, h_bill_line.artnr)], "departement": [(eq, h_bill_line.departement)]})

                if h_artikel:
                    h_artart = h_artikel.artart

                    if h_artikel.betriebsnr > 0:
                        continue
            else:
                h_artart = 2

            art_list = query(art_list_data, filters=(lambda art_list: art_list.artnr == h_bill_line.artnr and art_list.departement == h_bill_line.departement and art_list.bezeich == h_bill_line.bezeich and art_list.waehrungsnr == h_bill_line.waehrungsnr and art_list.betriebsnr == h_bill_line.betriebsnr and art_list.rec_id == rec_id_h_bill_line), first=True)

            if not art_list or (art_list and h_artart != 0):
                art_list = Art_list()
                art_list_data.append(art_list)

                art_list.artnr = h_bill_line.artnr
                art_list.departement = h_bill_line.departement
                art_list.bezeich = h_bill_line.bezeich
                art_list.epreis = to_decimal(h_bill_line.epreis)
                art_list.rechnr = h_bill_line.rechnr
                art_list.tischnr = h_bill_line.tischnr
                art_list.zeit = h_bill_line.zeit
                art_list.kellner_nr = h_bill_line.kellner_nr
                art_list.bill_datum = h_bill_line.bill_datum
                art_list.sysdate = h_bill_line.sysdate
                art_list.waehrungsnr = h_bill_line.waehrungsnr
                art_list.betriebsnr = h_bill_line.betriebsnr
                art_list.rec_id = rec_id_h_bill_line

            art_list.anzahl = art_list.anzahl + h_bill_line.anzahl
            art_list.betrag = to_decimal(
                art_list.betrag) + to_decimal(h_bill_line.betrag)
            art_list.nettobetrag = to_decimal(
                art_list.nettobetrag) + to_decimal(h_bill_line.nettobetrag)

        for art_list in query(art_list_data):
            if art_list.anzahl == 0 and round(art_list.betrag, 0) == 0:
                art_list_data.remove(art_list)

        for h_bill_line in db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == dept)).order_by(H_bill_line._recid).with_for_update().all():
            h_artikel = get_cache(
                H_artikel, {"artnr": [(eq, h_bill_line.artnr)], "departement": [(eq, h_bill_line.departement)]})

            if h_artikel:
                if h_artikel.betriebsnr > 0:
                    continue

            if h_bill_line.waehrungsnr != 0:
                continue
            db_session.delete(h_bill_line)

        for art_list in query(art_list_data):
            amount = to_decimal("0")
            pos_anz = art_list.anzahl

            if pos_anz < 0:
                pos_anz = - pos_anz
            splitamount = to_decimal(
                round(art_list.betrag / pos_anz, price_decimal))
            for i in range(1, pos_anz + 1):
                if i < pos_anz:
                    amount = to_decimal(splitamount)
                else:
                    amount = to_decimal(
                        round(art_list.betrag - amount * (pos_anz - 1), price_decimal))
                h_bill_line = H_bill_line()
                db_session.add(h_bill_line)

                h_bill_line.steuercode = 9999
                h_bill_line.artnr = art_list.artnr
                h_bill_line.departement = art_list.departement
                h_bill_line.bezeich = art_list.bezeich
                h_bill_line.rechnr = art_list.rechnr
                h_bill_line.tischnr = art_list.tischnr
                h_bill_line.zeit = art_list.zeit
                h_bill_line.kellner_nr = art_list.kellner_nr
                h_bill_line.epreis = to_decimal(art_list.epreis)
                h_bill_line.betrag = to_decimal(amount)
                h_bill_line.nettobetrag = to_decimal(
                    round(art_list.nettobetrag / art_list.anzahl, price_decimal))
                h_bill_line.bill_datum = art_list.bill_datum
                h_bill_line.sysdate = art_list.sysdate
                h_bill_line.waehrungsnr = art_list.waehrungsnr
                h_bill_line.betriebsnr = art_list.betriebsnr

                if art_list.anzahl > 0:
                    h_bill_line.anzahl = 1
                else:
                    h_bill_line.anzahl = - 1
        art_list_data.clear()

    h_bill = get_cache(H_bill, {"_recid": [(eq, rec_id)]})
    split_bill()

    h_bill_line_obj_list = {}
    for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel, (H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == dept)).filter(
            (H_bill_line.departement == dept) & (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.waehrungsnr == 0)).order_by(H_bill_line.bezeich).all():
        if h_bill_line_obj_list.get(h_bill_line._recid):
            continue
        else:
            h_bill_line_obj_list[h_bill_line._recid] = True

        t_h_bill_line = T_h_bill_line()
        t_h_bill_line_data.append(t_h_bill_line)

        buffer_copy(h_bill_line, t_h_bill_line)
        t_h_bill_line.rec_id = h_bill_line._recid

        t_h_bill_line.menu_flag = 1
        t_h_bill_line.sub_menu_betriebsnr = h_artikel.betriebsnr

        h_mjourn_obj_list = {}
        h_mjourn = H_mjourn()
        h_artikel_buff = H_artikel()
        for h_mjourn.nr, h_mjourn.anzahl, h_mjourn.request, h_mjourn._recid, h_artikel_buff.artart, h_artikel_buff.betriebsnr, h_artikel_buff._recid, h_artikel_buff.bezeich, h_artikel_buff.artnr in db_session.query(H_mjourn.nr, H_mjourn.anzahl, H_mjourn.request, H_mjourn._recid, H_artikel_buff.artart, H_artikel_buff.betriebsnr, H_artikel_buff._recid, H_artikel_buff.bezeich, H_artikel_buff.artnr).join(H_artikel_buff, (H_artikel_buff.artnr == H_mjourn.artnr) & (H_artikel_buff.departement == h_bill_line.departement)).filter(
                (H_mjourn.nr == h_artikel.betriebsnr) & (H_mjourn.departement == h_bill_line.departement) & (H_mjourn.rechnr == h_bill_line.rechnr)).order_by(H_mjourn._recid).all():
            if h_mjourn_obj_list.get(h_mjourn._recid):
                continue
            else:
                h_mjourn_obj_list[h_mjourn._recid] = True

            if num_entries(h_mjourn.request, "|") > 1:
                if entry(0, h_mjourn.request, "|") == to_string(h_bill_line._recid):
                    t_h_bill_line = T_h_bill_line()
                    t_h_bill_line_data.append(t_h_bill_line)

                    t_h_bill_line.menu_flag = 2
                    t_h_bill_line.sub_menu_bezeich = h_artikel_buff.bezeich
                    t_h_bill_line.sub_menu_betriebsnr = h_mjourn.nr
                    t_h_bill_line.sub_menu_qty = h_mjourn.anzahl
                    t_h_bill_line.rec_id = h_bill_line._recid
                    t_h_bill_line.artnr = h_artikel_buff.artnr
                    t_h_bill_line.rechnr = None
                    t_h_bill_line.bill_datum = None
                    t_h_bill_line.anzahl = None
                    t_h_bill_line.epreis = to_decimal(None)
                    t_h_bill_line.betrag = to_decimal(None)
                    t_h_bill_line.steuercode = None
                    t_h_bill_line.bezeich = None
                    t_h_bill_line.fremdwbetrag = to_decimal(None)
                    t_h_bill_line.zeit = None
                    t_h_bill_line.waehrungsnr = None
                    t_h_bill_line.sysdate = None
                    t_h_bill_line.departement = None
                    t_h_bill_line.prtflag = None
                    t_h_bill_line.tischnr = None
                    t_h_bill_line.kellner_nr = None
                    t_h_bill_line.nettobetrag = to_decimal(None)
                    t_h_bill_line.paid_flag = None
                    t_h_bill_line.betriebsnr = None
                    t_h_bill_line.segmentcode = None
                    t_h_bill_line.transferred = None

    return generate_output()
