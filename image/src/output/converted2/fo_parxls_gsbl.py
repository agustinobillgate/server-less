#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.htpint import htpint
from models import Segmentstat, Arrangement, Res_line, Bill_line, Zimmer, Zinrstat, Zkstat, H_umsatz, Segment, Genstat, Uebertrag, Artikel, H_artikel, Wgrpdep, Umsatz, Budget, Htparam, Exrate, H_cost, H_journal, Reservation, H_bill_line, H_bill, Bill, Queasy, Gl_acct, Waehrung, L_lager, L_artikel, L_op, H_compli, Fbstat, Sources, Paramtext, Parameters

w1_list, W1 = create_model("W1", {"nr":int, "varname":string, "main_code":int, "s_artnr":string, "artnr":int, "dept":int, "grpflag":int, "done":bool, "bezeich":string, "int_flag":bool, "tday":Decimal, "tday_serv":Decimal, "tday_tax":Decimal, "mtd_serv":Decimal, "mtd_tax":Decimal, "ytd_serv":Decimal, "ytd_tax":Decimal, "yesterday":Decimal, "saldo":Decimal, "lastmon":Decimal, "pmtd_serv":Decimal, "pmtd_tax":Decimal, "lmtd_serv":Decimal, "lmtd_tax":Decimal, "lastyr":Decimal, "lytoday":Decimal, "ytd_saldo":Decimal, "lytd_saldo":Decimal, "year_saldo":[Decimal,12], "mon_saldo":[Decimal,31], "mon_budget":[Decimal,31], "mon_lmtd":[Decimal,31], "tbudget":Decimal, "budget":Decimal, "lm_budget":Decimal, "lm_today":Decimal, "lm_today_serv":Decimal, "lm_today_tax":Decimal, "lm_mtd":Decimal, "lm_ytd":Decimal, "ly_budget":Decimal, "ny_budget":Decimal, "ytd_budget":Decimal, "nytd_budget":Decimal, "nmtd_budget":Decimal, "lytd_budget":Decimal, "lytd_serv":Decimal, "lytd_tax":Decimal, "lytoday_serv":Decimal, "lytoday_tax":Decimal, "month_budget":Decimal, "year_budget":Decimal, "tischnr":int, "mon_serv":[Decimal,31], "mon_tax":[Decimal,31]})
w2_list, W2 = create_model("W2", {"val_sign":int, "nr1":int, "nr2":int}, {"val_sign": 1})

def fo_parxls_gsbl(pvilanguage:int, ytd_flag:bool, jan1:date, ljan1:date, lfrom_date:date, lto_date:date, pfrom_date:date, pto_date:date, from_date:date, to_date:date, start_date:date, lytd_flag:bool, lmtd_flag:bool, pmtd_flag:bool, lytoday_flag:bool, lytoday:date, foreign_flag:bool, budget_flag:bool, foreign_nr:int, price_decimal:int, briefnr:int, link:string, budget_all:bool, w1_list:[W1], w2_list:[W2]):

    prepare_cache ([Segmentstat, Arrangement, Res_line, Zkstat, H_umsatz, Segment, Genstat, Uebertrag, Artikel, H_artikel, Htparam, Exrate, H_cost, H_journal, Reservation, H_bill_line, H_bill, Bill, Queasy, Waehrung, L_op, H_compli, Fbstat, Sources, Paramtext, Parameters])

    msg_str = ""
    error_nr = 0
    lfr_date:date = None
    exrate_betrag:Decimal = to_decimal("0.0")
    frate:Decimal = 1
    prog_error:bool = False
    ch:string = ""
    month_str:List[string] = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "FalseVEMBER", "DECEMBER"]
    lvcarea:string = "fo-parxls"
    prev_param:string = ""
    k:int = 0
    j:int = 0
    curr_row:int = 0
    curr_col:int = 0
    htl_no:string = ""
    cell_value:string = ""
    chcol:List[string] = ["A", "b", "C", "D", "E", "F", "G", "H", "i", "j", "k", "L", "M", "n", "O", "P", "Q", "R", "s", "T", "U", "V", "W", "X", "Y", "z"]
    dayname:List[string] = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    segmentstat = arrangement = res_line = bill_line = zimmer = zinrstat = zkstat = h_umsatz = segment = genstat = uebertrag = artikel = h_artikel = wgrpdep = umsatz = budget = htparam = exrate = h_cost = h_journal = reservation = h_bill_line = h_bill = bill = queasy = gl_acct = waehrung = l_lager = l_artikel = l_op = h_compli = fbstat = sources = paramtext = parameters = None

    w1 = shift_list = w2 = tmp_room = t_list = t_rechnr = temp_rechnr = s_list = fbstat_dept = stream_list = segmbuff = curr_child = ww1 = ww2 = wdu = w11 = w12 = w13 = w11 = w12 = w13 = w11 = tbuff = w1a = w11 = w12 = w11 = w12 = w11 = w12 = w11 = w753 = w754 = w755 = w11 = w11 = w11 = w11 = w12 = w13 = wlos = wspc = btemp_rechnr = wf1 = wf2 = wf3 = wf4 = wb1 = wb2 = wb3 = wb4 = wo1 = wo2 = wo3 = wo4 = w11 = w11 = w12 = w13 = parent = child = curr_child = curr_w2 = None

    shift_list_list, Shift_list = create_model("Shift_list", {"shift":int, "ftime":int, "ttime":int})
    tmp_room_list, Tmp_room = create_model("Tmp_room", {"gastnr":int, "zinr":string, "flag":int})
    t_list_list, T_list = create_model("T_list", {"dept":int, "datum":date, "shift":int, "pax_food":int, "pax_bev":int})
    t_rechnr_list, T_rechnr = create_model("T_rechnr", {"datum":date, "dept":int, "rechnr":int, "shift":int, "found_food":bool, "found_bev":bool})
    temp_rechnr_list, Temp_rechnr = create_model("Temp_rechnr", {"datum":date, "dept":int, "rechnr":int, "shift":int, "belegung":int, "artnrfront":int, "compli_flag":bool, "tischnr":int, "betrag":Decimal, "artnr":int, "artart":int, "resnr":int, "reslinnr":int, "f_pax":int, "b_pax":int, "f_qty":int, "b_qty":int})
    s_list_list, S_list = create_model("S_list", {"datum":date, "reihenfolge":int, "lager_nr":int, "fibukonto":string, "bezeich":string, "flag":int, "betrag":Decimal, "t_betrag":Decimal, "betrag1":Decimal, "t_betrag1":Decimal}, {"reihenfolge": 1, "flag": 2})
    fbstat_dept_list, Fbstat_dept = create_model("Fbstat_dept", {"done":bool, "dept":int})
    stream_list_list, Stream_list = create_model("Stream_list", {"crow":int, "ccol":int, "cval":string})

    Segmbuff = create_buffer("Segmbuff",Segmentstat)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        return {"msg_str": msg_str, "error_nr": error_nr}

    def fill_value():

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        mm:int = 0
        i:int = 0
        k:int = 0
        n:int = 0
        val_sign:int = 0
        num__row:int = 0
        z:int = 0
        n__bar:int = 0
        n__pct:int = 50
        done_pax_shift:bool = False
        done_fbstat:bool = False
        done_los:bool = False
        done_adddayuse:bool = False
        Curr_child = W1
        curr_child_list = w1_list
        Ww1 = W1
        ww1_list = w1_list
        Ww2 = W1
        ww2_list = w1_list
        fbstat_dept_list.clear()

        for ww1 in query(ww1_list, filters=(lambda ww1: ww1.grpflag == 0)):
            num__row = num__row + 1

        for ww1 in query(ww1_list, filters=(lambda ww1: ww1.grpflag == 0)):

            ww2 = query(ww2_list, filters=(lambda ww2: ww2.varname == ww1.varname and ww1._recid != ww2._recid), first=True)

            if ww2:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Duplicate name found : ", lvcarea, "") + ww2.varname
                error_nr = -1

                return
        z = 0

        for ww1 in query(ww1_list, filters=(lambda ww1: ww1.grpflag == 0), sort_by=[("main_code",True)]):
            z = z + 1
            n__bar = to_int(z * n__pct / num__row)

            ww2 = query(ww2_list, filters=(lambda ww2: ww2.varname == ww1.varname and ww1._recid != ww2._recid), first=True)

            if ww2:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Duplicate name found : ", lvcarea, "") + ww2.varname
                error_nr = -1

                return

            if ww1.main_code == 288:
                fill_totroom(ww1._recid)

            elif ww1.main_code == 805:
                fill_rmavail(ww1._recid)

            elif ww1.main_code == 122:
                fill_rmstat(ww1._recid, "ooo")

            elif ww1.main_code == 752:
                fill_rmstat(ww1._recid, "oos")

            elif ww1.main_code == 129:
                fill_rmstat(ww1._recid, "vacant")

            elif ww1.main_code == 1019:
                fill_rmstat(ww1._recid, "dayuse")

            elif ww1.main_code == 192:
                fill_pax_cover_shift1(ww1._recid)

            elif ww1.main_code == 197:
                fill_pax_cover_shift1(ww1._recid)

            elif ww1.main_code == 552:
                fill_pax_cover_shift1(ww1._recid)

            elif ww1.main_code == 1921:
                fill_cover_shift(ww1._recid)

            elif ww1.main_code == 1922:
                fill_cover_shift(ww1._recid)

            elif ww1.main_code == 1923:
                fill_cover_shift(ww1._recid)

            elif ww1.main_code == 1924:
                fill_cover_shift(ww1._recid)

            elif ww1.main_code == 1971:
                fill_cover_shift(ww1._recid)

            elif ww1.main_code == 1972:
                fill_cover_shift(ww1._recid)

            elif ww1.main_code == 1973:
                fill_cover_shift(ww1._recid)

            elif ww1.main_code == 1974:
                fill_cover_shift(ww1._recid)

            elif ww1.main_code == 1991:
                fill_cover_shift(ww1._recid)

            elif ww1.main_code == 1992:
                fill_cover_shift(ww1._recid)

            elif ww1.main_code == 1993:
                fill_cover_shift(ww1._recid)

            elif ww1.main_code == 1994:
                fill_cover_shift(ww1._recid)

            elif ww1.main_code >= 2001 and ww1.main_code <= 2004:
                fill_pax_cover_shift1(ww1._recid)

            elif ww1.main_code == 2005:
                fill_cover_shift1(ww1._recid)

            elif ww1.main_code == 2006:
                fill_cover_shift1(ww1._recid)

            elif ww1.main_code == 2007:
                fill_cover_shift1(ww1._recid)

            elif ww1.main_code == 2008:
                fill_cover_shift1(ww1._recid)

            elif ww1.main_code == 2009:
                fill_cover_shift2(ww1._recid)

            elif ww1.main_code == 2010:
                fill_cover_shift2(ww1._recid)

            elif ww1.main_code == 2011:
                fill_cover_shift2(ww1._recid)

            elif ww1.main_code == 2012:
                fill_cover_shift2(ww1._recid)

            elif ww1.main_code == 2013:
                fill_cover_shift2(ww1._recid)

            elif ww1.main_code == 2014:
                fill_cover_shift2(ww1._recid)

            elif ww1.main_code == 2015:
                fill_cover_shift2(ww1._recid)

            elif ww1.main_code == 2016:
                fill_cover_shift2(ww1._recid)

            elif (ww1.main_code == 1995 or ww1.main_code == 1996):
                fill_pax_cover_shift1(ww1._recid)

            elif (ww1.main_code == 1997 or ww1.main_code == 1998 or ww1.main_code == 1999):
                fill_fbstat(ww1._recid)

            elif ww1.main_code >= 2020 and ww1.main_code <= 2051:
                fill_pax_cover_shift1(ww1._recid)

            elif ww1.main_code >= 2052 and ww1.main_code <= 2055:
                fill_pax_cover_shift1(ww1._recid)

            elif ww1.main_code >= 2056 and ww1.main_code <= 2059:
                fill_fb_flash(ww1._recid)

            elif ww1.main_code == 9000:
                done_los = fill_los()

            elif ww1.main_code == 9106:
                fill_new_wig(ww1._recid)

            elif ww1.main_code == 85:
                fill_arrdep(ww1._recid, "arrival-RSV", 85, 86, 0)

            elif ww1.main_code == 86:
                fill_arrdep(ww1._recid, "arrival-RSV", 85, 86, 0)

            elif ww1.main_code == 106:
                fill_arrdep(ww1._recid, "arrival-WIG", 106, 107, 0)

            elif ww1.main_code == 107:
                fill_arrdep(ww1._recid, "arrival-WIG", 106, 107, 0)

            elif ww1.main_code == 187:
                fill_arrdep(ww1._recid, "arrival", 187, 188, 0)

            elif ww1.main_code == 188:
                fill_arrdep(ww1._recid, "arrival", 187, 188, 0)

            elif ww1.main_code == 9188:
                fill_arrdep(ww1._recid, "arrival", 0, 0, 9188)

            elif ww1.main_code == 189:
                fill_arrdep(ww1._recid, "departure", 189, 190, 0)

            elif ww1.main_code == 190:
                fill_arrdep(ww1._recid, "departure", 189, 190, 0)

            elif ww1.main_code == 9190:
                fill_arrdep(ww1._recid, "departure", 0, 0, 9190)

            elif ww1.main_code == 191:
                fill_arrdep(ww1._recid, "VIP", 0, 191, 0)

            elif ww1.main_code == 193:
                fill_arrdep(ww1._recid, "NewRes", 193, 0, 0)

            elif ww1.main_code == 194:
                fill_arrdep(ww1._recid, "CancRes", 194, 0, 0)

            elif ww1.main_code == 7194:
                fill_canc_room_night(ww1._recid)

            elif ww1.main_code == 7195:
                fill_canc_cidate(ww1._recid)

            elif ww1.main_code == 195:
                fill_avrgstay(ww1._recid, "Avrg-Stay", 195)

            elif ww1.main_code == 211:
                fill_arrdep(ww1._recid, "ArrTmrw", 211, 231, 0)

            elif ww1.main_code == 231:
                fill_arrdep(ww1._recid, "ArrTmrw", 211, 231, 0)

            elif ww1.main_code == 742:
                fill_arrdep(ww1._recid, "Early-CO", 742, 0, 0)

            elif ww1.main_code == 750:
                fill_arrdep(ww1._recid, "DepTmrw", 750, 751, 0)

            elif ww1.main_code == 751:
                fill_arrdep(ww1._recid, "DepTmrw", 750, 751, 0)

            elif ww1.main_code == 969:
                fill_arrdep(ww1._recid, "No-Show", 969, 0, 0)

            elif ww1.main_code == 806:
                fill_new_rmocc(ww1._recid)

                if error_nr != 0:

                    return

            elif ww1.main_code == 182:
                fill_gledger(ww1._recid)

                if error_nr != 0:

                    return

            elif ww1.main_code == 183:
                fill_comproomsnew(ww1._recid)

                if error_nr != 0:

                    return

            elif ww1.main_code == 807:
                fill_rmocc_perc(ww1._recid)

                if error_nr != 0:

                    return

            elif ww1.main_code == 808:
                fill_docc_perc(ww1._recid)

                if error_nr != 0:

                    return

            elif ww1.main_code == 1008:
                fill_fbcost(ww1._recid)

            elif ww1.main_code == 9985 or ww1.main_code == 9986:
                fill_sgfb(ww1._recid, ww1.main_code)

            elif ww1.main_code == 1084:
                fill_quantity(ww1._recid)

            elif ww1.main_code == 809:
                fill_revenue(ww1._recid)

            elif ww1.main_code == 810:
                fill_persocc(ww1._recid)

            elif ww1.main_code == 811:
                fill_avrgrate(ww1._recid)

            elif ww1.main_code == 812:
                fill_avrglrate(ww1._recid)

            elif ww1.main_code == 842:
                fill_avrglodg(ww1._recid)

            elif ww1.main_code == 46:
                fill_avrgllodge(ww1._recid)

            elif ww1.main_code == 92 or ww1.main_code == 813 or ww1.main_code == 814 or ww1.main_code == 756 or ww1.main_code == 757 or ww1.main_code == 758:
                fill_segment(ww1._recid, ww1.main_code)

            elif ww1.main_code == 8092 or ww1.main_code == 8813 or ww1.main_code == 8814:
                fill_nation(ww1._recid, ww1.main_code)

            elif ww1.main_code == 9981 or ww1.main_code == 9982 or ww1.main_code == 9983 or ww1.main_code == 9984:
                fill_competitor(ww1._recid, ww1.main_code)

            elif ww1.main_code == 179:
                fill_rmcatstat(ww1._recid, ww1.main_code)

            elif ww1.main_code == 180 or ww1.main_code == 181 or ww1.main_code == 800:
                fill_zinrstat(ww1._recid, ww1.main_code)

            elif ww1.main_code == 9092 or ww1.main_code == 9813 or ww1.main_code == 9814:
                fill_source(ww1._recid, ww1.main_code)

            elif ww1.main_code == 9008 and not done_adddayuse:
                done_adddayuse = fill_adddayuse()

        for w1 in query(w1_list, filters=(lambda w1: w1.grpflag >= 1 and w1.grpflag != 9), sort_by=[("nr",False)]):

            for w2 in query(w2_list, filters=(lambda w2: w2.nr1 == w1.nr)):

                curr_child = query(curr_child_list, filters=(lambda curr_child: curr_child.nr == w2.nr2), first=True)
                fill_value1(w1._recid, curr_child._recid, w2.val_sign)


    def fill_adddayuse():

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        done = False
        datum1:date = None

        def generate_inner_output():
            return (done)

        Wdu = W1
        wdu_list = w1_list

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        res_line_obj_list = {}
        res_line = Res_line()
        arrangement = Arrangement()
        for res_line.ankunft, res_line.resnr, res_line.reslinnr, res_line.zimmeranz, res_line.active_flag, res_line.abreise, res_line._recid, arrangement.argt_artikelnr, arrangement._recid in db_session.query(Res_line.ankunft, Res_line.resnr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.active_flag, Res_line.abreise, Res_line._recid, Arrangement.argt_artikelnr, Arrangement._recid).join(Arrangement,(Arrangement.arrangement == Res_line.arrangement)).filter(
                 (Res_line.active_flag == 2) & (Res_line.ankunft >= datum1) & (Res_line.ankunft <= to_date) & (Res_line.abreise == Res_line.ankunft) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Res_line.zinr, Res_line.resnr, Res_line.reslinnr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            bill_line = get_cache (Bill_line, {"departement": [(eq, 0)],"artnr": [(eq, arrangement.argt_artikelnr)],"bill_datum": [(eq, res_line.ankunft)],"massnr": [(eq, res_line.resnr)],"billin_nr": [(eq, res_line.reslinnr)]})

            if not bill_line:

                if res_line.ankunft == to_date:
                    wdu.tday =  to_decimal(wdu.tday) + to_decimal(res_line.zimmeranz)

                if res_line.ankunft >= from_date:
                    wdu.saldo =  to_decimal(wdu.saldo) + to_decimal(res_line.zimmeranz)
                wdu.ytd_saldo =  to_decimal(wdu.ytd_saldo) + to_decimal(res_line.zimmeranz)
        done = True

        return generate_inner_output()


    def fill_totroom(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum:date = None
        datum1:date = None
        datum2:date = None
        curr_date:date = None
        anz:int = 0
        anz0:int = 0
        d_flag:bool = False
        dlmtd_flag:bool = False

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return
        anz0 = 0

        for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
            anz0 = anz0 + 1

        if (get_day(to_date) == 31 and get_month(to_date) != 8 and get_month(to_date) != 1) or (get_day(to_date) == 30 and get_month(to_date) == 3) or (get_day(date_mdy(3, 1, get_year(to_date)) - 1) == 28 and get_month(to_date) == 3 and get_day(to_date) == 29):
            w1.lm_today =  to_decimal("0")
        else:

            if get_month(to_date) == 1:
                curr_date = date_mdy(12, get_day(to_date) , get_year(to_date) - timedelta(days=1))
            else:
                curr_date = date_mdy(get_month(to_date) - timedelta(days=1, get_day(to_date) , get_year(to_date)))

            zinrstat = get_cache (Zinrstat, {"datum": [(eq, curr_date)],"zinr": [(eq, "tot-rm")]})

            if zinrstat:
                w1.lm_today =  to_decimal(zinrstat.zimmeranz)
            else:
                w1.lm_today =  to_decimal(anz0)

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date
        for datum in date_range(datum1,to_date) :

            zinrstat = get_cache (Zinrstat, {"datum": [(eq, datum)],"zinr": [(eq, "tot-rm")]})

            if zinrstat:
                anz = zinrstat.zimmeranz
            else:
                anz = anz0
            d_flag = None != zinrstat and (get_month(zinrstat.datum) == get_month(to_date)) and (get_year(zinrstat.datum) == get_year(to_date))

            if zinrstat:

                if d_flag:
                    w1.mon_saldo[get_day(zinrstat.datum) - 1] = w1.mon_saldo[get_day(zinrstat.datum) - 1] + anz

            if datum == to_date - timedelta(days=1):
                w1.yesterday =  to_decimal(w1.yesterday) + to_decimal(anz)

            if datum == to_date:
                w1.tday =  to_decimal(w1.tday) + to_decimal(anz)

            if start_date != None:

                if (datum < from_date) and (datum >= start_date):
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(anz)
                else:

                    if (datum >= start_date):
                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(anz)

                    if ytd_flag and (datum >= start_date):
                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(anz)
            else:

                if datum <= lfr_date:
                    w1.lm_ytd =  to_decimal(w1.lm_ytd) + to_decimal(anz)

                if (datum < from_date):
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(anz)
                else:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(anz)

                    if ytd_flag:
                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(anz)

        if (lytd_flag or lmtd_flag):

            if lytd_flag:
                datum2 = ljan1
            else:
                datum2 = lfrom_date
            for datum in date_range(datum2,lto_date) :

                zinrstat = get_cache (Zinrstat, {"datum": [(eq, datum)],"zinr": [(eq, "tot-rm")]})

                if zinrstat:
                    anz = zinrstat.zimmeranz
                else:
                    anz = anz0
                dlmtd_flag = None != zinrstat and (get_month(zinrstat.datum) == get_month(to_date)) and (get_year(zinrstat.datum) == get_year(to_date) - 1)

                if dlmtd_flag:
                    w1.mon_lmtd[get_day(zinrstat.datum) - 1] = w1.mon_lmtd[get_day(zinrstat.datum) - 1] + anz

                if start_date != None:

                    if (datum < lfrom_date) and (datum >= start_date):
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(anz)

                    elif (datum >= start_date):
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(anz)

                        if lytd_flag:
                            w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(anz)
                else:

                    if (datum < lfrom_date):
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(anz)
                    else:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(anz)

                        if lytd_flag:
                            w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(anz)

        if pmtd_flag:
            for datum in date_range(pfrom_date,pto_date) :

                zinrstat = get_cache (Zinrstat, {"datum": [(eq, datum)],"zinr": [(eq, "tot-rm")]})

                if zinrstat:
                    anz = zinrstat.zimmeranz
                else:
                    anz = anz0

                if start_date != None:

                    if (datum >= start_date):
                        w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(anz)
                else:
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(anz)

        if lytoday_flag:
            w1.lytoday =  to_decimal(anz)
        w1.done = True


    def fill_rmavail(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        datum2:date = None
        curr_date:date = None

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        if (get_day(to_date) == 31 and get_month(to_date) != 8 and get_month(to_date) != 1) or (get_day(to_date) == 30 and get_month(to_date) == 3) or (get_day(date_mdy(3, 1, get_year(to_date)) - 1) == 28 and get_month(to_date) == 3 and get_day(to_date) == 29):
            w1.lm_today =  to_decimal("0")
        else:

            if get_month(to_date) == 1:
                curr_date = date_mdy(12, get_day(to_date) , get_year(to_date) - timedelta(days=1))
            else:
                curr_date = date_mdy(get_month(to_date) - timedelta(days=1, get_day(to_date) , get_year(to_date)))

            zkstat = get_cache (Zkstat, {"datum": [(eq, curr_date)],"zikatnr": [(eq, zimkateg.zikatnr)]})

            if zkstat:
                w1.lm_today =  to_decimal(w1.lm_today) + to_decimal(zkstat.anz100)

        for zkstat in db_session.query(Zkstat).filter(
                 (Zkstat.datum >= datum1) & (Zkstat.datum <= to_date)).order_by(Zkstat._recid).all():

            if zkstat.datum == to_date - timedelta(days=1):
                w1.yesterday =  to_decimal(w1.yesterday) + to_decimal(zkstat.anz100)

            if zkstat.datum == to_date:
                w1.tday =  to_decimal(w1.tday) + to_decimal(zkstat.anz100)

            if zkstat.datum < from_date:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zkstat.anz100)
            else:
                w1.saldo =  to_decimal(w1.saldo) + to_decimal(zkstat.anz100)

                if ytd_flag:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zkstat.anz100)

            if get_month(zkstat.datum) == get_month(to_date) and get_year(zkstat.datum) == get_year(to_date):
                w1.mon_saldo[get_day(zkstat.datum) - 1] = w1.mon_saldo[get_day(zkstat.datum) - 1] + zkstat.anz100

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum2 = ljan1
            else:
                datum2 = lfrom_date

            for zkstat in db_session.query(Zkstat).filter(
                     (Zkstat.datum >= datum2) & (Zkstat.datum <= lto_date)).order_by(Zkstat._recid).all():

                if zkstat.datum < lfrom_date:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zkstat.anz100)
                else:
                    w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(zkstat.anz100)

                    if lytd_flag:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zkstat.anz100)

        if lytoday_flag:

            for zkstat in db_session.query(Zkstat).filter(
                     (Zkstat.datum == lytoday)).order_by(Zkstat._recid).all():
                w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(zkstat.anz100)


        if pmtd_flag:

            for zkstat in db_session.query(Zkstat).filter(
                     (Zkstat.datum >= pfrom_date) & (Zkstat.datum <= pto_date)).order_by(Zkstat._recid).all():
                w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(zkstat.anz100)

        w1.done = True


    def fill_ooo(rec_w1:int, key_word:string):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.datum >= datum1) & (Zinrstat.datum <= to_date) & (Zinrstat.zinr == (key_word).lower())).order_by(Zinrstat._recid).all():

            if zinrstat.datum == to_date:
                w1.tday =  to_decimal(w1.tday) + to_decimal(zinrstat.zimmeranz)

            if zinrstat.datum < from_date:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.zimmeranz)
            else:
                w1.saldo =  to_decimal(w1.saldo) + to_decimal(zinrstat.zimmeranz)

                if ytd_flag:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.zimmeranz)

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= datum1) & (Zinrstat.datum <= lto_date) & (Zinrstat.zinr == (key_word).lower())).order_by(Zinrstat._recid).all():

                if zinrstat.datum < lfrom_date:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.zimmeranz)
                else:
                    w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(zinrstat.zimmeranz)

                    if lytd_flag:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.zimmeranz)

        if pmtd_flag:

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= pfrom_date) & (Zinrstat.datum <= pto_date) & (Zinrstat.zinr == (key_word).lower())).order_by(Zinrstat._recid).all():
                w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(zinrstat.zimmeranz)


        if lytoday_flag:

            zinrstat = get_cache (Zinrstat, {"datum": [(eq, lytoday)],"zinr": [(eq, key_word)]})

            if zinrstat:
                w1.lytoday =  to_decimal(zinrstat.zimmeranz)
        w1.done = True


    def fill_vacant(rec_w1:int, key_word:string):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.datum >= datum1) & (Zinrstat.datum <= to_date) & (Zinrstat.zinr == (key_word).lower())).order_by(Zinrstat._recid).all():

            if zinrstat.datum == to_date:
                w1.tday =  to_decimal(w1.tday) + to_decimal(zinrstat.zimmeranz)

            if zinrstat.datum < from_date:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.zimmeranz)
            else:
                w1.saldo =  to_decimal(w1.saldo) + to_decimal(zinrstat.zimmeranz)

                if ytd_flag:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.zimmeranz)

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= datum1) & (Zinrstat.datum <= lto_date) & (Zinrstat.zinr == (key_word).lower())).order_by(Zinrstat._recid).all():

                if zinrstat.datum < lfrom_date:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.zimmeranz)
                else:
                    w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(zinrstat.zimmeranz)

                    if lytd_flag:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.zimmeranz)

        if pmtd_flag:

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= pfrom_date) & (Zinrstat.datum <= pto_date) & (Zinrstat.zinr == (key_word).lower())).order_by(Zinrstat._recid).all():
                w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(zinrstat.zimmeranz)


        if lytoday_flag:

            zinrstat = get_cache (Zinrstat, {"datum": [(eq, lytoday)],"zinr": [(eq, key_word)]})

            if zinrstat:
                w1.lytoday =  to_decimal(zinrstat.zimmeranz)
        w1.done = True


    def fill_cover(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        curr_date:date = None
        d_flag:bool = False
        dlmtd_flag:bool = False
        hbuff = None
        Hbuff =  create_buffer("Hbuff",H_umsatz)
        W11 = W1
        w11_list = w1_list
        W12 = W1
        w12_list = w1_list
        W13 = W1
        w13_list = w1_list

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return
        pass
        pass
        pass

        w12 = query(w12_list, filters=(lambda w12: w12.main_code == 192 and w12.dept == w1.dept), first=True)

        w13 = query(w13_list, filters=(lambda w13: w13.main_code == 197 and w13.dept == w1.dept), first=True)

        if (get_day(to_date) == 31 and get_month(to_date) != 8 and get_month(to_date) != 1) or (get_day(to_date) == 30 and get_month(to_date) == 3) or (get_day(date_mdy(3, 1, get_year(to_date)) - 1) == 28 and get_month(to_date) == 3 and get_day(to_date) == 29):

            if w11:
                w11.lm_today =  to_decimal("0")

            if w12:
                w12.lm_today =  to_decimal("0")

            if w13:
                w13.lm_today =  to_decimal("0")
        else:

            if get_month(to_date) == 1:
                curr_date = date_mdy(12, get_day(to_date) , get_year(to_date) - timedelta(days=1))
            else:
                curr_date = date_mdy(get_month(to_date) - timedelta(days=1, get_day(to_date) , get_year(to_date)))

            h_umsatz = get_cache (H_umsatz, {"datum": [(eq, curr_date)],"artnr": [(eq, 0)],"departement": [(eq, w1.dept)],"betriebsnr": [(eq, w1.dept)]})

            if h_umsatz:

                if w11:
                    w11.lm_today =  to_decimal(h_umsatz.anzahl)

                if w12:
                    w12.lm_today =  to_decimal(h_umsatz.betrag)

                if w13:
                    w13.lm_today =  to_decimal(h_umsatz.nettobetrag)

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for h_umsatz in db_session.query(H_umsatz).filter(
                 (H_umsatz.datum >= datum1) & (H_umsatz.datum <= to_date) & (H_umsatz.artnr == 0) & (H_umsatz.departement == w1.dept) & (H_umsatz.betriebsnr == w1.dept)).order_by(H_umsatz._recid).all():
            d_flag = (get_month(h_umsatz.datum) == get_month(to_date)) and (get_year(h_umsatz.datum) == get_year(to_date))

            if d_flag:

                if w11:
                    w11.mon_saldo[get_day(h_umsatz.datum) - 1] = h_umsatz.anzahl

                if w12:
                    w12.mon_saldo[get_day(h_umsatz.datum) - 1] = h_umsatz.betrag

                if w13:
                    w13.mon_saldo[get_day(h_umsatz.datum) - 1] = h_umsatz.nettobetrag

            if h_umsatz.datum == to_date - timedelta(days=1):

                if w11:
                    w11.yesterday =  to_decimal(h_umsatz.anzahl)

                if w12:
                    w12.yesterday =  to_decimal(h_umsatz.betrag)

                if w13:
                    w13.yesterday =  to_decimal(h_umsatz.nettobetrag)

            if h_umsatz.datum == to_date:

                if w11:
                    w11.tday =  to_decimal(h_umsatz.anzahl)

                if w12:
                    w12.tday =  to_decimal(h_umsatz.betrag)

                if w13:
                    w13.tday =  to_decimal(h_umsatz.nettobetrag)

            if h_umsatz.datum <= lfr_date:

                if w11:
                    w11.lm_ytd =  to_decimal(w11.lm_ytd) + to_decimal(h_umsatz.anzahl)

                if w12:
                    w12.lm_ytd =  to_decimal(w12.lm_ytd) + to_decimal(h_umsatz.betrag)

                if w13:
                    w13.lm_ytd =  to_decimal(w13.lm_ytd) + to_decimal(h_umsatz.nettobetrag)

            if h_umsatz.datum < from_date:

                if w11:
                    w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(h_umsatz.anzahl)

                if w12:
                    w12.ytd_saldo =  to_decimal(w12.ytd_saldo) + to_decimal(h_umsatz.betrag)

                if w13:
                    w13.ytd_saldo =  to_decimal(w13.ytd_saldo) + to_decimal(h_umsatz.nettobetrag)
            else:

                if w11:
                    w11.saldo =  to_decimal(w11.saldo) + to_decimal(h_umsatz.anzahl)

                if ytd_flag and w11:
                    w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(h_umsatz.anzahl)

                if w12:
                    w12.saldo =  to_decimal(w12.saldo) + to_decimal(h_umsatz.betrag)

                if ytd_flag and w12:
                    w12.ytd_saldo =  to_decimal(w12.ytd_saldo) + to_decimal(h_umsatz.betrag)

                if w13:
                    w13.saldo =  to_decimal(w13.saldo) + to_decimal(h_umsatz.nettobetrag)

                if ytd_flag and w13:
                    w13.ytd_saldo =  to_decimal(w13.ytd_saldo) + to_decimal(h_umsatz.nettobetrag)

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            for h_umsatz in db_session.query(H_umsatz).filter(
                     (H_umsatz.datum >= datum1) & (H_umsatz.datum <= lto_date) & (H_umsatz.artnr == 0) & (H_umsatz.departement == w1.dept) & (H_umsatz.betriebsnr == w1.dept)).order_by(H_umsatz._recid).all():

                if h_umsatz.datum < lfrom_date:

                    if w11:
                        w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(h_umsatz.anzahl)

                    if w12:
                        w12.lytd_saldo =  to_decimal(w12.lytd_saldo) + to_decimal(h_umsatz.betrag)

                    if w13:
                        w13.lytd_saldo =  to_decimal(w13.lytd_saldo) + to_decimal(h_umsatz.nettobetrag)
                else:
                    dlmtd_flag = (get_month(h_umsatz.datum) == get_month(to_date)) and (get_year(h_umsatz.datum) == get_year(to_date) - 1)

                    if dlmtd_flag:

                        if w11:
                            w11.mon_lmtd[get_day(h_umsatz.datum) - 1] = w11.mon_lmtd[get_day(h_umsatz.datum) - 1] + h_umsatz.anzahl

                        if w12:
                            w12.mon_lmtd[get_day(h_umsatz.datum) - 1] = w12.mon_lmtd[get_day(h_umsatz.datum) - 1] + h_umsatz.betrag

                        if w13:
                            w13.mon_lmtd[get_day(h_umsatz.datum) - 1] = w13.mon_lmtd[get_day(h_umsatz.datum) - 1] + h_umsatz.nettobetrag

                    if w11:
                        w11.lastyr =  to_decimal(w11.lastyr) + to_decimal(h_umsatz.anzahl)

                    if lytd_flag and w11:
                        w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(h_umsatz.anzahl)

                    if w12:
                        w12.lastyr =  to_decimal(w12.lastyr) + to_decimal(h_umsatz.betrag)

                    if lytd_flag and w12:
                        w12.lytd_saldo =  to_decimal(w12.lytd_saldo) + to_decimal(h_umsatz.betrag)

                    if w13:
                        w13.lastyr =  to_decimal(w13.lastyr) + to_decimal(h_umsatz.nettobetrag)

                    if lytd_flag and w13:
                        w13.lytd_saldo =  to_decimal(w13.lytd_saldo) + to_decimal(h_umsatz.nettobetrag)

        if pmtd_flag:

            for h_umsatz in db_session.query(H_umsatz).filter(
                     (H_umsatz.datum >= pfrom_date) & (H_umsatz.datum <= pto_date) & (H_umsatz.artnr == 0) & (H_umsatz.departement == w1.dept) & (H_umsatz.betriebsnr == w1.dept)).order_by(H_umsatz._recid).all():

                if w11:
                    w11.lastmon =  to_decimal(w11.lastmon) + to_decimal(h_umsatz.anzahl)

                if w12:
                    w12.lastmon =  to_decimal(w12.lastmon) + to_decimal(h_umsatz.betrag)

                if w13:
                    w13.lastmon =  to_decimal(w13.lastmon) + to_decimal(h_umsatz.nettobetrag)


        if lytoday_flag:

            for h_umsatz in db_session.query(H_umsatz).filter(
                     (H_umsatz.datum == lytoday) & (H_umsatz.artnr == 0) & (H_umsatz.departement == w1.dept) & (H_umsatz.betriebsnr == w1.dept)).order_by(H_umsatz._recid).all():

                if w11:
                    w11.lytoday =  to_decimal(w11.lytoday) + to_decimal(h_umsatz.anzahl)

                if w12:
                    w12.lytoday =  to_decimal(w12.lytoday) + to_decimal(h_umsatz.betrag)

                if w13:
                    w13.lytoday =  to_decimal(w13.lytoday) + to_decimal(h_umsatz.nettobetrag)


        if w11:
            w11.done = True

        if w12:
            w12.done = True

        if w13:
            w13.done = True


    def fill_canc_room_night(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        resbuff = None
        Resbuff =  create_buffer("Resbuff",Res_line)

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        if w1:

            for resbuff in db_session.query(Resbuff).filter(
                     (Resbuff.resstatus == 9) & (Resbuff.active_flag == 2) & (Resbuff.betrieb_gastpay != 3) & (Resbuff.cancelled >= datum1) & (Resbuff.cancelled <= to_date) & (Resbuff.l_zuordnung[inc_value(2)] == 0)).order_by(Resbuff._recid).all():

                if resbuff.cancelled == to_date:
                    w1.tday =  to_decimal(w1.tday) + to_decimal((resbuff.abreise) - to_decimal(resbuff.ankunft)) * to_decimal(resbuff.zimmeranz)

                if resbuff.cancelled < from_date:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal((resbuff.abreise) - to_decimal(resbuff.ankunft)) * to_decimal(resbuff.zimmeranz)
                else:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal((resbuff.abreise) - to_decimal(resbuff.ankunft)) * to_decimal(resbuff.zimmeranz)

                    if ytd_flag:
                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal((resbuff.abreise) - to_decimal(resbuff.ankunft)) * to_decimal(resbuff.zimmeranz)

            if lytd_flag or lmtd_flag:

                if lytd_flag:
                    datum1 = ljan1
                else:
                    datum1 = lfrom_date

                for resbuff in db_session.query(Resbuff).filter(
                         (Resbuff.resstatus == 9) & (Resbuff.active_flag == 2) & (Resbuff.betrieb_gastpay != 3) & (Resbuff.cancelled >= datum1) & (Resbuff.cancelled <= lto_date) & (Resbuff.l_zuordnung[inc_value(2)] == 0)).order_by(Resbuff._recid).all():

                    if resbuff.cancelled < lfrom_date:
                        w1.lytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal((resbuff.abreise) - to_decimal(resbuff.ankunft)) * to_decimal(resbuff.zimmeranz)
                    else:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal((resbuff.abreise) - to_decimal(resbuff.ankunft)) * to_decimal(resbuff.zimmeranz)

                        if lytd_flag:
                            w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal((resbuff.abreise) - to_decimal(resbuff.ankunft)) * to_decimal(resbuff.zimmeranz)


    def fill_canc_cidate(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        resbuff = None
        Resbuff =  create_buffer("Resbuff",Res_line)

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        if w1:

            for resbuff in db_session.query(Resbuff).filter(
                     (Resbuff.resstatus == 9) & (Resbuff.active_flag == 2) & (Resbuff.betrieb_gastpay != 3) & (Resbuff.cancelled >= datum1) & (Resbuff.cancelled <= to_date) & (Resbuff.cancelled == Resbuff.ankunft) & (Resbuff.l_zuordnung[inc_value(2)] == 0)).order_by(Resbuff._recid).all():

                if resbuff.ankunft == to_date:
                    w1.tday =  to_decimal(w1.tday) + to_decimal((resbuff.abreise) - to_decimal(resbuff.ankunft)) * to_decimal(resbuff.zimmeranz)

                if resbuff.cancelled < from_date:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal((resbuff.abreise) - to_decimal(resbuff.ankunft)) * to_decimal(resbuff.zimmeranz)
                else:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal((resbuff.abreise) - to_decimal(resbuff.ankunft)) * to_decimal(resbuff.zimmeranz)

                    if ytd_flag:
                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal((resbuff.abreise) - to_decimal(resbuff.ankunft)) * to_decimal(resbuff.zimmeranz)

            if lytd_flag or lmtd_flag:

                if lytd_flag:
                    datum1 = ljan1
                else:
                    datum1 = lfrom_date

                for resbuff in db_session.query(Resbuff).filter(
                         (Resbuff.resstatus == 9) & (Resbuff.active_flag == 2) & (Resbuff.betrieb_gastpay != 3) & (Resbuff.cancelled >= datum1) & (Resbuff.cancelled <= lto_date) & (Resbuff.cancelled == Resbuff.ankunft) & (Resbuff.l_zuordnung[inc_value(2)] == 0)).order_by(Resbuff._recid).all():

                    if resbuff.ankunft < lfrom_date:
                        w1.lytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal((resbuff.abreise) - to_decimal(resbuff.ankunft)) * to_decimal(resbuff.zimmeranz)
                    else:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal((resbuff.abreise) - to_decimal(resbuff.ankunft)) * to_decimal(resbuff.zimmeranz)

                        if lytd_flag:
                            w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal((resbuff.abreise) - to_decimal(resbuff.ankunft)) * to_decimal(resbuff.zimmeranz)


    def fill_arrdep(rec_w1:int, key_word:string, number1:int, number2:int, number3:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        curr_date:date = None
        d_flag:bool = False
        W11 = W1
        w11_list = w1_list
        W12 = W1
        w12_list = w1_list
        W13 = W1
        w13_list = w1_list

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return
        pass
        pass
        pass

        if number1 != 0:

            w11 = query(w11_list, filters=(lambda w11: w11.main_code == number1 and not w11.done), first=True)

        if number2 != 0:

            w12 = query(w12_list, filters=(lambda w12: w12.main_code == number2 and not w12.done), first=True)

        if number3 != 0:

            w13 = query(w13_list, filters=(lambda w13: w13.main_code == number3 and not w13.done), first=True)

        if (get_day(to_date) == 31 and get_month(to_date) != 8 and get_month(to_date) != 1) or (get_day(to_date) == 30 and get_month(to_date) == 3) or (get_day(date_mdy(3, 1, get_year(to_date)) - 1) == 28 and get_month(to_date) == 3 and get_day(to_date) == 29):

            if w11:
                w11.lm_today =  to_decimal("0")

            if w12:
                w12.lm_today =  to_decimal("0")
        else:

            if get_month(to_date) == 1:
                curr_date = date_mdy(12, get_day(to_date) , get_year(to_date) - timedelta(days=1))
            else:
                curr_date = date_mdy(get_month(to_date) - timedelta(days=1, get_day(to_date) , get_year(to_date)))

            zinrstat = get_cache (Zinrstat, {"datum": [(eq, curr_date)],"zinr": [(eq, key_word)]})

            if zinrstat:

                if w11:
                    w11.lm_today =  to_decimal(w11.lm_today) + to_decimal(zinrstat.zimmeranz)

                if w12:
                    w12.lm_today =  to_decimal(w12.lm_today) + to_decimal(zinrstat.personen)

                if w13:
                    w13.lm_today =  to_decimal(w13.lm_today) + to_decimal(zinrstat.betriebsnr)

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.datum >= datum1) & (Zinrstat.datum <= to_date) & (Zinrstat.zinr == (key_word).lower())).order_by(Zinrstat._recid).all():
            d_flag = (get_month(zinrstat.datum) == get_month(to_date)) and (get_year(zinrstat.datum) == get_year(to_date))

            if zinrstat.datum == to_date - timedelta(days=1):

                if w11:
                    w11.yesterday =  to_decimal(w11.yesterday) + to_decimal(zinrstat.zimmeranz)

                if w12:
                    w12.yesterday =  to_decimal(w12.yesterday) + to_decimal(zinrstat.personen)

                if w13:
                    w13.yesterday =  to_decimal(w13.yesterday) + to_decimal(zinrstat.betriebsnr)

            if zinrstat.datum == to_date:

                if w11:
                    w11.tday =  to_decimal(w11.tday) + to_decimal(zinrstat.zimmeranz)

                if w12:
                    w12.tday =  to_decimal(w12.tday) + to_decimal(zinrstat.personen)

                if w13:
                    w13.tday =  to_decimal(w13.tday) + to_decimal(zinrstat.betriebsnr)

            if zinrstat.datum < from_date:

                if w11:
                    w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(zinrstat.zimmeranz)

                if w12:
                    w12.ytd_saldo =  to_decimal(w12.ytd_saldo) + to_decimal(zinrstat.personen)

                if w13:
                    w13.ytd_saldo =  to_decimal(w13.ytd_saldo) + to_decimal(zinrstat.betriebsnr)
            else:

                if w11:
                    w11.saldo =  to_decimal(w11.saldo) + to_decimal(zinrstat.zimmeranz)

                if ytd_flag and w11:
                    w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(zinrstat.zimmeranz)

                if w12:
                    w12.saldo =  to_decimal(w12.saldo) + to_decimal(zinrstat.personen)

                if ytd_flag and w12:
                    w12.ytd_saldo =  to_decimal(w12.ytd_saldo) + to_decimal(zinrstat.personen)

                if w13:
                    w13.saldo =  to_decimal(w13.saldo) + to_decimal(zinrstat.betriebsnr)

                if ytd_flag and w13:
                    w13.ytd_saldo =  to_decimal(w13.ytd_saldo) + to_decimal(zinrstat.betriebsnr)

            if w11:

                if d_flag:
                    w11.mon_saldo[get_day(zinrstat.datum) - 1] = w11.mon_saldo[get_day(zinrstat.datum) - 1] + zinrstat.zimmeranz

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= datum1) & (Zinrstat.datum <= lto_date) & (Zinrstat.zinr == (key_word).lower())).order_by(Zinrstat._recid).all():

                if zinrstat.datum < lfrom_date:

                    if w11:
                        w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(zinrstat.zimmeranz)

                    if w12:
                        w12.lytd_saldo =  to_decimal(w12.lytd_saldo) + to_decimal(zinrstat.personen)

                    if w13:
                        w13.lytd_saldo =  to_decimal(w13.lytd_saldo) + to_decimal(zinrstat.betriebsnr)
                else:

                    if w11:
                        w11.lastyr =  to_decimal(w11.lastyr) + to_decimal(zinrstat.zimmeranz)

                    if lytd_flag and w11:
                        w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(zinrstat.zimmeranz)

                    if w12:
                        w12.lastyr =  to_decimal(w12.lastyr) + to_decimal(zinrstat.personen)

                    if lytd_flag and w12:
                        w12.lytd_saldo =  to_decimal(w12.lytd_saldo) + to_decimal(zinrstat.personen)

                    if w13:
                        w13.lastyr =  to_decimal(w13.lastyr) + to_decimal(zinrstat.betriebsnr)

                    if lytd_flag and w13:
                        w13.lytd_saldo =  to_decimal(w13.lytd_saldo) + to_decimal(zinrstat.betriebsnr)

        if pmtd_flag:

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= pfrom_date) & (Zinrstat.datum <= pto_date) & (Zinrstat.zinr == (key_word).lower())).order_by(Zinrstat._recid).all():

                if w11:
                    w11.lastmon =  to_decimal(w11.lastmon) + to_decimal(zinrstat.zimmeranz)

                if w12:
                    w12.lastmon =  to_decimal(w12.lastmon) + to_decimal(zinrstat.personen)

                if w13:
                    w13.lastmon =  to_decimal(w13.lastmon) + to_decimal(zinrstat.betriebsnr)


        if lytoday_flag:

            zinrstat = get_cache (Zinrstat, {"datum": [(eq, lytoday)],"zinr": [(eq, key_word)]})

            if zinrstat:

                if w11:
                    w11.lytoday =  to_decimal(zinrstat.zimmeranz)

                if w12:
                    w12.lytoday =  to_decimal(zinrstat.personen)

                if w13:
                    w13.lytoday =  to_decimal(zinrstat.betriebsnr)

        if w11:
            w11.done = True

        if w12:
            w12.done = True

        if w13:
            w13.done = True


    def fill_avrgstay(rec_w1:int, key_word:string, number1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        W11 = W1
        w11_list = w1_list
        Tbuff = W1
        tbuff_list = w1_list

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        if number1 != 0:

            w11 = query(w11_list, filters=(lambda w11: w11.main_code == number1 and not w11.done), first=True)

        if not w11:

            return
        tbuff = Tbuff()
        tbuff_list.append(tbuff)


        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.datum >= datum1) & (Zinrstat.datum <= to_date) & (Zinrstat.zinr == (key_word).lower())).order_by(Zinrstat._recid).all():

            if zinrstat.datum == to_date:
                w11.tday =  to_decimal(w11.tday) + to_decimal(zinrstat.personen) / to_decimal(zinrstat.zimmeranz)

            if (zinrstat.datum < from_date):
                w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(zinrstat.personen)
                tbuff.ytd_saldo =  to_decimal(tbuff.ytd_saldo) + to_decimal(zinrstat.zimmeranz)
            else:
                w11.saldo =  to_decimal(w11.saldo) + to_decimal(zinrstat.personen)
                tbuff.saldo =  to_decimal(tbuff.saldo) + to_decimal(zinrstat.zimmeranz)

                if ytd_flag:
                    w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(zinrstat.personen)
                    tbuff.ytd_saldo =  to_decimal(tbuff.ytd_saldo) + to_decimal(zinrstat.zimmeranz)

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= datum1) & (Zinrstat.datum <= lto_date) & (Zinrstat.zinr == (key_word).lower())).order_by(Zinrstat._recid).all():

                if zinrstat.datum < lfrom_date:
                    w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(zinrstat.personen)
                    tbuff.lytd_saldo =  to_decimal(tbuff.lytd_saldo) + to_decimal(zinrstat.zimmeranz)
                else:
                    w11.lastyr =  to_decimal(w11.lastyr) + to_decimal(zinrstat.personen)
                    tbuff.lastyr =  to_decimal(tbuff.lastyr) + to_decimal(zinrstat.zimmeranz)

                    if lytd_flag:
                        w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(zinrstat.personen)
                        tbuff.lytd_saldo =  to_decimal(tbuff.lytd_saldo) + to_decimal(zinrstat.zimmeranz)

        if pmtd_flag:

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= pfrom_date) & (Zinrstat.datum <= pto_date) & (Zinrstat.zinr == (key_word).lower())).order_by(Zinrstat._recid).all():
                w11.lastmon =  to_decimal(w11.lastmon) + to_decimal(zinrstat.personen)
                tbuff.lastmon =  to_decimal(tbuff.lastmon) + to_decimal(zinrstat.zimmeranz)


        if lytoday_flag:

            zinrstat = get_cache (Zinrstat, {"datum": [(eq, lytoday)],"zinr": [(eq, key_word)]})

            if zinrstat:
                w11.lytoday =  to_decimal(zinrstat.personen)
                tbuff.lytoday =  to_decimal(zinrstat.zimmeranz)

        if tbuff.saldo != 0:
            w11.saldo =  to_decimal(w11.saldo) / to_decimal(tbuff.saldo)

        if tbuff.ytd_saldo != 0:
            w11.ytd_saldo =  to_decimal(w11.ytd_saldo) / to_decimal(tbuff.ytd_saldo)

        if tbuff.lytd_saldo != 0:
            w11.lytd_saldo =  to_decimal(w11.lytd_saldo) / to_decimal(tbuff.lytd_saldo)

        if tbuff.lastyr != 0:
            w11.lastyr =  to_decimal(w11.lastyr) / to_decimal(tbuff.lastyr)

        if tbuff.lastmon != 0:
            w11.lastmon =  to_decimal(w11.lastmon) / to_decimal(tbuff.lastmon)

        if tbuff.lytoday != 0:
            w11.lytoday =  to_decimal(w11.lytoday) / to_decimal(tbuff.lytoday)
        w11.done = True
        tbuff_list.remove(tbuff)


    def fill_rmocc(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        curr_date:date = None
        datum1:date = None
        datum2:date = None
        d_flag:bool = False
        dbudget_flag:bool = False
        dlmtd_flag:bool = False
        frate1:Decimal = to_decimal("0.0")
        W1a = W1
        w1a_list = w1_list

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        w1a = query(w1a_list, filters=(lambda w1a: w1a.main_code == 810), first=True)

        if w1a and w1a.done:
            pass

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for segment in db_session.query(Segment).order_by(Segment._recid).all():

            for segmentstat in db_session.query(Segmentstat).filter(
                     (Segmentstat.datum >= datum1) & (Segmentstat.datum <= to_date) & (Segmentstat.segmentcode == segment.segmentcode)).order_by(Segmentstat._recid).all():
                frate =  to_decimal("1")

                if foreign_flag:
                    find_exrate(segmentstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)
                d_flag = (get_month(segmentstat.datum) == get_month(to_date)) and (get_year(segmentstat.datum) == get_year(to_date))
                dbudget_flag = (get_month(segmentstat.datum) == get_month(to_date)) and (get_year(segmentstat.datum) == get_year(to_date))

                if segmentstat.datum == to_date - timedelta(days=1):

                    if w1a:
                        w1a.yesterday =  to_decimal(w1a.yesterday) + to_decimal(segmentstat.persanz) +\
                                segmentstat.kind1 + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)

                if segmentstat.datum == to_date:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(segmentstat.zimmeranz)
                    w1.tbudget =  to_decimal(w1.tbudget) + to_decimal(segmentstat.budzimmeranz)

                    if w1a:
                        w1a.tday =  to_decimal(w1a.tday) + to_decimal(segmentstat.persanz) +\
                                segmentstat.kind1 + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)


                        w1a.tbudget =  to_decimal(w1a.tbudget) + to_decimal(segmentstat.budpersanz)

                if segmentstat.datum < from_date:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(segmentstat.zimmeranz)
                    w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(segmentstat.budzimmeranz)

                    if w1a:
                        w1a.ytd_saldo =  to_decimal(w1a.ytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w1a.ytd_budget =  to_decimal(w1a.ytd_budget) + to_decimal(segmentstat.budpersanz)
                else:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(segmentstat.zimmeranz)
                    w1.budget =  to_decimal(w1.budget) + to_decimal(segmentstat.budzimmeranz)

                    if d_flag:
                        w1.mon_saldo[get_day(segmentstat.datum) - 1] = w1.mon_saldo[get_day(segmentstat.datum) - 1] + segmentstat.zimmeranz

                    if dbudget_flag:
                        w1.mon_budget[get_day(segmentstat.datum) - 1] = w1.mon_budget[get_day(segmentstat.datum) - 1] + segmentstat.budzimmeranz

                    if ytd_flag:
                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(segmentstat.zimmeranz)
                        w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(segmentstat.budzimmeranz)

                    if w1a:
                        w1a.saldo =  to_decimal(w1a.saldo) + to_decimal(segmentstat.persanz) +\
                                segmentstat.kind1 + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w1a.budget =  to_decimal(w1a.budget) + to_decimal(segmentstat.budpersanz)

                        if d_flag:
                            w1a.mon_saldo[get_day(segmentstat.datum) - 1] = w1a.mon_saldo[get_day(segmentstat.datum) - 1] + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis

                        if dbudget_flag:
                            w1a.mon_budget[get_day(segmentstat.datum) - 1] = w1a.mon_budget[get_day(segmentstat.datum) - 1] + segmentstat.budpersanz

                        if ytd_flag:
                            w1a.ytd_saldo =  to_decimal(w1a.ytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                            w1a.ytd_budget =  to_decimal(w1a.ytd_budget) + to_decimal(segmentstat.budpersanz)

            if lytd_flag or lmtd_flag:

                if lytd_flag:
                    datum2 = ljan1
                else:
                    datum2 = lfrom_date

                for segmentstat in db_session.query(Segmentstat).filter(
                         (Segmentstat.datum >= datum2) & (Segmentstat.datum <= lto_date) & (Segmentstat.segmentcode == segment.segmentcode)).order_by(Segmentstat._recid).all():
                    frate =  to_decimal("1")

                    if foreign_flag:
                        find_exrate(segmentstat.datum)

                        if exrate:
                            frate =  to_decimal(exrate.betrag)

                    if segmentstat.datum < lfrom_date:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(segmentstat.zimmeranz)
                        w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(segmentstat.budzimmeranz)

                        if w1a:
                            w1a.lytd_saldo =  to_decimal(w1a.lytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                            w1a.lytd_budget =  to_decimal(w1a.lytd_budget) + to_decimal(segmentstat.budpersanz)
                    else:
                        dlmtd_flag = (get_month(segmentstat.datum) == get_month(to_date)) and (get_year(segmentstat.datum) == get_year(to_date) - 1)

                        if dlmtd_flag:
                            w1.mon_lmtd[get_day(segmentstat.datum) - 1] = w1.mon_lmtd[get_day(segmentstat.datum) - 1] + segmentstat.zimmeranz
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(segmentstat.zimmeranz)

                        if lytd_flag:
                            w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(segmentstat.zimmeranz)
                        w1.ly_budget =  to_decimal(w1.ly_budget) + to_decimal(segmentstat.budzimmeranz)

                        if lytd_flag:
                            w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(segmentstat.budzimmeranz)

                        if w1a:

                            if dlmtd_flag:
                                w1a.mon_lmtd[get_day(segmentstat.datum) - 1] = w1a.mon_lmtd[get_day(segmentstat.datum) - 1] + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
                            w1a.lastyr =  to_decimal(w1a.lastyr) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                            w1a.ly_budget =  to_decimal(w1a.ly_budget) + to_decimal(segmentstat.budpersanz)

                            if lytd_flag:
                                w1a.lytd_saldo =  to_decimal(w1a.lytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                                w1a.lytd_budget =  to_decimal(w1a.lytd_budget) + to_decimal(segmentstat.budpersanz)

            if pmtd_flag:

                for segmentstat in db_session.query(Segmentstat).filter(
                         (Segmentstat.datum >= pfrom_date) & (Segmentstat.datum <= pto_date) & (Segmentstat.segmentcode == segment.segmentcode)).order_by(Segmentstat._recid).all():
                    frate =  to_decimal("1")

                    if foreign_flag:
                        find_exrate(segmentstat.datum)

                        if exrate:
                            frate =  to_decimal(exrate.betrag)
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(segmentstat.zimmeranz)
                    w1.lm_budget =  to_decimal(w1.lm_budget) + to_decimal(segmentstat.budzimmeranz)

                    if w1a:
                        w1a.lastmon =  to_decimal(w1a.lastmon) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w1a.lm_budget =  to_decimal(w1a.lm_budget) + to_decimal(segmentstat.budpersanz)


            if lytoday_flag:

                for segmentstat in db_session.query(Segmentstat).filter(
                         (Segmentstat.datum == lytoday) & (Segmentstat.segmentcode == segment.segmentcode)).order_by(Segmentstat._recid).all():
                    frate =  to_decimal("1")

                    if foreign_flag:
                        find_exrate(segmentstat.datum)

                        if exrate:
                            frate =  to_decimal(exrate.betrag)
                    w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(segmentstat.zimmeranz)

                    if w1a:
                        w1a.lytoday =  to_decimal(w1a.lytoday) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)

        w1.done = True

        if w1a:
            w1a.done = True


    def fill_new_rmocc(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        curr_date:date = None
        datum1:date = None
        datum2:date = None
        d_flag:bool = False
        dbudget_flag:bool = False
        dlmtd_flag:bool = False
        frate1:Decimal = to_decimal("0.0")

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.datum >= datum1) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.segmentcode).all():
            d_flag = (get_month(genstat.datum) == get_month(to_date)) and (get_year(genstat.datum) == get_year(to_date))

            if genstat.datum == to_date:
                w1.tday =  to_decimal(w1.tday) + to_decimal("1")

            if get_month(genstat.datum) == get_month(to_date) and get_year(genstat.datum) == get_year(to_date):
                w1.saldo =  to_decimal(w1.saldo) + to_decimal("1")

            if genstat.datum < from_date:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal("1")

            if ytd_flag:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal("1")

            if d_flag:
                w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + 1

        for segment in db_session.query(Segment).order_by(Segment._recid).all():

            for segmentstat in db_session.query(Segmentstat).filter(
                     (Segmentstat.datum >= datum1) & (Segmentstat.datum <= to_date) & (Segmentstat.segmentcode == segment.segmentcode)).order_by(Segmentstat._recid).all():
                frate =  to_decimal("1")

                if foreign_flag:
                    find_exrate(segmentstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)
                dbudget_flag = (get_month(segmentstat.datum) == get_month(to_date)) and (get_year(segmentstat.datum) == get_year(to_date))

                if segmentstat.datum == to_date:
                    w1.tbudget =  to_decimal(w1.tbudget) + to_decimal(segmentstat.budzimmeranz)

                if segmentstat.datum < from_date:
                    w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(segmentstat.budzimmeranz)

                if get_month(segmentstat.datum) == get_month(to_date) and get_year(segmentstat.datum) == get_year(to_date):
                    w1.budget =  to_decimal(w1.budget) + to_decimal(segmentstat.budzimmeranz)

                if ytd_flag:
                    w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(segmentstat.budzimmeranz)

                if dbudget_flag:
                    w1.mon_budget[get_day(segmentstat.datum) - 1] = w1.mon_budget[get_day(segmentstat.datum) - 1] + segmentstat.budzimmeranz

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum2 = ljan1
            else:
                datum2 = lfrom_date

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum >= datum2) & (Genstat.datum <= lto_date) & (Genstat.resstatus != 13) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.segmentcode).all():

                if genstat.datum < lfrom_date:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal("1")
                else:
                    dlmtd_flag = (get_month(genstat.datum) == get_month(to_date)) and (get_year(genstat.datum) == get_year(to_date) - 1)

                    if dlmtd_flag:
                        w1.mon_lmtd[get_day(genstat.datum) - 1] = w1.mon_lmtd[get_day(genstat.datum) - 1] + 1
                    w1.lastyr =  to_decimal(w1.lastyr) + to_decimal("1")

                    if lytd_flag:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal("1")

            for segmentstat in db_session.query(Segmentstat).filter(
                     (Segmentstat.datum >= datum2) & (Segmentstat.datum <= lto_date) & (Segmentstat.segmentcode == segment.segmentcode)).order_by(Segmentstat._recid).all():
                frate =  to_decimal("1")

                if foreign_flag:
                    find_exrate(segmentstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)

                if segmentstat.datum < lfrom_date:
                    w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(segmentstat.budzimmeranz)
                else:
                    w1.ly_budget =  to_decimal(w1.ly_budget) + to_decimal(segmentstat.budzimmeranz)

                    if lytd_flag:
                        w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(segmentstat.budzimmeranz)

        if pmtd_flag:

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum >= pfrom_date) & (Genstat.datum <= pto_date) & (Genstat.resstatus != 13) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.segmentcode).all():
                w1.lastmon =  to_decimal(w1.lastmon) + to_decimal("1")

            for segmentstat in db_session.query(Segmentstat).filter(
                     (Segmentstat.datum >= pfrom_date) & (Segmentstat.datum <= pto_date) & (Segmentstat.segmentcode == segment.segmentcode)).order_by(Segmentstat._recid).all():
                frate =  to_decimal("1")

                if foreign_flag:
                    find_exrate(segmentstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)
                w1.lm_budget =  to_decimal(w1.lm_budget) + to_decimal(segmentstat.budzimmeranz)

        if lytoday_flag:

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum == lytoday) & (Genstat.resstatus != 13) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.segmentcode).all():
                w1.lytoday =  to_decimal(w1.lytoday) + to_decimal("1")
        w1.done = True


    def fill_gledger(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        W11 = W1
        w11_list = w1_list
        W12 = W1
        w12_list = w1_list

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        for uebertrag in db_session.query(Uebertrag).filter(
                 (Uebertrag.datum >= from_date - timedelta(days=1)) & (Uebertrag.datum <= to_date - timedelta(days=1))).order_by(Uebertrag.datum).all():
            w1.mon_saldo[get_day(uebertrag.datum + 1) - 1] = uebertrag.betrag

        uebertrag = get_cache (Uebertrag, {"datum": [(eq, to_date - timedelta(days=1))]})

        if uebertrag:
            w1.tday =  to_decimal(uebertrag.betrag)
            w1.done = True


    def fill_comproomsnew(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        mm:int = 0
        d_flag:bool = False

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date
        mm = get_month(to_date)

        genstat_obj_list = {}
        genstat = Genstat()
        segment = Segment()
        for genstat.datum, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.gratis, genstat.logis, genstat.segmentcode, genstat.gastnr, genstat.zinr, genstat._recid, segment.segmentcode, segment.segmentgrup, segment.betriebsnr, segment._recid in db_session.query(Genstat.datum, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.gratis, Genstat.logis, Genstat.segmentcode, Genstat.gastnr, Genstat.zinr, Genstat._recid, Segment.segmentcode, Segment.segmentgrup, Segment.betriebsnr, Segment._recid).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).filter(
                 (Genstat.datum >= datum1) & (Genstat.datum <= to_date) & (Genstat.zipreis == 0) & (Genstat.gratis != 0) & (Genstat.resstatus == 6)).order_by(Genstat._recid).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            if segment.betriebsnr == 0:
                d_flag = (get_month(genstat.datum) == get_month(to_date)) and (get_year(genstat.datum) == get_year(to_date))

                if d_flag:
                    w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + 1

                if genstat.datum == to_date:
                    w1.tday =  to_decimal(w1.tday) + to_decimal("1")

                if get_month(genstat.datum) == mm:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal("1")

                if ytd_flag:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal("1")

        if (lytd_flag or lmtd_flag):

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date
            mm = get_month(lto_date)

            genstat_obj_list = {}
            genstat = Genstat()
            segment = Segment()
            for genstat.datum, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.gratis, genstat.logis, genstat.segmentcode, genstat.gastnr, genstat.zinr, genstat._recid, segment.segmentcode, segment.segmentgrup, segment.betriebsnr, segment._recid in db_session.query(Genstat.datum, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.gratis, Genstat.logis, Genstat.segmentcode, Genstat.gastnr, Genstat.zinr, Genstat._recid, Segment.segmentcode, Segment.segmentgrup, Segment.betriebsnr, Segment._recid).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).filter(
                     (Genstat.datum >= datum1) & (Genstat.datum <= lto_date) & (Genstat.zipreis == 0) & (Genstat.gratis != 0) & (Genstat.resstatus == 6)).order_by(Genstat._recid).all():
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True

                if segment.betriebsnr == 0:

                    if get_month(genstat.datum) == mm:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal("1")
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal("1")

        if pmtd_flag:
            mm = get_month(pto_date)

            genstat_obj_list = {}
            genstat = Genstat()
            segment = Segment()
            for genstat.datum, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.gratis, genstat.logis, genstat.segmentcode, genstat.gastnr, genstat.zinr, genstat._recid, segment.segmentcode, segment.segmentgrup, segment.betriebsnr, segment._recid in db_session.query(Genstat.datum, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.gratis, Genstat.logis, Genstat.segmentcode, Genstat.gastnr, Genstat.zinr, Genstat._recid, Segment.segmentcode, Segment.segmentgrup, Segment.betriebsnr, Segment._recid).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).filter(
                     (Genstat.datum >= pfrom_date) & (Genstat.datum <= pto_date) & (Genstat.zipreis == 0) & (Genstat.gratis != 0) & (Genstat.resstatus == 6)).order_by(Genstat._recid).all():
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True

                if segment.betriebsnr == 0:

                    if get_month(genstat.datum) == mm:
                        w1.lastmon =  to_decimal(w1.lastmon) + to_decimal("1")


    def fill_comprooms(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        datum2:date = None
        curr_date:date = None
        d_flag:bool = False

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for segment in db_session.query(Segment).filter(
                 (Segment.betriebsnr == 0)).order_by(Segment._recid).all():

            if (get_day(to_date) == 31 and get_month(to_date) != 8 and get_month(to_date) != 1) or (get_day(to_date) == 30 and get_month(to_date) == 3) or (get_day(date_mdy(3, 1, get_year(to_date)) - 1) == 28 and get_month(to_date) == 3 and get_day(to_date) == 29):
                w1.lm_today =  to_decimal("0")
            else:

                if get_month(to_date) == 1:
                    curr_date = date_mdy(12, get_day(to_date) , get_year(to_date) - timedelta(days=1))
                else:
                    curr_date = date_mdy(get_month(to_date) - timedelta(days=1, get_day(to_date) , get_year(to_date)))

                segmentstat = get_cache (Segmentstat, {"datum": [(eq, curr_date)],"segmentcode": [(eq, segment.segmentcode)],"betriebsnr": [(gt, 0)]})

                if segmentstat:
                    frate =  to_decimal("1")

                    if foreign_flag:
                        find_exrate(segmentstat.datum)

                        if exrate:
                            frate =  to_decimal(exrate.betrag)
                    w1.lm_today =  to_decimal(w1.lm_today) + to_decimal(segmentstat.betriebsnr)

            for segmentstat in db_session.query(Segmentstat).filter(
                     (Segmentstat.datum >= datum1) & (Segmentstat.datum <= to_date) & (Segmentstat.segmentcode == segment.segmentcode) & (Segmentstat.betriebsnr > 0)).order_by(Segmentstat._recid).all():
                frate =  to_decimal("1")

                if foreign_flag:
                    find_exrate(segmentstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)
                d_flag = (get_month(segmentstat.datum) == get_month(to_date)) and (get_year(segmentstat.datum) == get_year(to_date))

                if segmentstat.datum == to_date - timedelta(days=1):
                    w1.yesterday =  to_decimal(w1.yesterday) + to_decimal(segmentstat.betriebsnr)

                if segmentstat.datum == to_date:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(segmentstat.betriebsnr)

                if segmentstat.datum < from_date:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(segmentstat.betriebsnr)
                else:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(segmentstat.betriebsnr)

                    if d_flag:
                        w1.mon_saldo[get_day(segmentstat.datum) - 1] = w1.mon_saldo[get_day(segmentstat.datum) - 1] + segmentstat.betriebsnr

                    if ytd_flag:
                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(segmentstat.betriebsnr)

            if lytd_flag or lmtd_flag:

                if lytd_flag:
                    datum2 = ljan1
                else:
                    datum2 = lfrom_date

                for segmentstat in db_session.query(Segmentstat).filter(
                         (Segmentstat.datum >= datum2) & (Segmentstat.datum <= lto_date) & (Segmentstat.segmentcode == segment.segmentcode)).order_by(Segmentstat._recid).all():

                    if foreign_flag:
                        find_exrate(segmentstat.datum)

                        if exrate:
                            frate =  to_decimal(exrate.betrag)

                    if segmentstat.datum < lfrom_date:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(segmentstat.betriebsnr)
                    else:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(segmentstat.betriebsnr)

                        if lytd_flag:
                            w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(segmentstat.betriebsnr)

            if pmtd_flag:

                for segmentstat in db_session.query(Segmentstat).filter(
                         (Segmentstat.datum >= pfrom_date) & (Segmentstat.datum <= pto_date) & (Segmentstat.segmentcode == segment.segmentcode)).order_by(Segmentstat._recid).all():
                    frate =  to_decimal("1")

                    if foreign_flag:
                        find_exrate(segmentstat.datum)

                        if exrate:
                            frate =  to_decimal(exrate.betrag)
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(segmentstat.betriebsnr)


            if lytoday_flag:

                for segmentstat in db_session.query(Segmentstat).filter(
                         (Segmentstat.datum == lytoday) & (Segmentstat.segmentcode == segment.segmentcode)).order_by(Segmentstat._recid).all():
                    frate =  to_decimal("1")

                    if foreign_flag:
                        find_exrate(segmentstat.datum)

                        if exrate:
                            frate =  to_decimal(exrate.betrag)
                    w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(segmentstat.betriebsnr)

        w1.done = True


    def fill_rmocc_perc(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        W11 = W1
        w11_list = w1_list
        W12 = W1
        w12_list = w1_list

        w11 = query(w11_list, filters=(lambda w11: w11.main_code == 805), first=True)

        if not w11:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Variable for Room Availablity not defined,", lvcarea, "") + chr_unicode(10) + translateExtended ("which is necessary for calculating of room occupancy.", lvcarea, "")
            prog_error = True
            error_nr = - 1

            return

        w12 = query(w12_list, filters=(lambda w12: w12.main_code == 806), first=True)

        if not w12:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Variable for Occupied Rooms not defined,", lvcarea, "") + chr_unicode(10) + translateExtended ("which is necessary for calculating of room occupancy in %.", lvcarea, "")
            prog_error = True
            error_nr = - 1

            return

        if not w11.done:
            fill_rmavail(w11._recid)

        if not w12.done:
            fill_new_rmocc(w12._recid)

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        if w11.tday != 0:
            w1.tday =  to_decimal(w12.tday) / to_decimal(w11.tday) * to_decimal("100")

        if w11.saldo != 0:
            w1.saldo =  to_decimal(w12.saldo) / to_decimal(w11.saldo) * to_decimal("100")

        if w11.ytd_saldo != 0:
            w1.ytd_saldo =  to_decimal(w12.ytd_saldo) / to_decimal(w11.ytd_saldo) * to_decimal("100")

        if w11.lytd_saldo != 0:
            w1.lytd_saldo =  to_decimal(w12.lytd_saldo) / to_decimal(w11.lytd_saldo) * to_decimal("100")

        if w11.lastyr != 0:
            w1.lastyr =  to_decimal(w12.lastyr) / to_decimal(w11.lastyr) * to_decimal("100")

        if w11.lastmon != 0:
            w1.lastmon =  to_decimal(w12.lastmon) / to_decimal(w11.lastmon) * to_decimal("100")

        if w11.lytoday != 0:
            w1.lytoday =  to_decimal(w12.lytoday) / to_decimal(w11.lytoday) * to_decimal("100")
        w1.done = True


    def fill_docc_perc(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        W11 = W1
        w11_list = w1_list
        W12 = W1
        w12_list = w1_list

        w11 = query(w11_list, filters=(lambda w11: w11.main_code == 806), first=True)

        if not w11:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Variable for Occupied Rooms not defined,", lvcarea, "") + chr_unicode(10) + translateExtended ("which is necessary for calculating of double room occupancy.", lvcarea, "")
            prog_error = True
            error_nr = - 1

            return

        w12 = query(w12_list, filters=(lambda w12: w12.main_code == 810), first=True)

        if not w12:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Variable for Occupied Persons not defined,", lvcarea, "") + chr_unicode(10) + translateExtended ("which is necessary for calculating of double room occupancy.", lvcarea, "")
            prog_error = True
            error_nr = - 1

            return

        if not w11.done:
            fill_new_rmocc(w11._recid)

        if not w12.done:
            fill_persocc(w12._recid)

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        if w11.tday != 0:
            w1.tday = ( to_decimal(w12.tday) - to_decimal(w11.tday)) / to_decimal(w11.tday) * to_decimal("100")

        if w11.saldo != 0:
            w1.saldo = ( to_decimal(w12.saldo) - to_decimal(w11.saldo)) / to_decimal(w11.saldo) * to_decimal("100")

        if w11.ytd_saldo != 0:
            w1.ytd_saldo = ( to_decimal(w12.ytd_saldo) - to_decimal(w11.ytd_saldo)) / to_decimal(w11.ytd_saldo) * to_decimal("100")

        if w11.lytd_saldo != 0:
            w1.lytd_saldo = ( to_decimal(w12.lytd_saldo) - to_decimal(w11.lytd_saldo)) / to_decimal(w11.lytd_saldo) * to_decimal("100")

        if w11.lastyr != 0:
            w1.lastyr = ( to_decimal(w12.lastyr) - to_decimal(w11.lastyr)) / to_decimal(w11.lastyr) * to_decimal("100")

        if w11.lastmon != 0:
            w1.lastmon = ( to_decimal(w12.lastmon) - to_decimal(w11.lastmon)) / to_decimal(w11.lastmon) * to_decimal("100")

        if w11.lytoday != 0:
            w1.lytoday = ( to_decimal(w12.lytoday) - to_decimal(w11.lytoday)) / to_decimal(w11.lytoday) * to_decimal("100")
        w1.done = True


    def fill_fbcost(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        datum2:date = None
        cost:Decimal = to_decimal("0.0")

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        artikel = get_cache (Artikel, {"artnr": [(eq, w1.artnr)],"departement": [(eq, w1.dept)]})

        if not artikel:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Article for cost-variable not found : ", lvcarea, "") + w1.varname
            error_nr = -1

            return

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        h_umsatz_obj_list = {}
        h_umsatz = H_umsatz()
        h_artikel = H_artikel()
        for h_umsatz.anzahl, h_umsatz.betrag, h_umsatz.nettobetrag, h_umsatz.datum, h_umsatz.artnr, h_umsatz.departement, h_umsatz.epreis, h_umsatz._recid, h_artikel.departement, h_artikel.artnr, h_artikel.service_code, h_artikel.mwst_code, h_artikel.prozent, h_artikel.artnrfront, h_artikel.artart, h_artikel._recid in db_session.query(H_umsatz.anzahl, H_umsatz.betrag, H_umsatz.nettobetrag, H_umsatz.datum, H_umsatz.artnr, H_umsatz.departement, H_umsatz.epreis, H_umsatz._recid, H_artikel.departement, H_artikel.artnr, H_artikel.service_code, H_artikel.mwst_code, H_artikel.prozent, H_artikel.artnrfront, H_artikel.artart, H_artikel._recid).join(H_artikel,(H_artikel.artnr == H_umsatz.artnr) & (H_artikel.departement == H_umsatz.departement) & (H_artikel.artnrfront == artikel.artnr)).filter(
                 (H_umsatz.datum >= datum1) & (H_umsatz.datum <= to_date) & (H_umsatz.departement == w1.dept)).order_by(H_umsatz._recid).all():
            if h_umsatz_obj_list.get(h_umsatz._recid):
                continue
            else:
                h_umsatz_obj_list[h_umsatz._recid] = True


            cost = cal_fbcost(h_umsatz.artnr, h_umsatz.departement, h_umsatz.datum)

            if h_umsatz.datum == to_date:
                w1.tday =  to_decimal(w1.tday) + to_decimal(cost)

            if h_umsatz.datum < from_date:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(cost)
            else:
                w1.saldo =  to_decimal(w1.saldo) + to_decimal(cost)

                if ytd_flag:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(cost)

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            h_umsatz_obj_list = {}
            h_umsatz = H_umsatz()
            h_artikel = H_artikel()
            for h_umsatz.anzahl, h_umsatz.betrag, h_umsatz.nettobetrag, h_umsatz.datum, h_umsatz.artnr, h_umsatz.departement, h_umsatz.epreis, h_umsatz._recid, h_artikel.departement, h_artikel.artnr, h_artikel.service_code, h_artikel.mwst_code, h_artikel.prozent, h_artikel.artnrfront, h_artikel.artart, h_artikel._recid in db_session.query(H_umsatz.anzahl, H_umsatz.betrag, H_umsatz.nettobetrag, H_umsatz.datum, H_umsatz.artnr, H_umsatz.departement, H_umsatz.epreis, H_umsatz._recid, H_artikel.departement, H_artikel.artnr, H_artikel.service_code, H_artikel.mwst_code, H_artikel.prozent, H_artikel.artnrfront, H_artikel.artart, H_artikel._recid).join(H_artikel,(H_artikel.artnr == H_umsatz.artnr) & (H_artikel.departement == H_umsatz.departement) & (H_artikel.artnrfront == artikel.artnr)).filter(
                     (H_umsatz.datum >= datum1) & (H_umsatz.datum <= lto_date) & (H_umsatz.departement == w1.dept)).order_by(H_umsatz._recid).all():
                if h_umsatz_obj_list.get(h_umsatz._recid):
                    continue
                else:
                    h_umsatz_obj_list[h_umsatz._recid] = True


                cost = cal_fbcost(h_umsatz.artnr, h_umsatz.departement, h_umsatz.datum)

                if h_umsatz.datum < lfrom_date:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(cost)
                else:
                    w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(cost)

                    if lytd_flag:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(cost)

        if pmtd_flag:

            h_umsatz_obj_list = {}
            h_umsatz = H_umsatz()
            h_artikel = H_artikel()
            for h_umsatz.anzahl, h_umsatz.betrag, h_umsatz.nettobetrag, h_umsatz.datum, h_umsatz.artnr, h_umsatz.departement, h_umsatz.epreis, h_umsatz._recid, h_artikel.departement, h_artikel.artnr, h_artikel.service_code, h_artikel.mwst_code, h_artikel.prozent, h_artikel.artnrfront, h_artikel.artart, h_artikel._recid in db_session.query(H_umsatz.anzahl, H_umsatz.betrag, H_umsatz.nettobetrag, H_umsatz.datum, H_umsatz.artnr, H_umsatz.departement, H_umsatz.epreis, H_umsatz._recid, H_artikel.departement, H_artikel.artnr, H_artikel.service_code, H_artikel.mwst_code, H_artikel.prozent, H_artikel.artnrfront, H_artikel.artart, H_artikel._recid).join(H_artikel,(H_artikel.artnr == H_umsatz.artnr) & (H_artikel.departement == H_umsatz.departement) & (H_artikel.artnrfront == artikel.artnr)).filter(
                     (H_umsatz.datum >= pfrom_date) & (H_umsatz.datum <= pto_date) & (H_umsatz.departement == w1.dept)).order_by(H_umsatz._recid).all():
                if h_umsatz_obj_list.get(h_umsatz._recid):
                    continue
                else:
                    h_umsatz_obj_list[h_umsatz._recid] = True


                cost = cal_fbcost(h_umsatz.artnr, h_umsatz.departement, h_umsatz.datum)
                w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(cost)


        if lytoday_flag:

            h_umsatz_obj_list = {}
            h_umsatz = H_umsatz()
            h_artikel = H_artikel()
            for h_umsatz.anzahl, h_umsatz.betrag, h_umsatz.nettobetrag, h_umsatz.datum, h_umsatz.artnr, h_umsatz.departement, h_umsatz.epreis, h_umsatz._recid, h_artikel.departement, h_artikel.artnr, h_artikel.service_code, h_artikel.mwst_code, h_artikel.prozent, h_artikel.artnrfront, h_artikel.artart, h_artikel._recid in db_session.query(H_umsatz.anzahl, H_umsatz.betrag, H_umsatz.nettobetrag, H_umsatz.datum, H_umsatz.artnr, H_umsatz.departement, H_umsatz.epreis, H_umsatz._recid, H_artikel.departement, H_artikel.artnr, H_artikel.service_code, H_artikel.mwst_code, H_artikel.prozent, H_artikel.artnrfront, H_artikel.artart, H_artikel._recid).join(H_artikel,(H_artikel.artnr == H_umsatz.artnr) & (H_artikel.departement == H_umsatz.departement) & (H_artikel.artnrfront == artikel.artnr)).filter(
                     (H_umsatz.datum == lytoday) & (H_umsatz.departement == w1.dept)).order_by(H_umsatz._recid).all():
                if h_umsatz_obj_list.get(h_umsatz._recid):
                    continue
                else:
                    h_umsatz_obj_list[h_umsatz._recid] = True


                cost = cal_fbcost(h_umsatz.artnr, h_umsatz.departement, h_umsatz.datum)
                w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(cost)

        w1.done = True


    def fill_sgfb(rec_w1:int, main_nr:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        datum2:date = None
        cost:Decimal = to_decimal("0.0")
        sg_dept:int = 0
        subgr:int = 0
        vat:Decimal = to_decimal("0.0")
        serv:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return
        sg_dept = to_int(substring(w1.s_artnr, 0, 2))
        subgr = to_int(substring(w1.s_artnr, 2))

        wgrpdep = get_cache (Wgrpdep, {"zknr": [(eq, subgr)],"departement": [(eq, sg_dept)]})

        if not wgrpdep:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("SubGroup not found : ", lvcarea, "") + w1.varname
            error_nr = -1

            return

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        h_umsatz_obj_list = {}
        h_umsatz = H_umsatz()
        h_artikel = H_artikel()
        for h_umsatz.anzahl, h_umsatz.betrag, h_umsatz.nettobetrag, h_umsatz.datum, h_umsatz.artnr, h_umsatz.departement, h_umsatz.epreis, h_umsatz._recid, h_artikel.departement, h_artikel.artnr, h_artikel.service_code, h_artikel.mwst_code, h_artikel.prozent, h_artikel.artnrfront, h_artikel.artart, h_artikel._recid in db_session.query(H_umsatz.anzahl, H_umsatz.betrag, H_umsatz.nettobetrag, H_umsatz.datum, H_umsatz.artnr, H_umsatz.departement, H_umsatz.epreis, H_umsatz._recid, H_artikel.departement, H_artikel.artnr, H_artikel.service_code, H_artikel.mwst_code, H_artikel.prozent, H_artikel.artnrfront, H_artikel.artart, H_artikel._recid).join(H_artikel,(H_artikel.artnr == H_umsatz.artnr) & (H_artikel.departement == H_umsatz.departement) & (H_artikel.zwkum == subgr) & (H_artikel.artart == 0)).filter(
                 (H_umsatz.datum >= datum1) & (H_umsatz.datum <= to_date) & (H_umsatz.departement == sg_dept)).order_by(H_umsatz._recid).all():
            if h_umsatz_obj_list.get(h_umsatz._recid):
                continue
            else:
                h_umsatz_obj_list[h_umsatz._recid] = True


            serv, vat = get_output(calc_servvat(h_artikel.departement, h_artikel.artnr, datum, h_artikel.service_code, h_artikel.mwst_code))
            fact = ( to_decimal(1.00) + to_decimal(serv) + to_decimal(vat))

            if h_umsatz.datum == to_date:

                if main_nr == 9985:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(h_umsatz.betrag) / to_decimal(fact)

                elif main_nr == 9986:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(h_umsatz.anzahl)

            if get_month(h_umsatz.datum) == get_month(to_date):

                if main_nr == 9985:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_umsatz.betrag) / to_decimal(fact)

                elif main_nr == 9986:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_umsatz.anzahl)

            if ytd_flag:

                if main_nr == 9985:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_umsatz.betrag) / to_decimal(fact)

                elif main_nr == 9986:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_umsatz.anzahl)

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            h_umsatz_obj_list = {}
            h_umsatz = H_umsatz()
            h_artikel = H_artikel()
            for h_umsatz.anzahl, h_umsatz.betrag, h_umsatz.nettobetrag, h_umsatz.datum, h_umsatz.artnr, h_umsatz.departement, h_umsatz.epreis, h_umsatz._recid, h_artikel.departement, h_artikel.artnr, h_artikel.service_code, h_artikel.mwst_code, h_artikel.prozent, h_artikel.artnrfront, h_artikel.artart, h_artikel._recid in db_session.query(H_umsatz.anzahl, H_umsatz.betrag, H_umsatz.nettobetrag, H_umsatz.datum, H_umsatz.artnr, H_umsatz.departement, H_umsatz.epreis, H_umsatz._recid, H_artikel.departement, H_artikel.artnr, H_artikel.service_code, H_artikel.mwst_code, H_artikel.prozent, H_artikel.artnrfront, H_artikel.artart, H_artikel._recid).join(H_artikel,(H_artikel.artnr == H_umsatz.artnr) & (H_artikel.departement == H_umsatz.departement) & (H_artikel.zwkum == subgr) & (H_artikel.artart == 0)).filter(
                     (H_umsatz.datum >= datum1) & (H_umsatz.datum <= lto_date) & (H_umsatz.departement == sg_dept)).order_by(H_umsatz._recid).all():
                if h_umsatz_obj_list.get(h_umsatz._recid):
                    continue
                else:
                    h_umsatz_obj_list[h_umsatz._recid] = True


                cost = cal_fbcost(h_umsatz.artnr, h_umsatz.departement, h_umsatz.datum)

                if h_umsatz.datum < lfrom_date:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(cost)
                else:
                    w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(cost)

                    if lytd_flag:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(cost)

        if pmtd_flag:

            h_umsatz_obj_list = {}
            h_umsatz = H_umsatz()
            h_artikel = H_artikel()
            for h_umsatz.anzahl, h_umsatz.betrag, h_umsatz.nettobetrag, h_umsatz.datum, h_umsatz.artnr, h_umsatz.departement, h_umsatz.epreis, h_umsatz._recid, h_artikel.departement, h_artikel.artnr, h_artikel.service_code, h_artikel.mwst_code, h_artikel.prozent, h_artikel.artnrfront, h_artikel.artart, h_artikel._recid in db_session.query(H_umsatz.anzahl, H_umsatz.betrag, H_umsatz.nettobetrag, H_umsatz.datum, H_umsatz.artnr, H_umsatz.departement, H_umsatz.epreis, H_umsatz._recid, H_artikel.departement, H_artikel.artnr, H_artikel.service_code, H_artikel.mwst_code, H_artikel.prozent, H_artikel.artnrfront, H_artikel.artart, H_artikel._recid).join(H_artikel,(H_artikel.artnr == H_umsatz.artnr) & (H_artikel.departement == H_umsatz.departement) & (H_artikel.zwkum == subgr) & (H_artikel.artart == 0)).filter(
                     (H_umsatz.datum >= pfrom_date) & (H_umsatz.datum <= pto_date) & (H_umsatz.departement == sg_dept)).order_by(H_umsatz._recid).all():
                if h_umsatz_obj_list.get(h_umsatz._recid):
                    continue
                else:
                    h_umsatz_obj_list[h_umsatz._recid] = True


                cost = cal_fbcost(h_umsatz.artnr, h_umsatz.departement, h_umsatz.datum)
                w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(cost)


        if lytoday_flag:

            h_umsatz_obj_list = {}
            h_umsatz = H_umsatz()
            h_artikel = H_artikel()
            for h_umsatz.anzahl, h_umsatz.betrag, h_umsatz.nettobetrag, h_umsatz.datum, h_umsatz.artnr, h_umsatz.departement, h_umsatz.epreis, h_umsatz._recid, h_artikel.departement, h_artikel.artnr, h_artikel.service_code, h_artikel.mwst_code, h_artikel.prozent, h_artikel.artnrfront, h_artikel.artart, h_artikel._recid in db_session.query(H_umsatz.anzahl, H_umsatz.betrag, H_umsatz.nettobetrag, H_umsatz.datum, H_umsatz.artnr, H_umsatz.departement, H_umsatz.epreis, H_umsatz._recid, H_artikel.departement, H_artikel.artnr, H_artikel.service_code, H_artikel.mwst_code, H_artikel.prozent, H_artikel.artnrfront, H_artikel.artart, H_artikel._recid).join(H_artikel,(H_artikel.artnr == H_umsatz.artnr) & (H_artikel.departement == H_umsatz.departement) & (H_artikel.zwkum == subgr) & (H_artikel.artart == 0)).filter(
                     (H_umsatz.datum >= lytoday) & (H_umsatz.departement == sg_dept)).order_by(H_umsatz._recid).all():
                if h_umsatz_obj_list.get(h_umsatz._recid):
                    continue
                else:
                    h_umsatz_obj_list[h_umsatz._recid] = True


                cost = cal_fbcost(h_umsatz.artnr, h_umsatz.departement, h_umsatz.datum)
                w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(cost)

        w1.done = True


    def fill_quantity(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        datum2:date = None
        curr_date:date = None
        d_flag:bool = False
        dlmtd_flag:bool = False

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        artikel = get_cache (Artikel, {"artnr": [(eq, w1.artnr)],"departement": [(eq, w1.dept)]})

        if not artikel:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("No such article number : ", lvcarea, "") + to_string(w1.artnr) + " " + translateExtended ("dept", lvcarea, "") + " " + to_string(w1.dept)

            return

        if (get_day(to_date) == 31 and get_month(to_date) != 8 and get_month(to_date) != 1) or (get_day(to_date) == 30 and get_month(to_date) == 3) or (get_day(date_mdy(3, 1, get_year(to_date)) - 1) == 28 and get_month(to_date) == 3 and get_day(to_date) == 29):
            w1.lm_today =  to_decimal("0")
        else:

            if get_month(to_date) == 1:
                curr_date = date_mdy(12, get_day(to_date) , get_year(to_date) - timedelta(days=1))
            else:
                curr_date = date_mdy(get_month(to_date) - timedelta(days=1, get_day(to_date) , get_year(to_date)))

            umsatz = get_cache (Umsatz, {"datum": [(eq, curr_date)],"artnr": [(eq, w1.artnr)],"departement": [(eq, w1.dept)]})

            if umsatz:
                w1.lm_today =  to_decimal(umsatz.anzahl)

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for umsatz in db_session.query(Umsatz).filter(
                 (Umsatz.datum >= datum1) & (Umsatz.datum <= to_date) & (Umsatz.artnr == w1.artnr) & (Umsatz.departement == w1.dept)).order_by(Umsatz._recid).all():
            d_flag = (get_month(umsatz.datum) == get_month(to_date)) and (get_year(umsatz.datum) == get_year(to_date))

            if umsatz.datum == to_date - timedelta(days=1):
                w1.yesterday =  to_decimal(w1.yesterday) + to_decimal(umsatz.anzahl)

            if umsatz.datum == to_date:
                w1.tday =  to_decimal(w1.tday) + to_decimal(umsatz.anzahl)

            if umsatz.datum < from_date:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(umsatz.anzahl)
            else:
                w1.saldo =  to_decimal(w1.saldo) + to_decimal(umsatz.anzahl)

                if ytd_flag:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(umsatz.anzahl)

                if d_flag:
                    w1.mon_saldo[get_day(umsatz.datum) - 1] = w1.mon_saldo[get_day(umsatz.datum) - 1] + umsatz.anzahl

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum2 = ljan1
            else:
                datum2 = lfrom_date

            for umsatz in db_session.query(Umsatz).filter(
                     (Umsatz.datum >= datum2) & (Umsatz.datum <= lto_date) & (Umsatz.artnr == w1.artnr) & (Umsatz.departement == w1.dept)).order_by(Umsatz._recid).all():

                if umsatz.datum < lfrom_date:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(umsatz.anzahl)
                else:
                    dlmtd_flag = (get_month(umsatz.datum) == get_month(to_date)) and (get_year(umsatz.datum) == get_year(to_date) - 1)

                    if dlmtd_flag:
                        w1.mon_lmtd[get_day(umsatz.datum) - 1] = w1.mon_lmtd[get_day(umsatz.datum) - 1] + umsatz.anzahl
                    w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(umsatz.anzahl)

                    if lytd_flag:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(umsatz.anzahl)

        if pmtd_flag:

            for umsatz in db_session.query(Umsatz).filter(
                     (Umsatz.datum >= pfrom_date) & (Umsatz.datum <= pto_date) & (Umsatz.artnr == w1.artnr) & (Umsatz.departement == w1.dept)).order_by(Umsatz._recid).all():
                w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(umsatz.anzahl)


        if lytoday_flag:

            umsatz = get_cache (Umsatz, {"datum": [(eq, lytoday)],"artnr": [(eq, w1.artnr)],"departement": [(eq, w1.dept)]})

            if umsatz:
                w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(umsatz.anzahl)
        w1.done = True


    def fill_revenue(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        curr_date:date = None
        datum1:date = None
        serv:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        n_betrag:Decimal = to_decimal("0.0")
        n_serv:Decimal = to_decimal("0.0")
        n_tax:Decimal = to_decimal("0.0")
        ly_betrag:Decimal = to_decimal("0.0")
        d_flag:bool = False
        dbudget_flag:bool = False
        dlmtd_flag:bool = False
        yes_serv:Decimal = to_decimal("0.0")
        yes_vat:Decimal = to_decimal("0.0")
        yes_vat2:Decimal = to_decimal("0.0")
        yes_fact:Decimal = to_decimal("0.0")
        yes_betrag:Decimal = to_decimal("0.0")
        date1:date = None
        date2:date = None
        temp_date2:date = None
        temp_curr_date:date = None
        ubuff = None
        buff_umsatz = None
        tot_betrag:Decimal = to_decimal("0.0")
        st_date:int = 0
        Ubuff =  create_buffer("Ubuff",Umsatz)
        Buff_umsatz =  create_buffer("Buff_umsatz",Umsatz)

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        artikel = get_cache (Artikel, {"artnr": [(eq, w1.artnr)],"departement": [(eq, w1.dept)]})

        if not artikel:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("No such article number : ", lvcarea, "") + to_string(w1.artnr) + " " + translateExtended ("dept", lvcarea, "") + " " + to_string(w1.dept)

            return

        if (get_day(to_date) == 31 and get_month(to_date) != 8 and get_month(to_date) != 1) or (get_day(to_date) == 30 and get_month(to_date) == 3) or (get_day(date_mdy(3, 1, get_year(to_date)) - 1) == 28 and get_month(to_date) == 3 and get_day(to_date) == 29):
            st_date = 1
            curr_date = date_mdy(get_month(to_date) , 1, get_year(to_date)) - timedelta(days=1)
            w1.lm_today =  to_decimal("0")
        else:
            st_date = 2

            if get_month(to_date) == 1:
                curr_date = date_mdy(12, get_day(to_date) , get_year(to_date) - timedelta(days=1))
            else:
                curr_date = date_mdy(get_month(to_date) - timedelta(days=1, get_day(to_date) , get_year(to_date)))

        for buff_umsatz in db_session.query(Buff_umsatz).filter(
                 (Buff_umsatz.datum >= date_mdy(get_month(curr_date) , 1, get_year(curr_date))) & (Buff_umsatz.datum <= curr_date) & (Buff_umsatz.artnr == w1.artnr) & (Buff_umsatz.departement == w1.dept)).order_by(Buff_umsatz._recid).all():
            serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, buff_umsatz.artnr, buff_umsatz.departement, buff_umsatz.datum))
            fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat) + to_decimal(vat2)
            n_betrag =  to_decimal("0")

            if foreign_flag:
                find_exrate(curr_date)

                if exrate:
                    frate =  to_decimal(exrate.betrag)
            n_betrag =  to_decimal(buff_umsatz.betrag) / to_decimal((fact) * to_decimal(frate) )
            n_serv =  to_decimal(n_betrag) * to_decimal(serv)
            n_tax =  to_decimal(n_betrag) * to_decimal(vat)

            if price_decimal == 0:
                n_betrag = to_decimal(round(n_betrag , 0))
                n_serv = to_decimal(round(n_serv , 0))
                n_tax = to_decimal(round(n_tax , 0))

            if buff_umsatz.datum == curr_date and st_date == 2:
                w1.lm_today =  to_decimal(w1.lm_today) + to_decimal(n_betrag)
                w1.lm_today_serv =  to_decimal(w1.lm_today_serv) + to_decimal(n_serv)
                w1.lm_today_tax =  to_decimal(w1.lm_today_tax) + to_decimal(n_tax)


            w1.lm_mtd =  to_decimal(w1.lm_mtd) + to_decimal(n_betrag)

        if budget_all:
            date2 = date_mdy(12, 31, get_year(to_date))

            if ytd_flag:
                date1 = jan1


            else:
                date1 = from_date
            for temp_curr_date in date_range(date1,date2) :

                budget = get_cache (Budget, {"artnr": [(eq, w1.artnr)],"departement": [(eq, w1.dept)],"datum": [(eq, temp_curr_date)]})

                if budget:

                    if temp_curr_date >= date_mdy(get_month(to_date) , 1, get_year(to_date)) and temp_curr_date <= date_mdy((get_month(to_date) + 1) , 1, get_year(to_date)) - 1:
                        w1.month_budget =  to_decimal(w1.month_budget) + to_decimal(budget.betrag)
                    w1.year_budget =  to_decimal(w1.year_budget) + to_decimal(budget.betrag)

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date
        for curr_date in date_range(datum1,to_date) :
            serv =  to_decimal("0")
            vat =  to_decimal("0")

            umsatz = get_cache (Umsatz, {"datum": [(eq, curr_date)],"artnr": [(eq, w1.artnr)],"departement": [(eq, w1.dept)]})

            if umsatz:
                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, umsatz.artnr, umsatz.departement, umsatz.datum))
            fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat) + to_decimal(vat2)
            d_flag = None != umsatz and (get_month(umsatz.datum) == get_month(to_date)) and (get_year(umsatz.datum) == get_year(to_date))
            n_betrag =  to_decimal("0")

            if umsatz:

                if foreign_flag:
                    find_exrate(curr_date)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)
                n_betrag =  to_decimal(umsatz.betrag) / to_decimal((fact) * to_decimal(frate) )
                n_serv =  to_decimal(n_betrag) * to_decimal(serv)
                n_tax =  to_decimal(n_betrag) * to_decimal(vat)

                if umsatz.artnr == 100:
                    tot_betrag =  to_decimal(tot_betrag) + to_decimal(n_betrag)

                if price_decimal == 0:
                    n_betrag = to_decimal(round(n_betrag , 0))
                    n_serv = to_decimal(round(n_serv , 0))
                    n_tax = to_decimal(round(n_tax , 0))

            if budget_flag:

                budget = get_cache (Budget, {"artnr": [(eq, w1.artnr)],"departement": [(eq, w1.dept)],"datum": [(eq, curr_date)]})
            dbudget_flag = None != budget and (get_month(budget.datum) == get_month(to_date)) and (get_year(budget.datum) == get_year(to_date))

            if dbudget_flag:
                w1.mon_budget[get_day(budget.datum) - 1] = w1.mon_budget[get_day(budget.datum) - 1] + budget.betrag

            if d_flag:
                w1.mon_serv[get_day(umsatz.datum) - 1] = w1.mon_serv[get_day(umsatz.datum) - 1] + n_serv
                w1.mon_tax[get_day(umsatz.datum) - 1] = w1.mon_tax[get_day(umsatz.datum) - 1] + n_tax
            ly_betrag =  to_decimal("0")

            if curr_date == to_date:
                serv =  to_decimal("0")
                vat =  to_decimal("0")

                if umsatz:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(n_betrag)
                    w1.tday_serv =  to_decimal(w1.tday_serv) + to_decimal(n_serv)
                    w1.tday_tax =  to_decimal(w1.tday_tax) + to_decimal(n_tax)

                if budget:
                    w1.tbudget =  to_decimal(w1.tbudget) + to_decimal(budget.betrag)

            if curr_date == to_date:

                buff_umsatz = db_session.query(Buff_umsatz).filter(
                         (Buff_umsatz.datum == curr_date - timedelta(days=1)) & (Buff_umsatz.artnr == w1.artnr) & (Buff_umsatz.departement == w1.dept)).first()

                if buff_umsatz:
                    yes_serv, yes_vat, yes_vat2, fact = get_output(calc_servtaxesbl(1, buff_umsatz.artnr, buff_umsatz.departement, buff_umsatz.datum))
                    yes_fact =  to_decimal(1.00) + to_decimal(yes_serv) + to_decimal(yes_vat) + to_decimal(yes_vat2)
                    yes_betrag =  to_decimal("0")

                    if foreign_flag:
                        find_exrate(curr_date - 1)

                        if exrate:
                            frate =  to_decimal(exrate.betrag)
                    yes_betrag =  to_decimal(buff_umsatz.betrag) / to_decimal((yes_fact) * to_decimal(frate))

                    if price_decimal == 0:
                        yes_betrag = to_decimal(round(yes_betrag , 0))
                    w1.yesterday =  to_decimal(w1.yesterday) + to_decimal(yes_betrag)

            if curr_date <= to_date:

                if umsatz:
                    w1.ytd_serv =  to_decimal(w1.ytd_serv) + to_decimal(n_serv)
                    w1.ytd_tax =  to_decimal(w1.ytd_tax) + to_decimal(n_tax)

            if curr_date < from_date:

                if umsatz:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(n_betrag)

                if budget:
                    w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(budget.betrag)
            else:

                if umsatz:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(n_betrag)

                    if ytd_flag:
                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(n_betrag)

                    if d_flag:
                        w1.mon_saldo[get_day(umsatz.datum) - 1] = w1.mon_saldo[get_day(umsatz.datum) - 1] + n_betrag
                    w1.mtd_serv =  to_decimal(w1.mtd_serv) + to_decimal(n_serv)
                    w1.mtd_tax =  to_decimal(w1.mtd_tax) + to_decimal(n_tax)

                if budget:
                    w1.budget =  to_decimal(w1.budget) + to_decimal(budget.betrag)

                    if ytd_flag:
                        w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(budget.betrag)

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date
            for curr_date in date_range(datum1,lto_date) :
                serv =  to_decimal("0")
                vat =  to_decimal("0")

                umsatz = get_cache (Umsatz, {"datum": [(eq, curr_date)],"artnr": [(eq, w1.artnr)],"departement": [(eq, w1.dept)]})

                if umsatz:
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, umsatz.artnr, umsatz.departement, umsatz.datum))
                fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat) + to_decimal(vat2)
                n_betrag =  to_decimal("0")

                if umsatz:

                    if foreign_flag:
                        find_exrate(curr_date)

                        if exrate:
                            frate =  to_decimal(exrate.betrag)
                    n_betrag =  to_decimal(umsatz.betrag) / to_decimal((fact) * to_decimal(frate) )
                    n_serv =  to_decimal(n_betrag) * to_decimal(serv)
                    n_tax =  to_decimal(n_betrag) * to_decimal(vat)

                    if price_decimal == 0:
                        n_betrag =  to_decimal(round (n_betrag , 0) )
                        n_serv = to_decimal(round(n_serv , 0))
                        n_tax = to_decimal(round(n_tax , 0))

                if budget_flag:

                    budget = get_cache (Budget, {"artnr": [(eq, w1.artnr)],"departement": [(eq, w1.dept)],"datum": [(eq, curr_date)]})

                if curr_date < lfrom_date:

                    if umsatz:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(n_betrag)
                        w1.lytd_serv =  to_decimal(w1.lytd_serv) + to_decimal(n_serv)
                        w1.lytd_tax =  to_decimal(w1.lytd_tax) + to_decimal(n_tax)

                    if budget:
                        w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(budget.betrag)
                else:

                    if umsatz:
                        dlmtd_flag = None != umsatz and (get_month(umsatz.datum) == get_month(to_date)) and (get_year(umsatz.datum) == get_year(to_date) - 1)

                        if dlmtd_flag:
                            w1.mon_lmtd[get_day(umsatz.datum) - 1] = w1.mon_lmtd[get_day(umsatz.datum) - 1] + n_betrag
                            w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(n_betrag)
                            w1.lmtd_serv =  to_decimal(w1.lmtd_serv) + to_decimal(n_serv)
                            w1.lmtd_tax =  to_decimal(w1.lmtd_tax) + to_decimal(n_tax)

                        if (get_day(umsatz.datum) == get_day(to_date)) and (get_month(umsatz.datum) == get_month(to_date)) and (get_year(umsatz.datum) == get_year(to_date) - 1):
                            w1.lytoday_serv =  to_decimal(w1.lytoday_serv) + to_decimal(n_serv)
                            w1.lytoday_tax =  to_decimal(w1.lytoday_tax) + to_decimal(n_tax)

                        if lytd_flag:
                            w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(n_betrag)
                            w1.lytd_serv =  to_decimal(w1.lytd_serv) + to_decimal(n_serv)
                            w1.lytd_tax =  to_decimal(w1.lytd_tax) + to_decimal(n_tax)

                    if budget:
                        w1.ly_budget =  to_decimal(w1.ly_budget) + to_decimal(budget.betrag)

                        if lytd_flag:
                            w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(budget.betrag)

        if pmtd_flag:
            for curr_date in date_range(pfrom_date,pto_date) :
                serv =  to_decimal("0")
                vat =  to_decimal("0")

                umsatz = get_cache (Umsatz, {"datum": [(eq, curr_date)],"artnr": [(eq, w1.artnr)],"departement": [(eq, w1.dept)]})

                if umsatz:
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, umsatz.artnr, umsatz.departement, umsatz.datum))
                fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat) + to_decimal(vat2)
                n_betrag =  to_decimal("0")

                if umsatz:

                    if foreign_flag:
                        find_exrate(curr_date)

                        if exrate:
                            frate =  to_decimal(exrate.betrag)
                    n_betrag =  to_decimal(umsatz.betrag) / to_decimal((fact) * to_decimal(frate) )
                    n_serv =  to_decimal(n_betrag) * to_decimal(serv)
                    n_tax =  to_decimal(n_betrag) * to_decimal(vat)

                    if price_decimal == 0:
                        n_betrag =  to_decimal(round (n_betrag , 0) )
                        n_serv = to_decimal(round(n_serv , 0))
                        n_tax = to_decimal(round(n_tax , 0))

                if budget_flag:

                    budget = get_cache (Budget, {"artnr": [(eq, w1.artnr)],"departement": [(eq, w1.dept)],"datum": [(eq, curr_date)]})

                if umsatz:
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(n_betrag)
                    w1.pmtd_serv =  to_decimal(w1.pmtd_serv) + to_decimal(n_serv)
                    w1.pmtd_tax =  to_decimal(w1.pmtd_tax) + to_decimal(n_tax)

                if budget:
                    w1.lm_budget =  to_decimal(w1.lm_budget) + to_decimal(budget.betrag)

        if lytoday_flag:
            for curr_date in date_range(lytoday,lytoday) :
                serv =  to_decimal("0")
                vat =  to_decimal("0")

                umsatz = get_cache (Umsatz, {"datum": [(eq, curr_date)],"artnr": [(eq, w1.artnr)],"departement": [(eq, w1.dept)]})

                if umsatz:
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, umsatz.artnr, umsatz.departement, umsatz.datum))
                fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat) + to_decimal(vat2)
                n_betrag =  to_decimal("0")

                if umsatz:

                    if foreign_flag:
                        find_exrate(curr_date)

                        if exrate:
                            frate =  to_decimal(exrate.betrag)
                    n_betrag =  to_decimal(umsatz.betrag) / to_decimal((fact) * to_decimal(frate))

                    if price_decimal == 0:
                        n_betrag =  to_decimal(round (n_betrag , 0))

                if budget_flag:

                    budget = get_cache (Budget, {"artnr": [(eq, w1.artnr)],"departement": [(eq, w1.dept)],"datum": [(eq, curr_date)]})

                if umsatz:
                    w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(n_betrag)
        w1.done = True


    def fill_persocc(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        datum2:date = None
        curr_date:date = None
        ly_currdate:date = None
        d_flag:bool = False
        dbudget_flag:bool = False
        dlmtd_flag:bool = False
        frate1:Decimal = to_decimal("0.0")
        W11 = W1
        w11_list = w1_list
        W753 = W1
        w753_list = w1_list
        W754 = W1
        w754_list = w1_list
        W755 = W1
        w755_list = w1_list

        w753 = query(w753_list, filters=(lambda w753: w753.main_code == 753 and not w753.done), first=True)

        w754 = query(w754_list, filters=(lambda w754: w754.main_code == 754 and not w754.done), first=True)

        w755 = query(w755_list, filters=(lambda w755: w755.main_code == 755 and not w755.done), first=True)

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        if lytd_flag:
            datum2 = ljan1
        else:
            datum2 = lfrom_date

        for segment in db_session.query(Segment).order_by(Segment._recid).all():

            if (get_day(to_date) == 31 and get_month(to_date) != 8 and get_month(to_date) != 1) or (get_day(to_date) == 30 and get_month(to_date) == 3) or (get_day(date_mdy(3, 1, get_year(to_date)) - 1) == 28 and get_month(to_date) == 3 and get_day(to_date) == 29):

                if w1:
                    w1.lm_today =  to_decimal("0")

                if w753:
                    w753.lm_today =  to_decimal("0")
            else:

                if get_month(to_date) == 1:
                    curr_date = date_mdy(12, get_day(to_date) , get_year(to_date) - timedelta(days=1))
                else:
                    curr_date = date_mdy(get_month(to_date) - timedelta(days=1, get_day(to_date) , get_year(to_date)))

                segmentstat = get_cache (Segmentstat, {"datum": [(eq, curr_date)],"segmentcode": [(eq, segment.segmentcode)]})

                if segmentstat:
                    frate =  to_decimal("1")

                    if foreign_flag:
                        find_exrate(segmentstat.datum)

                        if exrate:
                            frate =  to_decimal(exrate.betrag)
                    w1.lm_today =  to_decimal(w1.lm_today) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)

                    if w753:
                        w753.lm_today =  to_decimal(w753.lm_today) + to_decimal(segmentstat.persanz)

            for segmentstat in db_session.query(Segmentstat).filter(
                     (Segmentstat.datum >= datum1) & (Segmentstat.datum <= to_date) & (Segmentstat.segmentcode == segment.segmentcode)).order_by(Segmentstat._recid).all():
                frate =  to_decimal("1")

                if foreign_flag:
                    find_exrate(segmentstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)
                d_flag = (get_month(segmentstat.datum) == get_month(to_date)) and (get_year(segmentstat.datum) == get_year(to_date))
                dbudget_flag = (get_month(segmentstat.datum) == get_month(to_date)) and (get_year(segmentstat.datum) == get_year(to_date))

                if segmentstat.datum == to_date - timedelta(days=1):
                    w1.yesterday =  to_decimal(w1.yesterday) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)

                    if w753:
                        w753.yesterday =  to_decimal(w753.yesterday) + to_decimal(segmentstat.persanz)

                if segmentstat.datum == to_date:
                    pass

                    if lytd_flag and segmentstat.datum == to_date:

                        if get_month(to_date) == 2 and get_day(to_date) == 29:
                            pass
                        else:
                            ly_currdate = date_mdy(get_month(to_date) , get_day(to_date) , get_year(to_date) - timedelta(days=1))

                            segmbuff = get_cache (Segmentstat, {"datum": [(eq, ly_currdate)],"segmentcode": [(eq, segment.segmentcode)]})
                    w1.tday =  to_decimal(w1.tday) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                    w1.tbudget =  to_decimal(w1.tbudget) + to_decimal(segmentstat.budpersanz)

                    if w753:
                        w753.tday =  to_decimal(w753.tday) + to_decimal(segmentstat.persanz)

                    if w754:
                        w754.tday =  to_decimal(w754.tday) + to_decimal(segmentstat.kind1)

                    if w755:
                        w755.tday =  to_decimal(w755.tday) + to_decimal(segmentstat.kind2)

                if segmentstat.datum <= lfr_date:
                    w1.lm_ytd =  to_decimal(w1.lm_ytd) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)

                    if w753:
                        w753.lm_ytd =  to_decimal(w753.lm_ytd) + to_decimal(segmentstat.persanz)

                    if w754:
                        w754.lm_ytd =  to_decimal(w754.lm_ytd) + to_decimal(segmentstat.kind1)

                    if w755:
                        w755.lm_ytd =  to_decimal(w755.lm_ytd) + to_decimal(segmentstat.kind2)

                if segmentstat.datum < from_date:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                    w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(segmentstat.budpersanz)

                    if w753:
                        w753.ytd_saldo =  to_decimal(w753.ytd_saldo) + to_decimal(segmentstat.persanz)

                    if w754:
                        w754.ytd_saldo =  to_decimal(w754.ytd_saldo) + to_decimal(segmentstat.kind1)

                    if w755:
                        w755.ytd_saldo =  to_decimal(w755.ytd_saldo) + to_decimal(segmentstat.kind2)
                else:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(segmentstat.persanz) +\
                            segmentstat.kind1 + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                    w1.budget =  to_decimal(w1.budget) + to_decimal(segmentstat.budpersanz)

                    if d_flag:
                        w1.mon_saldo[get_day(segmentstat.datum) - 1] = w1.mon_saldo[get_day(segmentstat.datum) - 1]+ segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis

                    if dbudget_flag:
                        w1.mon_budget[get_day(segmentstat.datum) - 1] = w1.mon_budget[get_day(segmentstat.datum) - 1]+ segmentstat.budpersanz

                    if w753:
                        w753.saldo =  to_decimal(w753.saldo) + to_decimal(segmentstat.persanz)

                        if d_flag:
                            w753.mon_saldo[get_day(segmentstat.datum) - 1] = w753.mon_saldo[get_day(segmentstat.datum) - 1] + segmentstat.persanz

                    if w754:
                        w754.saldo =  to_decimal(w754.saldo) + to_decimal(segmentstat.kind1)

                        if d_flag:
                            w754.mon_saldo[get_day(segmentstat.datum) - 1] = w754.mon_saldo[get_day(segmentstat.datum) - 1] + segmentstat.kind1

                    if w755:
                        w755.saldo =  to_decimal(w755.saldo) + to_decimal(segmentstat.kind2)

                        if d_flag:
                            w755.mon_saldo[get_day(segmentstat.datum) - 1] = w755.mon_saldo[get_day(segmentstat.datum) - 1] + segmentstat.kind2

                    if ytd_flag:
                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(segmentstat.budpersanz)

                        if w753:
                            w753.ytd_saldo =  to_decimal(w753.ytd_saldo) + to_decimal(segmentstat.persanz)

                        if w754:
                            w754.ytd_saldo =  to_decimal(w754.ytd_saldo) + to_decimal(segmentstat.kind1)

                        if w755:
                            w755.ytd_saldo =  to_decimal(w755.ytd_saldo) + to_decimal(segmentstat.kind2)

            if lytd_flag or lmtd_flag:

                for segmentstat in db_session.query(Segmentstat).filter(
                         (Segmentstat.datum >= datum2) & (Segmentstat.datum <= lto_date) & (Segmentstat.segmentcode == segment.segmentcode)).order_by(Segmentstat._recid).all():

                    if foreign_flag:
                        find_exrate(segmentstat.datum)

                        if exrate:
                            frate =  to_decimal(exrate.betrag)

                    if segmentstat.datum < lfrom_date:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(segmentstat.budpersanz)

                        if w753:
                            w753.lytd_saldo =  to_decimal(w753.lytd_saldo) + to_decimal(segmentstat.persanz)

                        if w754:
                            w754.lytd_saldo =  to_decimal(w754.lytd_saldo) + to_decimal(segmentstat.kind1)

                        if w755:
                            w755.lytd_saldo =  to_decimal(w755.lytd_saldo) + to_decimal(segmentstat.kind2)
                    else:
                        dlmtd_flag = (get_month(segmentstat.datum) == get_month(to_date)) and (get_year(segmentstat.datum) == get_year(to_date) - 1)

                        if dlmtd_flag:
                            w1.mon_lmtd[get_day(segmentstat.datum) - 1] = w1.mon_lmtd[get_day(segmentstat.datum) - 1] + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w1.ly_budget =  to_decimal(w1.ly_budget) + to_decimal(segmentstat.budpersanz)

                        if w753:

                            if dlmtd_flag:
                                w753.mon_lmtd[get_day(segmentstat.datum) - 1] = w753.mon_lmtd[get_day(segmentstat.datum) - 1] + segmentstat.persanz
                            w753.lastyr =  to_decimal(w753.lastyr) + to_decimal(segmentstat.persanz)

                        if w754:

                            if dlmtd_flag:
                                w754.mon_lmtd[get_day(segmentstat.datum) - 1] = w754.mon_lmtd[get_day(segmentstat.datum) - 1] + segmentstat.kind1
                            w754.lastyr =  to_decimal(w754.lastyr) + to_decimal(segmentstat.kind1)

                        if w755:

                            if dlmtd_flag:
                                w755.mon_lmtd[get_day(segmentstat.datum) - 1] = w755.mon_lmtd[get_day(segmentstat.datum) - 1] + segmentstat.kind2
                            w755.lastyr =  to_decimal(w755.lastyr) + to_decimal(segmentstat.kind2)

                        if lytd_flag:
                            w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                            w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(segmentstat.budpersanz)

                            if w753:
                                w753.lytd_saldo =  to_decimal(w753.lytd_saldo) + to_decimal(segmentstat.persanz)

                            if w754:
                                w754.lytd_saldo =  to_decimal(w754.lytd_saldo) + to_decimal(segmentstat.kind1)

                            if w755:
                                w755.lytd_saldo =  to_decimal(w755.lytd_saldo) + to_decimal(segmentstat.kind2)

            if pmtd_flag:

                for segmentstat in db_session.query(Segmentstat).filter(
                         (Segmentstat.datum >= pfrom_date) & (Segmentstat.datum <= pto_date) & (Segmentstat.segmentcode == segment.segmentcode)).order_by(Segmentstat._recid).all():

                    if foreign_flag:
                        find_exrate(segmentstat.datum)

                        if exrate:
                            frate =  to_decimal(exrate.betrag)
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                    w1.lm_budget =  to_decimal(w1.lm_budget) + to_decimal(segmentstat.budpersanz)

                    if w753:
                        w753.lastmon =  to_decimal(w753.lastmon) + to_decimal(segmentstat.persanz)

                    if w754:
                        w754.lastmon =  to_decimal(w754.lastmon) + to_decimal(segmentstat.kind1)

                    if w755:
                        w755.lastmon =  to_decimal(w755.lastmon) + to_decimal(segmentstat.kind2)


            if lytoday_flag:

                segmentstat = get_cache (Segmentstat, {"datum": [(eq, lytoday)],"segmentcode": [(eq, segment.segmentcode)]})

                if segmentstat:

                    if foreign_flag:
                        find_exrate(segmentstat.datum)

                        if exrate:
                            frate =  to_decimal(exrate.betrag)
                    w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)

                    if w753:
                        w753.lytoday =  to_decimal(w753.lytoday) + to_decimal(segmentstat.persanz)

                    if w754:
                        w754.lytoday =  to_decimal(w754.lytoday) + to_decimal(segmentstat.kind1)

                    if w755:
                        w755.lytoday =  to_decimal(w755.lytoday) + to_decimal(segmentstat.kind2)
        w1.done = True

        if w753:
            w753.done = True

        if w754:
            w754.done = True

        if w755:
            w755.done = True


    def fill_avrgrate(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        W11 = W1
        w11_list = w1_list

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        w11 = query(w11_list, filters=(lambda w11: w11.main_code == 842), first=True)

        if w11 and w11.done:
            pass

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.datum >= datum1) & (Zinrstat.datum <= to_date) & (Zinrstat.zinr == ("avrgrate").lower())).order_by(Zinrstat._recid).all():

            if zinrstat.datum == to_date:
                w1.tday =  to_decimal(w1.tday) + to_decimal(zinrstat.argtumsatz)

                if w11:
                    w11.tday =  to_decimal(w11.tday) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

            if zinrstat.datum < from_date:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

                if w11:
                    w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)
            else:
                w1.saldo =  to_decimal(w1.saldo) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

                if ytd_flag:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

                if w11:
                    w11.saldo =  to_decimal(w11.saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

                    if ytd_flag:
                        w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= datum1) & (Zinrstat.datum <= lto_date) & (Zinrstat.zinr == ("avrgrate").lower())).order_by(Zinrstat._recid).all():

                if zinrstat.datum < lfrom_date:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

                    if w11:
                        w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)
                else:
                    w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

                    if lytd_flag:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

                    if w11:
                        w11.lastyr =  to_decimal(w11.lastyr) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

                        if lytd_flag:
                            w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

        if pmtd_flag:

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= pfrom_date) & (Zinrstat.datum <= pto_date) & (Zinrstat.zinr == ("avrgrate").lower())).order_by(Zinrstat._recid).all():
                w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

                if w11:
                    w11.lastmon =  to_decimal(w11.lastmon) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)


        if lytoday_flag:

            zinrstat = get_cache (Zinrstat, {"datum": [(eq, lytoday)],"zinr": [(eq, "avrgrate")]})

            if zinrstat:
                w1.lytoday =  to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

                if w11:
                    w11.lytoday =  to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)
        w1.done = True

        if w11:
            w11.done = True


    def fill_avrglrate(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        W11 = W1
        w11_list = w1_list

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        w11 = query(w11_list, filters=(lambda w11: w11.main_code == 46), first=True)

        if w11 and w11.done:
            pass

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.datum >= datum1) & (Zinrstat.datum <= to_date) & (Zinrstat.zinr == ("avrgLrate").lower())).order_by(Zinrstat._recid).all():

            if zinrstat.datum == to_date:
                w1.tday =  to_decimal(w1.tday) + to_decimal(zinrstat.argtumsatz)

                if w11:
                    w11.tday =  to_decimal(w11.tday) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

            if zinrstat.datum < from_date:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

                if w11:
                    w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)
            else:
                w1.saldo =  to_decimal(w1.saldo) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

                if ytd_flag:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

                if w11:
                    w11.saldo =  to_decimal(w11.saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

                    if ytd_flag:
                        w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= datum1) & (Zinrstat.datum <= lto_date) & (Zinrstat.zinr == ("avrgLrate").lower())).order_by(Zinrstat._recid).all():

                if zinrstat.datum < lfrom_date:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

                    if w11:
                        w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)
                else:
                    w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

                    if lytd_flag:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

                    if w11:
                        w11.lastyr =  to_decimal(w11.lastyr) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

                        if lytd_flag:
                            w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

        if pmtd_flag:

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= pfrom_date) & (Zinrstat.datum <= pto_date) & (Zinrstat.zinr == ("avrgLrate").lower())).order_by(Zinrstat._recid).all():
                w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

                if w11:
                    w11.lastmon =  to_decimal(w11.lastmon) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)


        if lytoday_flag:

            zinrstat = get_cache (Zinrstat, {"datum": [(eq, lytoday)],"zinr": [(eq, "avrglrate")]})

            if zinrstat:
                w1.lytoday =  to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

                if w11:
                    w11.lytoday =  to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)
        w1.done = True

        if w11:
            w11.done = True


    def fill_avrglodge(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        W11 = W1
        w11_list = w1_list

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        w11 = query(w11_list, filters=(lambda w11: w11.main_code == 811), first=True)

        if w11 and w11.done:
            pass

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.datum >= datum1) & (Zinrstat.datum <= to_date) & (Zinrstat.zinr == ("avrgrate").lower())).order_by(Zinrstat._recid).all():

            if zinrstat.datum == to_date:
                w1.tday =  to_decimal(w1.tday) + to_decimal(zinrstat.logisumsatz)

                if w11:
                    w11.tday =  to_decimal(w11.tday) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

            if zinrstat.datum < from_date:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

                if w11:
                    w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)
            else:
                w1.saldo =  to_decimal(w1.saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

                if ytd_flag:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

                if w11:
                    w11.saldo =  to_decimal(w11.saldo) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

                    if ytd_flag:
                        w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= datum1) & (Zinrstat.datum <= lto_date) & (Zinrstat.zinr == ("avrgrate").lower())).order_by(Zinrstat._recid).all():

                if zinrstat.datum < lfrom_date:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

                    if w11:
                        w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)
                else:
                    w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

                    if lytd_flag:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

                    if w11:
                        w11.lastyr =  to_decimal(w11.lastyr) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

                        if lytd_flag:
                            w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

        if pmtd_flag:

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= pfrom_date) & (Zinrstat.datum <= pto_date) & (Zinrstat.zinr == ("avrgrate").lower())).order_by(Zinrstat._recid).all():

                if foreign_flag:
                    find_exrate(zinrstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)
                w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

                if w11:
                    w11.lastmon =  to_decimal(w11.lastmon) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)


        if lytoday_flag:

            zinrstat = get_cache (Zinrstat, {"datum": [(eq, lytoday)],"zinr": [(eq, "avrgrate")]})

            if zinrstat:

                if foreign_flag:
                    find_exrate(zinrstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)
                w1.lytoday =  to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

                if w11:
                    w11.lytoday =  to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)
        w1.done = True

        if w11:
            w11.done = True


    def fill_nation(rec_w1:int, main_nr:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        mm:int = 0
        natnr:int = 0
        datum1:date = None
        curr_date:date = None
        ly_currdate:date = None
        ny_currdate:date = None
        njan1:date = None
        nmth1:date = None
        d_flag:bool = False
        dbudget_flag:bool = False
        dlmtd_flag:bool = False
        frate1:Decimal = to_decimal("0.0")

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)
        natnr = w1.artnr

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date
        mm = get_month(to_date)

        for genstat in db_session.query(Genstat).filter(
                     (Genstat.resident == natnr) & (Genstat.datum >= datum1) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.resident != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
            frate =  to_decimal("1")
            d_flag = (get_month(genstat.datum) == get_month(to_date)) and (get_year(genstat.datum) == get_year(to_date))

            if genstat.datum == to_date:

                if main_nr == 8814:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                if main_nr == 8813:
                    w1.tday =  to_decimal(w1.tday) + to_decimal("1")

                if main_nr == 8092:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(genstat.logis)

            if get_month(genstat.datum) == mm:

                if main_nr == 8814:

                    if d_flag:
                        w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                if main_nr == 8813:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal("1")

                    if d_flag:
                        w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + 1

                if main_nr == 8092:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(genstat.logis)

                    if d_flag:
                        w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + genstat.logis

            if main_nr == 8814:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

            if main_nr == 8813:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal("1")

            if main_nr == 8092:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(genstat.logis)

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date
            mm = get_month(lto_date)

            for genstat in db_session.query(Genstat).filter(
                         (Genstat.resident == natnr) & (Genstat.datum >= datum1) & (Genstat.datum <= lto_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.resident != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
                dlmtd_flag = (get_month(genstat.datum) == get_month(lto_date)) and (get_year(genstat.datum) == get_year(lto_date))

                if genstat.datum == lto_date:

                    if main_nr == 8814:
                        w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                    if main_nr == 8813:
                        w1.lytoday =  to_decimal(w1.lytoday) + to_decimal("1")

                    if main_nr == 8092:
                        w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(genstat.logis)

                if get_month(genstat.datum) == mm:

                    if main_nr == 8814:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                    if main_nr == 8813:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal("1")

                    if main_nr == 8092:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(genstat.logis)

                if main_nr == 8814:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                if main_nr == 8813:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal("1")

                if main_nr == 8092:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(genstat.logis)


    def fill_competitor(rec_w1:int, main_nr:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        mm:int = 0
        compnr:int = 0
        datum1:date = None
        curr_date:date = None
        ly_currdate:date = None
        ny_currdate:date = None
        njan1:date = None
        nmth1:date = None
        d_flag:bool = False
        dbudget_flag:bool = False
        dlmtd_flag:bool = False
        frate1:Decimal = to_decimal("0.0")

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)
        compnr = w1.artnr

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date
        mm = get_month(to_date)

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.datum >= datum1) & (Zinrstat.datum <= to_date) & (Zinrstat.zinr == ("Competitor").lower()) & (Zinrstat.betriebsnr == compnr)).order_by(Zinrstat._recid).all():
            frate =  to_decimal("1")
            d_flag = (get_month(zinrstat.datum) == get_month(to_date)) and (get_year(zinrstat.datum) == get_year(to_date))

            if zinrstat.datum == to_date:

                if main_nr == 9981:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(zinrstat.zimmeranz)

                if main_nr == 9982:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(zinrstat.personen)

                if main_nr == 9983:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(to_int(zinrstat.argtumsatz))

                if main_nr == 9984:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(zinrstat.logisumsatz)

            if get_month(zinrstat.datum) == mm:

                if main_nr == 9981:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(zinrstat.zimmeranz)

                    if d_flag:
                        w1.mon_saldo[get_day(zinrstat.datum) - 1] = w1.mon_saldo[get_day(zinrstat.datum) - 1] + zinrstat.zimmeranz

                elif main_nr == 9982:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(zinrstat.personen)

                    if d_flag:
                        w1.mon_saldo[get_day(zinrstat.datum) - 1] = w1.mon_saldo[get_day(zinrstat.datum) - 1] + zinrstat.personen

                elif main_nr == 9983:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(to_int(zinrstat.argtumsatz))

                    if d_flag:
                        w1.mon_saldo[get_day(zinrstat.datum) - 1] = w1.mon_saldo[get_day(zinrstat.datum) - 1] + to_int(zinrstat.argtumsatz)

                elif main_nr == 9984:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(zinrstat.logisumsatz)

                    if d_flag:
                        w1.mon_saldo[get_day(zinrstat.datum) - 1] = w1.mon_saldo[get_day(zinrstat.datum) - 1] + zinrstat.logisumsatz

            if main_nr == 9981:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.zimmeranz)

            elif main_nr == 9982:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.personen)

            elif main_nr == 9983:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(to_int(zinrstat.argtumsatz))

            elif main_nr == 9984:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.logisumsatz)

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date
            mm = get_month(lto_date)

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= datum1) & (Zinrstat.datum <= lto_date) & (Zinrstat.zinr == ("Competitor").lower()) & (Zinrstat.betriebsnr == compnr)).order_by(Zinrstat._recid).all():
                dlmtd_flag = (get_month(zinrstat.datum) == get_month(lto_date)) and (get_year(zinrstat.datum) == get_year(lto_date))

                if zinrstat.datum == lto_date:

                    if main_nr == 9981:
                        w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(zinrstat.zimmeranz)

                    if main_nr == 9982:
                        w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(zinrstat.personen)

                    if main_nr == 9983:
                        w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(to_int(zinrstat.argtumsatz))

                    if main_nr == 9984:
                        w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(zinrstat.logisumsatz)

                if get_month(zinrstat.datum) == mm:

                    if main_nr == 9981:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(zinrstat.zimmeranz)

                    if main_nr == 9982:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(zinrstat.personen)

                    if main_nr == 9983:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(to_int(zinrstat.argtumsatz))

                    if main_nr == 9984:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(zinrstat.logisumsatz)

                if main_nr == 9981:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.zimmeranz)

                elif main_nr == 9982:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.personen)

                elif main_nr == 9983:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(to_int(zinrstat.argtumsatz))

                elif main_nr == 9984:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.logisumsatz)


    def fill_segment(rec_w1:int, main_nr:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        mm:int = 0
        segm:int = 0
        datum1:date = None
        curr_date:date = None
        ly_currdate:date = None
        ny_currdate:date = None
        njan1:date = None
        nmth1:date = None
        d_flag:bool = False
        dbudget_flag:bool = False
        dlmtd_flag:bool = False
        frate1:Decimal = to_decimal("0.0")
        black_list:int = 0
        segmbuffny = None
        Segmbuffny =  create_buffer("Segmbuffny",Segmentstat)

        if get_month(to_date) == 2 and get_day(to_date) == 29:
            ny_currdate = date_mdy(get_month(to_date) , 28, get_year(to_date) + timedelta(days=1))
        else:
            ny_currdate = date_mdy(get_month(to_date) , get_day(to_date) , get_year(to_date) + timedelta(days=1))
        njan1 = date_mdy(1, 1, get_year(to_date) + timedelta(days=1))
        nmth1 = date_mdy(get_month(to_date) , 1, get_year(to_date) + timedelta(days=1))

        htparam = get_cache (Htparam, {"paramnr": [(eq, 709)]})
        black_list = htparam.finteger

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)
        segm = w1.artnr

        segmbuffny = get_cache (Segmentstat, {"datum": [(eq, ny_currdate)],"segmentcode": [(eq, segm)]})

        if segmbuffny:

            if main_nr == 92:
                w1.ny_budget =  to_decimal(segmbuffny.budlogis)

            if main_nr == 813:
                w1.ny_budget =  to_decimal(segmbuffny.budzimmeranz)

            if main_nr == 814:
                w1.ny_budget =  to_decimal(segmbuffny.budpersanz)

        for segmbuffny in db_session.query(Segmbuffny).filter(
                 (Segmbuffny.datum >= njan1) & (Segmbuffny.datum <= ny_currdate) & (Segmbuffny.segmentcode == segm)).order_by(Segmbuffny._recid).all():

            if main_nr == 92:
                w1.nytd_budget =  to_decimal(w1.nytd_budget) + to_decimal(segmbuffny.budlogis)

            if main_nr == 813:
                w1.nytd_budget =  to_decimal(w1.nytd_budget) + to_decimal(segmbuffny.budzimmeranz)

            if main_nr == 814:
                w1.nytd_budget =  to_decimal(w1.nytd_budget) + to_decimal(segmbuffny.budpersanz)

        for segmbuffny in db_session.query(Segmbuffny).filter(
                 (Segmbuffny.datum >= nmth1) & (Segmbuffny.datum <= ny_currdate) & (Segmbuffny.segmentcode == segm)).order_by(Segmbuffny._recid).all():

            if main_nr == 92:
                w1.nmtd_budget =  to_decimal(w1.nmtd_budget) + to_decimal(segmbuffny.budlogis)

            if main_nr == 813:
                w1.nmtd_budget =  to_decimal(w1.nmtd_budget) + to_decimal(segmbuffny.budzimmeranz)

            if main_nr == 814:
                w1.nmtd_budget =  to_decimal(w1.nmtd_budget) + to_decimal(segmbuffny.budpersanz)

        segmentstat = get_cache (Segmentstat, {"datum": [(eq, to_date - timedelta(days=1))],"segmentcode": [(eq, segm)]})

        if segmentstat:
            frate =  to_decimal("1")

            if foreign_flag:
                find_exrate(segmentstat.datum)

                if exrate:
                    frate =  to_decimal(exrate.betrag)

            if main_nr == 92:
                w1.yesterday =  to_decimal(segmentstat.logis) / to_decimal(frate)

            elif main_nr == 813:
                w1.yesterday =  to_decimal(segmentstat.zimmeranz)

            elif main_nr == 814:
                w1.yesterday =  to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)

            if main_nr == 9007:

                zinrstat = get_cache (Zinrstat, {"datum": [(eq, segmbuffny.datum)],"zinr": [(eq, "segm")],"betriebsnr": [(eq, segmbuffny.segmentcode)]})

                if zinrstat:
                    w1.yesterday =  to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

        if (get_day(to_date) == 31 and get_month(to_date) != 8 and get_month(to_date) != 1) or (get_day(to_date) == 30 and get_month(to_date) == 3) or (get_day(date_mdy(3, 1, get_year(to_date)) - 1) == 28 and get_month(to_date) == 3 and get_day(to_date) == 29):
            w1.lm_today =  to_decimal("0")
        else:

            if get_month(to_date) == 1:
                curr_date = date_mdy(12, get_day(to_date) , get_year(to_date) - timedelta(days=1))
            else:
                curr_date = date_mdy(get_month(to_date) - timedelta(days=1, get_day(to_date) , get_year(to_date)))

            segmentstat = get_cache (Segmentstat, {"datum": [(eq, curr_date)],"segmentcode": [(eq, segm)]})

            if segmentstat:
                frate =  to_decimal("1")

                if foreign_flag:
                    find_exrate(segmentstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)

                if main_nr == 92:
                    w1.lm_today =  to_decimal(segmentstat.logis) / to_decimal(frate)

                elif main_nr == 813:
                    w1.lm_today =  to_decimal(segmentstat.zimmeranz)

                elif main_nr == 814:
                    w1.lm_today =  to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)

                if main_nr == 9007:

                    zinrstat = get_cache (Zinrstat, {"datum": [(eq, segmbuffny.datum)],"zinr": [(eq, "segm")],"betriebsnr": [(eq, segmbuffny.segmentcode)]})

                    if zinrstat:
                        w1.lm_today =  to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date
        mm = get_month(to_date)

        for genstat in db_session.query(Genstat).filter(
                     (Genstat.segmentcode == segm) & (Genstat.datum >= datum1) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
            frate =  to_decimal("1")

            if foreign_flag:
                find_exrate(genstat.datum)

                if exrate:
                    frate =  to_decimal(exrate.betrag)
            d_flag = (get_month(genstat.datum) == get_month(to_date)) and (get_year(genstat.datum) == get_year(to_date))

            if genstat.datum == to_date:

                if main_nr == 814:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                if main_nr == 813:
                    w1.tday =  to_decimal(w1.tday) + to_decimal("1")

                if main_nr == 92:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(genstat.logis)

                if main_nr == 756:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(genstat.erwachs)

                elif main_nr == 757:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(genstat.kind1)

                elif main_nr == 758:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(genstat.kind2)

            if get_month(genstat.datum) == mm:

                if main_nr == 814 and d_flag:
                    w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                if main_nr == 813 and d_flag:
                    w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + 1

                if main_nr == 92 and d_flag:
                    w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + genstat.logis

                if main_nr == 756 and d_flag:
                    w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + genstat.erwachs

                elif main_nr == 757 and d_flag:
                    w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + genstat.kind1

                elif main_nr == 758 and d_flag:
                    w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + genstat.kind2

            if genstat.datum >= from_date:

                if main_nr == 814:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                if main_nr == 813:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal("1")

                if main_nr == 92:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(genstat.logis)

                if main_nr == 756:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(genstat.erwachs)

                elif main_nr == 757:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(genstat.kind1)

                elif main_nr == 758:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(genstat.kind2)

            if main_nr == 814:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

            if main_nr == 813:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal("1")

            if main_nr == 92:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(genstat.logis)

            if main_nr == 756:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(genstat.erwachs)

            elif main_nr == 757:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(genstat.kind1)

            elif main_nr == 758:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(genstat.kind2)

        zinrstat_obj_list = {}
        for zinrstat, segment in db_session.query(Zinrstat, Segment).join(Segment,(Segment.segmentcode == Zinrstat.betriebsnr) & (Segment.segmentcode != black_list) & (Segment.segmentgrup <= 99)).filter(
                     (Zinrstat.datum >= datum1) & (Zinrstat.datum <= to_date) & (Zinrstat.zinr == ("segm").lower()) & (Zinrstat.betriebsnr == segm)).order_by(Segment.segmentgrup, Segment.segmentcode).all():
            if zinrstat_obj_list.get(zinrstat._recid):
                continue
            else:
                zinrstat_obj_list[zinrstat._recid] = True


            d_flag = (get_month(zinrstat.datum) == get_month(to_date)) and (get_year(zinrstat.datum) == get_year(to_date))
            frate =  to_decimal("1")

            if foreign_flag:
                find_exrate(genstat.datum)

                if exrate:
                    frate =  to_decimal(exrate.betrag)

            if main_nr == 9007:

                if zinrstat.datum == to_date:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(zinrstat.logisumsatz)

                if get_month(zinrstat.datum) == get_month(to_date) and d_flag:
                    w1.mon_saldo[get_day(zinrstat.datum) - 1] = w1.mon_saldo[get_day(zinrstat.datum) - 1] + zinrstat.logisumsatz

                if zinrstat.datum >= from_date:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(zinrstat.logisumsatz)
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.logisumsatz)

        for segmentstat in db_session.query(Segmentstat).filter(
                     (Segmentstat.datum >= datum1) & (Segmentstat.datum <= to_date) & (Segmentstat.segmentcode == segm)).order_by(Segmentstat._recid).all():
            dbudget_flag = (get_month(segmentstat.datum) == get_month(to_date)) and (get_year(segmentstat.datum) == get_year(to_date))

            if segmentstat.datum == to_date:

                if main_nr == 814:
                    w1.tbudget =  to_decimal(w1.tbudget) + to_decimal(segmentstat.budpersanz)

                if main_nr == 813:
                    w1.tbudget =  to_decimal(w1.tbudget) + to_decimal(segmentstat.budzimmeranz)

                if main_nr == 92:
                    w1.tbudget =  to_decimal(w1.tbudget) + to_decimal(segmentstat.budlogis)

            if get_month(segmentstat.datum) == mm:

                if main_nr == 814 and dbudget_flag:
                    w1.mon_budget[get_day(segmentstat.datum) - 1] = w1.mon_budget[get_day(segmentstat.datum) - 1] + segmentstat.budpersanz

                if main_nr == 813 and dbudget_flag:
                    w1.mon_budget[get_day(segmentstat.datum) - 1] = w1.mon_budget[get_day(segmentstat.datum) - 1] + segmentstat.budzimmeranz

                if main_nr == 92 and dbudget_flag:
                    w1.mon_budget[get_day(segmentstat.datum) - 1] = w1.mon_budget[get_day(segmentstat.datum) - 1] + segmentstat.budlogis

            if segmentstat.datum >= from_date:

                if main_nr == 814:
                    w1.budget =  to_decimal(w1.budget) + to_decimal(segmentstat.budpersanz)

                if main_nr == 813:
                    w1.budget =  to_decimal(w1.budget) + to_decimal(segmentstat.budzimmeranz)

                if main_nr == 92:
                    w1.budget =  to_decimal(w1.budget) + to_decimal(segmentstat.budlogis)

            if main_nr == 814:
                w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(segmentstat.budpersanz)

            if main_nr == 813:
                w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(segmentstat.budzimmeranz)

            if main_nr == 92:
                w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(segmentstat.budlogis)

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date
            mm = get_month(lto_date)

            for genstat in db_session.query(Genstat).filter(
                         (Genstat.segmentcode == segm) & (Genstat.datum >= datum1) & (Genstat.datum <= lto_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
                frate =  to_decimal("1")

                if foreign_flag:
                    find_exrate(genstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)
                dlmtd_flag = (get_month(genstat.datum) == get_month(lto_date)) and (get_year(genstat.datum) == get_year(lto_date))

                if genstat.datum == lto_date:

                    if main_nr == 814:
                        w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                    if main_nr == 813:
                        w1.lytoday =  to_decimal(w1.lytoday) + to_decimal("1")

                    if main_nr == 92:
                        w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(genstat.logis)

                if get_month(genstat.datum) == mm:

                    if main_nr == 814:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                    if main_nr == 813:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal("1")

                    if main_nr == 92:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(genstat.logis)

                if main_nr == 814:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                if main_nr == 813:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal("1")

                if main_nr == 92:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(genstat.logis)

            zinrstat_obj_list = {}
            for zinrstat, segment in db_session.query(Zinrstat, Segment).join(Segment,(Segment.segmentcode == Zinrstat.betriebsnr) & (Segment.segmentcode != black_list) & (Segment.segmentgrup <= 99)).filter(
                         (Zinrstat.datum >= datum1) & (Zinrstat.datum <= lto_date) & (Zinrstat.zinr == ("segm").lower()) & (Zinrstat.betriebsnr == segm)).order_by(Segment.segmentgrup, Segment.segmentcode).all():
                if zinrstat_obj_list.get(zinrstat._recid):
                    continue
                else:
                    zinrstat_obj_list[zinrstat._recid] = True


                frate =  to_decimal("1")

                if foreign_flag:
                    find_exrate(zinrstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)
                dlmtd_flag = (get_month(zinrstat.datum) == get_month(lto_date)) and (get_year(zinrstat.datum) == get_year(lto_date))

                if main_nr == 9007:

                    if zinrstat.datum == lto_date:
                        w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(zinrstat.logisumsatz)

                    if get_month(zinrstat.datum) == mm:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(zinrstat.logisumsatz)
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.logisumsatz)

            for segmentstat in db_session.query(Segmentstat).filter(
                         (Segmentstat.datum >= datum1) & (Segmentstat.datum <= lto_date) & (Segmentstat.segmentcode == segm)).order_by(Segmentstat._recid).all():

                if get_month(segmentstat.datum) == mm:

                    if main_nr == 814:
                        w1.ly_budget =  to_decimal(w1.ly_budget) + to_decimal(segmentstat.budpersanz)

                    if main_nr == 813:
                        w1.ly_budget =  to_decimal(w1.ly_budget) + to_decimal(segmentstat.budzimmeranz)

                    if main_nr == 92:
                        w1.ly_budget =  to_decimal(w1.ly_budget) + to_decimal(segmentstat.budlogis)

                if main_nr == 814:
                    w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(segmentstat.budpersanz)

                if main_nr == 813:
                    w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(segmentstat.budzimmeranz)

                if main_nr == 92:
                    w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(segmentstat.budlogis)

        if pmtd_flag:

            for genstat in db_session.query(Genstat).filter(
                         (Genstat.segmentcode == segm) & (Genstat.datum >= pfrom_date) & (Genstat.datum <= pto_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():

                if foreign_flag:
                    find_exrate(genstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)

                if main_nr == 814:
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                if main_nr == 813:
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal("1")

                if main_nr == 92:
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(genstat.logis)

            zinrstat_obj_list = {}
            for zinrstat, segment in db_session.query(Zinrstat, Segment).join(Segment,(Segment.segmentcode == Zinrstat.betriebsnr) & (Segment.segmentcode != black_list) & (Segment.segmentgrup <= 99)).filter(
                         (Zinrstat.datum >= pfrom_date) & (Zinrstat.datum <= pto_date) & (Zinrstat.zinr == ("segm").lower()) & (Zinrstat.betriebsnr == segm)).order_by(Segment.segmentgrup, Segment.segmentcode).all():
                if zinrstat_obj_list.get(zinrstat._recid):
                    continue
                else:
                    zinrstat_obj_list[zinrstat._recid] = True


                frate =  to_decimal("1")

                if foreign_flag:
                    find_exrate(genstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)

                if main_nr == 9007:
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(zinrstat.logisumsatz)


    def fill_rmcatstat(rec_w1:int, main_nr:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        zikatno:int = 0
        datum1:date = None

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return
        zikatno = w1.artnr

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for zkstat in db_session.query(Zkstat).filter(
                 (Zkstat.datum >= datum1) & (Zkstat.datum <= to_date) & (Zkstat.zikatnr == zikatno)).order_by(Zkstat._recid).all():

            if zkstat.datum == to_date:
                w1.tday =  to_decimal(w1.tday) + to_decimal(zkstat.zimmeranz) - to_decimal(zkstat.betriebsnr) + to_decimal(zkstat.arrangement_art[0])

            if zkstat.datum < from_date:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zkstat.zimmeranz) - to_decimal(zkstat.betriebsnr) + to_decimal(zkstat.arrangement_art[0])
            else:
                w1.saldo =  to_decimal(w1.saldo) + to_decimal(zkstat.zimmeranz) - to_decimal(zkstat.betriebsnr) + to_decimal(zkstat.arrangement_art[0])

                if ytd_flag:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zkstat.zimmeranz) - to_decimal(zkstat.betriebsnr) + to_decimal(zkstat.arrangement_art[0])

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            for zkstat in db_session.query(Zkstat).filter(
                     (Zkstat.datum >= datum1) & (Zkstat.datum <= lto_date) & (Zkstat.zikatnr == zikatno)).order_by(Zkstat._recid).all():

                if zkstat.datum < lfrom_date:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zkstat.zimmeranz) - to_decimal(zkstat.betriebsnr) + to_decimal(zkstat.arrangement_art[0])
                else:
                    w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(zkstat.zimmeranz) - to_decimal(zkstat.betriebsnr) + to_decimal(zkstat.arrangement_art[0])

                    if lytd_flag:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zkstat.zimmeranz) - to_decimal(zkstat.betriebsnr) + to_decimal(zkstat.arrangement_art[0])

        if pmtd_flag:

            for zkstat in db_session.query(Zkstat).filter(
                     (Zkstat.datum >= pfrom_date) & (Zkstat.datum <= pto_date) & (Zkstat.zikatnr == zikatno)).order_by(Zkstat._recid).all():
                w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(zkstat.zimmeranz) - to_decimal(zkstat.betriebsnr) + to_decimal(zkstat.arrangement_art[0])


        if lytoday_flag:

            zkstat = get_cache (Zkstat, {"datum": [(eq, lytoday)],"zikatnr": [(eq, zikatno)]})

            if zkstat:
                w1.lytoday =  to_decimal(zkstat.zimmeranz) - to_decimal(zkstat.betriebsnr) + to_decimal(zkstat.arrangement_art[0])
        w1.done = True


    def fill_zinrstat(rec_w1:int, main_nr:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        rmno:int = 0
        mm:int = 0
        s_rmno:string = ""
        datum1:date = None
        d_flag:bool = False
        W11 = W1
        w11_list = w1_list
        W12 = W1
        w12_list = w1_list
        W13 = W1
        w13_list = w1_list

        if main_nr == 800:

            w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

            if w1.done:

                return
            rmno = w1.artnr


            s_rmno = w1.s_artnr

            w12 = query(w12_list, filters=(lambda w12: w12.main_code == 180 and w12.artnr == rmno and w12.s_artnr.lower()  == (s_rmno).lower()), first=True)

            w13 = query(w13_list, filters=(lambda w13: w13.main_code == 181 and w13.artnr == rmno and w13.s_artnr.lower()  == (s_rmno).lower()), first=True)

        elif main_nr == 180:

            w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

            if w1.done:

                return
            rmno = w1.artnr
            s_rmno = w1.s_artnr

            w11 = query(w11_list, filters=(lambda w11: w11.main_code == 800 and w11.artnr == rmno and w11.s_artnr.lower()  == (s_rmno).lower()), first=True)

            w13 = query(w13_list, filters=(lambda w13: w13.main_code == 181 and w13.artnr == rmno and w13.s_artnr.lower()  == (s_rmno).lower()), first=True)

        elif main_nr == 181:

            w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

            if w1.done:

                return
            rmno = w1.artnr
            s_rmno = w1.s_artnr

            w11 = query(w11_list, filters=(lambda w11: w11.main_code == 800 and w11.artnr == rmno and w11.s_artnr.lower()  == (s_rmno).lower()), first=True)

            w12 = query(w12_list, filters=(lambda w12: w12.main_code == 180 and w12.artnr == rmno and w12.s_artnr.lower()  == (s_rmno).lower()), first=True)

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.datum >= datum1) & (Zinrstat.datum <= to_date) & (Zinrstat.zinr == (s_rmno).lower())).order_by(Zinrstat._recid).all():

            if foreign_flag:
                find_exrate(zinrstat.datum)

                if exrate:
                    frate =  to_decimal(exrate.betrag)
            d_flag = (get_month(zinrstat.datum) == get_month(to_date)) and (get_year(zinrstat.datum) == get_year(to_date))

            if d_flag:

                if main_nr == 800:
                    w1.mon_saldo[get_day(zinrstat.datum) - 1] = w1.mon_saldo[get_day(zinrstat.datum) - 1] + zinrstat.logisumsatz / frate

                    if w12:
                        w12.mon_saldo[get_day(zinrstat.datum) - 1] = w12.mon_saldo[get_day(zinrstat.datum) - 1] + zinrstat.zimmeranz

                    if w13:
                        w13.mon_saldo[get_day(zinrstat.datum) - 1] = w13.mon_saldo[get_day(zinrstat.datum) - 1] + zinrstat.personen

                elif main_nr == 180:
                    w1.mon_saldo[get_day(zinrstat.datum) - 1] = w1.mon_saldo[get_day(zinrstat.datum) - 1] + zinrstat.zimmeranz

                    if w11:
                        w11.mon_saldo[get_day(zinrstat.datum) - 1] = w11.mon_saldo[get_day(zinrstat.datum) - 1] + zinrstat.logisumsatz / frate

                    if w13:
                        w13.mon_saldo[get_day(zinrstat.datum) - 1] = w13.mon_saldo[get_day(zinrstat.datum) - 1] + zinrstat.personen

                elif main_nr == 181:
                    w1.mon_saldo[get_day(zinrstat.datum) - 1] = w1.mon_saldo[get_day(zinrstat.datum) - 1] + zinrstat.personen

                    if w11:
                        w11.mon_saldo[get_day(zinrstat.datum) - 1] = w11.mon_saldo[get_day(zinrstat.datum) - 1] + zinrstat.logisumsatz / frate

                    if w12:
                        w12.mon_saldo[get_day(zinrstat.datum) - 1] = w12.mon_saldo[get_day(zinrstat.datum) - 1] + zinrstat.zimmeranz

            if zinrstat.datum == to_date:

                if main_nr == 800:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                    if w12:
                        w12.tday =  to_decimal(w12.tday) + to_decimal(zinrstat.zimmeranz)

                    if w13:
                        w13.tday =  to_decimal(w13.tday) + to_decimal(zinrstat.personen)

                elif main_nr == 180:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(zinrstat.zimmeranz)

                    if w11:
                        w11.tday =  to_decimal(w11.tday) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                    if w13:
                        w13.tday =  to_decimal(w13.tday) + to_decimal(zinrstat.personen)

                elif main_nr == 181:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(zinrstat.personen)

                    if w11:
                        w11.tday =  to_decimal(w11.tday) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                    if w12:
                        w12.tday =  to_decimal(w12.tday) + to_decimal(zinrstat.zimmeranz)

            if zinrstat.datum < from_date:

                if main_nr == 800:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                    if w12:
                        w12.ytd_saldo =  to_decimal(w12.ytd_saldo) + to_decimal(zinrstat.zimmeranz)

                    if w13:
                        w13.ytd_saldo =  to_decimal(w13.ytd_saldo) + to_decimal(zinrstat.personen)

                elif main_nr == 180:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.zimmeranz)

                    if w11:
                        w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                    if w13:
                        w13.ytd_saldo =  to_decimal(w13.ytd_saldo) + to_decimal(zinrstat.personen)

                elif main_nr == 181:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.personen)

                    if w11:
                        w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                    if w12:
                        w12.ytd_saldo =  to_decimal(w12.ytd_saldo) + to_decimal(zinrstat.zimmeranz)
            else:

                if main_nr == 800:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                    if w12:
                        w12.saldo =  to_decimal(w12.saldo) + to_decimal(zinrstat.zimmeranz)

                    if w13:
                        w13.saldo =  to_decimal(w13.saldo) + to_decimal(zinrstat.personen)

                elif main_nr == 180:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(zinrstat.zimmeranz)

                    if w11:
                        w11.saldo =  to_decimal(w11.saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                    if w13:
                        w13.saldo =  to_decimal(w13.saldo) + to_decimal(zinrstat.personen)

                elif main_nr == 181:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(zinrstat.personen)

                    if w11:
                        w11.saldo =  to_decimal(w11.saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                    if w12:
                        w12.saldo =  to_decimal(w12.saldo) + to_decimal(zinrstat.zimmeranz)

                if ytd_flag:

                    if main_nr == 800:
                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                        if w12:
                            w12.ytd_saldo =  to_decimal(w12.ytd_saldo) + to_decimal(zinrstat.zimmeranz)

                        if w13:
                            w13.ytd_saldo =  to_decimal(w13.ytd_saldo) + to_decimal(zinrstat.personen)

                    elif main_nr == 180:
                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.zimmeranz)

                        if w11:
                            w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                        if w13:
                            w13.ytd_saldo =  to_decimal(w13.ytd_saldo) + to_decimal(zinrstat.personen)

                    elif main_nr == 181:
                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.personen)

                        if w11:
                            w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                        if w12:
                            w12.ytd_saldo =  to_decimal(w12.ytd_saldo) + to_decimal(zinrstat.zimmeranz)

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= datum1) & (Zinrstat.datum <= lto_date) & (Zinrstat.zinr == (s_rmno).lower())).order_by(Zinrstat._recid).all():

                if foreign_flag:
                    find_exrate(zinrstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)

                if zinrstat.datum < lfrom_date:

                    if main_nr == 800:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                        if w12:
                            w12.lytd_saldo =  to_decimal(w12.lytd_saldo) + to_decimal(zinrstat.zimmeranz)

                        if w13:
                            w13.lytd_saldo =  to_decimal(w13.lytd_saldo) + to_decimal(zinrstat.personen)

                    elif main_nr == 180:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.zimmeranz)

                        if w11:
                            w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                        if w13:
                            w13.lytd_saldo =  to_decimal(w13.lytd_saldo) + to_decimal(zinrstat.personen)

                    elif main_nr == 181:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.personen)

                        if w11:
                            w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                        if w12:
                            w12.lytd_saldo =  to_decimal(w12.lytd_saldo) + to_decimal(zinrstat.zimmeranz)
                else:

                    if main_nr == 800:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                        if w12:
                            w12.lastyr =  to_decimal(w12.lastyr) + to_decimal(zinrstat.zimmeranz)

                        if w13:
                            w13.lastyr =  to_decimal(w13.lastyr) + to_decimal(zinrstat.personen)

                    elif main_nr == 180:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(zinrstat.zimmeranz)

                        if w11:
                            w11.lastyr =  to_decimal(w11.lastyr) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                        if w13:
                            w13.lastyr =  to_decimal(w13.lastyr) + to_decimal(zinrstat.personen)

                    elif main_nr == 181:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(zinrstat.personen)

                        if w11:
                            w11.lastyr =  to_decimal(w11.lastyr) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                        if w12:
                            w12.lastyr =  to_decimal(w12.lastyr) + to_decimal(zinrstat.zimmeranz)

                    if lytd_flag:

                        if main_nr == 800:
                            w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                            if w12:
                                w12.lytd_saldo =  to_decimal(w12.lytd_saldo) + to_decimal(zinrstat.zimmeranz)

                            if w13:
                                w13.lytd_saldo =  to_decimal(w13.lytd_saldo) + to_decimal(zinrstat.personen)

                        elif main_nr == 180:
                            w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.zimmeranz)

                            if w11:
                                w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                            if w13:
                                w13.lytd_saldo =  to_decimal(w13.lytd_saldo) + to_decimal(zinrstat.personen)

                        elif main_nr == 181:
                            w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.personen)

                            if w11:
                                w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                            if w12:
                                w12.lytd_saldo =  to_decimal(w12.lytd_saldo) + to_decimal(zinrstat.zimmeranz)

        if pmtd_flag:

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= pfrom_date) & (Zinrstat.datum <= pto_date) & (Zinrstat.zinr == (s_rmno).lower())).order_by(Zinrstat._recid).all():

                if foreign_flag:
                    find_exrate(zinrstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)

                if main_nr == 800:
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                    if w12:
                        w12.lastmon =  to_decimal(w12.lastmon) + to_decimal(zinrstat.zimmeranz)

                    if w13:
                        w13.lastmon =  to_decimal(w13.lastmon) + to_decimal(zinrstat.personen)

                elif main_nr == 180:
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(zinrstat.zimmeranz)

                    if w11:
                        w11.lastmon =  to_decimal(w11.lastmon) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                    if w13:
                        w13.lastmon =  to_decimal(w13.lastmon) + to_decimal(zinrstat.personen)

                elif main_nr == 181:
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(zinrstat.personen)

                    if w11:
                        w11.lastmon =  to_decimal(w11.lastmon) + to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                    if w12:
                        w12.lastmon =  to_decimal(w12.lastmon) + to_decimal(zinrstat.zimmeranz)


        if lytoday_flag:

            zinrstat = get_cache (Zinrstat, {"datum": [(eq, lytoday)],"zinr": [(eq, s_rmno)]})

        if zinrstat:

            if foreign_flag:
                find_exrate(zinrstat.datum)

                if exrate:
                    frate =  to_decimal(exrate.betrag)

            if main_nr == 800:
                w1.lytoday =  to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                if w12:
                    w12.lytoday =  to_decimal(zinrstat.zimmeranz)

                if w13:
                    w13.lytoday =  to_decimal(zinrstat.personen)

            elif main_nr == 180:
                w1.lytoday =  to_decimal(zinrstat.zimmeranz)

                if w11:
                    w11.lytoday =  to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                if w13:
                    w13.lytoday =  to_decimal(zinrstat.personen)

            elif main_nr == 181:
                w1.lytoday =  to_decimal(zinrstat.personen)

                if w11:
                    w11.lytoday =  to_decimal(zinrstat.logisumsatz) / to_decimal(frate)

                if w12:
                    w12.lytoday =  to_decimal(zinrstat.zimmeranz)
        w1.done = True

        if w11:
            w11.done = True

        if w12:
            w12.done = True

        if w13:
            w13.done = True


    def find_exrate(curr_date:date):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        if foreign_nr != 0:

            exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, curr_date)]})
        else:

            exrate = get_cache (Exrate, {"datum": [(eq, curr_date)]})


    def cal_fbcost(artnr:int, dept:int, datum:date):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        cost = to_decimal("0.0")

        def generate_inner_output():
            return (cost)


        h_cost = get_cache (H_cost, {"artnr": [(eq, artnr)],"departement": [(eq, dept)],"datum": [(eq, datum)],"flag": [(eq, 1)]})

        if h_cost and h_cost.betrag != 0:
            cost =  to_decimal(h_cost.anzahl) * to_decimal(h_cost.betrag)
        else:

            for h_journal in db_session.query(H_journal).filter(
                     (H_journal.artnr == artnr) & (H_journal.departement == dept) & (H_journal.bill_datum == datum)).order_by(H_journal._recid).all():
                cost =  to_decimal(cost) + to_decimal(h_journal.betrag) * to_decimal(h_artikel.prozent) / to_decimal("100")

        return generate_inner_output()


    def fill_wig(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        curr_date:date = None
        wig_gastnr:int = 0
        d_flag:bool = False

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 109)]})
        wig_gastnr = htparam.finteger

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum >= datum1) & (Genstat.datum <= to_date) & (Genstat.gastnrmember > 0) & (Genstat.gastnr == wig_gastnr) & (Genstat.zinr != "") & (Genstat.resstatus != 13)).order_by(Genstat.datum).all():
            d_flag = (get_month(genstat.datum) == get_month(to_date)) and (get_year(genstat.datum) == get_year(to_date))

            if d_flag:
                w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + 1

            if genstat.datum == to_date:
                w1.tday =  to_decimal(w1.tday) + to_decimal("1")

            if genstat.datum < from_date:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal("1")
            else:
                w1.saldo =  to_decimal(w1.saldo) + to_decimal("1")

                if ytd_flag:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal("1")


    def fill_new_wig(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        curr_date:date = None
        wig_gastnr:int = 0
        ci_date:date = None
        datum:date = None
        walk_in:int = 0
        wi_grp:int = 0
        d_flag:bool = False

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
        ci_date = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 109)]})
        wig_gastnr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 48)]})

        segment = get_cache (Segment, {"segmentcode": [(eq, htparam.finteger)]})

        if segment:
            walk_in = htparam.finteger
            wi_grp = segment.segmentgrup

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date
        for datum in date_range(datum1,to_date) :

            if datum >= ci_date:

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12)).order_by(Res_line.zinr).all():

                    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                    if segment.segmentcode == walk_in and segment.segmentgrup != 0:
                        d_flag = (get_month(datum) == get_month(to_date)) and (get_year(datum) == get_year(to_date))

                        if d_flag:
                            w1.mon_saldo[get_day(datum) - 1] = w1.mon_saldo[get_day(datum) - 1] + res_line.zimmeranz

                        if datum == to_date:
                            w1.tday =  to_decimal(w1.tday) + to_decimal(res_line.zimmeranz)

                        if datum >= date_mdy(get_month(to_date) , 1, get_year(to_date)):
                            w1.saldo =  to_decimal(w1.saldo) + to_decimal(res_line.zimmeranz)

                        if ytd_flag:
                            w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(res_line.zimmeranz)

            elif datum < ci_date:

                genstat_obj_list = {}
                for genstat, zinrstat in db_session.query(Genstat, Zinrstat).join(Zinrstat,(Zinrstat.datum == Genstat.datum) & (Zinrstat.zinr == Genstat.zinr)).filter(
                         (Genstat.datum == datum) & (Genstat.gastnrmember > 0) & (Genstat.zinr != "") & (Genstat.resstatus != 13)).order_by(Genstat._recid).all():
                    if genstat_obj_list.get(genstat._recid):
                        continue
                    else:
                        genstat_obj_list[genstat._recid] = True

                    segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                    if segment:

                        if segment.segmentcode == walk_in:
                            d_flag = (get_month(genstat.datum) == get_month(to_date)) and (get_year(genstat.datum) == get_year(to_date))

                            if d_flag:
                                w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + 1

                            if genstat.datum == to_date:
                                w1.tday =  to_decimal(w1.tday) + to_decimal("1")

                            if datum >= date_mdy(get_month(to_date) , 1, get_year(to_date)):
                                w1.saldo =  to_decimal(w1.saldo) + to_decimal("1")

                            if ytd_flag:
                                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal("1")


    def fill_cover_shift1(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        curr_date:date = None
        curr_i:int = 0
        curr_rechnr:int = 0
        billnr:int = 0
        i:int = 0
        found:bool = False
        hbuff = None
        Hbuff =  create_buffer("Hbuff",H_umsatz)

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.bill_datum >= datum1) & (H_bill_line.bill_datum <= to_date) & (H_bill_line.departement == w1.dept)).order_by(H_bill_line.rechnr, H_bill_line.sysdate.desc(), H_bill_line.zeit).all():

            if h_bill_line.artnr != 0:

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)],"artart": [(gt, 0)]})

                if h_artikel:

                    if curr_rechnr != h_bill_line.rechnr:

                        h_bill = get_cache (H_bill, {"rechnr": [(eq, h_bill_line.rechnr)],"departement": [(eq, h_bill_line.departement)]})

                        if h_bill:

                            if h_bill_line.bill_datum == to_date:

                                if h_bill_line.betriebsnr == 1:

                                    if w1.main_code == 2013:
                                        w1.tday =  to_decimal(w1.tday) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 2:

                                    if w1.main_code == 2014:
                                        w1.tday =  to_decimal(w1.tday) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 3:

                                    if w1.main_code == 2015:
                                        w1.tday =  to_decimal(w1.tday) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 4:

                                    if w1.main_code == 2016:
                                        w1.tday =  to_decimal(w1.tday) + to_decimal(h_bill.belegung)

                            elif h_bill_line.bill_datum >= from_date:

                                if h_bill_line.betriebsnr == 1:

                                    if w1.main_code == 2013:
                                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 2:

                                    if w1.main_code == 2014:
                                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 3:

                                    if w1.main_code == 2015:
                                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 4:

                                    if w1.main_code == 2016:
                                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_bill.belegung)

                            if h_bill_line.betriebsnr == 1:

                                if w1.main_code == 2013:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_bill.belegung)

                            if h_bill_line.betriebsnr == 2:

                                if w1.main_code == 2014:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_bill.belegung)

                            if h_bill_line.betriebsnr == 3:

                                if w1.main_code == 2015:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_bill.belegung)

                            if h_bill_line.betriebsnr == 4:

                                if w1.main_code == 2016:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_bill.belegung)
                    curr_rechnr = h_bill_line.rechnr

            elif h_bill_line.artnr == 0:
                i = 0
                found = no
                billnr = 0


                while not found:
                    i = i + 1

                    if substring(h_bill_line.bezeich, i - 1, 1) == ("*").lower() :
                        found = True
                billnr = to_int(substring(h_bill_line.bezeich, i + 1 - 1, length(h_bill_line.bezeich) - i))

                if billnr != 0:

                    bill = get_cache (Bill, {"rechnr": [(eq, billnr)]})

                    if bill and bill.zinr != " ":

                        h_bill = get_cache (H_bill, {"rechnr": [(eq, h_bill_line.rechnr)],"departement": [(eq, h_bill_line.departement)]})

                        if h_bill:

                            if h_bill_line.bill_datum == to_date:

                                if h_bill_line.betriebsnr == 1:

                                    if w1.main_code == 2009:
                                        w1.tday =  to_decimal(w1.tday) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 2:

                                    if w1.main_code == 2010:
                                        w1.tday =  to_decimal(w1.tday) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 3:

                                    if w1.main_code == 2011:
                                        w1.tday =  to_decimal(w1.tday) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 4:

                                    if w1.main_code == 2012:
                                        w1.tday =  to_decimal(w1.tday) + to_decimal(h_bill.belegung)

                            elif h_bill_line.bill_datum >= from_date:

                                if h_bill_line.betriebsnr == 1:

                                    if w1.main_code == 2009:
                                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 2:

                                    if w1.main_code == 2010:
                                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 3:

                                    if w1.main_code == 2011:
                                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 4:

                                    if w1.main_code == 2012:
                                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_bill.belegung)

                            if h_bill_line.betriebsnr == 1:

                                if w1.main_code == 2009:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_bill.belegung)

                            if h_bill_line.betriebsnr == 2:

                                if w1.main_code == 2010:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_bill.belegung)

                            if h_bill_line.betriebsnr == 3:

                                if w1.main_code == 2011:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_bill.belegung)

                            if h_bill_line.betriebsnr == 4:

                                if w1.main_code == 2012:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_bill.belegung)


    def fill_cover_shift2(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        curr_date:date = None
        curr_i:int = 0
        curr_rechnr:int = 0
        billnr:int = 0
        i:int = 0
        found:bool = False
        hbuff = None
        Hbuff =  create_buffer("Hbuff",H_umsatz)

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.bill_datum >= datum1) & (H_bill_line.bill_datum <= to_date) & (H_bill_line.departement == w1.dept)).order_by(H_bill_line.rechnr, H_bill_line.sysdate.desc(), H_bill_line.zeit).all():

            if h_bill_line.artnr != 0:

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)],"artart": [(gt, 0),(ne, 11),(ne, 12)]})

                if h_artikel:

                    if curr_rechnr != h_bill_line.rechnr:

                        h_bill = get_cache (H_bill, {"rechnr": [(eq, h_bill_line.rechnr)],"departement": [(eq, h_bill_line.departement)]})

                        if h_bill:

                            if h_bill_line.bill_datum == to_date:

                                if h_bill_line.betriebsnr == 1:

                                    if w1.main_code == 2013:
                                        w1.tday =  to_decimal(w1.tday) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 2:

                                    if w1.main_code == 2014:
                                        w1.tday =  to_decimal(w1.tday) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 3:

                                    if w1.main_code == 2015:
                                        w1.tday =  to_decimal(w1.tday) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 4:

                                    if w1.main_code == 2016:
                                        w1.tday =  to_decimal(w1.tday) + to_decimal(h_bill.belegung)

                            elif h_bill_line.bill_datum >= from_date:

                                if h_bill_line.betriebsnr == 1:

                                    if w1.main_code == 2013:
                                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 2:

                                    if w1.main_code == 2014:
                                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 3:

                                    if w1.main_code == 2015:
                                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 4:

                                    if w1.main_code == 2016:
                                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_bill.belegung)

                            if h_bill_line.betriebsnr == 1:

                                if w1.main_code == 2013:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_bill.belegung)

                            if h_bill_line.betriebsnr == 2:

                                if w1.main_code == 2014:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_bill.belegung)

                            if h_bill_line.betriebsnr == 3:

                                if w1.main_code == 2015:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_bill.belegung)

                            if h_bill_line.betriebsnr == 4:

                                if w1.main_code == 2016:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_bill.belegung)
                    curr_rechnr = h_bill_line.rechnr

            elif h_bill_line.artnr == 0:
                i = 0
                found = no
                billnr = 0


                while not found:
                    i = i + 1

                    if substring(h_bill_line.bezeich, i - 1, 1) == ("*").lower() :
                        found = True
                billnr = to_int(substring(h_bill_line.bezeich, i + 1 - 1, length(h_bill_line.bezeich) - i))

                if billnr != 0:

                    bill = get_cache (Bill, {"rechnr": [(eq, billnr)]})

                    if bill and bill.zinr != " ":

                        h_bill = get_cache (H_bill, {"rechnr": [(eq, h_bill_line.rechnr)],"departement": [(eq, h_bill_line.departement)]})

                        if h_bill:

                            if h_bill_line.bill_datum == to_date:

                                if h_bill_line.betriebsnr == 1:

                                    if w1.main_code == 2009:
                                        w1.tday =  to_decimal(w1.tday) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 2:

                                    if w1.main_code == 2010:
                                        w1.tday =  to_decimal(w1.tday) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 3:

                                    if w1.main_code == 2011:
                                        w1.tday =  to_decimal(w1.tday) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 4:

                                    if w1.main_code == 2012:
                                        w1.tday =  to_decimal(w1.tday) + to_decimal(h_bill.belegung)

                            elif h_bill_line.bill_datum >= from_date:

                                if h_bill_line.betriebsnr == 1:

                                    if w1.main_code == 2009:
                                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 2:

                                    if w1.main_code == 2010:
                                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 3:

                                    if w1.main_code == 2011:
                                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_bill.belegung)

                                if h_bill_line.betriebsnr == 4:

                                    if w1.main_code == 2012:
                                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_bill.belegung)

                            if h_bill_line.betriebsnr == 1:

                                if w1.main_code == 2009:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_bill.belegung)

                            if h_bill_line.betriebsnr == 2:

                                if w1.main_code == 2010:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_bill.belegung)

                            if h_bill_line.betriebsnr == 3:

                                if w1.main_code == 2011:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_bill.belegung)

                            if h_bill_line.betriebsnr == 4:

                                if w1.main_code == 2012:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_bill.belegung)


    def fill_cover_shift(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        curr_date:date = None
        curr_i:int = 0
        hbuff = None
        Hbuff =  create_buffer("Hbuff",H_umsatz)

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for h_umsatz in db_session.query(H_umsatz).filter(
                 (H_umsatz.datum >= datum1) & (H_umsatz.datum <= to_date) & (H_umsatz.artnr == 0) & (H_umsatz.departement == w1.dept)).order_by(H_umsatz._recid).all():

            if h_umsatz.epreis == 1:

                if h_umsatz.datum == to_date:

                    if w1.main_code == 1921:
                        w1.tday =  to_decimal(h_umsatz.betrag)

                    if w1.main_code == 1971:
                        w1.tday =  to_decimal(h_umsatz.nettobetrag)

                    if w1.main_code == 1991:
                        w1.tday =  to_decimal(h_umsatz.anzahl)

                if h_umsatz.datum >= from_date:

                    if w1.main_code == 1921:
                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_umsatz.betrag)

                    if w1.main_code == 1971:
                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_umsatz.nettobetrag)

                    if w1.main_code == 1991:
                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_umsatz.anzahl)

                if w1.main_code == 1921:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_umsatz.betrag)

                if w1.main_code == 1971:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_umsatz.nettobetrag)

                if w1.main_code == 1991:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_umsatz.anzahl)

            if h_umsatz.epreis == 2:

                if h_umsatz.datum == to_date:

                    if w1.main_code == 1922:
                        w1.tday =  to_decimal(h_umsatz.betrag)

                    if w1.main_code == 1972:
                        w1.tday =  to_decimal(h_umsatz.nettobetrag)

                    if w1.main_code == 1992:
                        w1.tday =  to_decimal(h_umsatz.anzahl)

                if h_umsatz.datum >= from_date:

                    if w1.main_code == 1922:
                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_umsatz.betrag)

                    if w1.main_code == 1972:
                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_umsatz.nettobetrag)

                    if w1.main_code == 1992:
                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_umsatz.anzahl)

                if w1.main_code == 1922:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_umsatz.betrag)

                if w1.main_code == 1972:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_umsatz.nettobetrag)

                if w1.main_code == 1992:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_umsatz.anzahl)

            if h_umsatz.epreis == 3:

                if h_umsatz.datum == to_date:

                    if w1.main_code == 1923:
                        w1.tday =  to_decimal(h_umsatz.betrag)

                    if w1.main_code == 1973:
                        w1.tday =  to_decimal(h_umsatz.nettobetrag)

                    if w1.main_code == 1993:
                        w1.tday =  to_decimal(h_umsatz.anzahl)

                if h_umsatz.datum >= from_date:

                    if w1.main_code == 1923:
                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_umsatz.betrag)

                    if w1.main_code == 1973:
                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_umsatz.nettobetrag)

                    if w1.main_code == 1993:
                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_umsatz.anzahl)

                if w1.main_code == 1923:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_umsatz.betrag)

                if w1.main_code == 1973:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_umsatz.nettobetrag)

                if w1.main_code == 1993:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_umsatz.anzahl)

            if h_umsatz.epreis == 4:

                if h_umsatz.datum == to_date:

                    if w1.main_code == 1924:
                        w1.tday =  to_decimal(h_umsatz.betrag)

                    if w1.main_code == 1974:
                        w1.tday =  to_decimal(h_umsatz.nettobetrag)

                    if w1.main_code == 1994:
                        w1.tday =  to_decimal(h_umsatz.anzahl)

                if h_umsatz.datum >= from_date:

                    if w1.main_code == 1924:
                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_umsatz.betrag)

                    if w1.main_code == 1974:
                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_umsatz.nettobetrag)

                    if w1.main_code == 1994:
                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(h_umsatz.anzahl)

                if w1.main_code == 1924:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_umsatz.betrag)

                if w1.main_code == 1974:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_umsatz.nettobetrag)

                if w1.main_code == 1994:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(h_umsatz.anzahl)

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            for h_umsatz in db_session.query(H_umsatz).filter(
                     (H_umsatz.datum >= datum1) & (H_umsatz.datum <= lto_date) & (H_umsatz.artnr == 0) & (H_umsatz.departement == w1.dept)).order_by(H_umsatz._recid).all():

                if h_umsatz.epreis == 1:

                    if h_umsatz.datum >= lfrom_date:

                        if w1.main_code == 1921:
                            w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(h_umsatz.betrag)

                        if w1.main_code == 1971:
                            w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(h_umsatz.nettobetrag)

                        if w1.main_code == 1991:
                            w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(h_umsatz.anzahl)

                    if w1.main_code == 1921:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(h_umsatz.betrag)

                    if w1.main_code == 1971:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(h_umsatz.nettobetrag)

                    if w1.main_code == 1991:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(h_umsatz.anzahl)

                if h_umsatz.epreis == 2:

                    if h_umsatz.datum >= lfrom_date:

                        if w1.main_code == 1922:
                            w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(h_umsatz.betrag)

                        if w1.main_code == 1972:
                            w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(h_umsatz.nettobetrag)

                        if w1.main_code == 1992:
                            w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(h_umsatz.anzahl)

                    if w1.main_code == 1922:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(h_umsatz.betrag)

                    if w1.main_code == 1972:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(h_umsatz.nettobetrag)

                    if w1.main_code == 1992:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(h_umsatz.anzahl)

                if h_umsatz.epreis == 3:

                    if h_umsatz.datum >= lfrom_date:

                        if w1.main_code == 1923:
                            w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(h_umsatz.betrag)

                        if w1.main_code == 1973:
                            w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(h_umsatz.nettobetrag)

                        if w1.main_code == 1993:
                            w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(h_umsatz.anzahl)

                    if w1.main_code == 1923:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(h_umsatz.betrag)

                    if w1.main_code == 1973:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(h_umsatz.nettobetrag)

                    if w1.main_code == 1993:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(h_umsatz.anzahl)

                if h_umsatz.epreis == 4:

                    if h_umsatz.datum >= lfrom_date:

                        if w1.main_code == 1924:
                            w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(h_umsatz.betrag)

                        if w1.main_code == 1974:
                            w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(h_umsatz.nettobetrag)

                        if w1.main_code == 1994:
                            w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(h_umsatz.anzahl)

                    if w1.main_code == 1924:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(h_umsatz.betrag)

                    if w1.main_code == 1974:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(h_umsatz.nettobetrag)

                    if w1.main_code == 1994:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(h_umsatz.anzahl)


    def fill_los():

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        done = False
        datum1:date = None
        datum:date = None
        ci_date:date = None
        end_date:date = None
        start_date:date = None
        i:int = 0
        los:int = 0
        mon_saldo1:List[Decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo2:List[Decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo3:List[Decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo4:List[Decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo5:List[Decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo6:List[Decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo7:List[Decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo8:List[Decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo9:List[Decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo10:List[Decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo11:List[Decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo12:List[Decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        def generate_inner_output():
            return (done)


        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
        ci_date = htparam.fdate
        Wlos = W1
        wlos_list = w1_list

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        wlos = query(wlos_list, filters=(lambda wlos: wlos.main_code == 9000), first=True)

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.abreise >= datum1) & (Res_line.ankunf <= to_date) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.zinr != "") & (Res_line.l_zuordnung[inc_value(0)] != 0) & (Res_line.resstatus != 9) & (Res_line.resstatus != 99) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12)).order_by(Res_line._recid).all():

            if res_line.ankunft == to_date and res_line.active_flag != 1:
                pass
            else:

                if res_line.abreise == res_line.ankunft:
                    end_date = res_line.abreise
                else:
                    end_date = res_line.abreise - timedelta(days=1)

                if end_date > to_date:
                    end_date = to_date

                if res_line.ankunft < datum1:
                    start_date = datum1
                else:
                    start_date = res_line.ankunft
                for datum in date_range(start_date,end_date) :

                    if res_line.abreise - datum == 0:
                        los = 1
                    else:
                        los = (res_line.abreise - datum).days

                    if datum == to_date:
                        wlos.tday =  to_decimal(wlos.tday) + to_decimal(los)

                    if get_month(datum) == get_month(to_date) and get_year(datum) == get_year(to_date):
                        wlos.mon_saldo[get_day(datum) - 1] = wlos.mon_saldo[get_day(datum) - 1] + los

                    if get_month(datum) == 1:
                        mon_saldo1[get_day(datum) - 1] = mon_saldo1[get_day(datum) - 1] + los

                    elif get_month(datum) == 2:
                        mon_saldo2[get_day(datum) - 1] = mon_saldo2[get_day(datum) - 1] + los

                    elif get_month(datum) == 3:
                        mon_saldo3[get_day(datum) - 1] = mon_saldo3[get_day(datum) - 1] + los

                    elif get_month(datum) == 4:
                        mon_saldo4[get_day(datum) - 1] = mon_saldo4[get_day(datum) - 1] + los

                    elif get_month(datum) == 5:
                        mon_saldo5[get_day(datum) - 1] = mon_saldo5[get_day(datum) - 1] + los

                    elif get_month(datum) == 6:
                        mon_saldo6[get_day(datum) - 1] = mon_saldo6[get_day(datum) - 1] + los

                    elif get_month(datum) == 7:
                        mon_saldo7[get_day(datum) - 1] = mon_saldo7[get_day(datum) - 1] + los

                    elif get_month(datum) == 8:
                        mon_saldo8[get_day(datum) - 1] = mon_saldo8[get_day(datum) - 1] + los

                    elif get_month(datum) == 9:
                        mon_saldo9[get_day(datum) - 1] = mon_saldo9[get_day(datum) - 1] + los

                    elif get_month(datum) == 10:
                        mon_saldo10[get_day(datum) - 1] = mon_saldo10[get_day(datum) - 1] + los

                    elif get_month(datum) == 11:
                        mon_saldo11[get_day(datum) - 1] = mon_saldo11[get_day(datum) - 1] + los

                    elif get_month(datum) == 12:
                        mon_saldo12[get_day(datum) - 1] = mon_saldo12[get_day(datum) - 1] + los
        for i in range(1,31 + 1) :
            wlos.saldo =  to_decimal(wlos.saldo) + to_decimal(wlos.mon_saldo[i - 1])
            wlos.ytd_saldo =  to_decimal(wlos.ytd_saldo) + to_decimal(mon_saldo1[i - 1] + mon_saldo2[i - 1] + mon_saldo3[i - 1] + mon_saldo4[i - 1] + mon_saldo5[i - 1] + mon_saldo6[i - 1] + mon_saldo7[i - 1] + mon_saldo8[i - 1] + mon_saldo9[i - 1] + mon_saldo10[i - 1] + mon_saldo11[i - 1] + mon_saldo12[i - 1])
        done = True

        return generate_inner_output()


    def fill_pax_cover_shift():

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        done = False
        datum1:date = None
        disc_art1:int = 0
        disc_art2:int = 0
        disc_art3:int = 0
        buff = None
        art_buff = None
        shift:int = 0
        temp1:string = ""
        temp2:string = ""
        do_it:bool = True

        def generate_inner_output():
            return (done)

        Buff =  create_buffer("Buff",H_bill_line)
        Art_buff =  create_buffer("Art_buff",H_artikel)
        Wspc = W1
        wspc_list = w1_list
        disc_art1 = get_output(htpint(557))
        disc_art2 = get_output(htpint(596))

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 5) & (Queasy.number3 != 0)).order_by(Queasy.number1).all():
            shift_list = Shift_list()
            shift_list_list.append(shift_list)

            shift_list.shift = queasy.number3
            temp1 = to_string(queasy.number1, "9999")
            temp2 = to_string(queasy.number2, "9999")
            shift_list.ftime = (to_int(substring(temp1, 0, 2)) * 3600) + (to_int(substring(temp1, 2, 2)) * 60)
            shift_list.ttime = (to_int(substring(temp2, 0, 2)) * 3600) + (to_int(substring(temp2, 2, 2)) * 60)

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date
        t_list_list.clear()

        h_bill_line_obj_list = {}
        h_bill_line = H_bill_line()
        h_artikel = H_artikel()
        artikel = Artikel()
        h_bill = H_bill()
        for h_bill_line.artnr, h_bill_line.departement, h_bill_line.rechnr, h_bill_line.bezeich, h_bill_line.zeit, h_bill_line.bill_datum, h_bill_line.betriebsnr, h_bill_line.tischnr, h_bill_line.betrag, h_bill_line.anzahl, h_bill_line._recid, h_artikel.departement, h_artikel.artnr, h_artikel.service_code, h_artikel.mwst_code, h_artikel.prozent, h_artikel.artnrfront, h_artikel.artart, h_artikel._recid, artikel.departement, artikel.artnrfront, artikel.artnr, artikel.umsatzart, artikel.endkum, artikel._recid, h_bill.belegung, h_bill.resnr, h_bill.reslinnr, h_bill._recid in db_session.query(H_bill_line.artnr, H_bill_line.departement, H_bill_line.rechnr, H_bill_line.bezeich, H_bill_line.zeit, H_bill_line.bill_datum, H_bill_line.betriebsnr, H_bill_line.tischnr, H_bill_line.betrag, H_bill_line.anzahl, H_bill_line._recid, H_artikel.departement, H_artikel.artnr, H_artikel.service_code, H_artikel.mwst_code, H_artikel.prozent, H_artikel.artnrfront, H_artikel.artart, H_artikel._recid, Artikel.departement, Artikel.artnrfront, Artikel.artnr, Artikel.umsatzart, Artikel.endkum, Artikel._recid, H_bill.belegung, H_bill.resnr, H_bill.reslinnr, H_bill._recid).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0) & (H_artikel.artart != 11) & (H_artikel.artart != 12)).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement)).join(H_bill,(H_bill.rechnr == H_bill_line.rechnr) & (H_bill.departement == H_bill_line.departement)).filter(
                 (H_bill_line.bill_datum >= datum1) & (H_bill_line.bill_datum <= to_date) & (H_bill_line.artnr > 0) & (H_bill_line.artnr != disc_art1) & (H_bill_line.artnr != disc_art2) & (H_bill_line.artnr != disc_art3) & (H_bill_line.zeit >= 0) & (H_bill_line.epreis > 0)).order_by(H_bill_line.departement, H_bill_line.betriebsnr, H_bill_line.rechnr, H_bill_line.bill_datum).all():
            if h_bill_line_obj_list.get(h_bill_line._recid):
                continue
            else:
                h_bill_line_obj_list[h_bill_line._recid] = True


            do_it = True

            buff_obj_list = {}
            buff = H_bill_line()
            art_buff = H_artikel()
            for buff.artnr, buff.departement, buff.rechnr, buff.bezeich, buff.zeit, buff.bill_datum, buff.betriebsnr, buff.tischnr, buff.betrag, buff.anzahl, buff._recid, art_buff.departement, art_buff.artnr, art_buff.service_code, art_buff.mwst_code, art_buff.prozent, art_buff.artnrfront, art_buff.artart, art_buff._recid in db_session.query(Buff.artnr, Buff.departement, Buff.rechnr, Buff.bezeich, Buff.zeit, Buff.bill_datum, Buff.betriebsnr, Buff.tischnr, Buff.betrag, Buff.anzahl, Buff._recid, Art_buff.departement, Art_buff.artnr, Art_buff.service_code, Art_buff.mwst_code, Art_buff.prozent, Art_buff.artnrfront, Art_buff.artart, Art_buff._recid).join(Art_buff,(Art_buff.artnr == Buff.artnr) & (Art_buff.departement == Buff.departement)).filter(
                     (Buff.rechnr == h_bill_line.rechnr) & (Buff.departement == h_bill_line.departement)).order_by(Art_buff.artart).yield_per(100):
                if buff_obj_list.get(buff._recid):
                    continue
                else:
                    buff_obj_list[buff._recid] = True

                if art_buff.artart == 11 or art_buff.artart == 12:
                    do_it = False
                    break

            if do_it:
                shift = 0

                shift_list = query(shift_list_list, filters=(lambda shift_list: shift_list.ftime <= h_bill_line.zeit and shift_list.ttime >= h_bill_line.zeit), first=True)

                if shift_list:
                    shift = shift_list.shift

                t_list = query(t_list_list, filters=(lambda t_list: t_list.dept == h_bill_line.departement and t_list.datum == h_bill_line.bill_datum and t_list.shift == h_bill_line.betriebsnr), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.datum = h_bill_line.bill_datum
                    t_list.dept = h_bill_line.departement
                    t_list.shift = h_bill_line.betriebsnr

                t_rechnr = query(t_rechnr_list, filters=(lambda t_rechnr: t_rechnr.rechnr == h_bill_line.rechnr and t_rechnr.dept == h_bill_line.departement and t_rechnr.datum == h_bill_line.bill_datum and t_rechnr.shift == shift), first=True)

                if not t_rechnr:
                    t_rechnr = T_rechnr()
                    t_rechnr_list.append(t_rechnr)

                    t_rechnr.rechnr = h_bill_line.rechnr
                    t_rechnr.dept = h_bill_line.departement
                    t_rechnr.datum = h_bill_line.bill_datum
                    t_rechnr.shift = shift

                if artikel.umsatzart == 3 or artikel.umsatzart == 5 and not t_rechnr.found_food:
                    t_rechnr.found_food = True
                    t_list.pax_food = t_list.pax_food + h_bill.belegung

                if artikel.umsatzart == 6 and not t_rechnr.found_bev:
                    t_rechnr.found_bev = True
                    t_list.pax_bev = t_list.pax_bev + h_bill.belegung
        done = True

        for t_list in query(t_list_list, sort_by=[("dept",False),("shift",False),("datum",False)]):

            wspc = query(wspc_list, filters=(lambda wspc: wspc.main_code == 1995 and to_int(substring(wspc.s_artnr, 0, 2)) == t_list.dept and to_int(substring(wspc.s_artnr, 2)) == t_list.shift), first=True)

            if wspc:

                if t_list.datum == to_date:
                    wspc.tday =  to_decimal(wspc.tday) + to_decimal(t_list.pax_food)

                if get_month(t_list.datum) == get_month(to_date):
                    wspc.saldo =  to_decimal(wspc.saldo) + to_decimal(t_list.pax_food)
                wspc.ytd_saldo =  to_decimal(wspc.ytd_saldo) + to_decimal(t_list.pax_food)

            wspc = query(wspc_list, filters=(lambda wspc: wspc.main_code == 1996 and to_int(substring(wspc.s_artnr, 0, 2)) == t_list.dept and to_int(substring(wspc.s_artnr, 2)) == t_list.shift), first=True)

            if wspc:

                if t_list.datum == to_date:
                    wspc.tday =  to_decimal(wspc.tday) + to_decimal(t_list.pax_bev)

                if get_month(t_list.datum) == get_month(to_date):
                    wspc.saldo =  to_decimal(wspc.saldo) + to_decimal(t_list.pax_bev)
                wspc.ytd_saldo =  to_decimal(wspc.ytd_saldo) + to_decimal(t_list.pax_bev)

        return generate_inner_output()


    def fill_pax_cover_shift1(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        endkum:int = 0
        artnrfront:int = 0
        compli_flag:bool = False
        vat:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        netto:Decimal = to_decimal("0.0")
        curr_rechnr:int = 0
        curr_dept:int = 0
        temp_time:int = 0
        d_flag:bool = False
        counter:int = 0
        bh_artikel = None
        bh_bill_line = None
        Btemp_rechnr = Temp_rechnr
        btemp_rechnr_list = temp_rechnr_list
        Bh_artikel =  create_buffer("Bh_artikel",H_artikel)
        Bh_bill_line =  create_buffer("Bh_bill_line",H_bill_line)

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date
        curr_rechnr = 0

        temp_rechnr = query(temp_rechnr_list, first=True)

        if not temp_rechnr:

            h_bill_line_obj_list = {}
            h_bill_line = H_bill_line()
            h_artikel = H_artikel()
            h_bill = H_bill()
            for h_bill_line.artnr, h_bill_line.departement, h_bill_line.rechnr, h_bill_line.bezeich, h_bill_line.zeit, h_bill_line.bill_datum, h_bill_line.betriebsnr, h_bill_line.tischnr, h_bill_line.betrag, h_bill_line.anzahl, h_bill_line._recid, h_artikel.departement, h_artikel.artnr, h_artikel.service_code, h_artikel.mwst_code, h_artikel.prozent, h_artikel.artnrfront, h_artikel.artart, h_artikel._recid, h_bill.belegung, h_bill.resnr, h_bill.reslinnr, h_bill._recid in db_session.query(H_bill_line.artnr, H_bill_line.departement, H_bill_line.rechnr, H_bill_line.bezeich, H_bill_line.zeit, H_bill_line.bill_datum, H_bill_line.betriebsnr, H_bill_line.tischnr, H_bill_line.betrag, H_bill_line.anzahl, H_bill_line._recid, H_artikel.departement, H_artikel.artnr, H_artikel.service_code, H_artikel.mwst_code, H_artikel.prozent, H_artikel.artnrfront, H_artikel.artart, H_artikel._recid, H_bill.belegung, H_bill.resnr, H_bill.reslinnr, H_bill._recid).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement)).join(H_bill,(H_bill.rechnr == H_bill_line.rechnr) & (H_bill.departement == H_bill_line.departement)).filter(
                     (H_bill_line.bill_datum >= datum1) & (H_bill_line.bill_datum <= to_date) & (H_bill_line.artnr > 0)).order_by(H_bill_line.bill_datum, H_bill_line.departement, H_bill_line.rechnr, H_bill_line.betriebsnr).all():
                if h_bill_line_obj_list.get(h_bill_line._recid):
                    continue
                else:
                    h_bill_line_obj_list[h_bill_line._recid] = True

                if curr_rechnr != h_bill_line.rechnr:
                    temp_rechnr = Temp_rechnr()
                    temp_rechnr_list.append(temp_rechnr)

                    temp_rechnr.rechnr = h_bill_line.rechnr
                    temp_rechnr.shift = h_bill_line.betriebsnr
                    temp_rechnr.dept = h_bill_line.departement
                    temp_rechnr.datum = h_bill_line.bill_datum
                    temp_rechnr.belegung = h_bill.belegung
                    temp_rechnr.artnrfront = h_artikel.artnrfront
                    temp_rechnr.tischnr = h_bill_line.tischnr
                    temp_rechnr.betrag =  to_decimal(h_bill_line.betrag)
                    temp_rechnr.artnr = h_bill_line.artnr
                    temp_rechnr.artart = h_artikel.artart
                    temp_rechnr.resnr = h_bill.resnr
                    temp_rechnr.reslinnr = h_bill.reslinnr
                    curr_rechnr = h_bill_line.rechnr
                    curr_dept = h_bill_line.departement

                    bh_bill_line_obj_list = {}
                    bh_bill_line = H_bill_line()
                    bh_artikel = H_artikel()
                    for bh_bill_line.artnr, bh_bill_line.departement, bh_bill_line.rechnr, bh_bill_line.bezeich, bh_bill_line.zeit, bh_bill_line.bill_datum, bh_bill_line.betriebsnr, bh_bill_line.tischnr, bh_bill_line.betrag, bh_bill_line.anzahl, bh_bill_line._recid, bh_artikel.departement, bh_artikel.artnr, bh_artikel.service_code, bh_artikel.mwst_code, bh_artikel.prozent, bh_artikel.artnrfront, bh_artikel.artart, bh_artikel._recid in db_session.query(Bh_bill_line.artnr, Bh_bill_line.departement, Bh_bill_line.rechnr, Bh_bill_line.bezeich, Bh_bill_line.zeit, Bh_bill_line.bill_datum, Bh_bill_line.betriebsnr, Bh_bill_line.tischnr, Bh_bill_line.betrag, Bh_bill_line.anzahl, Bh_bill_line._recid, Bh_artikel.departement, Bh_artikel.artnr, Bh_artikel.service_code, Bh_artikel.mwst_code, Bh_artikel.prozent, Bh_artikel.artnrfront, Bh_artikel.artart, Bh_artikel._recid).join(Bh_artikel,(Bh_artikel.artnr == Bh_bill_line.artnr) & (Bh_artikel.departement == Bh_bill_line.departement) & (Bh_artikel.artart >= 11) & (Bh_artikel.artart <= 12)).filter(
                             (Bh_bill_line.rechnr == h_bill_line.rechnr) & (Bh_bill_line.departement == h_bill_line.departement)).order_by(Bh_artikel.artart.desc()).yield_per(100):
                        if bh_bill_line_obj_list.get(bh_bill_line._recid):
                            continue
                        else:
                            bh_bill_line_obj_list[bh_bill_line._recid] = True


                        temp_rechnr.compli_flag = True


                        break

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

                if artikel:

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        temp_rechnr.f_pax = h_bill.belegung
                        temp_rechnr.f_qty = temp_rechnr.f_qty + h_bill_line.anzahl

                    elif artikel.umsatzart == 6:
                        temp_rechnr.b_pax = h_bill.belegung
                        temp_rechnr.b_qty = temp_rechnr.b_qty + h_bill_line.anzahl

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        for temp_rechnr in query(temp_rechnr_list, filters=(lambda temp_rechnr: temp_rechnr.dept == w1.dept)):

            if (w1.main_code == 192 or w1.main_code == 197 or w1.main_code == 1995 or w1.main_code == 1996):

                if not temp_rechnr.compli_flag:

                    if w1.main_code == 192 or w1.main_code == 1995:

                        if temp_rechnr.datum == to_date:
                            w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.f_pax)

                        if get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):
                            w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.f_pax)

                        if ytd_flag:
                            w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.f_pax)
                        d_flag = (get_month(temp_rechnr.datum) == get_month(to_date)) and (get_year(temp_rechnr.datum) == get_year(to_date))

                        if d_flag:
                            w1.mon_saldo[get_day(temp_rechnr.datum) - 1] = w1.mon_saldo[get_day(temp_rechnr.datum) - 1] + temp_rechnr.f_pax

                    if w1.main_code == 197 or w1.main_code == 1996:

                        if temp_rechnr.datum == to_date:
                            w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.b_pax)

                        if get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):
                            w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.b_pax)

                        if ytd_flag:
                            w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.b_pax)
                        d_flag = (get_month(temp_rechnr.datum) == get_month(to_date)) and (get_year(temp_rechnr.datum) == get_year(to_date))

                        if d_flag:
                            w1.mon_saldo[get_day(temp_rechnr.datum) - 1] = w1.mon_saldo[get_day(temp_rechnr.datum) - 1] + temp_rechnr.b_pax

            elif w1.main_code == 2028:

                if temp_rechnr.datum == to_date:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.belegung)

                if get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.belegung)

                if ytd_flag:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.belegung)
                d_flag = (get_month(temp_rechnr.datum) == get_month(to_date)) and (get_year(temp_rechnr.datum) == get_year(to_date))

                if d_flag:
                    w1.mon_saldo[get_day(temp_rechnr.datum) - 1] = w1.mon_saldo[get_day(temp_rechnr.datum) - 1] + temp_rechnr.belegung

            elif w1.main_code == 552:

                if not temp_rechnr.compli_flag:

                    if temp_rechnr.datum == to_date:
                        w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.belegung)

                    if get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):
                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.belegung)

                    if ytd_flag:
                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.belegung)
                    d_flag = (get_month(temp_rechnr.datum) == get_month(to_date)) and (get_year(temp_rechnr.datum) == get_year(to_date))

                    if d_flag:
                        w1.mon_saldo[get_day(temp_rechnr.datum) - 1] = w1.mon_saldo[get_day(temp_rechnr.datum) - 1] + temp_rechnr.belegung

            elif w1.main_code == 2029:

                if temp_rechnr.datum == to_date:
                    w1.tday =  to_decimal(w1.tday) + to_decimal("1")

                if get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal("1")

                if ytd_flag:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal("1")
                d_flag = (get_month(temp_rechnr.datum) == get_month(to_date)) and (get_year(temp_rechnr.datum) == get_year(to_date))

                if d_flag:
                    w1.mon_saldo[get_day(temp_rechnr.datum) - 1] = w1.mon_saldo[get_day(temp_rechnr.datum) - 1] + 1

            elif w1.main_code == 2031 and w1.tischnr == temp_rechnr.tischnr:

                if temp_rechnr.datum == to_date:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.belegung)

                if get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.belegung)

                if ytd_flag:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.belegung)
                d_flag = (get_month(temp_rechnr.datum) == get_month(to_date)) and (get_year(temp_rechnr.datum) == get_year(to_date))

                if d_flag:
                    w1.mon_saldo[get_day(temp_rechnr.datum) - 1] = w1.mon_saldo[get_day(temp_rechnr.datum) - 1] + temp_rechnr.belegung

            elif (w1.main_code >= 2020 and w1.main_code <= 2027):

                if not temp_rechnr.compli_flag:

                    if temp_rechnr.shift == 1:

                        if temp_rechnr.datum == to_date:

                            if w1.main_code == 2020:
                                w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.f_pax)

                            if w1.main_code == 2024:
                                w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.b_pax)

                        if get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):

                            if w1.main_code == 2020:
                                w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.f_pax)

                            if w1.main_code == 2024:
                                w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.b_pax)

                        if ytd_flag:

                            if w1.main_code == 2020:
                                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.f_pax)

                            if w1.main_code == 2024:
                                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.b_pax)

                    if temp_rechnr.shift == 2:

                        if temp_rechnr.datum == to_date:

                            if w1.main_code == 2021:
                                w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.f_pax)

                            if w1.main_code == 2025:
                                w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.b_pax)

                        if get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):

                            if w1.main_code == 2021:
                                w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.f_pax)

                            if w1.main_code == 2025:
                                w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.b_pax)

                        if ytd_flag:

                            if w1.main_code == 2021:
                                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.f_pax)

                            if w1.main_code == 2025:
                                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.b_pax)

                    if temp_rechnr.shift == 3:

                        if temp_rechnr.datum == to_date:

                            if w1.main_code == 2022:
                                w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.f_pax)

                            if w1.main_code == 2026:
                                w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.b_pax)

                        if get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):

                            if w1.main_code == 2022:
                                w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.f_pax)

                            if w1.main_code == 2026:
                                w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.b_pax)

                        if ytd_flag:

                            if w1.main_code == 2022:
                                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.f_pax)

                            if w1.main_code == 2026:
                                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.b_pax)

                    if temp_rechnr.shift == 4:

                        if temp_rechnr.datum == to_date:

                            if w1.main_code == 2023:
                                w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.f_pax)

                            if w1.main_code == 2027:
                                w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.b_pax)

                        if get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):

                            if w1.main_code == 2023:
                                w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.f_pax)

                            if w1.main_code == 2027:
                                w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.b_pax)

                        if ytd_flag:

                            if w1.main_code == 2023:
                                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.f_pax)

                            if w1.main_code == 2027:
                                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.b_pax)

            elif (w1.main_code >= 2001 and w1.main_code <= 2004) or (w1.main_code >= 2032 and w1.main_code <= 2051):

                res_line = get_cache (Res_line, {"resnr": [(eq, temp_rechnr.resnr)],"reslinnr": [(eq, temp_rechnr.reslinnr)]})

                if res_line:

                    if temp_rechnr.datum == to_date:

                        if temp_rechnr.shift == 1:

                            if w1.main_code == 2001:
                                w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.belegung)

                        if temp_rechnr.shift == 2:

                            if w1.main_code == 2002:
                                w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.belegung)

                        if temp_rechnr.shift == 3:

                            if w1.main_code == 2003:
                                w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.belegung)

                        if temp_rechnr.shift == 4:

                            if w1.main_code == 2004:
                                w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.belegung)

                    if get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):

                        if temp_rechnr.shift == 1:

                            if w1.main_code == 2001:
                                w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.belegung)

                        if temp_rechnr.shift == 2:

                            if w1.main_code == 2002:
                                w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.belegung)

                        if temp_rechnr.shift == 3:

                            if w1.main_code == 2003:
                                w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.belegung)

                        if temp_rechnr.shift == 4:

                            if w1.main_code == 2004:
                                w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.belegung)
                    else:

                        if ytd_flag:

                            if temp_rechnr.shift == 1:

                                if w1.main_code == 2001:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.belegung)

                            if temp_rechnr.shift == 2:

                                if w1.main_code == 2002:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.belegung)

                            if temp_rechnr.shift == 3:

                                if w1.main_code == 2003:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.belegung)

                            if temp_rechnr.shift == 4:

                                if w1.main_code == 2004:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.belegung)

                    if temp_rechnr.compli_flag :

                        if temp_rechnr.datum == to_date:

                            if temp_rechnr.shift == 1:

                                if w1.main_code == 2032:
                                    w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.belegung)

                            if temp_rechnr.shift == 2:

                                if w1.main_code == 2033:
                                    w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.belegung)

                            if temp_rechnr.shift == 3:

                                if w1.main_code == 2034:
                                    w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.belegung)

                            if temp_rechnr.shift == 4:

                                if w1.main_code == 2035:
                                    w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.belegung)

                        if get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):

                            if temp_rechnr.shift == 1:

                                if w1.main_code == 2032:
                                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.belegung)

                            if temp_rechnr.shift == 2:

                                if w1.main_code == 2033:
                                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.belegung)

                            if temp_rechnr.shift == 3:

                                if w1.main_code == 2034:
                                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.belegung)

                            if temp_rechnr.shift == 4:

                                if w1.main_code == 2035:
                                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.belegung)
                        else:

                            if ytd_flag:

                                if temp_rechnr.shift == 1:

                                    if w1.main_code == 2032:
                                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.belegung)

                                if temp_rechnr.shift == 2:

                                    if w1.main_code == 2033:
                                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.belegung)

                                if temp_rechnr.shift == 3:

                                    if w1.main_code == 2034:
                                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.belegung)

                                if temp_rechnr.shift == 4:

                                    if w1.main_code == 2035:
                                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.belegung)

                    artikel = get_cache (Artikel, {"departement": [(eq, temp_rechnr.dept)],"artnr": [(eq, temp_rechnr.artnrfront)]})

                    if artikel:
                        netto =  to_decimal(temp_rechnr.betrag) / to_decimal((1) + to_decimal(vat) + to_decimal(vat2) + to_decimal(service))

                        if temp_rechnr.datum == to_date:

                            if temp_rechnr.shift == 1:

                                if w1.main_code == 2044:
                                    w1.tday =  to_decimal(w1.tday) + to_decimal(netto)

                            if temp_rechnr.shift == 2:

                                if w1.main_code == 2045:
                                    w1.tday =  to_decimal(w1.tday) + to_decimal(netto)

                            if temp_rechnr.shift == 3:

                                if w1.main_code == 2046:
                                    w1.tday =  to_decimal(w1.tday) + to_decimal(netto)

                            if temp_rechnr.shift == 4:

                                if w1.main_code == 2047:
                                    w1.tday =  to_decimal(w1.tday) + to_decimal(netto)

                        if get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):

                            if temp_rechnr.shift == 1:

                                if w1.main_code == 2044:
                                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(netto)

                            if temp_rechnr.shift == 2:

                                if w1.main_code == 2045:
                                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(netto)

                            if temp_rechnr.shift == 3:

                                if w1.main_code == 2046:
                                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(netto)

                            if temp_rechnr.shift == 4:

                                if w1.main_code == 2047:
                                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(netto)
                        else:

                            if ytd_flag:

                                if temp_rechnr.shift == 1:

                                    if w1.main_code == 2044:
                                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(netto)

                                if temp_rechnr.shift == 2:

                                    if w1.main_code == 2045:
                                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(netto)

                                if temp_rechnr.shift == 3:

                                    if w1.main_code == 2046:
                                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(netto)

                                if temp_rechnr.shift == 4:

                                    if w1.main_code == 2047:
                                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(netto)

                elif not res_line:

                    if temp_rechnr.datum == to_date:

                        if temp_rechnr.shift == 1:

                            if w1.main_code == 2036:
                                w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.belegung)

                        if temp_rechnr.shift == 2:

                            if w1.main_code == 2037:
                                w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.belegung)

                        if temp_rechnr.shift == 3:

                            if w1.main_code == 2038:
                                w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.belegung)

                        if temp_rechnr.shift == 4:

                            if w1.main_code == 2039:
                                w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.belegung)

                    if get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):

                        if temp_rechnr.shift == 1:

                            if w1.main_code == 2036:
                                w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.belegung)

                        if temp_rechnr.shift == 2:

                            if w1.main_code == 2037:
                                w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.belegung)

                        if temp_rechnr.shift == 3:

                            if w1.main_code == 2038:
                                w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.belegung)

                        if temp_rechnr.shift == 4:

                            if w1.main_code == 2039:
                                w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.belegung)
                    else:

                        if ytd_flag:

                            if temp_rechnr.shift == 1:

                                if w1.main_code == 2036:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.belegung)

                            if temp_rechnr.shift == 2:

                                if w1.main_code == 2037:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.belegung)

                            if temp_rechnr.shift == 3:

                                if w1.main_code == 2038:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.belegung)

                            if temp_rechnr.shift == 4:

                                if w1.main_code == 2039:
                                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.belegung)

                    if temp_rechnr.compli_flag :

                        if temp_rechnr.datum == to_date:

                            if temp_rechnr.shift == 1:

                                if w1.main_code == 2040:
                                    w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.belegung)

                            if temp_rechnr.shift == 2:

                                if w1.main_code == 2041:
                                    w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.belegung)

                            if temp_rechnr.shift == 3:

                                if w1.main_code == 2042:
                                    w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.belegung)

                            if temp_rechnr.shift == 4:

                                if w1.main_code == 2043:
                                    w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.belegung)

                        if get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):

                            if temp_rechnr.shift == 1:

                                if w1.main_code == 2040:
                                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.belegung)

                            if temp_rechnr.shift == 2:

                                if w1.main_code == 2041:
                                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.belegung)

                            if temp_rechnr.shift == 3:

                                if w1.main_code == 2042:
                                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.belegung)

                            if temp_rechnr.shift == 4:

                                if w1.main_code == 2043:
                                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.belegung)
                        else:

                            if ytd_flag:

                                if temp_rechnr.shift == 1:

                                    if w1.main_code == 2040:
                                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.belegung)

                                if temp_rechnr.shift == 2:

                                    if w1.main_code == 2041:
                                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.belegung)

                                if temp_rechnr.shift == 3:

                                    if w1.main_code == 2042:
                                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.belegung)

                                if temp_rechnr.shift == 4:

                                    if w1.main_code == 2043:
                                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.belegung)

                    artikel = get_cache (Artikel, {"departement": [(eq, temp_rechnr.dept)],"artnr": [(eq, temp_rechnr.artnrfront)]})

                    if artikel:
                        netto =  to_decimal(temp_rechnr.betrag) / to_decimal((1) + to_decimal(vat) + to_decimal(vat2) + to_decimal(service))

                        if temp_rechnr.datum == to_date:

                            if temp_rechnr.shift == 1:

                                if w1.main_code == 2048:
                                    w1.tday =  to_decimal(w1.tday) + to_decimal(netto)

                            if temp_rechnr.shift == 2:

                                if w1.main_code == 2049:
                                    w1.tday =  to_decimal(w1.tday) + to_decimal(netto)

                            if temp_rechnr.shift == 3:

                                if w1.main_code == 2050:
                                    w1.tday =  to_decimal(w1.tday) + to_decimal(netto)

                            if temp_rechnr.shift == 4:

                                if w1.main_code == 2051:
                                    w1.tday =  to_decimal(w1.tday) + to_decimal(netto)

                        if get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):

                            if temp_rechnr.shift == 1:

                                if w1.main_code == 2048:
                                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(netto)

                            if temp_rechnr.shift == 2:

                                if w1.main_code == 2049:
                                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(netto)

                            if temp_rechnr.shift == 3:

                                if w1.main_code == 2050:
                                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(netto)

                            if temp_rechnr.shift == 4:

                                if w1.main_code == 2051:
                                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(netto)
                        else:

                            if ytd_flag:

                                if temp_rechnr.shift == 1:

                                    if w1.main_code == 2048:
                                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(netto)

                                if temp_rechnr.shift == 2:

                                    if w1.main_code == 2049:
                                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(netto)

                                if temp_rechnr.shift == 3:

                                    if w1.main_code == 2050:
                                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(netto)

                                if temp_rechnr.shift == 4:

                                    if w1.main_code == 2051:
                                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(netto)

            elif (w1.main_code >= 2052 and w1.main_code <= 2055):

                if w1.main_code == 2052 or w1.main_code == 2053:

                    if not temp_rechnr.compli_flag:

                        if w1.main_code == 2052:

                            if temp_rechnr.datum == to_date:
                                w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.f_qty)

                            if get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):
                                w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.f_qty)

                            if ytd_flag:
                                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.f_qty)

                        if w1.main_code == 2053:

                            if temp_rechnr.datum == to_date:
                                w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.b_qty)

                            if get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):
                                w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.b_qty)

                            if ytd_flag:
                                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.b_qty)

                elif w1.main_code == 2054 or w1.main_code == 2055:

                    if w1.main_code == 2054:

                        if temp_rechnr.datum == to_date:
                            w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.f_qty)

                        if get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):
                            w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.f_qty)

                        if ytd_flag:
                            w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.f_qty)

                    if w1.main_code == 2055:

                        if temp_rechnr.datum == to_date:
                            w1.tday =  to_decimal(w1.tday) + to_decimal(temp_rechnr.b_qty)

                        if get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):
                            w1.saldo =  to_decimal(w1.saldo) + to_decimal(temp_rechnr.b_qty)

                        if ytd_flag:
                            w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(temp_rechnr.b_qty)


    def fill_fb_flash(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        d_flag:bool = False
        f_eknr:int = 0
        b_eknr:int = 0
        fl_eknr:int = 0
        bl_eknr:int = 0
        ldry:int = 0
        dstore:int = 0
        main_storage:int = 1
        warenwert:Decimal = to_decimal("0.0")
        stornground:string = ""
        double_currency:bool = False
        foreign_nr:int = 0
        exchg_rate:Decimal = 1
        curr_datum:date = None
        rate:Decimal = 1
        cost:Decimal = to_decimal("0.0")
        h_art = None
        gl_acc1 = None
        H_art =  create_buffer("H_art",H_artikel)
        Gl_acc1 =  create_buffer("Gl_acc1",Gl_acct)

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)
        s_list_list.clear()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1081)]})
        ldry = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1082)]})
        dstore = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})

        if htparam.flogical:
            double_currency = True

            htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

            if waehrung:
                foreign_nr = waehrung.waehrungsnr
                exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
            else:
                exchg_rate =  to_decimal("1")

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
        f_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
        b_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})
        fl_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})
        bl_eknr = htparam.finteger

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date
        warenwert =  to_decimal("0")

        if w1.main_code == 2056:

            l_op_obj_list = {}
            for l_op, l_lager, l_artikel in db_session.query(L_op, L_lager, L_artikel).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == w1.dept)).filter(
                     (L_op.op_art == 1) & (L_op.pos > 0) & (L_op.loeschflag <= 1) & (L_op.lager_nr != main_storage) & (L_op.datum >= datum1) & (L_op.datum <= to_date)).order_by(L_op._recid).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == w1.dept), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.datum = l_op.datum
                    s_list.flag = w1.dept


                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == w1.dept)):

                if s_list.datum == to_date:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(s_list.betrag)

                if get_month(s_list.datum) == get_month(to_date) and get_year(s_list.datum) == get_year(to_date):
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(s_list.betrag)

                if ytd_flag:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(s_list.betrag)
                d_flag = (get_month(s_list.datum) == get_month(to_date)) and (get_year(s_list.datum) == get_year(to_date))

                if d_flag:
                    w1.mon_saldo[get_day(s_list.datum) - 1] = w1.mon_saldo[get_day(s_list.datum) - 1] + s_list.betrag

        if w1.main_code == 2057:

            l_op_obj_list = {}
            for l_op, l_lager, l_artikel in db_session.query(L_op, L_lager, L_artikel).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == w1.dept)).filter(
                     (L_op.op_art == 4) & (L_op.loeschflag <= 1) & (L_op.herkunftflag == 1) & (L_op.datum >= datum1) & (L_op.datum <= to_date)).order_by(L_op._recid).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == w1.dept), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.datum = l_op.datum
                    s_list.flag = w1.dept

                if l_op.lager_nr != main_storage:
                    s_list.betrag =  to_decimal(s_list.betrag) - to_decimal(l_op.warenwert)

                if l_op.pos != main_storage:
                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == w1.dept)):

                if s_list.datum == to_date:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(s_list.betrag)

                if get_month(s_list.datum) == get_month(to_date) and get_year(s_list.datum) == get_year(to_date):
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(s_list.betrag)

                if ytd_flag:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(s_list.betrag)
                d_flag = (get_month(s_list.datum) == get_month(to_date)) and (get_year(s_list.datum) == get_year(to_date))

                if d_flag:
                    w1.mon_saldo[get_day(s_list.datum) - 1] = w1.mon_saldo[get_day(s_list.datum) - 1] + s_list.betrag

        if w1.main_code == 2058:

            if w1.dept == fl_eknr:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 272)]})

                if htparam:
                    stornground = htparam.fchar

            elif w1.dept == bl_eknr:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 275)]})

                if htparam:
                    stornground = htparam.fchar

            l_op_obj_list = {}
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) & ((L_artikel.endkum == fl_eknr) | (L_artikel.endkum == bl_eknr))).filter(
                     (L_op.op_art == 3) & (L_op.loeschflag <= 1) & (L_op.datum >= datum1) & (L_op.datum <= to_date) & (L_op.stornogrund == (stornground).lower())).order_by(L_op._recid).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                if l_op.stornogrund == stornogrund:

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == w1.dept), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.datum = l_op.datum
                        s_list.flag = w1.dept


                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == w1.dept)):

                if s_list.datum == to_date:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(s_list.betrag)

                if get_month(s_list.datum) == get_month(to_date) and get_year(s_list.datum) == get_year(to_date):
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(s_list.betrag)

                if ytd_flag:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(s_list.betrag)
                d_flag = (get_month(s_list.datum) == get_month(to_date)) and (get_year(s_list.datum) == get_year(to_date))

                if d_flag:
                    w1.mon_saldo[get_day(s_list.datum) - 1] = w1.mon_saldo[get_day(s_list.datum) - 1] + s_list.betrag

        if w1.main_code == 2059:

            h_compli_obj_list = {}
            h_compli = H_compli()
            h_art = H_artikel()
            for h_compli.datum, h_compli.artnr, h_compli.departement, h_compli.anzahl, h_compli.epreis, h_compli._recid, h_art.departement, h_art.artnr, h_art.service_code, h_art.mwst_code, h_art.prozent, h_art.artnrfront, h_art.artart, h_art._recid in db_session.query(H_compli.datum, H_compli.artnr, H_compli.departement, H_compli.anzahl, H_compli.epreis, H_compli._recid, H_art.departement, H_art.artnr, H_art.service_code, H_art.mwst_code, H_art.prozent, H_art.artnrfront, H_art.artart, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                     (H_compli.datum >= datum1) & (H_compli.datum <= to_date) & (H_compli.departement != ldry) & (H_compli.departement != dstore) & (H_compli.betriebsnr == 0)).order_by(H_compli.datum, H_compli.rechnr).all():
                if h_compli_obj_list.get(h_compli._recid):
                    continue
                else:
                    h_compli_obj_list[h_compli._recid] = True


                cost =  to_decimal("0")

                if double_currency and curr_datum != h_compli.datum:
                    curr_datum = h_compli.datum

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, curr_datum)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, curr_datum)]})

                    if exrate:
                        rate =  to_decimal(exrate.betrag)
                    else:
                        rate =  to_decimal(exchg_rate)

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)]})

                if w1.dept == fl_eknr:

                    artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_compli.departement)]})

                    if artikel:

                        if artikel.endkum == fl_eknr or artikel.umsatzart == 3 or artikel.umsatzart == 5:

                            h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                            if h_cost and h_cost.betrag != 0:
                                cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)

                            elif not h_cost or (h_cost and h_cost.betrag == 0):
                                cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)

                elif w1.dept == bl_eknr:

                    artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_compli.departement)]})

                    if artikel:

                        if artikel.endkum == bl_eknr or artikel.umsatzart == 6:

                            h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                            if h_cost and h_cost.betrag != 0:
                                cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)

                            elif not h_cost or (h_cost and h_cost.betrag == 0):
                                cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)

                s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == w1.dept), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.datum = h_compli.datum
                    s_list.flag = w1.dept


                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(cost)

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == w1.dept)):

                if s_list.datum == to_date:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(s_list.betrag)

                if get_month(s_list.datum) == get_month(to_date) and get_year(s_list.datum) == get_year(to_date):
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(s_list.betrag)

                if ytd_flag:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(s_list.betrag)
                d_flag = (get_month(s_list.datum) == get_month(to_date)) and (get_year(s_list.datum) == get_year(to_date))

                if d_flag:
                    w1.mon_saldo[get_day(s_list.datum) - 1] = w1.mon_saldo[get_day(s_list.datum) - 1] + s_list.betrag


    def fill_fbstat(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        fbdept:int = 0
        shift:int = 0
        do_it:bool = True
        d_flag:bool = False
        mm:int = 0
        yy:int = 0
        Wf1 = W1
        wf1_list = w1_list
        Wf2 = W1
        wf2_list = w1_list
        Wf3 = W1
        wf3_list = w1_list
        Wf4 = W1
        wf4_list = w1_list
        Wb1 = W1
        wb1_list = w1_list
        Wb2 = W1
        wb2_list = w1_list
        Wb3 = W1
        wb3_list = w1_list
        Wb4 = W1
        wb4_list = w1_list
        Wo1 = W1
        wo1_list = w1_list
        Wo2 = W1
        wo2_list = w1_list
        Wo3 = W1
        wo3_list = w1_list
        Wo4 = W1
        wo4_list = w1_list

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)
        fbdept = to_int(substring(w1.s_artnr, 0, 2))

        fbstat_dept = query(fbstat_dept_list, filters=(lambda fbstat_dept: fbstat_dept.dept == fbdept), first=True)

        if fbstat_dept:
            do_it = False

        if do_it:
            fbstat_dept = Fbstat_dept()
            fbstat_dept_list.append(fbstat_dept)

            fbstat_dept.dept = fbdept

            wf1 = query(wf1_list, filters=(lambda wf1: wf1.main_code == 1997 and to_int(substring(wf1.s_artnr, 0, 2)) == fbdept and to_int(substring(wf1.s_artnr, 2)) == 1), first=True)

            wf2 = query(wf2_list, filters=(lambda wf2: wf2.main_code == 1997 and to_int(substring(wf2.s_artnr, 0, 2)) == fbdept and to_int(substring(wf2.s_artnr, 2)) == 2), first=True)

            wf3 = query(wf3_list, filters=(lambda wf3: wf3.main_code == 1997 and to_int(substring(wf3.s_artnr, 0, 2)) == fbdept and to_int(substring(wf3.s_artnr, 2)) == 3), first=True)

            wf4 = query(wf4_list, filters=(lambda wf4: wf4.main_code == 1997 and to_int(substring(wf4.s_artnr, 0, 2)) == fbdept and to_int(substring(wf4.s_artnr, 2)) == 4), first=True)

            wb1 = query(wb1_list, filters=(lambda wb1: wb1.main_code == 1998 and to_int(substring(wb1.s_artnr, 0, 2)) == fbdept and to_int(substring(wb1.s_artnr, 2)) == 1), first=True)

            wb2 = query(wb2_list, filters=(lambda wb2: wb2.main_code == 1998 and to_int(substring(wb2.s_artnr, 0, 2)) == fbdept and to_int(substring(wb2.s_artnr, 2)) == 2), first=True)

            wb3 = query(wb3_list, filters=(lambda wb3: wb3.main_code == 1998 and to_int(substring(wb3.s_artnr, 0, 2)) == fbdept and to_int(substring(wb3.s_artnr, 2)) == 3), first=True)

            wb4 = query(wb4_list, filters=(lambda wb4: wb4.main_code == 1998 and to_int(substring(wb4.s_artnr, 0, 2)) == fbdept and to_int(substring(wb4.s_artnr, 2)) == 4), first=True)

            wo1 = query(wo1_list, filters=(lambda wo1: wo1.wb1.main_code == 1999 and to_int(substring(wo1.s_artnr, 0, 2)) == fbdept and to_int(substring(wo1.s_artnr, 2)) == 1), first=True)

            wo2 = query(wo2_list, filters=(lambda wo2: wo2.main_code == 1999 and to_int(substring(wo2.s_artnr, 0, 2)) == fbdept and to_int(substring(wo2.s_artnr, 2)) == 2), first=True)

            wo3 = query(wo3_list, filters=(lambda wo3: wo3.main_code == 1999 and to_int(substring(wo3.s_artnr, 0, 2)) == fbdept and to_int(substring(wo3.s_artnr, 2)) == 3), first=True)

            wo4 = query(wo4_list, filters=(lambda wo4: wo4.main_code == 1999 and to_int(substring(wo4.s_artnr, 0, 2)) == fbdept and to_int(substring(wo4.s_artnr, 2)) == 4), first=True)

            if ytd_flag:
                datum1 = jan1
            else:
                datum1 = from_date
            mm = get_month(to_date)
            yy = get_year(to_date)

            for fbstat in db_session.query(Fbstat).filter(
                     (Fbstat.datum >= datum1) & (Fbstat.datum <= to_date) & (Fbstat.departement == fbdept)).order_by(Fbstat._recid).all():
                d_flag = None != zinrstat and (get_month(zinrstat.datum) == get_month(to_date)) and (get_year(zinrstat.datum) == get_year(to_date))

                if fbstat.datum == to_date:

                    if wf1:
                        wf1.tday =  to_decimal(wf1.tday) + to_decimal(fbstat.food_wpax[0] + fbstat.food_gpax[0])

                    if wf2:
                        wf2.tday =  to_decimal(wf2.tday) + to_decimal(fbstat.food_wpax[1] + fbstat.food_gpax[1])

                    if wf3:
                        wf3.tday =  to_decimal(wf3.tday) + to_decimal(fbstat.food_wpax[2] + fbstat.food_gpax[2])

                    if wf4:
                        wf4.tday =  to_decimal(wf4.tday) + to_decimal(fbstat.food_wpax[3] + fbstat.food_gpax[3])

                    if wb1:
                        wb1.tday =  to_decimal(wb1.tday) + to_decimal(fbstat.bev_wpax[0] + fbstat.bev_gpax[0])

                    if wb2:
                        wb2.tday =  to_decimal(wb2.tday) + to_decimal(fbstat.bev_wpax[1] + fbstat.bev_gpax[1])

                    if wb3:
                        wb3.tday =  to_decimal(wb3.tday) + to_decimal(fbstat.bev_wpax[2] + fbstat.bev_gpax[2])

                    if wb4:
                        wb4.tday =  to_decimal(wb4.tday) + to_decimal(fbstat.bev_wpax[3] + fbstat.bev_gpax[3])

                    if wo1:
                        wo1.tday =  to_decimal(wo1.tday) + to_decimal(fbstat.other_wpax[0] + fbstat.other_gpax[0])

                    if wo2:
                        wo2.tday =  to_decimal(wo2.tday) + to_decimal(fbstat.other_wpax[1] + fbstat.other_gpax[1])

                    if wo3:
                        wo3.tday =  to_decimal(wo3.tday) + to_decimal(fbstat.other_wpax[2] + fbstat.other_gpax[2])

                    if wo4:
                        wo4.tday =  to_decimal(wo4.tday) + to_decimal(fbstat.other_wpax[3] + fbstat.other_gpax[3])

                if get_month(fbstat.datum) == mm:

                    if wf1:
                        wf1.saldo =  to_decimal(wf1.saldo) + to_decimal(fbstat.food_wpax[0] + fbstat.food_gpax[0])

                    if wf2:
                        wf2.saldo =  to_decimal(wf2.saldo) + to_decimal(fbstat.food_wpax[1] + fbstat.food_gpax[1])

                    if wf3:
                        wf3.saldo =  to_decimal(wf3.saldo) + to_decimal(fbstat.food_wpax[2] + fbstat.food_gpax[2])

                    if wf4:
                        wf4.saldo =  to_decimal(wf4.saldo) + to_decimal(fbstat.food_wpax[3] + fbstat.food_gpax[3])

                    if wb1:
                        wb1.saldo =  to_decimal(wb1.saldo) + to_decimal(fbstat.bev_wpax[0] + fbstat.bev_gpax[0])

                    if wb2:
                        wb2.saldo =  to_decimal(wb2.saldo) + to_decimal(fbstat.bev_wpax[1] + fbstat.bev_gpax[1])

                    if wb3:
                        wb3.saldo =  to_decimal(wb3.saldo) + to_decimal(fbstat.bev_wpax[2] + fbstat.bev_gpax[2])

                    if wb4:
                        wb4.saldo =  to_decimal(wb4.saldo) + to_decimal(fbstat.bev_wpax[3] + fbstat.bev_gpax[3])

                    if wo1:
                        wo1.saldo =  to_decimal(wo1.saldo) + to_decimal(fbstat.other_wpax[0] + fbstat.other_gpax[0])

                    if wo2:
                        wo2.saldo =  to_decimal(wo2.saldo) + to_decimal(fbstat.other_wpax[1] + fbstat.other_gpax[1])

                    if wo3:
                        wo3.saldo =  to_decimal(wo3.saldo) + to_decimal(fbstat.other_wpax[2] + fbstat.other_gpax[2])

                    if wo4:
                        wo4.saldo =  to_decimal(wo4.saldo) + to_decimal(fbstat.other_wpax[3] + fbstat.other_gpax[3])

                if get_month(fbstat.datum) == mm and get_year(fbstat.datum) == yy:

                    if wf1:
                        wf1.mon_saldo[get_day(fbstat.datum) - 1] = wf1.mon_saldo[get_day(fbstat.datum) - 1] + fbstat.food_wpax[0] + fbstat.food_gpax[0]

                    if wf2:
                        wf2.mon_saldo[get_day(fbstat.datum) - 1] = wf2.mon_saldo[get_day(fbstat.datum) - 1] + fbstat.food_wpax[1] + fbstat.food_gpax[1]

                    if wf3:
                        wf3.mon_saldo[get_day(fbstat.datum) - 1] = wf3.mon_saldo[get_day(fbstat.datum) - 1] + fbstat.food_wpax[2] + fbstat.food_gpax[2]

                    if wf4:
                        wf4.mon_saldo[get_day(fbstat.datum) - 1] = wf4.mon_saldo[get_day(fbstat.datum) - 1] + fbstat.food_wpax[3] + fbstat.food_gpax[3]

                    if wb1:
                        wb1.mon_saldo[get_day(fbstat.datum) - 1] = wb1.mon_saldo[get_day(fbstat.datum) - 1] + fbstat.bev_wpax[0] + fbstat.bev_gpax[0]

                    if wb2:
                        wb2.mon_saldo[get_day(fbstat.datum) - 1] = wb2.mon_saldo[get_day(fbstat.datum) - 1] + fbstat.bev_wpax[1] + fbstat.bev_gpax[1]

                    if wb3:
                        wb3.mon_saldo[get_day(fbstat.datum) - 1] = wb3.mon_saldo[get_day(fbstat.datum) - 1] + fbstat.bev_wpax[2] + fbstat.bev_gpax[2]

                    if wb4:
                        wb4.mon_saldo[get_day(fbstat.datum) - 1] = wb4.mon_saldo[get_day(fbstat.datum) - 1] + fbstat.bev_wpax[3] + fbstat.bev_gpax[3]

                    if wo1:
                        wo1.mon_saldo[get_day(fbstat.datum) - 1] = wo1.mon_saldo[get_day(fbstat.datum) - 1] + fbstat.other_wpax[0] + fbstat.other_gpax[0]

                    if wo2:
                        wo2.mon_saldo[get_day(fbstat.datum) - 1] = wo2.mon_saldo[get_day(fbstat.datum) - 1] + fbstat.other_wpax[1] + fbstat.other_gpax[1]

                    if wo3:
                        wo3.mon_saldo[get_day(fbstat.datum) - 1] = wo3.mon_saldo[get_day(fbstat.datum) - 1] + fbstat.other_wpax[2] + fbstat.other_gpax[2]

                    if wo4:
                        wo4.mon_saldo[get_day(fbstat.datum) - 1] = wo4.mon_saldo[get_day(fbstat.datum) - 1] + fbstat.other_wpax[3] + fbstat.other_gpax[3]

                if wf1:
                    wf1.ytd_saldo =  to_decimal(wf1.ytd_saldo) + to_decimal(fbstat.food_wpax[0] + fbstat.food_gpax[0])

                if wf2:
                    wf2.ytd_saldo =  to_decimal(wf2.ytd_saldo) + to_decimal(fbstat.food_wpax[1] + fbstat.food_gpax[1])

                if wf3:
                    wf3.ytd_saldo =  to_decimal(wf3.ytd_saldo) + to_decimal(fbstat.food_wpax[2] + fbstat.food_gpax[2])

                if wf4:
                    wf4.ytd_saldo =  to_decimal(wf4.ytd_saldo) + to_decimal(fbstat.food_wpax[3] + fbstat.food_gpax[3])

                if wb1:
                    wb1.ytd_saldo =  to_decimal(wb1.ytd_saldo) + to_decimal(fbstat.bev_wpax[0] + fbstat.bev_gpax[0])

                if wb2:
                    wb2.ytd_saldo =  to_decimal(wb2.ytd_saldo) + to_decimal(fbstat.bev_wpax[1] + fbstat.bev_gpax[1])

                if wb3:
                    wb3.ytd_saldo =  to_decimal(wb3.ytd_saldo) + to_decimal(fbstat.bev_wpax[2] + fbstat.bev_gpax[2])

                if wb4:
                    wb4.ytd_saldo =  to_decimal(wb4.ytd_saldo) + to_decimal(fbstat.bev_wpax[3] + fbstat.bev_gpax[3])

                if wo1:
                    wo1.ytd_saldo =  to_decimal(wo1.ytd_saldo) + to_decimal(fbstat.other_wpax[0] + fbstat.other_gpax[0])

                if wo2:
                    wo2.ytd_saldo =  to_decimal(wo2.ytd_saldo) + to_decimal(fbstat.other_wpax[1] + fbstat.other_gpax[1])

                if wo3:
                    wo3.ytd_saldo =  to_decimal(wo3.ytd_saldo) + to_decimal(fbstat.other_wpax[2] + fbstat.other_gpax[2])

                if wo4:
                    wo4.ytd_saldo =  to_decimal(wo4.ytd_saldo) + to_decimal(fbstat.other_wpax[3] + fbstat.other_gpax[3])


    def fill_rmstat(rec_w1:int, key_word:string):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        curr_date:date = None
        d_flag:bool = False
        dlmtd_flag:bool = False

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        if (get_day(to_date) == 31 and get_month(to_date) != 8 and get_month(to_date) != 1) or (get_day(to_date) == 30 and get_month(to_date) == 3) or (get_day(date_mdy(3, 1, get_year(to_date)) - 1) == 28 and get_month(to_date) == 3 and get_day(to_date) == 29):
            w1.lm_today =  to_decimal("0")
        else:

            if get_month(to_date) == 1:
                curr_date = date_mdy(12, get_day(to_date) , get_year(to_date) - timedelta(days=1))
            else:
                curr_date = date_mdy(get_month(to_date) - timedelta(days=1, get_day(to_date) , get_year(to_date)))

            zinrstat = get_cache (Zinrstat, {"datum": [(eq, curr_date)],"zinr": [(eq, key_word)]})

            if zinrstat:
                w1.lm_today =  to_decimal(zinrstat.zimmeranz)

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.datum >= datum1) & (Zinrstat.datum <= to_date) & (Zinrstat.zinr == (key_word).lower())).order_by(Zinrstat._recid).all():
            d_flag = (get_month(zinrstat.datum) == get_month(to_date)) and (get_year(zinrstat.datum) == get_year(to_date))

            if d_flag:
                w1.mon_saldo[get_day(zinrstat.datum) - 1] = w1.mon_saldo[get_day(zinrstat.datum) - 1] + zinrstat.zimmeranz

            if zinrstat.datum == to_date - timedelta(days=1):
                w1.yesterday =  to_decimal(w1.yesterday) + to_decimal(zinrstat.zimmeranz)

            if zinrstat.datum == to_date:
                w1.tday =  to_decimal(w1.tday) + to_decimal(zinrstat.zimmeranz)

            if zinrstat.datum < from_date:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.zimmeranz)
            else:
                w1.saldo =  to_decimal(w1.saldo) + to_decimal(zinrstat.zimmeranz)

                if ytd_flag:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.zimmeranz)

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= datum1) & (Zinrstat.datum <= lto_date) & (Zinrstat.zinr == (key_word).lower())).order_by(Zinrstat._recid).all():

                if zinrstat.datum < lfrom_date:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.zimmeranz)
                else:
                    dlmtd_flag = (get_month(zinrstat.datum) == get_month(to_date)) and (get_year(zinrstat.datum) == get_year(to_date) - 1)

                    if dlmtd_flag:
                        w1.mon_lmtd[get_day(zinrstat.datum) - 1] = w1.mon_lmtd[get_day(zinrstat.datum) - 1] + zinrstat.zimmeranz
                    w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(zinrstat.zimmeranz)

                    if lytd_flag:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.zimmeranz)

        if pmtd_flag:

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= pfrom_date) & (Zinrstat.datum <= pto_date) & (Zinrstat.zinr == (key_word).lower())).order_by(Zinrstat._recid).all():
                w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(zinrstat.zimmeranz)


        if lytoday_flag:

            zinrstat = get_cache (Zinrstat, {"datum": [(eq, lytoday)],"zinr": [(eq, key_word)]})

            if zinrstat:
                w1.lytoday =  to_decimal(zinrstat.zimmeranz)
        w1.done = True


    def fill_avrgllodge(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        W11 = W1
        w11_list = w1_list

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        w11 = query(w11_list, filters=(lambda w11: w11.main_code == 812), first=True)

        if w11 and w11.done:
            pass

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.datum >= datum1) & (Zinrstat.datum <= to_date) & (Zinrstat.zinr == ("avrgLrate").lower())).order_by(Zinrstat._recid).all():

            if zinrstat.datum == to_date:
                w1.tday =  to_decimal(w1.tday) + to_decimal(zinrstat.logisumsatz)

                if w11:
                    w11.tday =  to_decimal(w11.tday) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

            if zinrstat.datum < from_date:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

                if w11:
                    w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)
            else:
                w1.saldo =  to_decimal(w1.saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

                if ytd_flag:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

                if w11:
                    w11.saldo =  to_decimal(w11.saldo) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

                    if ytd_flag:
                        w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= datum1) & (Zinrstat.datum <= lto_date) & (Zinrstat.zinr == ("avrgLrate").lower())).order_by(Zinrstat._recid).all():

                if zinrstat.datum < lfrom_date:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

                    if w11:
                        w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)
                else:
                    w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

                    if lytd_flag:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

                    if w11:
                        w11.lastyr =  to_decimal(w11.lastyr) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

                        if lytd_flag:
                            w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)

        if pmtd_flag:

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= pfrom_date) & (Zinrstat.datum <= pto_date) & (Zinrstat.zinr == ("avrgLrate").lower())).order_by(Zinrstat._recid).all():
                w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

                if w11:
                    w11.lastmon =  to_decimal(w11.lastmon) + to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)


        if lytoday_flag:

            zinrstat = get_cache (Zinrstat, {"datum": [(eq, lytoday)],"zinr": [(eq, "avrglrate")]})

            if zinrstat:
                w1.lytoday =  to_decimal(zinrstat.logisumsatz) / to_decimal(zinrstat.zimmeranz)

                if w11:
                    w11.lytoday =  to_decimal(zinrstat.argtumsatz) / to_decimal(zinrstat.zimmeranz)
        w1.done = True

        if w11:
            w11.done = True


    def fill_source(rec_w1:int, main_nr:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        source_nr:int = 0
        mm:int = 0
        datum1:date = None
        curr_date:date = None
        ly_currdate:date = None
        ny_currdate:date = None
        njan1:date = None
        nmth1:date = None
        d_flag:bool = False
        dlmtd_flag:bool = False
        frate1:Decimal = to_decimal("0.0")
        sourcebuff = None
        sourcebuffny = None
        genstatbuff = None
        Sourcebuff =  create_buffer("Sourcebuff",Sources)
        Sourcebuffny =  create_buffer("Sourcebuffny",Sources)
        Genstatbuff =  create_buffer("Genstatbuff",Genstat)
        W11 = W1
        w11_list = w1_list
        W12 = W1
        w12_list = w1_list
        W13 = W1
        w13_list = w1_list
        tmp_room_list.clear()

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)
        source_nr = w1.artnr
        njan1 = date_mdy(1, 1, get_year(to_date) + timedelta(days=1))
        nmth1 = date_mdy(get_month(to_date) , 1, get_year(to_date) + timedelta(days=1))
        mm = get_month(to_date)

        if get_month(to_date) == 2 and get_day(to_date) == 29:
            ny_currdate = date_mdy(get_month(to_date) , 28, get_year(to_date) + timedelta(days=1))
        else:
            ny_currdate = date_mdy(get_month(to_date) , get_day(to_date) , get_year(to_date) + timedelta(days=1))

        sourcebuffny = get_cache (Sources, {"datum": [(eq, ny_currdate)],"source_code": [(eq, source_nr)]})

        if sourcebuffny:

            if main_nr == 9092:
                w1.ny_budget =  to_decimal(sourcebuffny.budlogis)

            if main_nr == 9813:
                w1.ny_budget =  to_decimal(sourcebuffny.budzimmeranz)

            if main_nr == 9814:
                w1.ny_budget =  to_decimal(sourcebuffny.persanz)

        for sourcebuffny in db_session.query(Sourcebuffny).filter(
                 (Sourcebuffny.datum >= njan1) & (Sourcebuffny.datum <= ny_currdate) & (Sourcebuffny.source_code == source_nr)).order_by(Sourcebuffny._recid).all():

            if main_nr == 9092:
                w1.nytd_budget =  to_decimal(w1.nytd_budget) + to_decimal(sourcebuffny.budlogis)

            if main_nr == 9813:
                w1.nytd_budget =  to_decimal(w1.nytd_budget) + to_decimal(sourcebuffny.budzimmeranz)

            if main_nr == 9814:
                w1.nytd_budget =  to_decimal(w1.nytd_budget) + to_decimal(sourcebuffny.budpersanz)

        for sourcebuffny in db_session.query(Sourcebuffny).filter(
                 (Sourcebuffny.datum >= nmth1) & (Sourcebuffny.datum <= ny_currdate) & (Sourcebuffny.source_code == source_nr)).order_by(Sourcebuffny._recid).all():

            if main_nr == 9092:
                w1.nmtd_budget =  to_decimal(w1.nmtd_budget) + to_decimal(sourcebuffny.budlogis)

            if main_nr == 9813:
                w1.nmtd_budget =  to_decimal(w1.nmtd_budget) + to_decimal(sourcebuffny.budzimmeranz)

            if main_nr == 9814:
                w1.nmtd_budget =  to_decimal(w1.nmtd_budget) + to_decimal(sourcebuffny.budpersanz)

        sources = get_cache (Sources, {"datum": [(eq, to_date - timedelta(days=1))],"source_code": [(eq, source_nr)]})

        if sources:

            if main_nr == 9092:
                w1.yesterday =  to_decimal(sources.logis) / to_decimal(frate)

            elif main_nr == 9813:
                w1.yesterday =  to_decimal(sources.zimmeranz)

            elif main_nr == 9814:
                w1.yesterday =  to_decimal(sources.persanz)

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum >= datum1) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.source == source_nr) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
            frate =  to_decimal("1")
            d_flag = (get_month(genstat.datum) == get_month(to_date))
            and (get_year(genstat.datum) = get_year(to_date))

            if foreign_flag:
                find_exrate(genstat.datum)

                if exrate:
                    frate =  to_decimal(exrate.betrag)

            if genstat.datum == to_date:

                tmp_room = query(tmp_room_list, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                if not tmp_room:

                    if main_nr == 9813:
                        w1.tday =  to_decimal(w1.tday) + to_decimal("1")
                    tmp_room = Tmp_room()
                    tmp_room_list.append(tmp_room)

                    tmp_room.gastnr = genstat.gastnr
                    tmp_room.zinr = genstat.zinr
                    tmp_room.flag = 1

                if main_nr == 9814:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                if main_nr == 9092:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(genstat.logis) / to_decimal(frate)

            if get_month(genstat.datum) == mm:

                if main_nr == 9092:

                    if d_flag:
                        w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + genstat.logis / frate
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(genstat.logis) / to_decimal(frate)

                if main_nr == 9814:

                    if d_flag:
                        w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                if main_nr == 9813:

                    if d_flag:
                        w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + 1
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal("1")

            if main_nr == 9092:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(genstat.logis) / to_decimal(frate)

            if main_nr == 9814:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

            if main_nr == 9813:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal("1")
        tmp_room_list.clear()

        if lytd_flag or lmtd_flag:
            mm = get_month(lto_date)

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            for genstat in db_session.query(Genstat).filter(
                         (Genstat.datum >= datum1) & (Genstat.datum <= lto_date) & (Genstat.resstatus != 13) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.source == source_nr) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
                dlmtd_flag = (get_month(genstat.datum) == get_month(lto_date)) and (get_year(genstat.datum) == get_year(lto_date))

                if foreign_flag:
                    find_exrate(genstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)

                if genstat.datum == lto_date:

                    tmp_room = query(tmp_room_list, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                    if not tmp_room:

                        if main_nr == 9813:
                            w1.lytoday =  to_decimal(w1.lytoday) + to_decimal("1")
                        tmp_room = Tmp_room()
                        tmp_room_list.append(tmp_room)

                        tmp_room.gastnr = genstat.gastnr
                        tmp_room.zinr = genstat.zinr
                        tmp_room.flag = 1

                    if main_nr == 9814:
                        w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                    if main_nr == 9092:
                        w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(genstat.logis) / to_decimal(frate)

                if get_month(genstat.datum) == mm:

                    if main_nr == 9092:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(genstat.logis) / to_decimal(frate)

                    if main_nr == 9814:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                    if main_nr == 9813:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal("1")

                if main_nr == 9092:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(genstat.logis) / to_decimal(frate)

                if main_nr == 9814:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                if main_nr == 9813:
                    w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal("1")

        if pmtd_flag:

            for genstat in db_session.query(Genstat).filter(
                         (Genstat.datum >= pfrom_date) & (Genstat.datum <= pto_date) & (Genstat.resstatus != 13) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.source == source_nr) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():

                if foreign_flag:
                    find_exrate(genstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)

                if main_nr == 9092:
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(genstat.logis) / to_decimal(frate)

                if main_nr == 9814:
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                if main_nr == 9813:
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal("1")

    def fill_value1(recid1_w1:int, recid2_w1:int, val_sign:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        sign1:int = 0
        texte:string = ""
        n:int = 0
        Parent = W1
        parent_list = w1_list
        Child = W1
        child_list = w1_list
        Curr_child = W1
        curr_child_list = w1_list
        Curr_w2 = W2
        curr_w2_list = w2_list

        parent = query(parent_list, filters=(lambda parent: parent._recid == recid1_w1), first=True)

        child = query(child_list, filters=(lambda child: child._recid == recid2_w1), first=True)
        parent.tday =  to_decimal(parent.tday) + to_decimal(val_sign) * to_decimal(child.tday)
        parent.tbudget =  to_decimal(parent.tbudget) + to_decimal(val_sign) * to_decimal(child.tbudget)
        parent.saldo =  to_decimal(parent.saldo) + to_decimal(val_sign) * to_decimal(child.saldo)
        parent.budget =  to_decimal(parent.budget) + to_decimal(val_sign) * to_decimal(child.budget)
        parent.lytoday =  to_decimal(parent.lytoday) + to_decimal(val_sign) * to_decimal(child.lytoday)
        parent.lastmon =  to_decimal(parent.lastmon) + to_decimal(val_sign) * to_decimal(child.lastmon)
        parent.lm_budget =  to_decimal(parent.lm_budget) + to_decimal(val_sign) * to_decimal(child.lm_budget)
        parent.lastyr =  to_decimal(parent.lastyr) + to_decimal(val_sign) * to_decimal(child.lastyr)
        parent.ly_budget =  to_decimal(parent.ly_budget) + to_decimal(val_sign) * to_decimal(child.ly_budget)
        parent.ytd_saldo =  to_decimal(parent.ytd_saldo) + to_decimal(val_sign) * to_decimal(child.ytd_saldo)
        parent.ytd_budget =  to_decimal(parent.ytd_budget) + to_decimal(val_sign) * to_decimal(child.ytd_budget)
        parent.lytd_saldo =  to_decimal(parent.lytd_saldo) + to_decimal(val_sign) * to_decimal(child.lytd_saldo)
        parent.lytd_budget =  to_decimal(parent.lytd_budget) + to_decimal(val_sign) * to_decimal(child.lytd_budget)


    def convert_varname(str:string):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        crow = 0
        ccol = 0
        loop_str:int = 0
        loop_col:int = 0
        found:bool = False
        str_col:string = ""
        str_row:string = ""

        def generate_inner_output():
            return (crow, ccol)

            for loop_str in range(1,length(str)  + 1) :
                found = False
                for loop_col in range(1,26 + 1) :

                    if substring(str, loop_str - 1, 1) == chcol[loop_col - 1]:
                        found = True
                        break

                if found:
                    str_col = str_col + substring(str, loop_str - 1, 1)
                else:
                    str_row = str_row + substring(str, loop_str - 1, 1)
            ccol = get_columnno(str_col)
            crow = to_int(str_row)

        return generate_inner_output()


    def get_columnno(last_column:string):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        ind = 1
        i:int = 0
        ind1:int = 0
        ind2:int = 0

        def generate_inner_output():
            return (ind)


            if length(last_column) == 2:
                for i in range(1,26 + 1) :

                    if chcol[i - 1] == substring(last_column, 0, 1):
                        ind1 = i * 26
                        break
                for i in range(1,26 + 1) :

                    if chcol[i - 1] == substring(last_column, 1, 1):
                        ind2 = i
                        break
                ind = ind1 + ind2
            else:
                for i in range(1,26 + 1) :

                    if chcol[i - 1] == (last_column).lower() :
                        ind = i
                        break

        return generate_inner_output()


    def convert_diff(v1:Decimal, v2:Decimal):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, j, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        s = ""
        balance:Decimal = to_decimal("0.0")
        b:Decimal = to_decimal("0.0")
        rs:string = ""

        def generate_inner_output():
            return (s)


            if v2 == 0:
                rs = "0.00"
            else:
                balance = ( to_decimal(v1) - to_decimal(v2)) / to_decimal(v2) * to_decimal("100")

                if balance >= 0:
                    b =  to_decimal(balance)
                else:
                    b =  - to_decimal(balance)

                if b <= 999:
                    rs = to_string(balance, "->>9.99")

                elif b <= 9999:
                    rs = to_string(balance, "->>>9.9")
                else:
                    rs = to_string(balance, "->>>>>>>>>9")
            s = rs

        return generate_inner_output()


    def decode_string(in_str:string):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, prev_param, k, curr_row, curr_col, htl_no, cell_value, chcol, dayname, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, genstat, uebertrag, artikel, h_artikel, wgrpdep, umsatz, budget, htparam, exrate, h_cost, h_journal, reservation, h_bill_line, h_bill, bill, queasy, gl_acct, waehrung, l_lager, l_artikel, l_op, h_compli, fbstat, sources, paramtext, parameters
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, s_list, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, w11, w12, w13, w11, w12, w13, w11, tbuff, w1a, w11, w12, w11, w12, w11, w12, w11, w753, w754, w755, w11, w11, w11, w11, w12, w13, wlos, wspc, btemp_rechnr, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, w11, w11, w12, w13, parent, child, curr_child, curr_w2
        nonlocal shift_list_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, s_list_list, fbstat_dept_list, stream_list_list

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

            s = in_str
            j = asc(substring(s, 0, 1)) - 70
            len_ = length(in_str) - 1
            s = substring(in_str, 1, len_)
            for len_ in range(1,length(s)  + 1) :
                out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    fill_value()
    find_exrate(to_date)
    exrate_betrag =  to_decimal("0")

    if exrate:
        exrate_betrag =  to_decimal(exrate.betrag)
    ch = trim(to_string(exrate_betrag, ">>>,>>9.99"))
    lfr_date = from_date - timedelta(days=1)

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        htl_no = decode_string(paramtext.ptexte)
    OS_DELETE VALUE ("/usr1/vhp/tmp/outputFO_" + htl_no + ".txt")
    OUTPUT STREAM s1 TO VALUE ("/usr1/vhp/tmp/outputFO_" + htl_no + ".txt") APPEND UNBUFFERED

    for parameters in db_session.query(Parameters).filter(
             (Parameters.progname == ("FO-macro").lower()) & (Parameters.section == to_string(briefnr))).order_by(Parameters.varname).all():

        if prev_param != parameters.varname:
            curr_row, curr_col = convert_varname(parameters.varname)
            prev_param = parameters.varname

            if parameters.vtype != 0:

                w1 = query(w1_list, filters=(lambda w1: w1.varname == parameters.vstring), first=True)

                if parameters.vtype >= 9150 and parameters.vtype <= 9180:
                    k = 0
                    for j in range(9150,9180 + 1) :
                        k = k + 1

                        if parameters.vtype == j:
                            cell_value = trim(to_string(w1.mon_saldo[k - 1], "->>>>>>>>>>>9.99"))
                            break

                elif parameters.vtype >= 8120 and parameters.vtype <= 8150:
                    k = 0
                    for j in range(8120,8150 + 1) :
                        k = k + 1

                        if parameters.vtype == j:
                            cell_value = trim(to_string(w1.mon_lmtd[k - 1], "->>>>>>>>>>>9.99"))
                            break

                elif parameters.vtype >= 9119 and parameters.vtype <= 9149:
                    k = 0
                    for j in range(9119,9149 + 1) :
                        k = k + 1

                        if parameters.vtype == j:
                            cell_value = trim(to_string(w1.mon_budget[k - 1], "->>>>>>>>>>>9.99"))
                            break

                elif parameters.vtype >= 9231 and parameters.vtype <= 9261:
                    k = 0
                    for j in range(9231,9261 + 1) :
                        k = k + 1

                        if parameters.vtype == j:
                            cell_value = trim(to_string(w1.mon_serv[k - 1], "->>>>>>>>>>>9.99"))
                            break

                elif parameters.vtype >= 9262 and parameters.vtype <= 9292:
                    k = 0
                    for j in range(9262,9292 + 1) :
                        k = k + 1

                        if parameters.vtype == j:
                            cell_value = trim(to_string(w1.mon_tax[k - 1], "->>>>>>>>>>>9.99"))
                            break

                elif parameters.vtype == 9197:
                    cell_value = trim(to_string(w1.ny_budget, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 9196:
                    cell_value = trim(to_string(w1.nmtd_budget, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 9195:
                    cell_value = trim(to_string(w1.nytd_budget, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 9199:
                    cell_value = trim(to_string(w1.yesterday, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 9198:
                    cell_value = trim(to_string(w1.lm_today, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 9194:
                    cell_value = trim(to_string(w1.tday_serv, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 9193:
                    cell_value = trim(to_string(w1.tday_tax, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 9192:
                    cell_value = trim(to_string(w1.mtd_serv, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 9191:
                    cell_value = trim(to_string(w1.mtd_tax, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 9190:
                    cell_value = trim(to_string(w1.ytd_serv, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 9189:
                    cell_value = trim(to_string(w1.ytd_tax, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 9188:
                    cell_value = trim(to_string(w1.lm_today_serv, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 9187:
                    cell_value = trim(to_string(w1.lm_today_tax, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 9186:
                    cell_value = trim(to_string(w1.pmtd_serv, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 9185:
                    cell_value = trim(to_string(w1.pmtd_serv, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 9184:
                    cell_value = trim(to_string(w1.lmtd_serv, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 9183:
                    cell_value = trim(to_string(w1.lmtd_tax, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 9182:
                    cell_value = trim(to_string(w1.lm_mtd, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 9181:
                    cell_value = trim(to_string(w1.lm_ytd, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 93:
                    cell_value = trim(to_string(w1.tday, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 94:
                    cell_value = trim(to_string(w1.saldo, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 96:
                    cell_value = trim(to_string(w1.lastmon, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 95:
                    cell_value = trim(to_string(w1.ytd_saldo, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 185:
                    cell_value = trim(to_string(w1.lytoday, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 196:
                    cell_value = trim(to_string(w1.lastyr, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 815:
                    cell_value = trim(to_string(w1.lytd_saldo, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 816:
                    cell_value = trim(to_string(w1.tbudget, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 817:
                    cell_value = trim(to_string(w1.budget, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 819:
                    cell_value = trim(to_string(w1.lm_budget, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 679:
                    cell_value = trim(to_string(w1.ly_budget, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 827:
                    cell_value = trim(to_string(w1.ly_budget, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 843:
                    cell_value = trim(to_string(w1.lytd_budget, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 828:
                    cell_value = trim(to_string(w1.lytd_budget, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 818:
                    cell_value = trim(to_string(w1.ytd_budget, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 820:
                    cell_value = trim(to_string(w1.tday - w1.tbudget, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 821:
                    cell_value = trim(to_string(w1.saldo - w1.budget, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 822:
                    cell_value = trim(to_string(w1.lastmon - w1.lm_budget, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 2065:
                    cell_value = trim(to_string(w1.lastyr - w1.ly_budget, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 2066:
                    cell_value = trim(to_string(w1.ytd_saldo - w1.ytd_budget, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 2067:
                    cell_value = convert_diff(w1.saldo, w1.budget)

                elif parameters.vtype == 2068:
                    cell_value = convert_diff(w1.lastmon, w1.lm_budget)

                elif parameters.vtype == 2069:
                    cell_value = trim(to_string(w1.lastyr - w1.ly_budget, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 2043:
                    cell_value = convert_diff(w1.ytd_saldo, w1.ytd_budget)

                elif parameters.vtype == 2044:
                    cell_value = trim(to_string(w1.lytd_saldo, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 2045:
                    cell_value = trim(to_string(w1.lytd_budget, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 2046:
                    cell_value = trim(to_string(w1.lytd_saldo - w1.lytd_budget, "->>>>>>>>>>>9.99"))

                elif parameters.vtype == 2047:
                    cell_value = convert_diff(w1.lytd_saldo, w1.lytd_budget)
            else:

                if parameters.vstring.lower()  == ("$exrate").lower() :
                    cell_value = ch

                elif parameters.vstring.lower()  == ("$weekday").lower() :
                    cell_value = dayname[get_weekday(to_date) - 1]

                elif parameters.vstring.lower()  == ("$today").lower() :
                    cell_value = to_string(get_day(get_current_date()) , "99") + "/" + to_string(get_month(get_current_date()) , "99") + "/" + to_string(get_year(get_current_date()) , "9999")

                elif parameters.vstring.lower()  == ("$to-date").lower() :
                    cell_value = to_string(get_day(to_date) , "99") + "/" + to_string(get_month(to_date) , "99") + "/" + to_string(get_year(to_date) , "9999")

                elif parameters.vstring.lower()  == ("$month-str").lower() :
                    cell_value = month_str[get_month(to_date) - 1]

                elif parameters.vstring.lower()  == ("$to-date1").lower() :
                    cell_value = to_string(get_day(to_date) , "99") + "-" + month_str[get_month(to_date) - 1] + "-" + to_string(get_year(to_date) , "9999")
            stream_list = Stream_list()
            stream_list_list.append(stream_list)

            stream_list.crow = curr_row
            stream_list.ccol = curr_col
            stream_list.cval = cell_value

    for stream_list in query(stream_list_list, sort_by=[("ccol",False),("crow",False)]):

        if stream_list.cval != "":
            else:
            OUTPUT STREAM s1 CLOSE
        OS_COMMAND SILENT VALUE ("php /usr1/vhp/php-script/write-sheet.php /usr1/vhp/tmp/outputFO_" + htl_no + ".txt " + link)

    return generate_output()