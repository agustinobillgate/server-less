from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htpint import htpint
from models import H_artikel, H_bill_line, Artikel, H_bill, H_umsatz

def nt_shiftcover_2():
    billdate:date = None
    progname:str = "nt-shiftcover.p"
    night_type:int = 0
    reihenfolge:int = 0
    str:str = ""
    h_artikel = h_bill_line = artikel = h_bill = h_umsatz = None

    temp_rechnr = temp = None

    temp_rechnr_list, Temp_rechnr = create_model("Temp_rechnr", {"dept":int, "rechnr":int, "pax":int, "flag":bool, "nr":int})
    temp_list, Temp = create_model("Temp", {"dept":int, "pax":[int,4], "f_pax":[int,4], "b_pax":[int,4]})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, progname, night_type, reihenfolge, str, h_artikel, h_bill_line, artikel, h_bill, h_umsatz


        nonlocal temp_rechnr, temp
        nonlocal temp_rechnr_list, temp_list

        return {}

    def cover_by_shift():

        nonlocal billdate, progname, night_type, reihenfolge, str, h_artikel, h_bill_line, artikel, h_bill, h_umsatz


        nonlocal temp_rechnr, temp
        nonlocal temp_rechnr_list, temp_list

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
        temp_list.clear()

        h_bill_line_obj_list = []
        for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement)).filter(
                 (H_bill_line.bill_datum == billdate) & (H_bill_line.artnr > 0) & (H_bill_line.artnr != disc_art1) & (H_bill_line.artnr != disc_art2) & (H_bill_line.artnr != disc_art3) & (H_bill_line.zeit >= 0)).order_by(H_bill_line.departement, H_bill_line.rechnr).all():
            if h_bill_line._recid in h_bill_line_obj_list:
                continue
            else:
                h_bill_line_obj_list.append(h_bill_line._recid)

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()

            h_bill = db_session.query(H_bill).filter(
                     (H_bill.rechnr == h_bill_line.rechnr) & (H_bill.departement == h_bill_line.departement)).first()

            if curr_dept == None:
                temp = Temp()
                temp_list.append(temp)

                curr_dept = h_bill_line.departement


                temp.dept = curr_dept

            if curr_dept != h_bill_line.departement:
                temp = Temp()
                temp_list.append(temp)

                temp.dept = h_bill_line.departement

            if curr_rechnr == None and h_bill_line.betriebsnr != 0:
                temp_rechnr = Temp_rechnr()
                temp_rechnr_list.append(temp_rechnr)

                temp_rechnr.nr = h_bill_line.betriebsnr
                temp_rechnr.dept = h_bill_line.departement
                temp_rechnr.rechnr = h_bill_line.rechnr
                temp_rechnr.pax = h_bill.belegung

            temp_rechnr = query(temp_rechnr_list, filters=(lambda temp_rechnr: temp_rechnr.rechnr == h_bill_line.rechnr), first=True)

            if not temp_rechnr and h_bill_line.betriebsnr != 0:
                temp_rechnr = Temp_rechnr()
                temp_rechnr_list.append(temp_rechnr)

                temp_rechnr.nr = h_bill_line.betriebsnr
                temp_rechnr.dept = h_bill_line.departement
                temp_rechnr.rechnr = h_bill_line.rechnr
                temp_rechnr.pax = h_bill.belegung

            temp_rechnr = query(temp_rechnr_list, filters=(lambda temp_rechnr: temp_rechnr.rechnr == h_bill_line.rechnr), first=True)

            if temp_rechnr:

                if h_artikel.artart == 11:
                    temp_rechnr.flag = True

            if artikel:

                if artikel.umsatzart == 3 or artikel.umsatzart == 5:

                    if h_bill_line.betriebsnr != 0:

                        temp = query(temp_list, filters=(lambda temp: temp.dept == h_bill_line.departement), first=True)
                        temp.f_pax[h_bill_line.betriebsnr - 1] = temp.f_pax[h_bill_line.betriebsnr - 1] + h_bill_line.anzahl

                elif artikel.umsatzart == 6:

                    if h_bill_line.betriebsnr != 0:

                        temp = query(temp_list, filters=(lambda temp: temp.dept == h_bill_line.departement), first=True)
                        temp.b_pax[h_bill_line.betriebsnr - 1] = temp.b_pax[h_bill_line.betriebsnr - 1] + h_bill_line.anzahl
            curr_dept = h_bill_line.departement
            curr_rechnr = h_bill_line.rechnr

        for temp in query(temp_list):

            for temp_rechnr in query(temp_rechnr_list, filters=(lambda temp_rechnr: temp_rechnr.dept == temp.dept and temp_rechnr.flag == False)):
                temp.pax[temp_rechnr.nr - 1] = temp.pax[temp_rechnr.nr - 1] + temp_rechnr.pax

        for temp in query(temp_list):
            for curr_i in range(1,4 + 1) :

                h_umsatz = db_session.query(H_umsatz).filter(
                         (H_umsatz.artnr == 0) & (H_umsatz.departement == temp.dept) & (H_umsatz.epreis == curr_i) & (H_umsatz.datum == billdate)).first()

                if not h_umsatz:
                    h_umsatz = H_umsatz()
                    db_session.add(h_umsatz)

                    h_umsatz.artnr = 0
                    h_umsatz.departement = temp.dept
                    h_umsatz.epreis =  to_decimal(curr_i)
                    h_umsatz.datum = billdate
                    h_umsatz.betrag =  to_decimal(temp.f_pax[curr_i - 1])
                    h_umsatz.nettobetrag =  to_decimal(temp.b_pax[curr_i - 1])
                    h_umsatz.anzahl = temp.pax[curr_i - 1]


                else:
                    h_umsatz.betrag =  to_decimal(h_umsatz.betrag) + to_decimal(temp.f_pax[curr_i - 1])
                    h_umsatz.nettobetrag =  to_decimal(h_umsatz.nettobetrag) + to_decimal(temp.b_pax[curr_i - 1])
                    h_umsatz.anzahl = h_umsatz.anzahl + temp.pax[curr_i - 1]


    billdate = get_output(htpdate(110))
    cover_by_shift()

    return generate_output()