from functions.additional_functions import *
import decimal
from models import H_bill_line

def ts_split_item_procbl(rec_id:int, split_qty:int, rest:decimal, foreign_rest:decimal, curr_qty:int, price_decimal:int, amount:decimal, foreign_amt:decimal, qty_sign:int):
    i:int = 0
    h_bill_line = None

    h_bline = None

    H_bline = H_bill_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, h_bill_line
        nonlocal h_bline


        nonlocal h_bline
        return {}


    h_bill_line = db_session.query(H_bill_line).filter(
            (H_bill_line._recid == rec_id)).first()
    for i in range(1,split_qty + 1) :

        if i == split_qty:

            h_bill_line = db_session.query(H_bill_line).first()
            amount = rest
            foreign_amt = foreign_rest
            h_bill_line.anzahl = qty_sign
            h_bill_line.fremdwbetrag = foreign_amt
            h_bill_line.betrag = amount
            h_bill_line.epreis = h_bill_line.epreis * curr_qty *\
                    qty_sign / split_qty
            h_bill_line.epreis = round(h_bill_line.epreis, price_decimal)
            h_bill_line.nettobetrag = h_bill_line.epreis * h_bill_line.anzahl
            h_bill_line.zeit = get_current_time_in_seconds() + i

            if split_qty != curr_qty:
                h_bill_line.bezeich = h_bill_line.bezeich + "*"

            h_bill_line = db_session.query(H_bill_line).first()
        else:
            h_bline = H_bline()
            db_session.add(h_bline)

            rest = rest - amount
            foreign_rest = foreign_rest - foreign_amt
            h_bline.steuercode = 9999
            h_bline.rechnr = h_bill_line.rechnr
            h_bline.artnr = h_bill_line.artnr
            h_bline.anzahl = qty_sign
            h_bline.fremdwbetrag = foreign_amt
            h_bline.betrag = amount
            h_bline.tischnr = h_bill_line.tisch
            h_bline.departement = h_bill_line.departement
            h_bline.epreis = h_bill_line.epreis * curr_qty *\
                    qty_sign / split_qty
            h_bline.epreis = round(h_bline.epreis, price_decimal)
            h_bline.nettobetrag = h_bline.epreis * h_bline.anzahl
            h_bline.zeit = get_current_time_in_seconds() + i
            h_bline.bill_datum = h_bill_line.bill_datum
            h_bline.sysdate = h_bill_line.sysdate

            if split_qty == curr_qty:
                h_bline.bezeich = h_bill_line.bezeich
            else:
                h_bline.bezeich = h_bill_line.bezeich + "*"

            if price_decimal == 0:
                h_bline.epreis = round(h_bline.epreis, 0)

            h_bline = db_session.query(H_bline).first()

    return generate_output()