from functions.additional_functions import *
import decimal
from datetime import date
from functions.rest_addgastinfo import rest_addgastinfo
from models import H_artikel, H_bill, Tisch, Htparam, H_umsatz, Artikel, H_bill_line, Queasy

def ts_restinv_btn_ccard2bl(billart:int, rec_id:int, curr_dept:int, balance:decimal, paid:decimal, balance_foreign:decimal, exchg_rate:decimal, full_paid:bool, transdate:date, disc_art1:int, disc_art2:int, disc_art3:int, kellner_kellner_nr:int):
    qty = 0
    price = 0
    description = ""
    amount_foreign = 0
    amount = 0
    bill_date = None
    t_h_artikel_list = []
    t_h_bill_list = []
    h_artikel = h_bill = tisch = htparam = h_umsatz = artikel = h_bill_line = queasy = None

    t_h_artikel = t_h_bill = h_art1 = tbuff = None

    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})
    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    H_art1 = H_artikel
    Tbuff = Tisch

    db_session = local_storage.db_session

    def generate_output():
        nonlocal qty, price, description, amount_foreign, amount, bill_date, t_h_artikel_list, t_h_bill_list, h_artikel, h_bill, tisch, htparam, h_umsatz, artikel, h_bill_line, queasy
        nonlocal h_art1, tbuff


        nonlocal t_h_artikel, t_h_bill, h_art1, tbuff
        nonlocal t_h_artikel_list, t_h_bill_list
        return {"qty": qty, "price": price, "description": description, "amount_foreign": amount_foreign, "amount": amount, "bill_date": bill_date, "t-h-artikel": t_h_artikel_list, "t-h-bill": t_h_bill_list}

    def fill_cover():

        nonlocal qty, price, description, amount_foreign, amount, bill_date, t_h_artikel_list, t_h_bill_list, h_artikel, h_bill, tisch, htparam, h_umsatz, artikel, h_bill_line, queasy
        nonlocal h_art1, tbuff


        nonlocal t_h_artikel, t_h_bill, h_art1, tbuff
        nonlocal t_h_artikel_list, t_h_bill_list

        f_pax:int = 0
        b_pax:int = 0
        str:str = ""
        H_art1 = H_artikel
        Tbuff = Tisch

        tbuff = db_session.query(Tbuff).filter(
                    (Tbuff.tischnr == h_bill.tischnr) &  (Tbuff.departement == h_bill.departement)).first()

        if tbuff and tbuff.roomcharge and tbuff.kellner_nr != 0:

            tbuff = db_session.query(Tbuff).first()
            tbuff.kellner_nr = 0

            tbuff = db_session.query(Tbuff).first()
        release_tbplan()

        if h_bill.resnr > 0:
            get_output(rest_addgastinfo(h_bill.departement, h_bill.rechnr, h_bill.resnr, h_bill.reslinnr, 0, transdate))

        h_bill = db_session.query(H_bill).first()
        h_bill.kellner_nr = kellner_kellner_nr

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 739)).first()

        if htparam.flogical:
            pass

        h_bill = db_session.query(H_bill).first()

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate

        if transdate != None:
            bill_date = transdate
        else:

            htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 253)).first()

            if htparam.flogical and bill_date < get_current_date():
                bill_date = bill_date + 1

        h_umsatz = db_session.query(H_umsatz).filter(
                    (H_umsatz.artnr == 0) &  (H_umsatz.departement == curr_dept) &  (H_umsatz.betriebsnr == curr_dept) &  (H_umsatz.datum == bill_date)).first()

        if not h_umsatz:
            h_umsatz = H_umsatz()
            db_session.add(h_umsatz)

            h_umsatz.artnr = 0
            h_umsatz.departement = curr_dept
            h_umsatz.betriebsnr = curr_dept
            h_umsatz.datum = bill_date
        h_umsatz.anzahl = h_umsatz.anzahl + h_bill.belegung

        if h_bill.belegung != 0:

            h_bill_line_obj_list = []
            for h_bill_line, h_art1, artikel in db_session.query(H_bill_line, H_art1, Artikel).join(H_art1,(H_art1.artnr == H_bill_line.artnr) &  (H_art1.departement == H_bill_line.departement) &  (H_art1.artart == 0)).join(Artikel,(Artikel.artnr == h_art1.artnrfront) &  (Artikel.departement == h_art1.departement)).filter(
                        (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == h_bill.departement) &  (H_bill_line.artnr != disc_art1) &  (H_bill_line.artnr != disc_art2) &  (H_bill_line.artnr != disc_art3)).all():
                if h_bill_line._recid in h_bill_line_obj_list:
                    continue
                else:
                    h_bill_line_obj_list.append(h_bill_line._recid)

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
        h_umsatz.betrag = h_umsatz.betrag + f_pax
        h_umsatz.nettobetrag = h_umsatz.nettobetrag + b_pax

        h_umsatz = db_session.query(H_umsatz).first()

    def release_tbplan():

        nonlocal qty, price, description, amount_foreign, amount, bill_date, t_h_artikel_list, t_h_bill_list, h_artikel, h_bill, tisch, htparam, h_umsatz, artikel, h_bill_line, queasy
        nonlocal h_art1, tbuff


        nonlocal t_h_artikel, t_h_bill, h_art1, tbuff
        nonlocal t_h_artikel_list, t_h_bill_list

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 31) &  (Queasy.number1 == h_bill.departement) &  (Queasy.number2 == h_bill.tischnr)).first()

        if queasy:

            queasy = db_session.query(Queasy).first()
            queasy.number3 = 0
            queasy.date1 = None

            queasy = db_session.query(Queasy).first()

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id)).first()

    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.departement == curr_dept) &  (H_artikel.artnr == billart)).first()
    billart = h_artikel.artnr
    qty = 1
    price = 0
    description = h_artikel.bezeich

    if balance == - paid:
        amount_foreign = - balance_foreign
        amount = - balance
    else:
        amount_foreign = round(paid / exchg_rate, 2)
        amount = paid

    if full_paid:
        fill_cover()

    t_h_artikel = query(t_h_artikel_list, current=True)
    t_h_artikel = T_h_artikel()
    t_h_artikel_list.append(t_h_artikel)

    buffer_copy(h_artikel, t_h_artikel)
    t_h_artikel.rec_id = h_artikel._recid

    t_h_bill = query(t_h_bill_list, current=True)
    t_h_bill = T_h_bill()
    t_h_bill_list.append(t_h_bill)

    buffer_copy(h_bill, t_h_bill)
    t_h_bill.rec_id = h_bill._recid

    return generate_output()