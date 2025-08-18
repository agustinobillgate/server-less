#using conversion tools version: 1.0.0.118

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Htparam, Waehrung, H_bill, H_bill_line, Artikel, H_artikel, H_journal, Res_line, Kellner, Bill

bline_list_data, Bline_list = create_model("Bline_list", {"selected":bool, "depart":string, "dept":int, "knr":int, "bl_recid":int}, {"selected": True})
buf_art_data, Buf_art = create_model("Buf_art", {"artnr":int, "bezeich":string, "departement":int})

def rest_daysalesp2_btn_go_6_cldbl(bline_list_data:[Bline_list], buf_art_data:[Buf_art], disc_art1:int, disc_art2:int, disc_art3:int, curr_dept:int, all_user:bool, shift:int, from_date:date, to_date:date, art_str:string, voucher_art:int, zero_vat_compli:bool, exclude_compli:bool, show_fbodisc:bool, htl_dept_dptnr:int, incl_move_table:bool, wig:bool, inhouse:bool):

    prepare_cache ([Htparam, Waehrung, Artikel, H_artikel, H_journal, Res_line, Kellner, Bill])

    t_betrag = to_decimal("0.0")
    t_foreign = to_decimal("0.0")
    exchg_rate = to_decimal("0.0")
    tot_serv = to_decimal("0.0")
    tot_tax = to_decimal("0.0")
    tot_debit = to_decimal("0.0")
    tot_cash = to_decimal("0.0")
    tot_cash1 = to_decimal("0.0")
    tot_trans = to_decimal("0.0")
    tot_ledger = to_decimal("0.0")
    tot_cover = 0
    nt_cover = 0
    tot_other = to_decimal("0.0")
    nt_other = to_decimal("0.0")
    nt_serv = to_decimal("0.0")
    nt_tax = to_decimal("0.0")
    nt_debit = to_decimal("0.0")
    nt_cash = to_decimal("0.0")
    nt_cash1 = to_decimal("0.0")
    nt_trans = to_decimal("0.0")
    nt_ledger = to_decimal("0.0")
    tot_vat = to_decimal("0.0")
    nt_vat = to_decimal("0.0")
    avail_outstand_list = False
    turnover_data = []
    t_tot_betrag_data = []
    t_nt_betrag_data = []
    outstand_list_data = []
    pay_list_data = []
    summ_list_data = []
    tot_betrag:List[Decimal] = create_empty_list(20,to_decimal("0"))
    nt_betrag:List[Decimal] = create_empty_list(20,to_decimal("0"))
    t_cash1:Decimal = to_decimal("0.0")
    tt_other:Decimal = to_decimal("0.0")
    anz_comp:int = 0
    val_comp:Decimal = to_decimal("0.0")
    anz_coup:int = 0
    val_coup:Decimal = to_decimal("0.0")
    total_fdisc:Decimal = to_decimal("0.0")
    total_bdisc:Decimal = to_decimal("0.0")
    total_odisc:Decimal = to_decimal("0.0")
    t_serv:Decimal = to_decimal("0.0")
    t_tax:Decimal = to_decimal("0.0")
    t_debit:Decimal = to_decimal("0.0")
    t_cash:Decimal = to_decimal("0.0")
    t_trans:Decimal = to_decimal("0.0")
    t_ledger:Decimal = to_decimal("0.0")
    t_cover:int = 0
    fo_disc1:int = 0
    fo_disc2:int = 0
    fo_disc3:int = 0
    tt_betrag:List[Decimal] = create_empty_list(20,to_decimal("0"))
    multi_vat:bool = False
    f_endkum:int = 0
    b_endkum:int = 0
    tot_deposit:Decimal = to_decimal("0.0")
    t_deposit:Decimal = to_decimal("0.0")
    nt_deposit:Decimal = to_decimal("0.0")
    qty:int = 0
    counter:int = 0
    artnr_data:List[int] = create_empty_list(20,0)
    i:int = 0
    artnr_list:List[int] = create_empty_list(20,0)
    t_pvoucher:Decimal = to_decimal("0.0")
    tot_pvoucher:Decimal = to_decimal("0.0")
    nt_pvoucher:Decimal = to_decimal("0.0")
    pax_cash:int = 0
    pax:int = 0
    pax2:int = 0
    htparam = waehrung = h_bill = h_bill_line = artikel = h_artikel = h_journal = res_line = kellner = bill = None

    other_art = temp = t_tot_betrag = t_nt_betrag = bline_list = outstand_list = pay_list = pay_listbuff = turnover = summ_list = buf_art = t_artnr = tlist = None

    other_art_data, Other_art = create_model("Other_art", {"artnr":int})
    temp_data, Temp = create_model("Temp", {"rechnr":int})
    t_tot_betrag_data, T_tot_betrag = create_model("T_tot_betrag", {"tot_betrag1":Decimal, "tot_betrag2":Decimal, "tot_betrag3":Decimal, "tot_betrag4":Decimal, "tot_betrag5":Decimal, "tot_betrag6":Decimal, "tot_betrag7":Decimal, "tot_betrag8":Decimal, "tot_betrag9":Decimal, "tot_betrag10":Decimal, "tot_betrag11":Decimal, "tot_betrag12":Decimal, "tot_betrag13":Decimal, "tot_betrag14":Decimal, "tot_betrag15":Decimal, "tot_betrag16":Decimal, "tot_betrag17":Decimal, "tot_betrag18":Decimal, "tot_betrag19":Decimal, "tot_betrag20":Decimal})
    t_nt_betrag_data, T_nt_betrag = create_model("T_nt_betrag", {"nt_betrag1":Decimal, "nt_betrag2":Decimal, "nt_betrag3":Decimal, "nt_betrag4":Decimal, "nt_betrag5":Decimal, "nt_betrag6":Decimal, "nt_betrag7":Decimal, "nt_betrag8":Decimal, "nt_betrag":Decimal, "nt_betrag10":Decimal, "nt_betrag11":Decimal, "nt_betrag12":Decimal, "nt_betrag13":Decimal, "nt_betrag14":Decimal, "nt_betrag15":Decimal, "nt_betrag16":Decimal, "nt_betrag17":Decimal, "nt_betrag18":Decimal, "nt_betrag19":Decimal, "nt_betrag20":Decimal})
    outstand_list_data, Outstand_list = create_model("Outstand_list", {"name":string, "rechnr":int, "foreign":Decimal, "saldo":Decimal})
    pay_list_data, Pay_list = create_model("Pay_list", {"compli":bool, "person":int, "flag":int, "bezeich":string, "artnr":int, "rechnr":int, "foreign":Decimal, "saldo":Decimal}, {"compli": False})
    turnover_data, Turnover = create_model("Turnover", {"departement":int, "kellner_nr":int, "name":string, "tischnr":int, "rechnr":string, "belegung":int, "artnr":int, "info":string, "betrag":[Decimal,20], "other":Decimal, "t_service":Decimal, "t_tax":Decimal, "t_debit":Decimal, "t_credit":Decimal, "p_cash":Decimal, "p_cash1":Decimal, "r_transfer":Decimal, "c_ledger":Decimal, "compli":bool, "flag":int, "gname":string, "int_rechnr":int, "st_comp":int, "p_curr":string, "t_vat":Decimal, "qty_fpax":int, "qty_bpax":int, "qty_opax":int, "rest_deposit":Decimal, "resnr":int, "p_voucher":Decimal, "cvr_food":int, "cvr_bev":int})
    summ_list_data, Summ_list = create_model("Summ_list", {"amount_food":Decimal, "amount_bev":Decimal, "amount_other":Decimal, "disc_food":Decimal, "disc_bev":Decimal, "disc_other":Decimal, "qty_disc_food":int, "qty_disc_bev":int, "qty_disc_other":int})
    t_artnr_data, T_artnr = create_model("T_artnr", {"nr":int, "artnr":int})

    Pay_listbuff = Pay_list
    pay_listbuff_data = pay_list_data

    Tlist = Turnover
    tlist_data = turnover_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_betrag, t_foreign, exchg_rate, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, nt_cover, tot_other, nt_other, nt_serv, nt_tax, nt_debit, nt_cash, nt_cash1, nt_trans, nt_ledger, tot_vat, nt_vat, avail_outstand_list, turnover_data, t_tot_betrag_data, t_nt_betrag_data, outstand_list_data, pay_list_data, summ_list_data, tot_betrag, nt_betrag, t_cash1, tt_other, anz_comp, val_comp, anz_coup, val_coup, total_fdisc, total_bdisc, total_odisc, t_serv, t_tax, t_debit, t_cash, t_trans, t_ledger, t_cover, fo_disc1, fo_disc2, fo_disc3, tt_betrag, multi_vat, f_endkum, b_endkum, tot_deposit, t_deposit, nt_deposit, qty, counter, artnr_data, i, artnr_list, t_pvoucher, tot_pvoucher, nt_pvoucher, pax_cash, pax, pax2, htparam, waehrung, h_bill, h_bill_line, artikel, h_artikel, h_journal, res_line, kellner, bill
        nonlocal disc_art1, disc_art2, disc_art3, curr_dept, all_user, shift, from_date, to_date, art_str, voucher_art, zero_vat_compli, exclude_compli, show_fbodisc, htl_dept_dptnr, incl_move_table, wig, inhouse
        nonlocal pay_listbuff, tlist


        nonlocal other_art, temp, t_tot_betrag, t_nt_betrag, bline_list, outstand_list, pay_list, pay_listbuff, turnover, summ_list, buf_art, t_artnr, tlist
        nonlocal other_art_data, temp_data, t_tot_betrag_data, t_nt_betrag_data, outstand_list_data, pay_list_data, turnover_data, summ_list_data, t_artnr_data

        return {"t_betrag": t_betrag, "t_foreign": t_foreign, "exchg_rate": exchg_rate, "tot_serv": tot_serv, "tot_tax": tot_tax, "tot_debit": tot_debit, "tot_cash": tot_cash, "tot_cash1": tot_cash1, "tot_trans": tot_trans, "tot_ledger": tot_ledger, "tot_cover": tot_cover, "nt_cover": nt_cover, "tot_other": tot_other, "nt_other": nt_other, "nt_serv": nt_serv, "nt_tax": nt_tax, "nt_debit": nt_debit, "nt_cash": nt_cash, "nt_cash1": nt_cash1, "nt_trans": nt_trans, "nt_ledger": nt_ledger, "tot_vat": tot_vat, "nt_vat": nt_vat, "avail_outstand_list": avail_outstand_list, "turnover": turnover_data, "t-tot-betrag": t_tot_betrag_data, "t-nt-betrag": t_nt_betrag_data, "outstand-list": outstand_list_data, "pay-list": pay_list_data, "summ-list": summ_list_data}

    def calculate_disc():

        nonlocal t_betrag, t_foreign, exchg_rate, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, nt_cover, tot_other, nt_other, nt_serv, nt_tax, nt_debit, nt_cash, nt_cash1, nt_trans, nt_ledger, tot_vat, nt_vat, avail_outstand_list, turnover_data, t_tot_betrag_data, t_nt_betrag_data, outstand_list_data, pay_list_data, summ_list_data, tot_betrag, nt_betrag, t_cash1, tt_other, anz_comp, val_comp, anz_coup, val_coup, total_fdisc, total_bdisc, total_odisc, t_serv, t_tax, t_debit, t_cash, t_trans, t_ledger, t_cover, fo_disc1, fo_disc2, fo_disc3, tt_betrag, multi_vat, f_endkum, b_endkum, tot_deposit, t_deposit, nt_deposit, qty, counter, artnr_data, artnr_list, t_pvoucher, tot_pvoucher, nt_pvoucher, pax_cash, pax, pax2, htparam, waehrung, h_bill, h_bill_line, artikel, h_artikel, h_journal, res_line, kellner, bill
        nonlocal disc_art1, disc_art2, disc_art3, curr_dept, all_user, shift, from_date, to_date, art_str, voucher_art, zero_vat_compli, exclude_compli, show_fbodisc, htl_dept_dptnr, incl_move_table, wig, inhouse
        nonlocal pay_listbuff, tlist


        nonlocal other_art, temp, t_tot_betrag, t_nt_betrag, bline_list, outstand_list, pay_list, pay_listbuff, turnover, summ_list, buf_art, t_artnr, tlist
        nonlocal other_art_data, temp_data, t_tot_betrag_data, t_nt_betrag_data, outstand_list_data, pay_list_data, turnover_data, summ_list_data, t_artnr_data

        amt_food:Decimal = to_decimal("0.0")
        amt_bev:Decimal = to_decimal("0.0")
        amt_other:Decimal = to_decimal("0.0")
        amt_food_disc:Decimal = to_decimal("0.0")
        amt_bev_disc:Decimal = to_decimal("0.0")
        amt_other_disc:Decimal = to_decimal("0.0")
        qty_food_disc:Decimal = to_decimal("0.0")
        qty_bev_disc:Decimal = to_decimal("0.0")
        qty_other_disc:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        netto:Decimal = to_decimal("0.0")
        i:int = 0
        i_artnr:int = 0
        curr_date:date = None
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
        for curr_date in date_range(from_date,to_date) :

            h_journal_obj_list = {}
            for h_journal, h_artikel, artikel in db_session.query(H_journal, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_journal.artnr) & (H_artikel.departement == curr_dept)).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == curr_dept)).filter(
                     (H_journal.departement == curr_dept) & (H_journal.bill_datum == curr_date) & (H_journal.betrag != 0) & ((H_journal.artnr == disc_art1) | (H_journal.artnr == disc_art2) | (H_journal.artnr == disc_art3))).order_by(H_journal._recid).all():
                turnover = query(turnover_data, (lambda turnover: turnover.rechnr == to_string(h_journal.rechnr) and turnover.departement == h_journal.departement and turnover.flag == 0), first=True)
                if not turnover:
                    continue

                if h_journal_obj_list.get(h_journal._recid):
                    continue
                else:
                    h_journal_obj_list[h_journal._recid] = True


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
        summ_list = Summ_list()
        summ_list_data.append(summ_list)

        summ_list.disc_food =  to_decimal(amt_food_disc)
        summ_list.disc_bev =  to_decimal(amt_bev_disc)
        summ_list.disc_other =  to_decimal(amt_other_disc)
        summ_list.qty_disc_food = qty_food_disc
        summ_list.qty_disc_bev = qty_bev_disc
        summ_list.qty_disc_other = qty_other_disc


    def daysale_list1():

        nonlocal t_betrag, t_foreign, exchg_rate, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, nt_cover, tot_other, nt_other, nt_serv, nt_tax, nt_debit, nt_cash, nt_cash1, nt_trans, nt_ledger, tot_vat, nt_vat, avail_outstand_list, turnover_data, t_tot_betrag_data, t_nt_betrag_data, outstand_list_data, pay_list_data, summ_list_data, tot_betrag, nt_betrag, t_cash1, tt_other, anz_comp, val_comp, anz_coup, val_coup, total_fdisc, total_bdisc, total_odisc, t_serv, t_tax, t_debit, t_cash, t_trans, t_ledger, t_cover, fo_disc1, fo_disc2, fo_disc3, tt_betrag, multi_vat, f_endkum, b_endkum, tot_deposit, t_deposit, nt_deposit, qty, counter, artnr_data, artnr_list, t_pvoucher, tot_pvoucher, nt_pvoucher, pax_cash, pax, pax2, htparam, waehrung, h_bill, h_bill_line, artikel, h_artikel, h_journal, res_line, kellner, bill
        nonlocal disc_art1, disc_art2, disc_art3, curr_dept, all_user, shift, from_date, to_date, art_str, voucher_art, zero_vat_compli, exclude_compli, show_fbodisc, htl_dept_dptnr, incl_move_table, wig, inhouse
        nonlocal pay_listbuff, tlist


        nonlocal other_art, temp, t_tot_betrag, t_nt_betrag, bline_list, outstand_list, pay_list, pay_listbuff, turnover, summ_list, buf_art, t_artnr, tlist
        nonlocal other_art_data, temp_data, t_tot_betrag_data, t_nt_betrag_data, outstand_list_data, pay_list_data, turnover_data, summ_list_data, t_artnr_data

        curr_s:int = 0
        billnr:int = 0
        dept:int = 1
        d_name:string = ""
        usr_nr:int = 0
        d_found:bool = False
        c_found:bool = False
        vat:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        netto:Decimal = to_decimal("0.0")
        i:int = 0
        pos:int = 0
        bill_no:int = 0
        guestname:string = ""
        found:bool = False
        found_artpay:bool = False
        curr_date:date = None
        cancel_pay:bool = False
        h_bline = None
        buf_hbline = None
        b_hbline = None
        b_hartikel = None
        b_hbill = None
        H_bline =  create_buffer("H_bline",H_bill_line)
        Buf_hbline =  create_buffer("Buf_hbline",H_bill_line)
        B_hbline =  create_buffer("B_hbline",H_bill_line)
        B_hartikel =  create_buffer("B_hartikel",H_artikel)
        B_hbill =  create_buffer("B_hbill",H_bill)
        t_betrag =  to_decimal("0")
        t_foreign =  to_decimal("0")

        for turnover in query(turnover_data):
            turnover_data.remove(turnover)

        for pay_list in query(pay_list_data):
            pay_list_data.remove(pay_list)

        for outstand_list in query(outstand_list_data):
            outstand_list_data.remove(outstand_list)
        for i in range(1,20 + 1) :
            tot_betrag[i - 1] = 0
        tot_cover = 0
        tot_other =  to_decimal("0")
        tot_serv =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_debit =  to_decimal("0")
        tot_cash1 =  to_decimal("0")
        tot_cash =  to_decimal("0")
        tot_trans =  to_decimal("0")
        tot_ledger =  to_decimal("0")
        tot_vat =  to_decimal("0")
        nt_cover = 0
        for i in range(1,20 + 1) :
            nt_betrag[i - 1] = 0
        nt_other =  to_decimal("0")
        nt_serv =  to_decimal("0")
        nt_tax =  to_decimal("0")
        nt_debit =  to_decimal("0")
        nt_cash1 =  to_decimal("0")
        nt_cash =  to_decimal("0")
        nt_trans =  to_decimal("0")
        nt_vat =  to_decimal("0")
        nt_pvoucher =  to_decimal("0")

        for h_bill in db_session.query(H_bill).filter(
                 (H_bill.flag == 0) & (H_bill.saldo != 0) & (H_bill.departement == curr_dept)).order_by(H_bill._recid).all():

            if inhouse:

                res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                if res_line:

                    kellner = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)]})
                    outstand_list = Outstand_list()
                    outstand_list_data.append(outstand_list)

                    outstand_list.rechnr = h_bill.rechnr

                    if kellner:
                        outstand_list.name = kellner.kellnername

                    for h_bill_line in db_session.query(H_bill_line).filter(
                             (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == curr_dept)).order_by(H_bill_line._recid).all():
                        outstand_list.saldo =  to_decimal(outstand_list.saldo) + to_decimal(h_bill_line.betrag)
                        outstand_list.foreign =  to_decimal(outstand_list.foreign) + to_decimal(h_bill_line.fremdwbetrag)

            elif wig:

                res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                if not res_line:

                    kellner = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)]})
                    outstand_list = Outstand_list()
                    outstand_list_data.append(outstand_list)

                    outstand_list.rechnr = h_bill.rechnr

                    if kellner:
                        outstand_list.name = kellner.kellnername

                    for h_bill_line in db_session.query(H_bill_line).filter(
                             (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == curr_dept)).order_by(H_bill_line._recid).all():
                        outstand_list.saldo =  to_decimal(outstand_list.saldo) + to_decimal(h_bill_line.betrag)
                        outstand_list.foreign =  to_decimal(outstand_list.foreign) + to_decimal(h_bill_line.fremdwbetrag)
            else:

                kellner = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)]})
                outstand_list = Outstand_list()
                outstand_list_data.append(outstand_list)

                outstand_list.rechnr = h_bill.rechnr

                if kellner:
                    outstand_list.name = kellner.kellnername

                for h_bill_line in db_session.query(H_bill_line).filter(
                         (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == curr_dept)).order_by(H_bill_line._recid).all():
                    outstand_list.saldo =  to_decimal(outstand_list.saldo) + to_decimal(h_bill_line.betrag)
                    outstand_list.foreign =  to_decimal(outstand_list.foreign) + to_decimal(h_bill_line.fremdwbetrag)

        for h_bill in db_session.query(H_bill).filter(
                 (H_bill.flag == 1) & (H_bill.departement == curr_dept)).order_by(H_bill._recid).all():

            if inhouse:

                res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                if res_line:
                    daysale1()

            elif wig:

                res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                if not res_line:
                    daysale1()
            else:
                daysale1()

        if incl_move_table:
            for curr_date in date_range(from_date,to_date) :

                for h_journal in db_session.query(H_journal).filter(
                         (H_journal.bill_datum == curr_date) & (H_journal.departement == curr_dept)).order_by(H_journal.bill_datum, H_journal.rechnr).all():

                    b_hbill = db_session.query(B_hbill).filter(
                             (B_hbill.rechnr == h_journal.rechnr) & (B_hbill.departement == h_journal.departement)).first()

                    if not b_hbill:
                        turnover = Turnover()
                        turnover_data.append(turnover)

                        turnover.rechnr = trim(to_string(h_journal.rechnr))
                        turnover.belegung = 0
                        turnover.qty_fpax = 0
                        turnover.qty_bpax = 0
                        turnover.betrag[0] = 0
                        turnover.betrag[1] = 0
                        turnover.betrag[2] = 0
                        turnover.betrag[3] = 0
                        turnover.betrag[4] = 0
                        turnover.betrag[5] = 0
                        turnover.betrag[6] = 0
                        turnover.betrag[7] = 0
                        turnover.betrag[8] = 0
                        turnover.betrag[9] = 0
                        turnover.betrag[10] = 0
                        turnover.betrag[11] = 0
                        turnover.betrag[12] = 0
                        turnover.betrag[13] = 0
                        turnover.betrag[14] = 0
                        turnover.betrag[15] = 0
                        turnover.betrag[16] = 0
                        turnover.betrag[17] = 0
                        turnover.betrag[18] = 0
                        turnover.betrag[19] = 0
                        turnover.other =  to_decimal("0")
                        turnover.t_service =  to_decimal("0")
                        turnover.t_vat =  to_decimal("0")
                        turnover.t_tax =  to_decimal("0")
                        turnover.t_debit =  to_decimal("0")
                        turnover.rest_deposit =  to_decimal("0")
                        turnover.p_cash =  to_decimal("0")
                        turnover.p_curr = ""
                        turnover.p_cash1 =  to_decimal("0")
                        turnover.r_transfer =  to_decimal("0")
                        turnover.c_ledger =  to_decimal("0")
                        turnover.info = ""
                        turnover.gname = ""
                        turnover.flag = 0
                        turnover.compli = False
                        turnover.p_voucher =  to_decimal("0")
                        turnover.resnr = b_hbill.resnr
                        turnover.cvr_food = 0
                        turnover.cvr_bev = 0

        if zero_vat_compli:

            for tlist in query(tlist_data, filters=(lambda tlist: tlist.compli)):

                pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 6), first=True)

                if pay_list and tlist.st_comp == 1:
                    pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(tlist.t_service) - to_decimal(tlist.t_tax)
                    t_betrag =  to_decimal(t_betrag) - to_decimal(tlist.t_service) - to_decimal(tlist.t_tax)

                if tlist.r_transfer != 0 and tlist.t_debit != 0:
                    tlist.r_transfer =  to_decimal(tlist.r_transfer) - to_decimal(tlist.t_service) - to_decimal(tlist.t_tax)
                    tlist.t_debit =  to_decimal(tlist.t_debit) - to_decimal(tlist.t_service) - to_decimal(tlist.t_tax)
                    tot_trans =  to_decimal(tot_trans) - to_decimal(tlist.t_service) - to_decimal(tlist.t_tax)
                    tot_debit =  to_decimal(tot_debit) - to_decimal(tlist.t_service) - to_decimal(tlist.t_tax)


                tot_serv =  to_decimal(tot_serv) - to_decimal(tlist.t_service)
                tot_tax =  to_decimal(tot_tax) - to_decimal(tlist.t_tax)
                tot_vat =  to_decimal(tot_vat) - to_decimal(tlist.t_vat)
                tlist.t_service =  to_decimal("0")
                tlist.t_tax =  to_decimal("0")


        if show_fbodisc:
            fo_discarticle()

            for tlist in query(tlist_data):
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
        turnover_data.append(turnover)

        turnover.rechnr = "G-TOTAL"
        turnover.flag = 2

        if exclude_compli:

            for tlist in query(tlist_data, filters=(lambda tlist: tlist.flag == 0 and not tlist.compli)):
                turnover.belegung = turnover.belegung + tlist.belegung
                turnover.qty_fpax = turnover.qty_fpax + tlist.qty_fpax
                turnover.qty_bpax = turnover.qty_bpax + tlist.qty_bpax
                turnover.qty_opax = turnover.qty_opax + tlist.qty_opax
                turnover.cvr_food = turnover.cvr_food + tlist.cvr_food
                turnover.cvr_bev = turnover.cvr_bev + tlist.cvr_bev
                for i in range(1,20 + 1) :
                    turnover.betrag[i - 1] = turnover.betrag[i - 1] + tlist.betrag[i - 1]


                turnover.other =  to_decimal(turnover.other) + to_decimal(tlist.other)
                turnover.t_service =  to_decimal(turnover.t_service) + to_decimal(tlist.t_service)
                turnover.t_tax =  to_decimal(turnover.t_tax) + to_decimal(tlist.t_tax)
                turnover.t_debit =  to_decimal(turnover.t_debit) + to_decimal(tlist.t_debit)
                turnover.p_cash =  to_decimal(turnover.p_cash) + to_decimal(tlist.p_cash)
                turnover.p_cash1 =  to_decimal(turnover.p_cash1) + to_decimal(tlist.p_cash1)
                turnover.r_transfer =  to_decimal(turnover.r_transfer) + to_decimal(tlist.r_transfer)
                turnover.c_ledger =  to_decimal(turnover.c_ledger) + to_decimal(tlist.c_ledger)
                turnover.t_vat =  to_decimal(turnover.t_vat) + to_decimal(tlist.t_vat)
                turnover.rest_deposit =  to_decimal(turnover.rest_deposit) + to_decimal(tlist.rest_deposit)
                turnover.p_voucher =  to_decimal(turnover.p_voucher) + to_decimal(tlist.p_voucher)
            else:

                for tlist in query(tlist_data, filters=(lambda tlist: tlist.flag == 0)):
                    turnover.belegung = turnover.belegung + tlist.belegung
                    turnover.qty_fpax = turnover.qty_fpax + tlist.qty_fpax
                    turnover.qty_bpax = turnover.qty_bpax + tlist.qty_bpax
                    turnover.qty_opax = turnover.qty_opax + tlist.qty_opax
                    turnover.cvr_food = turnover.cvr_food + tlist.cvr_food
                    turnover.cvr_bev = turnover.cvr_bev + tlist.cvr_bev
                    for i in range(1,20 + 1) :
                        turnover.betrag[i - 1] = turnover.betrag[i - 1] + tlist.betrag[i - 1]


                    turnover.other =  to_decimal(turnover.other) + to_decimal(tlist.other)
                    turnover.t_service =  to_decimal(turnover.t_service) + to_decimal(tlist.t_service)
                    turnover.t_tax =  to_decimal(turnover.t_tax) + to_decimal(tlist.t_tax)
                    turnover.t_debit =  to_decimal(turnover.t_debit) + to_decimal(tlist.t_debit)
                    turnover.p_cash =  to_decimal(turnover.p_cash) + to_decimal(tlist.p_cash)
                    turnover.p_cash1 =  to_decimal(turnover.p_cash1) + to_decimal(tlist.p_cash1)
                    turnover.r_transfer =  to_decimal(turnover.r_transfer) + to_decimal(tlist.r_transfer)
                    turnover.c_ledger =  to_decimal(turnover.c_ledger) + to_decimal(tlist.c_ledger)
                    turnover.t_vat =  to_decimal(turnover.t_vat) + to_decimal(tlist.t_vat)
                    turnover.rest_deposit =  to_decimal(turnover.rest_deposit) + to_decimal(tlist.rest_deposit)
                    turnover.p_voucher =  to_decimal(turnover.p_voucher) + to_decimal(tlist.p_voucher)
        turnover = Turnover()
        turnover_data.append(turnover)

        turnover.rechnr = "R-TOTAL"
        turnover.flag = 3

        for tlist in query(tlist_data, filters=(lambda tlist: tlist.flag == 0 and not tlist.compli)):
            turnover.belegung = turnover.belegung + tlist.belegung
            turnover.qty_fpax = turnover.qty_fpax + tlist.qty_fpax
            turnover.qty_bpax = turnover.qty_bpax + tlist.qty_bpax
            turnover.qty_opax = turnover.qty_opax + tlist.qty_opax
            turnover.cvr_food = turnover.cvr_food + tlist.cvr_food
            turnover.cvr_bev = turnover.cvr_bev + tlist.cvr_bev
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
            turnover.t_service =  to_decimal(turnover.t_service) + to_decimal(tlist.t_service)
            turnover.t_tax =  to_decimal(turnover.t_tax) + to_decimal(tlist.t_tax)
            turnover.t_debit =  to_decimal(turnover.t_debit) + to_decimal(tlist.t_debit)
            turnover.p_cash =  to_decimal(turnover.p_cash) + to_decimal(tlist.p_cash)
            turnover.p_cash1 =  to_decimal(turnover.p_cash1) + to_decimal(tlist.p_cash1)
            turnover.r_transfer =  to_decimal(turnover.r_transfer) + to_decimal(tlist.r_transfer)
            turnover.c_ledger =  to_decimal(turnover.c_ledger) + to_decimal(tlist.c_ledger)
            turnover.t_vat =  to_decimal(turnover.t_vat) + to_decimal(tlist.t_vat)
            turnover.rest_deposit =  to_decimal(turnover.rest_deposit) + to_decimal(tlist.rest_deposit)
            turnover.p_voucher =  to_decimal(turnover.p_voucher) + to_decimal(tlist.p_voucher)
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
        nt_serv =  to_decimal(turnover.t_service)
        nt_tax =  to_decimal(turnover.t_tax)
        nt_debit =  to_decimal(turnover.t_debit)
        nt_cash =  to_decimal(turnover.p_cash)
        nt_cash1 =  to_decimal(turnover.p_cash1)
        nt_trans =  to_decimal(turnover.r_transfer)
        nt_ledger =  to_decimal(turnover.c_ledger)
        nt_vat =  to_decimal(turnover.t_vat)
        nt_pvoucher =  to_decimal(turnover.p_voucher)


    def daysale_list():

        nonlocal t_betrag, t_foreign, exchg_rate, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, nt_cover, tot_other, nt_other, nt_serv, nt_tax, nt_debit, nt_cash, nt_cash1, nt_trans, nt_ledger, tot_vat, nt_vat, avail_outstand_list, turnover_data, t_tot_betrag_data, t_nt_betrag_data, outstand_list_data, pay_list_data, summ_list_data, tot_betrag, nt_betrag, t_cash1, tt_other, anz_comp, val_comp, anz_coup, val_coup, total_fdisc, total_bdisc, total_odisc, t_serv, t_tax, t_debit, t_cash, t_trans, t_ledger, t_cover, fo_disc1, fo_disc2, fo_disc3, tt_betrag, multi_vat, f_endkum, b_endkum, tot_deposit, t_deposit, nt_deposit, qty, counter, artnr_data, artnr_list, t_pvoucher, tot_pvoucher, nt_pvoucher, pax_cash, pax, pax2, htparam, waehrung, h_bill, h_bill_line, artikel, h_artikel, h_journal, res_line, kellner, bill
        nonlocal disc_art1, disc_art2, disc_art3, curr_dept, all_user, shift, from_date, to_date, art_str, voucher_art, zero_vat_compli, exclude_compli, show_fbodisc, htl_dept_dptnr, incl_move_table, wig, inhouse
        nonlocal pay_listbuff, tlist


        nonlocal other_art, temp, t_tot_betrag, t_nt_betrag, bline_list, outstand_list, pay_list, pay_listbuff, turnover, summ_list, buf_art, t_artnr, tlist
        nonlocal other_art_data, temp_data, t_tot_betrag_data, t_nt_betrag_data, outstand_list_data, pay_list_data, turnover_data, summ_list_data, t_artnr_data

        curr_s:int = 0
        billnr:int = 0
        dept:int = 1
        d_name:string = ""
        usr_nr:int = 0
        d_found:bool = False
        c_found:bool = False
        vat:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        netto:Decimal = to_decimal("0.0")
        i:int = 0
        found:bool = False
        compli:bool = False
        guestname:string = ""
        bill_no:int = 0
        pos:int = 0
        curr_date:date = None
        cancel_pay:bool = False
        kellner1 = None
        h_bline = None
        buf_hbline = None
        b_hbline = None
        b_hbill = None
        Kellner1 =  create_buffer("Kellner1",Kellner)
        H_bline =  create_buffer("H_bline",H_bill_line)
        Buf_hbline =  create_buffer("Buf_hbline",H_bill_line)
        B_hbline =  create_buffer("B_hbline",H_bill_line)
        B_hbill =  create_buffer("B_hbill",H_bill)

        for turnover in query(turnover_data):
            turnover_data.remove(turnover)

        for pay_list in query(pay_list_data):
            pay_list_data.remove(pay_list)

        for outstand_list in query(outstand_list_data):
            outstand_list_data.remove(outstand_list)
        t_betrag =  to_decimal("0")
        t_foreign =  to_decimal("0")
        for i in range(1,20 + 1) :
            tot_betrag[i - 1] = 0
        tot_cover = 0
        tot_serv =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_debit =  to_decimal("0")
        tot_cash1 =  to_decimal("0")
        tot_cash =  to_decimal("0")
        tot_trans =  to_decimal("0")
        tot_ledger =  to_decimal("0")
        tot_vat =  to_decimal("0")
        for i in range(1,20 + 1) :
            nt_betrag[i - 1] = 0
        nt_cover = 0
        nt_serv =  to_decimal("0")
        nt_tax =  to_decimal("0")
        nt_debit =  to_decimal("0")
        nt_cash1 =  to_decimal("0")
        nt_cash =  to_decimal("0")
        nt_trans =  to_decimal("0")
        nt_ledger =  to_decimal("0")
        nt_vat =  to_decimal("0")
        nt_pvoucher =  to_decimal("0")

        for bline_list in query(bline_list_data, filters=(lambda bline_list: bline_list.recid (kellner) == bline_list.bl_recid and kellner.departement == curr_dept)):

            for h_bill in db_session.query(H_bill).filter(
                     (H_bill.flag == 0) & (H_bill.saldo != 0) & (H_bill.departement == bline_list.dept)).order_by(H_bill._recid).all():

                if inhouse:

                    res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                    if res_line:
                        outstand_list = Outstand_list()
                        outstand_list_data.append(outstand_list)


                        kellner1 = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, h_bill.departement)]})
                        outstand_list.rechnr = h_bill.rechnr

                        if kellner1:
                            outstand_list.name = kellner1.kellnername
                        else:
                            outstand_list.name = to_string(h_bill.kellner_nr)

                        for h_bill_line in db_session.query(H_bill_line).filter(
                                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == curr_dept)).order_by(H_bill_line._recid).all():
                            outstand_list.saldo =  to_decimal(outstand_list.saldo) + to_decimal(h_bill_line.betrag)
                            outstand_list.foreign =  to_decimal(outstand_list.foreign) + to_decimal(h_bill_line.fremdwbetrag)

                elif wig:

                    res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                    if not res_line:
                        outstand_list = Outstand_list()
                        outstand_list_data.append(outstand_list)


                        kellner1 = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, h_bill.departement)]})
                        outstand_list.rechnr = h_bill.rechnr

                        if kellner1:
                            outstand_list.name = kellner1.kellnername
                        else:
                            outstand_list.name = to_string(h_bill.kellner_nr)

                        for h_bill_line in db_session.query(H_bill_line).filter(
                                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == curr_dept)).order_by(H_bill_line._recid).all():
                            outstand_list.saldo =  to_decimal(outstand_list.saldo) + to_decimal(h_bill_line.betrag)
                            outstand_list.foreign =  to_decimal(outstand_list.foreign) + to_decimal(h_bill_line.fremdwbetrag)
                else:
                    outstand_list = Outstand_list()
                    outstand_list_data.append(outstand_list)


                    kellner1 = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, h_bill.departement)]})
                    outstand_list.rechnr = h_bill.rechnr

                    if kellner1:
                        outstand_list.name = kellner1.kellnername
                    else:
                        outstand_list.name = to_string(h_bill.kellner_nr)

                    for h_bill_line in db_session.query(H_bill_line).filter(
                             (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == curr_dept)).order_by(H_bill_line._recid).all():
                        outstand_list.saldo =  to_decimal(outstand_list.saldo) + to_decimal(h_bill_line.betrag)
                        outstand_list.foreign =  to_decimal(outstand_list.foreign) + to_decimal(h_bill_line.fremdwbetrag)

            for h_bill in db_session.query(H_bill).filter(
                     (H_bill.flag == 1) & (H_bill.departement == bline_list.dept) & (H_bill.kellner_nr == kellner.kellner_nr)).order_by(H_bill._recid).all():

                if inhouse:

                    res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                    if res_line:
                        daysale()

                elif wig:

                    res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                    if not res_line:
                        daysale()
                else:
                    daysale()

            if incl_move_table:
                for curr_date in date_range(from_date,to_date) :

                    for h_journal in db_session.query(H_journal).filter(
                             (H_journal.bill_datum == curr_date) & (H_journal.departement == curr_dept)).order_by(H_journal.bill_datum, H_journal.rechnr).all():

                        b_hbill = db_session.query(B_hbill).filter(
                                 (B_hbill.rechnr == h_journal.rechnr) & (B_hbill.departement == h_journal.departement)).first()

                        if not b_hbill:
                            turnover = Turnover()
                            turnover_data.append(turnover)

                            turnover.rechnr = trim(to_string(h_journal.rechnr))
                            turnover.belegung = 0
                            turnover.qty_fpax = 0
                            turnover.qty_bpax = 0
                            turnover.betrag[0] = 0
                            turnover.betrag[1] = 0
                            turnover.betrag[2] = 0
                            turnover.betrag[3] = 0
                            turnover.betrag[4] = 0
                            turnover.betrag[5] = 0
                            turnover.betrag[6] = 0
                            turnover.betrag[7] = 0
                            turnover.betrag[8] = 0
                            turnover.betrag[9] = 0
                            turnover.betrag[10] = 0
                            turnover.betrag[11] = 0
                            turnover.betrag[12] = 0
                            turnover.betrag[13] = 0
                            turnover.betrag[14] = 0
                            turnover.betrag[15] = 0
                            turnover.betrag[16] = 0
                            turnover.betrag[17] = 0
                            turnover.betrag[18] = 0
                            turnover.betrag[19] = 0
                            turnover.other =  to_decimal("0")
                            turnover.t_service =  to_decimal("0")
                            turnover.t_vat =  to_decimal("0")
                            turnover.t_tax =  to_decimal("0")
                            turnover.t_debit =  to_decimal("0")
                            turnover.rest_deposit =  to_decimal("0")
                            turnover.p_cash =  to_decimal("0")
                            turnover.p_curr = ""
                            turnover.p_cash1 =  to_decimal("0")
                            turnover.r_transfer =  to_decimal("0")
                            turnover.c_ledger =  to_decimal("0")
                            turnover.info = ""
                            turnover.gname = ""
                            turnover.flag = 0
                            turnover.compli = False
                            turnover.p_voucher =  to_decimal("0")
                            turnover.resnr = b_hbill.resnr
                            turnover.cvr_food = 0
                            turnover.cvr_bev = 0

            if zero_vat_compli:

                for tlist in query(tlist_data, filters=(lambda tlist: tlist.compli)):

                    pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 6), first=True)

                    if pay_list:
                        pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(tlist.t_service) - to_decimal(tlist.t_tax)
                        t_betrag =  to_decimal(t_betrag) - to_decimal(tlist.t_service) - to_decimal(tlist.t_tax)

                    if tlist.r_transfer != 0 and tlist.t_debit != 0:
                        tlist.r_transfer =  to_decimal(tlist.r_transfer) - to_decimal(tlist.t_service) - to_decimal(tlist.t_tax)
                        tlist.t_debit =  to_decimal(tlist.t_debit) - to_decimal(tlist.t_service) - to_decimal(tlist.t_tax)
                        tot_trans =  to_decimal(tot_trans) - to_decimal(tlist.t_service) - to_decimal(tlist.t_tax)
                        tot_debit =  to_decimal(tot_debit) - to_decimal(tlist.t_service) - to_decimal(tlist.t_tax)


                    tot_serv =  to_decimal(tot_serv) - to_decimal(tlist.t_service)
                    tot_tax =  to_decimal(tot_tax) - to_decimal(tlist.t_tax)
                    tot_vat =  to_decimal(tot_vat) - to_decimal(tlist.t_vat)
                    tlist.t_service =  to_decimal("0")
                    tlist.t_tax =  to_decimal("0")
                    tlist.t_vat =  to_decimal("0")


            if show_fbodisc:
                fo_discarticle()

                for tlist in query(tlist_data):
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
        turnover_data.append(turnover)

        turnover.rechnr = "G-TOTAL"
        turnover.flag = 2

        if exclude_compli:

            for tlist in query(tlist_data, filters=(lambda tlist: tlist.flag == 0 and not tlist.compli)):
                turnover.belegung = turnover.belegung + tlist.belegung
                turnover.qty_fpax = turnover.qty_fpax + tlist.qty_fpax
                turnover.qty_bpax = turnover.qty_bpax + tlist.qty_bpax
                turnover.qty_opax = turnover.qty_opax + tlist.qty_opax
                turnover.cvr_food = turnover.cvr_food + tlist.cvr_food
                turnover.cvr_bev = turnover.cvr_bev + tlist.cvr_bev
                for i in range(1,20 + 1) :
                    turnover.betrag[i - 1] = turnover.betrag[i - 1] + tlist.betrag[i - 1]
                    tot_betrag[i - 1] = tot_betrag[i - 1] + tlist.betrag[i - 1]


                turnover.other =  to_decimal(turnover.other) + to_decimal(tlist.other)
                turnover.t_service =  to_decimal(turnover.t_service) + to_decimal(tlist.t_service)
                turnover.t_tax =  to_decimal(turnover.t_tax) + to_decimal(tlist.t_tax)
                turnover.t_debit =  to_decimal(turnover.t_debit) + to_decimal(tlist.t_debit)
                turnover.p_cash =  to_decimal(turnover.p_cash) + to_decimal(tlist.p_cash)
                turnover.p_cash1 =  to_decimal(turnover.p_cash1) + to_decimal(tlist.p_cash1)
                turnover.r_transfer =  to_decimal(turnover.r_transfer) + to_decimal(tlist.r_transfer)
                turnover.c_ledger =  to_decimal(turnover.c_ledger) + to_decimal(tlist.c_ledger)
                turnover.t_vat =  to_decimal(turnover.t_vat) + to_decimal(tlist.t_vat)
                turnover.rest_deposit =  to_decimal(turnover.rest_deposit) + to_decimal(tlist.rest_deposit)
                turnover.p_voucher =  to_decimal(turnover.p_voucher) + to_decimal(tlist.p_voucher)
            else:

                for tlist in query(tlist_data, filters=(lambda tlist: tlist.flag == 0)):
                    turnover.belegung = turnover.belegung + tlist.belegung
                    turnover.qty_fpax = turnover.qty_fpax + tlist.qty_fpax
                    turnover.qty_bpax = turnover.qty_bpax + tlist.qty_bpax
                    turnover.qty_opax = turnover.qty_opax + tlist.qty_opax
                    turnover.cvr_food = turnover.cvr_food + tlist.cvr_food
                    turnover.cvr_bev = turnover.cvr_bev + tlist.cvr_bev
                    for i in range(1,20 + 1) :
                        turnover.betrag[i - 1] = turnover.betrag[i - 1] + tlist.betrag[i - 1]
                        tot_betrag[i - 1] = tot_betrag[i - 1] + tlist.betrag[i - 1]


                    turnover.other =  to_decimal(turnover.other) + to_decimal(tlist.other)
                    turnover.t_service =  to_decimal(turnover.t_service) + to_decimal(tlist.t_service)
                    turnover.t_tax =  to_decimal(turnover.t_tax) + to_decimal(tlist.t_tax)
                    turnover.t_debit =  to_decimal(turnover.t_debit) + to_decimal(tlist.t_debit)
                    turnover.p_cash =  to_decimal(turnover.p_cash) + to_decimal(tlist.p_cash)
                    turnover.p_cash1 =  to_decimal(turnover.p_cash1) + to_decimal(tlist.p_cash1)
                    turnover.r_transfer =  to_decimal(turnover.r_transfer) + to_decimal(tlist.r_transfer)
                    turnover.c_ledger =  to_decimal(turnover.c_ledger) + to_decimal(tlist.c_ledger)
                    turnover.t_vat =  to_decimal(turnover.t_vat) + to_decimal(tlist.t_vat)
                    turnover.rest_deposit =  to_decimal(turnover.rest_deposit) + to_decimal(tlist.rest_deposit)
                    turnover.p_voucher =  to_decimal(turnover.p_voucher) + to_decimal(tlist.p_voucher)
        turnover = Turnover()
        turnover_data.append(turnover)

        turnover.rechnr = "R-TOTAL"
        turnover.flag = 3

        for tlist in query(tlist_data, filters=(lambda tlist: tlist.flag == 0 and not tlist.compli)):
            turnover.belegung = turnover.belegung + tlist.belegung
            turnover.qty_fpax = turnover.qty_fpax + tlist.qty_fpax
            turnover.qty_bpax = turnover.qty_bpax + tlist.qty_bpax
            turnover.qty_opax = turnover.qty_opax + tlist.qty_opax
            turnover.cvr_food = turnover.cvr_food + tlist.cvr_food
            turnover.cvr_bev = turnover.cvr_bev + tlist.cvr_bev
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
            turnover.t_service =  to_decimal(turnover.t_service) + to_decimal(tlist.t_service)
            turnover.t_tax =  to_decimal(turnover.t_tax) + to_decimal(tlist.t_tax)
            turnover.t_debit =  to_decimal(turnover.t_debit) + to_decimal(tlist.t_debit)
            turnover.p_cash =  to_decimal(turnover.p_cash) + to_decimal(tlist.p_cash)
            turnover.p_cash1 =  to_decimal(turnover.p_cash1) + to_decimal(tlist.p_cash1)
            turnover.r_transfer =  to_decimal(turnover.r_transfer) + to_decimal(tlist.r_transfer)
            turnover.c_ledger =  to_decimal(turnover.c_ledger) + to_decimal(tlist.c_ledger)
            turnover.t_vat =  to_decimal(turnover.t_vat) + to_decimal(tlist.t_vat)
            turnover.rest_deposit =  to_decimal(turnover.rest_deposit) + to_decimal(tlist.rest_deposit)
            turnover.p_voucher =  to_decimal(turnover.p_voucher) + to_decimal(tlist.p_voucher)
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
        nt_serv =  to_decimal(turnover.t_service)
        nt_tax =  to_decimal(turnover.t_tax)
        nt_debit =  to_decimal(turnover.t_debit)
        nt_cash =  to_decimal(turnover.p_cash)
        nt_cash1 =  to_decimal(turnover.p_cash1)
        nt_trans =  to_decimal(turnover.r_transfer)
        nt_ledger =  to_decimal(turnover.c_ledger)
        nt_vat =  to_decimal(turnover.t_vat)
        nt_pvoucher =  to_decimal(turnover.p_voucher)


    def daysale1():

        nonlocal t_betrag, t_foreign, exchg_rate, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, nt_cover, tot_other, nt_other, nt_serv, nt_tax, nt_debit, nt_cash, nt_cash1, nt_trans, nt_ledger, tot_vat, nt_vat, avail_outstand_list, turnover_data, t_tot_betrag_data, t_nt_betrag_data, outstand_list_data, pay_list_data, summ_list_data, tot_betrag, nt_betrag, t_cash1, tt_other, anz_comp, val_comp, anz_coup, val_coup, total_fdisc, total_bdisc, total_odisc, t_serv, t_tax, t_debit, t_cash, t_trans, t_ledger, t_cover, fo_disc1, fo_disc2, fo_disc3, tt_betrag, multi_vat, f_endkum, b_endkum, tot_deposit, t_deposit, nt_deposit, qty, counter, artnr_data, artnr_list, t_pvoucher, tot_pvoucher, nt_pvoucher, pax_cash, pax, pax2, htparam, waehrung, h_bill, h_bill_line, artikel, h_artikel, h_journal, res_line, kellner, bill
        nonlocal disc_art1, disc_art2, disc_art3, curr_dept, all_user, shift, from_date, to_date, art_str, voucher_art, zero_vat_compli, exclude_compli, show_fbodisc, htl_dept_dptnr, incl_move_table, wig, inhouse
        nonlocal pay_listbuff, tlist


        nonlocal other_art, temp, t_tot_betrag, t_nt_betrag, bline_list, outstand_list, pay_list, pay_listbuff, turnover, summ_list, buf_art, t_artnr, tlist
        nonlocal other_art_data, temp_data, t_tot_betrag_data, t_nt_betrag_data, outstand_list_data, pay_list_data, turnover_data, summ_list_data, t_artnr_data

        curr_s:int = 0
        billnr:int = 0
        dept:int = 1
        d_name:string = ""
        usr_nr:int = 0
        d_found:bool = False
        c_found:bool = False
        vat:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        netto:Decimal = to_decimal("0.0")
        i:int = 0
        pos:int = 0
        bill_no:int = 0
        guestname:string = ""
        found:bool = False
        found_artpay:bool = False
        curr_date:date = None
        cancel_pay:bool = False
        h_bline = None
        buf_hbline = None
        b_hbline = None
        b_hartikel = None
        b_hbill = None
        H_bline =  create_buffer("H_bline",H_bill_line)
        Buf_hbline =  create_buffer("Buf_hbline",H_bill_line)
        B_hbline =  create_buffer("B_hbline",H_bill_line)
        B_hartikel =  create_buffer("B_hartikel",H_artikel)
        B_hbill =  create_buffer("B_hbill",H_bill)

        if incl_move_table:

            buf_hbline = db_session.query(Buf_hbline).filter(
                         (Buf_hbline.rechnr == h_bill.rechnr) & (Buf_hbline.departement == h_bill.departement)).first()

            if not buf_hbline:
                turnover = Turnover()
                turnover_data.append(turnover)

                turnover.rechnr = trim(to_string(h_bill.rechnr))
                turnover.belegung = h_bill.belegung
                turnover.qty_fpax = 0
                turnover.qty_bpax = 0
                turnover.betrag[0] = 0
                turnover.betrag[1] = 0
                turnover.betrag[2] = 0
                turnover.betrag[3] = 0
                turnover.betrag[4] = 0
                turnover.betrag[5] = 0
                turnover.betrag[6] = 0
                turnover.betrag[7] = 0
                turnover.betrag[8] = 0
                turnover.betrag[9] = 0
                turnover.betrag[10] = 0
                turnover.betrag[11] = 0
                turnover.betrag[12] = 0
                turnover.betrag[13] = 0
                turnover.betrag[14] = 0
                turnover.betrag[15] = 0
                turnover.betrag[16] = 0
                turnover.betrag[17] = 0
                turnover.betrag[18] = 0
                turnover.betrag[19] = 0
                turnover.other =  to_decimal("0")
                turnover.t_service =  to_decimal("0")
                turnover.t_vat =  to_decimal("0")
                turnover.t_tax =  to_decimal("0")
                turnover.t_debit =  to_decimal("0")
                turnover.rest_deposit =  to_decimal("0")
                turnover.p_cash =  to_decimal("0")
                turnover.p_curr = ""
                turnover.p_cash1 =  to_decimal("0")
                turnover.r_transfer =  to_decimal("0")
                turnover.c_ledger =  to_decimal("0")
                turnover.info = ""
                turnover.gname = h_bill.bilname
                turnover.flag = 0
                turnover.compli = False
                turnover.resnr = h_bill.resnr
                turnover.p_voucher =  to_decimal("0")
                turnover.cvr_food = 0
                turnover.cvr_bev = 0

        if shift == 0:

            h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"bill_datum": [(ge, from_date),(le, to_date)],"departement": [(eq, curr_dept)]})
        else:

            h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"bill_datum": [(ge, from_date),(le, to_date)],"departement": [(eq, curr_dept)],"betriebsnr": [(eq, shift)]})
        while None != h_bill_line:

            turnover = query(turnover_data, filters=(lambda turnover: turnover.departement == curr_dept and turnover.rechnr == to_string(h_bill.rechnr)), first=True)

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
                    pos = get_index(h_bline.bezeich, "*")

                    if pos != 0:
                        bill_no = to_int(substring(h_bline.bezeich, pos - 1, (length(h_bline.bezeich) - pos + 1)))

                    if bill_no != 0:

                        bill = get_cache (Bill, {"rechnr": [(eq, bill_no)]})

                        if bill:

                            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

                            if res_line:
                                guestname = res_line.name

                if guestname == "":
                    guestname = h_bill.bilname
                turnover = Turnover()
                turnover_data.append(turnover)

                turnover.departement = curr_dept
                turnover.tischnr = h_bill.tischnr
                turnover.belegung = h_bill.belegung
                turnover.rechnr = trim(to_string(h_bill.rechnr))
                turnover.gname = guestname
                turnover.resnr = h_bill.resnr
                tot_cover = tot_cover + h_bill.belegung

            if h_bill_line.artnr != 0:

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, curr_dept)]})

            if h_bill_line.artnr == 0:

                pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 2), first=True)

                if not pay_list:
                    pay_list = Pay_list()
                    pay_list_data.append(pay_list)

                    pay_list.flag = 2
                    pay_list.bezeich = "Room / Bill Transfer"
                pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag)
                t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)
                turnover.r_transfer =  to_decimal(turnover.r_transfer) - to_decimal(h_bill_line.betrag)
                turnover.compli = False
                i = 0

                if matches(h_bill_line.bezeich,r"*RmNo*") or matches(h_bill_line.bezeich,r"*Transfer*"):

                    if num_entries(h_bill_line.bezeich, "*") > 1:
                        billnr = to_int(entry(1, h_bill_line.bezeich, "*"))

                bill = get_cache (Bill, {"rechnr": [(eq, billnr)]})

                if bill:

                    if bill.resnr != 0 and bill.reslinnr != 0:
                        turnover.info = "Room " + bill.zinr

                    elif bill.resnr != 0 and bill.reslinnr == 0:
                        turnover.info = "Master Bill *" + to_string(billnr)
                    else:
                        turnover.info = "NonGuest Bill *" + to_string(billnr)
                turnover.t_credit =  to_decimal(turnover.t_credit) - to_decimal(h_bill_line.betrag)
                tot_trans =  to_decimal(tot_trans) - to_decimal(h_bill_line.betrag)

            elif h_artikel.artart == 11 or h_artikel.artart == 12:

                if not cancel_pay:

                    if h_artikel.artart == 11:

                        pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 6), first=True)

                        if not pay_list:
                            pay_list = Pay_list()
                            pay_list_data.append(pay_list)

                            pay_list.flag = 6
                            pay_list.compli = True
                            pay_list.bezeich = "Compliment"
                        pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag) - to_decimal(turnover.t_service) - to_decimal(turnover.t_tax)

                        if h_bill_line.betrag < 0:
                            pay_list.person = pay_list.person + h_bill.belegung

                        elif h_bill_line.betrag > 0:

                            if h_bill.belegung > 0:
                                pay_list.person = pay_list.person - h_bill.belegung
                            else:
                                pay_list.person = pay_list.person + h_bill.belegung
                        t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)
                        anz_comp = anz_comp + 1
                        val_comp =  to_decimal(val_comp) - to_decimal(h_bill_line.betrag)
                        turnover.st_comp = 1

                    elif h_artikel.artart == 12:

                        pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 7 and pay_list.bezeich == h_artikel.bezeich), first=True)

                        if not pay_list:
                            pay_list = Pay_list()
                            pay_list_data.append(pay_list)

                            pay_list.compli = True
                            pay_list.flag = 7
                            pay_list.bezeich = h_artikel.bezeich
                        pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag) - to_decimal(turnover.t_service) - to_decimal(turnover.t_tax)

                        if h_bill_line.betrag < 0:
                            pay_list.person = pay_list.person + h_bill.belegung

                        elif h_bill_line.betrag > 0:

                            if h_bill.belegung > 0:
                                pay_list.person = pay_list.person - h_bill.belegung
                            else:
                                pay_list.person = pay_list.person + h_bill.belegung
                        t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)
                        anz_coup = anz_coup + 1
                        val_coup =  to_decimal(val_coup) - to_decimal(h_bill_line.betrag)
                        turnover.st_comp = 2
                    turnover.compli = not turnover.compli
                    turnover.r_transfer =  to_decimal(turnover.r_transfer) - to_decimal(h_bill_line.betrag)

                    if h_artikel.artart == 11:
                        turnover.info = h_artikel.bezeich

                    elif h_artikel.artart == 12:
                        turnover.info = substring(h_artikel.bezeich, 0, 4)
                    tot_trans =  to_decimal(tot_trans) - to_decimal(h_bill_line.betrag)

                    if turnover.p_cash1 != 0:
                        turnover.p_cash1 =  to_decimal(turnover.p_cash1) - to_decimal(turnover.t_service) - to_decimal(turnover.t_tax)

                    if turnover.p_cash != 0:
                        turnover.p_cash =  to_decimal(turnover.p_cash) - to_decimal(turnover.t_service) - to_decimal(turnover.t_tax)

                    if turnover.r_transfer != 0:
                        turnover.r_transfer =  to_decimal(turnover.r_transfer) - to_decimal(turnover.t_service) - to_decimal(turnover.t_tax)

                    if turnover.c_ledger != 0:
                        turnover.c_ledger =  to_decimal(turnover.c_ledger) - to_decimal(turnover.t_service) - to_decimal(turnover.t_tax)

                    if turnover.p_voucher != 0:
                        turnover.p_voucher =  to_decimal(turnover.p_voucher) - to_decimal(turnover.t_service) - to_decimal(turnover.t_tax)
                    turnover.t_debit =  to_decimal(turnover.t_debit) - to_decimal(turnover.t_service) - to_decimal(turnover.t_tax)
                    turnover.t_service =  to_decimal("0")
                    turnover.t_tax =  to_decimal("0")


                cancel_pay = False
            else:

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, curr_dept)]})

                if h_artikel.artart == 0:

                    artikel = get_cache (Artikel, {"departement": [(eq, curr_dept)],"artnr": [(eq, h_artikel.artnrfront)]})
                else:

                    artikel = get_cache (Artikel, {"departement": [(eq, 0)],"artnr": [(eq, h_artikel.artnrfront)]})

                if h_artikel.artart == 0:
                    service =  to_decimal("0")
                    vat =  to_decimal("0")
                    vat2 =  to_decimal("0")

                    if h_bill_line.artnr != disc_art1 and h_bill_line.artnr != disc_art2 and h_bill_line.artnr != disc_art3:

                        if (artikel.umsatzart == 3 or artikel.umsatzart == 5):
                            turnover.qty_fpax = turnover.qty_fpax + h_bill_line.anzahl
                            turnover.cvr_food = h_bill.belegung

                        elif artikel.umsatzart == 6:
                            turnover.qty_bpax = turnover.qty_bpax + h_bill_line.anzahl
                            turnover.cvr_bev = h_bill.belegung


                        else:
                            turnover.qty_opax = turnover.qty_opax + h_bill_line.anzahl
                    service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_bill_line.bill_datum))

                    if multi_vat == False:
                        vat =  to_decimal(vat) + to_decimal(vat2)


                    netto =  to_decimal(h_bill_line.betrag) / to_decimal((1) + to_decimal(vat) + to_decimal(vat2) + to_decimal(service))
                    turnover.t_service =  to_decimal(turnover.t_service) + to_decimal(netto) * to_decimal(service)
                    turnover.t_tax =  to_decimal(turnover.t_tax) + to_decimal(netto) * to_decimal(vat)
                    turnover.t_vat =  to_decimal(turnover.t_vat) + to_decimal(netto) * to_decimal(vat2)
                    turnover.t_debit =  to_decimal(turnover.t_debit) + to_decimal(h_bill_line.betrag)
                    tot_serv =  to_decimal(tot_serv) + to_decimal(netto) * to_decimal(service)
                    tot_tax =  to_decimal(tot_tax) + to_decimal(netto) * to_decimal(vat)
                    tot_debit =  to_decimal(tot_debit) + to_decimal(h_bill_line.betrag)
                    tot_vat =  to_decimal(tot_vat) + to_decimal(netto) * to_decimal(vat2)

                    if artikel.artnr == artnr_list[0]:
                        turnover.betrag[0] = turnover.betrag[0] + netto
                        tot_betrag[0] = tot_betrag[0] + netto

                    elif artikel.artnr == artnr_list[1]:
                        turnover.betrag[1] = turnover.betrag[1] + netto
                        tot_betrag[1] = tot_betrag[1] + netto

                    elif artikel.artnr == artnr_list[2]:
                        turnover.betrag[2] = turnover.betrag[2] + netto
                        tot_betrag[2] = tot_betrag[2] + netto

                    elif artikel.artnr == artnr_list[3]:
                        turnover.betrag[3] = turnover.betrag[3] + netto
                        tot_betrag[3] = tot_betrag[3] + netto

                    elif artikel.artnr == artnr_list[4]:
                        turnover.betrag[4] = turnover.betrag[4] + netto
                        tot_betrag[4] = tot_betrag[4] + netto

                    elif artikel.artnr == artnr_list[5]:
                        turnover.betrag[5] = turnover.betrag[5] + netto
                        tot_betrag[5] = tot_betrag[5] + netto

                    elif artikel.artnr == artnr_list[6]:
                        turnover.betrag[6] = turnover.betrag[6] + netto
                        tot_betrag[6] = tot_betrag[6] + netto

                    elif artikel.artnr == artnr_list[7]:
                        turnover.betrag[7] = turnover.betrag[7] + netto
                        tot_betrag[7] = tot_betrag[7] + netto

                    elif artikel.artnr == artnr_list[8]:
                        turnover.betrag[8] = turnover.betrag[8] + netto
                        tot_betrag[8] = tot_betrag[8] + netto

                    elif artikel.artnr == artnr_list[9]:
                        turnover.betrag[9] = turnover.betrag[9] + netto
                        tot_betrag[9] = tot_betrag[9] + netto

                    elif artikel.artnr == artnr_list[10]:
                        turnover.betrag[10] = turnover.betrag[10] + netto
                        tot_betrag[10] = tot_betrag[10] + netto

                    elif artikel.artnr == artnr_list[11]:
                        turnover.betrag[11] = turnover.betrag[11] + netto
                        tot_betrag[11] = tot_betrag[11] + netto

                    elif artikel.artnr == artnr_list[12]:
                        turnover.betrag[12] = turnover.betrag[12] + netto
                        tot_betrag[12] = tot_betrag[12] + netto

                    elif artikel.artnr == artnr_list[13]:
                        turnover.betrag[13] = turnover.betrag[13] + netto
                        tot_betrag[13] = tot_betrag[13] + netto

                    elif artikel.artnr == artnr_list[14]:
                        turnover.betrag[4] = turnover.betrag[14] + netto
                        tot_betrag[14] = tot_betrag[14] + netto

                    elif artikel.artnr == artnr_list[15]:
                        turnover.betrag[15] = turnover.betrag[15] + netto
                        tot_betrag[15] = tot_betrag[15] + netto

                    elif artikel.artnr == artnr_list[16]:
                        turnover.betrag[16] = turnover.betrag[16] + netto
                        tot_betrag[16] = tot_betrag[16] + netto

                    elif artikel.artnr == artnr_list[17]:
                        turnover.betrag[17] = turnover.betrag[17] + netto
                        tot_betrag[17] = tot_betrag[17] + netto

                    elif artikel.artnr == artnr_list[18]:
                        turnover.betrag[18] = turnover.betrag[18] + netto
                        tot_betrag[18] = tot_betrag[18] + netto

                    elif artikel.artnr == artnr_list[19]:
                        turnover.betrag[19] = turnover.betrag[19] + netto
                        tot_betrag[19] = tot_betrag[19] + netto
                    else:

                        for other_art in query(other_art_data):

                            if artikel.artnr == other_art.artnr:
                                turnover.other =  to_decimal(turnover.other) + to_decimal(netto)
                                tot_other =  to_decimal(tot_other) + to_decimal(netto)

                elif h_artikel.artart == 5:

                    pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 8), first=True)

                    if not pay_list:
                        pay_list = Pay_list()
                        pay_list_data.append(pay_list)

                        pay_list.flag = 8
                        pay_list.bezeich = "Restaurant Deposit"
                    pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag)
                    pay_list.person = pay_list.person + h_bill.belegung
                    turnover.rest_deposit =  to_decimal(turnover.rest_deposit) - to_decimal(h_bill_line.betrag)
                    t_deposit =  to_decimal(t_deposit) - to_decimal(h_bill_line.betrag)
                    tot_deposit =  to_decimal(tot_deposit) - to_decimal(h_bill_line.betrag)

                elif h_artikel.artart == 6:

                    artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, 0)]})

                    pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 1 and pay_list.bezeich == artikel.bezeich), first=True)

                    if not pay_list:
                        pay_list = Pay_list()
                        pay_list_data.append(pay_list)

                        pay_list.flag = 1
                        pay_list.bezeich = artikel.bezeich

                    if artikel.pricetab:
                        pay_list.foreign =  to_decimal(pay_list.foreign) - to_decimal((h_bill_line.betrag) / to_decimal(exchg_rate))
                        t_foreign =  to_decimal(t_foreign) - to_decimal((h_bill_line.betrag) / to_decimal(exchg_rate))
                    else:
                        pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag)
                        t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)

                    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

                    if waehrung:
                        turnover.p_curr = waehrung.wabkurz

                    if artikel.pricetab:
                        turnover.p_cash1 =  to_decimal(turnover.p_cash1) - to_decimal((h_bill_line.betrag) / to_decimal(exchg_rate))
                        tot_cash1 =  to_decimal(tot_cash1) - to_decimal((h_bill_line.betrag) / to_decimal(exchg_rate))

                    elif h_artikel.artnr == voucher_art:
                        turnover.p_voucher =  to_decimal(turnover.p_voucher) - to_decimal(h_bill_line.betrag)
                        t_pvoucher =  to_decimal(t_pvoucher) - to_decimal(h_bill_line.betrag)
                        tot_pvoucher =  to_decimal(tot_pvoucher) - to_decimal(h_bill_line.betrag)
                    else:
                        turnover.p_cash =  to_decimal(turnover.p_cash) - to_decimal(h_bill_line.betrag)
                        tot_cash =  to_decimal(tot_cash) - to_decimal(h_bill_line.betrag)
                    turnover.t_credit =  to_decimal(turnover.t_credit) - to_decimal(h_bill_line.betrag)
                    turnover.info = turnover.info + h_artikel.bezeich + ";"

                elif h_artikel.artart == 7 or h_artikel.artart == 2:

                    if h_artikel.artart == 7:

                        pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 3), first=True)

                        if not pay_list:
                            pay_list = Pay_list()
                            pay_list_data.append(pay_list)

                            pay_list.flag = 3
                            pay_list.bezeich = "Credit Card"

                    elif h_artikel.artart == 2:

                        pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 5), first=True)

                        if not pay_list:
                            pay_list = Pay_list()
                            pay_list_data.append(pay_list)

                            pay_list.flag = 5
                            pay_list.bezeich = "City- & Employee Ledger"
                    pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag)
                    pay_list.person = pay_list.person + h_bill.belegung
                    t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)
                    turnover.artnr = artikel.artnr
                    turnover.c_ledger =  to_decimal(turnover.c_ledger) - to_decimal(h_bill_line.betrag)
                    turnover.t_credit =  to_decimal(turnover.t_credit) - to_decimal(h_bill_line.betrag)
                    tot_ledger =  to_decimal(tot_ledger) - to_decimal(h_bill_line.betrag)

                    if h_artikel.artart == 7:
                        turnover.info = turnover.info + to_string(h_artikel.artnr) + " " + h_artikel.bezeich + ";"

                    elif h_artikel.artart == 2:
                        turnover.info = turnover.info + to_string(h_artikel.artnr) + " " + h_artikel.bezeich + ";"

            if shift == 0:

                curr_recid = h_bill_line._recid
                h_bill_line = db_session.query(H_bill_line).filter(
                             (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum >= from_date) & (H_bill_line.bill_datum <= to_date) & (H_bill_line.departement == curr_dept) & (H_bill_line._recid > curr_recid)).first()
            else:

                curr_recid = h_bill_line._recid
                h_bill_line = db_session.query(H_bill_line).filter(
                             (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum >= from_date) & (H_bill_line.bill_datum <= to_date) & (H_bill_line.departement == curr_dept) & (H_bill_line.betriebsnr == shift) & (H_bill_line._recid > curr_recid)).first()


    def fo_discarticle():

        nonlocal t_betrag, t_foreign, exchg_rate, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, nt_cover, tot_other, nt_other, nt_serv, nt_tax, nt_debit, nt_cash, nt_cash1, nt_trans, nt_ledger, tot_vat, nt_vat, avail_outstand_list, turnover_data, t_tot_betrag_data, t_nt_betrag_data, outstand_list_data, pay_list_data, summ_list_data, tot_betrag, nt_betrag, t_cash1, tt_other, anz_comp, val_comp, anz_coup, val_coup, total_fdisc, total_bdisc, total_odisc, t_serv, t_tax, t_debit, t_cash, t_trans, t_ledger, t_cover, fo_disc1, fo_disc2, fo_disc3, tt_betrag, multi_vat, f_endkum, b_endkum, tot_deposit, t_deposit, nt_deposit, qty, counter, artnr_data, i, artnr_list, t_pvoucher, tot_pvoucher, nt_pvoucher, pax_cash, pax, pax2, htparam, waehrung, h_bill, h_bill_line, artikel, h_artikel, h_journal, res_line, kellner, bill
        nonlocal disc_art1, disc_art2, disc_art3, curr_dept, all_user, shift, from_date, to_date, art_str, voucher_art, zero_vat_compli, exclude_compli, show_fbodisc, htl_dept_dptnr, incl_move_table, wig, inhouse
        nonlocal pay_listbuff, tlist


        nonlocal other_art, temp, t_tot_betrag, t_nt_betrag, bline_list, outstand_list, pay_list, pay_listbuff, turnover, summ_list, buf_art, t_artnr, tlist
        nonlocal other_art_data, temp_data, t_tot_betrag_data, t_nt_betrag_data, outstand_list_data, pay_list_data, turnover_data, summ_list_data, t_artnr_data


        fo_disc1 = 0
        fo_disc2 = 0
        fo_disc3 = 0

        h_artikel = get_cache (H_artikel, {"artnr": [(eq, disc_art1)],"departement": [(eq, curr_dept)]})

        if h_artikel:

            artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, curr_dept)]})

            if artikel:
                fo_disc1 = artikel.artnr

        h_artikel = get_cache (H_artikel, {"artnr": [(eq, disc_art2)],"departement": [(eq, curr_dept)]})

        if h_artikel:

            artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, curr_dept)]})

            if artikel:
                fo_disc2 = artikel.artnr

        h_artikel = get_cache (H_artikel, {"artnr": [(eq, disc_art3)],"departement": [(eq, curr_dept)]})

        if h_artikel:

            artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, curr_dept)]})

            if artikel:
                fo_disc3 = artikel.artnr


    def daysale():

        nonlocal t_betrag, t_foreign, exchg_rate, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, nt_cover, tot_other, nt_other, nt_serv, nt_tax, nt_debit, nt_cash, nt_cash1, nt_trans, nt_ledger, tot_vat, nt_vat, avail_outstand_list, turnover_data, t_tot_betrag_data, t_nt_betrag_data, outstand_list_data, pay_list_data, summ_list_data, tot_betrag, nt_betrag, t_cash1, tt_other, anz_comp, val_comp, anz_coup, val_coup, total_fdisc, total_bdisc, total_odisc, t_serv, t_tax, t_debit, t_cash, t_trans, t_ledger, t_cover, fo_disc1, fo_disc2, fo_disc3, tt_betrag, multi_vat, f_endkum, b_endkum, tot_deposit, t_deposit, nt_deposit, qty, counter, artnr_data, artnr_list, t_pvoucher, tot_pvoucher, nt_pvoucher, pax_cash, pax, pax2, htparam, waehrung, h_bill, h_bill_line, artikel, h_artikel, h_journal, res_line, kellner, bill
        nonlocal disc_art1, disc_art2, disc_art3, curr_dept, all_user, shift, from_date, to_date, art_str, voucher_art, zero_vat_compli, exclude_compli, show_fbodisc, htl_dept_dptnr, incl_move_table, wig, inhouse
        nonlocal pay_listbuff, tlist


        nonlocal other_art, temp, t_tot_betrag, t_nt_betrag, bline_list, outstand_list, pay_list, pay_listbuff, turnover, summ_list, buf_art, t_artnr, tlist
        nonlocal other_art_data, temp_data, t_tot_betrag_data, t_nt_betrag_data, outstand_list_data, pay_list_data, turnover_data, summ_list_data, t_artnr_data

        curr_s:int = 0
        billnr:int = 0
        dept:int = 1
        d_name:string = ""
        usr_nr:int = 0
        d_found:bool = False
        c_found:bool = False
        vat:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        netto:Decimal = to_decimal("0.0")
        i:int = 0
        found:bool = False
        compli:bool = False
        guestname:string = ""
        bill_no:int = 0
        pos:int = 0
        curr_date:date = None
        cancel_pay:bool = False
        kellner1 = None
        h_bline = None
        buf_hbline = None
        b_hbline = None
        b_hbill = None
        Kellner1 =  create_buffer("Kellner1",Kellner)
        H_bline =  create_buffer("H_bline",H_bill_line)
        Buf_hbline =  create_buffer("Buf_hbline",H_bill_line)
        B_hbline =  create_buffer("B_hbline",H_bill_line)
        B_hbill =  create_buffer("B_hbill",H_bill)

        if incl_move_table:

            buf_hbline = db_session.query(Buf_hbline).filter(
                         (Buf_hbline.rechnr == h_bill.rechnr) & (Buf_hbline.departement == h_bill.departement)).first()

            if not buf_hbline:
                turnover = Turnover()
                turnover_data.append(turnover)

                turnover.rechnr = trim(to_string(h_bill.rechnr))
                turnover.belegung = h_bill.belegung
                turnover.qty_fpax = 0
                turnover.qty_bpax = 0
                turnover.betrag[0] = 0
                turnover.betrag[1] = 0
                turnover.betrag[2] = 0
                turnover.betrag[3] = 0
                turnover.betrag[4] = 0
                turnover.betrag[5] = 0
                turnover.betrag[6] = 0
                turnover.betrag[7] = 0
                turnover.betrag[8] = 0
                turnover.betrag[9] = 0
                turnover.betrag[10] = 0
                turnover.betrag[11] = 0
                turnover.betrag[12] = 0
                turnover.betrag[13] = 0
                turnover.betrag[14] = 0
                turnover.betrag[15] = 0
                turnover.betrag[16] = 0
                turnover.betrag[17] = 0
                turnover.betrag[18] = 0
                turnover.betrag[19] = 0
                turnover.other =  to_decimal("0")
                turnover.t_service =  to_decimal("0")
                turnover.t_vat =  to_decimal("0")
                turnover.t_tax =  to_decimal("0")
                turnover.t_debit =  to_decimal("0")
                turnover.rest_deposit =  to_decimal("0")
                turnover.p_cash =  to_decimal("0")
                turnover.p_curr = ""
                turnover.p_cash1 =  to_decimal("0")
                turnover.r_transfer =  to_decimal("0")
                turnover.c_ledger =  to_decimal("0")
                turnover.info = ""
                turnover.gname = h_bill.bilname
                turnover.flag = 0
                turnover.compli = False
                turnover.resnr = h_bill.resnr
                turnover.p_voucher =  to_decimal("0")
                turnover.cvr_food = 0
                turnover.cvr_bev = 0

        if shift == 0:

            h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"bill_datum": [(ge, from_date),(le, to_date)],"departement": [(eq, curr_dept)]})
        else:

            h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"bill_datum": [(ge, from_date),(le, to_date)],"departement": [(eq, curr_dept)],"betriebsnr": [(eq, shift)]})
        while None != h_bill_line:

            turnover = query(turnover_data, filters=(lambda turnover: turnover.departement == curr_dept and turnover.kellner_nr == kellner.kellner_nr and turnover.rechnr == to_string(h_bill.rechnr)), first=True)

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
                    pos = get_index(h_bline.bezeich, "*")

                    if pos != 0:
                        bill_no = to_int(substring(h_bline.bezeich, pos - 1, (length(h_bline.bezeich) - pos + 1)))

                    if bill_no != 0:

                        bill = get_cache (Bill, {"rechnr": [(eq, bill_no)]})

                        if bill:

                            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

                            if res_line:
                                guestname = res_line.name

                if guestname == "":
                    guestname = h_bill.bilname
                turnover = Turnover()
                turnover_data.append(turnover)

                turnover.departement = kellner.departement
                turnover.kellner_nr = kellner.kellner_nr
                turnover.name = kellner.kellnername
                turnover.tischnr = h_bill.tischnr
                turnover.belegung = h_bill.belegung
                turnover.rechnr = trim(to_string(h_bill.rechnr))
                turnover.gname = guestname
                turnover.resnr = h_bill.resnr
                tot_cover = tot_cover + h_bill.belegung
                t_cover = t_cover + h_bill.belegung

            if h_bill_line.artnr == 0:
                turnover.r_transfer =  to_decimal(turnover.r_transfer) - to_decimal(h_bill_line.betrag)
                turnover.compli = False

                pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 2), first=True)

                if not pay_list:
                    pay_list = Pay_list()
                    pay_list_data.append(pay_list)

                    pay_list.flag = 2
                    pay_list.bezeich = "Room / Bill Transfer"
                pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag)
                t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)
                i = 0

                if matches(h_bill_line.bezeich,r"*RmNo*") or matches(h_bill_line.bezeich,r"*Transfer*"):

                    if num_entries(h_bill_line.bezeich, "*") > 1:
                        billnr = to_int(entry(1, h_bill_line.bezeich, "*"))

                bill = get_cache (Bill, {"rechnr": [(eq, billnr)]})

                if bill:

                    if bill.resnr != 0 and bill.reslinnr != 0:
                        turnover.info = "Room " + bill.zinr

                    elif bill.resnr != 0 and bill.reslinnr == 0:
                        turnover.info = "Master Bill *" + to_string(billnr)
                    else:
                        turnover.info = "NonGuest Bill *" + to_string(billnr)
                turnover.t_credit =  to_decimal(turnover.t_credit) - to_decimal(h_bill_line.betrag)
                t_trans =  to_decimal(t_trans) - to_decimal(h_bill_line.betrag)
                tot_trans =  to_decimal(tot_trans) - to_decimal(h_bill_line.betrag)
            else:

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, curr_dept)]})

                if h_artikel.artart == 11 or h_artikel.artart == 12:

                    if not cancel_pay:

                        if h_artikel.artart == 11:

                            pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 6), first=True)

                            if not pay_list:
                                pay_list = Pay_list()
                                pay_list_data.append(pay_list)

                                pay_list.flag = 6
                                pay_list.compli = True
                                pay_list.bezeich = "Compliment"
                            pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag) - to_decimal(turnover.t_service) - to_decimal(turnover.t_tax)

                            if h_bill_line.betrag < 0:
                                pay_list.person = pay_list.person + h_bill.belegung

                            elif h_bill_line.betrag > 0:

                                if h_bill.belegung > 0:
                                    pay_list.person = pay_list.person - h_bill.belegung
                                else:
                                    pay_list.person = pay_list.person + h_bill.belegung
                            t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)
                            anz_comp = anz_comp + 1
                            val_comp =  to_decimal(val_comp) - to_decimal(h_bill_line.betrag)
                            turnover.st_comp = 1

                        elif h_artikel.artart == 12:

                            pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 7 and pay_list.bezeich == h_artikel.bezeich), first=True)

                            if not pay_list:
                                pay_list = Pay_list()
                                pay_list_data.append(pay_list)

                                pay_list.flag = 7
                                pay_list.compli = True
                                pay_list.bezeich = h_artikel.bezeich
                            pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag) - to_decimal(turnover.t_service) - to_decimal(turnover.t_tax)

                            if h_bill_line.betrag < 0:
                                pay_list.person = pay_list.person + h_bill.belegung

                            elif h_bill_line.betrag > 0:

                                if h_bill.belegung > 0:
                                    pay_list.person = pay_list.person - h_bill.belegung
                                else:
                                    pay_list.person = pay_list.person + h_bill.belegung
                            t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)
                            anz_coup = anz_coup + 1
                            val_coup =  to_decimal(val_coup) - to_decimal(h_bill_line.betrag)
                            turnover.st_comp = 2
                        turnover.compli = not turnover.compli
                        turnover.r_transfer =  to_decimal(turnover.r_transfer) - to_decimal(h_bill_line.betrag)

                        if h_artikel.artart == 11:
                            turnover.info = h_artikel.bezeich

                        elif h_artikel.artart == 12:
                            turnover.info = substring(h_artikel.bezeich, 0, 4)
                        tot_trans =  to_decimal(tot_trans) - to_decimal(h_bill_line.betrag)

                        if turnover.p_cash1 != 0:
                            turnover.p_cash1 =  to_decimal(turnover.p_cash1) - to_decimal(turnover.t_service) - to_decimal(turnover.t_tax)

                        if turnover.p_cash != 0:
                            turnover.p_cash =  to_decimal(turnover.p_cash) - to_decimal(turnover.t_service) - to_decimal(turnover.t_tax)

                        if turnover.r_transfer != 0:
                            turnover.r_transfer =  to_decimal(turnover.r_transfer) - to_decimal(turnover.t_service) - to_decimal(turnover.t_tax)

                        if turnover.c_ledger != 0:
                            turnover.c_ledger =  to_decimal(turnover.c_ledger) - to_decimal(turnover.t_service) - to_decimal(turnover.t_tax)

                        if turnover.p_voucher != 0:
                            turnover.p_voucher =  to_decimal(turnover.p_voucher) - to_decimal(turnover.t_service) - to_decimal(turnover.t_tax)
                        turnover.t_debit =  to_decimal(turnover.t_debit) - to_decimal(turnover.t_service) - to_decimal(turnover.t_tax)
                        turnover.t_service =  to_decimal("0")
                        turnover.t_tax =  to_decimal("0")


                    cancel_pay = False

                elif h_artikel.artart == 0:

                    artikel = get_cache (Artikel, {"departement": [(eq, curr_dept)],"artnr": [(eq, h_artikel.artnrfront)]})

                    if artikel:
                        service =  to_decimal("0")
                    vat =  to_decimal("0")
                    vat2 =  to_decimal("0")

                    if h_bill_line.artnr != disc_art1 and h_bill_line.artnr != disc_art2 and h_bill_line.artnr != disc_art3:

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
                    turnover.t_service =  to_decimal(turnover.t_service) + to_decimal(netto) * to_decimal(service)
                    turnover.t_tax =  to_decimal(turnover.t_tax) + to_decimal(netto) * to_decimal(vat)
                    turnover.t_vat =  to_decimal(turnover.t_vat) + to_decimal(netto) * to_decimal(vat2)
                    turnover.t_debit =  to_decimal(turnover.t_debit) + to_decimal(h_bill_line.betrag)
                    tot_serv =  to_decimal(tot_serv) + to_decimal(netto) * to_decimal(service)
                    tot_tax =  to_decimal(tot_tax) + to_decimal(netto) * to_decimal(vat)
                    tot_vat =  to_decimal(tot_vat) + to_decimal(netto) * to_decimal(vat2)
                    tot_debit =  to_decimal(tot_debit) + to_decimal(h_bill_line.betrag)

                    if artikel.artnr == artnr_list[0]:
                        turnover.betrag[0] = turnover.betrag[0] + netto
                        tt_betrag[0] = tt_betrag[0] + netto
                        tot_betrag[0] = tot_betrag[0] + netto

                    elif artikel.artnr == artnr_list[1]:
                        turnover.betrag[1] = turnover.betrag[1] + netto
                        tt_betrag[1] = tt_betrag[1] + netto
                        tot_betrag[1] = tot_betrag[1] + netto

                    elif artikel.artnr == artnr_list[2]:
                        turnover.betrag[2] = turnover.betrag[2] + netto
                        tt_betrag[2] = tt_betrag[2] + netto
                        tot_betrag[2] = tot_betrag[2] + netto

                    elif artikel.artnr == artnr_list[3]:
                        turnover.betrag[3] = turnover.betrag[3] + netto
                        tt_betrag[3] = tt_betrag[3] + netto
                        tot_betrag[3] = tot_betrag[3] + netto

                    elif artikel.artnr == artnr_list[4]:
                        turnover.betrag[4] = turnover.betrag[4] + netto
                        tt_betrag[4] = tt_betrag[4] + netto
                        tot_betrag[4] = tot_betrag[4] + netto

                    elif artikel.artnr == artnr_list[5]:
                        turnover.betrag[5] = turnover.betrag[5] + netto
                        tt_betrag[5] = tt_betrag[5] + netto
                        tot_betrag[5] = tot_betrag[5] + netto

                    elif artikel.artnr == artnr_list[6]:
                        turnover.betrag[6] = turnover.betrag[6] + netto
                        tt_betrag[6] = tt_betrag[6] + netto
                        tot_betrag[6] = tot_betrag[6] + netto

                    elif artikel.artnr == artnr_list[7]:
                        turnover.betrag[7] = turnover.betrag[7] + netto
                        tt_betrag[7] = tt_betrag[7] + netto
                        tot_betrag[7] = tot_betrag[7] + netto

                    elif artikel.artnr == artnr_list[8]:
                        turnover.betrag[8] = turnover.betrag[8] + netto
                        tt_betrag[8] = tt_betrag[8] + netto
                        tot_betrag[8] = tot_betrag[8] + netto

                    elif artikel.artnr == artnr_list[9]:
                        turnover.betrag[9] = turnover.betrag[9] + netto
                        tt_betrag[9] = tt_betrag[9] + netto
                        tot_betrag[9] = tot_betrag[9] + netto

                    elif artikel.artnr == artnr_list[10]:
                        turnover.betrag[10] = turnover.betrag[10] + netto
                        tt_betrag[10] = tt_betrag[10] + netto
                        tot_betrag[10] = tot_betrag[10] + netto

                    elif artikel.artnr == artnr_list[11]:
                        turnover.betrag[11] = turnover.betrag[11] + netto
                        tt_betrag[11] = tt_betrag[11] + netto
                        tot_betrag[11] = tot_betrag[11] + netto

                    elif artikel.artnr == artnr_list[12]:
                        turnover.betrag[12] = turnover.betrag[12] + netto
                        tt_betrag[12] = tt_betrag[12] + netto
                        tot_betrag[12] = tot_betrag[12] + netto

                    elif artikel.artnr == artnr_list[13]:
                        turnover.betrag[13] = turnover.betrag[13] + netto
                        tt_betrag[13] = tt_betrag[13] + netto
                        tot_betrag[13] = tot_betrag[13] + netto

                    elif artikel.artnr == artnr_list[14]:
                        turnover.betrag[14] = turnover.betrag[14] + netto
                        tt_betrag[14] = tt_betrag[14] + netto
                        tot_betrag[14] = tot_betrag[14] + netto

                    elif artikel.artnr == artnr_list[15]:
                        turnover.betrag[15] = turnover.betrag[15] + netto
                        tt_betrag[15] = tt_betrag[15] + netto
                        tot_betrag[15] = tot_betrag[15] + netto

                    elif artikel.artnr == artnr_list[16]:
                        turnover.betrag[16] = turnover.betrag[16] + netto
                        tt_betrag[16] = tt_betrag[16] + netto
                        tot_betrag[16] = tot_betrag[16] + netto

                    elif artikel.artnr == artnr_list[17]:
                        turnover.betrag[17] = turnover.betrag[17] + netto
                        tt_betrag[17] = tt_betrag[17] + netto
                        tot_betrag[17] = tot_betrag[17] + netto

                    elif artikel.artnr == artnr_list[18]:
                        turnover.betrag[18] = turnover.betrag[18] + netto
                        tt_betrag[18] = tt_betrag[18] + netto
                        tot_betrag[18] = tot_betrag[18] + netto

                    elif artikel.artnr == artnr_list[19]:
                        turnover.betrag[19] = turnover.betrag[19] + netto
                        tt_betrag[19] = tt_betrag[19] + netto
                        tot_betrag[19] = tot_betrag[19] + netto
                    else:

                        for other_art in query(other_art_data):

                            if artikel.artnr == other_art.artnr:
                                turnover.other =  to_decimal(turnover.other) + to_decimal(netto)
                                tt_other =  to_decimal(tt_other) + to_decimal(netto)


                            tot_other =  to_decimal(tot_other) + to_decimal(netto)
                else:

                    artikel = get_cache (Artikel, {"departement": [(eq, 0)],"artnr": [(eq, h_artikel.artnrfront)]})

                if h_artikel.artart == 6:

                    artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, 0)]})

                    pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 1 and pay_list.bezeich == artikel.bezeich), first=True)

                    if not pay_list:
                        pay_list = Pay_list()
                        pay_list_data.append(pay_list)

                        pay_list.flag = 1
                        pay_list.bezeich = artikel.bezeich

                    if artikel.pricetab:
                        pay_list.foreign =  to_decimal(pay_list.foreign) - to_decimal((h_bill_line.betrag) / to_decimal(exchg_rate))
                        t_foreign =  to_decimal(t_foreign) - to_decimal((h_bill_line.betrag) / to_decimal(exchg_rate))
                    else:
                        pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag)
                        t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)

                    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

                    if waehrung:
                        turnover.p_curr = waehrung.wabkurz

                    if artikel.pricetab:
                        turnover.p_cash1 =  to_decimal(turnover.p_cash1) - to_decimal((h_bill_line.betrag) / to_decimal(exchg_rate))
                        t_cash1 =  to_decimal(t_cash1) - to_decimal((h_bill_line.betrag) / to_decimal(exchg_rate))

                    elif h_artikel.artnr == voucher_art:
                        turnover.p_voucher =  to_decimal(turnover.p_voucher) - to_decimal(h_bill_line.betrag)
                        t_pvoucher =  to_decimal(t_pvoucher) - to_decimal(h_bill_line.betrag)
                        tot_pvoucher =  to_decimal(tot_pvoucher) - to_decimal(h_bill_line.betrag)
                    else:
                        turnover.p_cash =  to_decimal(turnover.p_cash) - to_decimal(h_bill_line.betrag)
                        t_cash =  to_decimal(t_cash) - to_decimal(h_bill_line.betrag)
                    turnover.t_credit =  to_decimal(turnover.t_credit) - to_decimal(h_bill_line.betrag)
                    turnover.info = turnover.info + h_artikel.bezeich + ";"

                elif h_artikel.artart == 5:

                    pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 8), first=True)

                    if not pay_list:
                        pay_list = Pay_list()
                        pay_list_data.append(pay_list)

                        pay_list.flag = 8
                        pay_list.bezeich = "Restaurant Deposit"
                    pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag)
                    pay_list.person = pay_list.person + h_bill.belegung
                    turnover.rest_deposit =  to_decimal(turnover.rest_deposit) - to_decimal(h_bill_line.betrag)
                    t_deposit =  to_decimal(t_deposit) - to_decimal(h_bill_line.betrag)
                    tot_deposit =  to_decimal(tot_deposit) - to_decimal(h_bill_line.betrag)

                elif h_artikel.artart == 7 or h_artikel.artart == 2:

                    if h_artikel.artart == 7:

                        pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 3), first=True)

                        if not pay_list:
                            pay_list = Pay_list()
                            pay_list_data.append(pay_list)

                            pay_list.flag = 3
                            pay_list.bezeich = "Credit Card"

                    elif h_artikel.artart == 2:

                        pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 5), first=True)

                        if not pay_list:
                            pay_list = Pay_list()
                            pay_list_data.append(pay_list)

                            pay_list.flag = 5
                            pay_list.bezeich = "City- & Employee Ledger"
                    pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag)
                    pay_list.person = pay_list.person + h_bill.belegung
                    t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)
                    turnover.artnr = artikel.artnr
                    turnover.c_ledger =  to_decimal(turnover.c_ledger) - to_decimal(h_bill_line.betrag)
                    turnover.t_credit =  to_decimal(turnover.t_credit) - to_decimal(h_bill_line.betrag)
                    t_ledger =  to_decimal(t_ledger) - to_decimal(h_bill_line.betrag)
                    tot_ledger =  to_decimal(tot_ledger) - to_decimal(h_bill_line.betrag)

                    if h_artikel.artart == 7:
                        turnover.info = turnover.info + to_string(h_artikel.artnr) + " " + h_artikel.bezeich + ";"

                    elif h_artikel.artart == 2:
                        turnover.info = turnover.info + to_string(h_artikel.artnr) + " " + h_artikel.bezeich + ";"

            if shift == 0:

                curr_recid = h_bill_line._recid
                h_bill_line = db_session.query(H_bill_line).filter(
                             (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum >= from_date) & (H_bill_line.bill_datum <= to_date) & (H_bill_line.departement == curr_dept) & (H_bill_line._recid > curr_recid)).first()
            else:

                curr_recid = h_bill_line._recid
                h_bill_line = db_session.query(H_bill_line).filter(
                             (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum >= from_date) & (H_bill_line.bill_datum <= to_date) & (H_bill_line.departement == curr_dept) & (H_bill_line.betriebsnr == shift) & (H_bill_line._recid > curr_recid)).first()


    def cal_fbodisc(billno:int):

        nonlocal t_betrag, t_foreign, exchg_rate, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, nt_cover, tot_other, nt_other, nt_serv, nt_tax, nt_debit, nt_cash, nt_cash1, nt_trans, nt_ledger, tot_vat, nt_vat, avail_outstand_list, turnover_data, t_tot_betrag_data, t_nt_betrag_data, outstand_list_data, pay_list_data, summ_list_data, tot_betrag, nt_betrag, t_cash1, tt_other, anz_comp, val_comp, anz_coup, val_coup, total_fdisc, total_bdisc, total_odisc, t_serv, t_tax, t_debit, t_cash, t_trans, t_ledger, t_cover, fo_disc1, fo_disc2, fo_disc3, tt_betrag, multi_vat, f_endkum, b_endkum, tot_deposit, t_deposit, nt_deposit, qty, counter, artnr_data, artnr_list, t_pvoucher, tot_pvoucher, nt_pvoucher, pax_cash, pax, pax2, htparam, waehrung, h_bill, h_bill_line, artikel, h_artikel, h_journal, res_line, kellner, bill
        nonlocal disc_art1, disc_art2, disc_art3, curr_dept, all_user, shift, from_date, to_date, art_str, voucher_art, zero_vat_compli, exclude_compli, show_fbodisc, htl_dept_dptnr, incl_move_table, wig, inhouse
        nonlocal pay_listbuff, tlist


        nonlocal other_art, temp, t_tot_betrag, t_nt_betrag, bline_list, outstand_list, pay_list, pay_listbuff, turnover, summ_list, buf_art, t_artnr, tlist
        nonlocal other_art_data, temp_data, t_tot_betrag_data, t_nt_betrag_data, outstand_list_data, pay_list_data, turnover_data, summ_list_data, t_artnr_data

        vat:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        netto:Decimal = to_decimal("0.0")
        i:int = 0
        i_artnr:int = 0
        total_fdisc =  to_decimal("0")
        total_bdisc =  to_decimal("0")
        total_odisc =  to_decimal("0")

        if not show_fbodisc:

            return

        h_journal_obj_list = {}
        h_journal = H_journal()
        h_artikel = H_artikel()
        for h_journal.rechnr, h_journal.departement, h_journal.bill_datum, h_journal.betrag, h_journal.artnr, h_journal._recid, h_artikel.artart, h_artikel.bezeich, h_artikel.artnrfront, h_artikel.artnr, h_artikel._recid in db_session.query(H_journal.rechnr, H_journal.departement, H_journal.bill_datum, H_journal.betrag, H_journal.artnr, H_journal._recid, H_artikel.artart, H_artikel.bezeich, H_artikel.artnrfront, H_artikel.artnr, H_artikel._recid).join(H_artikel,(H_artikel.artnr == H_journal.artnr) & (H_artikel.departement == H_journal.departement) & (H_artikel.artart == 0)).filter(
                 (H_journal.bill_datum >= from_date) & (H_journal.bill_datum <= to_date) & (H_journal.departement == curr_dept) & (H_journal.rechnr == billno) & (H_journal.betrag != 0)).order_by(H_journal._recid).all():
            if h_journal_obj_list.get(h_journal._recid):
                continue
            else:
                h_journal_obj_list[h_journal._recid] = True


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


    htparam = get_cache (Htparam, {"paramnr": [(eq, 271)]})
    multi_vat = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    else:
        exchg_rate =  to_decimal("1")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})

    if htparam.finteger > 0:
        f_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})

    if htparam.finteger > 0:
        b_endkum = htparam.finteger
    t_artnr_data.clear()
    temp_data.clear()
    for i in range(1,num_entries(art_str, ",")  + 1) :

        if i > 21:
            pass
        else:
            artnr_data[i - 1] = to_int(entry(i - 1, art_str, ","))

            if artnr_data[i - 1] != 0:
                qty = qty + 1
    for i in range(1,qty + 1) :

        buf_art = query(buf_art_data, filters=(lambda buf_art: buf_art.artnr == artnr_data[i - 1] and buf_art.departement == curr_dept), first=True)

        if buf_art:
            counter = counter + 1
            t_artnr = T_artnr()
            t_artnr_data.append(t_artnr)

            t_artnr.nr = counter
            t_artnr.artnr = buf_art.artnr

    for t_artnr in query(t_artnr_data, sort_by=[("nr",False)]):
        artnr_list[t_artnr.nr - 1] = t_artnr.artnr

    if not all_user:
        daysale_list()
    else:
        daysale_list1()

    for turnover in query(turnover_data):

        h_bill = get_cache (H_bill, {"rechnr": [(eq, to_int(turnover.rechnr))],"departement": [(eq, curr_dept)]})

        if h_bill and turnover.p_cash != 0:
            pax_cash = pax_cash + turnover.belegung

        if h_bill:
            turnover.belegung = h_bill.belegung

    for pay_list in query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 1 and pay_list.foreign != 0)):
        pax2 = pax2 + 1

    turnover = query(turnover_data, first=True)

    if turnover:

        pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 1 and pay_list.saldo != 0), first=True)

        if pay_list:
            pay_list.person = pax_cash

        pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 1 and pay_list.foreign != 0), first=True)

        if pay_list:
            pay_list.person = pax2

        for pay_list in query(pay_list_data, filters=(lambda pay_list: pay_list.flag != 2)):
            pax = pax + pay_list.person

        pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 2), first=True)

        if pay_list:

            for tlist in query(tlist_data, filters=(lambda tlist: not tlist.compli and tlist.r_transfer != 0 and tlist.rechnr.lower()  != ("G-TOTAL").lower()  and tlist.rechnr.lower()  != ("R-TOTAL").lower())):
                pay_list.person = pay_list.person + tlist.belegung

        if outstand_list:
            avail_outstand_list = True
        t_tot_betrag = T_tot_betrag()
        t_tot_betrag_data.append(t_tot_betrag)

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
        t_nt_betrag_data.append(t_nt_betrag)

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