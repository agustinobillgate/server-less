#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from sqlalchemy import extract, or_, cast, String
from sqlalchemy.sql.expression import collate
from models import Htparam, Artikel, Billjournal, Res_line, Reservation

def deposit_list2_webbl(fdate:date, sortype:int):

    prepare_cache ([Htparam, Artikel, Billjournal, Res_line, Reservation])

    depo_list_data = []
    total_saldo = to_decimal("0.0")
    depo_foreign:bool = False
    depo_curr:int = 0
    depo_artnr:int = 0
    str_resnr:string = ""
    resnr:int = 0
    bill_date:date = None
    exchg_rate:Decimal = to_decimal("0.0")
    found_it:bool = True
    resno:int = 0
    tot_depo1:Decimal = to_decimal("0.0")
    tot_depo2:Decimal = to_decimal("0.0")
    tot:Decimal = to_decimal("0.0")
    curr_name:string = ""
    curr_date:date = None
    subtotal:Decimal = to_decimal("0.0")
    str_resnr2:string = ""
    str_resnr3:string = ""
    grpstr:List[string] = [" ", "G"]
    htparam = artikel = billjournal = res_line = reservation = None

    depo_list = out_list = None

    depo_list_data, Depo_list = create_model("Depo_list", {"resnr":int, "reserve_name":string, "grpname":string, "guestname":string, "ankunft":date, "deposit_type":int, "depositgef":Decimal, "bal":Decimal, "depo1":Decimal, "datum1":date, "depo2":Decimal, "datum2":date, "deposit_type2":int, "deposit_paid":Decimal})
    out_list_data, Out_list = create_model("Out_list", {"deposit":Decimal, "deposit2":Decimal, "datum":date, "datum2":date, "resno":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal depo_list_data, total_saldo, depo_foreign, depo_curr, depo_artnr, str_resnr, resnr, bill_date, exchg_rate, found_it, resno, tot_depo1, tot_depo2, tot, curr_name, curr_date, subtotal, str_resnr2, str_resnr3, grpstr, htparam, artikel, billjournal, res_line, reservation
        nonlocal fdate, sortype


        nonlocal depo_list, out_list
        nonlocal depo_list_data, out_list_data

        return {"depo-list": depo_list_data, "total_saldo": total_saldo}

    def extractdigits(pcstring:string):

        nonlocal depo_list_data, total_saldo, depo_foreign, depo_curr, depo_artnr, str_resnr, resnr, bill_date, exchg_rate, found_it, resno, tot_depo1, tot_depo2, tot, curr_name, curr_date, subtotal, str_resnr2, str_resnr3, grpstr, htparam, artikel, billjournal, res_line, reservation
        nonlocal fdate, sortype


        nonlocal depo_list, out_list
        nonlocal depo_list_data, out_list_data

        ichar:int = 0
        iasc:int = 0
        ctemp:string = ""
        cchar:string = ""
        for ichar in range(1,length(pcstring)  + 1) :
            cchar = substring(pcstring, ichar - 1, 1)
            iasc = asc(cchar)

            if iasc > 47 and iasc < 58:
                ctemp = ctemp + cchar

        if (ctemp > "") :
            return ctemp
        else:
            return None


    def create_depo1():

        nonlocal depo_list_data, total_saldo, depo_foreign, depo_curr, depo_artnr, str_resnr, resnr, bill_date, exchg_rate, found_it, resno, tot_depo1, tot_depo2, tot, curr_name, curr_date, subtotal, str_resnr2, str_resnr3, grpstr, htparam, artikel, billjournal, res_line, reservation
        nonlocal fdate, sortype


        nonlocal depo_list, out_list
        nonlocal depo_list_data, out_list_data

        # for billjournal in db_session.query(Billjournal).filter(
        #          (Billjournal.artnr == depo_artnr) & (Billjournal.bill_datum <= fdate) & (get_year(Billjournal.bill_datum) == get_year(fdate)) & (matches((Billjournal.bezeich,"*Reservation*") | (Billjournal.bezeich)))).order_by(Billjournal.bill_datum).all():
        billjournals = db_session.query(Billjournal).filter(
            (Billjournal.artnr == depo_artnr) &
            (Billjournal.bill_datum <= fdate) &
            (extract('year', Billjournal.bill_datum) == fdate.year) &
            or_(
                cast(Billjournal.bezeich, String).collate('C').like('%Reservation%'),
                cast(Billjournal.bezeich, String).collate('C').like('%#%')
            )
        ).order_by(Billjournal.bill_datum).all()

        for billjournal in billjournals:
            # if matches(billjournal.bezeich,r"*Reservation*"):
            if billjournal.bezeich and re.search(r"Reservation", billjournal.bezeich):
                str_resnr = entry(0, billjournal.bezeich, "]")
                str_resnr2 = entry(0, str_resnr, "[")
                resno = to_int(extractdigits (str_resnr2))
            else:
                str_resnr = entry(0, billjournal.bezeich, "]")
                str_resnr2 = entry(1, str_resnr, "[")
                str_resnr3 = entry(0, str_resnr2, " ")
                resno = to_int(extractdigits (str_resnr3))

            out_list = query(out_list_data, filters=(lambda out_list: out_list.resno == resno), first=True)

            if not out_list:
                out_list = Out_list()
                out_list_data.append(out_list)

                out_list.resno = resno

            if out_list.deposit == 0:
                out_list.deposit =  to_decimal(billjournal.betrag)
                out_list.datum = billjournal.bill_datum


            else:
                out_list.deposit2 =  to_decimal(out_list.deposit2) + to_decimal(billjournal.betrag)
                out_list.datum2 = billjournal.bill_datum


        tot =  to_decimal("0")
        tot_depo2 =  to_decimal("0")
        tot_depo1 =  to_decimal("0")

        res_line_obj_list = {}
        # for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resnr == out_list.resno)).filter(
        #          ((Res_line.resnr.in_(list(set([out_list.resno for out_list in out_list_data])))))).order_by(Res_line._recid).all():
        resno_list = list({out_list.resno for out_list in out_list_data})
        results = (
            db_session.query(Res_line, Reservation)
            .join(Reservation, Reservation.resnr == Res_line.resnr)
            .filter(Res_line.resnr.in_(resno_list))
            .order_by(Res_line._recid)
            .all()
        )

        for res_line, reservation in results:
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            out_list = query(out_list_data, (lambda out_list: (res_line.resnr == out_list.resno)), first=True)

            if out_list.deposit2 >= 0:
                depo_list = Depo_list()
                depo_list_data.append(depo_list)

                depo_list.resnr = reservation.resnr 
                depo_list.reserve_name == reservation.name 
                depo_list.grpname == reservation.groupname 
                depo_list.guestname == res_line.name 
                depo_list.ankunft == res_line.ankunft 
                depo_list.deposit_type == reservation.deposit_type 
                depo_list.depositgef == reservation.depositgef 
                depo_list.depo1 == out_list.deposit 
                depo_list.datum1 == out_list.datum 
                depo_list.depo2 == out_list.deposit2 
                depo_list.datum2 == out_list.datum2 
                depo_list.deposit_type2 == reservation.deposit_type 
                depo_list.deposit_paid == out_list.deposit + out_list.deposit2


                tot_depo2 =  to_decimal(tot_depo2) + to_decimal(out_list.deposit2)
                tot_depo1 =  to_decimal(tot_depo1) + to_decimal(out_list.deposit)
        tot =  to_decimal(tot_depo2) + to_decimal(tot_depo1)
        total_saldo =  to_decimal(tot)


    def create_depo2():

        nonlocal depo_list_data, total_saldo, depo_foreign, depo_curr, depo_artnr, str_resnr, resnr, bill_date, exchg_rate, found_it, resno, tot_depo1, tot_depo2, tot, curr_name, curr_date, subtotal, str_resnr2, str_resnr3, grpstr, htparam, artikel, billjournal, res_line, reservation
        nonlocal fdate, sortype


        nonlocal depo_list, out_list
        nonlocal depo_list_data, out_list_data

        for billjournal in db_session.query(Billjournal).filter(
                 (Billjournal.artnr == depo_artnr) & (Billjournal.bill_datum <= fdate) & (get_year(Billjournal.bill_datum) == get_year(fdate)) & (matches((Billjournal.bezeich,"*Reservation*") | (Billjournal.bezeich)))).order_by(Billjournal.bill_datum).all():

            if matches(billjournal.bezeich,r"*Reservation*"):
                str_resnr = entry(0, billjournal.bezeich, "]")
                str_resnr2 = entry(0, str_resnr, "[")
                resno = to_int(extractdigits (str_resnr2))
            else:
                str_resnr = entry(0, billjournal.bezeich, "]")
                str_resnr2 = entry(1, str_resnr, "[")
                str_resnr3 = entry(0, str_resnr2, " ")
                resno = to_int(extractdigits (str_resnr3))

            out_list = query(out_list_data, filters=(lambda out_list: out_list.resno == resno), first=True)

            if not out_list:
                out_list = Out_list()
                out_list_data.append(out_list)

                out_list.resno = resno

            if out_list.deposit == 0:
                out_list.deposit =  to_decimal(billjournal.betrag)
                out_list.datum = billjournal.bill_datum


            else:
                out_list.deposit2 =  to_decimal(out_list.deposit2) + to_decimal(billjournal.betrag)
                out_list.datum2 = billjournal.bill_datum


        tot =  to_decimal("0")
        tot_depo2 =  to_decimal("0")
        tot_depo1 =  to_decimal("0")
        curr_name = ""

        res_line_obj_list = {}
        for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resnr == out_list.resno)).filter(
                 ((Res_line.resnr.in_(list(set([out_list.resno for out_list in out_list_data])))))).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            out_list = query(out_list_data, (lambda out_list: (res_line.resnr == out_list.resno)), first=True)

            if out_list.deposit2 >= 0:

                if curr_name != "" and curr_name != reservation.name:
                    depo_list = Depo_list()
                    depo_list_data.append(depo_list)

                    depo_list.resnr = None 
                    depo_list.reserve_name == "" 
                    depo_list.grpname == "TOTAL" 
                    depo_list.guestname == "" 
                    depo_list.ankunft == None 
                    depo_list.deposit_type == None 
                    depo_list.depositgef == subtotal 
                    depo_list.depo1 == None 
                    depo_list.datum1 == None 
                    depo_list.depo2 == None 
                    depo_list.datum2 == None 
                    depo_list.deposit_type2 == None 
                    depo_list.deposit_paid == None


                    subtotal =  to_decimal("0")
                depo_list = Depo_list()
                depo_list_data.append(depo_list)

                depo_list.resnr = reservation.resnr 
                depo_list.reserve_name == reservation.name 
                depo_list.grpname == reservation.groupname 
                depo_list.guestname == res_line.name 
                depo_list.ankunft == res_line.ankunft 
                depo_list.deposit_type == reservation.deposit_type 
                depo_list.depositgef == reservation.depositgef 
                depo_list.depo1 == out_list.deposit 
                depo_list.datum1 == out_list.datum 
                depo_list.depo2 == out_list.deposit2 
                depo_list.datum2 == out_list.datum2 
                depo_list.deposit_type2 == reservation.deposit_type 
                depo_list.deposit_paid == out_list.deposit + out_list.deposit2


                tot_depo2 =  to_decimal(tot_depo2) + to_decimal(out_list.deposit2)
                tot_depo1 =  to_decimal(tot_depo1) + to_decimal(out_list.deposit)
                curr_name = reservation.name
                subtotal =  to_decimal(subtotal) + to_decimal(depo_list.depositgef)
        tot =  to_decimal(tot_depo2) + to_decimal(tot_depo1)
        total_saldo =  to_decimal(tot)


    def create_depo3():

        nonlocal depo_list_data, total_saldo, depo_foreign, depo_curr, depo_artnr, str_resnr, resnr, bill_date, exchg_rate, found_it, resno, tot_depo1, tot_depo2, tot, curr_name, curr_date, subtotal, str_resnr2, str_resnr3, grpstr, htparam, artikel, billjournal, res_line, reservation
        nonlocal fdate, sortype


        nonlocal depo_list, out_list
        nonlocal depo_list_data, out_list_data

        for billjournal in db_session.query(Billjournal).filter(
                 (Billjournal.artnr == depo_artnr) & (Billjournal.bill_datum <= fdate) & (get_year(Billjournal.bill_datum) == get_year(fdate)) & (matches((Billjournal.bezeich,"*Reservation*") | (Billjournal.bezeich)))).order_by(Billjournal.bill_datum).all():

            if matches(billjournal.bezeich,r"*Reservation*"):
                str_resnr = entry(0, billjournal.bezeich, "]")
                str_resnr2 = entry(0, str_resnr, "[")
                resno = to_int(extractdigits (str_resnr2))
            else:
                str_resnr = entry(0, billjournal.bezeich, "]")
                str_resnr2 = entry(1, str_resnr, "[")
                str_resnr3 = entry(0, str_resnr2, " ")
                resno = to_int(extractdigits (str_resnr3))

            out_list = query(out_list_data, filters=(lambda out_list: out_list.resno == resno), first=True)

            if not out_list:
                out_list = Out_list()
                out_list_data.append(out_list)

                out_list.resno = resno

            if out_list.deposit == 0:
                out_list.deposit =  to_decimal(billjournal.betrag)
                out_list.datum = billjournal.bill_datum


            else:
                out_list.deposit2 =  to_decimal(out_list.deposit2) + to_decimal(billjournal.betrag)
                out_list.datum2 = billjournal.bill_datum


        tot =  to_decimal("0")
        tot_depo2 =  to_decimal("0")
        tot_depo1 =  to_decimal("0")

        res_line_obj_list = {}
        for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resnr == out_list.resno)).filter(
                 ((Res_line.resnr.in_(list(set([out_list.resno for out_list in out_list_data])))))).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            out_list = query(out_list_data, (lambda out_list: (res_line.resnr == out_list.resno)), first=True)

            if out_list.deposit2 >= 0:

                if curr_date != None and curr_date != res_line.ankunft:
                    depo_list = Depo_list()
                    depo_list_data.append(depo_list)

                    depo_list.resnr = None 
                    depo_list.reserve_name == "" 
                    depo_list.grpname == "TOTAL" 
                    depo_list.guestname == "" 
                    depo_list.ankunft == None 
                    depo_list.deposit_type == None 
                    depo_list.depositgef == subtotal 
                    depo_list.depo1 == None 
                    depo_list.datum1 == None 
                    depo_list.depo2 == None 
                    depo_list.datum2 == None 
                    depo_list.deposit_type2 == None 
                    depo_list.deposit_paid == None


                    subtotal =  to_decimal("0")
                depo_list = Depo_list()
                depo_list_data.append(depo_list)

                depo_list.resnr = reservation.resnr 
                depo_list.reserve_name == reservation.name 
                depo_list.grpname == reservation.groupname 
                depo_list.guestname == res_line.name 
                depo_list.ankunft == res_line.ankunft 
                depo_list.deposit_type == reservation.deposit_type 
                depo_list.depositgef == reservation.depositgef 
                depo_list.depo1 == out_list.deposit 
                depo_list.datum1 == out_list.datum 
                depo_list.depo2 == out_list.deposit2 
                depo_list.datum2 == out_list.datum2 
                depo_list.deposit_type2 == reservation.deposit_type 
                depo_list.deposit_paid == out_list.deposit + out_list.deposit2


                tot_depo2 =  to_decimal(tot_depo2) + to_decimal(out_list.deposit2)
                tot_depo1 =  to_decimal(tot_depo1) + to_decimal(out_list.deposit)
                curr_date = res_line.ankunft
                subtotal =  to_decimal(subtotal) + to_decimal(depo_list.depositgef)
        tot =  to_decimal(tot_depo2) + to_decimal(tot_depo1)
        total_saldo =  to_decimal(tot)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 120)]})

    artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})
    depo_artnr = htparam.finteger
    depo_foreign = artikel.pricetab
    depo_curr = artikel.betriebsnr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate
    depo_list_data.clear()

    if sortype == 1:
        create_depo1()

    if sortype == 2:
        create_depo2()

    if sortype == 3:
        create_depo3()

    return generate_output()