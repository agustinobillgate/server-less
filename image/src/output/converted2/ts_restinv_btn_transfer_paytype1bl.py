#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.check_rpaymentbl import check_rpaymentbl
from functions.rest_addgastinfo import rest_addgastinfo
from models import H_artikel, Guest, H_bill, Tisch, Htparam, H_umsatz, Artikel, H_bill_line, Queasy

def ts_restinv_btn_transfer_paytype1bl(pvilanguage:int, rec_id:int, guestnr:int, curr_dept:int, paid:Decimal, exchg_rate:Decimal, price_decimal:int, balance:Decimal, transdate:date, disc_art1:int, disc_art2:int, disc_art3:int, kellner_kellner_nr:int):

    prepare_cache ([Guest, H_bill, Htparam, H_umsatz, Artikel, H_bill_line, Queasy])

    billart = 0
    qty = 0
    description = ""
    price = to_decimal("0.0")
    amount_foreign = to_decimal("0.0")
    amount = to_decimal("0.0")
    bill_date = None
    fl_code = 0
    fl_code1 = 0
    msg_str = ""
    var_testing = ""
    t_h_artikel_list = []
    h_artikel = guest = h_bill = tisch = htparam = h_umsatz = artikel = h_bill_line = queasy = None

    t_h_artikel = bill_guest = None

    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})

    Bill_guest = create_buffer("Bill_guest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billart, qty, description, price, amount_foreign, amount, bill_date, fl_code, fl_code1, msg_str, var_testing, t_h_artikel_list, h_artikel, guest, h_bill, tisch, htparam, h_umsatz, artikel, h_bill_line, queasy
        nonlocal pvilanguage, rec_id, guestnr, curr_dept, paid, exchg_rate, price_decimal, balance, transdate, disc_art1, disc_art2, disc_art3, kellner_kellner_nr
        nonlocal bill_guest


        nonlocal t_h_artikel, bill_guest
        nonlocal t_h_artikel_list

        return {"billart": billart, "qty": qty, "description": description, "price": price, "amount_foreign": amount_foreign, "amount": amount, "bill_date": bill_date, "fl_code": fl_code, "fl_code1": fl_code1, "msg_str": msg_str, "var_testing": var_testing, "t-h-artikel": t_h_artikel_list}

    def fill_cover():

        nonlocal billart, qty, description, price, amount_foreign, amount, bill_date, fl_code, fl_code1, msg_str, var_testing, t_h_artikel_list, h_artikel, guest, h_bill, tisch, htparam, h_umsatz, artikel, h_bill_line, queasy
        nonlocal pvilanguage, rec_id, guestnr, curr_dept, paid, exchg_rate, price_decimal, balance, transdate, disc_art1, disc_art2, disc_art3, kellner_kellner_nr
        nonlocal bill_guest


        nonlocal t_h_artikel, bill_guest
        nonlocal t_h_artikel_list

        f_pax:int = 0
        b_pax:int = 0
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
            fl_code1 = 1
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

        nonlocal billart, qty, description, price, amount_foreign, amount, bill_date, fl_code, fl_code1, msg_str, var_testing, t_h_artikel_list, h_artikel, guest, h_bill, tisch, htparam, h_umsatz, artikel, h_bill_line, queasy
        nonlocal pvilanguage, rec_id, guestnr, curr_dept, paid, exchg_rate, price_decimal, balance, transdate, disc_art1, disc_art2, disc_art3, kellner_kellner_nr
        nonlocal bill_guest


        nonlocal t_h_artikel, bill_guest
        nonlocal t_h_artikel_list

        queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, h_bill.departement)],"number2": [(eq, h_bill.tischnr)]})

        if queasy:
            pass
            queasy.number3 = 0
            queasy.date1 = None


            pass
            pass


    def create_queasy_interface(billno:int, department:int, paid:Decimal, artnr:int):

        nonlocal billart, qty, description, price, amount_foreign, amount, bill_date, fl_code, fl_code1, msg_str, var_testing, t_h_artikel_list, h_artikel, guest, h_bill, tisch, htparam, h_umsatz, artikel, h_bill_line, queasy
        nonlocal pvilanguage, rec_id, guestnr, curr_dept, exchg_rate, price_decimal, balance, transdate, disc_art1, disc_art2, disc_art3, kellner_kellner_nr
        nonlocal bill_guest


        nonlocal t_h_artikel, bill_guest
        nonlocal t_h_artikel_list

        queasy = get_cache (Queasy, {"key": [(eq, 313)],"number1": [(eq, billno)],"number2": [(eq, department)],"number3": [(eq, artnr)]})

        if queasy:
            pass
            queasy.deci1 =  to_decimal(paid)
            queasy.logi1 = True
            queasy.logi2 = False
            queasy.logi3 = False


            pass
            pass
        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 313
            queasy.number1 = billno
            queasy.number2 = department
            queasy.number3 = artnr
            queasy.deci1 =  to_decimal(paid)
            queasy.logi1 = True
            queasy.logi2 = False
            queasy.logi3 = False


            pass


    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})
    billart, msg_str = get_output(check_rpaymentbl(pvilanguage, guestnr, curr_dept))

    if billart > 0:

        h_artikel = get_cache (H_artikel, {"departement": [(eq, curr_dept)],"artnrfront": [(eq, billart)],"artart": [(eq, 2)]})

        if h_artikel:

            bill_guest = get_cache (Guest, {"gastnr": [(eq, guestnr)]})
            billart = h_artikel.artnr
            qty = 1
            description = h_artikel.bezeich
            price =  to_decimal("0")
            amount_foreign = to_decimal(round(paid / exchg_rate , 2))


            amount =  to_decimal(paid)
            create_queasy_interface(h_bill.rechnr, curr_dept, paid, billart)

            if h_bill.resnr == 0:
                pass
                h_bill.resnr = bill_guest.gastnr
                h_bill.reslinnr = 0
                h_bill.bilname = bill_guest.name + ", " + bill_guest.vorname1 +\
                        " " + bill_guest.anrede1


                pass

            if price_decimal == 0 and (balance + paid) >= -1 and (balance + paid) <= 1:
                fill_cover()

            elif price_decimal == 2 and (balance + paid) >= -0.01 and (balance + paid) <= 0.01:
                fill_cover()
            fl_code = 1
        else:
            fl_code = 2
    else:
        fl_code = 3

    if h_artikel:
        t_h_artikel = T_h_artikel()
        t_h_artikel_list.append(t_h_artikel)

        buffer_copy(h_artikel, t_h_artikel)
        t_h_artikel.rec_id = h_artikel._recid

    return generate_output()