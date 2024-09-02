from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.calc_servvat import calc_servvat
from functions.htpint import htpint
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Segmentstat, Arrangement, Res_line, Bill_line, Zimmer, Zinrstat, Zkstat, H_umsatz, Segment, Uebertrag, Genstat, Artikel, H_artikel, Wgrpdep, Umsatz, Budget, Exrate, H_cost, H_journal, Htparam, H_bill_line, H_bill, Bill, Queasy, Fbstat, Sources, Paramtext, Parameters

def fo_parxls_gsbl(pvilanguage:int, ytd_flag:bool, jan1:date, ljan1:date, lfrom_date:date, lto_date:date, pfrom_date:date, pto_date:date, from_date:date, to_date:date, start_date:date, lytd_flag:bool, lmtd_flag:bool, pmtd_flag:bool, lytoday_flag:bool, lytoday:date, foreign_flag:bool, budget_flag:bool, foreign_nr:int, price_decimal:int, briefnr:int, link:str, w1:[W1], w2:[W2]):
    msg_str = ""
    error_nr = 0
    lfr_date:date = None
    exrate_betrag:decimal = 0
    frate:decimal = 1
    prog_error:bool = False
    ch:str = ""
    month_str:[str] = ["", "", "", "", "", "", "", "", "", "", "", "", ""]
    lvcarea:str = "fo_parxls"
    segmentstat = arrangement = res_line = bill_line = zimmer = zinrstat = zkstat = h_umsatz = segment = uebertrag = genstat = artikel = h_artikel = wgrpdep = umsatz = budget = exrate = h_cost = h_journal = htparam = h_bill_line = h_bill = bill = queasy = fbstat = sources = paramtext = parameters = None

    w1 = shift_list = w2 = tmp_room = t_list = t_rechnr = temp_rechnr = fbstat_dept = stream_list = segmbuff = curr_child = ww1 = ww2 = wdu = hbuff = w11 = w12 = w13 = resbuff = tbuff = w1a = ubuff = buff_umsatz = w753 = w754 = w755 = segmbuffny = wlos = buff = art_buff = wspc = btemp_rechnr = bh_artikel = bh_bill_line = wf1 = wf2 = wf3 = wf4 = wb1 = wb2 = wb3 = wb4 = wo1 = wo2 = wo3 = wo4 = sourcebuff = sourcebuffny = genstatbuff = parent = child = curr_w2 = None

    w1_list, W1 = create_model("W1", {"nr":int, "varname":str, "main_code":int, "s_artnr":str, "artnr":int, "dept":int, "grpflag":int, "done":bool, "bezeich":str, "int_flag":bool, "tday":decimal, "tday_serv":decimal, "tday_tax":decimal, "mtd_serv":decimal, "mtd_tax":decimal, "ytd_serv":decimal, "ytd_tax":decimal, "yesterday":decimal, "saldo":decimal, "lastmon":decimal, "pmtd_serv":decimal, "pmtd_tax":decimal, "lmtd_serv":decimal, "lmtd_tax":decimal, "lastyr":decimal, "lytoday":decimal, "ytd_saldo":decimal, "lytd_saldo":decimal, "year_saldo":[decimal, 12], "mon_saldo":[decimal, 31], "mon_budget":[decimal, 31], "mon_lmtd":[decimal, 31], "tbudget":decimal, "budget":decimal, "lm_budget":decimal, "lm_today":decimal, "lm_today_serv":decimal, "lm_today_tax":decimal, "lm_mtd":decimal, "lm_ytd":decimal, "ly_budget":decimal, "ny_budget":decimal, "ytd_budget":decimal, "nytd_budget":decimal, "nmtd_budget":decimal, "lytd_budget":decimal, "lytd_serv":decimal, "lytd_tax":decimal, "lytoday_serv":decimal, "lytoday_tax":decimal, "month_budget":decimal, "year_budget":decimal, "tischnr":int, "pax":[int, 31]})
    shift_list_list, Shift_list = create_model("Shift_list", {"shift":int, "ftime":int, "ttime":int})
    w2_list, W2 = create_model("W2", {"val_sign":int, "nr1":int, "nr2":int}, {"val_sign": 1})
    tmp_room_list, Tmp_room = create_model("Tmp_room", {"gastnr":int, "zinr":str, "flag":int})
    t_list_list, T_list = create_model("T_list", {"dept":int, "datum":date, "shift":int, "pax_food":int, "pax_bev":int})
    t_rechnr_list, T_rechnr = create_model("T_rechnr", {"datum":date, "dept":int, "rechnr":int, "shift":int, "found_food":bool, "found_bev":bool})
    temp_rechnr_list, Temp_rechnr = create_model("Temp_rechnr", {"datum":date, "dept":int, "rechnr":int, "shift":int, "belegung":int, "artnrfront":int, "compli_flag":bool, "tischnr":int, "betrag":decimal, "artnr":int, "artart":int})
    fbstat_dept_list, Fbstat_dept = create_model("Fbstat_dept", {"done":bool, "dept":int})
    stream_list_list, Stream_list = create_model("Stream_list", {"crow":int, "ccol":int, "cval":str})

    Segmbuff = Segmentstat
    Curr_child = W1
    curr_child_list = w1_list

    Ww1 = W1
    ww1_list = w1_list

    Ww2 = W1
    ww2_list = w1_list

    Wdu = W1
    wdu_list = w1_list

    Hbuff = H_umsatz
    W11 = W1
    w11_list = w1_list

    W12 = W1
    w12_list = w1_list

    W13 = W1
    w13_list = w1_list

    Resbuff = Res_line
    Tbuff = W1
    tbuff_list = w1_list

    W1a = W1
    w1a_list = w1_list

    Ubuff = Umsatz
    Buff_umsatz = Umsatz
    W753 = W1
    w753_list = w1_list

    W754 = W1
    w754_list = w1_list

    W755 = W1
    w755_list = w1_list

    Segmbuffny = Segmentstat
    Wlos = W1
    wlos_list = w1_list

    Buff = H_bill_line
    Art_buff = H_artikel
    Wspc = W1
    wspc_list = w1_list

    Btemp_rechnr = Temp_rechnr
    btemp_rechnr_list = temp_rechnr_list

    Bh_artikel = H_artikel
    Bh_bill_line = H_bill_line
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

    Sourcebuff = Sources
    Sourcebuffny = Sources
    Genstatbuff = Genstat
    Parent = W1
    parent_list = w1_list

    Child = W1
    child_list = w1_list

    Curr_w2 = W2
    curr_w2_list = w2_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list
        return {"msg_str": msg_str, "error_nr": error_nr}

    def fill_value():

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

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
        Ww1 = W1
        Ww2 = W1
        fbstat_dept._list.clear()

        for ww1 in query(ww1_list, filters=(lambda ww1 :ww1.grpflag == 0)):
            num__row = num__row + 1

        for ww1 in query(ww1_list, filters=(lambda ww1 :ww1.grpflag == 0)):

            ww2 = query(ww2_list, filters=(lambda ww2 :ww2.varname == ww1.varname and ww1._recid != ww2._recid), first=True)

            if ww2:
                msg_str = msg_str + chr(2) + translateExtended ("Duplicate name found : ", lvcarea, "") + ww2.varname
                error_nr = -1

                return
        z = 0

        for ww1 in query(ww1_list, filters=(lambda ww1 :ww1.grpflag == 0)):
            z = z + 1
            n__bar = to_int(z * n__pct / num__row)

            ww2 = query(ww2_list, filters=(lambda ww2 :ww2.varname == ww1.varname and ww1._recid != ww2._recid), first=True)

            if ww2:
                msg_str = msg_str + chr(2) + translateExtended ("Duplicate name found : ", lvcarea, "") + ww2.varname
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
                fill_cover(ww1._recid)

            elif ww1.main_code == 197:
                fill_cover(ww1._recid)

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

            elif ww1.main_code == 9000:
                done_los = fill_los()

            elif ww1.main_code == 9106:
                fill_wig(ww1._recid)

            elif ww1.main_code == 85:
                fill_arrdep(ww1._recid, "arrival_RSV", 85, 86, 0)

            elif ww1.main_code == 86:
                fill_arrdep(ww1._recid, "arrival_RSV", 85, 86, 0)

            elif ww1.main_code == 106:
                fill_arrdep(ww1._recid, "arrival_WIG", 106, 107, 0)

            elif ww1.main_code == 107:
                fill_arrdep(ww1._recid, "arrival_WIG", 106, 107, 0)

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
                fill_avrgstay(ww1._recid, "Avrg_Stay", 195)

            elif ww1.main_code == 211:
                fill_arrdep(ww1._recid, "ArrTmrw", 211, 231, 0)

            elif ww1.main_code == 231:
                fill_arrdep(ww1._recid, "ArrTmrw", 211, 231, 0)

            elif ww1.main_code == 742:
                fill_arrdep(ww1._recid, "Early_CO", 742, 0, 0)

            elif ww1.main_code == 750:
                fill_arrdep(ww1._recid, "DepTmrw", 750, 751, 0)

            elif ww1.main_code == 751:
                fill_arrdep(ww1._recid, "DepTmrw", 750, 751, 0)

            elif ww1.main_code == 969:
                fill_arrdep(ww1._recid, "No_Show", 969, 0, 0)

            elif ww1.main_code == 806:
                fill_rmocc(ww1._recid)

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
                fill_rmocc%(ww1._recid)

                if error_nr != 0:

                    return

            elif ww1.main_code == 808:
                fill_docc%(ww1._recid)

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

        for w1 in query(w1_list, filters=(lambda w1 :w1.grpflag >= 1 and w1.grpflag != 9)):

            for w2 in query(w2_list, filters=(lambda w2 :w2.nr1 == w1.nr)):

                curr_child = query(curr_child_list, filters=(lambda curr_child :curr_child.nr == w2.nr2), first=True)
                fill_value1(w1._recid, curr_child._recid, w2.val_sign)

    def fill_adddayuse():

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        done = False
        datum1:date = None

        def generate_inner_output():
            return done
        Wdu = W1

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        res_line_obj_list = []
        for res_line, arrangement in db_session.query(Res_line, Arrangement).join(Arrangement,(Arrangement == Res_line.arrangement)).filter(
                (Res_line.active_flag == 2) &  (Res_line.ankunft >= datum1) &  (Res_line.ankunft <= to_date) &  (Res_line.abreise == Res_line.ankunft) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 99)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            bill_line = db_session.query(Bill_line).filter(
                    (Bill_line.departement == 0) &  (Bill_line.artnr == arrangement.argt_artikelnr) &  (Bill_line.bill_datum == res_line.ankunft) &  (Bill_line.massnr == res_line.resnr) &  (Bill_line.billin_nr == res_line.reslinnr)).first()

            if not bill_line:

                if res_line.ankunft == to_date:
                    wdu.tday = wdu.tday + res_line.zimmeranz

                if res_line.ankunft >= from_date:
                    wdu.saldo = wdu.saldo + res_line.zimmeranz
                wdu.ytd_saldo = wdu.ytd_saldo + res_line.zimmeranz
        done = True


        return generate_inner_output()

    def fill_totroom(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum:date = None
        datum1:date = None
        datum2:date = None
        curr_date:date = None
        anz:int = 0
        anz0:int = 0
        d_flag:bool = False
        dlmtd_flag:bool = False

        w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

        if w1.done:

            return
        anz0 = 0

        for zimmer in db_session.query(Zimmer).all():
            anz0 = anz0 + 1

        if (get_day(to_date) == 31 and get_month(to_date) != 8 and get_month(to_date) != 1) or (get_day(to_date) == 30 and get_month(to_date) == 3) or (get_day(date_mdy(3, 1, get_year(to_date)) - 1) == 28 and get_month(to_date) == 3 and get_day(to_date) == 29):
            w1.lm_today = 0
        else:

            if get_month(to_date) == 1:
                curr_date = date_mdy(12, get_day(to_date) , get_year(to_date) - 1)
            else:
                curr_date = date_mdy(get_month(to_date) - 1, get_day(to_date) , get_year(to_date))

            zinrstat = db_session.query(Zinrstat).filter(
                    (Zinrstat.datum == curr_date) &  (func.lower(Zinrstat.zinr) == "tot_rm")).first()

            if zinrstat:
                w1.lm_today = zinrstat.zimmeranz
            else:
                w1.lm_today = anz0

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date
        for datum in range(datum1,to_date + 1) :

            zinrstat = db_session.query(Zinrstat).filter(
                    (Zinrstat.datum == datum) &  (func.lower(Zinrstat.zinr) == "tot_rm")).first()

            if zinrstat:
                anz = zinrstat.zimmeranz
            else:
                anz = anz0
            d_flag = None != zinrstat and (get_month(zinrstat.datum) == get_month(to_date)) and (get_year(zinrstat.datum) == get_year(to_date))

            if zinrstat:

                if d_flag:
                    w1.mon_saldo[get_day(zinrstat.datum) - 1] = w1.mon_saldo[get_day(zinrstat.datum) - 1] + anz

            if datum == to_date - 1:
                w1.yesterday = w1.yesterday + anz

            if datum == to_date:
                w1.tday = w1.tday + anz

            if start_date != None:

                if (datum < from_date) and (datum >= start_date):
                    w1.ytd_saldo = w1.ytd_saldo + anz
                else:

                    if (datum >= start_date):
                        w1.saldo = w1.saldo + anz

                    if ytd_flag and (datum >= start_date):
                        w1.ytd_saldo = w1.ytd_saldo + anz
            else:

                if datum <= lfr_date:
                    w1.lm_ytd = w1.lm_ytd + anz

                if (datum < from_date):
                    w1.ytd_saldo = w1.ytd_saldo + anz
                else:
                    w1.saldo = w1.saldo + anz

                    if ytd_flag:
                        w1.ytd_saldo = w1.ytd_saldo + anz

        if (lytd_flag or lmtd_flag):

            if lytd_flag:
                datum2 = ljan1
            else:
                datum2 = lfrom_date
            for datum in range(datum2,lto_date + 1) :

                zinrstat = db_session.query(Zinrstat).filter(
                        (Zinrstat.datum == datum) &  (func.lower(Zinrstat.zinr) == "tot_rm")).first()

                if zinrstat:
                    anz = zinrstat.zimmeranz
                else:
                    anz = anz0
                dlmtd_flag = None != zinrstat and (get_month(zinrstat.datum) == get_month(to_date)) and (get_year(zinrstat.datum) == get_year(to_date) - 1)

                if dlmtd_flag:
                    w1.mon_lmtd[get_day(zinrstat.datum) - 1] = w1.mon_lmtd[get_day(zinrstat.datum) - 1] + anz

                if start_date != None:

                    if (datum < lfrom_date) and (datum >= start_date):
                        w1.lytd_saldo = w1.lytd_saldo + anz

                    elif (datum >= start_date):
                        w1.lastyr = w1.lastyr + anz

                        if lytd_flag:
                            w1.lytd_saldo = w1.lytd_saldo + anz
                else:

                    if (datum < lfrom_date):
                        w1.lytd_saldo = w1.lytd_saldo + anz
                    else:
                        w1.lastyr = w1.lastyr + anz

                        if lytd_flag:
                            w1.lytd_saldo = w1.lytd_saldo + anz

        if pmtd_flag:
            for datum in range(pfrom_date,pto_date + 1) :

                zinrstat = db_session.query(Zinrstat).filter(
                        (Zinrstat.datum == datum) &  (func.lower(Zinrstat.zinr) == "tot_rm")).first()

                if zinrstat:
                    anz = zinrstat.zimmeranz
                else:
                    anz = anz0

                if start_date != None:

                    if (datum >= start_date):
                        w1.lastmon = w1.lastmon + anz
                else:
                    w1.lastmon = w1.lastmon + anz

        if lytoday_flag:
            w1.lytoday = anz
        w1.done = True

    def fill_rmavail(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        datum2:date = None
        curr_date:date = None

        w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

        if w1.done:

            return

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        if (get_day(to_date) == 31 and get_month(to_date) != 8 and get_month(to_date) != 1) or (get_day(to_date) == 30 and get_month(to_date) == 3) or (get_day(date_mdy(3, 1, get_year(to_date)) - 1) == 28 and get_month(to_date) == 3 and get_day(to_date) == 29):
            w1.lm_today = 0
        else:

            if get_month(to_date) == 1:
                curr_date = date_mdy(12, get_day(to_date) , get_year(to_date) - 1)
            else:
                curr_date = date_mdy(get_month(to_date) - 1, get_day(to_date) , get_year(to_date))

            zkstat = db_session.query(Zkstat).filter(
                    (Zkstat.datum == curr_date) &  (Zkstat.zikatnr == zimkateg.zikatnr)).first()

            if zkstat:
                w1.lm_today = w1.lm_today + zkstat.anz100

        for zkstat in db_session.query(Zkstat).filter(
                (Zkstat.datum >= datum1) &  (Zkstat.datum <= to_date)).all():

            if zkstat.datum == to_date - 1:
                w1.yesterday = w1.yesterday + zkstat.anz100

            if zkstat.datum == to_date:
                w1.tday = w1.tday + zkstat.anz100

            if zkstat.datum < from_date:
                w1.ytd_saldo = w1.ytd_saldo + zkstat.anz100
            else:
                w1.saldo = w1.saldo + zkstat.anz100

                if ytd_flag:
                    w1.ytd_saldo = w1.ytd_saldo + zkstat.anz100

            if get_month(zkstat.datum) == get_month(to_date) and get_year(zkstat.datum) == get_year(to_date):
                w1.mon_saldo[get_day(zkstat.datum) - 1] = w1.mon_saldo[get_day(zkstat.datum) - 1] + zkstat.anz100

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum2 = ljan1
            else:
                datum2 = lfrom_date

            for zkstat in db_session.query(Zkstat).filter(
                    (Zkstat.datum >= datum2) &  (Zkstat.datum <= lto_date)).all():

                if zkstat.datum < lfrom_date:
                    w1.lytd_saldo = w1.lytd_saldo + zkstat.anz100
                else:
                    w1.lastyr = w1.lastyr + zkstat.anz100

                    if lytd_flag:
                        w1.lytd_saldo = w1.lytd_saldo + zkstat.anz100

        if lytoday_flag:

            for zkstat in db_session.query(Zkstat).filter(
                    (Zkstat.datum == lytoday)).all():
                w1.lytoday = w1.lytoday + zkstat.anz100


        if pmtd_flag:

            for zkstat in db_session.query(Zkstat).filter(
                    (Zkstat.datum >= pfrom_date) &  (Zkstat.datum <= pto_date)).all():
                w1.lastmon = w1.lastmon + zkstat.anz100

        w1.done = True

    def fill_ooo(rec_w1:int, key_word:str):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None

        w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

        if w1.done:

            return

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for zinrstat in db_session.query(Zinrstat).filter(
                    (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= to_date) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).all():

            if zinrstat.datum == to_date:
                w1.tday = w1.tday + zinrstat.zimmeranz

            if zinrstat.datum < from_date:
                w1.ytd_saldo = w1.ytd_saldo + zinrstat.zimmeranz
            else:
                w1.saldo = w1.saldo + zinrstat.zimmeranz

                if ytd_flag:
                    w1.ytd_saldo = w1.ytd_saldo + zinrstat.zimmeranz

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            for zinrstat in db_session.query(Zinrstat).filter(
                        (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= lto_date) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).all():

                if zinrstat.datum < lfrom_date:
                    w1.lytd_saldo = w1.lytd_saldo + zinrstat.zimmeranz
                else:
                    w1.lastyr = w1.lastyr + zinrstat.zimmeranz

                    if lytd_flag:
                        w1.lytd_saldo = w1.lytd_saldo + zinrstat.zimmeranz

        if pmtd_flag:

            for zinrstat in db_session.query(Zinrstat).filter(
                        (Zinrstat.datum >= pfrom_date) &  (Zinrstat.datum <= pto_date) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).all():
                w1.lastmon = w1.lastmon + zinrstat.zimmeranz


        if lytoday_flag:

            zinrstat = db_session.query(Zinrstat).filter(
                        (Zinrstat.datum == lytoday) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).first()

            if zinrstat:
                w1.lytoday = zinrstat.zimmeranz
        w1.done = True

    def fill_vacant(rec_w1:int, key_word:str):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None

        w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

        if w1.done:

            return

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for zinrstat in db_session.query(Zinrstat).filter(
                    (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= to_date) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).all():

            if zinrstat.datum == to_date:
                w1.tday = w1.tday + zinrstat.zimmeranz

            if zinrstat.datum < from_date:
                w1.ytd_saldo = w1.ytd_saldo + zinrstat.zimmeranz
            else:
                w1.saldo = w1.saldo + zinrstat.zimmeranz

                if ytd_flag:
                    w1.ytd_saldo = w1.ytd_saldo + zinrstat.zimmeranz

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            for zinrstat in db_session.query(Zinrstat).filter(
                        (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= lto_date) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).all():

                if zinrstat.datum < lfrom_date:
                    w1.lytd_saldo = w1.lytd_saldo + zinrstat.zimmeranz
                else:
                    w1.lastyr = w1.lastyr + zinrstat.zimmeranz

                    if lytd_flag:
                        w1.lytd_saldo = w1.lytd_saldo + zinrstat.zimmeranz

        if pmtd_flag:

            for zinrstat in db_session.query(Zinrstat).filter(
                        (Zinrstat.datum >= pfrom_date) &  (Zinrstat.datum <= pto_date) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).all():
                w1.lastmon = w1.lastmon + zinrstat.zimmeranz


        if lytoday_flag:

            zinrstat = db_session.query(Zinrstat).filter(
                        (Zinrstat.datum == lytoday) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).first()

            if zinrstat:
                w1.lytoday = zinrstat.zimmeranz
        w1.done = True

    def fill_cover(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        curr_date:date = None
        d_flag:bool = False
        dlmtd_flag:bool = False
        Hbuff = H_umsatz
        W11 = W1
        W12 = W1
        W13 = W1

        w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

        if w1.done:

            return


        w11 = query(w11_list, filters=(lambda w11 :w11.main_code == 552 and w11.dept == w1.dept), first=True)

        w12 = query(w12_list, filters=(lambda w12 :w12.main_code == 192 and w12.dept == w1.dept), first=True)

        w13 = query(w13_list, filters=(lambda w13 :w13.main_code == 197 and w13.dept == w1.dept), first=True)

        if (get_day(to_date) == 31 and get_month(to_date) != 8 and get_month(to_date) != 1) or (get_day(to_date) == 30 and get_month(to_date) == 3) or (get_day(date_mdy(3, 1, get_year(to_date)) - 1) == 28 and get_month(to_date) == 3 and get_day(to_date) == 29):

            if w11:
                w11.lm_today = 0

            if w12:
                w12.lm_today = 0

            if w13:
                w13.lm_today = 0
        else:

            if get_month(to_date) == 1:
                curr_date = date_mdy(12, get_day(to_date) , get_year(to_date) - 1)
            else:
                curr_date = date_mdy(get_month(to_date) - 1, get_day(to_date) , get_year(to_date))

            h_umsatz = db_session.query(H_umsatz).filter(
                    (H_umsatz.datum == curr_date) &  (H_umsatz.artnr == 0) &  (H_umsatz.departement == w1.dept) &  (H_umsatz.betriebsnr == w1.dept)).first()

            if h_umsatz:

                if w11:
                    w11.lm_today = h_umsatz.anzahl

                if w12:
                    w12.lm_today = h_umsatz.betrag

                if w13:
                    w13.lm_today = h_umsatz.nettobetrag

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for h_umsatz in db_session.query(H_umsatz).filter(
                (H_umsatz.datum >= datum1) &  (H_umsatz.datum <= to_date) &  (H_umsatz.artnr == 0) &  (H_umsatz.departement == w1.dept) &  (H_umsatz.betriebsnr == w1.dept)).all():
            d_flag = (get_month(h_umsatz.datum) == get_month(to_date)) and (get_year(h_umsatz.datum) == get_year(to_date))

            if d_flag:

                if w11:
                    w11.mon_saldo[get_day(h_umsatz.datum) - 1] = h_umsatz.anzahl

                if w12:
                    w12.mon_saldo[get_day(h_umsatz.datum) - 1] = h_umsatz.betrag

                if w13:
                    w13.mon_saldo[get_day(h_umsatz.datum) - 1] = h_umsatz.nettobetrag

            if h_umsatz.datum == to_date - 1:

                if w11:
                    w11.yesterday = h_umsatz.anzahl

                if w12:
                    w12.yesterday = h_umsatz.betrag

                if w13:
                    w13.yesterday = h_umsatz.nettobetrag

            if h_umsatz.datum == to_date:

                if w11:
                    w11.tday = h_umsatz.anzahl

                if w12:
                    w12.tday = h_umsatz.betrag

                if w13:
                    w13.tday = h_umsatz.nettobetrag

            if h_umsatz.datum <= lfr_date:

                if w11:
                    w11.lm_ytd = w11.lm_ytd + h_umsatz.anzahl

                if w12:
                    w12.lm_ytd = w12.lm_ytd + h_umsatz.betrag

                if w13:
                    w13.lm_ytd = w13.lm_ytd + h_umsatz.nettobetrag

            if h_umsatz.datum < from_date:

                if w11:
                    w11.ytd_saldo = w11.ytd_saldo + h_umsatz.anzahl

                if w12:
                    w12.ytd_saldo = w12.ytd_saldo + h_umsatz.betrag

                if w13:
                    w13.ytd_saldo = w13.ytd_saldo + h_umsatz.nettobetrag
            else:

                if w11:
                    w11.saldo = w11.saldo + h_umsatz.anzahl

                if ytd_flag and w11:
                    w11.ytd_saldo = w11.ytd_saldo + h_umsatz.anzahl

                if w12:
                    w12.saldo = w12.saldo + h_umsatz.betrag

                if ytd_flag and w12:
                    w12.ytd_saldo = w12.ytd_saldo + h_umsatz.betrag

                if w13:
                    w13.saldo = w13.saldo + h_umsatz.nettobetrag

                if ytd_flag and w13:
                    w13.ytd_saldo = w13.ytd_saldo + h_umsatz.nettobetrag

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            for h_umsatz in db_session.query(H_umsatz).filter(
                    (H_umsatz.datum >= datum1) &  (H_umsatz.datum <= lto_date) &  (H_umsatz.artnr == 0) &  (H_umsatz.departement == w1.dept) &  (H_umsatz.betriebsnr == w1.dept)).all():

                if h_umsatz.datum < lfrom_date:

                    if w11:
                        w11.lytd_saldo = w11.lytd_saldo + h_umsatz.anzahl

                    if w12:
                        w12.lytd_saldo = w12.lytd_saldo + h_umsatz.betrag

                    if w13:
                        w13.lytd_saldo = w13.lytd_saldo + h_umsatz.nettobetrag
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
                        w11.lastyr = w11.lastyr + h_umsatz.anzahl

                    if lytd_flag and w11:
                        w11.lytd_saldo = w11.lytd_saldo + h_umsatz.anzahl

                    if w12:
                        w12.lastyr = w12.lastyr + h_umsatz.betrag

                    if lytd_flag and w12:
                        w12.lytd_saldo = w12.lytd_saldo + h_umsatz.betrag

                    if w13:
                        w13.lastyr = w13.lastyr + h_umsatz.nettobetrag

                    if lytd_flag and w13:
                        w13.lytd_saldo = w13.lytd_saldo + h_umsatz.nettobetrag

        if pmtd_flag:

            for h_umsatz in db_session.query(H_umsatz).filter(
                    (H_umsatz.datum >= pfrom_date) &  (H_umsatz.datum <= pto_date) &  (H_umsatz.artnr == 0) &  (H_umsatz.departement == w1.dept) &  (H_umsatz.betriebsnr == w1.dept)).all():

                if w11:
                    w11.lastmon = w11.lastmon + h_umsatz.anzahl

                if w12:
                    w12.lastmon = w12.lastmon + h_umsatz.betrag

                if w13:
                    w13.lastmon = w13.lastmon + h_umsatz.nettobetrag


        if lytoday_flag:

            for h_umsatz in db_session.query(H_umsatz).filter(
                    (H_umsatz.datum == lytoday) &  (H_umsatz.artnr == 0) &  (H_umsatz.departement == w1.dept) &  (H_umsatz.betriebsnr == w1.dept)).all():

                if w11:
                    w11.lytoday = w11.lytoday + h_umsatz.anzahl

                if w12:
                    w12.lytoday = w12.lytoday + h_umsatz.betrag

                if w13:
                    w13.lytoday = w13.lytoday + h_umsatz.nettobetrag


        if w11:
            w11.done = True

        if w12:
            w12.done = True

        if w13:
            w13.done = True

    def fill_canc_room_night(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        Resbuff = Res_line

        w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

        if w1.done:

            return

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        if w1:

            for resbuff in db_session.query(Resbuff).filter(
                    (Resbuff.resstatus == 9) &  (Resbuff.active_flag == 2) &  (Resbuff.betrieb_gastpay != 3) &  (Resbuff.CANCELLED >= datum1) &  (Resbuff.CANCELLED <= to_date) &  (Resbuff.l_zuordnung[2] == 0)).all():

                if resbuff.CANCELLED == to_date:
                    w1.tday = w1.tday + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz

                if resbuff.CANCELLED < from_date:
                    w1.ytd_saldo = w1.ytd_saldo + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz
                else:
                    w1.saldo = w1.saldo + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz

                    if ytd_flag:
                        w1.ytd_saldo = w1.ytd_saldo + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz

            if lytd_flag or lmtd_flag:

                if lytd_flag:
                    datum1 = ljan1
                else:
                    datum1 = lfrom_date

                for resbuff in db_session.query(Resbuff).filter(
                        (Resbuff.resstatus == 9) &  (Resbuff.active_flag == 2) &  (Resbuff.betrieb_gastpay != 3) &  (Resbuff.CANCELLED >= datum1) &  (Resbuff.CANCELLED <= lto_date) &  (Resbuff.l_zuordnung[2] == 0)).all():

                    if resbuff.CANCELLED < lfrom_date:
                        w1.lytd_saldo = w1.ytd_saldo + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz
                    else:
                        w1.lastyr = w1.lastyr + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz

                        if lytd_flag:
                            w1.lytd_saldo = w1.lytd_saldo + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz

    def fill_canc_cidate(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        Resbuff = Res_line

        w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

        if w1.done:

            return

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        if w1:

            for resbuff in db_session.query(Resbuff).filter(
                    (Resbuff.resstatus == 9) &  (Resbuff.active_flag == 2) &  (Resbuff.betrieb_gastpay != 3) &  (Resbuff.CANCELLED >= datum1) &  (Resbuff.CANCELLED <= to_date) &  (Resbuff.CANCELLED == Resbuff.ankunft) &  (Resbuff.l_zuordnung[2] == 0)).all():

                if resbuff.ankunft == to_date:
                    w1.tday = w1.tday + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz

                if resbuff.CANCELLED < from_date:
                    w1.ytd_saldo = w1.ytd_saldo + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz
                else:
                    w1.saldo = w1.saldo + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz

                    if ytd_flag:
                        w1.ytd_saldo = w1.ytd_saldo + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz

            if lytd_flag or lmtd_flag:

                if lytd_flag:
                    datum1 = ljan1
                else:
                    datum1 = lfrom_date

                for resbuff in db_session.query(Resbuff).filter(
                        (Resbuff.resstatus == 9) &  (Resbuff.active_flag == 2) &  (Resbuff.betrieb_gastpay != 3) &  (Resbuff.CANCELLED >= datum1) &  (Resbuff.CANCELLED <= lto_date) &  (Resbuff.CANCELLED == Resbuff.ankunft) &  (Resbuff.l_zuordnung[2] == 0)).all():

                    if resbuff.ankunft < lfrom_date:
                        w1.lytd_saldo = w1.ytd_saldo + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz
                    else:
                        w1.lastyr = w1.lastyr + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz

                        if lytd_flag:
                            w1.lytd_saldo = w1.lytd_saldo + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz

    def fill_arrdep(rec_w1:int, key_word:str, number1:int, number2:int, number3:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        curr_date:date = None
        W11 = W1
        W12 = W1
        W13 = W1

        w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

        if w1.done:

            return


        if number1 != 0:

            w11 = query(w11_list, filters=(lambda w11 :w11.main_code == number1 and not w11.done), first=True)

        if number2 != 0:

            w12 = query(w12_list, filters=(lambda w12 :w12.main_code == number2 and not w12.done), first=True)

        if number3 != 0:

            w13 = query(w13_list, filters=(lambda w13 :w13.main_code == number3 and not w13.done), first=True)

        if (get_day(to_date) == 31 and get_month(to_date) != 8 and get_month(to_date) != 1) or (get_day(to_date) == 30 and get_month(to_date) == 3) or (get_day(date_mdy(3, 1, get_year(to_date)) - 1) == 28 and get_month(to_date) == 3 and get_day(to_date) == 29):

            if w11:
                w11.lm_today = 0

            if w12:
                w12.lm_today = 0
        else:

            if get_month(to_date) == 1:
                curr_date = date_mdy(12, get_day(to_date) , get_year(to_date) - 1)
            else:
                curr_date = date_mdy(get_month(to_date) - 1, get_day(to_date) , get_year(to_date))

            zinrstat = db_session.query(Zinrstat).filter(
                    (Zinrstat.datum == curr_date) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).first()

            if zinrstat:

                if w11:
                    w11.lm_today = w11.lm_today + zinrstat.zimmeranz

                if w12:
                    w12.lm_today = w12.lm_today + zinrstat.personen

                if w13:
                    w13.lm_today = w13.lm_today + zinrstat.betriebsnr

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for zinrstat in db_session.query(Zinrstat).filter(
                    (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= to_date) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).all():

            if zinrstat.datum == to_date - 1:

                if w11:
                    w11.yesterday = w11.yesterday + zinrstat.zimmeranz

                if w12:
                    w12.yesterday = w12.yesterday + zinrstat.personen

                if w13:
                    w13.yesterday = w13.yesterday + zinrstat.betriebsnr

            if zinrstat.datum == to_date:

                if w11:
                    w11.tday = w11.tday + zinrstat.zimmeranz

                if w12:
                    w12.tday = w12.tday + zinrstat.personen

                if w13:
                    w13.tday = w13.tday + zinrstat.betriebsnr

            if zinrstat.datum < from_date:

                if w11:
                    w11.ytd_saldo = w11.ytd_saldo + zinrstat.zimmeranz

                if w12:
                    w12.ytd_saldo = w12.ytd_saldo + zinrstat.personen

                if w13:
                    w13.ytd_saldo = w13.ytd_saldo + zinrstat.betriebsnr
            else:

                if w11:
                    w11.saldo = w11.saldo + zinrstat.zimmeranz

                if ytd_flag and w11:
                    w11.ytd_saldo = w11.ytd_saldo + zinrstat.zimmeranz

                if w12:
                    w12.saldo = w12.saldo + zinrstat.personen

                if ytd_flag and w12:
                    w12.ytd_saldo = w12.ytd_saldo + zinrstat.personen

                if w13:
                    w13.saldo = w13.saldo + zinrstat.betriebsnr

                if ytd_flag and w13:
                    w13.ytd_saldo = w13.ytd_saldo + zinrstat.betriebsnr

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            for zinrstat in db_session.query(Zinrstat).filter(
                        (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= lto_date) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).all():

                if zinrstat.datum < lfrom_date:

                    if w11:
                        w11.lytd_saldo = w11.lytd_saldo + zinrstat.zimmeranz

                    if w12:
                        w12.lytd_saldo = w12.lytd_saldo + zinrstat.personen

                    if w13:
                        w13.lytd_saldo = w13.lytd_saldo + zinrstat.betriebsnr
                else:

                    if w11:
                        w11.lastyr = w11.lastyr + zinrstat.zimmeranz

                    if lytd_flag and w11:
                        w11.lytd_saldo = w11.lytd_saldo + zinrstat.zimmeranz

                    if w12:
                        w12.lastyr = w12.lastyr + zinrstat.personen

                    if lytd_flag and w12:
                        w12.lytd_saldo = w12.lytd_saldo + zinrstat.personen

                    if w13:
                        w13.lastyr = w13.lastyr + zinrstat.betriebsnr

                    if lytd_flag and w13:
                        w13.lytd_saldo = w13.lytd_saldo + zinrstat.betriebsnr

        if pmtd_flag:

            for zinrstat in db_session.query(Zinrstat).filter(
                        (Zinrstat.datum >= pfrom_date) &  (Zinrstat.datum <= pto_date) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).all():

                if w11:
                    w11.lastmon = w11.lastmon + zinrstat.zimmeranz

                if w12:
                    w12.lastmon = w12.lastmon + zinrstat.personen

                if w13:
                    w13.lastmon = w13.lastmon + zinrstat.betriebsnr


        if lytoday_flag:

            zinrstat = db_session.query(Zinrstat).filter(
                        (Zinrstat.datum == lytoday) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).first()

            if zinrstat:

                if w11:
                    w11.lytoday = zinrstat.zimmeranz

                if w12:
                    w12.lytoday = zinrstat.personen

                if w13:
                    w13.lytoday = zinrstat.betriebsnr

        if w11:
            w11.done = True

        if w12:
            w12.done = True

        if w13:
            w13.done = True

    def fill_avrgstay(rec_w1:int, key_word:str, number1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        W11 = W1
        Tbuff = W1

        w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

        if w1.done:

            return

        if number1 != 0:

            w11 = query(w11_list, filters=(lambda w11 :w11.main_code == number1 and not w11.done), first=True)

        if not w11:

            return
        tbuff = Tbuff()
        tbuff_list.append(tbuff)


        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for zinrstat in db_session.query(Zinrstat).filter(
                    (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= to_date) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).all():

            if zinrstat.datum == to_date:
                w11.tday = w11.tday + zinrstat.personen / zinrstat.zimmeranz

            if (zinrstat.datum < from_date):
                w11.ytd_saldo = w11.ytd_saldo + zinrstat.personen
                tbuff.ytd_saldo = tbuff.ytd_saldo + zinrstat.zimmeranz
            else:
                w11.saldo = w11.saldo + zinrstat.personen
                tbuff.saldo = tbuff.saldo + zinrstat.zimmeranz

                if ytd_flag:
                    w11.ytd_saldo = w11.ytd_saldo + zinrstat.personen
                    tbuff.ytd_saldo = tbuff.ytd_saldo + zinrstat.zimmeranz

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            for zinrstat in db_session.query(Zinrstat).filter(
                        (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= lto_date) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).all():

                if zinrstat.datum < lfrom_date:
                    w11.lytd_saldo = w11.lytd_saldo + zinrstat.personen
                    tbuff.lytd_saldo = tbuff.lytd_saldo + zinrstat.zimmeranz
                else:
                    w11.lastyr = w11.lastyr + zinrstat.personen
                    tbuff.lastyr = tbuff.lastyr + zinrstat.zimmeranz

                    if lytd_flag:
                        w11.lytd_saldo = w11.lytd_saldo + zinrstat.personen
                        tbuff.lytd_saldo = tbuff.lytd_saldo + zinrstat.zimmeranz

        if pmtd_flag:

            for zinrstat in db_session.query(Zinrstat).filter(
                        (Zinrstat.datum >= pfrom_date) &  (Zinrstat.datum <= pto_date) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).all():
                w11.lastmon = w11.lastmon + zinrstat.personen
                tbuff.lastmon = tbuff.lastmon + zinrstat.zimmeranz


        if lytoday_flag:

            zinrstat = db_session.query(Zinrstat).filter(
                        (Zinrstat.datum == lytoday) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).first()

            if zinrstat:
                w11.lytoday = zinrstat.personen
                tbuff.lytoday = zinrstat.zimmeranz

        if tbuff.saldo != 0:
            w11.saldo = w11.saldo / tbuff.saldo

        if tbuff.ytd_saldo != 0:
            w11.ytd_saldo = w11.ytd_saldo / tbuff.ytd_saldo

        if tbuff.lytd_saldo != 0:
            w11.lytd_saldo = w11.lytd_saldo / tbuff.lytd_saldo

        if tbuff.lastyr != 0:
            w11.lastyr = w11.lastyr / tbuff.lastyr

        if tbuff.lastmon != 0:
            w11.lastmon = w11.lastmon / tbuff.lastmon

        if tbuff.lytoday != 0:
            w11.lytoday = w11.lytoday / tbuff.lytoday
        w11.done = True
        tbuff_list.remove(tbuff)

    def fill_gledger(rec_w1:int, rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        curr_date:date = None
        datum1:date = None
        datum2:date = None
        d_flag:bool = False
        dbudget_flag:bool = False
        dlmtd_flag:bool = False
        frate1:decimal = 0
        datum1:date = None
        W1a = W1

        w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

        if w1.done:

            return

        w1a = query(w1a_list, filters=(lambda w1a :w1a.main_code == 810), first=True)

        if w1a and w1a.done:


            if ytd_flag:
                datum1 = jan1
            else:
                datum1 = from_date

            for segment in db_session.query(Segment).all():

                for segmentstat in db_session.query(Segmentstat).filter(
                        (Segmentstat.datum >= datum1) &  (Segmentstat.datum <= to_date) &  (Segmentstat.segmentcode == segmentcode)).all():
                    frate = 1

                    if foreign_flag:
                        find_exrate(segmentstat.datum)

                        if exrate:
                            frate = exrate.betrag
                    d_flag = (get_month(segmentstat.datum) == get_month(to_date)) and (get_year(segmentstat.datum) == get_year(to_date))
                    dbudget_flag = (get_month(segmentstat.datum) == get_month(to_date)) and (get_year(segmentstat.datum) == get_year(to_date))

                    if segmentstat.datum == to_date - 1:

                        if w1a:
                            w1a.yesterday = w1a.yesterday + segmentstat.persanz +\
                                    segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis

                    if segmentstat.datum == to_date:
                        w1.tday = w1.tday + segmentstat.zimmeranz
                        w1.tbudget = w1.tbudget + segmentstat.budzimmeranz

                        if w1a:
                            w1a.tday = w1a.tday + segmentstat.persanz +\
                                    segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis


                            w1a.tbudget = w1a.tbudget + segmentstat.budpersanz

                    if segmentstat.datum < from_date:
                        w1.ytd_saldo = w1.ytd_saldo + segmentstat.zimmeranz
                        w1.ytd_budget = w1.ytd_budget + segmentstat.budzimmeranz

                        if w1a:
                            w1a.ytd_saldo = w1a.ytd_saldo + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
                            w1a.ytd_budget = w1a.ytd_budget + segmentstat.budpersanz
                    else:
                        w1.saldo = w1.saldo + segmentstat.zimmeranz
                        w1.budget = w1.budget + segmentstat.budzimmeranz

                        if d_flag:
                            w1.mon_saldo[get_day(segmentstat.datum) - 1] = w1.mon_saldo[get_day(segmentstat.datum) - 1] + segmentstat.zimmeranz

                        if dbudget_flag:
                            w1.mon_budget[get_day(segmentstat.datum) - 1] = w1.mon_budget[get_day(segmentstat.datum) - 1] + segmentstat.budzimmeranz

                        if ytd_flag:
                            w1.ytd_saldo = w1.ytd_saldo + segmentstat.zimmeranz
                            w1.ytd_budget = w1.ytd_budget + segmentstat.budzimmeranz

                        if w1a:
                            w1a.saldo = w1a.saldo + segmentstat.persanz +\
                                    segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
                            w1a.budget = w1a.budget + segmentstat.budpersanz

                            if d_flag:
                                w1a.mon_saldo[get_day(segmentstat.datum) - 1] = w1a.mon_saldo[get_day(segmentstat.datum) - 1] + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis

                            if dbudget_flag:
                                w1a.mon_budget[get_day(segmentstat.datum) - 1] = w1a.mon_budget[get_day(segmentstat.datum) - 1] + segmentstat.budpersanz

                            if ytd_flag:
                                w1a.ytd_saldo = w1a.ytd_saldo + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
                                w1a.ytd_budget = w1a.ytd_budget + segmentstat.budpersanz

                if lytd_flag or lmtd_flag:

                    if lytd_flag:
                        datum2 = ljan1
                    else:
                        datum2 = lfrom_date

                    for segmentstat in db_session.query(Segmentstat).filter(
                            (Segmentstat.datum >= datum2) &  (Segmentstat.datum <= lto_date) &  (Segmentstat.segmentcode == segmentcode)).all():
                        frate = 1

                        if foreign_flag:
                            find_exrate(segmentstat.datum)

                            if exrate:
                                frate = exrate.betrag

                        if segmentstat.datum < lfrom_date:
                            w1.lytd_saldo = w1.lytd_saldo + segmentstat.zimmeranz
                            w1.lytd_budget = w1.lytd_budget + segmentstat.budzimmeranz

                            if w1a:
                                w1a.lytd_saldo = w1a.lytd_saldo + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
                                w1a.lytd_budget = w1a.lytd_budget + segmentstat.budpersanz
                        else:
                            dlmtd_flag = (get_month(segmentstat.datum) == get_month(to_date)) and (get_year(segmentstat.datum) == get_year(to_date) - 1)

                            if dlmtd_flag:
                                w1.mon_lmtd[get_day(segmentstat.datum) - 1] = w1.mon_lmtd[get_day(segmentstat.datum) - 1] + segmentstat.zimmeranz
                            w1.lastyr = w1.lastyr + segmentstat.zimmeranz

                            if lytd_flag:
                                w1.lytd_saldo = w1.lytd_saldo + segmentstat.zimmeranz
                            w1.ly_budget = w1.ly_budget + segmentstat.budzimmeranz

                            if lytd_flag:
                                w1.lytd_budget = w1.lytd_budget + segmentstat.budzimmeranz

                            if w1a:

                                if dlmtd_flag:
                                    w1a.mon_lmtd[get_day(segmentstat.datum) - 1] = w1a.mon_lmtd[get_day(segmentstat.datum) - 1] + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
                                w1a.lastyr = w1a.lastyr + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
                                w1a.ly_budget = w1a.ly_budget + segmentstat.budpersanz

                                if lytd_flag:
                                    w1a.lytd_saldo = w1a.lytd_saldo + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
                                    w1a.lytd_budget = w1a.lytd_budget + segmentstat.budpersanz

                if pmtd_flag:

                    for segmentstat in db_session.query(Segmentstat).filter(
                            (Segmentstat.datum >= pfrom_date) &  (Segmentstat.datum <= pto_date) &  (Segmentstat.segmentcode == segmentcode)).all():
                        frate = 1

                        if foreign_flag:
                            find_exrate(segmentstat.datum)

                            if exrate:
                                frate = exrate.betrag
                        w1.lastmon = w1.lastmon + segmentstat.zimmeranz
                        w1.lm_budget = w1.lm_budget + segmentstat.budzimmeranz

                        if w1a:
                            w1a.lastmon = w1a.lastmon + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
                            w1a.lm_budget = w1a.lm_budget + segmentstat.budpersanz


                if lytoday_flag:

                    for segmentstat in db_session.query(Segmentstat).filter(
                            (Segmentstat.datum == lytoday) &  (Segmentstat.segmentcode == segmentcode)).all():
                        frate = 1

                        if foreign_flag:
                            find_exrate(segmentstat.datum)

                            if exrate:
                                frate = exrate.betrag
                        w1.lytoday = w1.lytoday + segmentstat.zimmeranz

                        if w1a:
                            w1a.lytoday = w1a.lytoday + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis

            w1.done = True

            if w1a:
                w1a.done = True
            W11 = W1
            W12 = W1

            w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

            if w1.done:

                return

            for uebertrag in db_session.query(Uebertrag).filter(
                    (Uebertrag.datum >= from_date - 1) &  (Uebertrag.datum <= to_date - 1)).all():
                w1.mon_saldo[get_day(uebertrag.datum + 1) - 1] = uebertrag.betrag

            uebertrag = db_session.query(Uebertrag).filter(
                    (Uebertrag.datum == to_date - 1)).first()

            if uebertrag:
                w1.tday = uebertrag.betrag
                w1.done = True

    def fill_comproomsnew(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        mm:int = 0

            w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

            if ytd_flag:
                datum1 = jan1
            else:
                datum1 = from_date
            mm = get_month(to_date)

            genstat_obj_list = []
            for genstat, segment in db_session.query(Genstat, Segment).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).filter(
                    (Genstat.datum >= datum1) &  (Genstat.datum <= to_date) &  (Genstat.zipreis == 0) &  (Genstat.gratis != 0) &  (Genstat.resstatus == 6)).all():
                if genstat._recid in genstat_obj_list:
                    continue
                else:
                    genstat_obj_list.append(genstat._recid)

                if segment.betriebsnr == 0:

                    if genstat.datum == to_date:
                        w1.tday = w1.tday + 1

                    if get_month(genstat.datum) == mm:
                        w1.saldo = w1.saldo + 1
                    w1.ytd_saldo = w1.ytd_saldo + 1

            if (lytd_flag or lmtd_flag):

                if lytd_flag:
                    datum1 = ljan1
                else:
                    datum1 = lfrom_date
                mm = get_month(lto_date)

                genstat_obj_list = []
                for genstat, segment in db_session.query(Genstat, Segment).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).filter(
                        (Genstat.datum >= datum1) &  (Genstat.datum <= lto_date) &  (Genstat.zipreis == 0) &  (Genstat.gratis != 0) &  (Genstat.resstatus == 6)).all():
                    if genstat._recid in genstat_obj_list:
                        continue
                    else:
                        genstat_obj_list.append(genstat._recid)

                    if segment.betriebsnr == 0:

                        if get_month(genstat.datum) == mm:
                            w1.lastyr = w1.lastyr + 1
                        w1.lytd_saldo = w1.lytd_saldo + 1

            if pmtd_flag:
                mm = get_month(pto_date)

                genstat_obj_list = []
                for genstat, segment in db_session.query(Genstat, Segment).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).filter(
                        (Genstat.datum >= pfrom_date) &  (Genstat.datum <= pto_date) &  (Genstat.zipreis == 0) &  (Genstat.gratis != 0) &  (Genstat.resstatus == 6)).all():
                    if genstat._recid in genstat_obj_list:
                        continue
                    else:
                        genstat_obj_list.append(genstat._recid)

                    if segment.betriebsnr == 0:

                        if get_month(genstat.datum) == mm:
                            w1.lastmon = w1.lastmon + 1

    def fill_comprooms(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        datum2:date = None
        curr_date:date = None
        d_flag:bool = False

            w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

            if w1.done:

                return

            if ytd_flag:
                datum1 = jan1
            else:
                datum1 = from_date

            for segment in db_session.query(Segment).filter(
                    (Segment.betriebsnr == 0)).all():

                if (get_day(to_date) == 31 and get_month(to_date) != 8 and get_month(to_date) != 1) or (get_day(to_date) == 30 and get_month(to_date) == 3) or (get_day(date_mdy(3, 1, get_year(to_date)) - 1) == 28 and get_month(to_date) == 3 and get_day(to_date) == 29):
                    w1.lm_today = 0
                else:

                    if get_month(to_date) == 1:
                        curr_date = date_mdy(12, get_day(to_date) , get_year(to_date) - 1)
                    else:
                        curr_date = date_mdy(get_month(to_date) - 1, get_day(to_date) , get_year(to_date))

                    segmentstat = db_session.query(Segmentstat).filter(
                            (Segmentstat.datum == curr_date) &  (Segmentstat.segmentcode == segmentcode) &  (Segmentstat.betriebsnr > 0)).first()

                    if segmentstat:
                        frate = 1

                        if foreign_flag:
                            find_exrate(segmentstat.datum)

                            if exrate:
                                frate = exrate.betrag
                        w1.lm_today = w1.lm_today + segmentstat.betriebsnr

                for segmentstat in db_session.query(Segmentstat).filter(
                        (Segmentstat.datum >= datum1) &  (Segmentstat.datum <= to_date) &  (Segmentstat.segmentcode == segmentcode) &  (Segmentstat.betriebsnr > 0)).all():
                    frate = 1

                    if foreign_flag:
                        find_exrate(segmentstat.datum)

                        if exrate:
                            frate = exrate.betrag
                    d_flag = (get_month(segmentstat.datum) == get_month(to_date)) and (get_year(segmentstat.datum) == get_year(to_date))

                    if segmentstat.datum == to_date - 1:
                        w1.yesterday = w1.yesterday + segmentstat.betriebsnr

                    if segmentstat.datum == to_date:
                        w1.tday = w1.tday + segmentstat.betriebsnr

                    if segmentstat.datum < from_date:
                        w1.ytd_saldo = w1.ytd_saldo + segmentstat.betriebsnr
                    else:
                        w1.saldo = w1.saldo + segmentstat.betriebsnr

                        if d_flag:
                            w1.mon_saldo[get_day(segmentstat.datum) - 1] = w1.mon_saldo[get_day(segmentstat.datum) - 1] + segmentstat.betriebsnr

                        if ytd_flag:
                            w1.ytd_saldo = w1.ytd_saldo + segmentstat.betriebsnr

                if lytd_flag or lmtd_flag:

                    if lytd_flag:
                        datum2 = ljan1
                    else:
                        datum2 = lfrom_date

                    for segmentstat in db_session.query(Segmentstat).filter(
                            (Segmentstat.datum >= datum2) &  (Segmentstat.datum <= lto_date) &  (Segmentstat.segmentcode == segmentcode)).all():

                        if foreign_flag:
                            find_exrate(segmentstat.datum)

                            if exrate:
                                frate = exrate.betrag

                        if segmentstat.datum < lfrom_date:
                            w1.lytd_saldo = w1.lytd_saldo + segmentstat.betriebsnr
                        else:
                            w1.lastyr = w1.lastyr + segmentstat.betriebsnr

                            if lytd_flag:
                                w1.lytd_saldo = w1.lytd_saldo + segmentstat.betriebsnr

                if pmtd_flag:

                    for segmentstat in db_session.query(Segmentstat).filter(
                            (Segmentstat.datum >= pfrom_date) &  (Segmentstat.datum <= pto_date) &  (Segmentstat.segmentcode == segmentcode)).all():
                        frate = 1

                        if foreign_flag:
                            find_exrate(segmentstat.datum)

                            if exrate:
                                frate = exrate.betrag
                        w1.lastmon = w1.lastmon + segmentstat.betriebsnr


                if lytoday_flag:

                    for segmentstat in db_session.query(Segmentstat).filter(
                            (Segmentstat.datum == lytoday) &  (Segmentstat.segmentcode == segmentcode)).all():
                        frate = 1

                        if foreign_flag:
                            find_exrate(segmentstat.datum)

                            if exrate:
                                frate = exrate.betrag
                        w1.lytoday = w1.lytoday + segmentstat.betriebsnr

            w1.done = True

    def fill_rmocc%(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
            W11 = W1
            W12 = W1

            w11 = query(w11_list, filters=(lambda w11 :w11.main_code == 805), first=True)

            if not w11:
                msg_str = msg_str + chr(2) + translateExtended ("Variable for Room Availablity not defined,", lvcarea, "") + chr(10) + translateExtended ("which is necessary for calculating of room occupancy.", lvcarea, "")
                prog_error = True
                error_nr = - 1

                return

            w12 = query(w12_list, filters=(lambda w12 :w12.main_code == 806), first=True)

            if not w12:
                msg_str = msg_str + chr(2) + translateExtended ("Variable for Occupied Rooms not defined,", lvcarea, "") + chr(10) + translateExtended ("which is necessary for calculating of room occupancy in %.", lvcarea, "")
                prog_error = True
                error_nr = - 1

                return

            if not w11.done:
                fill_rmavail(w11._recid)

            if not w12.done:
                fill_rmocc(w12._recid)

            w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

            if w1.done:

                return

            if w11.tday != 0:
                w1.tday = w12.tday / w11.tday * 100

            if w11.saldo != 0:
                w1.saldo = w12.saldo / w11.saldo * 100

            if w11.ytd_saldo != 0:
                w1.ytd_saldo = w12.ytd_saldo / w11.ytd_saldo * 100

            if w11.lytd_saldo != 0:
                w1.lytd_saldo = w12.lytd_saldo / w11.lytd_saldo * 100

            if w11.lastyr != 0:
                w1.lastyr = w12.lastyr / w11.lastyr * 100

            if w11.lastmon != 0:
                w1.lastmon = w12.lastmon / w11.lastmon * 100

            if w11.lytoday != 0:
                w1.lytoday = w12.lytoday / w11.lytoday * 100
            w1.done = True

    def fill_docc%(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
            W11 = W1
            W12 = W1

            w11 = query(w11_list, filters=(lambda w11 :w11.main_code == 806), first=True)

            if not w11:
                msg_str = msg_str + chr(2) + translateExtended ("Variable for Occupied Rooms not defined,", lvcarea, "") + chr(10) + translateExtended ("which is necessary for calculating of double room occupancy.", lvcarea, "")
                prog_error = True
                error_nr = - 1

                return

            w12 = query(w12_list, filters=(lambda w12 :w12.main_code == 810), first=True)

            if not w12:
                msg_str = msg_str + chr(2) + translateExtended ("Variable for Occupied Persons not defined,", lvcarea, "") + chr(10) + translateExtended ("which is necessary for calculating of double room occupancy.", lvcarea, "")
                prog_error = True
                error_nr = - 1

                return

            if not w11.done:
                fill_rmocc(w11._recid)

            if not w12.done:
                fill_persocc(w12._recid)

            w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

            if w1.done:

                return

            if w11.tday != 0:
                w1.tday = (w12.tday - w11.tday) / w11.tday * 100

            if w11.saldo != 0:
                w1.saldo = (w12.saldo - w11.saldo) / w11.saldo * 100

            if w11.ytd_saldo != 0:
                w1.ytd_saldo = (w12.ytd_saldo - w11.ytd_saldo) / w11.ytd_saldo * 100

            if w11.lytd_saldo != 0:
                w1.lytd_saldo = (w12.lytd_saldo - w11.lytd_saldo) / w11.lytd_saldo * 100

            if w11.lastyr != 0:
                w1.lastyr = (w12.lastyr - w11.lastyr) / w11.lastyr * 100

            if w11.lastmon != 0:
                w1.lastmon = (w12.lastmon - w11.lastmon) / w11.lastmon * 100

            if w11.lytoday != 0:
                w1.lytoday = (w12.lytoday - w11.lytoday) / w11.lytoday * 100
            w1.done = True

    def fill_fbcost(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        datum2:date = None
        cost:decimal = 0

            w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

            if w1.done:

                return

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == w1.artnr) &  (Artikel.departement == w1.dept)).first()

            if not artikel:
                msg_str = msg_str + chr(2) + translateExtended ("Article for cost_variable not found : ", lvcarea, "") + w1.varname
                error_nr = -1

                return

            if ytd_flag:
                datum1 = jan1
            else:
                datum1 = from_date

            h_umsatz_obj_list = []
            for h_umsatz, h_artikel in db_session.query(H_umsatz, H_artikel).join(H_artikel,(H_artikel.artnr == H_umsatz.artnr) &  (H_artikel.departement == H_umsatz.departement) &  (H_artikel.artnrfront == artikel.artnr)).filter(
                    (H_umsatz.datum >= datum1) &  (H_umsatz.datum <= to_date) &  (H_umsatz.departement == w1.dept)).all():
                if h_umsatz._recid in h_umsatz_obj_list:
                    continue
                else:
                    h_umsatz_obj_list.append(h_umsatz._recid)


                cost = cal_fbcost(h_umsatz.artnr, h_umsatz.departement, h_umsatz.datum)

                if h_umsatz.datum == to_date:
                    w1.tday = w1.tday + cost

                if h_umsatz.datum < from_date:
                    w1.ytd_saldo = w1.ytd_saldo + cost
                else:
                    w1.saldo = w1.saldo + cost

                    if ytd_flag:
                        w1.ytd_saldo = w1.ytd_saldo + cost

            if lytd_flag or lmtd_flag:

                if lytd_flag:
                    datum1 = ljan1
                else:
                    datum1 = lfrom_date

                h_umsatz_obj_list = []
                for h_umsatz, h_artikel in db_session.query(H_umsatz, H_artikel).join(H_artikel,(H_artikel.artnr == H_umsatz.artnr) &  (H_artikel.departement == H_umsatz.departement) &  (H_artikel.artnrfront == artikel.artnr)).filter(
                        (H_umsatz.datum >= datum1) &  (H_umsatz.datum <= lto_date) &  (H_umsatz.departement == w1.dept)).all():
                    if h_umsatz._recid in h_umsatz_obj_list:
                        continue
                    else:
                        h_umsatz_obj_list.append(h_umsatz._recid)


                    cost = cal_fbcost(h_umsatz.artnr, h_umsatz.departement, h_umsatz.datum)

                    if h_umsatz.datum < lfrom_date:
                        w1.lytd_saldo = w1.lytd_saldo + cost
                    else:
                        w1.lastyr = w1.lastyr + cost

                        if lytd_flag:
                            w1.lytd_saldo = w1.lytd_saldo + cost

            if pmtd_flag:

                h_umsatz_obj_list = []
                for h_umsatz, h_artikel in db_session.query(H_umsatz, H_artikel).join(H_artikel,(H_artikel.artnr == H_umsatz.artnr) &  (H_artikel.departement == H_umsatz.departement) &  (H_artikel.artnrfront == artikel.artnr)).filter(
                        (H_umsatz.datum >= pfrom_date) &  (H_umsatz.datum <= pto_date) &  (H_umsatz.departement == w1.dept)).all():
                    if h_umsatz._recid in h_umsatz_obj_list:
                        continue
                    else:
                        h_umsatz_obj_list.append(h_umsatz._recid)


                    cost = cal_fbcost(h_umsatz.artnr, h_umsatz.departement, h_umsatz.datum)
                    w1.lastmon = w1.lastmon + cost


            if lytoday_flag:

                h_umsatz_obj_list = []
                for h_umsatz, h_artikel in db_session.query(H_umsatz, H_artikel).join(H_artikel,(H_artikel.artnr == H_umsatz.artnr) &  (H_artikel.departement == H_umsatz.departement) &  (H_artikel.artnrfront == artikel.artnr)).filter(
                        (H_umsatz.datum == lytoday) &  (H_umsatz.departement == w1.dept)).all():
                    if h_umsatz._recid in h_umsatz_obj_list:
                        continue
                    else:
                        h_umsatz_obj_list.append(h_umsatz._recid)


                    cost = cal_fbcost(h_umsatz.artnr, h_umsatz.departement, h_umsatz.datum)
                    w1.lytoday = w1.lytoday + cost

            w1.done = True

    def fill_sgfb(rec_w1:int, main_nr:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        datum2:date = None
        cost:decimal = 0
        sg_dept:int = 0
        subgr:int = 0
        vat:decimal = 0
        serv:decimal = 0
        fact:decimal = 0

            w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

            if w1.done:

                return
            sg_dept = to_int(substring(w1.s_artnr, 0, 2))
            subgr = to_int(substring(w1.s_artnr, 2))

            wgrpdep = db_session.query(Wgrpdep).filter(
                    (Wgrpdep.zknr == subgr) &  (Wgrpdep.departement == sg_dept)).first()

            if not wgrpdep:
                msg_str = msg_str + chr(2) + translateExtended ("SubGroup not found : ", lvcarea, "") + w1.varname
                error_nr = -1

                return

            if ytd_flag:
                datum1 = jan1
            else:
                datum1 = from_date

            h_umsatz_obj_list = []
            for h_umsatz, h_artikel in db_session.query(H_umsatz, H_artikel).join(H_artikel,(H_artikel.artnr == H_umsatz.artnr) &  (H_artikel.departement == H_umsatz.departement) &  (H_artikel.zwkum == subgr) &  (H_artikel.artart == 0)).filter(
                    (H_umsatz.datum >= datum1) &  (H_umsatz.datum <= to_date) &  (H_umsatz.departement == sg_dept)).all():
                if h_umsatz._recid in h_umsatz_obj_list:
                    continue
                else:
                    h_umsatz_obj_list.append(h_umsatz._recid)


                serv, vat = get_output(calc_servvat(h_artikel.departement, h_artikel.artnr, datum, h_artikel.service_code, h_artikel.mwst_code))
                fact = (1.00 + serv + vat)

                if h_umsatz.datum == to_date:

                    if main_nr == 9985:
                        w1.tday = w1.tday + h_umsatz.betrag / fact

                    elif main_nr == 9986:
                        w1.tday = w1.tday + h_umsatz.anzahl

                if get_month(h_umsatz.datum) == get_month(to_date):

                    if main_nr == 9985:
                        w1.saldo = w1.saldo + h_umsatz.betrag / fact

                    elif main_nr == 9986:
                        w1.saldo = w1.saldo + h_umsatz.anzahl

                if ytd_flag:

                    if main_nr == 9985:
                        w1.ytd_saldo = w1.ytd_saldo + h_umsatz.betrag / fact

                    elif main_nr == 9986:
                        w1.ytd_saldo = w1.ytd_saldo + h_umsatz.anzahl

            if lytd_flag or lmtd_flag:

                if lytd_flag:
                    datum1 = ljan1
                else:
                    datum1 = lfrom_date

                h_umsatz_obj_list = []
                for h_umsatz, h_artikel in db_session.query(H_umsatz, H_artikel).join(H_artikel,(H_artikel.artnr == H_umsatz.artnr) &  (H_artikel.departement == H_umsatz.departement) &  (H_artikel.zwkum == subgr) &  (H_artikel.artart == 0)).filter(
                        (H_umsatz.datum >= datum1) &  (H_umsatz.datum <= lto_date) &  (H_umsatz.departement == sg_dept)).all():
                    if h_umsatz._recid in h_umsatz_obj_list:
                        continue
                    else:
                        h_umsatz_obj_list.append(h_umsatz._recid)


                    cost = cal_fbcost(h_umsatz.artnr, h_umsatz.departement, h_umsatz.datum)

                    if h_umsatz.datum < lfrom_date:
                        w1.lytd_saldo = w1.lytd_saldo + cost
                    else:
                        w1.lastyr = w1.lastyr + cost

                        if lytd_flag:
                            w1.lytd_saldo = w1.lytd_saldo + cost

            if pmtd_flag:

                h_umsatz_obj_list = []
                for h_umsatz, h_artikel in db_session.query(H_umsatz, H_artikel).join(H_artikel,(H_artikel.artnr == H_umsatz.artnr) &  (H_artikel.departement == H_umsatz.departement) &  (H_artikel.zwkum == subgr) &  (H_artikel.artart == 0)).filter(
                        (H_umsatz.datum >= pfrom_date) &  (H_umsatz.datum <= pto_date) &  (H_umsatz.departement == sg_dept)).all():
                    if h_umsatz._recid in h_umsatz_obj_list:
                        continue
                    else:
                        h_umsatz_obj_list.append(h_umsatz._recid)


                    cost = cal_fbcost(h_umsatz.artnr, h_umsatz.departement, h_umsatz.datum)
                    w1.lastmon = w1.lastmon + cost


            if lytoday_flag:

                h_umsatz_obj_list = []
                for h_umsatz, h_artikel in db_session.query(H_umsatz, H_artikel).join(H_artikel,(H_artikel.artnr == H_umsatz.artnr) &  (H_artikel.departement == H_umsatz.departement) &  (H_artikel.zwkum == subgr) &  (H_artikel.artart == 0)).filter(
                        (H_umsatz.datum >= lytoday) &  (H_umsatz.departement == sg_dept)).all():
                    if h_umsatz._recid in h_umsatz_obj_list:
                        continue
                    else:
                        h_umsatz_obj_list.append(h_umsatz._recid)


                    cost = cal_fbcost(h_umsatz.artnr, h_umsatz.departement, h_umsatz.datum)
                    w1.lytoday = w1.lytoday + cost

            w1.done = True

    def fill_quantity(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        datum2:date = None
        curr_date:date = None
        d_flag:bool = False
        dlmtd_flag:bool = False

            w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

            if w1.done:

                return

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == w1.artnr) &  (Artikel.departement == w1.dept)).first()

            if not artikel:
                msg_str = msg_str + chr(2) + translateExtended ("No such article number : ", lvcarea, "") + to_string(w1.artnr) + " " + translateExtended ("dept", lvcarea, "") + " " + to_string(w1.dept)

                return

            if (get_day(to_date) == 31 and get_month(to_date) != 8 and get_month(to_date) != 1) or (get_day(to_date) == 30 and get_month(to_date) == 3) or (get_day(date_mdy(3, 1, get_year(to_date)) - 1) == 28 and get_month(to_date) == 3 and get_day(to_date) == 29):
                w1.lm_today = 0
            else:

                if get_month(to_date) == 1:
                    curr_date = date_mdy(12, get_day(to_date) , get_year(to_date) - 1)
                else:
                    curr_date = date_mdy(get_month(to_date) - 1, get_day(to_date) , get_year(to_date))

                umsatz = db_session.query(Umsatz).filter(
                        (Umsatz.datum == curr_date) &  (Umsatz.artnr == w1.artnr) &  (Umsatz.departement == w1.dept)).first()

                if umsatz:
                    w1.lm_today = umsatz.anzahl

            if ytd_flag:
                datum1 = jan1
            else:
                datum1 = from_date

            for umsatz in db_session.query(Umsatz).filter(
                    (Umsatz.datum >= datum1) &  (Umsatz.datum <= to_date) &  (Umsatz.artnr == w1.artnr) &  (Umsatz.departement == w1.dept)).all():
                d_flag = (get_month(umsatz.datum) == get_month(to_date)) and (get_year(umsatz.datum) == get_year(to_date))

                if umsatz.datum == to_date - 1:
                    w1.yesterday = w1.yesterday + umsatz.anzahl

                if umsatz.datum == to_date:
                    w1.tday = w1.tday + umsatz.anzahl

                if umsatz.datum < from_date:
                    w1.ytd_saldo = w1.ytd_saldo + umsatz.anzahl
                else:
                    w1.saldo = w1.saldo + umsatz.anzahl

                    if ytd_flag:
                        w1.ytd_saldo = w1.ytd_saldo + umsatz.anzahl

                    if d_flag:
                        w1.mon_saldo[get_day(umsatz.datum) - 1] = w1.mon_saldo[get_day(umsatz.datum) - 1] + umsatz.anzahl

            if lytd_flag or lmtd_flag:

                if lytd_flag:
                    datum2 = ljan1
                else:
                    datum2 = lfrom_date

                for umsatz in db_session.query(Umsatz).filter(
                        (Umsatz.datum >= datum2) &  (Umsatz.datum <= lto_date) &  (Umsatz.artnr == w1.artnr) &  (Umsatz.departement == w1.dept)).all():

                    if umsatz.datum < lfrom_date:
                        w1.lytd_saldo = w1.lytd_saldo + umsatz.anzahl
                    else:
                        dlmtd_flag = (get_month(umsatz.datum) == get_month(to_date)) and (get_year(umsatz.datum) == get_year(to_date) - 1)

                        if dlmtd_flag:
                            w1.mon_lmtd[get_day(umsatz.datum) - 1] = w1.mon_lmtd[get_day(umsatz.datum) - 1] + umsatz.anzahl
                        w1.lastyr = w1.lastyr + umsatz.anzahl

                        if lytd_flag:
                            w1.lytd_saldo = w1.lytd_saldo + umsatz.anzahl

            if pmtd_flag:

                for umsatz in db_session.query(Umsatz).filter(
                        (Umsatz.datum >= pfrom_date) &  (Umsatz.datum <= pto_date) &  (Umsatz.artnr == w1.artnr) &  (Umsatz.departement == w1.dept)).all():
                    w1.lastmon = w1.lastmon + umsatz.anzahl


            if lytoday_flag:

                umsatz = db_session.query(Umsatz).filter(
                        (Umsatz.datum == lytoday) &  (Umsatz.artnr == w1.artnr) &  (Umsatz.departement == w1.dept)).first()

                if umsatz:
                    w1.lastmon = w1.lastmon + umsatz.anzahl
            w1.done = True

    def fill_revenue(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        curr_date:date = None
        datum1:date = None
        serv:decimal = 0
        vat:decimal = 0
        fact:decimal = 0
        n_betrag:decimal = 0
        n_serv:decimal = 0
        n_tax:decimal = 0
        ly_betrag:decimal = 0
        d_flag:bool = False
        dbudget_flag:bool = False
        dlmtd_flag:bool = False
        yes_serv:decimal = 0
        yes_vat:decimal = 0
        yes_fact:decimal = 0
        yes_betrag:decimal = 0
        st_date:int = 0
            Ubuff = Umsatz
            Buff_umsatz = Umsatz

            w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

            if w1.done:

                return

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == w1.artnr) &  (Artikel.departement == w1.dept)).first()

            if not artikel:
                msg_str = msg_str + chr(2) + translateExtended ("No such article number : ", lvcarea, "") + to_string(w1.artnr) + " " + translateExtended ("dept", lvcarea, "") + " " + to_string(w1.dept)

                return

            if (get_day(to_date) == 31 and get_month(to_date) != 8 and get_month(to_date) != 1) or (get_day(to_date) == 30 and get_month(to_date) == 3) or (get_day(date_mdy(3, 1, get_year(to_date)) - 1) == 28 and get_month(to_date) == 3 and get_day(to_date) == 29):
                st_date = 1
                curr_date = date_mdy(get_month(to_date) , 1, get_year(to_date)) - 1
                w1.lm_today = 0
            else:
                st_date = 2

                if get_month(to_date) == 1:
                    curr_date = date_mdy(12, get_day(to_date) , get_year(to_date) - 1)
                else:
                    curr_date = date_mdy(get_month(to_date) - 1, get_day(to_date) , get_year(to_date))

            for buff_umsatz in db_session.query(Buff_umsatz).filter(
                    (Buff_umsatz.datum >= date_mdy(get_month(curr_date) , 1, get_year(curr_date))) &  (Buff_umsatz.datum <= curr_date) &  (Buff_umsatz.artnr == w1.artnr) &  (Buff_umsatz.departement == w1.dept)).all():
                serv, vat = get_output(calc_servvat(buff_umsatz.departement, buff_umsatz.artnr, buff_umsatz.datum, artikel.service_code, artikel.mwst_code))
                fact = 1.00 + serv + vat
                n_betrag = 0

                if foreign_flag:
                    find_exrate(curr_date)

                    if exrate:
                        frate = exrate.betrag
                n_betrag = buff_umsatz.betrag / (fact * frate)
                n_serv = n_betrag * serv
                n_tax = n_betrag * vat

                if buff_umsatz.datum == curr_date and st_date == 2:
                    w1.lm_today = w1.lm_today + n_betrag
                    w1.lm_today_serv = w1.lm_today_serv + n_serv
                    w1.lm_today_tax = w1.lm_today_tax + n_tax


                w1.lm_mtd = w1.lm_mtd + n_betrag

            if ytd_flag:
                datum1 = jan1
            else:
                datum1 = from_date
            for curr_date in range(datum1,to_date + 1) :
                serv = 0
                vat = 0

                umsatz = db_session.query(Umsatz).filter(
                        (Umsatz.datum == curr_date) &  (Umsatz.artnr == w1.artnr) &  (Umsatz.departement == w1.dept)).first()

                if umsatz:
                    serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                fact = 1.00 + serv + vat
                d_flag = None != umsatz and (get_month(umsatz.datum) == get_month(to_date)) and (get_year(umsatz.datum) == get_year(to_date))
                n_betrag = 0

                if umsatz:

                    if foreign_flag:
                        find_exrate(curr_date)

                        if exrate:
                            frate = exrate.betrag
                    n_betrag = umsatz.betrag / (fact * frate)
                    n_serv = n_betrag * serv
                    n_tax = n_betrag * vat

                if budget_flag:

                    budget = db_session.query(Budget).filter(
                            (Budget.artnr == w1.artnr) &  (Budget.departement == w1.dept) &  (Budget.datum == curr_date)).first()
                dbudget_flag = None != budget and (get_month(budget.datum) == get_month(to_date)) and (get_year(budget.datum) == get_year(to_date))

                if dbudget_flag:
                    w1.mon_budget[get_day(budget.datum) - 1] = w1.mon_budget[get_day(budget.datum) - 1] + budget.betrag
                ly_betrag = 0

                if curr_date == to_date:
                    serv = 0
                    vat = 0

                    if umsatz:
                        w1.tday = w1.tday + n_betrag
                        w1.tday_serv = w1.tday_serv + n_serv
                        w1.tday_tax = w1.tday_tax + n_tax

                    if budget:
                        w1.tbudget = w1.tbudget + budget.betrag

                if curr_date == to_date:

                    buff_umsatz = db_session.query(Buff_umsatz).filter(
                            (Buff_umsatz.datum == curr_date - 1) &  (Buff_umsatz.artnr == w1.artnr) &  (Buff_umsatz.departement == w1.dept)).first()

                    if buff_umsatz:
                        yes_serv, yes_vat = get_output(calc_servvat(buff_umsatz.departement, buff_umsatz.artnr, buff_umsatz.datum, artikel.service_code, artikel.mwst_code))
                        yes_fact = 1.00 + yes_serv + yes_vat
                        yes_betrag = 0

                        if foreign_flag:
                            find_exrate(curr_date - 1)

                            if exrate:
                                frate = exrate.betrag
                        yes_betrag = buff_umsatz.betrag / (yes_fact * frate)
                        w1.yesterday = w1.yesterday + yes_betrag

                if curr_date <= to_date:

                    if umsatz:
                        w1.ytd_serv = w1.ytd_serv + n_serv
                        w1.ytd_tax = w1.ytd_tax + n_tax

                if d_flag:
                    w1.mtd_serv = w1.mtd_serv + n_serv
                    w1.mtd_tax = w1.mtd_tax + n_tax

                if curr_date < from_date:

                    if umsatz:
                        w1.ytd_saldo = w1.ytd_saldo + n_betrag

                    if budget:
                        w1.ytd_budget = w1.ytd_budget + budget.betrag
                else:

                    if umsatz:
                        w1.saldo = w1.saldo + n_betrag

                        if ytd_flag:
                            w1.ytd_saldo = w1.ytd_saldo + n_betrag

                        if d_flag:
                            w1.mon_saldo[get_day(umsatz.datum) - 1] = w1.mon_saldo[get_day(umsatz.datum) - 1] + n_betrag

                    if budget:
                        w1.budget = w1.budget + budget.betrag

                        if ytd_flag:
                            w1.ytd_budget = w1.ytd_budget + budget.betrag

            if lytd_flag or lmtd_flag:

                if lytd_flag:
                    datum1 = ljan1
                else:
                    datum1 = lfrom_date
                for curr_date in range(datum1,lto_date + 1) :
                    serv = 0
                    vat = 0

                    umsatz = db_session.query(Umsatz).filter(
                            (Umsatz.datum == curr_date) &  (Umsatz.artnr == w1.artnr) &  (Umsatz.departement == w1.dept)).first()

                    if umsatz:
                        serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                    fact = 1.00 + serv + vat
                    n_betrag = 0

                    if umsatz:

                        if foreign_flag:
                            find_exrate(curr_date)

                            if exrate:
                                frate = exrate.betrag
                        n_betrag = umsatz.betrag / (fact * frate)
                        n_serv = n_betrag * serv
                        n_tax = n_betrag * vat

                    if budget_flag:

                        budget = db_session.query(Budget).filter(
                                (Budget.artnr == w1.artnr) &  (Budget.departement == w1.dept) &  (Budget.datum == curr_date)).first()

                    if curr_date < lfrom_date:

                        if umsatz:
                            w1.lytd_saldo = w1.lytd_saldo + n_betrag

                        if budget:
                            w1.lytd_budget = w1.lytd_budget + budget.betrag
                    else:

                        if umsatz:
                            dlmtd_flag = None != umsatz and (get_month(umsatz.datum) == get_month(to_date)) and (get_year(umsatz.datum) == get_year(to_date) - 1)

                            if dlmtd_flag:
                                w1.mon_lmtd[get_day(umsatz.datum) - 1] = w1.mon_lmtd[get_day(umsatz.datum) - 1] + n_betrag
                            w1.lastyr = w1.lastyr + n_betrag
                            w1.lmtd_serv = w1.lmtd_serv + n_serv
                            w1.lmtd_tax = w1.lmtd_tax + n_tax

                            if lytd_flag:
                                w1.lytd_saldo = w1.lytd_saldo + n_betrag

                        if budget:
                            w1.ly_budget = w1.ly_budget + budget.betrag

                            if lytd_flag:
                                w1.lytd_budget = w1.lytd_budget + budget.betrag

            if pmtd_flag:
                for curr_date in range(pfrom_date,pto_date + 1) :
                    serv = 0
                    vat = 0

                    umsatz = db_session.query(Umsatz).filter(
                            (Umsatz.datum == curr_date) &  (Umsatz.artnr == w1.artnr) &  (Umsatz.departement == w1.dept)).first()

                    if umsatz:
                        serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                    fact = 1.00 + serv + vat
                    n_betrag = 0

                    if umsatz:

                        if foreign_flag:
                            find_exrate(curr_date)

                            if exrate:
                                frate = exrate.betrag
                        n_betrag = umsatz.betrag / (fact * frate)
                        n_serv = n_betrag * serv
                        n_tax = n_betrag * vat

                    if budget_flag:

                        budget = db_session.query(Budget).filter(
                                (Budget.artnr == w1.artnr) &  (Budget.departement == w1.dept) &  (Budget.datum == curr_date)).first()

                    if umsatz:
                        w1.lastmon = w1.lastmon + n_betrag
                        w1.pmtd_serv = w1.pmtd_serv + n_serv
                        w1.pmtd_tax = w1.pmtd_tax + n_tax

                    if budget:
                        w1.lm_budget = w1.lm_budget + budget.betrag

            if lytoday_flag:
                for curr_date in range(lytoday,lytoday + 1) :
                    serv = 0
                    vat = 0

                    umsatz = db_session.query(Umsatz).filter(
                            (Umsatz.datum == curr_date) &  (Umsatz.artnr == w1.artnr) &  (Umsatz.departement == w1.dept)).first()

                    if umsatz:
                        serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                    fact = 1.00 + serv + vat
                    n_betrag = 0

                    if umsatz:

                        if foreign_flag:
                            find_exrate(curr_date)

                            if exrate:
                                frate = exrate.betrag
                        n_betrag = umsatz.betrag / (fact * frate)

                    if budget_flag:

                        budget = db_session.query(Budget).filter(
                                (Budget.artnr == w1.artnr) &  (Budget.departement == w1.dept) &  (Budget.datum == curr_date)).first()

                    if umsatz:
                        w1.lytoday = w1.lytoday + n_betrag
            w1.done = True

    def fill_persocc(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        datum2:date = None
        curr_date:date = None
        ly_currdate:date = None
        d_flag:bool = False
        dbudget_flag:bool = False
        dlmtd_flag:bool = False
        frate1:decimal = 0
            W11 = W1
            W753 = W1
            W754 = W1
            W755 = W1

            w11 = query(w11_list, filters=(lambda w11 :w11.main_code == 806), first=True)

            if w11 and w11.done:


                w753 = query(w753_list, filters=(lambda w753 :w753.main_code == 753 and not w753.done), first=True)

            w754 = query(w754_list, filters=(lambda w754 :w754.main_code == 754 and not w754.done), first=True)

            w755 = query(w755_list, filters=(lambda w755 :w755.main_code == 755 and not w755.done), first=True)

            w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

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

            for segment in db_session.query(Segment).all():

                if (get_day(to_date) == 31 and get_month(to_date) != 8 and get_month(to_date) != 1) or (get_day(to_date) == 30 and get_month(to_date) == 3) or (get_day(date_mdy(3, 1, get_year(to_date)) - 1) == 28 and get_month(to_date) == 3 and get_day(to_date) == 29):

                    if w1:
                        w1.lm_today = 0

                    if w753:
                        w753.lm_today = 0

                    if w11:
                        w11.lm_today = 0
                else:

                    if get_month(to_date) == 1:
                        curr_date = date_mdy(12, get_day(to_date) , get_year(to_date) - 1)
                    else:
                        curr_date = date_mdy(get_month(to_date) - 1, get_day(to_date) , get_year(to_date))

                    segmentstat = db_session.query(Segmentstat).filter(
                            (Segmentstat.datum == curr_date) &  (Segmentstat.segmentcode == segmentcode)).first()

                    if segmentstat:
                        frate = 1

                        if foreign_flag:
                            find_exrate(segmentstat.datum)

                            if exrate:
                                frate = exrate.betrag
                        w1.lm_today = w1.lm_today + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis

                        if w753:
                            w753.lm_today = w753.lm_today + segmentstat.persanz

                        if w11:
                            w11.lm_today = w11.lm_today + segmentstat.zimmeranz

                for segmentstat in db_session.query(Segmentstat).filter(
                        (Segmentstat.datum >= datum1) &  (Segmentstat.datum <= to_date) &  (Segmentstat.segmentcode == segmentcode)).all():
                    frate = 1

                    if foreign_flag:
                        find_exrate(segmentstat.datum)

                        if exrate:
                            frate = exrate.betrag
                    d_flag = (get_month(segmentstat.datum) == get_month(to_date)) and (get_year(segmentstat.datum) == get_year(to_date))
                    dbudget_flag = (get_month(segmentstat.datum) == get_month(to_date)) and (get_year(segmentstat.datum) == get_year(to_date))

                    if segmentstat.datum == to_date - 1:
                        w1.yesterday = w1.yesterday + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis

                        if w753:
                            w753.yesterday = w753.yesterday + segmentstat.persanz

                        if w11:
                            w11.yesterday = w11.yesterday + segmentstat.zimmeranz

                    if segmentstat.datum == to_date:


                        if lytd_flag and segmentstat.datum == to_date:

                            if get_month(to_date) == 2 and get_day(to_date) == 29:
                                1
                            else:
                                ly_currdate = date_mdy(get_month(to_date) , get_day(to_date) , get_year(to_date) - 1)

                                segmbuff = db_session.query(Segmbuff).filter(
                                        (Segmbuff.datum == ly_currdate) &  (Segmbuff.segmentcode == segmentcode)).first()
                        w1.tday = w1.tday + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
                        w1.tbudget = w1.tbudget + segmentstat.budpersanz

                        if w11:
                            w11.tday = w11.tday + segmentstat.zimmeranz
                            w11.tbudget = w11.tbudget + segmentstat.budzimmeranz

                        if w753:
                            w753.tday = w753.tday + segmentstat.persanz

                        if w754:
                            w754.tday = w754.tday + segmentstat.kind1

                        if w755:
                            w755.tday = w755.tday + segmentstat.kind2

                    if segmentstat.datum <= lfr_date:
                        w1.lm_ytd = w1.lm_ytd + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis

                        if w11:
                            w11.lm_ytd = w11.lm_ytd + segmentstat.zimmeranz

                        if w753:
                            w753.lm_ytd = w753.lm_ytd + segmentstat.persanz

                        if w754:
                            w754.lm_ytd = w754.lm_ytd + segmentstat.kind1

                        if w755:
                            w755.lm_ytd = w755.lm_ytd + segmentstat.kind2

                    if segmentstat.datum < from_date:
                        w1.ytd_saldo = w1.ytd_saldo + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
                        w1.ytd_budget = w1.ytd_budget + segmentstat.budpersanz

                        if w11:
                            w11.ytd_saldo = w11.ytd_saldo + segmentstat.zimmeranz
                            w11.ytd_budget = w11.ytd_budget + segmentstat.budzimmeranz

                        if w753:
                            w753.ytd_saldo = w753.ytd_saldo + segmentstat.persanz

                        if w754:
                            w754.ytd_saldo = w754.ytd_saldo + segmentstat.kind1

                        if w755:
                            w755.ytd_saldo = w755.ytd_saldo + segmentstat.kind2
                    else:
                        w1.saldo = w1.saldo + segmentstat.persanz +\
                                segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
                        w1.budget = w1.budget + segmentstat.budpersanz

                        if d_flag:
                            w1.mon_saldo[get_day(segmentstat.datum) - 1] = w1.mon_saldo[get_day(segmentstat.datum) - 1]+ segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis

                        if dbudget_flag:
                            w1.mon_budget[get_day(segmentstat.datum) - 1] = w1.mon_budget[get_day(segmentstat.datum) - 1]+ segmentstat.budpersanz

                        if w11:
                            w11.saldo = w11.saldo + segmentstat.zimmeranz
                            w11.budget = w11.budget + segmentstat.budzimmeranz

                            if d_flag:
                                w11.mon_saldo[get_day(segmentstat.datum) - 1] = w11.mon_saldo[get_day(segmentstat.datum) - 1] + segmentstat.zimmeranz

                            if dbudget_flag:
                                w11.mon_budget[get_day(segmentstat.datum) - 1] = w11.mon_budget[get_day(segmentstat.datum) - 1]+ segmentstat.budzimmeranz

                        if w753:
                            w753.saldo = w753.saldo + segmentstat.persanz

                            if d_flag:
                                w753.mon_saldo[get_day(segmentstat.datum) - 1] = w753.mon_saldo[get_day(segmentstat.datum) - 1] + segmentstat.persanz

                        if w754:
                            w754.saldo = w754.saldo + segmentstat.kind1

                            if d_flag:
                                w754.mon_saldo[get_day(segmentstat.datum) - 1] = w754.mon_saldo[get_day(segmentstat.datum) - 1] + segmentstat.kind1

                        if w755:
                            w755.saldo = w755.saldo + segmentstat.kind2

                            if d_flag:
                                w755.mon_saldo[get_day(segmentstat.datum) - 1] = w755.mon_saldo[get_day(segmentstat.datum) - 1] + segmentstat.kind2

                        if ytd_flag:
                            w1.ytd_saldo = w1.ytd_saldo + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
                            w1.ytd_budget = w1.ytd_budget + segmentstat.budpersanz

                            if w11:
                                w11.ytd_saldo = w11.ytd_saldo + segmentstat.zimmeranz
                                w11.ytd_budget = w11.ytd_budget + segmentstat.budzimmeranz

                            if w753:
                                w753.ytd_saldo = w753.ytd_saldo + segmentstat.persanz

                            if w754:
                                w754.ytd_saldo = w754.ytd_saldo + segmentstat.kind1

                            if w755:
                                w755.ytd_saldo = w755.ytd_saldo + segmentstat.kind2

                if lytd_flag or lmtd_flag:

                    for segmentstat in db_session.query(Segmentstat).filter(
                            (Segmentstat.datum >= datum2) &  (Segmentstat.datum <= lto_date) &  (Segmentstat.segmentcode == segmentcode)).all():

                        if foreign_flag:
                            find_exrate(segmentstat.datum)

                            if exrate:
                                frate = exrate.betrag

                        if segmentstat.datum < lfrom_date:
                            w1.lytd_saldo = w1.lytd_saldo + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
                            w1.lytd_budget = w1.lytd_budget + segmentstat.budpersanz

                            if w11:
                                w11.lytd_saldo = w11.lytd_saldo + segmentstat.zimmeranz
                                w11.lytd_budget = w11.lytd_budget + segmentstat.budzimmeranz

                            if w753:
                                w753.lytd_saldo = w753.lytd_saldo + segmentstat.persanz

                            if w754:
                                w754.lytd_saldo = w754.lytd_saldo + segmentstat.kind1

                            if w755:
                                w755.lytd_saldo = w755.lytd_saldo + segmentstat.kind2
                        else:
                            dlmtd_flag = (get_month(segmentstat.datum) == get_month(to_date)) and (get_year(segmentstat.datum) == get_year(to_date) - 1)

                            if dlmtd_flag:
                                w1.mon_lmtd[get_day(segmentstat.datum) - 1] = w1.mon_lmtd[get_day(segmentstat.datum) - 1] + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
                            w1.lastyr = w1.lastyr + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
                            w1.ly_budget = w1.ly_budget + segmentstat.budpersanz

                            if w11:

                                if dlmtd_flag:
                                    w11.mon_lmtd[get_day(segmentstat.datum) - 1] = w11.mon_lmtd[get_day(segmentstat.datum) - 1] + segmentstat.zimmeranz
                                w11.lastyr = w11.lastyr + segmentstat.zimmeranz
                                w11.ly_budget = w11.ly_budget + segmentstat.budzimmeranz

                            if w753:

                                if dlmtd_flag:
                                    w753.mon_lmtd[get_day(segmentstat.datum) - 1] = w753.mon_lmtd[get_day(segmentstat.datum) - 1] + segmentstat.persanz
                                w753.lastyr = w753.lastyr + segmentstat.persanz

                            if w754:

                                if dlmtd_flag:
                                    w754.mon_lmtd[get_day(segmentstat.datum) - 1] = w754.mon_lmtd[get_day(segmentstat.datum) - 1] + segmentstat.kind1
                                w754.lastyr = w754.lastyr + segmentstat.kind1

                            if w755:

                                if dlmtd_flag:
                                    w755.mon_lmtd[get_day(segmentstat.datum) - 1] = w755.mon_lmtd[get_day(segmentstat.datum) - 1] + segmentstat.kind2
                                w755.lastyr = w755.lastyr + segmentstat.kind2

                            if lytd_flag:
                                w1.lytd_saldo = w1.lytd_saldo + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
                                w1.lytd_budget = w1.lytd_budget + segmentstat.budpersanz

                                if w11:
                                    w11.lytd_saldo = w11.lytd_saldo + segmentstat.zimmeranz
                                    w11.lytd_budget = w11.lytd_budget + segmentstat.budzimmeranz

                                if w753:
                                    w753.lytd_saldo = w753.lytd_saldo + segmentstat.persanz

                                if w754:
                                    w754.lytd_saldo = w754.lytd_saldo + segmentstat.kind1

                                if w755:
                                    w755.lytd_saldo = w755.lytd_saldo + segmentstat.kind2

                if pmtd_flag:

                    for segmentstat in db_session.query(Segmentstat).filter(
                            (Segmentstat.datum >= pfrom_date) &  (Segmentstat.datum <= pto_date) &  (Segmentstat.segmentcode == segmentcode)).all():

                        if foreign_flag:
                            find_exrate(segmentstat.datum)

                            if exrate:
                                frate = exrate.betrag
                        w1.lastmon = w1.lastmon + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
                        w1.lm_budget = w1.lm_budget + segmentstat.budpersanz

                        if w11:
                            w11.lastmon = w11.lastmon + segmentstat.zimmeranz
                            w11.lm_budget = w11.lm_budget + segmentstat.budzimmeranz

                        if w753:
                            w753.lastmon = w753.lastmon + segmentstat.persanz

                        if w754:
                            w754.lastmon = w754.lastmon + segmentstat.kind1

                        if w755:
                            w755.lastmon = w755.lastmon + segmentstat.kind2


                if lytoday_flag:

                    segmentstat = db_session.query(Segmentstat).filter(
                            (Segmentstat.datum == lytoday) &  (Segmentstat.segmentcode == segmentcode)).first()

                    if segmentstat:

                        if foreign_flag:
                            find_exrate(segmentstat.datum)

                            if exrate:
                                frate = exrate.betrag
                        w1.lytoday = w1.lytoday + segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis

                        if w11:
                            w11.lytoday = w11.lytoday + segmentstat.zimmeranz

                        if w753:
                            w753.lytoday = w753.lytoday + segmentstat.persanz

                        if w754:
                            w754.lytoday = w754.lytoday + segmentstat.kind1

                        if w755:
                            w755.lytoday = w755.lytoday + segmentstat.kind2
            w1.done = True

            if w11:
                w11.done = True

            if w753:
                w753.done = True

            if w754:
                w754.done = True

            if w755:
                w755.done = True

    def fill_nation(rec_w1:int, rec_w1:int, rec_w1:int, rec_w1:int, main_nr:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        datum1:date = None
        datum1:date = None
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
        frate1:decimal = 0
            W11 = W1

            w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

            if w1.done:

                return

            w11 = query(w11_list, filters=(lambda w11 :w11.main_code == 842), first=True)

            if w11 and w11.done:


                if ytd_flag:
                    datum1 = jan1
                else:
                    datum1 = from_date

                for zinrstat in db_session.query(Zinrstat).filter(
                            (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= to_date) &  (func.lower(Zinrstat.zinr) == "avrgrate")).all():

                    if zinrstat.datum == to_date:
                        w1.tday = w1.tday + zinrstat.argtumsatz

                        if w11:
                            w11.tday = w11.tday + zinrstat.logisumsatz / zinrstat.zimmeranz

                    if zinrstat.datum < from_date:
                        w1.ytd_saldo = w1.ytd_saldo + zinrstat.argtumsatz / zinrstat.zimmeranz

                        if w11:
                            w11.ytd_saldo = w11.ytd_saldo + zinrstat.logisumsatz / zinrstat.zimmeranz
                    else:
                        w1.saldo = w1.saldo + zinrstat.argtumsatz / zinrstat.zimmeranz

                        if ytd_flag:
                            w1.ytd_saldo = w1.ytd_saldo + zinrstat.argtumsatz / zinrstat.zimmeranz

                        if w11:
                            w11.saldo = w11.saldo + zinrstat.logisumsatz / zinrstat.zimmeranz

                            if ytd_flag:
                                w11.ytd_saldo = w11.ytd_saldo + zinrstat.logisumsatz / zinrstat.zimmeranz

                if lytd_flag or lmtd_flag:

                    if lytd_flag:
                        datum1 = ljan1
                    else:
                        datum1 = lfrom_date

                    for zinrstat in db_session.query(Zinrstat).filter(
                                (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= lto_date) &  (func.lower(Zinrstat.zinr) == "avrgrate")).all():

                        if zinrstat.datum < lfrom_date:
                            w1.lytd_saldo = w1.lytd_saldo + zinrstat.argtumsatz / zinrstat.zimmeranz

                            if w11:
                                w11.lytd_saldo = w11.lytd_saldo + zinrstat.logisumsatz / zinrstat.zimmeranz
                        else:
                            w1.lastyr = w1.lastyr + zinrstat.argtumsatz / zinrstat.zimmeranz

                            if lytd_flag:
                                w1.lytd_saldo = w1.lytd_saldo + zinrstat.argtumsatz / zinrstat.zimmeranz

                            if w11:
                                w11.lastyr = w11.lastyr + zinrstat.logisumsatz / zinrstat.zimmeranz

                                if lytd_flag:
                                    w11.lytd_saldo = w11.lytd_saldo + zinrstat.logisumsatz / zinrstat.zimmeranz

                if pmtd_flag:

                    for zinrstat in db_session.query(Zinrstat).filter(
                                (Zinrstat.datum >= pfrom_date) &  (Zinrstat.datum <= pto_date) &  (func.lower(Zinrstat.zinr) == "avrgrate")).all():
                        w1.lastmon = w1.lastmon + zinrstat.argtumsatz / zinrstat.zimmeranz

                        if w11:
                            w11.lastmon = w11.lastmon + zinrstat.logisumsatz / zinrstat.zimmeranz


                if lytoday_flag:

                    zinrstat = db_session.query(Zinrstat).filter(
                                (Zinrstat.datum == lytoday) &  (func.lower(Zinrstat.zinr) == "avrgrate")).first()

                    if zinrstat:
                        w1.lytoday = zinrstat.argtumsatz / zinrstat.zimmeranz

                        if w11:
                            w11.lytoday = zinrstat.logisumsatz / zinrstat.zimmeranz
                w1.done = True

                if w11:
                    w11.done = True
                W11 = W1

                w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

                if w1.done:

                    return

                w11 = query(w11_list, filters=(lambda w11 :w11.main_code == 46), first=True)

                if w11 and w11.done:


                    if ytd_flag:
                        datum1 = jan1
                    else:
                        datum1 = from_date

                    for zinrstat in db_session.query(Zinrstat).filter(
                                (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= to_date) &  (func.lower(Zinrstat.zinr) == "avrgLrate")).all():

                        if zinrstat.datum == to_date:
                            w1.tday = w1.tday + zinrstat.argtumsatz

                            if w11:
                                w11.tday = w11.tday + zinrstat.logisumsatz / zinrstat.zimmeranz

                        if zinrstat.datum < from_date:
                            w1.ytd_saldo = w1.ytd_saldo + zinrstat.argtumsatz / zinrstat.zimmeranz

                            if w11:
                                w11.ytd_saldo = w11.ytd_saldo + zinrstat.logisumsatz / zinrstat.zimmeranz
                        else:
                            w1.saldo = w1.saldo + zinrstat.argtumsatz / zinrstat.zimmeranz

                            if ytd_flag:
                                w1.ytd_saldo = w1.ytd_saldo + zinrstat.argtumsatz / zinrstat.zimmeranz

                            if w11:
                                w11.saldo = w11.saldo + zinrstat.logisumsatz / zinrstat.zimmeranz

                                if ytd_flag:
                                    w11.ytd_saldo = w11.ytd_saldo + zinrstat.logisumsatz / zinrstat.zimmeranz

                    if lytd_flag or lmtd_flag:

                        if lytd_flag:
                            datum1 = ljan1
                        else:
                            datum1 = lfrom_date

                        for zinrstat in db_session.query(Zinrstat).filter(
                                    (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= lto_date) &  (func.lower(Zinrstat.zinr) == "avrgLrate")).all():

                            if zinrstat.datum < lfrom_date:
                                w1.lytd_saldo = w1.lytd_saldo + zinrstat.argtumsatz / zinrstat.zimmeranz

                                if w11:
                                    w11.lytd_saldo = w11.lytd_saldo + zinrstat.logisumsatz / zinrstat.zimmeranz
                            else:
                                w1.lastyr = w1.lastyr + zinrstat.argtumsatz / zinrstat.zimmeranz

                                if lytd_flag:
                                    w1.lytd_saldo = w1.lytd_saldo + zinrstat.argtumsatz / zinrstat.zimmeranz

                                if w11:
                                    w11.lastyr = w11.lastyr + zinrstat.logisumsatz / zinrstat.zimmeranz

                                    if lytd_flag:
                                        w11.lytd_saldo = w11.lytd_saldo + zinrstat.logisumsatz / zinrstat.zimmeranz

                    if pmtd_flag:

                        for zinrstat in db_session.query(Zinrstat).filter(
                                    (Zinrstat.datum >= pfrom_date) &  (Zinrstat.datum <= pto_date) &  (func.lower(Zinrstat.zinr) == "avrgLrate")).all():
                            w1.lastmon = w1.lastmon + zinrstat.argtumsatz / zinrstat.zimmeranz

                            if w11:
                                w11.lastmon = w11.lastmon + zinrstat.logisumsatz / zinrstat.zimmeranz


                    if lytoday_flag:

                        zinrstat = db_session.query(Zinrstat).filter(
                                    (Zinrstat.datum == lytoday) &  (func.lower(Zinrstat.zinr) == "avrgLrate")).first()

                        if zinrstat:
                            w1.lytoday = zinrstat.argtumsatz / zinrstat.zimmeranz

                            if w11:
                                w11.lytoday = zinrstat.logisumsatz / zinrstat.zimmeranz
                    w1.done = True

                    if w11:
                        w11.done = True
                    W11 = W1

                    w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

                    if w1.done:

                        return

                    w11 = query(w11_list, filters=(lambda w11 :w11.main_code == 811), first=True)

                    if w11 and w11.done:


                        if ytd_flag:
                            datum1 = jan1
                        else:
                            datum1 = from_date

                        for zinrstat in db_session.query(Zinrstat).filter(
                                    (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= to_date) &  (func.lower(Zinrstat.zinr) == "avrgrate")).all():

                            if zinrstat.datum == to_date:
                                w1.tday = w1.tday + zinrstat.logisumsatz

                                if w11:
                                    w11.tday = w11.tday + zinrstat.argtumsatz / zinrstat.zimmeranz

                            if zinrstat.datum < from_date:
                                w1.ytd_saldo = w1.ytd_saldo + zinrstat.logisumsatz / zinrstat.zimmeranz

                                if w11:
                                    w11.ytd_saldo = w11.ytd_saldo + zinrstat.argtumsatz / zinrstat.zimmeranz
                            else:
                                w1.saldo = w1.saldo + zinrstat.logisumsatz / zinrstat.zimmeranz

                                if ytd_flag:
                                    w1.ytd_saldo = w1.ytd_saldo + zinrstat.logisumsatz / zinrstat.zimmeranz

                                if w11:
                                    w11.saldo = w11.saldo + zinrstat.argtumsatz / zinrstat.zimmeranz

                                    if ytd_flag:
                                        w11.ytd_saldo = w11.ytd_saldo + zinrstat.argtumsatz / zinrstat.zimmeranz

                        if lytd_flag or lmtd_flag:

                            if lytd_flag:
                                datum1 = ljan1
                            else:
                                datum1 = lfrom_date

                            for zinrstat in db_session.query(Zinrstat).filter(
                                        (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= lto_date) &  (func.lower(Zinrstat.zinr) == "avrgrate")).all():

                                if zinrstat.datum < lfrom_date:
                                    w1.lytd_saldo = w1.lytd_saldo + zinrstat.logisumsatz / zinrstat.zimmeranz

                                    if w11:
                                        w11.lytd_saldo = w11.lytd_saldo + zinrstat.argtumsatz / zinrstat.zimmeranz
                                else:
                                    w1.lastyr = w1.lastyr + zinrstat.logisumsatz / zinrstat.zimmeranz

                                    if lytd_flag:
                                        w1.lytd_saldo = w1.lytd_saldo + zinrstat.logisumsatz / zinrstat.zimmeranz

                                    if w11:
                                        w11.lastyr = w11.lastyr + zinrstat.argtumsatz / zinrstat.zimmeranz

                                        if lytd_flag:
                                            w11.lytd_saldo = w11.lytd_saldo + zinrstat.argtumsatz / zinrstat.zimmeranz

                        if pmtd_flag:

                            for zinrstat in db_session.query(Zinrstat).filter(
                                        (Zinrstat.datum >= pfrom_date) &  (Zinrstat.datum <= pto_date) &  (func.lower(Zinrstat.zinr) == "avrgrate")).all():

                                if foreign_flag:
                                    find_exrate(zinrstat.datum)

                                    if exrate:
                                        frate = exrate.betrag
                                w1.lastmon = w1.lastmon + zinrstat.logisumsatz / zinrstat.zimmeranz

                                if w11:
                                    w11.lastmon = w11.lastmon + zinrstat.argtumsatz / zinrstat.zimmeranz


                        if lytoday_flag:

                            zinrstat = db_session.query(Zinrstat).filter(
                                        (Zinrstat.datum == lytoday) &  (func.lower(Zinrstat.zinr) == "avrgrate")).first()

                            if zinrstat:

                                if foreign_flag:
                                    find_exrate(zinrstat.datum)

                                    if exrate:
                                        frate = exrate.betrag
                                w1.lytoday = zinrstat.logisumsatz / zinrstat.zimmeranz

                                if w11:
                                    w11.lytoday = zinrstat.argtumsatz / zinrstat.zimmeranz
                        w1.done = True

                        if w11:
                            w11.done = True

                        w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)
                        natnr = w1.artnr

                        if ytd_flag:
                            datum1 = jan1
                        else:
                            datum1 = from_date
                        mm = get_month(to_date)

                        for genstat in db_session.query(Genstat).filter(
                                    (Genstat.resident == natnr) &  (Genstat.datum >= datum1) &  (Genstat.datum <= to_date) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.resident != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
                            frate = 1
                            d_flag = (get_month(genstat.datum) == get_month(to_date)) and (get_year(genstat.datum) == get_year(to_date))

                            if genstat.datum == to_date:

                                if main_nr == 8814:
                                    w1.tday = w1.tday + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                                if main_nr == 8813:
                                    w1.tday = w1.tday + 1

                                if main_nr == 8092:
                                    w1.tday = w1.tday + genstat.logis

                            if get_month(genstat.datum) == mm:

                                if main_nr == 8814:

                                    if d_flag:
                                        w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                                    w1.saldo = w1.saldo + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                                if main_nr == 8813:
                                    w1.saldo = w1.saldo + 1

                                    if d_flag:
                                        w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + 1

                                if main_nr == 8092:
                                    w1.saldo = w1.saldo + genstat.logis

                                    if d_flag:
                                        w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + genstat.logis

                            if main_nr == 8814:
                                w1.ytd_saldo = w1.ytd_saldo + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                            if main_nr == 8813:
                                w1.ytd_saldo = w1.ytd_saldo + 1

                            if main_nr == 8092:
                                w1.ytd_saldo = w1.ytd_saldo + genstat.logis

                        if lytd_flag or lmtd_flag:

                            if lytd_flag:
                                datum1 = ljan1
                            else:
                                datum1 = lfrom_date
                            mm = get_month(lto_date)

                            for genstat in db_session.query(Genstat).filter(
                                        (Genstat.resident == natnr) &  (Genstat.datum >= datum1) &  (Genstat.datum <= lto_date) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.resident != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
                                dlmtd_flag = (get_month(genstat.datum) == get_month(lto_date)) and (get_year(genstat.datum) == get_year(lto_date))

                                if genstat.datum == lto_date:

                                    if main_nr == 8814:
                                        w1.lytoday = w1.lytoday + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                                    if main_nr == 8813:
                                        w1.lytoday = w1.lytoday + 1

                                    if main_nr == 8092:
                                        w1.lytoday = w1.lytoday + genstat.logis

                                if get_month(genstat.datum) == mm:

                                    if main_nr == 8814:
                                        w1.lastyr = w1.lastyr + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                                    if main_nr == 8813:
                                        w1.lastyr = w1.lastyr + 1

                                    if main_nr == 8092:
                                        w1.lastyr = w1.lastyr + genstat.logis

                                if main_nr == 8814:
                                    w1.lytd_saldo = w1.lytd_saldo + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                                if main_nr == 8813:
                                    w1.lytd_saldo = w1.lytd_saldo + 1

                                if main_nr == 8092:
                                    w1.lytd_saldo = w1.lytd_saldo + genstat.logis

    def fill_competitor(rec_w1:int, main_nr:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

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
        frate1:decimal = 0

                        w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)
                        compnr = w1.artnr

                        if ytd_flag:
                            datum1 = jan1
                        else:
                            datum1 = from_date
                        mm = get_month(to_date)

                        for zinrstat in db_session.query(Zinrstat).filter(
                                    (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= to_date) &  (func.lower(Zinrstat.zinr) == "Competitor") &  (Zinrstat.betriebsnr == compnr)).all():
                            frate = 1
                            d_flag = (get_month(zinrstat.datum) == get_month(to_date)) and (get_year(zinrstat.datum) == get_year(to_date))

                            if zinrstat.datum == to_date:

                                if main_nr == 9981:
                                    w1.tday = w1.tday + zinrstat.zimmeranz

                                if main_nr == 9982:
                                    w1.tday = w1.tday + zinrstat.personen

                                if main_nr == 9983:
                                    w1.tday = w1.tday + to_int(zinrstat.argtumsatz)

                                if main_nr == 9984:
                                    w1.tday = w1.tday + zinrstat.logisumsatz

                            if get_month(zinrstat.datum) == mm:

                                if main_nr == 9981:
                                    w1.saldo = w1.saldo + zinrstat.zimmeranz

                                    if d_flag:
                                        w1.mon_saldo[get_day(zinrstat.datum) - 1] = w1.mon_saldo[get_day(zinrstat.datum) - 1] + zinrstat.zimmeranz

                                elif main_nr == 9982:
                                    w1.saldo = w1.saldo + zinrstat.personen

                                    if d_flag:
                                        w1.mon_saldo[get_day(zinrstat.datum) - 1] = w1.mon_saldo[get_day(zinrstat.datum) - 1] + zinrstat.personen

                                elif main_nr == 9983:
                                    w1.saldo = w1.saldo + to_int(zinrstat.argtumsatz)

                                    if d_flag:
                                        w1.mon_saldo[get_day(zinrstat.datum) - 1] = w1.mon_saldo[get_day(zinrstat.datum) - 1] + to_int(zinrstat.argtumsatz)

                                elif main_nr == 9984:
                                    w1.saldo = w1.saldo + zinrstat.logisumsatz

                                    if d_flag:
                                        w1.mon_saldo[get_day(zinrstat.datum) - 1] = w1.mon_saldo[get_day(zinrstat.datum) - 1] + zinrstat.logisumsatz

                            if main_nr == 9981:
                                w1.ytd_saldo = w1.ytd_saldo + zinrstat.zimmeranz

                            elif main_nr == 9982:
                                w1.ytd_saldo = w1.ytd_saldo + zinrstat.personen

                            elif main_nr == 9983:
                                w1.ytd_saldo = w1.ytd_saldo + to_int(zinrstat.argtumsatz)

                            elif main_nr == 9984:
                                w1.ytd_saldo = w1.ytd_saldo + zinrstat.logisumsatz

                        if lytd_flag or lmtd_flag:

                            if lytd_flag:
                                datum1 = ljan1
                            else:
                                datum1 = lfrom_date
                            mm = get_month(lto_date)

                            for zinrstat in db_session.query(Zinrstat).filter(
                                        (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= lto_date) &  (func.lower(Zinrstat.zinr) == "Competitor") &  (Zinrstat.betriebsnr == compnr)).all():
                                dlmtd_flag = (get_month(zinrstat.datum) == get_month(lto_date)) and (get_year(zinrstat.datum) == get_year(lto_date))

                                if zinrstat.datum == lto_date:

                                    if main_nr == 9981:
                                        w1.lytoday = w1.lytoday + zinrstat.zimmeranz

                                    if main_nr == 9982:
                                        w1.lytoday = w1.lytoday + zinrstat.personen

                                    if main_nr == 9983:
                                        w1.lytoday = w1.lytoday + to_int(zinrstat.argtumsatz)

                                    if main_nr == 9984:
                                        w1.lytoday = w1.lytoday + zinrstat.logisumsatz

                                if get_month(zinrstat.datum) == mm:

                                    if main_nr == 9981:
                                        w1.lastyr = w1.lastyr + zinrstat.zimmeranz

                                    if main_nr == 9982:
                                        w1.lastyr = w1.lastyr + zinrstat.personen

                                    if main_nr == 9983:
                                        w1.lastyr = w1.lastyr + to_int(zinrstat.argtumsatz)

                                    if main_nr == 9984:
                                        w1.lastyr = w1.lastyr + zinrstat.logisumsatz

                                if main_nr == 9981:
                                    w1.lytd_saldo = w1.lytd_saldo + zinrstat.zimmeranz

                                elif main_nr == 9982:
                                    w1.lytd_saldo = w1.lytd_saldo + zinrstat.personen

                                elif main_nr == 9983:
                                    w1.lytd_saldo = w1.lytd_saldo + to_int(zinrstat.argtumsatz)

                                elif main_nr == 9984:
                                    w1.lytd_saldo = w1.lytd_saldo + zinrstat.logisumsatz

    def fill_segment(rec_w1:int, main_nr:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

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
        frate1:decimal = 0
                        Segmbuffny = Segmentstat

                        if get_month(to_date) == 2 and get_day(to_date) == 29:
                            ny_currdate = date_mdy(get_month(to_date) , 28, get_year(to_date) + 1)
                        else:
                            ny_currdate = date_mdy(get_month(to_date) , get_day(to_date) , get_year(to_date) + 1)
                        njan1 = date_mdy(1, 1, get_year(to_date) + 1)
                        nmth1 = date_mdy(get_month(to_date) , 1, get_year(to_date) + 1)

                        w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)
                        segm = w1.artnr

                        segmbuffny = db_session.query(Segmbuffny).filter(
                                (Segmbuffny.datum == ny_currdate) &  (Segmbuffny.segmentcode == segm)).first()

                        if segmbuffny:

                            if main_nr == 92:
                                w1.ny_budget = segmbuffny.budlogis

                            if main_nr == 813:
                                w1.ny_budget = segmbuffny.budzimmeranz

                            if main_nr == 814:
                                w1.ny_budget = segmbuffny.budpersanz

                        for segmbuffny in db_session.query(Segmbuffny).filter(
                                (Segmbuffny.datum >= njan1) &  (Segmbuffny.datum <= ny_currdate) &  (Segmbuffny.segmentcode == segm)).all():

                            if main_nr == 92:
                                w1.nytd_budget = w1.nytd_budget + segmbuffny.budlogis

                            if main_nr == 813:
                                w1.nytd_budget = w1.nytd_budget + segmbuffny.budzimmeranz

                            if main_nr == 814:
                                w1.nytd_budget = w1.nytd_budget + segmbuffny.budpersanz

                        for segmbuffny in db_session.query(Segmbuffny).filter(
                                (Segmbuffny.datum >= nmth1) &  (Segmbuffny.datum <= ny_currdate) &  (Segmbuffny.segmentcode == segm)).all():

                            if main_nr == 92:
                                w1.nmtd_budget = w1.nmtd_budget + segmbuffny.budlogis

                            if main_nr == 813:
                                w1.nmtd_budget = w1.nmtd_budget + segmbuffny.budzimmeranz

                            if main_nr == 814:
                                w1.nmtd_budget = w1.nmtd_budget + segmbuffny.budpersanz

                        segmentstat = db_session.query(Segmentstat).filter(
                                (Segmentstat.datum == to_date - 1) &  (Segmentstat.segmentcode == segm)).first()

                        if segmentstat:
                            frate = 1

                            if foreign_flag:
                                find_exrate(segmentstat.datum)

                                if exrate:
                                    frate = exrate.betrag

                            if main_nr == 92:
                                w1.yesterday = segmentstat.logis / frate

                            elif main_nr == 813:
                                w1.yesterday = segmentstat.zimmeranz

                            elif main_nr == 814:
                                w1.yesterday = segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis

                        if (get_day(to_date) == 31 and get_month(to_date) != 8 and get_month(to_date) != 1) or (get_day(to_date) == 30 and get_month(to_date) == 3) or (get_day(date_mdy(3, 1, get_year(to_date)) - 1) == 28 and get_month(to_date) == 3 and get_day(to_date) == 29):
                            w1.lm_today = 0
                        else:

                            if get_month(to_date) == 1:
                                curr_date = date_mdy(12, get_day(to_date) , get_year(to_date) - 1)
                            else:
                                curr_date = date_mdy(get_month(to_date) - 1, get_day(to_date) , get_year(to_date))

                            segmentstat = db_session.query(Segmentstat).filter(
                                    (Segmentstat.datum == curr_date) &  (Segmentstat.segmentcode == segm)).first()

                            if segmentstat:
                                frate = 1

                                if foreign_flag:
                                    find_exrate(segmentstat.datum)

                                    if exrate:
                                        frate = exrate.betrag

                                if main_nr == 92:
                                    w1.lm_today = segmentstat.logis / frate

                                elif main_nr == 813:
                                    w1.lm_today = segmentstat.zimmeranz

                                elif main_nr == 814:
                                    w1.lm_today = segmentstat.persanz + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis

                        if ytd_flag:
                            datum1 = jan1
                        else:
                            datum1 = from_date
                        mm = get_month(to_date)

                        for genstat in db_session.query(Genstat).filter(
                                    (Genstat.segmentcode == segm) &  (Genstat.datum >= datum1) &  (Genstat.datum <= to_date) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
                            frate = 1

                            if foreign_flag:
                                find_exrate(genstat.datum)

                                if exrate:
                                    frate = exrate.betrag
                            d_flag = (get_month(genstat.datum) == get_month(to_date)) and (get_year(genstat.datum) == get_year(to_date))

                            if genstat.datum == to_date:

                                if main_nr == 814:
                                    w1.tday = w1.tday + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                                if main_nr == 813:
                                    w1.tday = w1.tday + 1

                                if main_nr == 92:
                                    w1.tday = w1.tday + genstat.logis

                                if main_nr == 756:
                                    w1.tday = w1.tday + genstat.erwachs

                                elif main_nr == 757:
                                    w1.tday = w1.tday + genstat.kind1

                                elif main_nr == 758:
                                    w1.tday = w1.tday + genstat.kind2

                            if get_month(genstat.datum) == mm:

                                if main_nr == 814:

                                    if d_flag:
                                        w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                                    w1.saldo = w1.saldo + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                                if main_nr == 813:
                                    w1.saldo = w1.saldo + 1

                                    if d_flag:
                                        w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + 1

                                if main_nr == 92:
                                    w1.saldo = w1.saldo + genstat.logis

                                    if d_flag:
                                        w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + genstat.logis

                                if main_nr == 756:

                                    if d_flag:
                                        w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + genstat.erwachs
                                    w1.saldo = w1.saldo + genstat.erwachs

                                elif main_nr == 757:

                                    if d_flag:
                                        w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + genstat.kind1
                                    w1.saldo = w1.saldo + genstat.kind1

                                elif main_nr == 758:

                                    if d_flag:
                                        w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + genstat.kind2
                                    w1.saldo = w1.saldo + genstat.kind2

                            if main_nr == 814:
                                w1.ytd_saldo = w1.ytd_saldo + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                            if main_nr == 813:
                                w1.ytd_saldo = w1.ytd_saldo + 1

                            if main_nr == 92:
                                w1.ytd_saldo = w1.ytd_saldo + genstat.logis

                            if main_nr == 756:
                                w1.ytd_saldo = w1.ytd_saldo + genstat.erwachs

                            elif main_nr == 757:
                                w1.ytd_saldo = w1.ytd_saldo + genstat.kind1

                            elif main_nr == 758:
                                w1.ytd_saldo = w1.ytd_saldo + genstat.kind2

                        for segmentstat in db_session.query(Segmentstat).filter(
                                    (Segmentstat.datum >= datum1) &  (Segmentstat.datum <= to_date) &  (Segmentstat.segmentcode == segm)).all():
                            dbudget_flag = (get_month(segmentstat.datum) == get_month(to_date)) and (get_year(segmentstat.datum) == get_year(to_date))

                            if segmentstat.datum == to_date:

                                if main_nr == 814:
                                    w1.tbudget = w1.tbudget + segmentstat.budpersanz

                                if main_nr == 813:
                                    w1.tbudget = w1.tbudget + segmentstat.budzimmeranz

                                if main_nr == 92:
                                    w1.tbudget = w1.tbudget + segmentstat.budlogis

                            if get_month(segmentstat.datum) == mm:

                                if main_nr == 814:

                                    if dbudget_flag:
                                        w1.mon_budget[get_day(segmentstat.datum) - 1] = w1.mon_budget[get_day(segmentstat.datum) - 1] + segmentstat.budpersanz
                                    w1.budget = w1.budget + segmentstat.budpersanz

                                if main_nr == 813:

                                    if dbudget_flag:
                                        w1.mon_budget[get_day(segmentstat.datum) - 1] = w1.mon_budget[get_day(segmentstat.datum) - 1] + segmentstat.budzimmeranz
                                    w1.budget = w1.budget + segmentstat.budzimmeranz

                                if main_nr == 92:

                                    if dbudget_flag:
                                        w1.mon_budget[get_day(segmentstat.datum) - 1] = w1.mon_budget[get_day(segmentstat.datum) - 1] + segmentstat.budlogis
                                    w1.budget = w1.budget + segmentstat.budlogis

                            if main_nr == 814:
                                w1.ytd_budget = w1.ytd_budget + segmentstat.budpersanz

                            if main_nr == 813:
                                w1.ytd_budget = w1.ytd_budget + segmentstat.budzimmeranz

                            if main_nr == 92:
                                w1.ytd_budget = w1.ytd_budget + segmentstat.budlogis

                        if lytd_flag or lmtd_flag:

                            if lytd_flag:
                                datum1 = ljan1
                            else:
                                datum1 = lfrom_date
                            mm = get_month(lto_date)

                            for genstat in db_session.query(Genstat).filter(
                                        (Genstat.segmentcode == segm) &  (Genstat.datum >= datum1) &  (Genstat.datum <= lto_date) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
                                frate = 1

                                if foreign_flag:
                                    find_exrate(genstat.datum)

                                    if exrate:
                                        frate = exrate.betrag
                                dlmtd_flag = (get_month(genstat.datum) == get_month(lto_date)) and (get_year(genstat.datum) == get_year(lto_date))

                                if genstat.datum == lto_date:

                                    if main_nr == 814:
                                        w1.lytoday = w1.lytoday + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                                    if main_nr == 813:
                                        w1.lytoday = w1.lytoday + 1

                                    if main_nr == 92:
                                        w1.lytoday = w1.lytoday + genstat.logis

                                if get_month(genstat.datum) == mm:

                                    if main_nr == 814:
                                        w1.lastyr = w1.lastyr + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                                    if main_nr == 813:
                                        w1.lastyr = w1.lastyr + 1

                                    if main_nr == 92:
                                        w1.lastyr = w1.lastyr + genstat.logis

                                if main_nr == 814:
                                    w1.lytd_saldo = w1.lytd_saldo + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                                if main_nr == 813:
                                    w1.lytd_saldo = w1.lytd_saldo + 1

                                if main_nr == 92:
                                    w1.lytd_saldo = w1.lytd_saldo + genstat.logis

                            for segmentstat in db_session.query(Segmentstat).filter(
                                        (Segmentstat.datum >= datum1) &  (Segmentstat.datum <= lto_date) &  (Segmentstat.segmentcode == segm)).all():

                                if segmentstat.datum == to_date:

                                    if get_month(segmentstat.datum) == mm:

                                        if main_nr == 814:
                                            w1.ly_budget = w1.ly_budget + segmentstat.budpersanz

                                        if main_nr == 813:
                                            w1.ly_budget = w1.ly_budget + segmentstat.budzimmeranz

                                        if main_nr == 92:
                                            w1.ly_budget = w1.ly_budget + segmentstat.budlogis

                                if main_nr == 814:
                                    w1.lytd_budget = w1.lytd_budget + segmentstat.budpersanz

                                if main_nr == 813:
                                    w1.lytd_budget = w1.lytd_budget + segmentstat.budzimmeranz

                                if main_nr == 92:
                                    w1.lytd_budget = w1.lytd_budget + segmentstat.budlogis

                        if pmtd_flag:

                            for genstat in db_session.query(Genstat).filter(
                                        (Genstat.segmentcode == segm) &  (Genstat.datum >= pfrom_date) &  (Genstat.datum <= pto_date) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():

                                if foreign_flag:
                                    find_exrate(genstat.datum)

                                    if exrate:
                                        frate = exrate.betrag

                                if main_nr == 814:
                                    w1.lastmon = w1.lastmon + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                                if main_nr == 813:
                                    w1.lastmon = w1.lastmon + 1

                                if main_nr == 92:
                                    w1.lastmon = w1.lastmon + genstat.logis


    def fill_rmcatstat(rec_w1:int, main_nr:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        zikatno:int = 0
        datum1:date = None

                        w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

                        if w1.done:

                            return
                        zikatno = w1.artnr

                        if ytd_flag:
                            datum1 = jan1
                        else:
                            datum1 = from_date

                        for zkstat in db_session.query(Zkstat).filter(
                                (Zkstat.datum >= datum1) &  (Zkstat.datum <= to_date) &  (Zkstat.zikatnr == zikatno)).all():

                            if zkstat.datum == to_date:
                                w1.tday = w1.tday + zkstat.zimmeranz - zkstat.betriebsnr + zkstat.arrangement_art[0]

                            if zkstat.datum < from_date:
                                w1.ytd_saldo = w1.ytd_saldo + zkstat.zimmeranz - zkstat.betriebsnr + zkstat.arrangement_art[0]
                            else:
                                w1.saldo = w1.saldo + zkstat.zimmeranz - zkstat.betriebsnr + zkstat.arrangement_art[0]

                                if ytd_flag:
                                    w1.ytd_saldo = w1.ytd_saldo + zkstat.zimmeranz - zkstat.betriebsnr + zkstat.arrangement_art[0]

                        if lytd_flag or lmtd_flag:

                            if lytd_flag:
                                datum1 = ljan1
                            else:
                                datum1 = lfrom_date

                            for zkstat in db_session.query(Zkstat).filter(
                                    (Zkstat.datum >= datum1) &  (Zkstat.datum <= lto_date) &  (Zkstat.zikatnr == zikatno)).all():

                                if zkstat.datum < lfrom_date:
                                    w1.lytd_saldo = w1.lytd_saldo + zkstat.zimmeranz - zkstat.betriebsnr + zkstat.arrangement_art[0]
                                else:
                                    w1.lastyr = w1.lastyr + zkstat.zimmeranz - zkstat.betriebsnr + zkstat.arrangement_art[0]

                                    if lytd_flag:
                                        w1.lytd_saldo = w1.lytd_saldo + zkstat.zimmeranz - zkstat.betriebsnr + zkstat.arrangement_art[0]

                        if pmtd_flag:

                            for zkstat in db_session.query(Zkstat).filter(
                                    (Zkstat.datum >= pfrom_date) &  (Zkstat.datum <= pto_date) &  (Zkstat.zikatnr == zikatno)).all():
                                w1.lastmon = w1.lastmon + zkstat.zimmeranz - zkstat.betriebsnr + zkstat.arrangement_art[0]


                        if lytoday_flag:

                            zkstat = db_session.query(Zkstat).filter(
                                    (Zkstat.datum == lytoday) &  (Zkstat.zikatnr == zikatno)).first()

                            if zkstat:
                                w1.lytoday = zkstat.zimmeranz - zkstat.betriebsnr + zkstat.arrangement_art[0]
                        w1.done = True

    def fill_zinrstat(rec_w1:int, main_nr:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        rmno:int = 0
        s_rmno:str = ""
        datum1:date = None
                        W11 = W1
                        W12 = W1
                        W13 = W1

                        if main_nr == 800:

                            w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

                            if w1.done:

                                return
                            rmno = w1.artnr


                            s_rmno = w1.s_artnr

                            w12 = query(w12_list, filters=(lambda w12 :w12.main_code == 180 and w12.artnr == rmno and w12.s_artnr.lower()  == (s_rmno).lower()), first=True)

                            w13 = query(w13_list, filters=(lambda w13 :w13.main_code == 181 and w13.artnr == rmno and w13.s_artnr.lower()  == (s_rmno).lower()), first=True)

                        elif main_nr == 180:

                            w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

                            if w1.done:

                                return
                            rmno = w1.artnr
                            s_rmno = w1.s_artnr

                            w11 = query(w11_list, filters=(lambda w11 :w11.main_code == 800 and w11.artnr == rmno and w11.s_artnr.lower()  == (s_rmno).lower()), first=True)

                            w13 = query(w13_list, filters=(lambda w13 :w13.main_code == 181 and w13.artnr == rmno and w13.s_artnr.lower()  == (s_rmno).lower()), first=True)

                        elif main_nr == 181:

                            w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

                            if w1.done:

                                return
                            rmno = w1.artnr
                            s_rmno = w1.s_artnr

                            w11 = query(w11_list, filters=(lambda w11 :w11.main_code == 800 and w11.artnr == rmno and w11.s_artnr.lower()  == (s_rmno).lower()), first=True)

                            w12 = query(w12_list, filters=(lambda w12 :w12.main_code == 180 and w12.artnr == rmno and w12.s_artnr.lower()  == (s_rmno).lower()), first=True)

                        if ytd_flag:
                            datum1 = jan1
                        else:
                            datum1 = from_date

                        for zinrstat in db_session.query(Zinrstat).filter(
                                    (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= to_date) &  (func.lower(Zinrstat.zinr) == (s_rmno).lower())).all():

                            if foreign_flag:
                                find_exrate(zinrstat.datum)

                                if exrate:
                                    frate = exrate.betrag

                            if zinrstat.datum == to_date:

                                if main_nr == 800:
                                    w1.tday = w1.tday + zinrstat.logisumsatz / frate

                                    if w12:
                                        w12.tday = w12.tday + zinrstat.zimmeranz

                                    if w13:
                                        w13.tday = w13.tday + zinrstat.personen

                                elif main_nr == 180:
                                    w1.tday = w1.tday + zinrstat.zimmeranz

                                    if w11:
                                        w11.tday = w11.tday + zinrstat.logisumsatz / frate

                                    if w13:
                                        w13.tday = w13.tday + zinrstat.personen

                                elif main_nr == 181:
                                    w1.tday = w1.tday + zinrstat.personen

                                    if w11:
                                        w11.tday = w11.tday + zinrstat.logisumsatz / frate

                                    if w12:
                                        w12.tday = w12.tday + zinrstat.zimmeranz

                            if zinrstat.datum < from_date:

                                if main_nr == 800:
                                    w1.ytd_saldo = w1.ytd_saldo + zinrstat.logisumsatz / frate

                                    if w12:
                                        w12.ytd_saldo = w12.ytd_saldo + zinrstat.zimmeranz

                                    if w13:
                                        w13.ytd_saldo = w13.ytd_saldo + zinrstat.personen

                                elif main_nr == 180:
                                    w1.ytd_saldo = w1.ytd_saldo + zinrstat.zimmeranz

                                    if w11:
                                        w11.ytd_saldo = w11.ytd_saldo + zinrstat.logisumsatz / frate

                                    if w13:
                                        w13.ytd_saldo = w13.ytd_saldo + zinrstat.personen

                                elif main_nr == 181:
                                    w1.ytd_saldo = w1.ytd_saldo + zinrstat.personen

                                    if w11:
                                        w11.ytd_saldo = w11.ytd_saldo + zinrstat.logisumsatz / frate

                                    if w12:
                                        w12.ytd_saldo = w12.ytd_saldo + zinrstat.zimmeranz
                            else:

                                if main_nr == 800:
                                    w1.saldo = w1.saldo + zinrstat.logisumsatz / frate

                                    if w12:
                                        w12.saldo = w12.saldo + zinrstat.zimmeranz

                                    if w13:
                                        w13.saldo = w13.saldo + zinrstat.personen

                                elif main_nr == 180:
                                    w1.saldo = w1.saldo + zinrstat.zimmeranz

                                    if w11:
                                        w11.saldo = w11.saldo + zinrstat.logisumsatz / frate

                                    if w13:
                                        w13.saldo = w13.saldo + zinrstat.personen

                                elif main_nr == 181:
                                    w1.saldo = w1.saldo + zinrstat.personen

                                    if w11:
                                        w11.saldo = w11.saldo + zinrstat.logisumsatz / frate

                                    if w12:
                                        w12.saldo = w12.saldo + zinrstat.zimmeranz

                                if ytd_flag:

                                    if main_nr == 800:
                                        w1.ytd_saldo = w1.ytd_saldo + zinrstat.logisumsatz / frate

                                        if w12:
                                            w12.ytd_saldo = w12.ytd_saldo + zinrstat.zimmeranz

                                        if w13:
                                            w13.ytd_saldo = w13.ytd_saldo + zinrstat.personen

                                    elif main_nr == 180:
                                        w1.ytd_saldo = w1.ytd_saldo + zinrstat.zimmeranz

                                        if w11:
                                            w11.ytd_saldo = w11.ytd_saldo + zinrstat.logisumsatz / frate

                                        if w13:
                                            w13.ytd_saldo = w13.ytd_saldo + zinrstat.personen

                                    elif main_nr == 181:
                                        w1.ytd_saldo = w1.ytd_saldo + zinrstat.personen

                                        if w11:
                                            w11.ytd_saldo = w11.ytd_saldo + zinrstat.logisumsatz / frate

                                        if w12:
                                            w12.ytd_saldo = w12.ytd_saldo + zinrstat.zimmeranz

                        if lytd_flag or lmtd_flag:

                            if lytd_flag:
                                datum1 = ljan1
                            else:
                                datum1 = lfrom_date

                            for zinrstat in db_session.query(Zinrstat).filter(
                                        (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= lto_date) &  (func.lower(Zinrstat.zinr) == (s_rmno).lower())).all():

                                if foreign_flag:
                                    find_exrate(zinrstat.datum)

                                    if exrate:
                                        frate = exrate.betrag

                                if zinrstat.datum < lfrom_date:

                                    if main_nr == 800:
                                        w1.lytd_saldo = w1.lytd_saldo + zinrstat.logisumsatz / frate

                                        if w12:
                                            w12.lytd_saldo = w12.lytd_saldo + zinrstat.zimmeranz

                                        if w13:
                                            w13.lytd_saldo = w13.lytd_saldo + zinrstat.personen

                                    elif main_nr == 180:
                                        w1.lytd_saldo = w1.lytd_saldo + zinrstat.zimmeranz

                                        if w11:
                                            w11.lytd_saldo = w11.lytd_saldo + zinrstat.logisumsatz / frate

                                        if w13:
                                            w13.lytd_saldo = w13.lytd_saldo + zinrstat.personen

                                    elif main_nr == 181:
                                        w1.lytd_saldo = w1.lytd_saldo + zinrstat.personen

                                        if w11:
                                            w11.lytd_saldo = w11.lytd_saldo + zinrstat.logisumsatz / frate

                                        if w12:
                                            w12.lytd_saldo = w12.lytd_saldo + zinrstat.zimmeranz
                                else:

                                    if main_nr == 800:
                                        w1.lastyr = w1.lastyr + zinrstat.logisumsatz / frate

                                        if w12:
                                            w12.lastyr = w12.lastyr + zinrstat.zimmeranz

                                        if w13:
                                            w13.lastyr = w13.lastyr + zinrstat.personen

                                    elif main_nr == 180:
                                        w1.lastyr = w1.lastyr + zinrstat.zimmeranz

                                        if w11:
                                            w11.lastyr = w11.lastyr + zinrstat.logisumsatz / frate

                                        if w13:
                                            w13.lastyr = w13.lastyr + zinrstat.personen

                                    elif main_nr == 181:
                                        w1.lastyr = w1.lastyr + zinrstat.personen

                                        if w11:
                                            w11.lastyr = w11.lastyr + zinrstat.logisumsatz / frate

                                        if w12:
                                            w12.lastyr = w12.lastyr + zinrstat.zimmeranz

                                    if lytd_flag:

                                        if main_nr == 800:
                                            w1.lytd_saldo = w1.lytd_saldo + zinrstat.logisumsatz / frate

                                            if w12:
                                                w12.lytd_saldo = w12.lytd_saldo + zinrstat.zimmeranz

                                            if w13:
                                                w13.lytd_saldo = w13.lytd_saldo + zinrstat.personen

                                        elif main_nr == 180:
                                            w1.lytd_saldo = w1.lytd_saldo + zinrstat.zimmeranz

                                            if w11:
                                                w11.lytd_saldo = w11.lytd_saldo + zinrstat.logisumsatz / frate

                                            if w13:
                                                w13.lytd_saldo = w13.lytd_saldo + zinrstat.personen

                                        elif main_nr == 181:
                                            w1.lytd_saldo = w1.lytd_saldo + zinrstat.personen

                                            if w11:
                                                w11.lytd_saldo = w11.lytd_saldo + zinrstat.logisumsatz / frate

                                            if w12:
                                                w12.lytd_saldo = w12.lytd_saldo + zinrstat.zimmeranz

                        if pmtd_flag:

                            for zinrstat in db_session.query(Zinrstat).filter(
                                        (Zinrstat.datum >= pfrom_date) &  (Zinrstat.datum <= pto_date) &  (func.lower(Zinrstat.zinr) == (s_rmno).lower())).all():

                                if foreign_flag:
                                    find_exrate(zinrstat.datum)

                                    if exrate:
                                        frate = exrate.betrag

                                if main_nr == 800:
                                    w1.lastmon = w1.lastmon + zinrstat.logisumsatz / frate

                                    if w12:
                                        w12.lastmon = w12.lastmon + zinrstat.zimmeranz

                                    if w13:
                                        w13.lastmon = w13.lastmon + zinrstat.personen

                                elif main_nr == 180:
                                    w1.lastmon = w1.lastmon + zinrstat.zimmeranz

                                    if w11:
                                        w11.lastmon = w11.lastmon + zinrstat.logisumsatz / frate

                                    if w13:
                                        w13.lastmon = w13.lastmon + zinrstat.personen

                                elif main_nr == 181:
                                    w1.lastmon = w1.lastmon + zinrstat.personen

                                    if w11:
                                        w11.lastmon = w11.lastmon + zinrstat.logisumsatz / frate

                                    if w12:
                                        w12.lastmon = w12.lastmon + zinrstat.zimmeranz


                        if lytoday_flag:

                            zinrstat = db_session.query(Zinrstat).filter(
                                        (Zinrstat.datum == lytoday) &  (func.lower(Zinrstat.zinr) == (s_rmno).lower())).first()

                        if zinrstat:

                            if foreign_flag:
                                find_exrate(zinrstat.datum)

                                if exrate:
                                    frate = exrate.betrag

                            if main_nr == 800:
                                w1.lytoday = zinrstat.logisumsatz / frate

                                if w12:
                                    w12.lytoday = zinrstat.zimmeranz

                                if w13:
                                    w13.lytoday = zinrstat.personen

                            elif main_nr == 180:
                                w1.lytoday = zinrstat.zimmeranz

                                if w11:
                                    w11.lytoday = zinrstat.logisumsatz / frate

                                if w13:
                                    w13.lytoday = zinrstat.personen

                            elif main_nr == 181:
                                w1.lytoday = zinrstat.personen

                                if w11:
                                    w11.lytoday = zinrstat.logisumsatz / frate

                                if w12:
                                    w12.lytoday = zinrstat.zimmeranz
                        w1.done = True

                        if w11:
                            w11.done = True

                        if w12:
                            w12.done = True

                        if w13:
                            w13.done = True

    def find_exrate(curr_date:date):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

                        if foreign_nr != 0:

                            exrate = db_session.query(Exrate).filter(
                                    (Exrate.artnr == foreign_nr) &  (Exrate.datum == curr_date)).first()
                        else:

                            exrate = db_session.query(Exrate).filter(
                                    (Exrate.datum == curr_date)).first()

    def cal_fbcost(artnr:int, dept:int, datum:date):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        cost = 0

        def generate_inner_output():
            return cost

                        h_cost = db_session.query(H_cost).filter(
                                (H_cost.artnr == artnr) &  (H_cost.departement == dept) &  (H_cost.datum == datum) &  (H_cost.flag == 1)).first()

                        if h_cost and h_cost.betrag != 0:
                            cost = h_cost.anzahl * h_cost.betrag
                        else:

                            for h_journal in db_session.query(H_journal).filter(
                                    (H_journal.artnr == artnr) &  (H_journal.departement == dept) &  (H_journal.bill_datum == datum)).all():
                                cost = cost + h_journal.betrag * h_artikel.prozent / 100


        return generate_inner_output()

    def fill_wig(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        curr_date:date = None
        wig_gastnr:int = 0
        d_flag:bool = False

                        w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

                        if w1.done:

                            return

                        htparam = db_session.query(Htparam).filter(
                                (Htparam.paramnr == 109)).first()
                        wig_gastnr = htparam.fint

                        if ytd_flag:
                            datum1 = jan1
                        else:
                            datum1 = from_date

                        for genstat in db_session.query(Genstat).filter(
                                    (Genstat.datum >= datum1) &  (Genstat.datum <= to_date) &  (Genstat.gastnrmember > 0) &  (Genstat.gastnr == wig_gastnr) &  (Genstat.zinr != "") &  (Genstat.resstatus != 13)).all():
                            d_flag = (get_month(genstat.datum) == get_month(to_date)) and (get_year(genstat.datum) == get_year(to_date))

                            if d_flag:
                                w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + 1

                            if genstat.datum == to_date:
                                w1.tday = w1.tday + 1

                            if genstat.datum < from_date:
                                w1.ytd_saldo = w1.ytd_saldo + 1
                            else:
                                w1.saldo = w1.saldo + 1

                                if ytd_flag:
                                    w1.ytd_saldo = w1.ytd_saldo + 1

    def fill_cover_shift2(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        curr_date:date = None
        curr_i:int = 0
        curr_rechnr:int = 0
        billnr:int = 0
        i:int = 0
        found:bool = False
                        Hbuff = H_umsatz

                        w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

                        if ytd_flag:
                            datum1 = jan1
                        else:
                            datum1 = from_date

                        for h_bill_line in db_session.query(H_bill_line).filter(
                                (H_bill_line.bill_datum >= datum1) &  (H_bill_line.bill_datum <= to_date) &  (H_bill_line.departement == w1.dept)).all():

                            if h_bill_line.artnr != 0:

                                h_artikel = db_session.query(H_artikel).filter(
                                        (H_artikel.artnr == h_bill_line.artnr) &  (H_artikel.departement == h_bill_line.departement) &  (H_artikel.artart > 0) &  (H_artikel.artart != 11) &  (H_artikel.artart != 12)).first()

                                if h_artikel:

                                    if curr_rechnr != h_bill_line.rechnr:

                                        h_bill = db_session.query(H_bill).filter(
                                                (H_bill.rechnr == h_bill_line.rechnr) &  (H_bill.departement == h_bill_line.departement)).first()

                                        if h_bill:

                                            if h_bill_line.bill_datum == to_date:

                                                if h_bill_line.betriebsnr == 1:

                                                    if w1.main_code == 2013:
                                                        w1.tday = w1.tday + h_bill.belegung

                                                if h_bill_line.betriebsnr == 2:

                                                    if w1.main_code == 2014:
                                                        w1.tday = w1.tday + h_bill.belegung

                                                if h_bill_line.betriebsnr == 3:

                                                    if w1.main_code == 2015:
                                                        w1.tday = w1.tday + h_bill.belegung

                                                if h_bill_line.betriebsnr == 4:

                                                    if w1.main_code == 2016:
                                                        w1.tday = w1.tday + h_bill.belegung

                                            elif h_bill_line.bill_datum >= from_date:

                                                if h_bill_line.betriebsnr == 1:

                                                    if w1.main_code == 2013:
                                                        w1.saldo = w1.saldo + h_bill.belegung

                                                if h_bill_line.betriebsnr == 2:

                                                    if w1.main_code == 2014:
                                                        w1.saldo = w1.saldo + h_bill.belegung

                                                if h_bill_line.betriebsnr == 3:

                                                    if w1.main_code == 2015:
                                                        w1.saldo = w1.saldo + h_bill.belegung

                                                if h_bill_line.betriebsnr == 4:

                                                    if w1.main_code == 2016:
                                                        w1.saldo = w1.saldo + h_bill.belegung

                                            if h_bill_line.betriebsnr == 1:

                                                if w1.main_code == 2013:
                                                    w1.ytd_saldo = w1.ytd_saldo + h_bill.belegung

                                            if h_bill_line.betriebsnr == 2:

                                                if w1.main_code == 2014:
                                                    w1.ytd_saldo = w1.ytd_saldo + h_bill.belegung

                                            if h_bill_line.betriebsnr == 3:

                                                if w1.main_code == 2015:
                                                    w1.ytd_saldo = w1.ytd_saldo + h_bill.belegung

                                            if h_bill_line.betriebsnr == 4:

                                                if w1.main_code == 2016:
                                                    w1.ytd_saldo = w1.ytd_saldo + h_bill.belegung
                                    curr_rechnr = h_bill_line.rechnr

                            elif h_bill_line.artnr == 0:
                                i = 0
                                found = no
                                billnr = 0


                                while not found:
                                    i = i + 1

                                    if substr (h_bill_line.bezeich, i, 1) == "*":
                                        found = True
                                billnr = to_int(substring(h_bill_line.bezeich, i + 1 - 1, len(h_bill_line.bezeich) - i))

                                if billnr != 0:

                                    bill = db_session.query(Bill).filter(
                                            (Bill.rechnr == billnr)).first()

                                    if bill and bill.zinr != " ":

                                        h_bill = db_session.query(H_bill).filter(
                                                (H_bill.rechnr == h_bill_line.rechnr) &  (H_bill.departement == h_bill_line.departement)).first()

                                        if h_bill:

                                            if h_bill_line.bill_datum == to_date:

                                                if h_bill_line.betriebsnr == 1:

                                                    if w1.main_code == 2009:
                                                        w1.tday = w1.tday + h_bill.belegung

                                                if h_bill_line.betriebsnr == 2:

                                                    if w1.main_code == 2010:
                                                        w1.tday = w1.tday + h_bill.belegung

                                                if h_bill_line.betriebsnr == 3:

                                                    if w1.main_code == 2011:
                                                        w1.tday = w1.tday + h_bill.belegung

                                                if h_bill_line.betriebsnr == 4:

                                                    if w1.main_code == 2012:
                                                        w1.tday = w1.tday + h_bill.belegung

                                            elif h_bill_line.bill_datum >= from_date:

                                                if h_bill_line.betriebsnr == 1:

                                                    if w1.main_code == 2009:
                                                        w1.saldo = w1.saldo + h_bill.belegung

                                                if h_bill_line.betriebsnr == 2:

                                                    if w1.main_code == 2010:
                                                        w1.saldo = w1.saldo + h_bill.belegung

                                                if h_bill_line.betriebsnr == 3:

                                                    if w1.main_code == 2011:
                                                        w1.saldo = w1.saldo + h_bill.belegung

                                                if h_bill_line.betriebsnr == 4:

                                                    if w1.main_code == 2012:
                                                        w1.saldo = w1.saldo + h_bill.belegung

                                            if h_bill_line.betriebsnr == 1:

                                                if w1.main_code == 2009:
                                                    w1.ytd_saldo = w1.ytd_saldo + h_bill.belegung

                                            if h_bill_line.betriebsnr == 2:

                                                if w1.main_code == 2010:
                                                    w1.ytd_saldo = w1.ytd_saldo + h_bill.belegung

                                            if h_bill_line.betriebsnr == 3:

                                                if w1.main_code == 2011:
                                                    w1.ytd_saldo = w1.ytd_saldo + h_bill.belegung

                                            if h_bill_line.betriebsnr == 4:

                                                if w1.main_code == 2012:
                                                    w1.ytd_saldo = w1.ytd_saldo + h_bill.belegung

    def fill_cover_shift(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        curr_date:date = None
        curr_i:int = 0
                        Hbuff = H_umsatz

                        w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

                        if ytd_flag:
                            datum1 = jan1
                        else:
                            datum1 = from_date

                        for h_umsatz in db_session.query(H_umsatz).filter(
                                (H_umsatz.datum >= datum1) &  (H_umsatz.datum <= to_date) &  (H_umsatz.artnr == 0) &  (H_umsatz.departement == w1.dept)).all():

                            if h_umsatz.epreis == 1:

                                if h_umsatz.datum == to_date:

                                    if w1.main_code == 1921:
                                        w1.tday = h_umsatz.betrag

                                    if w1.main_code == 1971:
                                        w1.tday = h_umsatz.nettobetrag

                                    if w1.main_code == 1991:
                                        w1.tday = h_umsatz.anzahl

                                if h_umsatz.datum >= from_date:

                                    if w1.main_code == 1921:
                                        w1.saldo = w1.saldo + h_umsatz.betrag

                                    if w1.main_code == 1971:
                                        w1.saldo = w1.saldo + h_umsatz.nettobetrag

                                    if w1.main_code == 1991:
                                        w1.saldo = w1.saldo + h_umsatz.anzahl

                                if w1.main_code == 1921:
                                    w1.ytd_saldo = w1.ytd_saldo + h_umsatz.betrag

                                if w1.main_code == 1971:
                                    w1.ytd_saldo = w1.ytd_saldo + h_umsatz.nettobetrag

                                if w1.main_code == 1991:
                                    w1.ytd_saldo = w1.ytd_saldo + h_umsatz.anzahl

                            if h_umsatz.epreis == 2:

                                if h_umsatz.datum == to_date:

                                    if w1.main_code == 1922:
                                        w1.tday = h_umsatz.betrag

                                    if w1.main_code == 1972:
                                        w1.tday = h_umsatz.nettobetrag

                                    if w1.main_code == 1992:
                                        w1.tday = h_umsatz.anzahl

                                if h_umsatz.datum >= from_date:

                                    if w1.main_code == 1922:
                                        w1.saldo = w1.saldo + h_umsatz.betrag

                                    if w1.main_code == 1972:
                                        w1.saldo = w1.saldo + h_umsatz.nettobetrag

                                    if w1.main_code == 1992:
                                        w1.saldo = w1.saldo + h_umsatz.anzahl

                                if w1.main_code == 1922:
                                    w1.ytd_saldo = w1.ytd_saldo + h_umsatz.betrag

                                if w1.main_code == 1972:
                                    w1.ytd_saldo = w1.ytd_saldo + h_umsatz.nettobetrag

                                if w1.main_code == 1992:
                                    w1.ytd_saldo = w1.ytd_saldo + h_umsatz.anzahl

                            if h_umsatz.epreis == 3:

                                if h_umsatz.datum == to_date:

                                    if w1.main_code == 1923:
                                        w1.tday = h_umsatz.betrag

                                    if w1.main_code == 1973:
                                        w1.tday = h_umsatz.nettobetrag

                                    if w1.main_code == 1993:
                                        w1.tday = h_umsatz.anzahl

                                if h_umsatz.datum >= from_date:

                                    if w1.main_code == 1923:
                                        w1.saldo = w1.saldo + h_umsatz.betrag

                                    if w1.main_code == 1973:
                                        w1.saldo = w1.saldo + h_umsatz.nettobetrag

                                    if w1.main_code == 1993:
                                        w1.saldo = w1.saldo + h_umsatz.anzahl

                                if w1.main_code == 1923:
                                    w1.ytd_saldo = w1.ytd_saldo + h_umsatz.betrag

                                if w1.main_code == 1973:
                                    w1.ytd_saldo = w1.ytd_saldo + h_umsatz.nettobetrag

                                if w1.main_code == 1993:
                                    w1.ytd_saldo = w1.ytd_saldo + h_umsatz.anzahl

                            if h_umsatz.epreis == 4:

                                if h_umsatz.datum == to_date:

                                    if w1.main_code == 1924:
                                        w1.tday = h_umsatz.betrag

                                    if w1.main_code == 1974:
                                        w1.tday = h_umsatz.nettobetrag

                                    if w1.main_code == 1994:
                                        w1.tday = h_umsatz.anzahl

                                if h_umsatz.datum >= from_date:

                                    if w1.main_code == 1924:
                                        w1.saldo = w1.saldo + h_umsatz.betrag

                                    if w1.main_code == 1974:
                                        w1.saldo = w1.saldo + h_umsatz.nettobetrag

                                    if w1.main_code == 1994:
                                        w1.saldo = w1.saldo + h_umsatz.anzahl

                                if w1.main_code == 1924:
                                    w1.ytd_saldo = w1.ytd_saldo + h_umsatz.betrag

                                if w1.main_code == 1974:
                                    w1.ytd_saldo = w1.ytd_saldo + h_umsatz.nettobetrag

                                if w1.main_code == 1994:
                                    w1.ytd_saldo = w1.ytd_saldo + h_umsatz.anzahl

                        if lytd_flag or lmtd_flag:

                            if lytd_flag:
                                datum1 = ljan1
                            else:
                                datum1 = lfrom_date

                            for h_umsatz in db_session.query(H_umsatz).filter(
                                    (H_umsatz.datum >= datum1) &  (H_umsatz.datum <= lto_date) &  (H_umsatz.artnr == 0) &  (H_umsatz.departement == w1.dept)).all():

                                if h_umsatz.epreis == 1:

                                    if h_umsatz.datum >= lfrom_date:

                                        if w1.main_code == 1921:
                                            w1.lastyr = w1.lastyr + h_umsatz.betrag

                                        if w1.main_code == 1971:
                                            w1.lastyr = w1.lastyr + h_umsatz.nettobetrag

                                        if w1.main_code == 1991:
                                            w1.lastyr = w1.lastyr + h_umsatz.anzahl

                                    if w1.main_code == 1921:
                                        w1.lytd_saldo = w1.lytd_saldo + h_umsatz.betrag

                                    if w1.main_code == 1971:
                                        w1.lytd_saldo = w1.lytd_saldo + h_umsatz.nettobetrag

                                    if w1.main_code == 1991:
                                        w1.lytd_saldo = w1.lytd_saldo + h_umsatz.anzahl

                                if h_umsatz.epreis == 2:

                                    if h_umsatz.datum >= lfrom_date:

                                        if w1.main_code == 1922:
                                            w1.lastyr = w1.lastyr + h_umsatz.betrag

                                        if w1.main_code == 1972:
                                            w1.lastyr = w1.lastyr + h_umsatz.nettobetrag

                                        if w1.main_code == 1992:
                                            w1.lastyr = w1.lastyr + h_umsatz.anzahl

                                    if w1.main_code == 1922:
                                        w1.lytd_saldo = w1.lytd_saldo + h_umsatz.betrag

                                    if w1.main_code == 1972:
                                        w1.lytd_saldo = w1.lytd_saldo + h_umsatz.nettobetrag

                                    if w1.main_code == 1992:
                                        w1.lytd_saldo = w1.lytd_saldo + h_umsatz.anzahl

                                if h_umsatz.epreis == 3:

                                    if h_umsatz.datum >= lfrom_date:

                                        if w1.main_code == 1923:
                                            w1.lastyr = w1.lastyr + h_umsatz.betrag

                                        if w1.main_code == 1973:
                                            w1.lastyr = w1.lastyr + h_umsatz.nettobetrag

                                        if w1.main_code == 1993:
                                            w1.lastyr = w1.lastyr + h_umsatz.anzahl

                                    if w1.main_code == 1923:
                                        w1.lytd_saldo = w1.lytd_saldo + h_umsatz.betrag

                                    if w1.main_code == 1973:
                                        w1.lytd_saldo = w1.lytd_saldo + h_umsatz.nettobetrag

                                    if w1.main_code == 1993:
                                        w1.lytd_saldo = w1.lytd_saldo + h_umsatz.anzahl

                                if h_umsatz.epreis == 4:

                                    if h_umsatz.datum >= lfrom_date:

                                        if w1.main_code == 1924:
                                            w1.lastyr = w1.lastyr + h_umsatz.betrag

                                        if w1.main_code == 1974:
                                            w1.lastyr = w1.lastyr + h_umsatz.nettobetrag

                                        if w1.main_code == 1994:
                                            w1.lastyr = w1.lastyr + h_umsatz.anzahl

                                    if w1.main_code == 1924:
                                        w1.lytd_saldo = w1.lytd_saldo + h_umsatz.betrag

                                    if w1.main_code == 1974:
                                        w1.lytd_saldo = w1.lytd_saldo + h_umsatz.nettobetrag

                                    if w1.main_code == 1994:
                                        w1.lytd_saldo = w1.lytd_saldo + h_umsatz.anzahl

    def fill_los():

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        done = False
        datum1:date = None
        datum:date = None
        ci_date:date = None
        end_date:date = None
        start_date:date = None
        i:int = 0
        los:int = 0
        mon_saldo1:[decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo2:[decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo3:[decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo4:[decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo5:[decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo6:[decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo7:[decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo8:[decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo9:[decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo10:[decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo11:[decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mon_saldo12:[decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        def generate_inner_output():
            return done

                        htparam = db_session.query(Htparam).filter(
                                (Htparam.paramnr == 87)).first()
                        ci_date = htparam.fdate
                        Wlos = W1

                        if ytd_flag:
                            datum1 = jan1
                        else:
                            datum1 = from_date

                        wlos = query(wlos_list, filters=(lambda wlos :wlos.main_code == 9000), first=True)

                        for res_line in db_session.query(Res_line).filter(
                                (Res_line.abreise >= datum1) &  (Res_line.ankunf <= to_date) &  (Res_line.l_zuordnung[2] == 0) &  (Res_line.zinr != "") &  (Res_line.l_zuordnung[0] != 0) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 99) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12)).all():

                            if res_line.ankunft == to_date and res_line.active_flag != 1:
                                pass
                            else:

                                if res_line.abreise == res_line.ankunft:
                                    end_date = res_line.abreise
                                else:
                                    end_date = res_line.abreise - 1

                                if end_date > to_date:
                                    end_date = to_date

                                if res_line.ankunft < datum1:
                                    start_date = datum1
                                else:
                                    start_date = res_line.ankunft
                                for datum in range(start_date,end_date + 1) :

                                    if res_line.abreise - datum == 0:
                                        los = 1
                                    else:
                                        los = res_line.abreise - datum

                                    if datum == to_date:
                                        wlos.tday = wlos.tday + los

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
                            wlos.saldo = wlos.saldo + wlos.mon_saldo[i - 1]
                            wlos.ytd_saldo = wlos.ytd_saldo + mon_saldo1[i - 1] + mon_saldo2[i - 1] + mon_saldo3[i - 1] + mon_saldo4[i - 1] + mon_saldo5[i - 1] + mon_saldo6[i - 1] + mon_saldo7[i - 1] + mon_saldo8[i - 1] + mon_saldo9[i - 1] + mon_saldo10[i - 1] + mon_saldo11[i - 1] + mon_saldo12[i - 1]
                        done = True


        return generate_inner_output()

    def fill_pax_cover_shift():

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        done = False
        datum1:date = None
        disc_art1:int = 0
        disc_art2:int = 0
        disc_art3:int = 0
        shift:int = 0
        temp1:str = ""
        temp2:str = ""
        do_it:bool = True

        def generate_inner_output():
            return done
                        Buff = H_bill_line
                        Art_buff = H_artikel
                        Wspc = W1
                        disc_art1 = get_output(htpint(557))
                        disc_art2 = get_output(htpint(596))

                        for queasy in db_session.query(Queasy).filter(
                                (Queasy.key == 5) &  (Queasy.number3 != 0)).all():
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
                        t_list._list.clear()

                        h_bill_line_obj_list = []
                        for h_bill_line, h_artikel, artikel, h_bill in db_session.query(H_bill_line, H_artikel, Artikel, H_bill).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) &  (H_artikel.departement == H_bill_line.departement) &  (H_artikel.artart == 0) &  (H_artikel.artart != 11) &  (H_artikel.artart != 12)).join(Artikel,(Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).join(H_bill,(H_bill.rechnr == H_bill_line.rechnr) &  (H_bill.departement == H_bill_line.departement)).filter(
                                (H_bill_line.bill_datum >= datum1) &  (H_bill_line.bill_datum <= to_date) &  (H_bill_line.artnr > 0) &  (H_bill_line.artnr != disc_art1) &  (H_bill_line.artnr != disc_art2) &  (H_bill_line.artnr != disc_art3) &  (H_bill_line.zeit >= 0) &  (H_bill_line.epreis > 0)).all():
                            if h_bill_line._recid in h_bill_line_obj_list:
                                continue
                            else:
                                h_bill_line_obj_list.append(h_bill_line._recid)


                            do_it = True

                            buff_obj_list = []
                            for buff, art_buff in db_session.query(Buff, Art_buff).join(Art_buff,(art_Buff.artnr == Buff.artnr) &  (art_Buff.departement == Buff.departement)).filter(
                                    (Buff.rechnr == h_bill_line.rechnr) &  (Buff.departement == h_bill_line.departement)).all():
                                if buff._recid in buff_obj_list:
                                    continue
                                else:
                                    buff_obj_list.append(buff._recid)

                                if art_buff.artart == 11 or art_buff.artart == 12:
                                    do_it = False
                                    break

                            if do_it:
                                shift = 0

                                shift_list = query(shift_list_list, filters=(lambda shift_list :shift_list.ftime <= h_bill_line.zeit and shift_list.ttime >= h_bill_line.zeit), first=True)

                                if shift_list:
                                    shift = shift_list.shift

                                t_list = query(t_list_list, filters=(lambda t_list :t_list.dept == h_bill_line.departement and t_list.datum == h_bill_line.bill_datum and t_list.shift == h_bill_line.betriebsnr), first=True)

                                if not t_list:
                                    t_list = T_list()
                                    t_list_list.append(t_list)

                                    t_list.datum = h_bill_line.bill_datum
                                    t_list.dept = h_bill_line.departement
                                    t_list.shift = h_bill_line.betriebsnr

                                t_rechnr = query(t_rechnr_list, filters=(lambda t_rechnr :t_rechnr.rechnr == h_bill_line.rechnr and t_rechnr.dept == h_bill_line.departement and t_rechnr.datum == h_bill_line.bill_datum and t_rechnr.shift == shift), first=True)

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

                        for t_list in query(t_list_list):

                            wspc = query(wspc_list, filters=(lambda wspc :wspc.main_code == 1995 and to_int(substring(wspc.s_artnr, 0, 2)) == t_list.dept and to_int(substring(wspc.s_artnr, 2)) == t_list.shift), first=True)

                            if wspc:

                                if t_list.datum == to_date:
                                    wspc.tday = wspc.tday + t_list.pax_food

                                if get_month(t_list.datum) == get_month(to_date):
                                    wspc.saldo = wspc.saldo + t_list.pax_food
                                wspc.ytd_saldo = wspc.ytd_saldo + t_list.pax_food

                            wspc = query(wspc_list, filters=(lambda wspc :wspc.main_code == 1996 and to_int(substring(wspc.s_artnr, 0, 2)) == t_list.dept and to_int(substring(wspc.s_artnr, 2)) == t_list.shift), first=True)

                            if wspc:

                                if t_list.datum == to_date:
                                    wspc.tday = wspc.tday + t_list.pax_bev

                                if get_month(t_list.datum) == get_month(to_date):
                                    wspc.saldo = wspc.saldo + t_list.pax_bev
                                wspc.ytd_saldo = wspc.ytd_saldo + t_list.pax_bev


        return generate_inner_output()

    def fill_pax_cover_shift1(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        endkum:int = 0
        artnrfront:int = 0
        compli_flag:bool = False
        vat:decimal = 0
        vat2:decimal = 0
        service:decimal = 0
        fact:decimal = 0
        netto:decimal = 0
        curr_rechnr:int = 0
        temp_time:int = 0
        d_flag:bool = False
                        Btemp_rechnr = Temp_rechnr
                        Bh_artikel = H_artikel
                        Bh_bill_line = H_bill_line

                        w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

                        if ytd_flag:
                            datum1 = jan1
                        else:
                            datum1 = from_date
                        curr_rechnr = 0

                        temp_rechnr = query(temp_rechnr_list, first=True)

                        if not temp_rechnr:

                            h_bill_line_obj_list = []
                            for h_bill_line, h_artikel, h_bill in db_session.query(H_bill_line, H_artikel, H_bill).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) &  (H_artikel.departement == H_bill_line.departement)).join(H_bill,(H_bill.rechnr == H_bill_line.rechnr) &  (H_bill.departement == H_bill_line.departement)).filter(
                                    (H_bill_line.bill_datum >= datum1) &  (H_bill_line.bill_datum <= to_date) &  (H_bill_line.artnr > 0)).all():
                                if h_bill_line._recid in h_bill_line_obj_list:
                                    continue
                                else:
                                    h_bill_line_obj_list.append(h_bill_line._recid)

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
                                    temp_rechnr.betrag = h_bill_line.betrag
                                    temp_rechnr.artnr = h_bill_line.artnr
                                    temp_rechnr.artart = h_artikel.artart


                                    curr_rechnr = h_bill_line.rechnr

                                    bh_bill_line_obj_list = []
                                    for bh_bill_line, bh_artikel in db_session.query(Bh_bill_line, Bh_artikel).join(Bh_artikel,(Bh_artikel.artnr == Bh_bill_line.artnr) &  (Bh_artikel.departement == Bh_bill_line.departement) &  (Bh_artikel.artart >= 11) &  (Bh_artikel.artart <= 12)).filter(
                                            (Bh_bill_line.rechnr == h_bill_line.rechnr) &  (Bh_bill_line.departement == h_bill_line.departement)).all():
                                        if bh_bill_line._recid in bh_bill_line_obj_list:
                                            continue
                                        else:
                                            bh_bill_line_obj_list.append(bh_bill_line._recid)


                                        temp_rechnr.compli_flag = True


                                        break

                        for temp_rechnr in query(temp_rechnr_list, filters=(lambda temp_rechnr :temp_rechnr.dept == w1.dept)):

                            if w1.main_code == 2028:

                                if temp_rechnr.datum == to_date:
                                    w1.tday = w1.tday + temp_rechnr.belegung

                                if temp_rechnr.datum >= date_mdy(get_month(to_date) , 1, get_year(to_date)):
                                    w1.saldo = w1.saldo + temp_rechnr.belegung
                                w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung
                                d_flag = (get_month(temp_rechnr.datum) == get_month(to_date)) and (get_year(temp_rechnr.datum) == get_year(to_date))

                                if d_flag:
                                    w1.mon_saldo[get_day(temp_rechnr.datum) - 1] = w1.mon_saldo[get_day(temp_rechnr.datum) - 1] + temp_rechnr.belegung

                            elif w1.main_code == 552:

                                if not temp_rechnr.compli_flag:

                                    if temp_rechnr.datum == to_date:
                                        w1.tday = w1.tday + temp_rechnr.belegung

                                    if temp_rechnr.datum >= date_mdy(get_month(to_date) , 1, get_year(to_date)):
                                        w1.saldo = w1.saldo + temp_rechnr.belegung
                                    w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung
                                    d_flag = (get_month(temp_rechnr.datum) == get_month(to_date)) and (get_year(temp_rechnr.datum) == get_year(to_date))

                                    if d_flag:
                                        w1.mon_saldo[get_day(temp_rechnr.datum) - 1] = w1.mon_saldo[get_day(temp_rechnr.datum) - 1] + temp_rechnr.belegung

                            elif w1.main_code == 2029:

                                if temp_rechnr.datum == to_date:
                                    w1.tday = w1.tday + 1

                                if temp_rechnr.datum >= date_mdy(get_month(to_date) , 1, get_year(to_date)):
                                    w1.saldo = w1.saldo + 1
                                w1.ytd_saldo = w1.ytd_saldo + 1

                            elif w1.main_code == 2031 and w1.tischnr == temp_rechnr.tischnr:

                                if temp_rechnr.datum == to_date:
                                    w1.tday = w1.tday + temp_rechnr.belegung

                                if temp_rechnr.datum >= date_mdy(get_month(to_date) , 1, get_year(to_date)):
                                    w1.saldo = w1.saldo + temp_rechnr.belegung
                                w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                            elif (w1.main_code >= 2020 and w1.main_code <= 2027) or (w1.main_code == 1995 or w1.main_code == 1996):

                                if not temp_rechnr.compli_flag and temp_rechnr.artnrfront >= 10 and temp_rechnr.artnrfront <= 11:

                                    if temp_rechnr.artnrfront == 10:

                                        if temp_rechnr.datum == to_date:

                                            if temp_rechnr.shift == 1:

                                                if w1.main_code == 2020:
                                                    w1.tday = w1.tday + temp_rechnr.belegung

                                            if temp_rechnr.shift == 2:

                                                if w1.main_code == 2021:
                                                    w1.tday = w1.tday + temp_rechnr.belegung

                                            if temp_rechnr.shift == 3:

                                                if w1.main_code == 2022:
                                                    w1.tday = w1.tday + temp_rechnr.belegung

                                            if temp_rechnr.shift == 4:

                                                if w1.main_code == 2023:
                                                    w1.tday = w1.tday + temp_rechnr.belegung

                                            if w1.main_code == 1995:
                                                w1.tday = w1.tday + temp_rechnr.belegung

                                        elif get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):

                                            if temp_rechnr.shift == 1:

                                                if w1.main_code == 2020:
                                                    w1.saldo = w1.saldo + temp_rechnr.belegung

                                            if temp_rechnr.shift == 2:

                                                if w1.main_code == 2021:
                                                    w1.saldo = w1.saldo + temp_rechnr.belegung

                                            if temp_rechnr.shift == 3:

                                                if w1.main_code == 2022:
                                                    w1.saldo = w1.saldo + temp_rechnr.belegung

                                            if temp_rechnr.shift == 4:

                                                if w1.main_code == 2023:
                                                    w1.saldo = w1.saldo + temp_rechnr.belegung

                                            if w1.main_code == 1995:
                                                w1.saldo = w1.saldo + temp_rechnr.belegung

                                        if temp_rechnr.shift == 1:

                                            if w1.main_code == 2020:
                                                w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                        if temp_rechnr.shift == 2:

                                            if w1.main_code == 2021:
                                                w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                        if temp_rechnr.shift == 3:

                                            if w1.main_code == 2022:
                                                w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                        if temp_rechnr.shift == 4:

                                            if w1.main_code == 2023:
                                                w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                        if w1.main_code == 1995:
                                            w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                    if temp_rechnr.artnrfront == 11:

                                        if temp_rechnr.datum == to_date:

                                            if temp_rechnr.shift == 1:

                                                if w1.main_code == 2024:
                                                    w1.tday = w1.tday + temp_rechnr.belegung

                                            if temp_rechnr.shift == 2:

                                                if w1.main_code == 2025:
                                                    w1.tday = w1.tday + temp_rechnr.belegung

                                            if temp_rechnr.shift == 3:

                                                if w1.main_code == 2026:
                                                    w1.tday = w1.tday + temp_rechnr.belegung

                                            if temp_rechnr.shift == 4:

                                                if w1.main_code == 2027:
                                                    w1.tday = w1.tday + temp_rechnr.belegung

                                            if w1.main_code == 1996:
                                                w1.tday = w1.tday + temp_rechnr.belegung

                                        elif get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):

                                            if temp_rechnr.shift == 1:

                                                if w1.main_code == 2024:
                                                    w1.saldo = w1.saldo + temp_rechnr.belegung

                                            if temp_rechnr.shift == 2:

                                                if w1.main_code == 2025:
                                                    w1.saldo = w1.saldo + temp_rechnr.belegung

                                            if temp_rechnr.shift == 3:

                                                if w1.main_code == 2026:
                                                    w1.saldo = w1.saldo + temp_rechnr.belegung

                                            if temp_rechnr.shift == 4:

                                                if w1.main_code == 2027:
                                                    w1.saldo = w1.saldo + temp_rechnr.belegung

                                            if w1.main_code == 1996:
                                                w1.tday = w1.tday + temp_rechnr.belegung

                                        if temp_rechnr.shift == 1:

                                            if w1.main_code == 2024:
                                                w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                        if temp_rechnr.shift == 2:

                                            if w1.main_code == 2025:
                                                w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                        if temp_rechnr.shift == 3:

                                            if w1.main_code == 2026:
                                                w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                        if temp_rechnr.shift == 4:

                                            if w1.main_code == 2027:
                                                w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                        if w1.main_code == 1996:
                                            w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                            elif (w1.main_code >= 2001 and w1.main_code <= 2004) or (w1.main_code >= 2032 and w1.main_code <= 2051):

                                bill = db_session.query(Bill).filter(
                                        (Bill.rechnr == temp_rechnr.rechnr)).first()

                                if bill:

                                    if bill.zinr != "":

                                        if temp_rechnr.datum == to_date:

                                            if temp_rechnr.shift == 1:

                                                if w1.main_code == 2001:
                                                    w1.tday = w1.tday + temp_rechnr.belegung

                                            if temp_rechnr.shift == 2:

                                                if w1.main_code == 2002:
                                                    w1.tday = w1.tday + temp_rechnr.belegung

                                            if temp_rechnr.shift == 3:

                                                if w1.main_code == 2003:
                                                    w1.tday = w1.tday + temp_rechnr.belegung

                                            if temp_rechnr.shift == 4:

                                                if w1.main_code == 2004:
                                                    w1.tday = w1.tday + temp_rechnr.belegung

                                        elif get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):

                                            if temp_rechnr.shift == 1:

                                                if w1.main_code == 2001:
                                                    w1.saldo = w1.saldo + temp_rechnr.belegung

                                            if temp_rechnr.shift == 2:

                                                if w1.main_code == 2002:
                                                    w1.saldo = w1.saldo + temp_rechnr.belegung

                                            if temp_rechnr.shift == 3:

                                                if w1.main_code == 2003:
                                                    w1.saldo = w1.saldo + temp_rechnr.belegung

                                            if temp_rechnr.shift == 4:

                                                if w1.main_code == 2004:
                                                    w1.saldo = w1.saldo + temp_rechnr.belegung

                                        if temp_rechnr.shift == 1:

                                            if w1.main_code == 2001:
                                                w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                        if temp_rechnr.shift == 2:

                                            if w1.main_code == 2002:
                                                w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                        if temp_rechnr.shift == 3:

                                            if w1.main_code == 2003:
                                                w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                        if temp_rechnr.shift == 4:

                                            if w1.main_code == 2004:
                                                w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                        if temp_rechnr.compli_flag :

                                            if temp_rechnr.datum == to_date:

                                                if temp_rechnr.shift == 1:

                                                    if w1.main_code == 2032:
                                                        w1.tday = w1.tday + temp_rechnr.belegung

                                                if temp_rechnr.shift == 2:

                                                    if w1.main_code == 2033:
                                                        w1.tday = w1.tday + temp_rechnr.belegung

                                                if temp_rechnr.shift == 3:

                                                    if w1.main_code == 2034:
                                                        w1.tday = w1.tday + temp_rechnr.belegung

                                                if temp_rechnr.shift == 4:

                                                    if w1.main_code == 2035:
                                                        w1.tday = w1.tday + temp_rechnr.belegung

                                            elif get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):

                                                if temp_rechnr.shift == 1:

                                                    if w1.main_code == 2032:
                                                        w1.saldo = w1.saldo + temp_rechnr.belegung

                                                if temp_rechnr.shift == 2:

                                                    if w1.main_code == 2033:
                                                        w1.saldo = w1.saldo + temp_rechnr.belegung

                                                if temp_rechnr.shift == 3:

                                                    if w1.main_code == 2034:
                                                        w1.saldo = w1.saldo + temp_rechnr.belegung

                                                if temp_rechnr.shift == 4:

                                                    if w1.main_code == 2035:
                                                        w1.saldo = w1.saldo + temp_rechnr.belegung

                                            if temp_rechnr.shift == 1:

                                                if w1.main_code == 2032:
                                                    w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                            if temp_rechnr.shift == 2:

                                                if w1.main_code == 2033:
                                                    w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                            if temp_rechnr.shift == 3:

                                                if w1.main_code == 2034:
                                                    w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                            if temp_rechnr.shift == 4:

                                                if w1.main_code == 2035:
                                                    w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                        artikel = db_session.query(Artikel).filter(
                                                (Artikel.departement == temp_rechnr.dept) &  (Artikel.artnr == temp_rechnr.artnrfront)).first()

                                        if artikel:
                                            service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, temp_rechnr.datum))
                                            netto = temp_rechnr.betrag / (1 + vat + vat2 + service)

                                            if temp_rechnr.datum == to_date:

                                                if temp_rechnr.shift == 1:

                                                    if w1.main_code == 2044:
                                                        w1.tday = w1.tday + netto

                                                if temp_rechnr.shift == 2:

                                                    if w1.main_code == 2045:
                                                        w1.tday = w1.tday + netto

                                                if temp_rechnr.shift == 3:

                                                    if w1.main_code == 2046:
                                                        w1.tday = w1.tday + netto

                                                if temp_rechnr.shift == 4:

                                                    if w1.main_code == 2047:
                                                        w1.tday = w1.tday + netto

                                            elif get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):

                                                if temp_rechnr.shift == 1:

                                                    if w1.main_code == 2044:
                                                        w1.saldo = w1.saldo + netto

                                                if temp_rechnr.shift == 2:

                                                    if w1.main_code == 2045:
                                                        w1.saldo = w1.saldo + netto

                                                if temp_rechnr.shift == 3:

                                                    if w1.main_code == 2046:
                                                        w1.saldo = w1.saldo + netto

                                                if temp_rechnr.shift == 4:

                                                    if w1.main_code == 2047:
                                                        w1.saldo = w1.saldo + netto

                                            if temp_rechnr.shift == 1:

                                                if w1.main_code == 2044:
                                                    w1.ytd_saldo = w1.ytd_saldo + netto

                                            if temp_rechnr.shift == 2:

                                                if w1.main_code == 2045:
                                                    w1.ytd_saldo = w1.ytd_saldo + netto

                                            if temp_rechnr.shift == 3:

                                                if w1.main_code == 2046:
                                                    w1.ytd_saldo = w1.ytd_saldo + netto

                                            if temp_rechnr.shift == 4:

                                                if w1.main_code == 2047:
                                                    w1.ytd_saldo = w1.ytd_saldo + netto

                                    elif bill.zinr == "":

                                        if temp_rechnr.datum == to_date:

                                            if temp_rechnr.shift == 1:

                                                if w1.main_code == 2036:
                                                    w1.tday = w1.tday + temp_rechnr.belegung

                                            if temp_rechnr.shift == 2:

                                                if w1.main_code == 2037:
                                                    w1.tday = w1.tday + temp_rechnr.belegung

                                            if temp_rechnr.shift == 3:

                                                if w1.main_code == 2038:
                                                    w1.tday = w1.tday + temp_rechnr.belegung

                                            if temp_rechnr.shift == 4:

                                                if w1.main_code == 2039:
                                                    w1.tday = w1.tday + temp_rechnr.belegung

                                        elif get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):

                                            if temp_rechnr.shift == 1:

                                                if w1.main_code == 2036:
                                                    w1.saldo = w1.saldo + temp_rechnr.belegung

                                            if temp_rechnr.shift == 2:

                                                if w1.main_code == 2037:
                                                    w1.saldo = w1.saldo + temp_rechnr.belegung

                                            if temp_rechnr.shift == 3:

                                                if w1.main_code == 2038:
                                                    w1.saldo = w1.saldo + temp_rechnr.belegung

                                            if temp_rechnr.shift == 4:

                                                if w1.main_code == 2039:
                                                    w1.saldo = w1.saldo + temp_rechnr.belegung

                                        if temp_rechnr.shift == 1:

                                            if w1.main_code == 2036:
                                                w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                        if temp_rechnr.shift == 2:

                                            if w1.main_code == 2037:
                                                w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                        if temp_rechnr.shift == 3:

                                            if w1.main_code == 2038:
                                                w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                        if temp_rechnr.shift == 4:

                                            if w1.main_code == 2039:
                                                w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                        if temp_rechnr.compli_flag :

                                            if temp_rechnr.datum == to_date:

                                                if temp_rechnr.shift == 1:

                                                    if w1.main_code == 2040:
                                                        w1.tday = w1.tday + temp_rechnr.belegung

                                                if temp_rechnr.shift == 2:

                                                    if w1.main_code == 2041:
                                                        w1.tday = w1.tday + temp_rechnr.belegung

                                                if temp_rechnr.shift == 3:

                                                    if w1.main_code == 2042:
                                                        w1.tday = w1.tday + temp_rechnr.belegung

                                                if temp_rechnr.shift == 4:

                                                    if w1.main_code == 2043:
                                                        w1.tday = w1.tday + temp_rechnr.belegung

                                            elif get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):

                                                if temp_rechnr.shift == 1:

                                                    if w1.main_code == 2040:
                                                        w1.saldo = w1.saldo + temp_rechnr.belegung

                                                if temp_rechnr.shift == 2:

                                                    if w1.main_code == 2041:
                                                        w1.saldo = w1.saldo + temp_rechnr.belegung

                                                if temp_rechnr.shift == 3:

                                                    if w1.main_code == 2042:
                                                        w1.saldo = w1.saldo + temp_rechnr.belegung

                                                if temp_rechnr.shift == 4:

                                                    if w1.main_code == 2043:
                                                        w1.saldo = w1.saldo + temp_rechnr.belegung

                                            if temp_rechnr.shift == 1:

                                                if w1.main_code == 2040:
                                                    w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                            if temp_rechnr.shift == 2:

                                                if w1.main_code == 2041:
                                                    w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                            if temp_rechnr.shift == 3:

                                                if w1.main_code == 2042:
                                                    w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                            if temp_rechnr.shift == 4:

                                                if w1.main_code == 2043:
                                                    w1.ytd_saldo = w1.ytd_saldo + temp_rechnr.belegung

                                        artikel = db_session.query(Artikel).filter(
                                                (Artikel.departement == temp_rechnr.dept) &  (Artikel.artnr == temp_rechnr.artnrfront)).first()

                                        if artikel:
                                            service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, temp_rechnr.datum))
                                            netto = temp_rechnr.betrag / (1 + vat + vat2 + service)

                                            if temp_rechnr.datum == to_date:

                                                if temp_rechnr.shift == 1:

                                                    if w1.main_code == 2048:
                                                        w1.tday = w1.tday + netto

                                                if temp_rechnr.shift == 2:

                                                    if w1.main_code == 2049:
                                                        w1.tday = w1.tday + netto

                                                if temp_rechnr.shift == 3:

                                                    if w1.main_code == 2050:
                                                        w1.tday = w1.tday + netto

                                                if temp_rechnr.shift == 4:

                                                    if w1.main_code == 2051:
                                                        w1.tday = w1.tday + netto

                                            elif get_month(temp_rechnr.datum) == get_month(to_date) and get_year(temp_rechnr.datum) == get_year(to_date):

                                                if temp_rechnr.shift == 1:

                                                    if w1.main_code == 2048:
                                                        w1.saldo = w1.saldo + netto

                                                if temp_rechnr.shift == 2:

                                                    if w1.main_code == 2049:
                                                        w1.saldo = w1.saldo + netto

                                                if temp_rechnr.shift == 3:

                                                    if w1.main_code == 2050:
                                                        w1.saldo = w1.saldo + netto

                                                if temp_rechnr.shift == 4:

                                                    if w1.main_code == 2051:
                                                        w1.saldo = w1.saldo + netto

                                            if temp_rechnr.shift == 1:

                                                if w1.main_code == 2048:
                                                    w1.ytd_saldo = w1.ytd_saldo + netto

                                            if temp_rechnr.shift == 2:

                                                if w1.main_code == 2049:
                                                    w1.ytd_saldo = w1.ytd_saldo + netto

                                            if temp_rechnr.shift == 3:

                                                if w1.main_code == 2050:
                                                    w1.ytd_saldo = w1.ytd_saldo + netto

                                            if temp_rechnr.shift == 4:

                                                if w1.main_code == 2051:
                                                    w1.ytd_saldo = w1.ytd_saldo + netto

    def fill_fbstat(rec_w1:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        fbdept:int = 0
        shift:int = 0
        do_it:bool = True
        d_flag:bool = False
        mm:int = 0
        yy:int = 0
                        Wf1 = W1
                        Wf2 = W1
                        Wf3 = W1
                        Wf4 = W1
                        Wb1 = W1
                        Wb2 = W1
                        Wb3 = W1
                        Wb4 = W1
                        Wo1 = W1
                        Wo2 = W1
                        Wo3 = W1
                        Wo4 = W1

                        w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)
                        fbdept = to_int(substring(w1.s_artnr, 0, 2))

                        fbstat_dept = query(fbstat_dept_list, filters=(lambda fbstat_dept :fbstat_dept.dept == fbdept), first=True)

                        if fbstat_dept:
                            do_it = False

                        if do_it:
                            fbstat_dept = Fbstat_dept()
                            fbstat_dept_list.append(fbstat_dept)

                            fbstat_dept.dept = fbdept

                            wf1 = query(wf1_list, filters=(lambda wf1 :wf1.main_code == 1997 and to_int(substring(wf1.s_artnr, 0, 2)) == fbdept and to_int(substring(wf1.s_artnr, 2)) == 1), first=True)

                            wf2 = query(wf2_list, filters=(lambda wf2 :wf2.main_code == 1997 and to_int(substring(wf2.s_artnr, 0, 2)) == fbdept and to_int(substring(wf2.s_artnr, 2)) == 2), first=True)

                            wf3 = query(wf3_list, filters=(lambda wf3 :wf3.main_code == 1997 and to_int(substring(wf3.s_artnr, 0, 2)) == fbdept and to_int(substring(wf3.s_artnr, 2)) == 3), first=True)

                            wf4 = query(wf4_list, filters=(lambda wf4 :wf4.main_code == 1997 and to_int(substring(wf4.s_artnr, 0, 2)) == fbdept and to_int(substring(wf4.s_artnr, 2)) == 4), first=True)

                            wb1 = query(wb1_list, filters=(lambda wb1 :wb1.main_code == 1998 and to_int(substring(wb1.s_artnr, 0, 2)) == fbdept and to_int(substring(wb1.s_artnr, 2)) == 1), first=True)

                            wb2 = query(wb2_list, filters=(lambda wb2 :wb2.main_code == 1998 and to_int(substring(wb2.s_artnr, 0, 2)) == fbdept and to_int(substring(wb2.s_artnr, 2)) == 2), first=True)

                            wb3 = query(wb3_list, filters=(lambda wb3 :wb3.main_code == 1998 and to_int(substring(wb3.s_artnr, 0, 2)) == fbdept and to_int(substring(wb3.s_artnr, 2)) == 3), first=True)

                            wb4 = query(wb4_list, filters=(lambda wb4 :wb4.main_code == 1998 and to_int(substring(wb4.s_artnr, 0, 2)) == fbdept and to_int(substring(wb4.s_artnr, 2)) == 4), first=True)

                            wo1 = query(wo1_list, filters=(lambda wo1 :wb1.main_code == 1999 and to_int(substring(wo1.s_artnr, 0, 2)) == fbdept and to_int(substring(wo1.s_artnr, 2)) == 1), first=True)

                            wo2 = query(wo2_list, filters=(lambda wo2 :wo2.main_code == 1999 and to_int(substring(wo2.s_artnr, 0, 2)) == fbdept and to_int(substring(wo2.s_artnr, 2)) == 2), first=True)

                            wo3 = query(wo3_list, filters=(lambda wo3 :wo3.main_code == 1999 and to_int(substring(wo3.s_artnr, 0, 2)) == fbdept and to_int(substring(wo3.s_artnr, 2)) == 3), first=True)

                            wo4 = query(wo4_list, filters=(lambda wo4 :wo4.main_code == 1999 and to_int(substring(wo4.s_artnr, 0, 2)) == fbdept and to_int(substring(wo4.s_artnr, 2)) == 4), first=True)

                            if ytd_flag:
                                datum1 = jan1
                            else:
                                datum1 = from_date
                            mm = get_month(to_date)
                            yy = get_year(to_date)

                            for fbstat in db_session.query(Fbstat).filter(
                                    (Fbstat.datum >= datum1) &  (Fbstat.datum <= to_date) &  (Fbstat.departement == fbdept)).all():
                                d_flag = None != zinrstat and (get_month(zinrstat.datum) == get_month(to_date)) and (get_year(zinrstat.datum) == get_year(to_date))

                                if fbstat.datum == to_date:

                                    if wf1:
                                        wf1.tday = wf1.tday + fbstat.food_wpax[0] + fbstat.food_gpax[0]

                                    if wf2:
                                        wf2.tday = wf2.tday + fbstat.food_wpax[1] + fbstat.food_gpax[1]

                                    if wf3:
                                        wf3.tday = wf3.tday + fbstat.food_wpax[2] + fbstat.food_gpax[2]

                                    if wf4:
                                        wf4.tday = wf4.tday + fbstat.food_wpax[3] + fbstat.food_gpax[3]

                                    if wb1:
                                        wb1.tday = wb1.tday + fbstat.bev_wpax[0] + fbstat.bev_gpax[0]

                                    if wb2:
                                        wb2.tday = wb2.tday + fbstat.bev_wpax[1] + fbstat.bev_gpax[1]

                                    if wb3:
                                        wb3.tday = wb3.tday + fbstat.bev_wpax[2] + fbstat.bev_gpax[2]

                                    if wb4:
                                        wb4.tday = wb4.tday + fbstat.bev_wpax[3] + fbstat.bev_gpax[3]

                                    if wo1:
                                        wo1.tday = wo1.tday + fbstat.other_wpax[0] + fbstat.other_gpax[0]

                                    if wo2:
                                        wo2.tday = wo2.tday + fbstat.other_wpax[1] + fbstat.other_gpax[1]

                                    if wo3:
                                        wo3.tday = wo3.tday + fbstat.other_wpax[2] + fbstat.other_gpax[2]

                                    if wo4:
                                        wo4.tday = wo4.tday + fbstat.other_wpax[3] + fbstat.other_gpax[3]

                                if get_month(fbstat.datum) == mm:

                                    if wf1:
                                        wf1.saldo = wf1.saldo + fbstat.food_wpax[0] + fbstat.food_gpax[0]

                                    if wf2:
                                        wf2.saldo = wf2.saldo + fbstat.food_wpax[1] + fbstat.food_gpax[1]

                                    if wf3:
                                        wf3.saldo = wf3.saldo + fbstat.food_wpax[2] + fbstat.food_gpax[2]

                                    if wf4:
                                        wf4.saldo = wf4.saldo + fbstat.food_wpax[3] + fbstat.food_gpax[3]

                                    if wb1:
                                        wb1.saldo = wb1.saldo + fbstat.bev_wpax[0] + fbstat.bev_gpax[0]

                                    if wb2:
                                        wb2.saldo = wb2.saldo + fbstat.bev_wpax[1] + fbstat.bev_gpax[1]

                                    if wb3:
                                        wb3.saldo = wb3.saldo + fbstat.bev_wpax[2] + fbstat.bev_gpax[2]

                                    if wb4:
                                        wb4.saldo = wb4.saldo + fbstat.bev_wpax[3] + fbstat.bev_gpax[3]

                                    if wo1:
                                        wo1.saldo = wo1.saldo + fbstat.other_wpax[0] + fbstat.other_gpax[0]

                                    if wo2:
                                        wo2.saldo = wo2.saldo + fbstat.other_wpax[1] + fbstat.other_gpax[1]

                                    if wo3:
                                        wo3.saldo = wo3.saldo + fbstat.other_wpax[2] + fbstat.other_gpax[2]

                                    if wo4:
                                        wo4.saldo = wo4.saldo + fbstat.other_wpax[3] + fbstat.other_gpax[3]

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
                                    wf1.ytd_saldo = wf1.ytd_saldo + fbstat.food_wpax[0] + fbstat.food_gpax[0]

                                if wf2:
                                    wf2.ytd_saldo = wf2.ytd_saldo + fbstat.food_wpax[1] + fbstat.food_gpax[1]

                                if wf3:
                                    wf3.ytd_saldo = wf3.ytd_saldo + fbstat.food_wpax[2] + fbstat.food_gpax[2]

                                if wf4:
                                    wf4.ytd_saldo = wf4.ytd_saldo + fbstat.food_wpax[3] + fbstat.food_gpax[3]

                                if wb1:
                                    wb1.ytd_saldo = wb1.ytd_saldo + fbstat.bev_wpax[0] + fbstat.bev_gpax[0]

                                if wb2:
                                    wb2.ytd_saldo = wb2.ytd_saldo + fbstat.bev_wpax[1] + fbstat.bev_gpax[1]

                                if wb3:
                                    wb3.ytd_saldo = wb3.ytd_saldo + fbstat.bev_wpax[2] + fbstat.bev_gpax[2]

                                if wb4:
                                    wb4.ytd_saldo = wb4.ytd_saldo + fbstat.bev_wpax[3] + fbstat.bev_gpax[3]

                                if wo1:
                                    wo1.ytd_saldo = wo1.ytd_saldo + fbstat.other_wpax[0] + fbstat.other_gpax[0]

                                if wo2:
                                    wo2.ytd_saldo = wo2.ytd_saldo + fbstat.other_wpax[1] + fbstat.other_gpax[1]

                                if wo3:
                                    wo3.ytd_saldo = wo3.ytd_saldo + fbstat.other_wpax[2] + fbstat.other_gpax[2]

                                if wo4:
                                    wo4.ytd_saldo = wo4.ytd_saldo + fbstat.other_wpax[3] + fbstat.other_gpax[3]

    def fill_rmstat(rec_w1:int, key_word:str):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
        curr_date:date = None
        d_flag:bool = False
        dlmtd_flag:bool = False

                        w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

                        if w1.done:

                            return

                        if (get_day(to_date) == 31 and get_month(to_date) != 8 and get_month(to_date) != 1) or (get_day(to_date) == 30 and get_month(to_date) == 3) or (get_day(date_mdy(3, 1, get_year(to_date)) - 1) == 28 and get_month(to_date) == 3 and get_day(to_date) == 29):
                            w1.lm_today = 0
                        else:

                            if get_month(to_date) == 1:
                                curr_date = date_mdy(12, get_day(to_date) , get_year(to_date) - 1)
                            else:
                                curr_date = date_mdy(get_month(to_date) - 1, get_day(to_date) , get_year(to_date))

                            zinrstat = db_session.query(Zinrstat).filter(
                                    (Zinrstat.datum == curr_date) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).first()

                            if zinrstat:
                                w1.lm_today = zinrstat.zimmeranz

                        if ytd_flag:
                            datum1 = jan1
                        else:
                            datum1 = from_date

                        for zinrstat in db_session.query(Zinrstat).filter(
                                    (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= to_date) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).all():
                            d_flag = (get_month(zinrstat.datum) == get_month(to_date)) and (get_year(zinrstat.datum) == get_year(to_date))

                            if d_flag:
                                w1.mon_saldo[get_day(zinrstat.datum) - 1] = w1.mon_saldo[get_day(zinrstat.datum) - 1] + zinrstat.zimmeranz

                            if zinrstat.datum == to_date - 1:
                                w1.yesterday = w1.yesterday + zinrstat.zimmeranz

                            if zinrstat.datum == to_date:
                                w1.tday = w1.tday + zinrstat.zimmeranz

                            if zinrstat.datum < from_date:
                                w1.ytd_saldo = w1.ytd_saldo + zinrstat.zimmeranz
                            else:
                                w1.saldo = w1.saldo + zinrstat.zimmeranz

                                if ytd_flag:
                                    w1.ytd_saldo = w1.ytd_saldo + zinrstat.zimmeranz

                        if lytd_flag or lmtd_flag:

                            if lytd_flag:
                                datum1 = ljan1
                            else:
                                datum1 = lfrom_date

                            for zinrstat in db_session.query(Zinrstat).filter(
                                        (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= lto_date) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).all():

                                if zinrstat.datum < lfrom_date:
                                    w1.lytd_saldo = w1.lytd_saldo + zinrstat.zimmeranz
                                else:
                                    dlmtd_flag = (get_month(zinrstat.datum) == get_month(to_date)) and (get_year(zinrstat.datum) == get_year(to_date) - 1)

                                    if dlmtd_flag:
                                        w1.mon_lmtd[get_day(zinrstat.datum) - 1] = w1.mon_lmtd[get_day(zinrstat.datum) - 1] + zinrstat.zimmeranz
                                    w1.lastyr = w1.lastyr + zinrstat.zimmeranz

                                    if lytd_flag:
                                        w1.lytd_saldo = w1.lytd_saldo + zinrstat.zimmeranz

                        if pmtd_flag:

                            for zinrstat in db_session.query(Zinrstat).filter(
                                        (Zinrstat.datum >= pfrom_date) &  (Zinrstat.datum <= pto_date) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).all():
                                w1.lastmon = w1.lastmon + zinrstat.zimmeranz


                        if lytoday_flag:

                            zinrstat = db_session.query(Zinrstat).filter(
                                        (Zinrstat.datum == lytoday) &  (func.lower(Zinrstat.zinr) == (key_word).lower())).first()

                            if zinrstat:
                                w1.lytoday = zinrstat.zimmeranz
                        w1.done = True

    def fill_source(rec_w1:int, rec_w1:int, main_nr:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        datum1:date = None
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
        frate1:decimal = 0
                        W11 = W1

                        w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)

                        if w1.done:

                            return

                        w11 = query(w11_list, filters=(lambda w11 :w11.main_code == 812), first=True)

                        if w11 and w11.done:


                            if ytd_flag:
                                datum1 = jan1
                            else:
                                datum1 = from_date

                            for zinrstat in db_session.query(Zinrstat).filter(
                                        (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= to_date) &  (func.lower(Zinrstat.zinr) == "avrgLrate")).all():

                                if zinrstat.datum == to_date:
                                    w1.tday = w1.tday + zinrstat.logisumsatz

                                    if w11:
                                        w11.tday = w11.tday + zinrstat.argtumsatz / zinrstat.zimmeranz

                                if zinrstat.datum < from_date:
                                    w1.ytd_saldo = w1.ytd_saldo + zinrstat.logisumsatz / zinrstat.zimmeranz

                                    if w11:
                                        w11.ytd_saldo = w11.ytd_saldo + zinrstat.argtumsatz / zinrstat.zimmeranz
                                else:
                                    w1.saldo = w1.saldo + zinrstat.logisumsatz / zinrstat.zimmeranz

                                    if ytd_flag:
                                        w1.ytd_saldo = w1.ytd_saldo + zinrstat.logisumsatz / zinrstat.zimmeranz

                                    if w11:
                                        w11.saldo = w11.saldo + zinrstat.argtumsatz / zinrstat.zimmeranz

                                        if ytd_flag:
                                            w11.ytd_saldo = w11.ytd_saldo + zinrstat.argtumsatz / zinrstat.zimmeranz

                            if lytd_flag or lmtd_flag:

                                if lytd_flag:
                                    datum1 = ljan1
                                else:
                                    datum1 = lfrom_date

                                for zinrstat in db_session.query(Zinrstat).filter(
                                            (Zinrstat.datum >= datum1) &  (Zinrstat.datum <= lto_date) &  (func.lower(Zinrstat.zinr) == "avrgLrate")).all():

                                    if zinrstat.datum < lfrom_date:
                                        w1.lytd_saldo = w1.lytd_saldo + zinrstat.logisumsatz / zinrstat.zimmeranz

                                        if w11:
                                            w11.lytd_saldo = w11.lytd_saldo + zinrstat.argtumsatz / zinrstat.zimmeranz
                                    else:
                                        w1.lastyr = w1.lastyr + zinrstat.logisumsatz / zinrstat.zimmeranz

                                        if lytd_flag:
                                            w1.lytd_saldo = w1.lytd_saldo + zinrstat.logisumsatz / zinrstat.zimmeranz

                                        if w11:
                                            w11.lastyr = w11.lastyr + zinrstat.argtumsatz / zinrstat.zimmeranz

                                            if lytd_flag:
                                                w11.lytd_saldo = w11.lytd_saldo + zinrstat.argtumsatz / zinrstat.zimmeranz

                            if pmtd_flag:

                                for zinrstat in db_session.query(Zinrstat).filter(
                                            (Zinrstat.datum >= pfrom_date) &  (Zinrstat.datum <= pto_date) &  (func.lower(Zinrstat.zinr) == "avrgLrate")).all():
                                    w1.lastmon = w1.lastmon + zinrstat.logisumsatz / zinrstat.zimmeranz

                                    if w11:
                                        w11.lastmon = w11.lastmon + zinrstat.argtumsatz / zinrstat.zimmeranz


                            if lytoday_flag:

                                zinrstat = db_session.query(Zinrstat).filter(
                                            (Zinrstat.datum == lytoday) &  (func.lower(Zinrstat.zinr) == "avrgLrate")).first()

                                if zinrstat:
                                    w1.lytoday = zinrstat.logisumsatz / zinrstat.zimmeranz

                                    if w11:
                                        w11.lytoday = zinrstat.argtumsatz / zinrstat.zimmeranz
                            w1.done = True

                            if w11:
                                w11.done = True
                            Sourcebuff = Sources
                            Sourcebuffny = Sources
                            Genstatbuff = Genstat
                            W11 = W1
                            W12 = W1
                            W13 = W1
                            tmp_room_list.clear()

                            w1 = query(w1_list, filters=(lambda w1 :w1._recid == rec_w1), first=True)
                            source_nr = w1.artnr
                            njan1 = date_mdy(1, 1, get_year(to_date) + 1)
                            nmth1 = date_mdy(get_month(to_date) , 1, get_year(to_date) + 1)
                            mm = get_month(to_date)

                            if get_month(to_date) == 2 and get_day(to_date) == 29:
                                ny_currdate = date_mdy(get_month(to_date) , 28, get_year(to_date) + 1)
                            else:
                                ny_currdate = date_mdy(get_month(to_date) , get_day(to_date) , get_year(to_date) + 1)

                            sourcebuffny = db_session.query(Sourcebuffny).filter(
                                    (Sourcebuffny.datum == ny_currdate) &  (Sourcebuffny.source_code == source_nr)).first()

                            if sourcebuffny:

                                if main_nr == 9092:
                                    w1.ny_budget = sourcebuffny.budlogis

                                if main_nr == 9813:
                                    w1.ny_budget = sourcebuffny.budzimmeranz

                                if main_nr == 9814:
                                    w1.ny_budget = sourcebuffny.persanz

                            for sourcebuffny in db_session.query(Sourcebuffny).filter(
                                    (Sourcebuffny.datum >= njan1) &  (Sourcebuffny.datum <= ny_currdate) &  (Sourcebuffny.source_code == source_nr)).all():

                                if main_nr == 9092:
                                    w1.nytd_budget = w1.nytd_budget + sourcebuffny.budlogis

                                if main_nr == 9813:
                                    w1.nytd_budget = w1.nytd_budget + sourcebuffny.budzimmeranz

                                if main_nr == 9814:
                                    w1.nytd_budget = w1.nytd_budget + sourcebuffny.budpersanz

                            for sourcebuffny in db_session.query(Sourcebuffny).filter(
                                    (Sourcebuffny.datum >= nmth1) &  (Sourcebuffny.datum <= ny_currdate) &  (Sourcebuffny.source_code == source_nr)).all():

                                if main_nr == 9092:
                                    w1.nmtd_budget = w1.nmtd_budget + sourcebuffny.budlogis

                                if main_nr == 9813:
                                    w1.nmtd_budget = w1.nmtd_budget + sourcebuffny.budzimmeranz

                                if main_nr == 9814:
                                    w1.nmtd_budget = w1.nmtd_budget + sourcebuffny.budpersanz

                            sources = db_session.query(Sources).filter(
                                    (Sources.datum == to_date - 1) &  (Sources.source_code == source_nr)).first()

                            if sources:

                                if main_nr == 9092:
                                    w1.yesterday = sources.logis / frate

                                elif main_nr == 9813:
                                    w1.yesterday = sources.zimmeranz

                                elif main_nr == 9814:
                                    w1.yesterday = sources.persanz

                            if ytd_flag:
                                datum1 = jan1
                            else:
                                datum1 = from_date

                            for genstat in db_session.query(Genstat).filter(
                                        (Genstat.datum >= datum1) &  (Genstat.datum <= to_date) &  (Genstat.resstatus != 13) &  (Genstat.nationnr != 0) &  (Genstat.segmentcode != 0) &  (Genstat.source == source_nr) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
                                frate = 1
                                d_flag = (get_month(genstat.datum) == get_month(to_date))
                                AND (get_year(genstat.datum) = get_year(to_date))

                                if foreign_flag:
                                    find_exrate(genstat.datum)

                                    if exrate:
                                        frate = exrate.betrag

                                if genstat.datum == to_date:

                                    tmp_room = query(tmp_room_list, filters=(lambda tmp_room :tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                                    if not tmp_room:

                                        if main_nr == 9813:
                                            w1.tday = w1.tday + 1
                                        tmp_room = Tmp_room()
                                        tmp_room_list.append(tmp_room)

                                        tmp_room.gastnr = genstat.gastnr
                                        tmp_room.zinr = genstat.zinr
                                        tmp_room.flag = 1

                                    if main_nr == 9814:
                                        w1.tday = w1.tday + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                                    if main_nr == 9092:
                                        w1.tday = w1.tday + genstat.logis / frate

                                if get_month(genstat.datum) == mm:

                                    if main_nr == 9092:

                                        if d_flag:
                                            w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + genstat.logis / frate
                                        w1.saldo = w1.saldo + genstat.logis / frate

                                    if main_nr == 9814:

                                        if d_flag:
                                            w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                                        w1.saldo = w1.saldo + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                                    if main_nr == 9813:

                                        if d_flag:
                                            w1.mon_saldo[get_day(genstat.datum) - 1] = w1.mon_saldo[get_day(genstat.datum) - 1] + 1
                                        w1.saldo = w1.saldo + 1

                                if main_nr == 9092:
                                    w1.ytd_saldo = w1.ytd_saldo + genstat.logis / frate

                                if main_nr == 9814:
                                    w1.ytd_saldo = w1.ytd_saldo + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                                if main_nr == 9813:
                                    w1.ytd_saldo = w1.ytd_saldo + 1
                            tmp_room_list.clear()

                            if lytd_flag or lmtd_flag:
                                mm = get_month(lto_date)

                                if lytd_flag:
                                    datum1 = ljan1
                                else:
                                    datum1 = lfrom_date

                                for genstat in db_session.query(Genstat).filter(
                                            (Genstat.datum >= datum1) &  (Genstat.datum <= lto_date) &  (Genstat.resstatus != 13) &  (Genstat.nationnr != 0) &  (Genstat.segmentcode != 0) &  (Genstat.source == source_nr) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
                                    dlmtd_flag = (get_month(genstat.datum) == get_month(lto_date)) and (get_year(genstat.datum) == get_year(lto_date))

                                    if foreign_flag:
                                        find_exrate(genstat.datum)

                                        if exrate:
                                            frate = exrate.betrag

                                    if genstat.datum == lto_date:

                                        tmp_room = query(tmp_room_list, filters=(lambda tmp_room :tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                                        if not tmp_room:

                                            if main_nr == 9813:
                                                w1.lytoday = w1.lytoday + 1
                                            tmp_room = Tmp_room()
                                            tmp_room_list.append(tmp_room)

                                            tmp_room.gastnr = genstat.gastnr
                                            tmp_room.zinr = genstat.zinr
                                            tmp_room.flag = 1

                                        if main_nr == 9814:
                                            w1.lytoday = w1.lytoday + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                                        if main_nr == 9092:
                                            w1.lytoday = w1.lytoday + genstat.logis / frate

                                    if get_month(genstat.datum) == mm:

                                        if main_nr == 9092:
                                            w1.lastyr = w1.lastyr + genstat.logis / frate

                                        if main_nr == 9814:
                                            w1.lastyr = w1.lastyr + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                                        if main_nr == 9813:
                                            w1.lastyr = w1.lastyr + 1

                                    if main_nr == 9092:
                                        w1.lytd_saldo = w1.lytd_saldo + genstat.logis / frate

                                    if main_nr == 9814:
                                        w1.lytd_saldo = w1.lytd_saldo + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                                    if main_nr == 9813:
                                        w1.lytd_saldo = w1.lytd_saldo + 1

                            if pmtd_flag:

                                for genstat in db_session.query(Genstat).filter(
                                            (Genstat.datum >= pfrom_date) &  (Genstat.datum <= pto_date) &  (Genstat.resstatus != 13) &  (Genstat.nationnr != 0) &  (Genstat.segmentcode != 0) &  (Genstat.source == source_nr) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():

                                    if foreign_flag:
                                        find_exrate(genstat.datum)

                                        if exrate:
                                            frate = exrate.betrag

                                    if main_nr == 9092:
                                        w1.lastmon = w1.lastmon + genstat.logis / frate

                                    if main_nr == 9814:
                                        w1.lastmon = w1.lastmon + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                                    if main_nr == 9813:
                                        w1.lastmon = w1.lastmon + 1


    def fill_value1(recid1_w1:int, recid2_w1:int, val_sign:int):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        sign1:int = 0
        texte:str = ""
        n:int = 0
                            Parent = W1
                            Child = W1
                            Curr_child = W1
                            Curr_w2 = W2

                            parent = query(parent_list, filters=(lambda parent :parent._recid == recid1_w1), first=True)

                            child = query(child_list, filters=(lambda child :child._recid == recid2_w1), first=True)
                            parent.tday = parent.tday + val_sign * child.tday
                            parent.tbudget = parent.tbudget + val_sign * child.tbudget
                            parent.saldo = parent.saldo + val_sign * child.saldo
                            parent.budget = parent.budget + val_sign * child.budget
                            parent.lytoday = parent.lytoday + val_sign * child.lytoday
                            parent.lastmon = parent.lastmon + val_sign * child.lastmon
                            parent.lm_budget = parent.lm_budget + val_sign * child.lm_budget
                            parent.lastyr = parent.lastyr + val_sign * child.lastyr
                            parent.ly_budget = parent.ly_budget + val_sign * child.ly_budget
                            parent.ytd_saldo = parent.ytd_saldo + val_sign * child.ytd_saldo
                            parent.ytd_budget = parent.ytd_budget + val_sign * child.ytd_budget
                            parent.lytd_saldo = parent.lytd_saldo + val_sign * child.lytd_saldo
                            parent.lytd_budget = parent.lytd_budget + val_sign * child.lytd_budget

    def convert_varname(str:str):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        prev_param:str = ""
        k:int = 0
        j:int = 0
        curr_row:int = 0
        curr_col:int = 0
        htl_no:str = ""
        cell_value:str = ""
        chcol:[str] = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        dayname:str = ""
        crow = 0
        ccol = 0
        loop_str:int = 0
        loop_col:int = 0
        found:bool = False
        str_col:str = ""
        str_row:str = ""

        def generate_inner_output():
            return crow, ccol

                        paramtext = db_session.query(Paramtext).filter(
                                (Paramtext.txtnr == 243)).first()

                        if paramtext and paramtext.ptexte != "":
                            htl_no = decode_string(paramtext.ptexte)
                        OS_DELETE VALUE ("/usr1/vhp/tmp/outputFO__" + htl_no + ".txt")
                        OUTPUT STREAM s1 TO VALUE ("/usr1/vhp/tmp/outputFO__" + htl_no + ".txt") APPEND UNBUFFERED

                        for parameters in db_session.query(Parameters).filter(
                                (func.lower(Parameters.progname) == "FO_macro") &  (Parameters.SECTION == to_string(briefnr))).all():

                            if prev_param != parameters.varname:
                                curr_row, curr_col = convert_varname(parameters.varname)
                                prev_param = parameters.varname

                                if parameters.vtype != 0:

                                    w1 = query(w1_list, filters=(lambda w1 :w1.varname == parameters.vstring), first=True)

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

                                    if parameters.vstring.lower()  == "$exrate":
                                        cell_value = ch

                                    elif parameters.vstring.lower()  == "$weekday":
                                        cell_value = dayname[get_weekday(to_date) - 1]

                                    elif parameters.vstring.lower()  == "$today":
                                        cell_value = to_string(get_day(get_current_date()) , "99") + "/" + to_string(get_month(get_current_date()) , "99") + "/" + to_string(get_year(get_current_date()) , "9999")

                                    elif parameters.vstring.lower()  == "$to_date":
                                        cell_value = to_string(get_day(to_date) , "99") + "/" + to_string(get_month(to_date) , "99") + "/" + to_string(get_year(to_date) , "9999")

                                    elif parameters.vstring.lower()  == "$month_str":
                                        cell_value = month_str[get_month(to_date) - 1]

                                    elif parameters.vstring.lower()  == "$to_date1":
                                        cell_value = to_string(get_day(to_date) , "99") + "-" + month_str[get_month(to_date) - 1] + "-" + to_string(get_year(to_date) , "9999")
                                stream_list = Stream_list()
                                stream_list_list.append(stream_list)

                                stream_list.crow = curr_row
                                stream_list.ccol = curr_col
                                stream_list.cval = cell_value

                        for stream_list in query(stream_list_list):

                            if stream_list.cval != "":
                                else:
                                OUTPUT STREAM s1 CLOSE
                            OS_COMMAND SILENT VALUE ("php /usr1/vhp/php_script/write_sheet.php /usr1/vhp/tmp/outputFO__" + htl_no + ".txt " + link)
                                for loop_str in range(1,len(str)  + 1) :
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

    def get_columnno(last_column:str):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        ind = 0
        i:int = 0
        ind1:int = 0
        ind2:int = 0

        def generate_inner_output():
            return ind

                                if len(last_column) == 2:
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

    def convert_diff(v1:decimal, v2:decimal):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        s = ""
        balance:decimal = 0
        b:decimal = 0
        rs:str = ""

        def generate_inner_output():
            return s

                                if v2 == 0:
                                    rs = "0.00"
                                else:
                                    balance = (v1 - v2) / v2 * 100

                                    if balance >= 0:
                                        b = balance
                                    else:
                                        b = - balance

                                    if b <= 999:
                                        rs = to_string(balance, "->>9.99")

                                    elif b <= 9999:
                                        rs = to_string(balance, "->>>9.9")
                                    else:
                                        rs = to_string(balance, "->>>>>>>>>9")
                                s = rs


        return generate_inner_output()

    def decode_string(in_str:str):

        nonlocal msg_str, error_nr, lfr_date, exrate_betrag, frate, prog_error, ch, month_str, lvcarea, segmentstat, arrangement, res_line, bill_line, zimmer, zinrstat, zkstat, h_umsatz, segment, uebertrag, genstat, artikel, h_artikel, wgrpdep, umsatz, budget, exrate, h_cost, h_journal, htparam, h_bill_line, h_bill, bill, queasy, fbstat, sources, paramtext, parameters
        nonlocal segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2


        nonlocal w1, shift_list, w2, tmp_room, t_list, t_rechnr, temp_rechnr, fbstat_dept, stream_list, segmbuff, curr_child, ww1, ww2, wdu, hbuff, w11, w12, w13, resbuff, tbuff, w1a, ubuff, buff_umsatz, w753, w754, w755, segmbuffny, wlos, buff, art_buff, wspc, btemp_rechnr, bh_artikel, bh_bill_line, wf1, wf2, wf3, wf4, wb1, wb2, wb3, wb4, wo1, wo2, wo3, wo4, sourcebuff, sourcebuffny, genstatbuff, parent, child, curr_w2
        nonlocal w1_list, shift_list_list, w2_list, tmp_room_list, t_list_list, t_rechnr_list, temp_rechnr_list, fbstat_dept_list, stream_list_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return out_str
                                s = in_str
                                j = ord(substring(s, 0, 1)) - 70
                                len_ = len(in_str) - 1
                                s = substring(in_str, 1, len_)
                                for len_ in range(1,len(s)  + 1) :
                                    out_str = out_str + chr (ord(substring(s, len_ - 1, 1)) - j)


        return generate_inner_output()


    fill_value()
    find_exrate(to_date)
    exrate_betrag = 0

    if exrate:
        exrate_betrag = exrate.betrag
    ch = trim(to_string(exrate_betrag, ">>>,>>9.99"))
    lfr_date = from_date - 1

    return generate_output()