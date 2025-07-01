#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Bill, Reservation, Guest, Zimkateg, Bill_line, Artikel, Arrangement

def co_guest_1_webbl(case_type:int, pvilanguage:int, fr_date:date, to_date:date, price_decimal:int):

    prepare_cache ([Res_line, Bill, Reservation, Guest, Zimkateg, Bill_line, Artikel, Arrangement])

    cl_list_list = []
    tot_rm:int = 0
    tot_deposit:Decimal = to_decimal("0.0")
    tot_cash:Decimal = to_decimal("0.0")
    tot_cc:Decimal = to_decimal("0.0")
    tot_cl:Decimal = to_decimal("0.0")
    tot_amt:Decimal = to_decimal("0.0")
    tot_bb:Decimal = to_decimal("0.0")
    lvcarea:string = "co-guest"
    res_line = bill = reservation = guest = zimkateg = bill_line = artikel = arrangement = None

    cl_list = bresline = mbill = None

    cl_list_list, Cl_list = create_model("Cl_list", {"flag":int, "reihe":int, "zinr":string, "name":string, "zipreis":Decimal, "s_zipreis":string, "rechnr":int, "ankunft":date, "abreise":date, "cotime":string, "deposit":Decimal, "s_deposit":string, "cash":Decimal, "s_cash":string, "cc":Decimal, "s_cc":string, "cl":Decimal, "s_cl":string, "tot":Decimal, "s_tot":string, "resnr":int, "company":string, "bill_balance":Decimal, "reslin_no":int, "bill_flag":int, "bill_type":string, "guest_bl_recid":int, "master_bl_recid":int, "fg_col":bool, "guest_nr":int, "guest_typ":int, "gastnr":int, "rm_type":string}, {"ankunft": None, "abreise": None})

    Bresline = create_buffer("Bresline",Res_line)
    Mbill = create_buffer("Mbill",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cl_list_list, tot_rm, tot_deposit, tot_cash, tot_cc, tot_cl, tot_amt, tot_bb, lvcarea, res_line, bill, reservation, guest, zimkateg, bill_line, artikel, arrangement
        nonlocal case_type, pvilanguage, fr_date, to_date, price_decimal
        nonlocal bresline, mbill


        nonlocal cl_list, bresline, mbill
        nonlocal cl_list_list

        return {"cl-list": cl_list_list}

    def disp_billbalance():

        nonlocal cl_list_list, tot_rm, tot_deposit, tot_cash, tot_cc, tot_cl, tot_amt, tot_bb, lvcarea, res_line, bill, reservation, guest, zimkateg, bill_line, artikel, arrangement
        nonlocal case_type, pvilanguage, fr_date, to_date, price_decimal
        nonlocal bresline, mbill


        nonlocal cl_list, bresline, mbill
        nonlocal cl_list_list

        gname:string = ""
        curr_zinr:string = ""
        curr_resnr:int = 0
        billno:int = 0
        b_bal:int = 0
        do_it:bool = True
        guest_bl_recid:int = 0
        master_bl_recid:int = 0
        bill_flag:int = 0
        bill_type:string = ""
        fg_col:bool = False
        tot_rm = 0
        tot_deposit =  to_decimal("0")
        tot_cash =  to_decimal("0")
        tot_cc =  to_decimal("0")
        tot_cl =  to_decimal("0")
        tot_amt =  to_decimal("0")
        cl_list_list.clear()

        res_line_obj_list = {}
        res_line = Res_line()
        reservation = Reservation()
        for res_line.resnr, res_line.resstatus, res_line.reslinnr, res_line.zinr, res_line.zipreis, res_line.ankunft, res_line.abreise, res_line.abreisezeit, res_line.gastnrmember, res_line.gastnr, res_line.zikatnr, res_line.name, res_line.arrangement, res_line._recid, reservation.resnr, reservation.name, reservation._recid in db_session.query(Res_line.resnr, Res_line.resstatus, Res_line.reslinnr, Res_line.zinr, Res_line.zipreis, Res_line.ankunft, Res_line.abreise, Res_line.abreisezeit, Res_line.gastnrmember, Res_line.gastnr, Res_line.zikatnr, Res_line.name, Res_line.arrangement, Res_line._recid, Reservation.resnr, Reservation.name, Reservation._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                 (Res_line.active_flag == 2) & (Res_line.abreise >= fr_date) & (Res_line.abreise <= to_date) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Res_line.zinr, Res_line.resnr, Res_line.reslinnr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            do_it = True

            bresline = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(ne, res_line.resstatus)],"resstatus": [(ne, 12)]})

            if not bresline:
                do_it = False

            if do_it :
                billno = 0
                b_bal = 0
                guest_bl_recid = 0
                master_bl_recid = 0
                fg_col = False

                bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr),(ne, 0)]})

                if bill:
                    billno = bill.rechnr
                    b_bal = bill.saldo
                    guest_bl_recid = bill._recid
                    bill_flag = bill.flag
                    bill_type = "G"

                    mbill = get_cache (Bill, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, 0)]})

                    if mbill:
                        fg_col = True
                        master_bl_recid = mbill._recid

                if curr_zinr != res_line.zinr:
                    curr_zinr = res_line.zinr
                    curr_resnr = res_line.resnr
                    tot_rm = tot_rm + 1

                elif curr_resnr != res_line.resnr:
                    curr_resnr = res_line.resnr
                    tot_rm = tot_rm + 1
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.resnr = reservation.resnr
                cl_list.reslin_no = res_line.reslinnr
                cl_list.company = reservation.name
                cl_list.zinr = res_line.zinr
                cl_list.zipreis =  to_decimal(res_line.zipreis)
                cl_list.ankunft = res_line.ankunft
                cl_list.abreise = res_line.abreise
                cl_list.rechnr = billno
                cl_list.cotime = to_string(res_line.abreisezeit, "HH:MM")
                cl_list.bill_balance =  to_decimal(b_bal)
                cl_list.bill_flag = bill_flag
                cl_list.bill_type = bill_type
                cl_list.guest_bl_recid = guest_bl_recid
                cl_list.master_bl_recid = master_bl_recid
                cl_list.fg_col = fg_col
                cl_list.guest_nr = res_line.gastnrmember
                cl_list.gastnr = res_line.gastnr

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if guest:
                    cl_list.guest_typ = guest.karteityp

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                if zimkateg:
                    cl_list.rm_type = zimkateg.kurzbez

                if res_line.resstatus == 12:
                    cl_list.name = translateExtended ("** Extra Bill", lvcarea, "")
                else:
                    cl_list.name = res_line.name

                for bill_line in db_session.query(Bill_line).filter(
                         (Bill_line.rechnr == billno)).order_by(Bill_line._recid).all():

                    artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, bill_line.departement)]})

                    if artikel:

                        if artikel.artart == 2:
                            cl_list.cl =  to_decimal(cl_list.cl) - to_decimal(bill_line.betrag)
                            cl_list.tot =  to_decimal(cl_list.tot) - to_decimal(bill_line.betrag)
                            tot_cl =  to_decimal(tot_cl) - to_decimal(bill_line.betrag)
                            tot_amt =  to_decimal(tot_amt) - to_decimal(bill_line.betrag)

                        if artikel.artart == 5:
                            cl_list.deposit =  to_decimal(cl_list.deposit) - to_decimal(bill_line.betrag)
                            cl_list.tot =  to_decimal(cl_list.tot) - to_decimal(bill_line.betrag)
                            tot_deposit =  to_decimal(tot_deposit) - to_decimal(bill_line.betrag)
                            tot_amt =  to_decimal(tot_amt) - to_decimal(bill_line.betrag)

                        if artikel.artart == 6:
                            cl_list.cash =  to_decimal(cl_list.cash) - to_decimal(bill_line.betrag)
                            cl_list.tot =  to_decimal(cl_list.tot) - to_decimal(bill_line.betrag)
                            tot_cash =  to_decimal(tot_cash) - to_decimal(bill_line.betrag)
                            tot_amt =  to_decimal(tot_amt) - to_decimal(bill_line.betrag)

                        if artikel.artart == 7:
                            cl_list.cc =  to_decimal(cl_list.cc) - to_decimal(bill_line.betrag)
                            cl_list.tot =  to_decimal(cl_list.tot) - to_decimal(bill_line.betrag)
                            tot_cc =  to_decimal(tot_cc) - to_decimal(bill_line.betrag)
                            tot_amt =  to_decimal(tot_amt) - to_decimal(bill_line.betrag)

        for cl_list in query(cl_list_list, filters=(lambda cl_list: cl_list.flag == 0)):

            if price_decimal == 0:

                if cl_list.zipreis <= 9999999:
                    cl_list.s_zipreis = to_string(cl_list.zipreis, ">,>>>,>>9.99")
                else:
                    cl_list.s_zipreis = to_string(cl_list.zipreis, " >>>,>>>,>>9.99")
            else:

                if cl_list.zipreis <= 9999999:
                    cl_list.s_zipreis = to_string(cl_list.zipreis, ">,>>>,>>9.99")
                else:
                    cl_list.s_zipreis = to_string(cl_list.zipreis, " >>>,>>>,>>9.99")
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.reihe = 1
        cl_list.name = translateExtended ("Total C/O Room(s)", lvcarea, "")
        cl_list.s_zipreis = to_string(tot_rm, ">>>>>>>>>>>9")
        cl_list.deposit =  to_decimal(tot_deposit)
        cl_list.cash =  to_decimal(tot_cash)
        cl_list.cc =  to_decimal(tot_cc)
        cl_list.cl =  to_decimal(tot_cl)
        cl_list.tot =  to_decimal(tot_amt)


    def disp_dubalance():

        nonlocal cl_list_list, tot_rm, tot_deposit, tot_cash, tot_cc, tot_cl, tot_amt, tot_bb, lvcarea, res_line, bill, reservation, guest, zimkateg, bill_line, artikel, arrangement
        nonlocal case_type, pvilanguage, fr_date, to_date, price_decimal
        nonlocal bresline, mbill


        nonlocal cl_list, bresline, mbill
        nonlocal cl_list_list

        gname:string = ""
        curr_zinr:string = ""
        curr_resnr:int = 0
        billno:int = 0
        b_bal:int = 0
        do_it:bool = True
        guest_bl_recid:int = 0
        master_bl_recid:int = 0
        bill_flag:int = 0
        bill_type:string = ""
        fg_col:bool = False
        tot_rm = 0
        tot_deposit =  to_decimal("0")
        tot_cash =  to_decimal("0")
        tot_cc =  to_decimal("0")
        tot_cl =  to_decimal("0")
        tot_amt =  to_decimal("0")
        cl_list_list.clear()

        res_line_obj_list = {}
        res_line = Res_line()
        reservation = Reservation()
        for res_line.resnr, res_line.resstatus, res_line.reslinnr, res_line.zinr, res_line.zipreis, res_line.ankunft, res_line.abreise, res_line.abreisezeit, res_line.gastnrmember, res_line.gastnr, res_line.zikatnr, res_line.name, res_line.arrangement, res_line._recid, reservation.resnr, reservation.name, reservation._recid in db_session.query(Res_line.resnr, Res_line.resstatus, Res_line.reslinnr, Res_line.zinr, Res_line.zipreis, Res_line.ankunft, Res_line.abreise, Res_line.abreisezeit, Res_line.gastnrmember, Res_line.gastnr, Res_line.zikatnr, Res_line.name, Res_line.arrangement, Res_line._recid, Reservation.resnr, Reservation.name, Reservation._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                 (Res_line.active_flag == 2) & (Res_line.ankunft >= fr_date) & (Res_line.ankunft <= to_date) & (Res_line.abreise == Res_line.ankunft) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Res_line.zinr, Res_line.resnr, Res_line.reslinnr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            do_it = True

            bresline = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(ne, res_line.resstatus)],"resstatus": [(ne, 12)]})

            if not bresline:
                do_it = False

            if do_it :

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})
                billno = 0
                b_bal = 0
                guest_bl_recid = 0
                master_bl_recid = 0
                fg_col = False

                bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr),(ne, 0)]})

                if bill:
                    billno = bill.rechnr
                    b_bal = bill.saldo
                    guest_bl_recid = bill._recid
                    bill_flag = bill.flag
                    bill_type = "G"

                    mbill = get_cache (Bill, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, 0)]})

                    if mbill:
                        fg_col = True
                        master_bl_recid = mbill._recid

                if curr_zinr != res_line.zinr:
                    curr_zinr = res_line.zinr
                    curr_resnr = res_line.resnr
                    tot_rm = tot_rm + 1

                elif curr_resnr != res_line.resnr:
                    curr_resnr = res_line.resnr
                    tot_rm = tot_rm + 1
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.resnr = reservation.resnr
                cl_list.reslin_no = res_line.reslinnr
                cl_list.company = reservation.name
                cl_list.zinr = res_line.zinr
                cl_list.zipreis =  to_decimal(res_line.zipreis)
                cl_list.rechnr = billno
                cl_list.ankunft = res_line.ankunft
                cl_list.abreise = res_line.abreise
                cl_list.cotime = to_string(res_line.abreisezeit, "HH:MM")
                cl_list.bill_balance =  to_decimal(b_bal)
                cl_list.bill_flag = bill_flag
                cl_list.bill_type = bill_type
                cl_list.guest_bl_recid = guest_bl_recid
                cl_list.master_bl_recid = master_bl_recid
                cl_list.fg_col = fg_col
                cl_list.guest_nr = res_line.gastnrmember
                cl_list.gastnr = res_line.gastnr

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if guest:
                    cl_list.guest_typ = guest.karteityp

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                if zimkateg:
                    cl_list.rm_type = zimkateg.kurzbez

                bill_line = get_cache (Bill_line, {"departement": [(eq, 0)],"artnr": [(eq, arrangement.argt_artikelnr)],"bill_datum": [(eq, res_line.ankunft)],"massnr": [(eq, res_line.resnr)],"billin_nr": [(eq, res_line.reslinnr)]})

                if bill_line:
                    cl_list.flag = 1

                if res_line.resstatus == 12:
                    cl_list.name = translateExtended ("** Extra Bill", lvcarea, "")
                else:
                    cl_list.name = res_line.name

                for bill_line in db_session.query(Bill_line).filter(
                         (Bill_line.rechnr == billno)).order_by(Bill_line._recid).all():

                    artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, bill_line.departement)]})

                    if artikel:

                        if artikel.artart == 2:
                            cl_list.cl =  to_decimal(cl_list.cl) - to_decimal(bill_line.betrag)
                            cl_list.tot =  to_decimal(cl_list.tot) - to_decimal(bill_line.betrag)
                            tot_cl =  to_decimal(tot_cl) - to_decimal(bill_line.betrag)
                            tot_amt =  to_decimal(tot_amt) - to_decimal(bill_line.betrag)

                        if artikel.artart == 5:
                            cl_list.deposit =  to_decimal(cl_list.deposit) - to_decimal(bill_line.betrag)
                            cl_list.tot =  to_decimal(cl_list.tot) - to_decimal(bill_line.betrag)
                            tot_deposit =  to_decimal(tot_deposit) - to_decimal(bill_line.betrag)
                            tot_amt =  to_decimal(tot_amt) - to_decimal(bill_line.betrag)

                        if artikel.artart == 6:
                            cl_list.cash =  to_decimal(cl_list.cash) - to_decimal(bill_line.betrag)
                            cl_list.tot =  to_decimal(cl_list.tot) - to_decimal(bill_line.betrag)
                            tot_cash =  to_decimal(tot_cash) - to_decimal(bill_line.betrag)
                            tot_amt =  to_decimal(tot_amt) - to_decimal(bill_line.betrag)

                        if artikel.artart == 7:
                            cl_list.cc =  to_decimal(cl_list.cc) - to_decimal(bill_line.betrag)
                            cl_list.tot =  to_decimal(cl_list.tot) - to_decimal(bill_line.betrag)
                            tot_cc =  to_decimal(tot_cc) - to_decimal(bill_line.betrag)
                            tot_amt =  to_decimal(tot_amt) - to_decimal(bill_line.betrag)

        for cl_list in query(cl_list_list):

            if price_decimal == 0:

                if cl_list.zipreis <= 9999999:
                    cl_list.s_zipreis = to_string(cl_list.zipreis, ">,>>>,>>9.99")
                else:
                    cl_list.s_zipreis = to_string(cl_list.zipreis, " >>>,>>>,>>9.99")
            else:

                if cl_list.zipreis <= 9999999:
                    cl_list.s_zipreis = to_string(cl_list.zipreis, ">,>>>,>>9.99")
                else:
                    cl_list.s_zipreis = to_string(cl_list.zipreis, " >>>,>>>,>>9.99")
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 2
        cl_list.reihe = 1
        cl_list.name = translateExtended ("Total C/O Room(s)", lvcarea, "")
        cl_list.s_zipreis = to_string(tot_rm, ">>>>>>>>>>>9")
        cl_list.deposit =  to_decimal(tot_deposit)
        cl_list.cash =  to_decimal(tot_cash)
        cl_list.cc =  to_decimal(tot_cc)
        cl_list.cl =  to_decimal(tot_cl)
        cl_list.tot =  to_decimal(tot_amt)


    if case_type == 1:
        disp_billbalance()
    else:
        disp_dubalance()

    for cl_list in query(cl_list_list):
        cl_list.s_deposit = to_string(cl_list.deposit, "->,>>>,>>>,>>9.99")
        cl_list.s_cc = to_string(cl_list.cc, "->,>>>,>>>,>>9.99")
        cl_list.s_cl = to_string(cl_list.cl, "->,>>>,>>>,>>9.99")
        cl_list.s_cash = to_string(cl_list.cash, "->,>>>,>>>,>>9.99")
        cl_list.s_tot = to_string(cl_list.tot, "->,>>>,>>>,>>9.99")

    return generate_output()