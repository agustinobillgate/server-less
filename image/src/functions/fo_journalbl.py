from functions.additional_functions import *
import decimal
from datetime import date
import re
from sqlalchemy import func
from models import Guest, Artikel, Hoteldpt, Billjournal, Bill, H_bill, Bk_veran, Reservation, Res_line

def fo_journalbl(from_art:int, to_art:int, from_dept:int, to_dept:int, from_date:date, to_date:date, sorttype:int, exclude_artrans:bool, long_digit:bool, foreign_flag:bool, mi_onlyjournal:bool, mi_excljournal:bool, mi_post:bool):
    gtot = 0
    output_list_list = []
    curr_date:date = None
    descr1:str = ""
    voucher_no:str = ""
    ind:int = 0
    gdelimiter:str = ""
    roomnumber:str = ""
    zinrdate:date = None
    billnumber:int = 0
    guest = artikel = hoteldpt = billjournal = bill = h_bill = bk_veran = reservation = res_line = None

    output_list = gbuff = None

    output_list_list, Output_list = create_model("Output_list", {"bezeich":str, "c":str, "ns":str, "mb":str, "shift":str, "dept":str, "str":str, "remark":str, "gname":str, "descr":str, "voucher":str})

    Gbuff = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gtot, output_list_list, curr_date, descr1, voucher_no, ind, gdelimiter, roomnumber, zinrdate, billnumber, guest, artikel, hoteldpt, billjournal, bill, h_bill, bk_veran, reservation, res_line
        nonlocal gbuff


        nonlocal output_list, gbuff
        nonlocal output_list_list
        return {"gtot": gtot, "output-list": output_list_list}

    def journal_list():

        nonlocal gtot, output_list_list, curr_date, descr1, voucher_no, ind, gdelimiter, roomnumber, zinrdate, billnumber, guest, artikel, hoteldpt, billjournal, bill, h_bill, bk_veran, reservation, res_line
        nonlocal gbuff


        nonlocal output_list, gbuff
        nonlocal output_list_list

        qty:int = 0
        sub_tot:decimal = 0
        tot:decimal = 0
        curr_date:date = None
        last_dept:int = -1
        it_exist:bool = False
        lviresnr:int = -1
        lvcs:str = ""
        amount:decimal = 0
        s:str = ""
        cnt:int = 0
        i:int = 0
        gqty:int = 0
        do_it:bool = True
        deptname:str = ""
        Gbuff = Guest
        output_list_list.clear()

        for artikel in db_session.query(Artikel).filter(
                (Artikel.artnr >= from_art) &  (Artikel.artnr <= to_art) &  (Artikel.departement >= from_dept) &  (Artikel.departement <= to_dept)).all():

            if last_dept != artikel.departement:

                hoteldpt = db_session.query(Hoteldpt).filter(
                        (Hoteldpt.num == artikel.departement)).first()
            last_dept = artikel.departement
            sub_tot = 0
            it_exist = False
            qty = 0
            for curr_date in range(from_date,to_date + 1) :

                if sorttype == 0:

                    for billjournal in db_session.query(Billjournal).filter(
                            (Billjournal.artnr == artikel.artnr) &  (Billjournal.departement == artikel.departement) &  (Billjournal.bill_datum == curr_date) &  (Billjournal.anzahl != 0)).all():
                        it_exist = True
                        do_it = True

                        if exclude_artrans and billjournal.kassarapport:
                            do_it = False

                        if do_it:

                            if (billjournal.bediener_nr == 0 and mi_onlyjournal == False) or (billjournal.bediener_nr != 0 and mi_excljournal == False):
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.remark = billjournal.stornogrund

                            if not re.match(".*<.*",billjournal.bezeich) and not re.match(".*>.*",billjournal.bezeich):

                                if billjournal.rechnr > 0:

                                    if billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                        bill = db_session.query(Bill).filter(
                                                (Bill.rechnr == billjournal.rechnr)).first()

                                        if bill:

                                            if bill.resnr == 0 and bill.bilname != "":
                                                output_list.gname = bill.bilname
                                            else:

                                                gbuff = db_session.query(Gbuff).filter(
                                                        (Gbuff.gastnr == bill.gastnr)).first()

                                                if gbuff:
                                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                                    elif billjournal.bediener_nr != 0 and mi_excljournal == False:

                                        h_bill = db_session.query(H_bill).filter(
                                                (H_bill.rechnr == billjournal.rechnr) &  (H_bill.departement == billjournal.betriebsnr)).first()

                                        if h_bill:
                                            output_list.gname = h_bill.bilname
                                else:
                                    IF1 + get_index(billjournal.bezeich, " *BQT") > 0 THEN

                                    bk_veran = db_session.query(Bk_veran).filter(
                                                (Bk_veran.veran_nr == to_int(substring(billjournal.bezeich,0 + get_index(billjournal.bezeich, " *BQT") + 5)))).first()

                                    if bk_veran:

                                        gbuff = db_session.query(Gbuff).filter(
                                                    (Gbuff.gastnr == bk_veran.gastnr)).first()

                                        if gbuff:
                                            output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                                    elif artikel.artart == 5 AND1 + get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                                        lviresnr = -1
                                        lvcs = substring(billjournal.bezeich,0 + get_index(billjournal.bezeich, "[#") + 2)
                                        lviresnr = to_int(entry(0, lvcs, " "))

                                        reservation = db_session.query(Reservation).filter(
                                                (Reservation.resnr == lviresnr)).first()

                                        if reservation:

                                            gbuff = db_session.query(Gbuff).filter(
                                                    (Gbuff.gastnr == reservation.gastnr)).first()

                                            if gbuff:
                                                output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                    ELSE IF1 + get_index(billjournal.bezeich, " #") > 0 and billjournal.departement = 0 THEN
                                    lvcs = substring(billjournal.bezeich,0 + get_index(billjournal.bezeich, " #") + 2)
                                    lviresnr = to_int(entry(0, lvcs, "]"))

                                    reservation = db_session.query(Reservation).filter(
                                                (Reservation.resnr == lviresnr)).first()

                                    if reservation:

                                        gbuff = db_session.query(Gbuff).filter(
                                                    (Gbuff.gastnr == reservation.gastnr)).first()

                                        if gbuff:
                                            output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                pass

                            if (billjournal.bediener_nr != 0 and mi_excljournal == False and billjournal.anzahl == 0) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False and billjournal.anzahl == 0):
                                output_list.bezeich = artikel.bezeich

                            if billjournal.bediener_nr != 0 and mi_excljournal == False:
                                output_list.c = to_string(billjournal.betriebsnr, "99")
                                output_list.shift = to_string(billjournal.betriebsnr, "99")

                            elif billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                if bill:

                                    if bill.reslinnr == 1 and bill.zinr == "":
                                        output_list.c = "N"
                                        output_list.NS = "*"

                                    elif bill.reslinnr == 0:
                                        output_list.c = "M"
                                        output_list.MB = "*"

                            if foreign_flag:
                                amount = billjournal.fremdwaehrng
                            else:
                                amount = billjournal.betrag
                            descr1 = ""
                            voucher_no = ""

                            if substring(billjournal.bezeich, 0, 1) == "*" or billjournal.kassarapport:
                                descr1 = billjournal.bezeich
                                voucher_no = ""


                            else:

                                if not artikel.bezaendern:
                                    ind = 1 + get_index(billjournal.bezeich, "/")

                                    if ind != 0:
                                        gdelimiter = "/"
                                    else:
                                        ind = 1 + get_index(billjournal.bezeich, "]")

                                        if ind != 0:
                                            gdelimiter = "]"

                                    if ind != 0:

                                        if ind > len(artikel.bezeich):
                                            descr1 = entry(0, billjournal.bezeich, gdelimiter)
                                            voucher_no = substring(billjournal.bezeich, (ind + 1) - 1)


                                        else:
                                            cnt = num_entries(artikel.bezeich, gdelimiter)
                                            for i in range(1,cnt + 1) :

                                                if descr1 == "":
                                                    descr1 = entry(i - 1, billjournal.bezeich, gdelimiter)
                                                else:
                                                    descr1 = descr1 + "/" + entry(i - 1, billjournal.bezeich, gdelimiter)
                                            voucher_no = substring(billjournal.bezeich, len(descr1) + 2 - 1)

                                        if gdelimiter.lower()  == "]":
                                            descr1 = descr1 + gdelimiter
                                    else:
                                        descr1 = billjournal.bezeich
                                else:
                                    ind = num_entries(billjournal.bezeich, "/")

                                    if ind == 1:
                                        descr1 = billjournal.bezeich
                                        voucher_no = ""


                                    else:
                                        descr1 = entry(ind - 1 - 1, billjournal.bezeich, "/")
                                        voucher_no = entry(ind - 1, billjournal.bezeich, "/")

                                if artikel.bezaendern:
                                    ind = num_entries(billjournal.bezeich, "]")

                                    if ind == 1:
                                        descr1 = billjournal.bezeich
                                        voucher_no = ""


                                    else:
                                        descr1 = entry(ind - 1 - 1, billjournal.bezeich, "]")
                                        voucher_no = entry(ind - 1, billjournal.bezeich, "]")

                            if output_list:
                                output_list.descr = to_string(descr1, "x(100)")
                                output_list.voucher = to_string(voucher_no, "x(20)")

                            if billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                hoteldpt = db_session.query(Hoteldpt).filter(
                                        (Hoteldpt.num == billjournal.departement)).first()

                                if hoteldpt:
                                    deptname = hoteldpt.depart

                                if not long_digit:
                                    STR = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, ">>>9") + to_string(descr1, "x(50)") + to_string(deptname, "x(12)") + to_string("", "x(6)") + to_string(billjournal.anzahl, "->>>9") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                else:
                                    STR = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, ">>>9") + to_string(billjournal.bezeich, "x(50)") + to_string(deptname, "x(12)") + to_string("", "x(6)") + to_string(billjournal.anzahl, "->>>9") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                qty = qty + billjournal.anzahl
                                gqty = gqty + billjournal.anzahl
                                roomnumber = substring(output_list.STR, 8, 6)
                                zinrdate = date_mdy(substring(output_list.STR, 0, 8))
                                billnumber = to_int(substring(output_list.STR, 14, 9))

                                bill = db_session.query(Bill).filter(
                                        (Bill.rechnr == billnumber)).first()

                                res_line = db_session.query(Res_line).filter(
                                        (Res_line.resnr == bill.resnr) &  (func.lower(Res_line.zinr) == (roomnumber).lower())).first()

                                guest = db_session.query(Guest).filter(
                                        (Guest.gastnr == res_line.gastnrmember)).first()

                                if guest:
                                    output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1

                                if foreign_flag:
                                    sub_tot = sub_tot + billjournal.fremdwaehrng
                                    tot = tot + billjournal.fremdwaehrng
                                else:
                                    sub_tot = sub_tot + billjournal.betrag
                                    tot = tot + billjournal.betrag

                            elif billjournal.bediener_nr != 0 and mi_excljournal == False:

                                hoteldpt = db_session.query(Hoteldpt).filter(
                                        (Hoteldpt.num == billjournal.departement)).first()

                                if hoteldpt:
                                    deptname = hoteldpt.depart

                                if not long_digit:
                                    STR = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, ">>>9") + to_string(descr1, "x(50)") + to_string(deptname, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "->>>9") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                else:
                                    STR = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, ">>>9") + to_string(billjournal.bezeich, "x(50)") + to_string(deptname, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "->>>9") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                qty = qty + billjournal.anzahl
                                gqty = gqty + billjournal.anzahl
                                roomnumber = substring(output_list.STR, 8, 6)
                                zinrdate = date_mdy(substring(output_list.STR, 0, 8))
                                billnumber = to_int(substring(output_list.STR, 14, 9))

                                bill = db_session.query(Bill).filter(
                                        (Bill.rechnr == billnumber)).first()

                                res_line = db_session.query(Res_line).filter(
                                        (Res_line.resnr == bill.resnr) &  (func.lower(Res_line.zinr) == (roomnumber).lower())).first()

                                guest = db_session.query(Guest).filter(
                                        (Guest.gastnr == res_line.gastnrmember)).first()

                                if guest:
                                    output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1

                                if foreign_flag:
                                    sub_tot = sub_tot + billjournal.fremdwaehrng
                                    tot = tot + billjournal.fremdwaehrng
                                else:
                                    sub_tot = sub_tot + billjournal.betrag
                                    tot = tot + billjournal.betrag


                elif sorttype == 1:

                    for billjournal in db_session.query(Billjournal).filter(
                            (Billjournal.artnr == artikel.artnr) &  (Billjournal.departement == artikel.departement) &  (Billjournal.bill_datum == curr_date)).all():
                        it_exist = True
                        do_it = True

                        if exclude_artrans and billjournal.kassarapport:
                            do_it = False

                        if do_it:

                            if (billjournal.bediener_nr != 0 and mi_excljournal == False) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False):
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.remark = billjournal.stornogrund

                            if not re.match(".*<.*",billjournal.bezeich) and not re.match(".*>.*",billjournal.bezeich):

                                if billjournal.rechnr > 0:

                                    bill = db_session.query(Bill).filter(
                                            (Bill.rechnr == billjournal.rechnr)).first()

                                    if bill:

                                        if (billjournal.bediener_nr != 0 and mi_excljournal == False) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False):

                                            if bill.resnr == 0 and bill.bilname != "":
                                                output_list.gname = bill.bilname
                                            else:

                                                gbuff = db_session.query(Gbuff).filter(
                                                        (Gbuff.gastnr == bill.gastnr)).first()

                                                if gbuff:
                                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                else:

                                    if artikel.artart == 5 AND1 + get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                                        lviresnr = -1
                                        lvcs = substring(billjournal.bezeich,0 + get_index(billjournal.bezeich, "[#") + 2)
                                        lviresnr = to_int(entry(0, lvcs, " "))

                                        reservation = db_session.query(Reservation).filter(
                                                (Reservation.resnr == lviresnr)).first()

                                        if reservation:

                                            gbuff = db_session.query(Gbuff).filter(
                                                    (Gbuff.gastnr == reservation.gastnr)).first()

                                            if gbuff:
                                                output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                    ELSE IF1 + get_index(billjournal.bezeich, " #") > 0 and billjournal.departement = 0 THEN
                                    lvcs = substring(billjournal.bezeich,0 + get_index(billjournal.bezeich, " #") + 2)
                                    lviresnr = to_int(entry(0, lvcs, "]"))

                                    reservation = db_session.query(Reservation).filter(
                                                (Reservation.resnr == lviresnr)).first()

                                    if reservation:

                                        gbuff = db_session.query(Gbuff).filter(
                                                    (Gbuff.gastnr == reservation.gastnr)).first()

                                        if gbuff:
                                            output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                pass

                            if (billjournal.bediener_nr != 0 and mi_excljournal == False and billjournal.anzahl == 0) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False and billjournal.anzahl == 0):
                                output_list.bezeich = artikel.bezeich

                            if billjournal.bediener_nr != 0 and mi_excljournal == False:
                                output_list.shift = to_string(billjournal.betriebsnr, "99")
                                output_list.c = to_string(billjournal.betriebsnr, "99")

                            elif billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                if bill:

                                    if bill.reslinnr == 1 and bill.zinr == "":
                                        output_list.c = "N"
                                        output_list.NS = "*"

                                    elif bill.reslinnr == 0:
                                        output_list.c = "M"
                                        output_list.MB = "*"

                            if foreign_flag:
                                amount = billjournal.fremdwaehrng
                            else:
                                amount = billjournal.betrag
                            descr1 = ""
                            voucher_no = ""

                            if substring(billjournal.bezeich, 0, 1) == "*" or billjournal.kassarapport:
                                descr1 = billjournal.bezeich
                                voucher_no = ""


                            else:

                                if not artikel.bezaendern:
                                    ind = 1 + get_index(billjournal.bezeich, "/")

                                    if ind != 0:
                                        gdelimiter = "/"
                                    else:
                                        ind = 1 + get_index(billjournal.bezeich, "]")

                                        if ind != 0:
                                            gdelimiter = "]"

                                    if ind != 0:

                                        if ind > len(artikel.bezeich):
                                            descr1 = entry(0, billjournal.bezeich, gdelimiter)
                                            voucher_no = substring(billjournal.bezeich, (ind + 1) - 1)


                                        else:
                                            cnt = num_entries(artikel.bezeich, gdelimiter)
                                            for i in range(1,cnt + 1) :

                                                if descr1 == "":
                                                    descr1 = entry(i - 1, billjournal.bezeich, gdelimiter)
                                                else:
                                                    descr1 = descr1 + "/" + entry(i - 1, billjournal.bezeich, gdelimiter)
                                            voucher_no = substring(billjournal.bezeich, len(descr1) + 2 - 1)

                                        if gdelimiter.lower()  == "]":
                                            descr1 = descr1 + gdelimiter
                                    else:
                                        descr1 = billjournal.bezeich
                                else:
                                    ind = num_entries(billjournal.bezeich, "/")

                                    if ind == 1:
                                        descr1 = billjournal.bezeich
                                        voucher_no = ""


                                    else:
                                        descr1 = entry(ind - 1 - 1, billjournal.bezeich, "/")
                                        voucher_no = entry(ind - 1, billjournal.bezeich, "/")

                            if output_list:
                                output_list.descr = to_string(descr1, "x(100)")
                                output_list.voucher = to_string(voucher_no, "x(20)")

                            if billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                if not long_digit:
                                    STR = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, ">>>9") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string("", "x(6)") + to_string(billjournal.anzahl, "->>>9") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                else:
                                    STR = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, ">>>9") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string("", "x(6)") + to_string(billjournal.anzahl, "->>>9") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                qty = qty + billjournal.anzahl
                                gqty = gqty + billjournal.anzahl
                                roomnumber = substring(output_list.STR, 8, 6)
                                zinrdate = date_mdy(substring(output_list.STR, 0, 8))
                                billnumber = to_int(substring(output_list.STR, 14, 9))

                                bill = db_session.query(Bill).filter(
                                        (Bill.rechnr == billnumber)).first()

                                res_line = db_session.query(Res_line).filter(
                                        (Res_line.resnr == bill.resnr) &  (func.lower(Res_line.zinr) == (roomnumber).lower())).first()

                                guest = db_session.query(Guest).filter(
                                        (Guest.gastnr == res_line.gastnrmember)).first()

                                if guest:
                                    output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1

                                if foreign_flag:
                                    sub_tot = sub_tot + billjournal.fremdwaehrng
                                    tot = tot + billjournal.fremdwaehrng
                                else:
                                    sub_tot = sub_tot + billjournal.betrag
                                    tot = tot + billjournal.betrag

                            elif billjournal.bediener_nr != 0 and mi_excljournal == False:

                                if not long_digit:
                                    STR = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, ">>>9") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "->>>9") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                else:
                                    STR = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, ">>>9") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "->>>9") + to_string(amount, "->>,>>>,>>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                qty = qty + billjournal.anzahl
                                gqty = gqty + billjournal.anzahl
                                roomnumber = substring(output_list.STR, 8, 6)
                                zinrdate = date_mdy(substring(output_list.STR, 0, 8))
                                billnumber = to_int(substring(output_list.STR, 14, 9))

                                bill = db_session.query(Bill).filter(
                                        (Bill.rechnr == billnumber)).first()

                                res_line = db_session.query(Res_line).filter(
                                        (Res_line.resnr == bill.resnr) &  (func.lower(Res_line.zinr) == (roomnumber).lower())).first()

                                guest = db_session.query(Guest).filter(
                                        (Guest.gastnr == res_line.gastnrmember)).first()

                                if guest:
                                    output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1

                                if foreign_flag:
                                    sub_tot = sub_tot + billjournal.fremdwaehrng
                                    tot = tot + billjournal.fremdwaehrng
                                else:
                                    sub_tot = sub_tot + billjournal.betrag
                                    tot = tot + billjournal.betrag


                elif sorttype == 2:

                    if mi_post :

                        for billjournal in db_session.query(Billjournal).filter(
                                (Billjournal.artnr == artikel.artnr) &  (Billjournal.departement == artikel.departement) &  (Billjournal.bill_datum == curr_date) &  (Billjournal.anzahl == 0)).all():
                            it_exist = True
                            do_it = True

                            if exclude_artrans and billjournal.kassarapport:
                                do_it = False

                            if do_it:

                                if (billjournal.bediener_nr != 0 and mi_excljournal == False) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False):
                                    output_list = Output_list()
                                    output_list_list.append(output_list)

                                    output_list.remark = billjournal.stornogrund

                                if not re.match(".*<.*",billjournal.bezeich) and not re.match(".*>.*",billjournal.bezeich):

                                    if billjournal.rechnr > 0:

                                        bill = db_session.query(Bill).filter(
                                                (Bill.rechnr == billjournal.rechnr)).first()

                                        if bill:

                                            if (billjournal.bediener_nr != 0 and mi_excljournal == False) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False):

                                                if bill.resnr == 0 and bill.bilname != "":
                                                    output_list.gname = bill.bilname
                                                else:

                                                    gbuff = db_session.query(Gbuff).filter(
                                                            (Gbuff.gastnr == bill.gastnr)).first()

                                                    if gbuff:
                                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                    else:

                                        if artikel.artart == 5 AND1 + get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                                            lviresnr = -1
                                            lvcs = substring(billjournal.bezeich,0 + get_index(billjournal.bezeich, "[#") + 2)
                                            lviresnr = to_int(entry(0, lvcs, " "))

                                            reservation = db_session.query(Reservation).filter(
                                                    (Reservation.resnr == lviresnr)).first()

                                            if reservation:

                                                gbuff = db_session.query(Gbuff).filter(
                                                        (Gbuff.gastnr == reservation.gastnr)).first()

                                                if gbuff:
                                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                        ELSE IF1 + get_index(billjournal.bezeich, " #") > 0 and billjournal.departement = 0 THEN
                                        lvcs = substring(billjournal.bezeich,0 + get_index(billjournal.bezeich, " #") + 2)
                                        lviresnr = to_int(entry(0, lvcs, "]"))

                                        reservation = db_session.query(Reservation).filter(
                                                    (Reservation.resnr == lviresnr)).first()

                                        if reservation:

                                            gbuff = db_session.query(Gbuff).filter(
                                                        (Gbuff.gastnr == reservation.gastnr)).first()

                                            if gbuff:
                                                output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                else:
                                    pass

                                if (billjournal.bediener_nr != 0 and mi_excljournal == False and billjournal.anzahl == 0) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False and billjournal.anzahl == 0):
                                    output_list.bezeich = artikel.bezeich

                                if billjournal.bediener_nr != 0 and mi_excljournal == False:
                                    output_list.shift = to_string(billjournal.betriebsnr, "99")
                                    output_list.c = to_string(billjournal.betriebsnr, "99")

                                elif billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                    if bill:

                                        if bill.reslinnr == 1 and bill.zinr == "":
                                            output_list.c = "N"
                                            output_list.NS = "*"

                                        elif bill.reslinnr == 0:
                                            output_list.c = "M"
                                            output_list.MB = "*"

                                if foreign_flag:
                                    amount = billjournal.fremdwaehrng
                                else:
                                    amount = billjournal.betrag
                                descr1 = ""
                                voucher_no = ""

                                if substring(billjournal.bezeich, 0, 1) == "*" or billjournal.kassarapport:
                                    descr1 = billjournal.bezeich
                                    voucher_no = ""


                                else:

                                    if not artikel.bezaendern:
                                        ind = 1 + get_index(billjournal.bezeich, "/")

                                        if ind != 0:
                                            gdelimiter = "/"
                                        else:
                                            ind = 1 + get_index(billjournal.bezeich, "]")

                                            if ind != 0:
                                                gdelimiter = "]"

                                        if ind != 0:

                                            if ind > len(artikel.bezeich):
                                                descr1 = entry(0, billjournal.bezeich, gdelimiter)
                                                voucher_no = substring(billjournal.bezeich, (ind + 1) - 1)


                                            else:
                                                cnt = num_entries(artikel.bezeich, gdelimiter)
                                                for i in range(1,cnt + 1) :

                                                    if descr1 == "":
                                                        descr1 = entry(i - 1, billjournal.bezeich, gdelimiter)
                                                    else:
                                                        descr1 = descr1 + "/" + entry(i - 1, billjournal.bezeich, gdelimiter)
                                                voucher_no = substring(billjournal.bezeich, len(descr1) + 2 - 1)

                                            if gdelimiter.lower()  == "]":
                                                descr1 = descr1 + gdelimiter
                                        else:
                                            descr1 = billjournal.bezeich
                                    else:
                                        ind = num_entries(billjournal.bezeich, "/")

                                        if ind == 1:
                                            descr1 = billjournal.bezeich
                                            voucher_no = ""


                                        else:
                                            descr1 = entry(ind - 1 - 1, billjournal.bezeich, "/")
                                            voucher_no = entry(ind - 1, billjournal.bezeich, "/")

                                if output_list:
                                    output_list.descr = to_string(descr1, "x(100)")
                                    output_list.voucher = to_string(voucher_no, "x(20)")

                                if billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                    if not long_digit:
                                        STR = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, ">>>9") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string("", "x(6)") + to_string(billjournal.anzahl, "->>>9") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                    else:
                                        STR = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, ">>>9") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string("", "x(6)") + to_string(billjournal.anzahl, "->>>9") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                    qty = qty + billjournal.anzahl
                                    gqty = gqty + billjournal.anzahl
                                    roomnumber = substring(output_list.STR, 8, 6)
                                    zinrdate = date_mdy(substring(output_list.STR, 0, 8))
                                    billnumber = to_int(substring(output_list.STR, 14, 9))

                                    bill = db_session.query(Bill).filter(
                                            (Bill.rechnr == billnumber)).first()

                                    res_line = db_session.query(Res_line).filter(
                                            (Res_line.resnr == bill.resnr) &  (func.lower(Res_line.zinr) == (roomnumber).lower())).first()

                                    guest = db_session.query(Guest).filter(
                                            (Guest.gastnr == res_line.gastnrmember)).first()

                                    if guest:
                                        output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1

                                    if foreign_flag:
                                        sub_tot = sub_tot + billjournal.fremdwaehrng
                                        tot = tot + billjournal.fremdwaehrng
                                    else:
                                        sub_tot = sub_tot + billjournal.betrag
                                        tot = tot + billjournal.betrag

                                elif billjournal.bediener_nr != 0 and mi_excljournal == False:

                                    if not long_digit:
                                        STR = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, ">>>9") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "->>>9") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                    else:
                                        STR = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, ">>>9") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "->>>9") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                    qty = qty + billjournal.anzahl
                                    gqty = gqty + billjournal.anzahl
                                    roomnumber = substring(output_list.STR, 8, 6)
                                    zinrdate = date_mdy(substring(output_list.STR, 0, 8))
                                    billnumber = to_int(substring(output_list.STR, 14, 9))

                                    bill = db_session.query(Bill).filter(
                                            (Bill.rechnr == billnumber)).first()

                                    res_line = db_session.query(Res_line).filter(
                                            (Res_line.resnr == bill.resnr) &  (func.lower(Res_line.zinr) == (roomnumber).lower())).first()

                                    guest = db_session.query(Guest).filter(
                                            (Guest.gastnr == res_line.gastnrmember)).first()

                                    if guest:
                                        output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1

                                    if foreign_flag:
                                        sub_tot = sub_tot + billjournal.fremdwaehrng
                                        tot = tot + billjournal.fremdwaehrng
                                    else:
                                        sub_tot = sub_tot + billjournal.betrag
                                        tot = tot + billjournal.betrag

                    else:

                        for billjournal in db_session.query(Billjournal).filter(
                                (Billjournal.artnr == artikel.artnr) &  (Billjournal.departement == artikel.departement) &  (Billjournal.sysdate == curr_date) &  (Billjournal.anzahl == 0)).all():
                            it_exist = True
                            do_it = True

                            if exclude_artrans and billjournal.kassarapport:
                                do_it = False

                            if do_it:

                                if (billjournal.bediener_nr != 0 and mi_excljournal == False) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False):
                                    output_list = Output_list()
                                    output_list_list.append(output_list)

                                    output_list.remark = billjournal.stornogrund

                                if not re.match(".*<.*",billjournal.bezeich) and not re.match(".*>.*",billjournal.bezeich):

                                    bill = db_session.query(Bill).filter(
                                            (Bill.rechnr == billjournal.rechnr)).first()

                                    if bill:

                                        if (billjournal.bediener_nr != 0 and mi_excljournal == False) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False):

                                            if bill.resnr == 0 and bill.bilname != "":
                                                output_list.gname = bill.bilname
                                            else:

                                                gbuff = db_session.query(Gbuff).filter(
                                                        (Gbuff.gastnr == bill.gastnr)).first()

                                                if gbuff:
                                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                else:
                                    pass

                                if (billjournal.bediener_nr != 0 and mi_excljournal == False and billjournal.anzahl == 0) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False and billjournal.anzahl == 0):
                                    output_list.bezeich = artikel.bezeich

                                if billjournal.bediener_nr != 0 and mi_excljournal == False:
                                    output_list.shift = to_string(billjournal.betriebsnr, "99")
                                    output_list.c = to_string(billjournal.betriebsnr, "99")

                                elif billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                    if bill:

                                        if bill.reslinnr == 1 and bill.zinr == "":
                                            output_list.NS = "*"
                                            output_list.c = "N"

                                        elif bill.reslinnr == 0:
                                            output_list.c = "M"
                                            output_list.MB = "*"

                                if foreign_flag:
                                    amount = billjournal.fremdwaehrng
                                else:
                                    amount = billjournal.betrag
                                descr1 = ""
                                voucher_no = ""

                                if substring(billjournal.bezeich, 0, 1) == "*" or billjournal.kassarapport:
                                    descr1 = billjournal.bezeich
                                    voucher_no = ""


                                else:

                                    if not artikel.bezaendern:
                                        ind = 1 + get_index(billjournal.bezeich, "/")

                                        if ind != 0:
                                            gdelimiter = "/"
                                        else:
                                            ind = 1 + get_index(billjournal.bezeich, "]")

                                            if ind != 0:
                                                gdelimiter = "]"

                                        if ind != 0:

                                            if ind > len(artikel.bezeich):
                                                descr1 = entry(0, billjournal.bezeich, gdelimiter)
                                                voucher_no = substring(billjournal.bezeich, (ind + 1) - 1)


                                            else:
                                                cnt = num_entries(artikel.bezeich, gdelimiter)
                                                for i in range(1,cnt + 1) :

                                                    if descr1 == "":
                                                        descr1 = entry(i - 1, billjournal.bezeich, gdelimiter)
                                                    else:
                                                        descr1 = descr1 + "/" + entry(i - 1, billjournal.bezeich, gdelimiter)
                                                voucher_no = substring(billjournal.bezeich, len(descr1) + 2 - 1)

                                            if gdelimiter.lower()  == "]":
                                                descr1 = descr1 + gdelimiter
                                        else:
                                            descr1 = billjournal.bezeich
                                    else:
                                        ind = num_entries(billjournal.bezeich, "/")

                                        if ind == 1:
                                            descr1 = billjournal.bezeich
                                            voucher_no = ""


                                        else:
                                            descr1 = entry(ind - 1 - 1, billjournal.bezeich, "/")
                                            voucher_no = entry(ind - 1, billjournal.bezeich, "/")

                                if output_list:
                                    output_list.descr = to_string(descr1, "x(100)")
                                    output_list.voucher = to_string(voucher_no, "x(20)")

                                if (billjournal.bediener_nr != 0 and mi_excljournal == False) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False):

                                    if not long_digit:
                                        STR = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, ">>>9") + to_string(billjournal.bezeich, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string("", "x(6)") + to_string(billjournal.anzahl, "->>>9") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate)
                                    else:
                                        STR = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, ">>>9") + to_string(billjournal.bezeich, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string("", "x(6)") + to_string(billjournal.anzahl, "->>>9") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate)
                                    qty = qty + billjournal.anzahl
                                    gqty = gqty + billjournal.anzahl
                                    roomnumber = substring(output_list.STR, 8, 6)
                                    zinrdate = date_mdy(substring(output_list.STR, 0, 8))
                                    billnumber = to_int(substring(output_list.STR, 14, 9))

                                    bill = db_session.query(Bill).filter(
                                            (Bill.rechnr == billnumber)).first()

                                    res_line = db_session.query(Res_line).filter(
                                            (Res_line.resnr == bill.resnr) &  (func.lower(Res_line.zinr) == (roomnumber).lower())).first()

                                    guest = db_session.query(Guest).filter(
                                            (Guest.gastnr == res_line.gastnrmember)).first()

                                    if guest:
                                        output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1

                                    if foreign_flag:
                                        sub_tot = sub_tot + billjournal.fremdwaehrng
                                        tot = tot + billjournal.fremdwaehrng
                                    else:
                                        sub_tot = sub_tot + billjournal.betrag
                                        tot = tot + billjournal.betrag

                                elif billjournal.bediener_nr != 0 and mi_excljournal == False:

                                    if not long_digit:
                                        STR = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, ">>>9") + to_string(billjournal.bezeich, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "->>>9") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate)
                                    else:
                                        STR = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, ">>>9") + to_string(billjournal.bezeich, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "->>>9") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate)
                                    qty = qty + billjournal.anzahl
                                    gqty = gqty + billjournal.anzahl
                                    roomnumber = substring(output_list.STR, 8, 6)
                                    zinrdate = date_mdy(substring(output_list.STR, 0, 8))
                                    billnumber = to_int(substring(output_list.STR, 14, 9))

                                    bill = db_session.query(Bill).filter(
                                            (Bill.rechnr == billnumber)).first()

                                    res_line = db_session.query(Res_line).filter(
                                            (Res_line.resnr == bill.resnr) &  (func.lower(Res_line.zinr) == (roomnumber).lower())).first()

                                    guest = db_session.query(Guest).filter(
                                            (Guest.gastnr == res_line.gastnrmember)).first()

                                    if guest:
                                        output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1

                                    if foreign_flag:
                                        sub_tot = sub_tot + billjournal.fremdwaehrng
                                        tot = tot + billjournal.fremdwaehrng
                                    else:
                                        sub_tot = sub_tot + billjournal.betrag
                                        tot = tot + billjournal.betrag


            if it_exist:
                output_list = Output_list()
                output_list_list.append(output_list)


                if not long_digit:
                    STR = to_string("", "x(77)") + to_string("T O T A L   ", "x(12)") + to_string("", "x(6)") + to_string(qty, "->>>9") + to_string(sub_tot, "->>,>>>,>>>,>>>,>>9.99")
                else:
                    STR = to_string("", "x(77)") + to_string("T O T A L   ", "x(12)") + to_string("", "x(6)") + to_string(qty, "->>>9") + to_string(sub_tot, "->,>>>,>>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)


        if not long_digit:
            STR = to_string("", "x(77)") + to_string("Grand TOTAL ", "x(12)") + to_string("", "x(6)") + to_string(gqty, "->>>9") + to_string(tot, "->>,>>>,>>>,>>>,>>9.99")
        else:
            STR = to_string("", "x(77)") + to_string("Grand TOTAL ", "x(12)") + to_string("", "x(6)") + to_string(gqty, "->>>9") + to_string(tot, "->,>>>,>>>,>>>,>>>,>>9")
        gtot = tot


    journal_list()

    return generate_output()