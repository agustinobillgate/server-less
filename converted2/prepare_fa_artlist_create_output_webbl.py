#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

q1_list_data, Q1_list = create_model("Q1_list", {"name":string, "asset":string, "datum":date, "price":Decimal, "anzahl":int, "warenwert":Decimal, "depn_wert":Decimal, "book_wert":Decimal, "katnr":int, "bezeich":string, "location":string, "first_depn":date, "next_depn":date, "last_depn":date, "id":string, "created":date, "cid":string, "changed":date, "remark":string, "mathis_nr":int, "fname":string, "supplier":string, "posted":bool, "fibukonto":string, "faartikel_nr":int, "credit_fibu":string, "debit_fibu":string, "recid_fa_artikel":int, "recid_mathis":int, "avail_glacct1":bool, "avail_glacct2":bool, "avail_glacct3":bool, "subgroup":int, "model":string, "gnr":int, "flag":int, "grp_bez":string, "sgrp_bez":string, "rate":Decimal, "mark":string, "spec":string, "anz_depn":int, "category":int, "lager_nr":int})
fibu_list_data, Fibu_list = create_model("Fibu_list", {"flag":int, "fibukonto":string, "bezeich":string, "credit":Decimal, "debit":Decimal})

def prepare_fa_artlist_create_output_webbl(idflag:string, q1_list_data:[Q1_list], fibu_list_data:[Fibu_list]):
    doneflag = False
    counter:int = 0
    htl_no:string = ""
    temp_char:string = ""
    ankunft:string = ""
    bill_datum:string = ""
    depart:string = ""
    isposted:bool = False
    isavail_glacct1:bool = False
    isavail_glacct2:bool = False
    isavail_glacct3:bool = False
    queasy = None

    q1_list = fibu_list = bqueasy = pqueasy = tqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Pqueasy = create_buffer("Pqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal doneflag, counter, htl_no, temp_char, ankunft, bill_datum, depart, isposted, isavail_glacct1, isavail_glacct2, isavail_glacct3, queasy
        nonlocal idflag, q1_list_data
        nonlocal bqueasy, pqueasy, tqueasy


        nonlocal q1_list, fibu_list, bqueasy, pqueasy, tqueasy

        return {"doneflag": doneflag, "q1-list": q1_list_data, "fibu-list": fibu_list_data}


    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 280) & (Queasy.char1 == ("Fixed Asset List Report").lower()) & (Queasy.char3 == idflag)).order_by(Queasy.number1).all():
        counter = counter + 1

        if counter > 500:
            break

        if entry(0, queasy.char2, "|") == ("article").lower() :

            if entry(23, queasy.char2, "|") == ("YES").lower() :
                isposted = True

            elif entry(23, queasy.char2, "|") == ("NO").lower() :
                isposted = False

            if entry(30, queasy.char2, "|") == ("YES").lower() :
                isavail_glacct1 = True
            else:
                isavail_glacct1 = False

            if entry(31, queasy.char2, "|") == ("YES").lower() :
                isavail_glacct2 = True
            else:
                isavail_glacct2 = False

            if entry(32, queasy.char2, "|") == ("YES").lower() :
                isavail_glacct3 = True
            else:
                isavail_glacct3 = False
            q1_list = Q1_list()
            q1_list_data.append(q1_list)

            q1_list.name = entry(1, queasy.char2, "|")
            q1_list.asset = entry(2, queasy.char2, "|")
            q1_list.datum = date_mdy(entry(3, queasy.char2, "|"))
            q1_list.price =  to_decimal(to_decimal(entry(4 , queasy.char2 , "|")) )
            q1_list.anzahl = to_int(entry(5, queasy.char2, "|"))
            q1_list.warenwert =  to_decimal(to_decimal(entry(6 , queasy.char2 , "|")) )
            q1_list.depn_wert =  to_decimal(to_decimal(entry(7 , queasy.char2 , "|")) )
            q1_list.book_wert =  to_decimal(to_decimal(entry(8 , queasy.char2 , "|")) )
            q1_list.katnr = to_int(entry(9, queasy.char2, "|"))
            q1_list.bezeich = entry(10, queasy.char2, "|")
            q1_list.location = entry(11, queasy.char2, "|")
            q1_list.first_depn = date_mdy(entry(12, queasy.char2, "|"))
            q1_list.next_depn = date_mdy(entry(13, queasy.char2, "|"))
            q1_list.last_depn = date_mdy(entry(14, queasy.char2, "|"))
            q1_list.id = entry(15, queasy.char2, "|")
            q1_list.created = date_mdy(entry(16, queasy.char2, "|"))
            q1_list.cid = entry(17, queasy.char2, "|")
            q1_list.changed = date_mdy(entry(18, queasy.char2, "|"))
            q1_list.remark = entry(19, queasy.char2, "|")
            q1_list.mathis_nr = to_int(entry(20, queasy.char2, "|"))
            q1_list.fname = entry(21, queasy.char2, "|")
            q1_list.supplier = entry(22, queasy.char2, "|")
            q1_list.posted = isposted
            q1_list.fibukonto = entry(24, queasy.char2, "|")
            q1_list.faartikel_nr = to_int(entry(25, queasy.char2, "|"))
            q1_list.credit_fibu = entry(26, queasy.char2, "|")
            q1_list.debit_fibu = entry(27, queasy.char2, "|")
            q1_list.recid_fa_artikel = to_int(entry(28, queasy.char2, "|"))
            q1_list.recid_mathis = to_int(entry(29, queasy.char2, "|"))
            q1_list.avail_glacct1 = isavail_glacct1
            q1_list.avail_glacct2 = isavail_glacct2
            q1_list.avail_glacct3 = isavail_glacct3
            q1_list.subgroup = to_int(entry(33, queasy.char2, "|"))
            q1_list.model = entry(34, queasy.char2, "|")
            q1_list.gnr = to_int(entry(35, queasy.char2, "|"))
            q1_list.flag = to_int(entry(36, queasy.char2, "|"))
            q1_list.grp_bez = entry(37, queasy.char2, "|")
            q1_list.sgrp_bez = entry(38, queasy.char2, "|")
            q1_list.rate =  to_decimal(to_decimal(entry(39 , queasy.char2 , "|")) )
            q1_list.mark = entry(40, queasy.char2, "|")
            q1_list.spec = entry(41, queasy.char2, "|")
            q1_list.anz_depn = to_int(entry(42, queasy.char2, "|"))
            q1_list.category = to_int(entry(43, queasy.char2, "|"))
            q1_list.lager_nr = to_int(entry(44, queasy.char2, "|"))

        elif entry(0, queasy.char2, "|") == ("fibu").lower() :
            fibu_list = Fibu_list()
            fibu_list_data.append(fibu_list)

            fibu_list.flag = to_int(entry(1, queasy.char2, "|"))
            fibu_list.fibukonto = entry(2, queasy.char2, "|")
            fibu_list.bezeich = entry(3, queasy.char2, "|")
            fibu_list.credit =  to_decimal(to_decimal(entry(4 , queasy.char2 , "|")) )
            fibu_list.debit =  to_decimal(to_decimal(entry(5 , queasy.char2 , "|")) )

        bqueasy = db_session.query(Bqueasy).filter(
                 (Bqueasy._recid == queasy._recid)).first()
        db_session.delete(bqueasy)
        pass

    pqueasy = db_session.query(Pqueasy).filter(
             (Pqueasy.key == 280) & (Pqueasy.char1 == ("Fixed Asset List Report").lower()) & (Pqueasy.char3 == idflag)).first()

    if pqueasy:
        doneflag = False


    else:

        tqueasy = db_session.query(Tqueasy).filter(
                 (Tqueasy.key == 285) & (Tqueasy.char1 == ("Fixed Asset List Report").lower()) & (Tqueasy.number1 == 1) & (Tqueasy.char2 == idflag)).first()

        if tqueasy:
            doneflag = False


        else:
            doneflag = True

    tqueasy = db_session.query(Tqueasy).filter(
             (Tqueasy.key == 285) & (Tqueasy.char1 == ("Fixed Asset List Report").lower()) & (Tqueasy.number1 == 0) & (Tqueasy.char2 == idflag)).first()

    if tqueasy:
        pass
        db_session.delete(tqueasy)
        pass

    return generate_output()