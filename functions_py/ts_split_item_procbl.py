# using conversion tools version: 1.0.0.117
"""_yusufwijasena_24/11/2025
        issue:  - cannot split item
                - fix h_bill_line.tisch to h_bill_line.tischnr
"""

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill_line, H_journal


def ts_split_item_procbl(rec_id: int, split_qty: int, rest: Decimal, foreign_rest: Decimal, curr_qty: int, price_decimal: int, amount: Decimal, foreign_amt: Decimal, qty_sign: int):

    prepare_cache([H_bill_line, H_journal])

    i: int = 0
    h_bill_line = h_journal = None

    h_bline = buff_h_journal = None

    H_bline = create_buffer("H_bline", H_bill_line)
    Buff_h_journal = create_buffer("Buff_h_journal", H_journal)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, h_bill_line, h_journal
        nonlocal rec_id, split_qty, rest, foreign_rest, curr_qty, price_decimal, amount, foreign_amt, qty_sign
        nonlocal h_bline, buff_h_journal

        return {
            "amount": amount,
            "foreign_amt": foreign_amt,
            "qty_sign": qty_sign
        }

    h_bill_line = get_cache(H_bill_line, {"_recid": [(eq, rec_id)]})

    h_journal = get_cache(H_journal, {"schankbuch": [(eq, rec_id)]})
    for i in range(1, split_qty + 1):

        if i == split_qty:
            amount = to_decimal(rest)
            foreign_amt = to_decimal(foreign_rest)
            h_bill_line.anzahl = qty_sign
            h_bill_line.fremdwbetrag = to_decimal(foreign_amt)
            h_bill_line.betrag = to_decimal(amount)
            h_bill_line.epreis = to_decimal(h_bill_line.epreis) * to_decimal(curr_qty) *\
                qty_sign / to_decimal(split_qty)
            h_bill_line.epreis = to_decimal(
                round(h_bill_line.epreis, price_decimal))
            h_bill_line.nettobetrag = to_decimal(
                h_bill_line.epreis) * to_decimal(h_bill_line.anzahl)
            h_bill_line.zeit = get_current_time_in_seconds() + i

            if split_qty != curr_qty:
                h_bill_line.bezeich = h_bill_line.bezeich + "*"

            if h_journal:
                h_journal.anzahl = h_bill_line.anzahl
                h_journal.fremdwaehrng = to_decimal(h_bill_line.fremdwbetrag)
                h_journal.betrag = to_decimal(h_bill_line.betrag)
                h_journal.epreis = to_decimal(h_bill_line.epreis)
                h_journal.zeit = h_bill_line.zeit

        else:
            h_bline = H_bill_line()
            db_session.add(h_bline)

            rest = to_decimal(rest) - to_decimal(amount)
            foreign_rest = to_decimal(foreign_rest) - to_decimal(foreign_amt)
            h_bline.steuercode = 9999
            h_bline.rechnr = h_bill_line.rechnr
            h_bline.artnr = h_bill_line.artnr
            h_bline.anzahl = qty_sign
            h_bline.fremdwbetrag = to_decimal(foreign_amt)
            h_bline.betrag = to_decimal(amount)
            h_bline.tischnr = h_bill_line.tischnr  # yusufwijasena: fix incorrect attribute
            h_bline.departement = h_bill_line.departement
            h_bline.epreis = to_decimal(h_bill_line.epreis) * to_decimal(curr_qty) *\
                qty_sign / to_decimal(split_qty)
            h_bline.epreis = to_decimal(round(h_bline.epreis, price_decimal))
            h_bline.nettobetrag = to_decimal(
                h_bline.epreis) * to_decimal(h_bline.anzahl)
            h_bline.zeit = get_current_time_in_seconds() + i
            h_bline.bill_datum = h_bill_line.bill_datum
            h_bline.sysdate = h_bill_line.sysdate

            if split_qty == curr_qty:
                h_bline.bezeich = h_bill_line.bezeich
            else:
                h_bline.bezeich = h_bill_line.bezeich + "*"

            if price_decimal == 0:
                h_bline.epreis = to_decimal(round(h_bline.epreis, 0))

            if h_journal:
                buff_h_journal = H_journal()
                db_session.add(buff_h_journal)

                buff_h_journal.schankbuch = h_bline._recid
                buff_h_journal.rechnr = h_bline.rechnr
                buff_h_journal.artnr = h_bline.artnr
                buff_h_journal.anzahl = h_bline.anzahl
                buff_h_journal.fremdwaehrng = to_decimal(h_bline.fremdwbetrag)
                buff_h_journal.betrag = to_decimal(h_bline.betrag)
                buff_h_journal.tischnr = h_bline.tischnr
                buff_h_journal.departement = h_bline.departement
                buff_h_journal.epreis = to_decimal(h_bline.epreis)
                buff_h_journal.zeit = h_bline.zeit
                buff_h_journal.bill_datum = h_bline.bill_datum
                buff_h_journal.sysdate = h_bline.sysdate
                buff_h_journal.bezeich = h_journal.bezeich
                buff_h_journal.kellner_nr = h_journal.kellner_nr
                buff_h_journal.artnr = h_journal.artnr
                buff_h_journal.stornogrund = h_journal.stornogrund
                buff_h_journal.aendertext = h_journal.aendertext
                buff_h_journal.wabkurz = h_journal.wabkurz
                buff_h_journal.segmentcode = h_journal.segmentcode
                buff_h_journal.artnrfront = h_journal.artnrfront
                buff_h_journal.bon_nr = h_journal.bon_nr
                buff_h_journal.zinr = h_journal.zinr
                buff_h_journal.gang = h_journal.gang

                if price_decimal == 0:
                    buff_h_journal.epreis = to_decimal(
                        round(h_bline.epreis, 0))

    return generate_output()
