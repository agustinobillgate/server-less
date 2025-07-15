from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Htparam, Waehrung, H_bill, H_bill_line, Artikel, H_journal, H_artikel, Kellner, Bill, Res_line

bline_list_list, Bline_list = create_model("Bline_list")
buf_art_list, Buf_art = create_model("Buf_art", {"artnr":int, "bezeich":str, "departement":int})

def rest_daysalesp2_btn_go_3_cldbl(bline_list_list:[Bline_list], buf_art_list:[Buf_art], disc_art1:int, disc_art2:int, disc_art3:int, curr_dept:int, all_user:bool, shift:int, from_date:date, to_date:date, art_str:str, voucher_art:int, zero_vat_compli:bool, show_fbodisc:bool, htl_dept_dptnr:int):
    t_betrag = to_decimal("0.0")
    t_foreign = to_decimal("0.0")
    exchg_rate = to_decimal("0.0")
    tot_serv = None
    tot_tax = None
    tot_debit = None
    tot_cash = None
    tot_cash1 = None
    tot_trans = None
    tot_ledger = None
    tot_cover = None
    nt_cover = None
    tot_other = to_decimal("0.0")
    nt_other = to_decimal("0.0")
    nt_serv = None
    nt_tax = None
    nt_debit = None
    nt_cash = None
    nt_cash1 = None
    nt_trans = None
    nt_ledger = None
    tot_vat = None
    nt_vat = None
    avail_outstand_list = False
    turnover_list = []
    t_tot_betrag_list = []
    t_nt_betrag_list = []
    outstand_list_list = []
    pay_list_list = []
    summ_list_list = []
    tot_betrag:List[decimal] = create_empty_list(20,to_decimal("0"))
    nt_betrag:List[decimal] = create_empty_list(20,to_decimal("0"))
    t_cash1:decimal = to_decimal("0.0")
    tt_other:decimal = to_decimal("0.0")
    anz_comp:int = 0
    val_comp:decimal = to_decimal("0.0")
    anz_coup:int = 0
    val_coup:decimal = to_decimal("0.0")
    total_fdisc:decimal = to_decimal("0.0")
    total_bdisc:decimal = to_decimal("0.0")
    total_odisc:decimal = to_decimal("0.0")
    t_serv:decimal = to_decimal("0.0")
    t_tax:decimal = to_decimal("0.0")
    t_debit:decimal = to_decimal("0.0")
    t_cash:decimal = to_decimal("0.0")
    t_trans:decimal = to_decimal("0.0")
    t_ledger:decimal = to_decimal("0.0")
    t_cover:int = 0
    fo_disc1:int = 0
    fo_disc2:int = 0
    fo_disc3:int = 0
    tt_betrag:List[decimal] = create_empty_list(20,to_decimal("0"))
    multi_vat:bool = False
    f_endkum:int = 0
    b_endkum:int = 0
    tot_deposit:decimal = to_decimal("0.0")
    t_deposit:decimal = to_decimal("0.0")
    nt_deposit:decimal = to_decimal("0.0")
    qty:int = 0
    counter:int = 0
    artnr_data:List[int] = create_empty_list(20,0)
    i:int = 0
    artnr_list:int = 0
    pax_cash:int = 0
    pax:int = 0
    pax2:int = 0
    htparam = waehrung = h_bill = h_bill_line = artikel = h_journal = h_artikel = kellner = bill = res_line = None

    other_art = temp = t_tot_betrag = t_nt_betrag = bline_list = outstand_list = pay_list = pay_listbuff = turnover = summ_list = buf_art = t_artnr = tlist = tlist = None

    other_art_list, Other_art = create_model("Other_art", {"artnr":int})
    temp_list, Temp = create_model("Temp", {"rechnr":int})
    t_tot_betrag_list, T_tot_betrag = create_model("T_tot_betrag", {"tot_betrag1":decimal, "tot_betrag2":decimal, "tot_betrag3":decimal, "tot_betrag4":decimal, "tot_betrag5":decimal, "tot_betrag6":decimal, "tot_betrag7":decimal, "tot_betrag8":decimal, "tot_betrag9":decimal, "tot_betrag10":decimal, "tot_betrag11":decimal, "tot_betrag12":decimal, "tot_betrag13":decimal, "tot_betrag14":decimal, "tot_betrag15":decimal, "tot_betrag16":decimal, "tot_betrag17":decimal, "tot_betrag18":decimal, "tot_betrag19":decimal, "tot_betrag20":decimal})
    t_nt_betrag_list, T_nt_betrag = create_model("T_nt_betrag", {"nt_betrag1":decimal, "nt_betrag2":decimal, "nt_betrag3":decimal, "nt_betrag4":decimal, "nt_betrag5":decimal, "nt_betrag6":decimal, "nt_betrag7":decimal, "nt_betrag8":decimal, "nt_betrag":decimal, "nt_betrag10":decimal, "nt_betrag11":decimal, "nt_betrag12":decimal, "nt_betrag13":decimal, "nt_betrag14":decimal, "nt_betrag15":decimal, "nt_betrag16":decimal, "nt_betrag17":decimal, "nt_betrag18":decimal, "nt_betrag19":decimal, "nt_betrag20":decimal})
    outstand_list_list, Outstand_list = create_model("Outstand_list")
    pay_list_list, Pay_list = create_model("Pay_list")
    turnover_list, Turnover = create_model("Turnover", {"betrag":[decimal,20], "other":decimal, "compli":bool, "flag":int, "gname":str, "int_rechnr":int, "st_comp":int, "p_curr":str, "t_vat":decimal, "qty_fpax":int, "qty_bpax":int, "qty_opax":int, "rest_deposit":decimal})
    summ_list_list, Summ_list = create_model("Summ_list", {"amount_food":decimal, "amount_bev":decimal, "amount_other":decimal, "disc_food":decimal, "disc_bev":decimal, "disc_other":decimal, "qty_disc_food":int, "qty_disc_bev":int, "qty_disc_other":int})
    t_artnr_list, T_artnr = create_model("T_artnr", {"nr":int, "artnr":int})

    Pay_listbuff = Pay_list
    pay_listbuff_list = pay_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_betrag, t_foreign, exchg_rate, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, nt_cover, tot_other, nt_other, nt_serv, nt_tax, nt_debit, nt_cash, nt_cash1, nt_trans, nt_ledger, tot_vat, nt_vat, avail_outstand_list, turnover_list, t_tot_betrag_list, t_nt_betrag_list, outstand_list_list, pay_list_list, summ_list_list, tot_betrag, nt_betrag, t_cash1, tt_other, anz_comp, val_comp, anz_coup, val_coup, total_fdisc, total_bdisc, total_odisc, t_serv, t_tax, t_debit, t_cash, t_trans, t_ledger, t_cover, fo_disc1, fo_disc2, fo_disc3, tt_betrag, multi_vat, f_endkum, b_endkum, tot_deposit, t_deposit, nt_deposit, qty, counter, artnr_data, i, artnr_list, pax_cash, pax, pax2, htparam, waehrung, h_bill, h_bill_line, artikel, h_journal, h_artikel, kellner, bill, res_line
        nonlocal disc_art1, disc_art2, disc_art3, curr_dept, all_user, shift, from_date, to_date, art_str, voucher_art, zero_vat_compli, show_fbodisc, htl_dept_dptnr
        nonlocal pay_listbuff


        nonlocal other_art, temp, t_tot_betrag, t_nt_betrag, bline_list, outstand_list, pay_list, pay_listbuff, turnover, summ_list, buf_art, t_artnr, tlist, tlist
        nonlocal other_art_list, temp_list, t_tot_betrag_list, t_nt_betrag_list, bline_list_list, outstand_list_list, pay_list_list, turnover_list, summ_list_list, buf_art_list, t_artnr_list
        return {"t_betrag": t_betrag, "t_foreign": t_foreign, "exchg_rate": exchg_rate, "tot_serv": tot_serv, "tot_tax": tot_tax, "tot_debit": tot_debit, "tot_cash": tot_cash, "tot_cash1": tot_cash1, "tot_trans": tot_trans, "tot_ledger": tot_ledger, "tot_cover": tot_cover, "nt_cover": nt_cover, "tot_other": tot_other, "nt_other": nt_other, "nt_serv": nt_serv, "nt_tax": nt_tax, "nt_debit": nt_debit, "nt_cash": nt_cash, "nt_cash1": nt_cash1, "nt_trans": nt_trans, "nt_ledger": nt_ledger, "tot_vat": tot_vat, "nt_vat": nt_vat, "avail_outstand_list": avail_outstand_list, "turnover": turnover_list, "t-tot-betrag": t_tot_betrag_list, "t-nt-betrag": t_nt_betrag_list, "outstand-list": outstand_list_list, "pay-list": pay_list_list, "summ-list": summ_list_list}

    def calculate_disc():

        nonlocal t_betrag, t_foreign, exchg_rate, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, nt_cover, tot_other, nt_other, nt_serv, nt_tax, nt_debit, nt_cash, nt_cash1, nt_trans, nt_ledger, tot_vat, nt_vat, avail_outstand_list, turnover_list, t_tot_betrag_list, t_nt_betrag_list, outstand_list_list, pay_list_list, summ_list_list, tot_betrag, nt_betrag, t_cash1, tt_other, anz_comp, val_comp, anz_coup, val_coup, total_fdisc, total_bdisc, total_odisc, t_serv, t_tax, t_debit, t_cash, t_trans, t_ledger, t_cover, fo_disc1, fo_disc2, fo_disc3, tt_betrag, multi_vat, f_endkum, b_endkum, tot_deposit, t_deposit, nt_deposit, qty, counter, artnr_data, artnr_list, pax_cash, pax, pax2, htparam, waehrung, h_bill, h_bill_line, artikel, h_journal, h_artikel, kellner, bill, res_line
        nonlocal disc_art1, disc_art2, disc_art3, curr_dept, all_user, shift, from_date, to_date, art_str, voucher_art, zero_vat_compli, show_fbodisc, htl_dept_dptnr
        nonlocal pay_listbuff


        nonlocal other_art, temp, t_tot_betrag, t_nt_betrag, bline_list, outstand_list, pay_list, pay_listbuff, turnover, summ_list, buf_art, t_artnr, tlist, tlist
        nonlocal other_art_list, temp_list, t_tot_betrag_list, t_nt_betrag_list, bline_list_list, outstand_list_list, pay_list_list, turnover_list, summ_list_list, buf_art_list, t_artnr_list

        amt_food:decimal = to_decimal("0.0")
        amt_bev:decimal = to_decimal("0.0")
        amt_other:decimal = to_decimal("0.0")
        amt_food_disc:decimal = to_decimal("0.0")
        amt_bev_disc:decimal = to_decimal("0.0")
        amt_other_disc:decimal = to_decimal("0.0")
        qty_food_disc:decimal = to_decimal("0.0")
        qty_bev_disc:decimal = to_decimal("0.0")
        qty_other_disc:decimal = to_decimal("0.0")
        vat:decimal = to_decimal("0.0")
        vat2:decimal = to_decimal("0.0")
        service:decimal = to_decimal("0.0")
        fact:decimal = to_decimal("0.0")
        netto:decimal = to_decimal("0.0")
        i:int = 0
        i_artnr:int = 0
        buf_hbline = None
        buf_artikel = None
        Buf_hbline =  create_buffer("Buf_hbline",H_bill_line)
        Buf_artikel =  create_buffer("Buf_artikel",Artikel)
        amt_food_disc =  to_decimal("0")
        amt_bev_disc =  to_decimal("0")
        amt_other_disc =  to_decimal("0")
        qty_food_disc =  to_decimal("0")
        qty_bev_disc =  to_decimal("0")
        qty_other_disc =  to_decimal("0")

        for turnover in query(turnover_list, filters=(lambda turnover: turnover.re.match(r".*G-TOTAL.*",not turnover.rechnr, re.IGNORECASE) and re.match(r".*R-TOTAL.*",not turnover.rechnr, re.IGNORECASE))):

            h_journal = db_session.query(H_journal).filter(
                     (H_journal.rechnr == to_int(turnover.rechnr)) & (H_journal.departement == curr_dept) & (H_journal.bill_datum >= from_date) & (H_journal.bill_datum <= to_date) & (H_journal.betrag != 0)).first()
            while None != h_journal:

                h_artikel = db_session.query(H_artikel).filter(
                         (H_artikel.artnr == h_journal.artnr) & (H_artikel.departement == curr_dept)).first()

                if h_artikel:

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == curr_dept)).first()

                    if artikel:
                        service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_journal.bill_datum))

                        if multi_vat == False:
                            vat =  to_decimal(vat) + to_decimal(vat2)


                        netto =  to_decimal(h_journal.betrag) / to_decimal((1) + to_decimal(vat) + to_decimal(vat2) + to_decimal(service))

                if h_journal.artnr == disc_art1:
                    amt_food_disc =  to_decimal(amt_food_disc) + to_decimal(netto)
                    qty_food_disc =  to_decimal(qty_food_disc) + to_decimal("1")

                elif h_journal.artnr == disc_art2:
                    amt_bev_disc =  to_decimal(amt_bev_disc) + to_decimal(netto)
                    qty_bev_disc =  to_decimal(qty_bev_disc) + to_decimal("1")

                elif h_journal.artnr == disc_art3:
                    amt_other_disc =  to_decimal(amt_other_disc) + to_decimal(netto)
                    qty_other_disc =  to_decimal(qty_other_disc) + to_decimal("1")

                curr_recid = h_journal._recid
                h_journal = db_session.query(H_journal).filter(
                         (H_journal.rechnr == to_int(turnover.rechnr)) & (H_journal.departement == curr_dept) & (H_journal.bill_datum >= from_date) & (H_journal.bill_datum <= to_date) & (H_journal.betrag != 0)).filter(H_journal._recid > curr_recid).first()
        summ_list = Summ_list()
        summ_list_list.append(summ_list)

        summ_list.disc_food =  to_decimal(amt_food_disc)
        summ_list.disc_bev =  to_decimal(amt_bev_disc)
        summ_list.disc_other =  to_decimal(amt_other_disc)
        summ_list.qty_disc_food = qty_food_disc
        summ_list.qty_disc_bev = qty_bev_disc
        summ_list.qty_disc_other = qty_other_disc


    def daysale_list1():

        nonlocal t_betrag, t_foreign, exchg_rate, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, nt_cover, tot_other, nt_other, nt_serv, nt_tax, nt_debit, nt_cash, nt_cash1, nt_trans, nt_ledger, tot_vat, nt_vat, avail_outstand_list, turnover_list, t_tot_betrag_list, t_nt_betrag_list, outstand_list_list, pay_list_list, summ_list_list, tot_betrag, nt_betrag, t_cash1, tt_other, anz_comp, val_comp, anz_coup, val_coup, total_fdisc, total_bdisc, total_odisc, t_serv, t_tax, t_debit, t_cash, t_trans, t_ledger, t_cover, fo_disc1, fo_disc2, fo_disc3, tt_betrag, multi_vat, f_endkum, b_endkum, tot_deposit, t_deposit, nt_deposit, qty, counter, artnr_data, artnr_list, pax_cash, pax, pax2, htparam, waehrung, h_bill, h_bill_line, artikel, h_journal, h_artikel, kellner, bill, res_line
        nonlocal disc_art1, disc_art2, disc_art3, curr_dept, all_user, shift, from_date, to_date, art_str, voucher_art, zero_vat_compli, show_fbodisc, htl_dept_dptnr
        nonlocal pay_listbuff


        nonlocal other_art, temp, t_tot_betrag, t_nt_betrag, bline_list, outstand_list, pay_list, pay_listbuff, turnover, summ_list, buf_art, t_artnr, tlist, tlist
        nonlocal other_art_list, temp_list, t_tot_betrag_list, t_nt_betrag_list, bline_list_list, outstand_list_list, pay_list_list, turnover_list, summ_list_list, buf_art_list, t_artnr_list

        curr_s:int = 0
        billnr:int = 0
        dept:int = 0
        d_name:str = ""
        usr_nr:int = 0
        d_found:bool = False
        c_found:bool = False
        vat:decimal = to_decimal("0.0")
        vat2:decimal = to_decimal("0.0")
        service:decimal = to_decimal("0.0")
        fact:decimal = to_decimal("0.0")
        netto:decimal = to_decimal("0.0")
        i:int = 0
        pos:int = 0
        bill_no:int = 0
        guestname:str = ""
        found:bool = False
        h_bline = None
        Tlist = Turnover
        tlist_list = turnover_list
        H_bline =  create_buffer("H_bline",H_bill_line)
        t_betrag =  to_decimal("0")
        t_foreign =  to_decimal("0")

        for turnover in query(turnover_list):
            turnover_list.remove(turnover)

        for pay_list in query(pay_list_list):
            pay_list_list.remove(pay_list)

        for outstand_list in query(outstand_list_list):
            outstand_list_list.remove(outstand_list)
        for i in range(1,20 + 1) :
            tot_betrag[i - 1] = 0
        tot_cover = 0
        tot_other =  to_decimal("0")
        tot_serv = 0
        tot_tax = 0
        tot_debit = 0
        tot_cash1 = 0
        tot_cash = 0
        tot_trans = 0
        tot_ledger = 0
        tot_vat = 0
        nt_cover = 0
        for i in range(1,20 + 1) :
            nt_betrag[i - 1] = 0
        nt_other =  to_decimal("0")
        nt_serv = 0
        nt_tax = 0
        nt_debit = 0
        nt_cash1 = 0
        nt_cash = 0
        nt_trans = 0
        nt_vat = 0

        for h_bill in db_session.query(H_bill).order_by(H_bill._recid).all():

            kellner = db_session.query(Kellner).filter(
                     (Kellner.kellner_nr == h_bill.kellner_nr)).first()
            outstand_list = Outstand_list()
            outstand_list_list.append(outstand_list)

            outstand_list.rechnr = h_bill.rechnr

            if kellner:
                outstand_list.name = kellner.kellnername

            for h_bill_line in db_session.query(H_bill_line).order_by(H_bill_line._recid).all():
                outstand_list.saldo = outstand_list.saldo + h_bill_line.betrag
                outstand_list.foreign = outstand_list.foreign + h_bill_line.fremdwbetrag

        for h_bill in db_session.query(H_bill).order_by(H_bill._recid).all():

            if shift == 0:

                h_bill_line = db_session.query(H_bill_line).filter(
                         (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum >= from_date) & (H_bill_line.bill_datum <= to_date) & (H_bill_line.departement == curr_dept)).first()
            else:

                h_bill_line = db_session.query(H_bill_line).filter(
                         (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum >= from_date) & (H_bill_line.bill_datum <= to_date) & (H_bill_line.departement == curr_dept) & (H_bill_line.betriebsnr == shift)).first()
            while available h_bill_line:

                turnover = query(turnover_list, filters=(lambda turnover: turnover.departement == curr_dept and turnover.rechnr == to_string(h_bill.rechnr)), first=True)

                if not turnover:
                    pos = 0
                    bill_no = 0
                    guestname = ""

                    if shift == 0:

                        h_bline = db_session.query(H_bline).filter(
                                 (H_bline.rechnr == h_bill.rechnr) & (H_bline.bill_datum >= from_date) & (H_bline.bill_datum <= to_date) & (H_bline.departement == curr_dept) & (H_bline.artnr == 0)).first()
                    else:

                        h_bline = db_session.query(H_bline).filter(
                                 (H_bline.rechnr == h_bill.rechnr) & (H_bline.bill_datum >= from_date) & (H_bline.bill_datum <= to_date) & (H_bline.departement == curr_dept) & (H_bline.betriebsnr == shift) & (H_bline.artnr == 0)).first()

                    if h_bline:
                        pos = 1 + get_index(h_bline.bezeich, "*")

                        if pos != 0:
                            bill_no = to_int(substring(h_bline.bezeich, pos - 1, (len(h_bline.bezeich) - pos + 1)))

                        if bill_no != 0:

                            bill = db_session.query(Bill).filter(
                                     (Bill.rechnr == bill_no)).first()

                            if bill:

                                res_line = db_session.query(Res_line).filter(
                                         (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.parent_nr)).first()

                                if res_line:
                                    guestname = res_line.name

                    if guestname == "":
                        guestname = h_bill.bilname
                    turnover = Turnover()
                    turnover_list.append(turnover)

                    turnover.departement = curr_dept
                    turnover.tischnr = h_bill.tischnr
                    turnover.belegung = h_bill.belegung
                    turnover.rechnr = to_string(h_bill.rechnr)
                    turnover.gname = guestname
                    tot_cover = tot_cover + h_bill.belegung

                if h_bill_line.artnr != 0:

                    h_artikel = db_session.query(H_artikel).filter(
                             (H_artikel.artnr == h_bill_line.artnr and H_artikel.departement == curr_dept)).first()

                if h_bill_line.artnr == 0:

                    pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 2), first=True)

                    if not pay_list:
                        pay_list = Pay_list()
                        pay_list_list.append(pay_list)

                        pay_list.flag = 2
                        pay_list.bezeich = "Room / Bill Transfer"
                    pay_list.saldo = pay_list.saldo - h_bill_line.betrag
                    t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)
                    turnover.r_transfer = turnover.r_transfer - h_bill_line.betrag
                    turnover.compli = False
                    i = 0
                    billnr = to_int(substring(h_bill_line.bezeich, i + 1 - 1, len(h_bill_line.bezeich) - i))

                    bill = db_session.query(Bill).filter(
                             (Bill.rechnr == billnr)).first()

                    if bill:
                        turnover.info = bill.zinr
                    turnover.t_credit = turnover.t_credit - h_bill_line.betrag
                    tot_trans = tot_trans - h_bill_line.betrag
                else:

                    if h_artikel.artart == 11 or h_artikel.artart == 12:

                        if h_artikel.artart == 11:

                            pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 6), first=True)

                            if not pay_list:
                                pay_list = Pay_list()
                                pay_list_list.append(pay_list)

                                pay_list.flag = 6
                                pay_list.compli = True
                                pay_list.bezeich = "Compliment"
                            pay_list.saldo = pay_list.saldo - h_bill_line.betrag - turnover.t_service - turnover.t_tax

                            if h_bill_line.betrag < 0:
                                pay_list.person = pay_list.person + h_bill.belegung
                            else:

                                if h_bill_line.betrag > 0:

                                    if h_bill.belegung > 0:
                                        pay_list.person = pay_list.person - h_bill.belegung
                                    else:
                                        pay_list.person = pay_list.person + h_bill.belegung
                            t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)
                            anz_comp = anz_comp + 1
                            val_comp =  to_decimal(val_comp) - to_decimal(h_bill_line.betrag)
                            turnover.st_comp = 1
                        else:

                            if h_artikel.artart == 12:

                                pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 7 and pay_list.bezeich == h_artikel.bezeich), first=True)

                                if not pay_list:
                                    pay_list = Pay_list()
                                    pay_list_list.append(pay_list)

                                    pay_list.compli = True
                                    pay_list.flag = 7
                                    pay_list.bezeich = h_artikel.bezeich
                                pay_list.saldo = pay_list.saldo - h_bill_line.betrag - turnover.t_service - turnover.t_tax

                                if h_bill_line.betrag < 0:
                                    pay_list.person = pay_list.person + h_bill.belegung
                                else:

                                    if h_bill_line.betrag > 0:

                                        if h_bill.belegung > 0:
                                            pay_list.person = pay_list.person - h_bill.belegung
                                        else:
                                            pay_list.person = pay_list.person + h_bill.belegung
                                t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)
                                anz_coup = anz_coup + 1
                                val_coup =  to_decimal(val_coup) - to_decimal(h_bill_line.betrag)
                                turnover.st_comp = 2
                        turnover.compli = not turnover.compli
                        turnover.r_transfer = turnover.r_transfer - h_bill_line.betrag

                        if h_artikel.artart == 11:
                            turnover.info = "Comp"
                        else:

                            if h_artikel.artart == 12:
                                turnover.info = substring(h_artikel.bezeich, 0, 4)
                        tot_trans = tot_trans - h_bill_line.betrag

                        if turnover.p_cash1 != 0:
                            turnover.p_cash1 = turnover.p_cash1 - turnover.t_service - turnover.t_tax

                        if turnover.p_cash != 0:
                            turnover.p_cash = turnover.p_cash - turnover.t_service - turnover.t_tax

                        if turnover.r_transfer != 0:
                            turnover.r_transfer = turnover.r_transfer - turnover.t_service - turnover.t_tax

                        if turnover.c_ledger != 0:
                            turnover.c_ledger = turnover.c_ledger - turnover.t_service - turnover.t_tax
                        turnover.t_debit = turnover.t_debit - turnover.t_service - turnover.t_tax
                        turnover.t_service = 0
                        turnover.t_tax = 0


                else:

                    h_artikel = db_session.query(H_artikel).filter(
                             (H_artikel.artnr == h_bill_line.artnr and H_artikel.departement == curr_dept)).first()

                    if h_artikel.artart == 0:

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.departement == curr_dept and Artikel.artnr == h_artikel.artnrfront)).first()
                    else:

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.departement == 0 and Artikel.artnr == h_artikel.artnrfront)).first()

                    if h_artikel.artart == 0:
                        service =  to_decimal("0")
                        vat =  to_decimal("0")
                        vat2 =  to_decimal("0")

                        if (artikel.umsatzart == 3 or artikel.umsatzart == 5):
                            turnover.qty_fpax = turnover.qty_fpax + h_bill_line.anzahl

                        elif artikel.umsatzart == 6:
                            turnover.qty_bpax = turnover.qty_bpax + h_bill_line.anzahl
                        else:
                            turnover.qty_opax = turnover.qty_opax + h_bill_line.anzahl
                        service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_bill_line.bill_datum))

                        if multi_vat == False:
                            vat =  to_decimal(vat) + to_decimal(vat2)


                        netto =  to_decimal(h_bill_line.betrag) / to_decimal((1) + to_decimal(vat) + to_decimal(vat2) + to_decimal(service))
                        turnover.t_service = turnover.t_service + netto * service
                        turnover.t_tax = turnover.t_tax + netto * vat
                        turnover.t_vat =  to_decimal(turnover.t_vat) + to_decimal(netto) * to_decimal(vat2)
                        turnover.t_debit = turnover.t_debit + h_bill_line.betrag
                        tot_serv = tot_serv + netto * service
                        tot_tax = tot_tax + netto * vat
                        tot_debit = tot_debit + h_bill_line.betrag
                        tot_vat = tot_vat + netto * vat2

                        if artikel.artnr == artnr_list[0]:
                            turnover.betrag[0] = turnover.betrag[0] + netto
                            tot_betrag[0] = tot_betrag[0] + netto
                        else:

                            if artikel.artnr == artnr_list[1]:
                                turnover.betrag[1] = turnover.betrag[1] + netto
                                tot_betrag[1] = tot_betrag[1] + netto
                        else:

                            if artikel.artnr == artnr_list[2]:
                                turnover.betrag[2] = turnover.betrag[2] + netto
                                tot_betrag[2] = tot_betrag[2] + netto
                        else:

                            if artikel.artnr == artnr_list[3]:
                                turnover.betrag[3] = turnover.betrag[3] + netto
                                tot_betrag[3] = tot_betrag[3] + netto
                        else:

                            if artikel.artnr == artnr_list[4]:
                                turnover.betrag[4] = turnover.betrag[4] + netto
                                tot_betrag[4] = tot_betrag[4] + netto
                        else:

                            if artikel.artnr == artnr_list[5]:
                                turnover.betrag[5] = turnover.betrag[5] + netto
                                tot_betrag[5] = tot_betrag[5] + netto
                        else:

                            if artikel.artnr == artnr_list[6]:
                                turnover.betrag[6] = turnover.betrag[6] + netto
                                tot_betrag[6] = tot_betrag[6] + netto
                        else:

                            if artikel.artnr == artnr_list[7]:
                                turnover.betrag[7] = turnover.betrag[7] + netto
                                tot_betrag[7] = tot_betrag[7] + netto
                        else:

                            if artikel.artnr == artnr_list[8]:
                                turnover.betrag[8] = turnover.betrag[8] + netto
                                tot_betrag[8] = tot_betrag[8] + netto
                        else:

                            if artikel.artnr == artnr_list[9]:
                                turnover.betrag[9] = turnover.betrag[9] + netto
                                tot_betrag[9] = tot_betrag[9] + netto
                        else:

                            if artikel.artnr == artnr_list[10]:
                                turnover.betrag[10] = turnover.betrag[10] + netto
                                tot_betrag[10] = tot_betrag[10] + netto
                        else:

                            if artikel.artnr == artnr_list[11]:
                                turnover.betrag[11] = turnover.betrag[11] + netto
                                tot_betrag[11] = tot_betrag[11] + netto
                        else:

                            if artikel.artnr == artnr_list[12]:
                                turnover.betrag[12] = turnover.betrag[12] + netto
                                tot_betrag[12] = tot_betrag[12] + netto
                        else:

                            if artikel.artnr == artnr_list[13]:
                                turnover.betrag[13] = turnover.betrag[13] + netto
                                tot_betrag[13] = tot_betrag[13] + netto
                        else:

                            if artikel.artnr == artnr_list[14]:
                                turnover.betrag[4] = turnover.betrag[14] + netto
                                tot_betrag[14] = tot_betrag[14] + netto
                        else:

                            if artikel.artnr == artnr_list[15]:
                                turnover.betrag[15] = turnover.betrag[15] + netto
                                tot_betrag[15] = tot_betrag[15] + netto
                        else:

                            if artikel.artnr == artnr_list[16]:
                                turnover.betrag[16] = turnover.betrag[16] + netto
                                tot_betrag[16] = tot_betrag[16] + netto
                        else:

                            if artikel.artnr == artnr_list[17]:
                                turnover.betrag[17] = turnover.betrag[17] + netto
                                tot_betrag[17] = tot_betrag[17] + netto
                        else:

                            if artikel.artnr == artnr_list[18]:
                                turnover.betrag[18] = turnover.betrag[18] + netto
                                tot_betrag[18] = tot_betrag[18] + netto
                        else:

                            if artikel.artnr == artnr_list[19]:
                                turnover.betrag[19] = turnover.betrag[19] + netto
                                tot_betrag[19] = tot_betrag[19] + netto
                        else:

                            for other_art in query(other_art_list):

                                if artikel.artnr == other_art.artnr:
                                    turnover.other =  to_decimal(turnover.other) + to_decimal(netto)
                                    tot_other =  to_decimal(tot_other) + to_decimal(netto)

                    elif h_artikel.artart == 5:

                        pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 8), first=True)

                        if not pay_list:
                            pay_list = Pay_list()
                            pay_list_list.append(pay_list)

                            pay_list.flag = 8
                            pay_list.bezeich = "Restaurant Deposit"
                        pay_list.saldo = pay_list.saldo - h_bill_line.betrag
                        pay_list.person = pay_list.person + h_bill.belegung
                        turnover.rest_deposit =  to_decimal(turnover.rest_deposit) - to_decimal(h_bill_line.betrag)
                        t_deposit =  to_decimal(t_deposit) - to_decimal(h_bill_line.betrag)
                        tot_deposit =  to_decimal(tot_deposit) - to_decimal(h_bill_line.betrag)
                    else:

                        if h_artikel.artart == 6:

                            artikel = db_session.query(Artikel).filter(
                                     (Artikel.artnr == h_artikel.artnrfront and Artikel.departement == 0)).first()

                            pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 1 and pay_list.bezeich == artikel.bezeich), first=True)

                            if not pay_list:
                                pay_list = Pay_list()
                                pay_list_list.append(pay_list)

                                pay_list.flag = 1
                                pay_list.bezeich = artikel.bezeich

                            if artikel.pricetab:
                                pay_list.foreign = pay_list.foreign - h_bill_line.fremdwbetrag
                                t_foreign =  to_decimal(t_foreign) - to_decimal(h_bill_line.fremdwbetrag)
                            else:
                                pay_list.saldo = pay_list.saldo - h_bill_line.betrag
                                t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)

                            waehrung = db_session.query(Waehrung).filter(
                                     (Waehrung.waehrungsnr == artikel.betriebsnr)).first()

                            if waehrung:
                                turnover.p_curr = waehrung.wabkurz

                            if artikel.pricetab:
                                turnover.p_cash1 = turnover.p_cash1 - h_bill_line.fremdwbetrag
                                tot_cash1 = tot_cash1 - h_bill_line.fremdwbetrag

                            elif h_artikel.artnr == voucher_art:
                                turnover.p_cash1 = turnover.p_cash1 - h_bill_line.betrag
                                t_cash1 =  to_decimal(t_cash1) - to_decimal(h_bill_line.betrag)
                                tot_cash1 = tot_cash1 - h_bill_line.betrag
                            else:
                                turnover.p_cash = turnover.p_cash - h_bill_line.betrag
                                tot_cash = tot_cash - h_bill_line.betrag
                            turnover.t_credit = turnover.t_credit - h_bill_line.betrag
                    else:

                        if h_artikel.artart == 7 or h_artikel.artart == 2:

                            if h_artikel.artart == 7:

                                pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 3), first=True)

                                if not pay_list:
                                    pay_list = Pay_list()
                                    pay_list_list.append(pay_list)

                                    pay_list.flag = 3
                                    pay_list.bezeich = "Credit Card"
                            else:

                                if h_artikel.artart == 2:

                                    pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 5), first=True)

                                    if not pay_list:
                                        pay_list = Pay_list()
                                        pay_list_list.append(pay_list)

                                        pay_list.flag = 5
                                        pay_list.bezeich = "City- & Employee Ledger"
                            pay_list.saldo = pay_list.saldo - h_bill_line.betrag
                            pay_list.person = pay_list.person + h_bill.belegung
                            t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)
                            turnover.info = to_string(h_artikel.artnr, ">>>9")
                            turnover.artnr = artikel.artnr
                            turnover.c_ledger = turnover.c_ledger - h_bill_line.betrag
                            turnover.t_credit = turnover.t_credit - h_bill_line.betrag
                            tot_ledger = tot_ledger - h_bill_line.betrag

                if shift == 0:

                    curr_recid = h_bill_line._recid
                    h_bill_line = db_session.query(H_bill_line).filter(
                             (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum >= from_date) & (H_bill_line.bill_datum <= to_date) & (H_bill_line.departement == curr_dept)).filter(H_bill_line._recid > curr_recid).first()
                else:

                    curr_recid = h_bill_line._recid
                    h_bill_line = db_session.query(H_bill_line).filter(
                             (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum >= from_date) & (H_bill_line.bill_datum <= to_date) & (H_bill_line.departement == curr_dept) & (H_bill_line.betriebsnr == shift)).filter(H_bill_line._recid > curr_recid).first()

        if zero_vat_compli:

            for tlist in query(tlist_list, filters=(lambda tlist: tlist.comp)):

                pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 6), first=True)

                if pay_list and tlist.st_comp == 1:
                    pay_list.saldo = pay_list.saldo - tlist.t_service - tlist.t_tax
                    t_betrag =  to_decimal(t_betrag) - to_decimal(tlist.t_service) - to_decimal(tlist.t_tax)

                if tlist.r_transfer != 0 and tlist.t_debit != 0:
                    tlist.r_transfer = tlist.r_transfer - tlist.t_service - tlist.t_tax
                    tlist.t_debit = tlist.t_debit - tlist.t_service - tlist.t_tax
                    tot_trans = tot_trans - tlist.t_service - tlist.t_tax
                    tot_debit = tot_debit - tlist.t_service - tlist.t_tax


                tot_serv = tot_serv - tlist.t_service
                tot_tax = tot_tax - tlist.t_tax
                tot_vat = tot_vat - tlist.t_vat
                tlist.t_service = 0
                tlist.t_tax = 0


        if show_fbodisc:
            fo_discarticle()

            for tlist in query(tlist_list):
                cal_fbodisc(tlist.rechnr)

                if total_fdisc != 0 or total_bdisc != 0 or total_odisc != 0:
                    for i in range(1,20 + 1) :

                        if artnr_list[i - 1] != 0:

                            if artnr_list[i - 1] == fo_disc1:
                                tlist.betrag[i - 1] = total_fdisc

                            elif artnr_list[i - 1] == fo_disc2:
                                tlist.betrag[i - 1] = total_bdisc

                            elif artnr_list[i - 1] == fo_disc3:
                                tlist.betrag[i - 1] = total_odisc
        turnover = Turnover()
        turnover_list.append(turnover)

        turnover.rechnr = "G-TOTAL"
        turnover.flag = 2

        for tlist in query(tlist_list, filters=(lambda tlist: tlist.flag == 0)):
            turnover.belegung = turnover.belegung + tlist.belegung
            turnover.qty_fpax = turnover.qty_fpax + tlist.qty_fpax
            turnover.qty_bpax = turnover.qty_bpax + tlist.qty_bpax
            turnover.qty_opax = turnover.qty_opax + tlist.qty_opax
            for i in range(1,20 + 1) :
                turnover.betrag[i - 1] = turnover.betrag[i - 1] + tlist.betrag[i - 1]


            turnover.other =  to_decimal(turnover.other) + to_decimal(tlist.other)
            turnover.t_service = turnover.t_service + tlist.t_service
            turnover.t_tax = turnover.t_tax + tlist.t_tax
            turnover.t_debit = turnover.t_debit + tlist.t_debit
            turnover.p_cash = turnover.p_cash + tlist.p_cash
            turnover.p_cash1 = turnover.p_cash1 + tlist.p_cash1
            turnover.r_transfer = turnover.r_transfer + tlist.r_transfer
            turnover.c_ledger = turnover.c_ledger + tlist.c_ledger
            turnover.t_vat =  to_decimal(turnover.t_vat) + to_decimal(tlist.t_vat)
            turnover.rest_deposit =  to_decimal(turnover.rest_deposit) + to_decimal(tlist.rest_deposit)
        turnover = Turnover()
        turnover_list.append(turnover)

        turnover.rechnr = "R-TOTAL"
        turnover.flag = 3

        for tlist in query(tlist_list, filters=(lambda tlist: tlist.flag == 0 and not tlist.compli)):
            turnover.belegung = turnover.belegung + tlist.belegung
            turnover.qty_fpax = turnover.qty_fpax + tlist.qty_fpax
            turnover.qty_bpax = turnover.qty_bpax + tlist.qty_bpax
            turnover.qty_opax = turnover.qty_opax + tlist.qty_opax
            turnover.betrag[0] = turnover.betrag[0] + tlist.betrag[0]
            turnover.betrag[1] = turnover.betrag[1] + tlist.betrag[1]
            turnover.betrag[2] = turnover.betrag[2] + tlist.betrag[2]
            turnover.betrag[3] = turnover.betrag[3] + tlist.betrag[3]
            turnover.betrag[4] = turnover.betrag[4] + tlist.betrag[4]
            turnover.betrag[5] = turnover.betrag[5] + tlist.betrag[5]
            turnover.betrag[6] = turnover.betrag[6] + tlist.betrag[6]
            turnover.betrag[7] = turnover.betrag[7] + tlist.betrag[7]
            turnover.betrag[8] = turnover.betrag[8] + tlist.betrag[8]
            turnover.betrag[9] = turnover.betrag[9] + tlist.betrag[9]
            turnover.betrag[10] = turnover.betrag[10] + tlist.betrag[10]
            turnover.betrag[11] = turnover.betrag[11] + tlist.betrag[11]
            turnover.betrag[12] = turnover.betrag[12] + tlist.betrag[12]
            turnover.betrag[13] = turnover.betrag[13] + tlist.betrag[13]
            turnover.betrag[14] = turnover.betrag[14] + tlist.betrag[14]
            turnover.betrag[15] = turnover.betrag[15] + tlist.betrag[15]
            turnover.betrag[16] = turnover.betrag[16] + tlist.betrag[16]
            turnover.betrag[17] = turnover.betrag[17] + tlist.betrag[17]
            turnover.betrag[18] = turnover.betrag[18] + tlist.betrag[18]
            turnover.betrag[19] = turnover.betrag[19] + tlist.betrag[19]
            turnover.other =  to_decimal(turnover.other) + to_decimal(tlist.other)
            turnover.t_service = turnover.t_service + tlist.t_service
            turnover.t_tax = turnover.t_tax + tlist.t_tax
            turnover.t_debit = turnover.t_debit + tlist.t_debit
            turnover.p_cash = turnover.p_cash + tlist.p_cash
            turnover.p_cash1 = turnover.p_cash1 + tlist.p_cash1
            turnover.r_transfer = turnover.r_transfer + tlist.r_transfer
            turnover.c_ledger = turnover.c_ledger + tlist.c_ledger
            turnover.t_vat =  to_decimal(turnover.t_vat) + to_decimal(tlist.t_vat)
            turnover.rest_deposit =  to_decimal(turnover.rest_deposit) + to_decimal(tlist.rest_deposit)
        nt_cover = turnover.belegung
        nt_betrag[0] = turnover.betrag[0]
        nt_betrag[1] = turnover.betrag[1]
        nt_betrag[2] = turnover.betrag[2]
        nt_betrag[3] = turnover.betrag[3]
        nt_betrag[4] = turnover.betrag[4]
        nt_betrag[5] = turnover.betrag[5]
        nt_betrag[6] = turnover.betrag[6]
        nt_betrag[7] = turnover.betrag[7]
        nt_betrag[8] = turnover.betrag[8]
        nt_betrag[9] = turnover.betrag[9]
        nt_betrag[10] = turnover.betrag[10]
        nt_betrag[11] = turnover.betrag[11]
        nt_betrag[12] = turnover.betrag[12]
        nt_betrag[13] = turnover.betrag[13]
        nt_betrag[14] = turnover.betrag[14]
        nt_betrag[15] = turnover.betrag[15]
        nt_betrag[16] = turnover.betrag[16]
        nt_betrag[17] = turnover.betrag[17]
        nt_betrag[18] = turnover.betrag[18]
        nt_betrag[19] = turnover.betrag[19]
        nt_serv = turnover.t_service
        nt_tax = turnover.t_tax
        nt_debit = turnover.t_debit
        nt_cash = turnover.p_cash
        nt_cash1 = turnover.p_cash1
        nt_trans = turnover.r_transfer
        nt_ledger = turnover.c_ledger
        nt_vat = turnover.t_vat


    def daysale_list():

        nonlocal t_betrag, t_foreign, exchg_rate, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, nt_cover, tot_other, nt_other, nt_serv, nt_tax, nt_debit, nt_cash, nt_cash1, nt_trans, nt_ledger, tot_vat, nt_vat, avail_outstand_list, turnover_list, t_tot_betrag_list, t_nt_betrag_list, outstand_list_list, pay_list_list, summ_list_list, tot_betrag, nt_betrag, t_cash1, tt_other, anz_comp, val_comp, anz_coup, val_coup, total_fdisc, total_bdisc, total_odisc, t_serv, t_tax, t_debit, t_cash, t_trans, t_ledger, t_cover, fo_disc1, fo_disc2, fo_disc3, tt_betrag, multi_vat, f_endkum, b_endkum, tot_deposit, t_deposit, nt_deposit, qty, counter, artnr_data, artnr_list, pax_cash, pax, pax2, htparam, waehrung, h_bill, h_bill_line, artikel, h_journal, h_artikel, kellner, bill, res_line
        nonlocal disc_art1, disc_art2, disc_art3, curr_dept, all_user, shift, from_date, to_date, art_str, voucher_art, zero_vat_compli, show_fbodisc, htl_dept_dptnr
        nonlocal pay_listbuff


        nonlocal other_art, temp, t_tot_betrag, t_nt_betrag, bline_list, outstand_list, pay_list, pay_listbuff, turnover, summ_list, buf_art, t_artnr, tlist, tlist
        nonlocal other_art_list, temp_list, t_tot_betrag_list, t_nt_betrag_list, bline_list_list, outstand_list_list, pay_list_list, turnover_list, summ_list_list, buf_art_list, t_artnr_list

        curr_s:int = 0
        billnr:int = 0
        dept:int = 0
        d_name:str = ""
        usr_nr:int = 0
        d_found:bool = False
        c_found:bool = False
        vat:decimal = to_decimal("0.0")
        vat2:decimal = to_decimal("0.0")
        service:decimal = to_decimal("0.0")
        fact:decimal = to_decimal("0.0")
        netto:decimal = to_decimal("0.0")
        i:int = 0
        found:bool = False
        compli:bool = False
        guestname:str = ""
        bill_no:int = 0
        pos:int = 0
        kellner1 = None
        h_bline = None
        Kellner1 =  create_buffer("Kellner1",Kellner)
        Tlist = Turnover
        tlist_list = turnover_list
        H_bline =  create_buffer("H_bline",H_bill_line)

        for turnover in query(turnover_list):
            turnover_list.remove(turnover)

        for pay_list in query(pay_list_list):
            pay_list_list.remove(pay_list)

        for outstand_list in query(outstand_list_list):
            outstand_list_list.remove(outstand_list)
        t_betrag =  to_decimal("0")
        t_foreign =  to_decimal("0")
        for i in range(1,20 + 1) :
            tot_betrag[i - 1] = 0
        tot_cover = 0
        tot_serv = 0
        tot_tax = 0
        tot_debit = 0
        tot_cash1 = 0
        tot_cash = 0
        tot_trans = 0
        tot_ledger = 0
        tot_vat = 0
        for i in range(1,20 + 1) :
            nt_betrag[i - 1] = 0
        nt_cover = 0
        nt_serv = 0
        nt_tax = 0
        nt_debit = 0
        nt_cash1 = 0
        nt_cash = 0
        nt_trans = 0
        nt_ledger = 0
        nt_vat = 0

        for bline_list in query(bline_list_list):

            for h_bill in db_session.query(H_bill).order_by(H_bill._recid).all():
                outstand_list = Outstand_list()
                outstand_list_list.append(outstand_list)


                kellner1 = db_session.query(Kellner1).filter(
                         (Kellner1.kellner_nr == h_bill.kellner_nr and Kellner1.departement == h_bill.departement)).first()
                outstand_list.rechnr = h_bill.rechnr

                if kellner1:
                    outstand_list.name = kellner1.kellnername
                else:
                    outstand_list.name = to_string(h_bill.kellner_nr)

                for h_bill_line in db_session.query(H_bill_line).order_by(H_bill_line._recid).all():
                    outstand_list.saldo = outstand_list.saldo + h_bill_line.betrag
                    outstand_list.foreign = outstand_list.foreign + h_bill_line.fremdwbetrag

            for h_bill in db_session.query(H_bill).order_by(H_bill._recid).all():

                if shift == 0:

                    h_bill_line = db_session.query(H_bill_line).filter(
                             (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum >= from_date) & (H_bill_line.bill_datum <= to_date) & (H_bill_line.departement == curr_dept)).first()
                else:

                    h_bill_line = db_session.query(H_bill_line).filter(
                             (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum >= from_date) & (H_bill_line.bill_datum <= to_date) & (H_bill_line.departement == curr_dept) & (H_bill_line.betriebsnr == shift)).first()
                while None != h_bill_line:

                    turnover = query(turnover_list, filters=(lambda turnover: turnover.departement == curr_dept and turnover.kellner_nr == kellner.kellner_nr and turnover.rechnr == to_string(h_bill.rechnr)), first=True)

                    if not turnover:
                        pos = 0
                        bill_no = 0
                        guestname = ""

                        if shift == 0:

                            h_bline = db_session.query(H_bline).filter(
                                     (H_bline.rechnr == h_bill.rechnr) & (H_bline.bill_datum >= from_date) & (H_bline.bill_datum <= to_date) & (H_bline.departement == curr_dept) & (H_bline.artnr == 0)).first()
                        else:

                            h_bline = db_session.query(H_bline).filter(
                                     (H_bline.rechnr == h_bill.rechnr) & (H_bline.bill_datum >= from_date) & (H_bline.bill_datum <= to_date) & (H_bline.departement == curr_dept) & (H_bline.betriebsnr == shift) & (H_bline.artnr == 0)).first()

                        if h_bline:
                            pos = 1 + get_index(h_bline.bezeich, "*")

                            if pos != 0:
                                bill_no = to_int(substring(h_bline.bezeich, pos - 1, (len(h_bline.bezeich) - pos + 1)))

                            if bill_no != 0:

                                bill = db_session.query(Bill).filter(
                                         (Bill.rechnr == bill_no)).first()

                                if bill:

                                    res_line = db_session.query(Res_line).filter(
                                             (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.parent_nr)).first()

                                    if res_line:
                                        guestname = res_line.name

                        if guestname == "":
                            guestname = h_bill.bilname
                        turnover = Turnover()
                        turnover_list.append(turnover)

                        turnover.departement = kellner.departement
                        turnover.kellner_nr = kellner.kellner_nr
                        turnover.name = kellner.kellnername
                        turnover.tischnr = h_bill.tischnr
                        turnover.belegung = h_bill.belegung
                        turnover.rechnr = to_string(h_bill.rechnr)
                        turnover.gname = guestname
                        tot_cover = tot_cover + h_bill.belegung
                        t_cover = t_cover + h_bill.belegung

                    if h_bill_line.artnr == 0:
                        turnover.r_transfer = turnover.r_transfer - h_bill_line.betrag
                        turnover.compli = False

                        pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 2), first=True)

                        if not pay_list:
                            pay_list = Pay_list()
                            pay_list_list.append(pay_list)

                            pay_list.flag = 2
                            pay_list.bezeich = "Room / Bill Transfer"
                        pay_list.saldo = pay_list.saldo - h_bill_line.betrag
                        t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)
                        i = 0
                        billnr = to_int(substring(h_bill_line.bezeich, i + 1 - 1, len(h_bill_line.bezeich) - i))

                        bill = db_session.query(Bill).filter(
                                 (Bill.rechnr == billnr)).first()

                        if bill:
                            turnover.info = bill.zinr
                        turnover.t_credit = turnover.t_credit - h_bill_line.betrag
                        t_trans =  to_decimal(t_trans) - to_decimal(h_bill_line.betrag)
                        tot_trans = tot_trans - h_bill_line.betrag
                    else:

                        h_artikel = db_session.query(H_artikel).filter(
                                 (H_artikel.artnr == h_bill_line.artnr and H_artikel.departement == curr_dept)).first()

                        if h_artikel.artart == 11 or h_artikel.artart == 12:

                            if h_artikel.artart == 11:

                                pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 6), first=True)

                                if not pay_list:
                                    pay_list = Pay_list()
                                    pay_list_list.append(pay_list)

                                    pay_list.flag = 6
                                    pay_list.compli = True
                                    pay_list.bezeich = "Compliment"
                                pay_list.saldo = pay_list.saldo - h_bill_line.betrag - turnover.t_service - turnover.t_tax

                                if h_bill_line.betrag < 0:
                                    pay_list.person = pay_list.person + h_bill.belegung
                                else:

                                    if h_bill_line.betrag > 0:

                                        if h_bill.belegung > 0:
                                            pay_list.person = pay_list.person - h_bill.belegung
                                        else:
                                            pay_list.person = pay_list.person + h_bill.belegung
                                t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)
                                anz_comp = anz_comp + 1
                                val_comp =  to_decimal(val_comp) - to_decimal(h_bill_line.betrag)
                                turnover.st_comp = 1
                            else:

                                if h_artikel.artart == 12:

                                    pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 7 and pay_list.bezeich == h_artikel.bezeich), first=True)

                                    if not pay_list:
                                        pay_list = Pay_list()
                                        pay_list_list.append(pay_list)

                                        pay_list.flag = 7
                                        pay_list.compli = True
                                        pay_list.bezeich = h_artikel.bezeich
                                    pay_list.saldo = pay_list.saldo - h_bill_line.betrag - turnover.t_service - turnover.t_tax

                                    if h_bill_line.betrag < 0:
                                        pay_list.person = pay_list.person + h_bill.belegung
                                    else:

                                        if h_bill_line.betrag > 0:

                                            if h_bill.belegung > 0:
                                                pay_list.person = pay_list.person - h_bill.belegung
                                            else:
                                                pay_list.person = pay_list.person + h_bill.belegung
                                    t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)
                                    anz_coup = anz_coup + 1
                                    val_coup =  to_decimal(val_coup) - to_decimal(h_bill_line.betrag)
                                    turnover.st_comp = 2
                            turnover.compli = not turnover.compli
                            turnover.r_transfer = turnover.r_transfer - h_bill_line.betrag

                            if h_artikel.artart == 11:
                                turnover.info = "Comp"
                            else:

                                if h_artikel.artart == 12:
                                    turnover.info = substring(h_artikel.bezeich, 0, 4)
                            tot_trans = tot_trans - h_bill_line.betrag

                            if turnover.p_cash1 != 0:
                                turnover.p_cash1 = turnover.p_cash1 - turnover.t_service - turnover.t_tax

                            if turnover.p_cash != 0:
                                turnover.p_cash = turnover.p_cash - turnover.t_service - turnover.t_tax

                            if turnover.r_transfer != 0:
                                turnover.r_transfer = turnover.r_transfer - turnover.t_service - turnover.t_tax

                            if turnover.c_ledger != 0:
                                turnover.c_ledger = turnover.c_ledger - turnover.t_service - turnover.t_tax
                            turnover.t_debit = turnover.t_debit - turnover.t_service - turnover.t_tax
                            turnover.t_service = 0
                            turnover.t_tax = 0


                        else:

                            if h_artikel.artart == 0:

                                artikel = db_session.query(Artikel).filter(
                                         (Artikel.departement == curr_dept and Artikel.artnr == h_artikel.artnrfront)).first()

                                if artikel:
                                    service =  to_decimal("0")
                                vat =  to_decimal("0")
                                vat2 =  to_decimal("0")

                                if (artikel.umsatzart == 3 or artikel.umsatzart == 5):
                                    turnover.qty_fpax = turnover.qty_fpax + h_bill_line.anzahl

                                elif artikel.umsatzart == 6:
                                    turnover.qty_bpax = turnover.qty_bpax + h_bill_line.anzahl
                                else:
                                    turnover.qty_opax = turnover.qty_opax + h_bill_line.anzahl
                                service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_bill_line.bill_datum))

                                if multi_vat == False:
                                    vat =  to_decimal(vat) + to_decimal(vat2)


                                netto =  to_decimal(h_bill_line.betrag) / to_decimal((1) + to_decimal(vat) + to_decimal(vat2) + to_decimal(service))
                                turnover.t_service = turnover.t_service + netto * service
                                turnover.t_tax = turnover.t_tax + netto * vat
                                turnover.t_vat =  to_decimal(turnover.t_vat) + to_decimal(netto) * to_decimal(vat2)
                                turnover.t_debit = turnover.t_debit + h_bill_line.betrag
                                tot_serv = tot_serv + netto * service
                                tot_tax = tot_tax + netto * vat
                                tot_vat = tot_vat + netto * vat2
                                tot_debit = tot_debit + h_bill_line.betrag

                                if artikel.artnr == artnr_list[0]:
                                    turnover.betrag[0] = turnover.betrag[0] + netto
                                    tt_betrag[0] = tt_betrag[0] + netto
                                    tot_betrag[0] = tot_betrag[0] + netto
                                else:

                                    if artikel.artnr == artnr_list[1]:
                                        turnover.betrag[1] = turnover.betrag[1] + netto
                                        tt_betrag[1] = tt_betrag[1] + netto
                                        tot_betrag[1] = tot_betrag[1] + netto
                                else:

                                    if artikel.artnr == artnr_list[2]:
                                        turnover.betrag[2] = turnover.betrag[2] + netto
                                        tt_betrag[2] = tt_betrag[2] + netto
                                        tot_betrag[2] = tot_betrag[2] + netto
                                else:

                                    if artikel.artnr == artnr_list[3]:
                                        turnover.betrag[3] = turnover.betrag[3] + netto
                                        tt_betrag[3] = tt_betrag[3] + netto
                                        tot_betrag[3] = tot_betrag[3] + netto
                                else:

                                    if artikel.artnr == artnr_list[4]:
                                        turnover.betrag[4] = turnover.betrag[4] + netto
                                        tt_betrag[4] = tt_betrag[4] + netto
                                        tot_betrag[4] = tot_betrag[4] + netto
                                else:

                                    if artikel.artnr == artnr_list[5]:
                                        turnover.betrag[5] = turnover.betrag[5] + netto
                                        tt_betrag[5] = tt_betrag[5] + netto
                                        tot_betrag[5] = tot_betrag[5] + netto
                                else:

                                    if artikel.artnr == artnr_list[6]:
                                        turnover.betrag[6] = turnover.betrag[6] + netto
                                        tt_betrag[6] = tt_betrag[6] + netto
                                        tot_betrag[6] = tot_betrag[6] + netto
                                else:

                                    if artikel.artnr == artnr_list[7]:
                                        turnover.betrag[7] = turnover.betrag[7] + netto
                                        tt_betrag[7] = tt_betrag[7] + netto
                                        tot_betrag[7] = tot_betrag[7] + netto
                                else:

                                    if artikel.artnr == artnr_list[8]:
                                        turnover.betrag[8] = turnover.betrag[8] + netto
                                        tt_betrag[8] = tt_betrag[8] + netto
                                        tot_betrag[8] = tot_betrag[8] + netto
                                else:

                                    if artikel.artnr == artnr_list[9]:
                                        turnover.betrag[9] = turnover.betrag[9] + netto
                                        tt_betrag[9] = tt_betrag[9] + netto
                                        tot_betrag[9] = tot_betrag[9] + netto
                                else:

                                    if artikel.artnr == artnr_list[10]:
                                        turnover.betrag[10] = turnover.betrag[10] + netto
                                        tt_betrag[10] = tt_betrag[10] + netto
                                        tot_betrag[10] = tot_betrag[10] + netto
                                else:

                                    if artikel.artnr == artnr_list[11]:
                                        turnover.betrag[11] = turnover.betrag[11] + netto
                                        tt_betrag[11] = tt_betrag[11] + netto
                                        tot_betrag[11] = tot_betrag[11] + netto
                                else:

                                    if artikel.artnr == artnr_list[12]:
                                        turnover.betrag[12] = turnover.betrag[12] + netto
                                        tt_betrag[12] = tt_betrag[12] + netto
                                        tot_betrag[12] = tot_betrag[12] + netto
                                else:

                                    if artikel.artnr == artnr_list[13]:
                                        turnover.betrag[13] = turnover.betrag[13] + netto
                                        tt_betrag[13] = tt_betrag[13] + netto
                                        tot_betrag[13] = tot_betrag[13] + netto
                                else:

                                    if artikel.artnr == artnr_list[14]:
                                        turnover.betrag[14] = turnover.betrag[14] + netto
                                        tt_betrag[14] = tt_betrag[14] + netto
                                        tot_betrag[14] = tot_betrag[14] + netto
                                else:

                                    if artikel.artnr == artnr_list[15]:
                                        turnover.betrag[15] = turnover.betrag[15] + netto
                                        tt_betrag[15] = tt_betrag[15] + netto
                                        tot_betrag[15] = tot_betrag[15] + netto
                                else:

                                    if artikel.artnr == artnr_list[16]:
                                        turnover.betrag[16] = turnover.betrag[16] + netto
                                        tt_betrag[16] = tt_betrag[16] + netto
                                        tot_betrag[16] = tot_betrag[16] + netto
                                else:

                                    if artikel.artnr == artnr_list[17]:
                                        turnover.betrag[17] = turnover.betrag[17] + netto
                                        tt_betrag[17] = tt_betrag[17] + netto
                                        tot_betrag[17] = tot_betrag[17] + netto
                                else:

                                    if artikel.artnr == artnr_list[18]:
                                        turnover.betrag[18] = turnover.betrag[18] + netto
                                        tt_betrag[18] = tt_betrag[18] + netto
                                        tot_betrag[18] = tot_betrag[18] + netto
                                else:

                                    if artikel.artnr == artnr_list[19]:
                                        turnover.betrag[19] = turnover.betrag[19] + netto
                                        tt_betrag[19] = tt_betrag[19] + netto
                                        tot_betrag[19] = tot_betrag[19] + netto
                                else:

                                    for other_art in query(other_art_list):

                                        if artikel.artnr == other_art.artnr:
                                            turnover.other =  to_decimal(turnover.other) + to_decimal(netto)
                                            tt_other =  to_decimal(tt_other) + to_decimal(netto)


                                        tot_other =  to_decimal(tot_other) + to_decimal(netto)
                        else:

                            artikel = db_session.query(Artikel).filter(
                                     (Artikel.departement == 0 and Artikel.artnr == h_artikel.artnrfront)).first()

                        if h_artikel.artart == 6:

                            artikel = db_session.query(Artikel).filter(
                                     (Artikel.artnr == h_artikel.artnrfront and Artikel.departement == 0)).first()

                            pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 1 and pay_list.bezeich == artikel.bezeich), first=True)

                            if not pay_list:
                                pay_list = Pay_list()
                                pay_list_list.append(pay_list)

                                pay_list.flag = 1
                                pay_list.bezeich = artikel.bezeich

                            if artikel.pricetab:
                                pay_list.foreign = pay_list.foreign - h_bill_line.fremdwbetrag
                                t_foreign =  to_decimal(t_foreign) - to_decimal(h_bill_line.fremdwbetrag)
                            else:
                                pay_list.saldo = pay_list.saldo - h_bill_line.betrag
                                t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)

                            waehrung = db_session.query(Waehrung).filter(
                                     (Waehrung.waehrungsnr == artikel.betriebsnr)).first()

                            if waehrung:
                                turnover.p_curr = waehrung.wabkurz

                            if artikel.pricetab:
                                turnover.p_cash1 = turnover.p_cash1 - h_bill_line.fremdwbetrag
                                t_cash1 =  to_decimal(t_cash1) - to_decimal(h_bill_line.fremdwbetrag)

                            elif h_artikel.artnr == voucher_art:
                                turnover.p_cash1 = turnover.p_cash1 - h_bill_line.betrag
                                t_cash1 =  to_decimal(t_cash1) - to_decimal(h_bill_line.betrag)
                                tot_cash1 = tot_cash1 - h_bill_line.betrag
                            else:
                                turnover.p_cash = turnover.p_cash - h_bill_line.betrag
                                t_cash =  to_decimal(t_cash) - to_decimal(h_bill_line.betrag)
                            turnover.t_credit = turnover.t_credit - h_bill_line.betrag
                            turnover.info = " "

                        elif h_artikel.artart == 5:

                            pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 8), first=True)

                            if not pay_list:
                                pay_list = Pay_list()
                                pay_list_list.append(pay_list)

                                pay_list.flag = 8
                                pay_list.bezeich = "Restaurant Deposit"
                            pay_list.saldo = pay_list.saldo - h_bill_line.betrag
                            pay_list.person = pay_list.person + h_bill.belegung
                            turnover.rest_deposit =  to_decimal(turnover.rest_deposit) - to_decimal(h_bill_line.betrag)
                            t_deposit =  to_decimal(t_deposit) - to_decimal(h_bill_line.betrag)
                            tot_deposit =  to_decimal(tot_deposit) - to_decimal(h_bill_line.betrag)
                        else:

                            if h_artikel.artart == 7 or h_artikel.artart == 2:

                                if h_artikel.artart == 7:

                                    pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 3), first=True)

                                    if not pay_list:
                                        pay_list = Pay_list()
                                        pay_list_list.append(pay_list)

                                        pay_list.flag = 3
                                        pay_list.bezeich = "Credit Card"
                                else:

                                    if h_artikel.artart == 2:

                                        pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 5), first=True)

                                        if not pay_list:
                                            pay_list = Pay_list()
                                            pay_list_list.append(pay_list)

                                            pay_list.flag = 5
                                            pay_list.bezeich = "City- & Employee Ledger"
                                pay_list.saldo = pay_list.saldo - h_bill_line.betrag
                                pay_list.person = pay_list.person + h_bill.belegung
                                t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)
                                turnover.info = to_string(h_artikel.artnr, ">>>9")
                                turnover.artnr = artikel.artnr
                                turnover.c_ledger = turnover.c_ledger - h_bill_line.betrag
                                turnover.t_credit = turnover.t_credit - h_bill_line.betrag
                                t_ledger =  to_decimal(t_ledger) - to_decimal(h_bill_line.betrag)
                                tot_ledger = tot_ledger - h_bill_line.betrag

                    if shift == 0:

                        curr_recid = h_bill_line._recid
                        h_bill_line = db_session.query(H_bill_line).filter(
                                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum >= from_date) & (H_bill_line.bill_datum <= to_date) & (H_bill_line.departement == curr_dept)).filter(H_bill_line._recid > curr_recid).first()
                    else:

                        curr_recid = h_bill_line._recid
                        h_bill_line = db_session.query(H_bill_line).filter(
                                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum >= from_date) & (H_bill_line.bill_datum <= to_date) & (H_bill_line.departement == curr_dept) & (H_bill_line.betriebsnr == shift)).filter(H_bill_line._recid > curr_recid).first()

            if zero_vat_compli:

                for tlist in query(tlist_list, filters=(lambda tlist: tlist.comp)):

                    pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 6), first=True)

                    if pay_list:
                        pay_list.saldo = pay_list.saldo - tlist.t_service - tlist.t_tax
                        t_betrag =  to_decimal(t_betrag) - to_decimal(tlist.t_service) - to_decimal(tlist.t_tax)

                    if tlist.r_transfer != 0 and tlist.t_debit != 0:
                        tlist.r_transfer = tlist.r_transfer - tlist.t_service - tlist.t_tax
                        tlist.t_debit = tlist.t_debit - tlist.t_service - tlist.t_tax
                        tot_trans = tot_trans - tlist.t_service - tlist.t_tax
                        tot_debit = tot_debit - tlist.t_service - tlist.t_tax


                    tot_serv = tot_serv - tlist.t_service
                    tot_tax = tot_tax - tlist.t_tax
                    tot_vat = tot_vat - tlist.t_vat
                    tlist.t_service = 0
                    tlist.t_tax = 0
                    tlist.t_vat =  to_decimal("0")


            if show_fbodisc:
                fo_discarticle()

                for tlist in query(tlist_list):
                    cal_fbodisc(tlist.rechnr)

                    if total_fdisc != 0 or total_bdisc != 0 or total_odisc != 0:
                        for i in range(1,20 + 1) :

                            if artnr_list[i - 1] != 0:

                                if artnr_list[i - 1] == fo_disc1:
                                    tlist.betrag[i - 1] = total_fdisc

                                elif artnr_list[i - 1] == fo_disc2:
                                    tlist.betrag[i - 1] = total_bdisc

                                elif artnr_list[i - 1] == fo_disc3:
                                    tlist.betrag[i - 1] = total_odisc
        for i in range(1,20 + 1) :
            tot_betrag[i - 1] = 0


        turnover = Turnover()
        turnover_list.append(turnover)

        turnover.rechnr = "G-TOTAL"
        turnover.flag = 2

        for tlist in query(tlist_list, filters=(lambda tlist: tlist.flag == 0)):
            turnover.belegung = turnover.belegung + tlist.belegung
            turnover.qty_fpax = turnover.qty_fpax + tlist.qty_fpax
            turnover.qty_bpax = turnover.qty_bpax + tlist.qty_bpax
            turnover.qty_opax = turnover.qty_opax + tlist.qty_opax
            for i in range(1,20 + 1) :
                turnover.betrag[i - 1] = turnover.betrag[i - 1] + tlist.betrag[i - 1]
                tot_betrag[i - 1] = tot_betrag[i - 1] + tlist.betrag[i - 1]


            turnover.other =  to_decimal(turnover.other) + to_decimal(tlist.other)
            turnover.t_service = turnover.t_service + tlist.t_service
            turnover.t_tax = turnover.t_tax + tlist.t_tax
            turnover.t_debit = turnover.t_debit + tlist.t_debit
            turnover.p_cash = turnover.p_cash + tlist.p_cash
            turnover.p_cash1 = turnover.p_cash1 + tlist.p_cash1
            turnover.r_transfer = turnover.r_transfer + tlist.r_transfer
            turnover.c_ledger = turnover.c_ledger + tlist.c_ledger
            turnover.t_vat =  to_decimal(turnover.t_vat) + to_decimal(tlist.t_vat)
            turnover.rest_deposit =  to_decimal(turnover.rest_deposit) + to_decimal(tlist.rest_deposit)
        turnover = Turnover()
        turnover_list.append(turnover)

        turnover.rechnr = "R-TOTAL"
        turnover.flag = 3

        for tlist in query(tlist_list, filters=(lambda tlist: tlist.flag == 0 and not tlist.compli)):
            turnover.belegung = turnover.belegung + tlist.belegung
            turnover.qty_fpax = turnover.qty_fpax + tlist.qty_fpax
            turnover.qty_bpax = turnover.qty_bpax + tlist.qty_bpax
            turnover.qty_opax = turnover.qty_opax + tlist.qty_opax
            turnover.betrag[0] = turnover.betrag[0] + tlist.betrag[0]
            turnover.betrag[1] = turnover.betrag[1] + tlist.betrag[1]
            turnover.betrag[2] = turnover.betrag[2] + tlist.betrag[2]
            turnover.betrag[3] = turnover.betrag[3] + tlist.betrag[3]
            turnover.betrag[4] = turnover.betrag[4] + tlist.betrag[4]
            turnover.betrag[5] = turnover.betrag[5] + tlist.betrag[5]
            turnover.betrag[6] = turnover.betrag[6] + tlist.betrag[6]
            turnover.betrag[7] = turnover.betrag[7] + tlist.betrag[7]
            turnover.betrag[8] = turnover.betrag[8] + tlist.betrag[8]
            turnover.betrag[9] = turnover.betrag[9] + tlist.betrag[9]
            turnover.betrag[10] = turnover.betrag[10] + tlist.betrag[10]
            turnover.betrag[11] = turnover.betrag[11] + tlist.betrag[11]
            turnover.betrag[12] = turnover.betrag[12] + tlist.betrag[12]
            turnover.betrag[13] = turnover.betrag[13] + tlist.betrag[13]
            turnover.betrag[14] = turnover.betrag[14] + tlist.betrag[14]
            turnover.betrag[15] = turnover.betrag[15] + tlist.betrag[15]
            turnover.betrag[16] = turnover.betrag[16] + tlist.betrag[16]
            turnover.betrag[17] = turnover.betrag[17] + tlist.betrag[17]
            turnover.betrag[18] = turnover.betrag[18] + tlist.betrag[18]
            turnover.betrag[19] = turnover.betrag[19] + tlist.betrag[19]
            turnover.other =  to_decimal(turnover.other) + to_decimal(tlist.other)
            turnover.t_service = turnover.t_service + tlist.t_service
            turnover.t_tax = turnover.t_tax + tlist.t_tax
            turnover.t_debit = turnover.t_debit + tlist.t_debit
            turnover.p_cash = turnover.p_cash + tlist.p_cash
            turnover.p_cash1 = turnover.p_cash1 + tlist.p_cash1
            turnover.r_transfer = turnover.r_transfer + tlist.r_transfer
            turnover.c_ledger = turnover.c_ledger + tlist.c_ledger
            turnover.t_vat =  to_decimal(turnover.t_vat) + to_decimal(tlist.t_vat)
            turnover.rest_deposit =  to_decimal(turnover.rest_deposit) + to_decimal(tlist.rest_deposit)
        nt_cover = turnover.belegung
        nt_betrag[0] = turnover.betrag[0]
        nt_betrag[1] = turnover.betrag[1]
        nt_betrag[2] = turnover.betrag[2]
        nt_betrag[3] = turnover.betrag[3]
        nt_betrag[4] = turnover.betrag[4]
        nt_betrag[5] = turnover.betrag[5]
        nt_betrag[6] = turnover.betrag[6]
        nt_betrag[7] = turnover.betrag[7]
        nt_betrag[8] = turnover.betrag[8]
        nt_betrag[9] = turnover.betrag[9]
        nt_betrag[10] = turnover.betrag[10]
        nt_betrag[11] = turnover.betrag[11]
        nt_betrag[12] = turnover.betrag[12]
        nt_betrag[13] = turnover.betrag[13]
        nt_betrag[14] = turnover.betrag[14]
        nt_betrag[15] = turnover.betrag[15]
        nt_betrag[16] = turnover.betrag[16]
        nt_betrag[17] = turnover.betrag[17]
        nt_betrag[18] = turnover.betrag[18]
        nt_betrag[19] = turnover.betrag[19]
        nt_other =  to_decimal(turnover.other)
        nt_serv = turnover.t_service
        nt_tax = turnover.t_tax
        nt_debit = turnover.t_debit
        nt_cash = turnover.p_cash
        nt_cash1 = turnover.p_cash1
        nt_trans = turnover.r_transfer
        nt_ledger = turnover.c_ledger
        nt_vat = turnover.t_vat


    def fo_discarticle():

        nonlocal t_betrag, t_foreign, exchg_rate, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, nt_cover, tot_other, nt_other, nt_serv, nt_tax, nt_debit, nt_cash, nt_cash1, nt_trans, nt_ledger, tot_vat, nt_vat, avail_outstand_list, turnover_list, t_tot_betrag_list, t_nt_betrag_list, outstand_list_list, pay_list_list, summ_list_list, tot_betrag, nt_betrag, t_cash1, tt_other, anz_comp, val_comp, anz_coup, val_coup, total_fdisc, total_bdisc, total_odisc, t_serv, t_tax, t_debit, t_cash, t_trans, t_ledger, t_cover, fo_disc1, fo_disc2, fo_disc3, tt_betrag, multi_vat, f_endkum, b_endkum, tot_deposit, t_deposit, nt_deposit, qty, counter, artnr_data, i, artnr_list, pax_cash, pax, pax2, htparam, waehrung, h_bill, h_bill_line, artikel, h_journal, h_artikel, kellner, bill, res_line
        nonlocal disc_art1, disc_art2, disc_art3, curr_dept, all_user, shift, from_date, to_date, art_str, voucher_art, zero_vat_compli, show_fbodisc, htl_dept_dptnr
        nonlocal pay_listbuff


        nonlocal other_art, temp, t_tot_betrag, t_nt_betrag, bline_list, outstand_list, pay_list, pay_listbuff, turnover, summ_list, buf_art, t_artnr, tlist, tlist
        nonlocal other_art_list, temp_list, t_tot_betrag_list, t_nt_betrag_list, bline_list_list, outstand_list_list, pay_list_list, turnover_list, summ_list_list, buf_art_list, t_artnr_list


        fo_disc1 = 0
        fo_disc2 = 0
        fo_disc3 = 0

        h_artikel = db_session.query(H_artikel).filter(
                 (H_artikel.artnr == disc_art1) & (H_artikel.departement == curr_dept)).first()

        if h_artikel:

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == curr_dept)).first()

            if artikel:
                fo_disc1 = artikel.artnr

        h_artikel = db_session.query(H_artikel).filter(
                 (H_artikel.artnr == disc_art2) & (H_artikel.departement == curr_dept)).first()

        if h_artikel:

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == curr_dept)).first()

            if artikel:
                fo_disc2 = artikel.artnr

        h_artikel = db_session.query(H_artikel).filter(
                 (H_artikel.artnr == disc_art3) & (H_artikel.departement == curr_dept)).first()

        if h_artikel:

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == curr_dept)).first()

            if artikel:
                fo_disc3 = artikel.artnr


    def cal_fbodisc(billno:int):

        nonlocal t_betrag, t_foreign, exchg_rate, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, nt_cover, tot_other, nt_other, nt_serv, nt_tax, nt_debit, nt_cash, nt_cash1, nt_trans, nt_ledger, tot_vat, nt_vat, avail_outstand_list, turnover_list, t_tot_betrag_list, t_nt_betrag_list, outstand_list_list, pay_list_list, summ_list_list, tot_betrag, nt_betrag, t_cash1, tt_other, anz_comp, val_comp, anz_coup, val_coup, total_fdisc, total_bdisc, total_odisc, t_serv, t_tax, t_debit, t_cash, t_trans, t_ledger, t_cover, fo_disc1, fo_disc2, fo_disc3, tt_betrag, multi_vat, f_endkum, b_endkum, tot_deposit, t_deposit, nt_deposit, qty, counter, artnr_data, artnr_list, pax_cash, pax, pax2, htparam, waehrung, h_bill, h_bill_line, artikel, h_journal, h_artikel, kellner, bill, res_line
        nonlocal disc_art1, disc_art2, disc_art3, curr_dept, all_user, shift, from_date, to_date, art_str, voucher_art, zero_vat_compli, show_fbodisc, htl_dept_dptnr
        nonlocal pay_listbuff


        nonlocal other_art, temp, t_tot_betrag, t_nt_betrag, bline_list, outstand_list, pay_list, pay_listbuff, turnover, summ_list, buf_art, t_artnr, tlist, tlist
        nonlocal other_art_list, temp_list, t_tot_betrag_list, t_nt_betrag_list, bline_list_list, outstand_list_list, pay_list_list, turnover_list, summ_list_list, buf_art_list, t_artnr_list

        vat:decimal = to_decimal("0.0")
        vat2:decimal = to_decimal("0.0")
        service:decimal = to_decimal("0.0")
        fact:decimal = to_decimal("0.0")
        netto:decimal = to_decimal("0.0")
        i:int = 0
        i_artnr:int = 0
        total_fdisc =  to_decimal("0")
        total_bdisc =  to_decimal("0")
        total_odisc =  to_decimal("0")

        if not show_fbodisc:

            return

        h_journal_obj_list = []
        for h_journal, h_artikel in db_session.query(H_journal, H_artikel).join(H_artikel,(H_artikel.artnr == H_journal.artnr) & (H_artikel.departement == H_journal.departement) & (H_artikel.artart == 0)).filter(
                 (H_journal.bill_datum >= from_date) & (H_journal.bill_datum <= to_date) & (H_journal.departement == curr_dept) & (H_journal.rechnr == billno) & (H_journal.betrag != 0)).order_by(H_journal._recid).all():
            if h_journal._recid in h_journal_obj_list:
                continue
            else:
                h_journal_obj_list.append(h_journal._recid)


            service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_journal.bill_datum))

            if multi_vat == False:
                vat =  to_decimal(vat) + to_decimal(vat2)


            netto =  to_decimal(h_journal.betrag) / to_decimal((1) + to_decimal(vat) + to_decimal(vat2) + to_decimal(service))

            if h_artikel.artnr == disc_art1:
                total_fdisc =  to_decimal(total_fdisc) + to_decimal(netto)

            elif h_artikel.artnr == disc_art2:
                total_bdisc =  to_decimal(total_bdisc) + to_decimal(netto)

            elif h_artikel.artnr == disc_art3:
                total_odisc =  to_decimal(total_odisc) + to_decimal(netto)


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 271)).first()
    multi_vat = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 144)).first()

    waehrung = db_session.query(Waehrung).filter(
             (Waehrung.wabkurz == htparam.fchar)).first()

    if waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    else:
        exchg_rate =  to_decimal("1")

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 862)).first()

    if htparam.finteger > 0:
        f_endkum = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 892)).first()

    if htparam.finteger > 0:
        b_endkum = htparam.finteger
    t_artnr_list.clear()
    temp_list.clear()
    for i in range(1,num_entries(art_str, ",")  + 1) :

        if i > 21:
            pass
        else:
            artnr_data[i - 1] = to_int(entry(i - 1, art_str, ","))

            if artnr_data[i - 1] != 0:
                qty = qty + 1
    for i in range(1,qty + 1) :

        buf_art = query(buf_art_list, filters=(lambda buf_art: buf_art.artnr == artnr_data[i - 1] and buf_art.departement == curr_dept), first=True)

        if buf_art:
            counter = counter + 1
            t_artnr = T_artnr()
            t_artnr_list.append(t_artnr)

            t_artnr.nr = counter
            t_artnr.artnr = buf_art.artnr

    for t_artnr in query(t_artnr_list, sort_by=[("nr",False)]):
        artnr_list[t_artnr.nr - 1] = t_artnr.artnr

    if not all_user:
        daysale_list()
    else:
        daysale_list1()

    for turnover in query(turnover_list):

        h_bill = db_session.query(H_bill).filter(
                 (H_bill.rechnr == to_int(turnover.rechnr)) & (H_bill.departement == curr_dept)).first()

        if h_bill and turnover.p_cash != 0:
            pax_cash = pax_cash + turnover.belegung

        if h_bill:
            turnover.belegung = h_bill.belegung

    for pay_list in query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 1 and pay_list.foreign != 0)):
        pax2 = pax2 + 1

    turnover = query(turnover_list, first=True)

    if turnover:

        pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 1 and pay_list.saldo != 0), first=True)

        if pay_list:
            pay_list.person = pax_cash

        pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 1 and pay_list.foreign != 0), first=True)

        if pay_list:
            pay_list.person = pax2

        for pay_list in query(pay_list_list, filters=(lambda pay_list: pay_list.flag != 2)):
            pax = pax + pay_list.person

        turnover = query(turnover_list, filters=(lambda turnover: turnover.rechnr.lower()  == ("G-Total").lower()), first=True)

        if turnover:

            pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 2), first=True)

            if pay_list:
                pay_list.person = turnover.belegung - pax

        if outstand_list:
            avail_outstand_list = True
        t_tot_betrag = T_tot_betrag()
        t_tot_betrag_list.append(t_tot_betrag)

        t_tot_betrag.tot_betrag1 =  to_decimal(tot_betrag[0])
        t_tot_betrag.tot_betrag2 =  to_decimal(tot_betrag[1])
        t_tot_betrag.tot_betrag3 =  to_decimal(tot_betrag[2])
        t_tot_betrag.tot_betrag4 =  to_decimal(tot_betrag[3])
        t_tot_betrag.tot_betrag5 =  to_decimal(tot_betrag[4])
        t_tot_betrag.tot_betrag6 =  to_decimal(tot_betrag[5])
        t_tot_betrag.tot_betrag7 =  to_decimal(tot_betrag[6])
        t_tot_betrag.tot_betrag8 =  to_decimal(tot_betrag[7])
        t_tot_betrag.tot_betrag9 =  to_decimal(tot_betrag[8])
        t_tot_betrag.tot_betrag10 =  to_decimal(tot_betrag[9])
        t_tot_betrag.tot_betrag11 =  to_decimal(tot_betrag[10])
        t_tot_betrag.tot_betrag12 =  to_decimal(tot_betrag[11])
        t_tot_betrag.tot_betrag13 =  to_decimal(tot_betrag[12])
        t_tot_betrag.tot_betrag14 =  to_decimal(tot_betrag[13])
        t_tot_betrag.tot_betrag15 =  to_decimal(tot_betrag[14])
        t_tot_betrag.tot_betrag16 =  to_decimal(tot_betrag[15])
        t_tot_betrag.tot_betrag17 =  to_decimal(tot_betrag[16])
        t_tot_betrag.tot_betrag18 =  to_decimal(tot_betrag[17])
        t_tot_betrag.tot_betrag19 =  to_decimal(tot_betrag[18])
        t_tot_betrag.tot_betrag20 =  to_decimal(tot_betrag[19])


        t_nt_betrag = T_nt_betrag()
        t_nt_betrag_list.append(t_nt_betrag)

        t_nt_betrag.nt_betrag1 =  to_decimal(nt_betrag[0])
        t_nt_betrag.nt_betrag2 =  to_decimal(nt_betrag[1])
        t_nt_betrag.nt_betrag3 =  to_decimal(nt_betrag[2])
        t_nt_betrag.nt_betrag4 =  to_decimal(nt_betrag[3])
        t_nt_betrag.nt_betrag5 =  to_decimal(nt_betrag[4])
        t_nt_betrag.nt_betrag6 =  to_decimal(nt_betrag[5])
        t_nt_betrag.nt_betrag7 =  to_decimal(nt_betrag[6])
        t_nt_betrag.nt_betrag8 =  to_decimal(nt_betrag[7])
        t_nt_betrag.nt_betrag =  to_decimal(nt_betrag[8])
        t_nt_betrag.nt_betrag10 =  to_decimal(nt_betrag[9])
        t_nt_betrag.nt_betrag11 =  to_decimal(nt_betrag[10])
        t_nt_betrag.nt_betrag12 =  to_decimal(nt_betrag[11])
        t_nt_betrag.nt_betrag13 =  to_decimal(nt_betrag[12])
        t_nt_betrag.nt_betrag14 =  to_decimal(nt_betrag[13])
        t_nt_betrag.nt_betrag15 =  to_decimal(nt_betrag[14])
        t_nt_betrag.nt_betrag16 =  to_decimal(nt_betrag[15])
        t_nt_betrag.nt_betrag17 =  to_decimal(nt_betrag[16])
        t_nt_betrag.nt_betrag18 =  to_decimal(nt_betrag[17])
        t_nt_betrag.nt_betrag19 =  to_decimal(nt_betrag[18])
        t_nt_betrag.nt_betrag10 =  to_decimal(nt_betrag[19])


        calculate_disc()

    return generate_output()