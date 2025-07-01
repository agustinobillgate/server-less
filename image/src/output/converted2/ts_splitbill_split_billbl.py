#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill_line, H_bill, H_artikel

def ts_splitbill_split_billbl(rec_id:int, dept:int, price_decimal:int):

    prepare_cache ([H_bill, H_artikel])

    t_h_bill_line_list = []
    h_bill_line = h_bill = h_artikel = None

    t_h_bill_line = art_list = None

    t_h_bill_line_list, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int})
    art_list_list, Art_list = create_model_like(H_bill_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_bill_line_list, h_bill_line, h_bill, h_artikel
        nonlocal rec_id, dept, price_decimal


        nonlocal t_h_bill_line, art_list
        nonlocal t_h_bill_line_list, art_list_list

        return {"t-h-bill-line": t_h_bill_line_list}

    def split_bill():

        nonlocal t_h_bill_line_list, h_bill_line, h_bill, h_artikel
        nonlocal rec_id, dept, price_decimal


        nonlocal t_h_bill_line, art_list
        nonlocal t_h_bill_line_list, art_list_list

        h_artart:int = 0
        i:int = 0
        amount:Decimal = to_decimal("0.0")
        splitamount:Decimal = to_decimal("0.0")
        pos_anz:int = 0

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == dept)).order_by(H_bill_line._recid).all():

            if h_bill_line.artnr != 0:

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)]})
                h_artart = h_artikel.artart
            else:
                h_artart = 2

            art_list = query(art_list_list, filters=(lambda art_list: art_list.artnr == h_bill_line.artnr and art_list.departement == h_bill_line.departement and art_list.bezeich == h_bill_line.bezeich and art_list.waehrungsnr == h_bill_line.waehrungsnr and art_list.betriebsnr == h_bill_line.betriebsnr), first=True)

            if not art_list or (art_list and h_artart != 0):
                art_list = Art_list()
                art_list_list.append(art_list)

                art_list.artnr = h_bill_line.artnr
                art_list.departement = h_bill_line.departement
                art_list.bezeich = h_bill_line.bezeich
                art_list.epreis =  to_decimal(h_bill_line.epreis)
                art_list.rechnr = h_bill_line.rechnr
                art_list.tischnr = h_bill_line.tischnr
                art_list.zeit = h_bill_line.zeit
                art_list.kellner_nr = h_bill_line.kellner_nr
                art_list.bill_datum = h_bill_line.bill_datum
                art_list.sysdate = h_bill_line.sysdate
                art_list.waehrungsnr = h_bill_line.waehrungsnr
                art_list.betriebsnr = h_bill_line.betriebsnr


            art_list.anzahl = art_list.anzahl + h_bill_line.anzahl
            art_list.betrag =  to_decimal(art_list.betrag) + to_decimal(h_bill_line.betrag)
            art_list.nettobetrag =  to_decimal(art_list.nettobetrag) + to_decimal(h_bill_line.nettobetrag)

        for art_list in query(art_list_list):

            if art_list.anzahl == 0 and round(art_list.betrag, 0) == 0:
                art_list_list.remove(art_list)

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == dept)).order_by(H_bill_line._recid).all():
            db_session.delete(h_bill_line)
        pass

        for art_list in query(art_list_list):
            amount =  to_decimal("0")
            pos_anz = art_list.anzahl

            if pos_anz < 0:
                pos_anz = - pos_anz
            splitamount = to_decimal(round(art_list.betrag / pos_anz , price_decimal))
            for i in range(1,pos_anz + 1) :

                if i < pos_anz:
                    amount =  to_decimal(splitamount)
                else:
                    amount = to_decimal(round(art_list.betrag - amount * (pos_anz - 1) , price_decimal))
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
                h_bill_line.epreis =  to_decimal(art_list.epreis)
                h_bill_line.betrag =  to_decimal(amount)
                h_bill_line.nettobetrag = to_decimal(round(art_list.nettobetrag / art_list.anzahl , price_decimal))
                h_bill_line.bill_datum = art_list.bill_datum
                h_bill_line.sysdate = art_list.sysdate
                h_bill_line.waehrungsnr = art_list.waehrungsnr
                h_bill_line.betriebsnr = art_list.betriebsnr

                if art_list.anzahl > 0:
                    h_bill_line.anzahl = 1
                else:
                    h_bill_line.anzahl = - 1
                pass
        art_list_list.clear()

    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})
    split_bill()

    for h_bill_line in db_session.query(H_bill_line).filter(
             (H_bill_line.departement == dept) & (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.waehrungsnr == 0)).order_by(H_bill_line.bezeich).all():
        t_h_bill_line = T_h_bill_line()
        t_h_bill_line_list.append(t_h_bill_line)

        buffer_copy(h_bill_line, t_h_bill_line)
        t_h_bill_line.rec_id = h_bill_line._recid

    return generate_output()