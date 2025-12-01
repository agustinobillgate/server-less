#using conversion tools version: 1.0.0.119

# =============================================
# Rulita, 01-12-2025
# - Added with_for_update all query 
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htpint import htpint
from models import H_artikel, Artikel, H_bill_line, H_bill, H_umsatz

def nt_shiftcover():

    prepare_cache ([Artikel, H_bill_line, H_bill, H_umsatz])

    billdate:date = None
    progname:string = "nt-shiftcover.p"
    night_type:int = 0
    reihenfolge:int = 0
    h_artikel = artikel = h_bill_line = h_bill = h_umsatz = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, progname, night_type, reihenfolge, h_artikel, artikel, h_bill_line, h_bill, h_umsatz

        return {}

    def cover_by_shift():

        nonlocal billdate, progname, night_type, reihenfolge, h_artikel, artikel, h_bill_line, h_bill, h_umsatz

        attach_it:bool = False
        curr_dept:int = None
        curr_rechnr:int = None
        f_pax:List[int] = [0, 0, 0, 0]
        b_pax:List[int] = [0, 0, 0, 0]
        curr_i:int = 0
        disc_art1:int = 0
        disc_art2:int = 0
        disc_art3:int = 0
        disc_art1 = get_output(htpint(557))
        disc_art2 = get_output(htpint(596))
        disc_art3 = get_output(htpint(556))

        h_bill_line_obj_list = {}
        for h_bill_line, h_artikel, artikel in db_session.query(H_bill_line, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0)).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement)).filter(
                 (H_bill_line.bill_datum == billdate) & (H_bill_line.artnr > 0) & (H_bill_line.artnr != disc_art1) & (H_bill_line.artnr != disc_art2) & (H_bill_line.artnr != disc_art3) & (H_bill_line.zeit >= 0) & (H_bill_line.epreis > 0)).order_by(H_bill_line.departement, H_bill_line.rechnr).all():
            if h_bill_line_obj_list.get(h_bill_line._recid):
                continue
            else:
                h_bill_line_obj_list[h_bill_line._recid] = True

            if curr_dept == None:
                curr_dept = h_bill_line.departement
                curr_rechnr = h_bill_line.rechnr

                h_bill = get_cache (H_bill, {"rechnr": [(eq, h_bill_line.rechnr)],"departement": [(eq, h_bill_line.departement)]})

            if curr_dept != h_bill_line.departement or curr_rechnr != h_bill_line.rechnr:

                if h_bill.belegung > 0:

                    if f_pax[0] > h_bill.belegung:
                        f_pax[0] = h_bill.belegung

                    if b_pax[0] > h_bill.belegung:
                        b_pax[0] = h_bill.belegung

                    if f_pax[1] > h_bill.belegung:
                        f_pax[1] = h_bill.belegung

                    if b_pax[1] > h_bill.belegung:
                        b_pax[1] = h_bill.belegung

                    if f_pax[2] > h_bill.belegung:
                        f_pax[2] = h_bill.belegung

                    if b_pax[2] > h_bill.belegung:
                        b_pax[2] = h_bill.belegung

                    if f_pax[3] > h_bill.belegung:
                        f_pax[3] = h_bill.belegung

                    if b_pax[3] > h_bill.belegung:
                        b_pax[3] = h_bill.belegung

                elif h_bill.belegung < 0:

                    if f_pax[0] < h_bill.belegung:
                        f_pax[0] = h_bill.belegung

                    if b_pax[0] < h_bill.belegung:
                        b_pax[0] = h_bill.belegung

                    if f_pax[1] < h_bill.belegung:
                        f_pax[1] = h_bill.belegung

                    if b_pax[1] < h_bill.belegung:
                        b_pax[1] = h_bill.belegung

                    if f_pax[2] < h_bill.belegung:
                        f_pax[2] = h_bill.belegung

                    if b_pax[2] < h_bill.belegung:
                        b_pax[2] = h_bill.belegung

                    if f_pax[3] < h_bill.belegung:
                        f_pax[3] = h_bill.belegung

                    if b_pax[3] < h_bill.belegung:
                        b_pax[3] = h_bill.belegung
                for curr_i in range(1,4 + 1) :

                    if f_pax[curr_i - 1] != 0 or b_pax[curr_i - 1] != 0:

                        # h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, 0)],"departement": [(eq, curr_dept)],"epreis": [(eq, curr_i)],"datum": [(eq, billdate)]})
                        h_umsatz = db_session.query(H_umsatz).filter((H_umsatz.artnr == 0) & (H_umsatz.departement == curr_dept) & (H_umsatz.epreis == to_decimal(curr_i)) & (H_umsatz.datum == billdate)).with_for_update().first()

                        if not h_umsatz:
                            h_umsatz = H_umsatz()
                            db_session.add(h_umsatz)

                            h_umsatz.artnr = 0
                            h_umsatz.departement = curr_dept
                            h_umsatz.epreis =  to_decimal(curr_i)
                            h_umsatz.datum = billdate


                        h_umsatz.betrag =  to_decimal(h_umsatz.betrag) + to_decimal(f_pax[curr_i - 1])
                        h_umsatz.nettobetrag =  to_decimal(h_umsatz.nettobetrag) + to_decimal(b_pax[curr_i - 1])


                        pass
                curr_dept = h_bill_line.departement
                curr_rechnr = h_bill_line.rechnr

                h_bill = get_cache (H_bill, {"rechnr": [(eq, h_bill_line.rechnr)],"departement": [(eq, h_bill_line.departement)]})
                for curr_i in range(1,4 + 1) :
                    f_pax[curr_i - 1] = 0
                    b_pax[curr_i - 1] = 0

            if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                f_pax[h_bill_line.betriebsnr - 1] = f_pax[h_bill_line.betriebsnr - 1] + h_bill_line.anzahl

            elif artikel.umsatzart == 6:
                b_pax[h_bill_line.betriebsnr - 1] = b_pax[h_bill_line.betriebsnr - 1] + h_bill_line.anzahl

        if h_bill.belegung > 0:

            if f_pax[0] > h_bill.belegung:
                f_pax[0] = h_bill.belegung

            if b_pax[0] > h_bill.belegung:
                b_pax[0] = h_bill.belegung

            if f_pax[1] > h_bill.belegung:
                f_pax[1] = h_bill.belegung

            if b_pax[1] > h_bill.belegung:
                b_pax[1] = h_bill.belegung

            if f_pax[2] > h_bill.belegung:
                f_pax[2] = h_bill.belegung

            if b_pax[2] > h_bill.belegung:
                b_pax[2] = h_bill.belegung

            if f_pax[3] > h_bill.belegung:
                f_pax[3] = h_bill.belegung

            if b_pax[3] > h_bill.belegung:
                b_pax[3] = h_bill.belegung

        elif h_bill.belegung < 0:

            if f_pax[0] < h_bill.belegung:
                f_pax[0] = h_bill.belegung

            if b_pax[0] < h_bill.belegung:
                b_pax[0] = h_bill.belegung

            if f_pax[1] < h_bill.belegung:
                f_pax[1] = h_bill.belegung

            if b_pax[1] < h_bill.belegung:
                b_pax[1] = h_bill.belegung

            if f_pax[2] < h_bill.belegung:
                f_pax[2] = h_bill.belegung

            if b_pax[2] < h_bill.belegung:
                b_pax[2] = h_bill.belegung

            if f_pax[3] < h_bill.belegung:
                f_pax[3] = h_bill.belegung

            if b_pax[3] < h_bill.belegung:
                b_pax[3] = h_bill.belegung
        for curr_i in range(1,4 + 1) :

            if f_pax[curr_i - 1] != 0 or b_pax[curr_i - 1] != 0:

                # h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, 0)],"departement": [(eq, curr_dept)],"epreis": [(eq, curr_i)],"datum": [(eq, billdate)]})
                h_umsatz = db_session.query(H_umsatz).filter((H_umsatz.artnr == 0) & (H_umsatz.departement == curr_dept) & (H_umsatz.epreis == to_decimal(curr_i)) & (H_umsatz.datum == billdate)).with_for_update().first()

                if not h_umsatz:
                    h_umsatz = H_umsatz()
                    db_session.add(h_umsatz)

                    h_umsatz.artnr = 0
                    h_umsatz.departement = curr_dept
                    h_umsatz.epreis =  to_decimal(curr_i)
                    h_umsatz.datum = billdate


                h_umsatz.betrag =  to_decimal(h_umsatz.betrag) + to_decimal(f_pax[curr_i - 1])
                h_umsatz.nettobetrag =  to_decimal(h_umsatz.nettobetrag) + to_decimal(b_pax[curr_i - 1])


                pass


    billdate = get_output(htpdate(110))
    cover_by_shift()

    return generate_output()