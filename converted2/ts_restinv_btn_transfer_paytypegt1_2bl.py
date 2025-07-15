#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.rest_addgastinfo import rest_addgastinfo
from models import H_bill, H_artikel, Tisch, Htparam, H_umsatz, Artikel, H_bill_line, Queasy

def ts_restinv_btn_transfer_paytypegt1_2bl(rec_id:int, do_it:bool, transdate:date, curr_dept:int, disc_art1:int, disc_art2:int, disc_art3:int, kellner_kellner_nr:int):

    prepare_cache ([Htparam, H_umsatz, Artikel, H_bill_line, Queasy])

    bill_date = None
    flag = 0
    t_h_bill_data = []
    h_bill = h_artikel = tisch = htparam = h_umsatz = artikel = h_bill_line = queasy = None

    t_h_bill = None

    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, flag, t_h_bill_data, h_bill, h_artikel, tisch, htparam, h_umsatz, artikel, h_bill_line, queasy
        nonlocal rec_id, do_it, transdate, curr_dept, disc_art1, disc_art2, disc_art3, kellner_kellner_nr


        nonlocal t_h_bill
        nonlocal t_h_bill_data

        return {"bill_date": bill_date, "flag": flag, "t-h-bill": t_h_bill_data}

    def fill_cover():

        nonlocal bill_date, flag, t_h_bill_data, h_bill, h_artikel, tisch, htparam, h_umsatz, artikel, h_bill_line, queasy
        nonlocal rec_id, do_it, transdate, curr_dept, disc_art1, disc_art2, disc_art3, kellner_kellner_nr


        nonlocal t_h_bill
        nonlocal t_h_bill_data

        f_pax:int = 0
        b_pax:int = 0
        str:string = ""
        h_art1 = None
        tbuff = None
        H_art1 =  create_buffer("H_art1",H_artikel)
        Tbuff =  create_buffer("Tbuff",Tisch)

        tbuff = db_session.query(Tbuff).filter(
                     (Tbuff.tischnr == h_bill.tischnr) & (Tbuff.departement == h_bill.departement)).first()

        if tbuff and tbuff.roomcharge and tbuff.kellner_nr != 0:
            pass
            tbuff.kellner_nr = 0


            pass
        release_tbplan()

        if h_bill.resnr > 0:
            get_output(rest_addgastinfo(h_bill.departement, h_bill.rechnr, h_bill.resnr, h_bill.reslinnr, 0, transdate))
        pass
        h_bill.kellner_nr = kellner_kellner_nr

        htparam = get_cache (Htparam, {"paramnr": [(eq, 739)]})

        if htparam.flogical:
            flag = 1
        pass

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate

        if transdate != None:
            bill_date = transdate
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

            if htparam.flogical and bill_date < get_current_date():
                bill_date = bill_date + timedelta(days=1)

        h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, 0)],"departement": [(eq, curr_dept)],"betriebsnr": [(eq, curr_dept)],"datum": [(eq, bill_date)]})

        if not h_umsatz:
            h_umsatz = H_umsatz()
            db_session.add(h_umsatz)

            h_umsatz.artnr = 0
            h_umsatz.departement = curr_dept
            h_umsatz.betriebsnr = curr_dept
            h_umsatz.datum = bill_date
        h_umsatz.anzahl = h_umsatz.anzahl + h_bill.belegung

        if h_bill.belegung != 0:

            h_bill_line_obj_list = {}
            for h_bill_line, h_art1, artikel in db_session.query(H_bill_line, H_art1, Artikel).join(H_art1,(H_art1.artnr == H_bill_line.artnr) & (H_art1.departement == H_bill_line.departement) & (H_art1.artart == 0)).join(Artikel,(Artikel.artnr == H_art1.artnrfront) & (Artikel.departement == H_art1.departement)).filter(
                         (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == h_bill.departement) & (H_bill_line.artnr != disc_art1) & (H_bill_line.artnr != disc_art2) & (H_bill_line.artnr != disc_art3)).order_by(H_bill_line._recid).all():
                if h_bill_line_obj_list.get(h_bill_line._recid):
                    continue
                else:
                    h_bill_line_obj_list[h_bill_line._recid] = True

                if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                    f_pax = f_pax + h_bill_line.anzahl

                elif artikel.umsatzart == 6:
                    b_pax = b_pax + h_bill_line.anzahl


        if h_bill.belegung > 0:

            if f_pax > h_bill.belegung:
                f_pax = h_bill.belegung

            if b_pax > h_bill.belegung:
                b_pax = h_bill.belegung

        elif h_bill.belegung < 0:

            if f_pax < h_bill.belegung:
                f_pax = h_bill.belegung

            if b_pax < h_bill.belegung:
                b_pax = h_bill.belegung
        h_umsatz.betrag =  to_decimal(h_umsatz.betrag) + to_decimal(f_pax)
        h_umsatz.nettobetrag =  to_decimal(h_umsatz.nettobetrag) + to_decimal(b_pax)
        pass
        pass


    def release_tbplan():

        nonlocal bill_date, flag, t_h_bill_data, h_bill, h_artikel, tisch, htparam, h_umsatz, artikel, h_bill_line, queasy
        nonlocal rec_id, do_it, transdate, curr_dept, disc_art1, disc_art2, disc_art3, kellner_kellner_nr


        nonlocal t_h_bill
        nonlocal t_h_bill_data

        queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, h_bill.departement)],"number2": [(eq, h_bill.tischnr)]})

        if queasy:
            pass
            queasy.number3 = 0
            queasy.date1 = None


            pass
            pass


    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})

    if do_it:
        pass
        h_bill.flag = 1
        pass
    fill_cover()

    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})
    t_h_bill = T_h_bill()
    t_h_bill_data.append(t_h_bill)

    buffer_copy(h_bill, t_h_bill)
    t_h_bill.rec_id = h_bill._recid

    return generate_output()