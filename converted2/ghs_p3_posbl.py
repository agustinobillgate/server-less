from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from models import H_bill_line, H_bill, Guest, Mc_guest, H_artikel, Artikel

def ghs_p3_posbl(datum:date, propid:str):
    pos_list_list = []
    disc_food_art:int = 0
    disc_bev_art:int = 0
    disc_other_art:int = 0
    bill_datum:date = None
    art_type:int = 0
    h_bill_line = h_bill = guest = mc_guest = h_artikel = artikel = None

    pos_list = hbill_list = tline_list = None

    pos_list_list, Pos_list = create_model("Pos_list", {"dept":int, "rechnr":int, "confno":str, "profile":str, "tableno":str, "trdate":str, "paymentype":str, "gname":str, "comp":str, "email":str, "memberno":str, "fbrev":decimal, "others":decimal, "totrev":decimal, "propid":str, "reward":str, "bookdate":str, "exportdate":str, "programtype":str, "note":str}, {"paymentype": "6"})
    hbill_list_list, Hbill_list = create_model("Hbill_list", {"dept":int, "rechnr":int, "i_fact":int, "do_it":bool, "tot_sales":decimal, "i_ledger":int, "lname":str, "vorname1":str, "paymentype":int, "cardnum":str, "billname":str, "email":str}, {"do_it": True, "paymentype": 6})
    tline_list_list, Tline_list = create_model("Tline_list", {"datum":date, "artnr":int, "arttype":int, "rechnr":int, "reslinnr":int, "s_reslin":int, "dept":int, "bezeich":str, "price":decimal, "email":str, "paymentype":int, "zeit":int, "checkin":date, "checkout":date, "billname":str, "cardnum":str, "ankzeit":int, "abrezeit":int, "resnr":int, "breslin":int, "gastnr":int, "gastpay":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal pos_list_list, disc_food_art, disc_bev_art, disc_other_art, bill_datum, art_type, h_bill_line, h_bill, guest, mc_guest, h_artikel, artikel
        nonlocal datum, propid


        nonlocal pos_list, hbill_list, tline_list
        nonlocal pos_list_list, hbill_list_list, tline_list_list
        return {"pos-list": pos_list_list}

    def resto_transaction():

        nonlocal pos_list_list, disc_food_art, disc_bev_art, disc_other_art, bill_datum, art_type, h_bill_line, h_bill, guest, mc_guest, h_artikel, artikel
        nonlocal datum, propid


        nonlocal pos_list, hbill_list, tline_list
        nonlocal pos_list_list, hbill_list_list, tline_list_list

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr > 0) & (H_bill_line.bill_datum == bill_datum) & (H_bill_line.zeit >= 0) & (H_bill_line.artnr > 0) & (H_bill_line.betrag != 0)).order_by(H_bill_line.departement, H_bill_line.rechnr, H_bill_line.sysdate.desc(), H_bill_line.zeit.desc()).all():

            hbill_list = query(hbill_list_list, filters=(lambda hbill_list: hbill_list.dept == h_bill_line.departement and hbill_list.rechnr == h_bill_line.rechnr), first=True)

            if not hbill_list:

                h_bill = db_session.query(H_bill).filter(
                         (H_bill.rechnr == h_bill_line.rechnr) & (H_bill.departement == h_bill_line.departement) & (H_bill.flag == 1)).first()

                if h_bill:
                    hbill_list = Hbill_list()
                    hbill_list_list.append(hbill_list)

                    hbill_list.dept = h_bill_line.departement
                    hbill_list.rechnr = h_bill_line.rechnr

                    if re.match(r".*,.*",h_bill.bilname, re.IGNORECASE):
                        hbill_list.lname = entry(0, h_bill.bilname, ",")
                        hbill_list.vorname1 = entry(1, h_bill.bilname, ",")
                    else:
                        hbill_list.lname = h_bill.bilname
                    hbill_list.billname = h_bill.bilname

        for hbill_list in query(hbill_list_list, filters=(lambda hbill_list: hbill_list.lname != "")):

            guest = db_session.query(Guest).filter(
                     (Guest.name == hbill_list.lname) & (Guest.vorname1 == hbill_list.vorname1)).first()
            while None != guest :

                mc_guest = db_session.query(Mc_guest).filter(
                         (Mc_guest.gastnr == guest.gastnr) & (Mc_guest.cardnum != "")).first()

                if mc_guest:
                    hbill_list.cardnum = mc_guest.cardnum

                if guest.email_adr != "":
                    hbill_list.email = guest.email_adr

                curr_recid = guest._recid
                guest = db_session.query(Guest).filter(
                         (Guest.name == hbill_list.lname) & (Guest.vorname1 == hbill_list.vorname1)).filter(Guest._recid > curr_recid).first()

        for hbill_list in query(hbill_list_list, filters=(lambda hbill_list: hbill_list.do_it)):

            h_bill_line_obj_list = []
            for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.departement == H_bill_line.departement) & (H_artikel.artnr == H_bill_line.artnr) & (H_artikel.artart == 0)).filter(
                     (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.artnr > 0)).order_by(H_bill_line._recid).all():
                if h_bill_line._recid in h_bill_line_obj_list:
                    continue
                else:
                    h_bill_line_obj_list.append(h_bill_line._recid)


                hbill_list.tot_sales =  to_decimal(hbill_list.tot_sales) + to_decimal(h_bill_line.betrag)

        for hbill_list in query(hbill_list_list, filters=(lambda hbill_list: hbill_list.do_it  and hbill_list.tot_sales >= 0)):

            for h_bill_line in db_session.query(H_bill_line).filter(
                     (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.bill_datum == bill_datum)).order_by(H_bill_line._recid).all():

                if h_bill_line.artnr == 0:
                    hbill_list.paymentype = 0

                    if hbill_list.tot_sales * h_bill_line.betrag <= 0:

                        if hbill_list.i_fact <= 0:
                            hbill_list.i_fact = hbill_list.i_fact + 1
                    else:

                        if hbill_list.i_fact >= 0:
                            hbill_list.i_fact = hbill_list.i_fact - 1

                elif hbill_list.tot_sales == 0:

                    if hbill_list.tot_sales * h_bill_line.betrag <= 0:

                        if hbill_list.i_fact <= 0:
                            hbill_list.i_fact = hbill_list.i_fact + 1
                else:

                    h_artikel = db_session.query(H_artikel).filter(
                             (H_artikel.departement == h_bill_line.departement) & (H_artikel.artnr == h_bill_line.artnr)).first()

                    if h_artikel.artart == 2 or h_artikel.artart == 6 or h_artikel.artart == 7:

                        if re.match(r".*(Change).*",not h_bill_line.bezeich, re.IGNORECASE):

                            if h_artikel.artart == 2:
                                hbill_list.paymentype = 2

                                if h_bill_line.betrag < 0:
                                    hbill_list.i_ledger = hbill_list.i_ledger + 1
                                else:
                                    hbill_list.i_ledger = hbill_list.i_ledger - 1

                            if hbill_list.tot_sales * h_bill_line.betrag <= 0:

                                if h_artikel.artart == 7:
                                    hbill_list.paymentype = 7

                                if hbill_list.i_fact <= 0:
                                    hbill_list.i_fact = hbill_list.i_fact + 1
                            else:

                                if hbill_list.i_fact >= 0:
                                    hbill_list.i_fact = hbill_list.i_fact - 1

        for hbill_list in query(hbill_list_list, filters=(lambda hbill_list: hbill_list.do_it and hbill_list.i_fact > 0)):

            h_bill_line_obj_list = []
            for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0)).filter(
                     (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.artnr > 0)).order_by(H_bill_line._recid).all():
                if h_bill_line._recid in h_bill_line_obj_list:
                    continue
                else:
                    h_bill_line_obj_list.append(h_bill_line._recid)

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()

                if artikel.artart == 9:
                    art_type = 5

                elif artikel.artart == 0:

                    if artikel.umsatzart == 1:
                        art_type = 1
                    elif artikel.umsatzart == 2:
                        art_type = 1
                    elif artikel.umsatzart == 4:
                        art_type = 4
                    elif artikel.umsatzart == 5:
                        art_type = 2
                    elif artikel.umsatzart == 6:
                        art_type = 3
                    else:
                        art_type = 4

                if h_bill_line.artnr == disc_food_art or h_bill_line.artnr == disc_bev_art or h_bill_line.artnr == disc_other_art:

                    tline_list = query(tline_list_list, filters=(lambda tline_list: tline_list.rechnr == h_bill_line.rechnr and tline_list.artnr == disc_food_art and tline_list.dept == h_bill_line.departement), first=True)

                    if not tline_list:
                        tline_list = Tline_list()
                        tline_list_list.append(tline_list)

                        tline_list.arttype = art_type
                        tline_list.rechnr = h_bill_line.rechnr
                        tline_list.resnr = h_bill_line.tischnr
                        tline_list.artnr = disc_food_art
                        tline_list.dept = h_bill_line.departement
                        tline_list.bezeich = "Discount"
                        tline_list.datum = bill_datum
                        tline_list.zeit = h_bill_line.zeit
                        tline_list.email = hbill_list.email
                        tline_list.paymentype = hbill_list.paymentype
                        tline_list.billname = hbill_list.billname
                        tline_list.cardnum = hbill_list.cardnum


                    tline_list.price =  to_decimal(tline_list.price) - to_decimal(h_bill_line.betrag)


                else:

                    tline_list = query(tline_list_list, filters=(lambda tline_list: tline_list.rechnr == h_bill_line.rechnr and tline_list.artnr == h_bill_line.artnr and tline_list.bezeich == h_bill_line.bezeich and tline_list.dept == h_bill_line.departement), first=True)

                    if not tline_list:
                        tline_list = Tline_list()
                        tline_list_list.append(tline_list)

                        tline_list.arttype = art_type
                        tline_list.rechnr = h_bill_line.rechnr
                        tline_list.resnr = h_bill_line.tischnr
                        tline_list.artnr = h_bill_line.artnr
                        tline_list.dept = h_bill_line.departement
                        tline_list.bezeich = h_bill_line.bezeich
                        tline_list.datum = bill_datum
                        tline_list.zeit = h_bill_line.zeit
                        tline_list.email = hbill_list.email
                        tline_list.paymentype = hbill_list.paymentype
                        tline_list.billname = hbill_list.billname
                        tline_list.cardnum = hbill_list.cardnum


                    tline_list.price =  to_decimal(tline_list.price) + to_decimal(h_bill_line.betrag)


    def create_pos_list():

        nonlocal pos_list_list, disc_food_art, disc_bev_art, disc_other_art, bill_datum, art_type, h_bill_line, h_bill, guest, mc_guest, h_artikel, artikel
        nonlocal datum, propid


        nonlocal pos_list, hbill_list, tline_list
        nonlocal pos_list_list, hbill_list_list, tline_list_list

        for tline_list in query(tline_list_list, filters=(lambda tline_list: tline_list.price > 0), sort_by=[("dept",False),("rechnr",False)]):
            tline_list.bezeich = replace_str(tline_list.bezeich, "|", "")

            pos_list = query(pos_list_list, filters=(lambda pos_list: pos_list.dept == tline_list.dept and pos_list.rechnr == tline_list.rechnr), first=True)

            if not pos_list:
                pos_list = Pos_list()
                pos_list_list.append(pos_list)

                pos_list.rechnr = tline_list.rechnr
                pos_list.dept = tline_list.dept
                pos_list.confno = propid + "-" + to_string(tline_list.dept, "99") + "-" + to_string(tline_list.rechnr)
                pos_list.profile = ""
                pos_list.tableno = to_string(tline_list.resnr)
                pos_list.trdate = to_string(get_year(bill_datum) , "9999") + "-" + to_string(get_month(bill_datum) , "99") + "-" + to_string(get_day(bill_datum) , "99")
                pos_list.paymentype = to_string(tline_list.paymentype)
                pos_list.gname = tline_list.billname
                pos_list.comp = ""
                pos_list.email = tline_list.email
                pos_list.memberno = tline_list.cardnum
                pos_list.propid = propid
                pos_list.programtype = ""
                pos_list.exportdate = to_string(get_year(get_current_date()) , "9999") + "-" + to_string(get_month(get_current_date()) , "99") + "-" + to_string(get_day(get_current_date()) , "99")
                pos_list.bookdate = ""
                pos_list.note = ""

                if tline_list.paymentype == 0:
                    pos_list.reward = "2"
                else:
                    pos_list.reward = "5"

            if tline_list.dept >= 1 and tline_list.bezeich.lower()  == ("Discount").lower() :
                pos_list.totrev =  to_decimal(pos_list.totrev) - to_decimal(tline_list.price)


            else:
                pos_list.totrev =  to_decimal(pos_list.totrev) + to_decimal(tline_list.price)

            if pos_list.dept == 1:
                pos_list.fbrev =  to_decimal(pos_list.totrev)
            else:
                pos_list.others =  to_decimal(pos_list.totrev)

    disc_other_art = get_output(htpint(556))
    disc_food_art = get_output(htpint(557))
    disc_bev_art = get_output(htpint(596))
    bill_datum = datum
    resto_transaction()
    create_pos_list()

    return generate_output()