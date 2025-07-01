#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Segmentstat, Htparam, Zimmer, Zimkateg, Zkstat, Zinrstat, H_umsatz, Segment, Uebertrag, Artikel, H_artikel, Umsatz, Budget

w1_list, W1 = create_model("W1", {"nr":int, "varname":string, "main_code":int, "artnr":int, "s_artnr":string, "dept":int, "grpflag":int, "done":bool, "bezeich":string, "int_flag":bool, "tday":Decimal, "saldo":Decimal, "lastmon":Decimal, "lastyr":Decimal, "lytoday":Decimal, "ytd_saldo":Decimal, "lytd_saldo":Decimal, "tbudget":Decimal, "budget":Decimal, "lm_budget":Decimal, "ly_budget":Decimal, "ytd_budget":Decimal, "lytd_budget":Decimal})
w2_list, W2 = create_model("W2", {"val_sign":int, "nr1":int, "nr2":int}, {"val_sign": 1})

def fo_parexcelbl(pvilanguage:int, ytd_flag:bool, jan1:date, ljan1:date, lfrom_date:date, lto_date:date, from_date:date, to_date:date, start_date:date, lytd_flag:bool, lmtd_flag:bool, pmtd_flag:bool, pfrom_date:date, pto_date:date, lytoday_flag:bool, lytoday:date, foreign_flag:bool, budget_flag:bool, w1_list:[W1], w2_list:[W2]):

    prepare_cache ([Segmentstat, Htparam, Zimkateg, Zkstat, Zinrstat, H_umsatz, Segment, Uebertrag, Artikel, Umsatz, Budget])

    error_nr = 0
    msg_str = ""
    lvcarea:string = "fo-parexcel"
    frate:Decimal = 1
    prog_error:bool = False
    serv_vat:bool = False
    price_decimal:int = 0
    segmentstat = htparam = zimmer = zimkateg = zkstat = zinrstat = h_umsatz = segment = uebertrag = artikel = h_artikel = umsatz = budget = None

    w1 = w2 = segmbuff = curr_child = ww1 = ww2 = w11 = w12 = w13 = w11 = w12 = w11 = tbuff = w1a = w11 = w12 = w13 = w22 = w11 = w12 = w11 = w12 = w11 = w12 = w11 = w22 = w753 = w754 = w755 = w11 = w11 = w11 = w11 = w12 = w13 = w756 = w757 = w758 = w11 = w12 = w13 = parent = child = curr_child = curr_w2 = None

    Segmbuff = create_buffer("Segmbuff",Segmentstat)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

        return {"error_nr": error_nr, "msg_str": msg_str, "w1": w1_list, "w2": w2_list}

    def fill_value():

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

        mm:int = 0
        i:int = 0
        k:int = 0
        n:int = 0
        val_sign:int = 0
        Curr_child = W1
        curr_child_list = w1_list
        Ww1 = W1
        ww1_list = w1_list
        Ww2 = W1
        ww2_list = w1_list

        for ww1 in query(ww1_list, filters=(lambda ww1: ww1.grpflag == 0)):

            ww2 = query(ww2_list, filters=(lambda ww2: ww2.varname == ww1.varname and ww1._recid != ww2._recid), first=True)

            if ww2:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Duplicate name found : ", lvcarea, "") + ww2.varname
                error_nr = -1

                return

        for ww1 in query(ww1_list, filters=(lambda ww1: ww1.grpflag == 0)):

            ww2 = query(ww2_list, filters=(lambda ww2: ww2.varname == ww1.varname and ww1._recid != ww2._recid), first=True)

            if ww2:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Duplicate name found : ", lvcarea, "") + ww2.varname
                error_nr = -1

                return

            elif ww1.main_code == 288:
                fill_totroom(ww1._recid)

            if ww1.main_code == 805:
                fill_rmavail(ww1._recid)

            elif ww1.main_code == 122:
                fill_ooo(ww1._recid, "ooo")

            elif ww1.main_code == 752:
                fill_ooo(ww1._recid, "oos")

            elif ww1.main_code == 192:
                fill_cover(ww1._recid)

            elif ww1.main_code == 197:
                fill_cover(ww1._recid)

            elif ww1.main_code == 552:
                fill_cover(ww1._recid)

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
                fill_arrdep(ww1._recid, "departure", 0, 9190, 0)

            elif ww1.main_code == 191:
                fill_arrdep(ww1._recid, "VIP", 0, 191, 0, 0)

            elif ww1.main_code == 193:
                fill_arrdep(ww1._recid, "NewRes", 193, 0, 0)

            elif ww1.main_code == 194:
                fill_arrdep(ww1._recid, "CancRes", 194, 0, 0)

            elif ww1.main_code == 7194:
                fill_canc_room_night(ww1._recid)

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
                fill_rmocc(ww1._recid)

                if error_nr != 0:

                    return

            elif ww1.main_code == 182:
                fill_gledger(ww1._recid)

                if error_nr != 0:

                    return

            elif ww1.main_code == 183:
                fill_comprooms(ww1._recid)

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

            elif ww1.main_code == 92 or ww1.main_code == 813 or ww1.main_code == 814:
                fill_segment(ww1._recid, ww1.main_code)

            elif ww1.main_code == 179:
                fill_rmcatstat(ww1._recid, ww1.main_code)

            elif ww1.main_code == 180 or ww1.main_code == 181 or ww1.main_code == 800:
                fill_zinrstat(ww1._recid, ww1.main_code)

        for w1 in query(w1_list, filters=(lambda w1: w1.grpflag >= 1 and w1.grpflag != 9), sort_by=[("nr",False)]):

            for w2 in query(w2_list, filters=(lambda w2: w2.nr1 == w1.nr)):

                curr_child = query(curr_child_list, filters=(lambda curr_child: curr_child.nr == w2.nr2), first=True)
                fill_value1(w1._recid, curr_child._recid, w2.val_sign)


    def fill_totroom(rec_w1:int):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

        datum:date = None
        datum1:date = None
        datum2:date = None
        anz:int = 0

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return
        anz = 0

        for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
            anz = anz + 1

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date
        for datum in date_range(datum1,to_date) :

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

                if start_date != None:

                    if (datum >= start_date):
                        w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(anz)
                else:
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(anz)
        w1.done = True


    def fill_rmavail(rec_w1:int):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

        datum1:date = None
        datum2:date = None

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():

            for zkstat in db_session.query(Zkstat).filter(
                     (Zkstat.datum >= datum1) & (Zkstat.datum <= to_date) & (Zkstat.zikatnr == zimkateg.zikatnr)).order_by(Zkstat._recid).all():

                if zkstat.datum == to_date:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(zkstat.anz100)

                if zkstat.datum < from_date:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zkstat.anz100)
                else:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(zkstat.anz100)

                    if ytd_flag:
                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(zkstat.anz100)

            if lytd_flag or lmtd_flag:

                if lytd_flag:
                    datum2 = ljan1
                else:
                    datum2 = lfrom_date

                for zkstat in db_session.query(Zkstat).filter(
                         (Zkstat.datum >= datum2) & (Zkstat.datum <= lto_date) & (Zkstat.zikatnr == zimkateg.zikatnr)).order_by(Zkstat._recid).all():

                    if zkstat.datum < lfrom_date:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zkstat.anz100)
                    else:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(zkstat.anz100)

                        if lytd_flag:
                            w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(zkstat.anz100)

            if pmtd_flag:

                for zkstat in db_session.query(Zkstat).filter(
                         (Zkstat.datum >= pfrom_date) & (Zkstat.datum <= pto_date) & (Zkstat.zikatnr == zimkateg.zikatnr)).order_by(Zkstat._recid).all():
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(zkstat.anz100)

        w1.done = True


    def fill_ooo(rec_w1:int, key_word:string):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

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

        w1.done = True


    def fill_cover(rec_w1:int):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

        datum1:date = None
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

        w11 = query(w11_list, filters=(lambda w11: w11.main_code == 552 and w11.dept == w1.dept), first=True)

        w12 = query(w12_list, filters=(lambda w12: w12.main_code == 192 and w12.dept == w1.dept), first=True)

        w13 = query(w13_list, filters=(lambda w13: w13.main_code == 197 and w13.dept == w1.dept), first=True)

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for h_umsatz in db_session.query(H_umsatz).filter(
                 (H_umsatz.datum >= datum1) & (H_umsatz.datum <= to_date) & (H_umsatz.artnr == 0) & (H_umsatz.departement == w1.dept) & (H_umsatz.betriebsnr == w1.dept)).order_by(H_umsatz._recid).all():

            if h_umsatz.datum == to_date and w11:
                w11.tday =  to_decimal(w11.tday) + to_decimal(h_umsatz.anzahl)

            if h_umsatz.datum == to_date and w12:
                w12.tday =  to_decimal(w12.tday) + to_decimal(h_umsatz.betrag)

            if h_umsatz.datum == to_date and w13:
                w13.tday =  to_decimal(w13.tday) + to_decimal(h_umsatz.nettobetrag)

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


        if w11:
            w11.done = True

        if w12:
            w12.done = True

        if w13:
            w13.done = True


    def fill_arrdep(rec_w1:int, key_word:string, number1:int, number2:int, number3:int):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

        datum1:date = None
        W11 = W1
        w11_list = w1_list
        W12 = W1
        w12_list = w1_list

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return
        pass
        pass

        if number1 != 0:

            w11 = query(w11_list, filters=(lambda w11: w11.main_code == number1 and not w11.done), first=True)

        if number2 != 0:

            w12 = query(w12_list, filters=(lambda w12: w12.main_code == number2 and not w12.done), first=True)

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.datum >= datum1) & (Zinrstat.datum <= to_date) & (Zinrstat.zinr == (key_word).lower())).order_by(Zinrstat._recid).all():

            if zinrstat.datum == to_date:

                if w11:
                    w11.tday =  to_decimal(w11.tday) + to_decimal(zinrstat.zimmeranz)

                if w12:
                    w12.tday =  to_decimal(w12.tday) + to_decimal(zinrstat.personen)

            if zinrstat.datum < from_date:

                if w11:
                    w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(zinrstat.zimmeranz)

                if w12:
                    w12.ytd_saldo =  to_decimal(w12.ytd_saldo) + to_decimal(zinrstat.personen)
            else:

                if w11:
                    w11.saldo =  to_decimal(w11.saldo) + to_decimal(zinrstat.zimmeranz)

                if ytd_flag and w11:
                    w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(zinrstat.zimmeranz)

                if w12:
                    w12.saldo =  to_decimal(w12.saldo) + to_decimal(zinrstat.personen)

                if ytd_flag and w12:
                    w12.ytd_saldo =  to_decimal(w12.ytd_saldo) + to_decimal(zinrstat.personen)

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
                else:

                    if w11:
                        w11.lastyr =  to_decimal(w11.lastyr) + to_decimal(zinrstat.zimmeranz)

                    if lytd_flag and w11:
                        w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(zinrstat.zimmeranz)

                    if w12:
                        w12.lastyr =  to_decimal(w12.lastyr) + to_decimal(zinrstat.personen)

                    if lytd_flag and w12:
                        w12.lytd_saldo =  to_decimal(w12.lytd_saldo) + to_decimal(zinrstat.personen)

        if pmtd_flag:

            for zinrstat in db_session.query(Zinrstat).filter(
                         (Zinrstat.datum >= pfrom_date) & (Zinrstat.datum <= pto_date) & (Zinrstat.zinr == (key_word).lower())).order_by(Zinrstat._recid).all():

                if w11:
                    w11.lastmon =  to_decimal(w11.lastmon) + to_decimal(zinrstat.zimmeranz)

                if w12:
                    w12.lastmon =  to_decimal(w12.lastmon) + to_decimal(zinrstat.personen)


        if w11:
            w11.done = True

        if w12:
            w12.done = True


    def fill_avrgstay(rec_w1:int, key_word:string, number1:int):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

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
        w11.done = True
        tbuff_list.remove(tbuff)


    def fill_rmocc(rec_w1:int):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

        curr_date:date = None
        datum1:date = None
        datum2:date = None
        W1a = W1
        w1a_list = w1_list
        W11 = W1
        w11_list = w1_list
        W12 = W1
        w12_list = w1_list
        W13 = W1
        w13_list = w1_list
        W22 = W1
        w22_list = w1_list

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        w1a = query(w1a_list, filters=(lambda w1a: w1a.main_code == 810), first=True)

        if w1a and w1a.done:
            pass

        w22 = query(w22_list, filters=(lambda w22: w22.main_code == 183), first=True)

        if w22 and w22.done:
            pass

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date
        lytoday_flag = (lytd_flag or lmtd_flag) and (get_month(to_date) != 2 or get_day(to_date) != 29)

        for segment in db_session.query(Segment).order_by(Segment._recid).all():

            w11 = query(w11_list, filters=(lambda w11: w11.main_code == 92 and w11.artnr == segment.segmentcode), first=True)

            if w11 and w11.done:
                pass

            w12 = query(w12_list, filters=(lambda w12: w12.main_code == 813 and w12.artnr == segment.segmentcode), first=True)

            if w12 and w12.done:
                pass

            w13 = query(w13_list, filters=(lambda w13: w13.main_code == 814 and w13.artnr == segment.segmentcode), first=True)

            if w13 and w13.done:
                pass

            for segmentstat in db_session.query(Segmentstat).filter(
                     (Segmentstat.datum >= datum1) & (Segmentstat.datum <= to_date) & (Segmentstat.segmentcode == segment.segmentcode)).order_by(Segmentstat._recid).all():

                if foreign_flag:
                    find_exrate(segmentstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)

                if segmentstat.datum == to_date:
                    pass

                    if lytoday_flag:
                        lytoday = to_date - timedelta(days=365)

                        segmbuff = get_cache (Segmentstat, {"datum": [(eq, lytoday)],"segmentcode": [(eq, segment.segmentcode)]})
                    w1.tday =  to_decimal(w1.tday) + to_decimal(segmentstat.zimmeranz)
                    w1.tbudget =  to_decimal(w1.tbudget) + to_decimal(segmentstat.budzimmeranz)

                    if segmbuff:
                        w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(segmbuff.zimmeranz)

                    if w22 and segment.betriebsnr == 0:
                        w22.tday =  to_decimal(w22.tday) + to_decimal(segmentstat.betriebsnr)

                        if segmbuff:
                            w22.lytoday =  to_decimal(w22.lytoday) + to_decimal(segmbuff.betriebsnr)

                    if w1a:
                        w1a.tday =  to_decimal(w1a.tday) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w1a.tbudget =  to_decimal(w1a.tbudget) + to_decimal(segmentstat.budpersanz)

                        if segmbuff:
                            w1a.lytoday =  to_decimal(w1a.lytoday) + to_decimal(segmbuff.persanz) + to_decimal(segmbuff.kind1) + to_decimal(segmbuff.kind2) + to_decimal(segmbuff.gratis)

                    if w11:
                        w11.tday =  to_decimal(w11.tday) + to_decimal(segmentstat.logis) / to_decimal(frate)
                        w11.tbudget =  to_decimal(w11.tbudget) + to_decimal(segmentstat.budlogis)

                        if segmbuff:
                            w11.lytoday =  to_decimal(w11.lytoday) + to_decimal(segmbuff.logis) / to_decimal(frate)

                    if w12:
                        w12.tday =  to_decimal(w12.tday) + to_decimal(segmentstat.zimmeranz)
                        w12.tbudget =  to_decimal(w12.tbudget) + to_decimal(segmentstat.budzimmeranz)

                        if segmbuff:
                            w12.lytoday =  to_decimal(w12.lytoday) + to_decimal(segmbuff.zimmeranz)

                    if w13:
                        w13.tday =  to_decimal(w13.tday) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w13.tbudget =  to_decimal(w13.tbudget) + to_decimal(segmentstat.budpersanz)

                        if segmbuff:
                            w13.lytoday =  to_decimal(w13.lytoday) + to_decimal(segmbuff.persanz) + to_decimal(segmbuff.kind1) + to_decimal(segmbuff.kind2) + to_decimal(segmbuff.gratis)

                if segmentstat.datum < from_date:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(segmentstat.zimmeranz)
                    w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(segmentstat.budzimmeranz)

                    if w22 and segment.betriebsnr == 0:
                        w22.ytd_saldo =  to_decimal(w22.ytd_saldo) + to_decimal(segmentstat.betriebsnr)

                    if w1a:
                        w1a.ytd_saldo =  to_decimal(w1a.ytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w1a.ytd_budget =  to_decimal(w1a.ytd_budget) + to_decimal(segmentstat.budpersanz)

                    if w11:
                        w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(segmentstat.logis) / to_decimal(frate)
                        w11.ytd_budget =  to_decimal(w11.ytd_budget) + to_decimal(segmentstat.budlogis)

                    if w12:
                        w12.ytd_saldo =  to_decimal(w12.ytd_saldo) + to_decimal(segmentstat.zimmeranz)
                        w12.ytd_budget =  to_decimal(w12.ytd_budget) + to_decimal(segmentstat.budzimmeranz)

                    if w13:
                        w13.ytd_saldo =  to_decimal(w13.ytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w13.ytd_budget =  to_decimal(w13.ytd_budget) + to_decimal(segmentstat.budpersanz)
                else:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(segmentstat.zimmeranz)
                    w1.budget =  to_decimal(w1.budget) + to_decimal(segmentstat.budzimmeranz)

                    if ytd_flag:
                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(segmentstat.zimmeranz)
                        w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(segmentstat.budzimmeranz)

                    if w22 and segment.betriebsnr == 0:
                        w22.saldo =  to_decimal(w22.saldo) + to_decimal(segmentstat.betriebsnr)

                        if ytd_flag:
                            w22.ytd_saldo =  to_decimal(w22.ytd_saldo) + to_decimal(segmentstat.betriebsnr)

                    if w1a:
                        w1a.saldo =  to_decimal(w1a.saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w1a.budget =  to_decimal(w1a.budget) + to_decimal(segmentstat.budpersanz)

                        if ytd_flag:
                            w1a.ytd_saldo =  to_decimal(w1a.ytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                            w1a.ytd_budget =  to_decimal(w1a.ytd_budget) + to_decimal(segmentstat.budpersanz)

                    if w11:
                        w11.saldo =  to_decimal(w11.saldo) + to_decimal(segmentstat.logis) / to_decimal(frate)
                        w11.budget =  to_decimal(w11.budget) + to_decimal(segmentstat.budlogis)

                        if ytd_flag:
                            w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(segmentstat.logis) / to_decimal(frate)
                            w11.ytd_budget =  to_decimal(w11.ytd_budget) + to_decimal(segmentstat.budlogis)

                    if w12:
                        w12.saldo =  to_decimal(w12.saldo) + to_decimal(segmentstat.zimmeranz)
                        w12.budget =  to_decimal(w12.budget) + to_decimal(segmentstat.budzimmeranz)

                        if ytd_flag:
                            w12.ytd_saldo =  to_decimal(w12.ytd_saldo) + to_decimal(segmentstat.zimmeranz)
                            w12.ytd_budget =  to_decimal(w12.ytd_budget) + to_decimal(segmentstat.budzimmeranz)

                    if w13:
                        w13.saldo =  to_decimal(w13.saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w13.budget =  to_decimal(w13.budget) + to_decimal(segmentstat.budpersanz)

                        if ytd_flag:
                            w13.ytd_saldo =  to_decimal(w13.ytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                            w13.ytd_budget =  to_decimal(w13.ytd_budget) + to_decimal(segmentstat.budpersanz)

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
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(segmentstat.zimmeranz)
                        w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(segmentstat.budzimmeranz)

                        if w22 and segment.betriebsnr == 0:
                            w22.lytd_saldo =  to_decimal(w22.lytd_saldo) + to_decimal(segmentstat.betriebsnr)

                        if w1a:
                            w1a.lytd_saldo =  to_decimal(w1a.lytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                            w1a.lytd_budget =  to_decimal(w1a.lytd_budget) + to_decimal(segmentstat.budpersanz)

                        if w11:
                            w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(segmentstat.logis) / to_decimal(frate)
                            w11.lytd_budget =  to_decimal(w11.lytd_budget) + to_decimal(segmentstat.budlogis)

                        if w12:
                            w12.lytd_saldo =  to_decimal(w12.lytd_saldo) + to_decimal(segmentstat.zimmeranz)
                            w12.lytd_budget =  to_decimal(w12.lytd_budget) + to_decimal(segmentstat.budzimmeranz)

                        if w13:
                            w13.lytd_saldo =  to_decimal(w13.lytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                            w13.lytd_budget =  to_decimal(w13.lytd_budget) + to_decimal(segmentstat.budpersanz)
                    else:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(segmentstat.zimmeranz)

                        if lytd_flag:
                            w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(segmentstat.zimmeranz)
                        w1.ly_budget =  to_decimal(w1.ly_budget) + to_decimal(segmentstat.budzimmeranz)

                        if lytd_flag:
                            w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(segmentstat.budzimmeranz)

                        if w22 and segment.betriebsnr == 0:
                            w22.lastyr =  to_decimal(w22.lastyr) + to_decimal(segmentstat.betriebsnr)

                            if lytd_flag:
                                w22.lytd_saldo =  to_decimal(w22.lytd_saldo) + to_decimal(segmentstat.betriebsnr)

                        if w1a:
                            w1a.lastyr =  to_decimal(w1a.lastyr) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                            w1a.ly_budget =  to_decimal(w1a.ly_budget) + to_decimal(segmentstat.budpersanz)

                            if lytd_flag:
                                w1a.lytd_saldo =  to_decimal(w1a.lytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                                w1a.lytd_budget =  to_decimal(w1a.lytd_budget) + to_decimal(segmentstat.budpersanz)

                        if w11:
                            w11.lastyr =  to_decimal(w11.lastyr) + to_decimal(segmentstat.logis) / to_decimal(frate)
                            w11.ly_budget =  to_decimal(w11.ly_budget) + to_decimal(segmentstat.budlogis)

                            if lytd_flag:
                                w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(segmentstat.logis) / to_decimal(frate)
                                w11.lytd_budget =  to_decimal(w11.lytd_budget) + to_decimal(segmentstat.budlogis)

                        if w12:
                            w12.lastyr =  to_decimal(w12.lastyr) + to_decimal(segmentstat.zimmeranz)
                            w12.ly_budget =  to_decimal(w12.ly_budget) + to_decimal(segmentstat.budzimmeranz)

                            if lytd_flag:
                                w12.lytd_saldo =  to_decimal(w12.lytd_saldo) + to_decimal(segmentstat.zimmeranz)
                                w12.lytd_budget =  to_decimal(w12.lytd_budget) + to_decimal(segmentstat.budzimmeranz)

                        if w13:
                            w13.lastyr =  to_decimal(w13.lastyr) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                            w13.ly_budget =  to_decimal(w13.ly_budget) + to_decimal(segmentstat.budpersanz)

                            if lytd_flag:
                                w13.lytd_saldo =  to_decimal(w13.lytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                                w13.lytd_budget =  to_decimal(w13.lytd_budget) + to_decimal(segmentstat.budpersanz)

            if pmtd_flag:

                for segmentstat in db_session.query(Segmentstat).filter(
                         (Segmentstat.datum >= pfrom_date) & (Segmentstat.datum <= pto_date) & (Segmentstat.segmentcode == segment.segmentcode)).order_by(Segmentstat._recid).all():

                    if foreign_flag:
                        find_exrate(segmentstat.datum)

                        if exrate:
                            frate =  to_decimal(exrate.betrag)
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(segmentstat.zimmeranz)
                    w1.lm_budget =  to_decimal(w1.lm_budget) + to_decimal(segmentstat.budzimmeranz)

                    if w22 and segment.betriebsnr == 0:
                        w22.lastmon =  to_decimal(w22.lastmon) + to_decimal(segmentstat.betriebsnr)

                    if w1a:
                        w1a.lastmon =  to_decimal(w1a.lastmon) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w1a.lm_budget =  to_decimal(w1a.lm_budget) + to_decimal(segmentstat.budpersanz)

                    if w11:
                        w11.lastmon =  to_decimal(w11.lastmon) + to_decimal(segmentstat.logis) / to_decimal(frate)
                        w11.lm_budget =  to_decimal(w11.lm_budget) + to_decimal(segmentstat.budlogis)

                    if w12:
                        w12.lastmon =  to_decimal(w12.lastmon) + to_decimal(segmentstat.zimmeranz)
                        w12.lm_budget =  to_decimal(w12.lm_budget) + to_decimal(segmentstat.budzimmeranz)

                    if w13:
                        w13.lastmon =  to_decimal(w13.lastmon) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w13.lm_budget =  to_decimal(w13.lm_budget) + to_decimal(segmentstat.budpersanz)


            if w11:
                w11.done = True

            if w12:
                w12.done = True

            if w13:
                w13.done = True
        w1.done = True

        if w1a:
            w1a.done = True

        if w22:
            w22.done = True


    def fill_gledger(rec_w1:int):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

        datum1:date = None
        W11 = W1
        w11_list = w1_list
        W12 = W1
        w12_list = w1_list

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        uebertrag = get_cache (Uebertrag, {"datum": [(eq, to_date - timedelta(days=1))]})

        if uebertrag:
            w1.tday =  to_decimal(uebertrag.betrag)
            w1.done = True


    def fill_comprooms(rec_w1:int):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

        datum1:date = None

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return
        lytoday_flag = (lytd_flag or lmtd_flag) and (get_month(to_date) != 2 or get_day(to_date) != 29)
        datum1 = from_date

        for segment in db_session.query(Segment).filter(
                 (Segment.betriebsnr == 0)).order_by(Segment._recid).all():

            for segmentstat in db_session.query(Segmentstat).filter(
                     (Segmentstat.datum >= datum1) & (Segmentstat.datum <= to_date) & (Segmentstat.segmentcode == segment.segmentcode) & (Segmentstat.betriebsnr > 0)).order_by(Segmentstat._recid).all():

                if foreign_flag:
                    find_exrate(segmentstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)

                if segmentstat.datum == to_date:
                    pass

                    if lytoday_flag:
                        lytoday = to_date - timedelta(days=365)

                        segmbuff = get_cache (Segmentstat, {"datum": [(eq, lytoday)],"segmentcode": [(eq, segment.segmentcode)]})
                    w1.tday =  to_decimal(w1.tday) + to_decimal(segmentstat.betriebsnr)

                    if segmbuff:
                        w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(segmbuff.betriebsnr)

                if segmentstat.datum < from_date:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(segmentstat.betriebsnr)
                else:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(segmentstat.betriebsnr)

                    if ytd_flag:
                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(segmentstat.betriebsnr)
        w1.done = True


    def fill_rmocc_perc(rec_w1:int):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

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
            fill_rmocc(w12._recid)

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
        w1.done = True


    def fill_docc_perc(rec_w1:int):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

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
            fill_rmocc(w11._recid)

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
        w1.done = True


    def fill_fbcost(rec_w1:int):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

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
        for h_umsatz, h_artikel in db_session.query(H_umsatz, H_artikel).join(H_artikel,(H_artikel.artnr == H_umsatz.artnr) & (H_artikel.departement == H_umsatz.departement) & (H_artikel.artnrfront == artikel.artnr)).filter(
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
            for h_umsatz, h_artikel in db_session.query(H_umsatz, H_artikel).join(H_artikel,(H_artikel.artnr == H_umsatz.artnr) & (H_artikel.departement == H_umsatz.departement) & (H_artikel.artnrfront == artikel.artnr)).filter(
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
            for h_umsatz, h_artikel in db_session.query(H_umsatz, H_artikel).join(H_artikel,(H_artikel.artnr == H_umsatz.artnr) & (H_artikel.departement == H_umsatz.departement) & (H_artikel.artnrfront == artikel.artnr)).filter(
                     (H_umsatz.datum >= pfrom_date) & (H_umsatz.datum <= pto_date) & (H_umsatz.departement == w1.dept)).order_by(H_umsatz._recid).all():
                if h_umsatz_obj_list.get(h_umsatz._recid):
                    continue
                else:
                    h_umsatz_obj_list[h_umsatz._recid] = True


                cost = cal_fbcost(h_umsatz.artnr, h_umsatz.departement, h_umsatz.datum)
                w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(cost)

        w1.done = True


    def fill_quantity(rec_w1:int):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

        datum1:date = None
        datum2:date = None

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        artikel = get_cache (Artikel, {"artnr": [(eq, w1.artnr)],"departement": [(eq, w1.dept)]})

        if not artikel:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Noch such article number : ", lvcarea, "") + to_string(w1.artnr) + " " + translateExtended ("Dept", lvcarea, "") + " " + to_string(w1.dept)

            return

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for umsatz in db_session.query(Umsatz).filter(
                 (Umsatz.datum >= datum1) & (Umsatz.datum <= to_date) & (Umsatz.artnr == w1.artnr) & (Umsatz.departement == w1.dept)).order_by(Umsatz._recid).all():

            if umsatz.datum == to_date:
                w1.tday =  to_decimal(w1.tday) + to_decimal(umsatz.anzahl)

            if umsatz.datum < from_date:
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(umsatz.anzahl)
            else:
                w1.saldo =  to_decimal(w1.saldo) + to_decimal(umsatz.anzahl)

                if ytd_flag:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(umsatz.anzahl)

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
                    w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(umsatz.anzahl)

                    if lytd_flag:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(umsatz.anzahl)

        if pmtd_flag:

            for umsatz in db_session.query(Umsatz).filter(
                     (Umsatz.datum >= pfrom_date) & (Umsatz.datum <= pto_date) & (Umsatz.artnr == w1.artnr) & (Umsatz.departement == w1.dept)).order_by(Umsatz._recid).all():
                w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(umsatz.anzahl)

        w1.done = True


    def fill_revenue(rec_w1:int):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

        curr_date:date = None
        datum1:date = None
        serv:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        n_betrag:Decimal = to_decimal("0.0")

        w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

        if w1.done:

            return

        artikel = get_cache (Artikel, {"artnr": [(eq, w1.artnr)],"departement": [(eq, w1.dept)]})

        if not artikel:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Noch such article number : ", lvcarea, "") + to_string(w1.artnr) + " " + translateExtended ("Dept", lvcarea, "") + " " + to_string(w1.dept)

            return

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date
        for curr_date in date_range(datum1,to_date) :

            umsatz = get_cache (Umsatz, {"datum": [(eq, curr_date)],"artnr": [(eq, w1.artnr)],"departement": [(eq, w1.dept)]})
            n_betrag =  to_decimal("0")

            if umsatz:
                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, curr_date))

                if foreign_flag:
                    find_exrate(curr_date)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)
                n_betrag =  to_decimal(umsatz.betrag) / to_decimal((fact) * to_decimal(frate))

                if price_decimal == 0:
                    n_betrag =  to_decimal(round (n_betrag , 0))

            if budget_flag:

                budget = get_cache (Budget, {"artnr": [(eq, w1.artnr)],"departement": [(eq, w1.dept)],"datum": [(eq, curr_date)]})

            if curr_date == to_date:

                if umsatz:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(n_betrag)

                if budget:
                    w1.tbudget =  to_decimal(w1.tbudget) + to_decimal(budget.betrag)

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

                umsatz = get_cache (Umsatz, {"datum": [(eq, curr_date)],"artnr": [(eq, w1.artnr)],"departement": [(eq, w1.dept)]})
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

                if curr_date < lfrom_date:

                    if umsatz:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(n_betrag)

                    if budget:
                        w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(budget.betrag)
                else:

                    if umsatz:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(n_betrag)

                        if lytd_flag:
                            w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(n_betrag)

                    if budget:
                        w1.ly_budget =  to_decimal(w1.ly_budget) + to_decimal(budget.betrag)

                        if lytd_flag:
                            w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(budget.betrag)

        if pmtd_flag:
            for curr_date in date_range(pfrom_date,pto_date) :

                umsatz = get_cache (Umsatz, {"datum": [(eq, curr_date)],"artnr": [(eq, w1.artnr)],"departement": [(eq, w1.dept)]})
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
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(n_betrag)

                if budget:
                    w1.lm_budget =  to_decimal(w1.lm_budget) + to_decimal(budget.betrag)
        w1.done = True


    def fill_persocc(rec_w1:int):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

        datum1:date = None
        datum2:date = None
        W11 = W1
        w11_list = w1_list
        W22 = W1
        w22_list = w1_list
        W753 = W1
        w753_list = w1_list
        W754 = W1
        w754_list = w1_list
        W755 = W1
        w755_list = w1_list
        lytoday_flag = (lytd_flag or lmtd_flag) and (get_month(to_date) != 2 or get_day(to_date) != 29)

        w11 = query(w11_list, filters=(lambda w11: w11.main_code == 806), first=True)

        if w11 and w11.done:
            pass

        w22 = query(w22_list, filters=(lambda w22: w22.main_code == 183), first=True)

        if w22 and w22.done:
            pass

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

            for segmentstat in db_session.query(Segmentstat).filter(
                     (Segmentstat.datum >= datum1) & (Segmentstat.datum <= to_date) & (Segmentstat.segmentcode == segment.segmentcode)).order_by(Segmentstat._recid).all():

                if foreign_flag:
                    find_exrate(segmentstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)

                if segmentstat.datum == to_date:
                    pass

                    if lytoday_flag:
                        lytoday = to_date - timedelta(days=365)

                        segmbuff = get_cache (Segmentstat, {"datum": [(eq, lytoday)],"segmentcode": [(eq, segment.segmentcode)]})
                    w1.tday =  to_decimal(w1.tday) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                    w1.tbudget =  to_decimal(w1.tbudget) + to_decimal(segmentstat.budpersanz)

                    if segmbuff:
                        w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(segmbuff.persanz) + to_decimal(segmbuff.kind1) + to_decimal(segmbuff.kind2) + to_decimal(segmbuff.gratis)

                    if w11:
                        w11.tday =  to_decimal(w11.tday) + to_decimal(segmentstat.zimmeranz)
                        w11.tbudget =  to_decimal(w11.tbudget) + to_decimal(segmentstat.budzimmeranz)

                        if segmbuff:
                            w11.lytoday =  to_decimal(w11.lytoday) + to_decimal(segmbuff.zimmeranz)

                    if w22 and segment.betriebsnr == 0:
                        w22.tday =  to_decimal(w22.tday) + to_decimal(segmentstat.betriebsnr)

                        if segmbuff:
                            w22.lytoday =  to_decimal(w22.lytoday) + to_decimal(segmbuff.betriebsnr)

                    if w753:
                        w753.tday =  to_decimal(w753.tday) + to_decimal(segmentstat.persanz)

                        if segmbuff:
                            w753.lytoday =  to_decimal(w753.lytoday) + to_decimal(segmbuff.persanz)

                    if w754:
                        w754.tday =  to_decimal(w754.tday) + to_decimal(segmentstat.kind1)

                        if segmbuff:
                            w754.lytoday =  to_decimal(w754.lytoday) + to_decimal(segmbuff.kind1)

                    if w755:
                        w755.tday =  to_decimal(w755.tday) + to_decimal(segmentstat.kind2)

                        if segmbuff:
                            w755.lytoday =  to_decimal(w755.lytoday) + to_decimal(segmbuff.kind2)

                if segmentstat.datum < from_date:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                    w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(segmentstat.budpersanz)

                    if w11:
                        w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(segmentstat.zimmeranz)
                        w11.ytd_budget =  to_decimal(w11.ytd_budget) + to_decimal(segmentstat.budzimmeranz)

                    if w22 and segment.betriebsnr == 0:
                        w22.ytd_saldo =  to_decimal(w22.ytd_saldo) + to_decimal(segmentstat.betriebsnr)

                    if w753:
                        w753.ytd_saldo =  to_decimal(w753.ytd_saldo) + to_decimal(segmentstat.persanz)

                    if w754:
                        w754.ytd_saldo =  to_decimal(w754.ytd_saldo) + to_decimal(segmentstat.kind1)

                    if w755:
                        w755.ytd_saldo =  to_decimal(w755.ytd_saldo) + to_decimal(segmentstat.kind2)
                else:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                    w1.budget =  to_decimal(w1.budget) + to_decimal(segmentstat.budpersanz)

                    if w11:
                        w11.saldo =  to_decimal(w11.saldo) + to_decimal(segmentstat.zimmeranz)
                        w11.budget =  to_decimal(w11.budget) + to_decimal(segmentstat.budzimmeranz)

                    if w22 and segment.betriebsnr == 0:
                        w22.saldo =  to_decimal(w22.saldo) + to_decimal(segmentstat.betriebsnr)

                    if w753:
                        w753.saldo =  to_decimal(w753.saldo) + to_decimal(segmentstat.persanz)

                    if w754:
                        w754.saldo =  to_decimal(w754.saldo) + to_decimal(segmentstat.kind1)

                    if w755:
                        w755.saldo =  to_decimal(w755.saldo) + to_decimal(segmentstat.kind2)

                    if ytd_flag:
                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(segmentstat.budpersanz)

                        if w11:
                            w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(segmentstat.zimmeranz)
                            w11.ytd_budget =  to_decimal(w11.ytd_budget) + to_decimal(segmentstat.budzimmeranz)

                        if w22 and segment.betriebsnr == 0:
                            w22.ytd_saldo =  to_decimal(w22.ytd_saldo) + to_decimal(segmentstat.betriebsnr)

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

                        if w11:
                            w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(segmentstat.zimmeranz)
                            w11.lytd_budget =  to_decimal(w11.lytd_budget) + to_decimal(segmentstat.budzimmeranz)

                        if w22 and segment.betriebsnr == 0:
                            w22.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(segmentstat.betriebsnr)

                        if w753:
                            w753.lytd_saldo =  to_decimal(w753.lytd_saldo) + to_decimal(segmentstat.persanz)

                        if w754:
                            w754.lytd_saldo =  to_decimal(w754.lytd_saldo) + to_decimal(segmentstat.kind1)

                        if w755:
                            w755.lytd_saldo =  to_decimal(w755.lytd_saldo) + to_decimal(segmentstat.kind2)
                    else:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w1.ly_budget =  to_decimal(w1.ly_budget) + to_decimal(segmentstat.budpersanz)

                        if w11:
                            w11.lastyr =  to_decimal(w11.lastyr) + to_decimal(segmentstat.zimmeranz)
                            w11.ly_budget =  to_decimal(w11.ly_budget) + to_decimal(segmentstat.budzimmeranz)

                        if w22 and segment.betriebsnr == 0:
                            w22.lastyr =  to_decimal(w22.lastyr) + to_decimal(segmentstat.betriebsnr)

                        if w753:
                            w753.lastyr =  to_decimal(w753.lastyr) + to_decimal(segmentstat.persanz)

                        if w754:
                            w754.lastyr =  to_decimal(w754.lastyr) + to_decimal(segmentstat.kind1)

                        if w755:
                            w755.lastyr =  to_decimal(w755.lastyr) + to_decimal(segmentstat.kind2)

                        if lytd_flag:
                            w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                            w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(segmentstat.budpersanz)

                            if w11:
                                w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(segmentstat.zimmeranz)
                                w11.lytd_budget =  to_decimal(w11.lytd_budget) + to_decimal(segmentstat.budzimmeranz)

                            if w22 and segment.betriebsnr == 0:
                                w22.lytd_saldo =  to_decimal(w22.lytd_saldo) + to_decimal(segmentstat.betriebsnr)

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

                    if w11:
                        w11.lastmon =  to_decimal(w11.lastmon) + to_decimal(segmentstat.zimmeranz)
                        w11.lm_budget =  to_decimal(w11.lm_budget) + to_decimal(segmentstat.budzimmeranz)

                    if w22 and segment.betriebsnr == 0:
                        w22.lastmon =  to_decimal(w22.lastmon) + to_decimal(segmentstat.betriebsnr)

                    if w753:
                        w753.lastmon =  to_decimal(w753.lastmon) + to_decimal(segmentstat.persanz)

                    if w754:
                        w754.lastmon =  to_decimal(w754.lastmon) + to_decimal(segmentstat.kind1)

                    if w755:
                        w755.lastmon =  to_decimal(w755.lastmon) + to_decimal(segmentstat.kind2)

        w1.done = True

        if w11:
            w11.done = True

        if w22:
            w22.done = True

        if w753:
            w753.done = True

        if w754:
            w754.done = True

        if w755:
            w755.done = True


    def fill_avrgrate(rec_w1:int):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

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

        w1.done = True

        if w11:
            w11.done = True


    def fill_avrglrate(rec_w1:int):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

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

        w1.done = True

        if w11:
            w11.done = True


    def fill_avrglodge(rec_w1:int):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

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

        w1.done = True

        if w11:
            w11.done = True


    def fill_segment(rec_w1:int, main_nr:int):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

        segm:int = 0
        datum1:date = None
        W11 = W1
        w11_list = w1_list
        W12 = W1
        w12_list = w1_list
        W13 = W1
        w13_list = w1_list
        W756 = W1
        w756_list = w1_list
        W757 = W1
        w757_list = w1_list
        W758 = W1
        w758_list = w1_list
        lytoday_flag = (lytd_flag or lmtd_flag) and (get_month(to_date) != 2 or get_day(to_date) != 29)

        if main_nr == 92:

            w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

            if w1.done:

                return
            segm = w1.artnr

            w12 = query(w12_list, filters=(lambda w12: w12.main_code == 813 and w12.artnr == segm and not w12.done), first=True)

            w13 = query(w13_list, filters=(lambda w13: w13.main_code == 814 and w13.artnr == segm and not w13.done), first=True)

            w756 = query(w756_list, filters=(lambda w756: w756.main_code == 756 and w756.artnr == segm and not w756.done), first=True)

            w757 = query(w757_list, filters=(lambda w757: w757.main_code == 757 and w757.artnr == segm and not w757.done), first=True)

            w758 = query(w758_list, filters=(lambda w758: w758.main_code == 758 and w758.artnr == segm and not w758.done), first=True)

        elif main_nr == 813:

            w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

            if w1.done:

                return
            segm = w1.artnr

            w11 = query(w11_list, filters=(lambda w11: w11.main_code == 92 and w11.artnr == segm and not w11.done), first=True)

            w13 = query(w13_list, filters=(lambda w13: w13.main_code == 814 and w13.artnr == segm and not w13.done), first=True)

            w757 = query(w757_list, filters=(lambda w757: w757.main_code == 757 and w757.artnr == segm and not w757.done), first=True)

            w758 = query(w758_list, filters=(lambda w758: w758.main_code == 758 and w758.artnr == segm and not w758.done), first=True)

        elif main_nr == 814:

            w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

            if w1.done:

                return
            segm = w1.artnr

            w11 = query(w11_list, filters=(lambda w11: w11.main_code == 92 and w11.artnr == segm and not w11.done), first=True)

            w12 = query(w12_list, filters=(lambda w12: w12.main_code == 813 and w12.artnr == segm and not w12.done), first=True)

            w757 = query(w757_list, filters=(lambda w757: w757.main_code == 757 and w757.artnr == segm and not w757.done), first=True)

            w758 = query(w758_list, filters=(lambda w758: w758.main_code == 758 and w758.artnr == segm and not w758.done), first=True)

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for segmentstat in db_session.query(Segmentstat).filter(
                     (Segmentstat.datum >= datum1) & (Segmentstat.datum <= to_date) & (Segmentstat.segmentcode == segm)).order_by(Segmentstat._recid).all():

            if foreign_flag:
                find_exrate(segmentstat.datum)

                if exrate:
                    frate =  to_decimal(exrate.betrag)

            if segmentstat.datum == to_date:
                pass

                if lytoday_flag:
                    lytoday = to_date - timedelta(days=365)

                    segmbuff = get_cache (Segmentstat, {"datum": [(eq, lytoday)],"segmentcode": [(eq, segment.segmentcode)]})

                if main_nr == 92:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(segmentstat.logis) / to_decimal(frate)
                    w1.tbudget =  to_decimal(w1.tbudget) + to_decimal(segmentstat.budlogis)

                    if segmbuff:
                        w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(segmbuff.logis) / to_decimal(frate)

                    if w12:
                        w12.tday =  to_decimal(w12.tday) + to_decimal(segmentstat.zimmeranz)
                        w12.tbudget =  to_decimal(w12.tbudget) + to_decimal(segmentstat.budzimmeranz)

                        if segmbuff:
                            w12.lytoday =  to_decimal(w12.lytoday) + to_decimal(segmbuff.zimmeranz)

                    if w13:
                        w13.tday =  to_decimal(w13.tday) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w13.tbudget =  to_decimal(w13.tbudget) + to_decimal(segmentstat.budpersanz)

                        if segmbuff:
                            w13.lytoday =  to_decimal(w13.lytoday) + to_decimal(segmbuff.persanz) + to_decimal(segmbuff.kind1) + to_decimal(segmbuff.kind2) + to_decimal(segmbuff.gratis)

                    if w756:
                        w756.tday =  to_decimal(w756.tday) + to_decimal(segmentstat.persanz)
                        w756.tbudget =  to_decimal(w756.tbudget) + to_decimal(segmentstat.budpersanz)

                        if segmbuff:
                            w756.lytoday =  to_decimal(w756.lytoday) + to_decimal(segmbuff.persanz)

                    if w757:
                        w757.tday =  to_decimal(w757.tday) + to_decimal(segmentstat.kind1)

                        if segmbuff:
                            w757.lytoday =  to_decimal(w757.lytoday) + to_decimal(segmbuff.kind1)

                    if w758:
                        w758.tday =  to_decimal(w758.tday) + to_decimal(segmentstat.kind2)

                        if segmbuff:
                            w758.lytoday =  to_decimal(w758.lytoday) + to_decimal(segmbuff.kind2)

                elif main_nr == 813:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(segmentstat.zimmeranz)
                    w1.tbudget =  to_decimal(w1.tbudget) + to_decimal(segmentstat.budzimmeranz)

                    if segmbuff:
                        w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(segmbuff.zimmeranz)

                    if w11:
                        w11.tday =  to_decimal(w11.tday) + to_decimal(segmentstat.logis) / to_decimal(frate)
                        w11.tbudget =  to_decimal(w11.tbudget) + to_decimal(segmentstat.budlogis)

                        if segmbuff:
                            w11.lytoday =  to_decimal(w11.lytoday) + to_decimal(segmbuff.logis) / to_decimal(frate)

                    if w13:
                        w13.tday =  to_decimal(w13.tday) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w13.tbudget =  to_decimal(w13.tbudget) + to_decimal(segmentstat.budpersanz)

                        if segmbuff:
                            w13.lytoday =  to_decimal(w13.lytoday) + to_decimal(segmbuff.persanz) + to_decimal(segmbuff.kind1) + to_decimal(segmbuff.kind2) + to_decimal(segmbuff.gratis)

                        if w756:
                            w756.tday =  to_decimal(w756.tday) + to_decimal(segmentstat.persanz)
                            w756.tbudget =  to_decimal(w756.tbudget) + to_decimal(segmentstat.budpersanz)

                            if segmbuff:
                                w756.lytoday =  to_decimal(w756.lytoday) + to_decimal(segmbuff.persanz)

                        if w757:
                            w757.tday =  to_decimal(w757.tday) + to_decimal(segmentstat.kind1)

                            if segmbuff:
                                w757.lytoday =  to_decimal(w757.lytoday) + to_decimal(segmbuff.kind1)

                        if w758:
                            w758.tday =  to_decimal(w758.tday) + to_decimal(segmentstat.kind2)

                            if segmbuff:
                                w758.lytoday =  to_decimal(w758.lytoday) + to_decimal(segmbuff.kind2)

                elif main_nr == 814:
                    w1.tday =  to_decimal(w1.tday) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                    w1.tbudget =  to_decimal(w1.tbudget) + to_decimal(segmentstat.budpersanz)

                    if segmbuff:
                        w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(segmbuff.persanz) + to_decimal(segmbuff.kind1) + to_decimal(segmbuff.kind2) + to_decimal(segmbuff.gratis)

                    if w11:
                        w11.tday =  to_decimal(w11.tday) + to_decimal(segmentstat.logis) / to_decimal(frate)
                        w11.tbudget =  to_decimal(w11.tbudget) + to_decimal(segmentstat.budlogis)

                        if segmbuff:
                            w1.lytoday =  to_decimal(w1.lytoday) + to_decimal(segmbuff.logis) / to_decimal(frate)

                    if w12:
                        w12.tday =  to_decimal(w12.tday) + to_decimal(segmentstat.zimmeranz)
                        w12.tbudget =  to_decimal(w12.tbudget) + to_decimal(segmentstat.budzimmeranz)

                        if segmbuff:
                            w12.lytoday =  to_decimal(w12.lytoday) + to_decimal(segmbuff.zimmeranz)

                    if w756:
                        w756.tday =  to_decimal(w756.tday) + to_decimal(segmentstat.persanz)
                        w756.tbudget =  to_decimal(w756.tbudget) + to_decimal(segmentstat.budpersanz)

                        if segmbuff:
                            w756.lytoday =  to_decimal(w756.lytoday) + to_decimal(segmbuff.persanz)

                    if w757:
                        w757.tday =  to_decimal(w757.tday) + to_decimal(segmentstat.kind1)

                        if segmbuff:
                            w757.lytoday =  to_decimal(w757.lytoday) + to_decimal(segmbuff.kind1)

                    if w758:
                        w758.tday =  to_decimal(w758.tday) + to_decimal(segmentstat.kind2)

                        if segmbuff:
                            w758.lytoday =  to_decimal(w758.lytoday) + to_decimal(segmbuff.kind2)

            if segmentstat.datum < from_date:

                if main_nr == 92:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(segmentstat.logis) / to_decimal(frate)
                    w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(segmentstat.budlogis)

                    if w12:
                        w12.ytd_saldo =  to_decimal(w12.ytd_saldo) + to_decimal(segmentstat.zimmeranz)
                        w12.ytd_budget =  to_decimal(w12.ytd_budget) + to_decimal(segmentstat.budzimmeranz)

                    if w13:
                        w13.ytd_saldo =  to_decimal(w13.ytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w13.ytd_budget =  to_decimal(w13.ytd_budget) + to_decimal(segmentstat.budpersanz)

                    if w756:
                        w756.ytd_saldo =  to_decimal(w756.ytd_saldo) + to_decimal(segmentstat.persanz)
                        w756.ytd_budget =  to_decimal(w756.ytd_budget) + to_decimal(segmentstat.budpersanz)

                    if w757:
                        w757.ytd_saldo =  to_decimal(w757.ytd_saldo) + to_decimal(segmentstat.kind1)

                    if w758:
                        w758.ytd_saldo =  to_decimal(w758.ytd_saldo) + to_decimal(segmentstat.kind2)

                elif main_nr == 813:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(segmentstat.zimmeranz)
                    w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(segmentstat.budzimmeranz)

                    if w11:
                        w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(segmentstat.logis) / to_decimal(frate)
                        w11.ytd_budget =  to_decimal(w11.ytd_budget) + to_decimal(segmentstat.budlogis)

                    if w13:
                        w13.ytd_saldo =  to_decimal(w13.ytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w13.ytd_budget =  to_decimal(w13.ytd_budget) + to_decimal(segmentstat.budpersanz)

                    if w756:
                        w756.ytd_saldo =  to_decimal(w756.ytd_saldo) + to_decimal(segmentstat.persanz)
                        w756.ytd_budget =  to_decimal(w756.ytd_budget) + to_decimal(segmentstat.budpersanz)

                    if w757:
                        w757.ytd_saldo =  to_decimal(w757.ytd_saldo) + to_decimal(segmentstat.kind1)

                    if w758:
                        w758.ytd_saldo =  to_decimal(w758.ytd_saldo) + to_decimal(segmentstat.kind2)

                elif main_nr == 814:
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                    w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(segmentstat.budpersanz)

                    if w11:
                        w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(segmentstat.logis) / to_decimal(frate)
                        w11.ytd_budget =  to_decimal(w11.ytd_budget) + to_decimal(segmentstat.budlogis)

                    if w12:
                        w12.ytd_saldo =  to_decimal(w12.ytd_saldo) + to_decimal(segmentstat.zimmeranz)
                        w12.ytd_budget =  to_decimal(w12.ytd_budget) + to_decimal(segmentstat.budzimmeranz)

                    if w756:
                        w756.ytd_saldo =  to_decimal(w756.ytd_saldo) + to_decimal(segmentstat.persanz)
                        w756.ytd_budget =  to_decimal(w756.ytd_budget) + to_decimal(segmentstat.budpersanz)

                    if w757:
                        w757.ytd_saldo =  to_decimal(w757.ytd_saldo) + to_decimal(segmentstat.kind1)

                    if w758:
                        w758.ytd_saldo =  to_decimal(w758.ytd_saldo) + to_decimal(segmentstat.kind2)
            else:

                if main_nr == 92:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(segmentstat.logis) / to_decimal(frate)
                    w1.budget =  to_decimal(w1.budget) + to_decimal(segmentstat.budlogis)

                    if w12:
                        w12.saldo =  to_decimal(w12.saldo) + to_decimal(segmentstat.zimmeranz)
                        w12.budget =  to_decimal(w12.budget) + to_decimal(segmentstat.budzimmeranz)

                    if w13:
                        w13.saldo =  to_decimal(w13.saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w13.budget =  to_decimal(w13.budget) + to_decimal(segmentstat.budpersanz)

                    if w756:
                        w756.saldo =  to_decimal(w756.saldo) + to_decimal(segmentstat.persanz)
                        w756.budget =  to_decimal(w756.budget) + to_decimal(segmentstat.budpersanz)

                    if w757:
                        w757.saldo =  to_decimal(w757.saldo) + to_decimal(segmentstat.kind1)

                    if w758:
                        w758.saldo =  to_decimal(w758.saldo) + to_decimal(segmentstat.kind2)

                elif main_nr == 813:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(segmentstat.zimmeranz)
                    w1.budget =  to_decimal(w1.budget) + to_decimal(segmentstat.budzimmeranz)

                    if w11:
                        w11.saldo =  to_decimal(w11.saldo) + to_decimal(segmentstat.logis) / to_decimal(frate)
                        w11.budget =  to_decimal(w11.budget) + to_decimal(segmentstat.budlogis)

                    if w13:
                        w13.saldo =  to_decimal(w13.saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w13.budget =  to_decimal(w13.budget) + to_decimal(segmentstat.budpersanz)

                    if w756:
                        w756.saldo =  to_decimal(w756.saldo) + to_decimal(segmentstat.persanz)
                        w756.budget =  to_decimal(w756.budget) + to_decimal(segmentstat.budpersanz)

                    if w757:
                        w757.saldo =  to_decimal(w757.saldo) + to_decimal(segmentstat.kind1)

                    if w758:
                        w758.saldo =  to_decimal(w758.saldo) + to_decimal(segmentstat.kind2)

                elif main_nr == 814:
                    w1.saldo =  to_decimal(w1.saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                    w1.budget =  to_decimal(w1.budget) + to_decimal(segmentstat.budpersanz)

                    if w11:
                        w11.saldo =  to_decimal(w11.saldo) + to_decimal(segmentstat.logis) / to_decimal(frate)
                        w11.budget =  to_decimal(w11.budget) + to_decimal(segmentstat.budlogis)

                    if w12:
                        w12.saldo =  to_decimal(w12.saldo) + to_decimal(segmentstat.zimmeranz)
                        w12.budget =  to_decimal(w12.budget) + to_decimal(segmentstat.budzimmeranz)

                    if w756:
                        w756.saldo =  to_decimal(w756.saldo) + to_decimal(segmentstat.persanz)
                        w756.budget =  to_decimal(w756.budget) + to_decimal(segmentstat.budpersanz)

                    if w757:
                        w757.saldo =  to_decimal(w757.saldo) + to_decimal(segmentstat.kind1)

                    if w758:
                        w758.saldo =  to_decimal(w758.saldo) + to_decimal(segmentstat.kind2)

                if ytd_flag:

                    if main_nr == 92:
                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(segmentstat.logis) / to_decimal(frate)
                        w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(segmentstat.budlogis)

                        if w12:
                            w12.ytd_saldo =  to_decimal(w12.ytd_saldo) + to_decimal(segmentstat.zimmeranz)
                            w12.ytd_budget =  to_decimal(w12.ytd_budget) + to_decimal(segmentstat.budzimmeranz)

                        if w13:
                            w13.ytd_saldo =  to_decimal(w13.ytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                            w13.ytd_budget =  to_decimal(w13.ytd_budget) + to_decimal(segmentstat.budpersanz)

                        if w756:
                            w756.ytd_saldo =  to_decimal(w756.ytd_saldo) + to_decimal(segmentstat.persanz)
                            w756.ytd_budget =  to_decimal(w756.ytd_budget) + to_decimal(segmentstat.budpersanz)

                        if w757:
                            w757.ytd_saldo =  to_decimal(w757.ytd_saldo) + to_decimal(segmentstat.kind1)

                        if w758:
                            w758.ytd_saldo =  to_decimal(w758.ytd_saldo) + to_decimal(segmentstat.kind2)

                    elif main_nr == 813:
                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(segmentstat.zimmeranz)
                        w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(segmentstat.budzimmeranz)

                        if w11:
                            w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(segmentstat.logis) / to_decimal(frate)
                            w11.ytd_budget =  to_decimal(w11.ytd_budget) + to_decimal(segmentstat.budlogis)

                        if w13:
                            w13.ytd_saldo =  to_decimal(w13.ytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                            w13.ytd_budget =  to_decimal(w13.ytd_budget) + to_decimal(segmentstat.budpersanz)

                        if w756:
                            w756.ytd_saldo =  to_decimal(w756.ytd_saldo) + to_decimal(segmentstat.persanz)
                            w756.ytd_budget =  to_decimal(w756.ytd_budget) + to_decimal(segmentstat.budpersanz)

                        if w757:
                            w757.ytd_saldo =  to_decimal(w757.ytd_saldo) + to_decimal(segmentstat.kind1)

                        if w758:
                            w758.ytd_saldo =  to_decimal(w758.ytd_saldo) + to_decimal(segmentstat.kind2)

                    elif main_nr == 814:
                        w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(segmentstat.budpersanz)

                        if w11:
                            w11.ytd_saldo =  to_decimal(w11.ytd_saldo) + to_decimal(segmentstat.logis) / to_decimal(frate)
                            w11.ytd_budget =  to_decimal(w11.ytd_budget) + to_decimal(segmentstat.budlogis)

                        if w12:
                            w12.ytd_saldo =  to_decimal(w12.ytd_saldo) + to_decimal(segmentstat.zimmeranz)
                            w12.ytd_budget =  to_decimal(w12.ytd_budget) + to_decimal(segmentstat.budzimmeranz)

                        if w756:
                            w756.ytd_saldo =  to_decimal(w756.ytd_saldo) + to_decimal(segmentstat.persanz)
                            w756.ytd_budget =  to_decimal(w756.ytd_budget) + to_decimal(segmentstat.budpersanz)

                        if w757:
                            w757.ytd_saldo =  to_decimal(w757.ytd_saldo) + to_decimal(segmentstat.kind1)

                        if w758:
                            w758.ytd_saldo =  to_decimal(w758.ytd_saldo) + to_decimal(segmentstat.kind2)

        if lytd_flag or lmtd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date

            for segmentstat in db_session.query(Segmentstat).filter(
                         (Segmentstat.datum >= datum1) & (Segmentstat.datum <= lto_date) & (Segmentstat.segmentcode == segm)).order_by(Segmentstat._recid).all():

                if foreign_flag:
                    find_exrate(segmentstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)

                if segmentstat.datum < lfrom_date:

                    if main_nr == 92:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(segmentstat.logis) / to_decimal(frate)
                        w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(segmentstat.budlogis)

                        if w12:
                            w12.lytd_saldo =  to_decimal(w12.lytd_saldo) + to_decimal(segmentstat.zimmeranz)
                            w12.lytd_budget =  to_decimal(w12.lytd_budget) + to_decimal(segmentstat.budzimmeranz)

                        if w13:
                            w13.lytd_saldo =  to_decimal(w13.lytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                            w13.lytd_budget =  to_decimal(w13.lytd_budget) + to_decimal(segmentstat.budpersanz)

                        if w756:
                            w756.lytd_saldo =  to_decimal(w756.lytd_saldo) + to_decimal(segmentstat.persanz)
                            w756.lytd_budget =  to_decimal(w756.lytd_budget) + to_decimal(segmentstat.budpersanz)

                        if w757:
                            w757.lytd_saldo =  to_decimal(w757.lytd_saldo) + to_decimal(segmentstat.kind1)

                        if w758:
                            w758.lytd_saldo =  to_decimal(w758.lytd_saldo) + to_decimal(segmentstat.kind2)

                    elif main_nr == 813:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(segmentstat.zimmeranz)
                        w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(segmentstat.budzimmeranz)

                        if w11:
                            w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(segmentstat.logis) / to_decimal(frate)
                            w11.lytd_budget =  to_decimal(w11.lytd_budget) + to_decimal(segmentstat.budlogis)

                        if w13:
                            w13.lytd_saldo =  to_decimal(w13.lytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                            w13.lytd_budget =  to_decimal(w13.lytd_budget) + to_decimal(segmentstat.budpersanz)

                        if w756:
                            w756.lytd_saldo =  to_decimal(w756.lytd_saldo) + to_decimal(segmentstat.persanz)
                            w756.lytd_budget =  to_decimal(w756.lytd_budget) + to_decimal(segmentstat.budpersanz)

                        if w757:
                            w757.lytd_saldo =  to_decimal(w757.lytd_saldo) + to_decimal(segmentstat.kind1)

                        if w758:
                            w758.lytd_saldo =  to_decimal(w758.lytd_saldo) + to_decimal(segmentstat.kind2)

                    elif main_nr == 814:
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(segmentstat.budpersanz)

                        if w11:
                            w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(segmentstat.logis) / to_decimal(frate)
                            w11.lytd_budget =  to_decimal(w11.lytd_budget) + to_decimal(segmentstat.budlogis)

                        if w12:
                            w12.lytd_saldo =  to_decimal(w12.lytd_saldo) + to_decimal(segmentstat.zimmeranz)
                            w12.lytd_budget =  to_decimal(w12.lytd_budget) + to_decimal(segmentstat.budzimmeranz)

                        if w756:
                            w756.lytd_saldo =  to_decimal(w756.lytd_saldo) + to_decimal(segmentstat.persanz)
                            w756.lytd_budget =  to_decimal(w756.lytd_budget) + to_decimal(segmentstat.budpersanz)

                        if w757:
                            w757.lytd_saldo =  to_decimal(w757.lytd_saldo) + to_decimal(segmentstat.kind1)

                        if w758:
                            w758.lytd_saldo =  to_decimal(w758.lytd_saldo) + to_decimal(segmentstat.kind2)
                else:

                    if main_nr == 92:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(segmentstat.logis) / to_decimal(frate)
                        w1.ly_budget =  to_decimal(w1.ly_budget) + to_decimal(segmentstat.budlogis)

                        if w12:
                            w12.lastyr =  to_decimal(w12.lastyr) + to_decimal(segmentstat.zimmeranz)
                            w12.ly_budget =  to_decimal(w12.ly_budget) + to_decimal(segmentstat.budzimmeranz)

                        if w13:
                            w13.lastyr =  to_decimal(w13.lastyr) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                            w13.ly_budget =  to_decimal(w13.ly_budget) + to_decimal(segmentstat.budpersanz)

                        if w756:
                            w756.lastyr =  to_decimal(w756.lastyr) + to_decimal(segmentstat.persanz)
                            w756.ly_budget =  to_decimal(w756.ly_budget) + to_decimal(segmentstat.budpersanz)

                        if w757:
                            w757.lastyr =  to_decimal(w757.lastyr) + to_decimal(segmentstat.kind1)

                        if w758:
                            w758.lastyr =  to_decimal(w758.lastyr) + to_decimal(segmentstat.kind2)

                    elif main_nr == 813:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(segmentstat.zimmeranz)
                        w1.ly_budget =  to_decimal(w1.ly_budget) + to_decimal(segmentstat.budzimmeranz)

                        if w11:
                            w11.lastyr =  to_decimal(w11.lastyr) + to_decimal(segmentstat.logis) / to_decimal(frate)
                            w11.ly_budget =  to_decimal(w11.ly_budget) + to_decimal(segmentstat.budlogis)

                        if w13:
                            w13.lastyr =  to_decimal(w13.lastyr) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                            w13.ly_budget =  to_decimal(w13.ly_budget) + to_decimal(segmentstat.budpersanz)

                        if w756:
                            w756.lastyr =  to_decimal(w756.lastyr) + to_decimal(segmentstat.persanz)
                            w756.ly_budget =  to_decimal(w756.ly_budget) + to_decimal(segmentstat.budpersanz)

                        if w757:
                            w757.lastyr =  to_decimal(w757.lastyr) + to_decimal(segmentstat.kind1)

                        if w758:
                            w758.lastyr =  to_decimal(w758.lastyr) + to_decimal(segmentstat.kind2)

                    elif main_nr == 814:
                        w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w1.ly_budget =  to_decimal(w1.ly_budget) + to_decimal(segmentstat.budpersanz)

                        if w11:
                            w11.lastyr =  to_decimal(w11.lastyr) + to_decimal(segmentstat.logis) / to_decimal(frate)
                            w11.ly_budget =  to_decimal(w11.ly_budget) + to_decimal(segmentstat.budlogis)

                        if w12:
                            w12.lastyr =  to_decimal(w12.lastyr) + to_decimal(segmentstat.zimmeranz)
                            w12.ly_budget =  to_decimal(w12.ly_budget) + to_decimal(segmentstat.budzimmeranz)

                        if w756:
                            w756.lastyr =  to_decimal(w756.lastyr) + to_decimal(segmentstat.persanz)
                            w756.ly_budget =  to_decimal(w756.ly_budget) + to_decimal(segmentstat.budpersanz)

                        if w757:
                            w757.lastyr =  to_decimal(w757.lastyr) + to_decimal(segmentstat.kind1)

                        if w758:
                            w758.lastyr =  to_decimal(w758.lastyr) + to_decimal(segmentstat.kind2)

                    if lytd_flag:

                        if main_nr == 92:
                            w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(segmentstat.logis) / to_decimal(frate)
                            w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(segmentstat.budlogis)

                            if w12:
                                w12.lytd_saldo =  to_decimal(w12.lytd_saldo) + to_decimal(segmentstat.zimmeranz)
                                w12.lytd_budget =  to_decimal(w12.lytd_budget) + to_decimal(segmentstat.budzimmeranz)

                            if w13:
                                w13.lytd_saldo =  to_decimal(w13.lytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                                w13.lytd_budget =  to_decimal(w13.lytd_budget) + to_decimal(segmentstat.budpersanz)

                            if w756:
                                w756.lytd_saldo =  to_decimal(w756.lytd_saldo) + to_decimal(segmentstat.persanz)
                                w756.lytd_budget =  to_decimal(w756.lytd_budget) + to_decimal(segmentstat.budpersanz)

                            if w757:
                                w757.lytd_saldo =  to_decimal(w757.lytd_saldo) + to_decimal(segmentstat.kind1)

                            if w758:
                                w758.lytd_saldo =  to_decimal(w758.lytd_saldo) + to_decimal(segmentstat.kind2)

                        elif main_nr == 813:
                            w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(segmentstat.zimmeranz)
                            w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(segmentstat.budzimmeranz)

                            if w11:
                                w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(segmentstat.logis) / to_decimal(frate)
                                w11.lytd_budget =  to_decimal(w11.lytd_budget) + to_decimal(segmentstat.budlogis)

                            if w13:
                                w13.lytd_saldo =  to_decimal(w13.lytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                                w13.lytd_budget =  to_decimal(w13.lytd_budget) + to_decimal(segmentstat.budpersanz)

                            if w756:
                                w756.lytd_saldo =  to_decimal(w756.lytd_saldo) + to_decimal(segmentstat.persanz)
                                w756.lytd_budget =  to_decimal(w756.lytd_budget) + to_decimal(segmentstat.budpersanz)

                            if w757:
                                w757.lytd_saldo =  to_decimal(w757.lytd_saldo) + to_decimal(segmentstat.kind1)

                            if w758:
                                w758.lytd_saldo =  to_decimal(w758.lytd_saldo) + to_decimal(segmentstat.kind2)

                        elif main_nr == 814:
                            w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                            w1.lytd_budget =  to_decimal(w1.lytd_budget) + to_decimal(segmentstat.budpersanz)

                            if w11:
                                w11.lytd_saldo =  to_decimal(w11.lytd_saldo) + to_decimal(segmentstat.logis) / to_decimal(frate)
                                w11.lytd_budget =  to_decimal(w11.lytd_budget) + to_decimal(segmentstat.budlogis)

                            if w12:
                                w12.lytd_saldo =  to_decimal(w12.lytd_saldo) + to_decimal(segmentstat.zimmeranz)
                                w12.lytd_budget =  to_decimal(w12.lytd_budget) + to_decimal(segmentstat.budzimmeranz)

                            if w756:
                                w756.lytd_saldo =  to_decimal(w756.lytd_saldo) + to_decimal(segmentstat.persanz)
                                w756.lytd_budget =  to_decimal(w756.lytd_budget) + to_decimal(segmentstat.budpersanz)

                            if w757:
                                w757.lytd_saldo =  to_decimal(w757.lytd_saldo) + to_decimal(segmentstat.kind1)

                            if w758:
                                w758.lytd_saldo =  to_decimal(w758.lytd_saldo) + to_decimal(segmentstat.kind2)

        if pmtd_flag:

            for segmentstat in db_session.query(Segmentstat).filter(
                         (Segmentstat.datum >= pfrom_date) & (Segmentstat.datum <= pto_date) & (Segmentstat.segmentcode == segm)).order_by(Segmentstat._recid).all():

                if foreign_flag:
                    find_exrate(segmentstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)

                if main_nr == 92:
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(segmentstat.logis) / to_decimal(frate)
                    w1.lm_budget =  to_decimal(w1.lm_budget) + to_decimal(segmentstat.budlogis)

                    if w12:
                        w12.lastmon =  to_decimal(w12.lastmon) + to_decimal(segmentstat.zimmeranz)
                        w12.lm_budget =  to_decimal(w12.lm_budget) + to_decimal(segmentstat.budzimmeranz)

                    if w13:
                        w13.lastmon =  to_decimal(w13.lastmon) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w13.lm_budget =  to_decimal(w13.lm_budget) + to_decimal(segmentstat.budpersanz)

                    if w756:
                        w756.lastmon =  to_decimal(w756.lastmon) + to_decimal(segmentstat.persanz)
                        w756.lm_budget =  to_decimal(w756.lm_budget) + to_decimal(segmentstat.budpersanz)

                    if w757:
                        w757.lastmon =  to_decimal(w757.lastmon) + to_decimal(segmentstat.kind1)

                    if w758:
                        w758.lastmon =  to_decimal(w758.lastmon) + to_decimal(segmentstat.kind2)

                elif main_nr == 813:
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(segmentstat.zimmeranz)
                    w1.lm_budget =  to_decimal(w1.lm_budget) + to_decimal(segmentstat.budzimmeranz)

                    if w11:
                        w11.lastmon =  to_decimal(w11.lastmon) + to_decimal(segmentstat.logis) / to_decimal(frate)
                        w11.lm_budget =  to_decimal(w11.lm_budget) + to_decimal(segmentstat.budlogis)

                    if w13:
                        w13.lastmon =  to_decimal(w13.lastmon) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                        w13.lm_budget =  to_decimal(w13.lm_budget) + to_decimal(segmentstat.budpersanz)

                    if w756:
                        w756.lastmon =  to_decimal(w756.lastmon) + to_decimal(segmentstat.persanz)
                        w756.lm_budget =  to_decimal(w756.lm_budget) + to_decimal(segmentstat.budpersanz)

                    if w757:
                        w757.lastmon =  to_decimal(w757.lastmon) + to_decimal(segmentstat.kind1)

                    if w758:
                        w758.lastmon =  to_decimal(w758.lastmon) + to_decimal(segmentstat.kind2)

                elif main_nr == 814:
                    w1.lastmon =  to_decimal(w1.lastmon) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                    w1.lm_budget =  to_decimal(w1.lm_budget) + to_decimal(segmentstat.budpersanz)

                    if w11:
                        w11.lastmon =  to_decimal(w11.lastmon) + to_decimal(segmentstat.logis) / to_decimal(frate)
                        w11.lm_budget =  to_decimal(w11.lm_budget) + to_decimal(segmentstat.budlogis)

                    if w12:
                        w12.lastmon =  to_decimal(w12.lastmon) + to_decimal(segmentstat.zimmeranz)
                        w12.lm_budget =  to_decimal(w12.lm_budget) + to_decimal(segmentstat.budzimmeranz)

                    if w756:
                        w756.lastmon =  to_decimal(w756.lastmon) + to_decimal(segmentstat.persanz)
                        w756.lm_budget =  to_decimal(w756.lm_budget) + to_decimal(segmentstat.budpersanz)

                    if w757:
                        w757.lastmon =  to_decimal(w757.lastmon) + to_decimal(segmentstat.kind1)

                    if w758:
                        w758.lastmon =  to_decimal(w758.lastmon) + to_decimal(segmentstat.kind2)

        w1.done = True

        if w11:
            w11.done = True

        if w12:
            w12.done = True

        if w13:
            w13.done = True

        if w756:
            w756.done = True

        if w757:
            w757.done = True

        if w758:
            w758.done = True


    def fill_rmcatstat(rec_w1:int, main_nr:int):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

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

        w1.done = True


    def fill_zinrstat(rec_w1:int, main_nr:int):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

        rmno:int = 0
        datum1:date = None
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

            w12 = query(w12_list, filters=(lambda w12: w12.main_code == 180 and w12.artnr == rmno), first=True)

            w13 = query(w13_list, filters=(lambda w13: w13.main_code == 181 and w13.artnr == rmno), first=True)

        elif main_nr == 180:

            w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

            if w1.done:

                return
            rmno = w1.artnr

            w11 = query(w11_list, filters=(lambda w11: w11.main_code == 800 and w11.artnr == rmno), first=True)

            w13 = query(w13_list, filters=(lambda w13: w13.main_code == 181 and w13.artnr == rmno), first=True)

        elif main_nr == 181:

            w1 = query(w1_list, filters=(lambda w1: w1._recid == rec_w1), first=True)

            if w1.done:

                return
            rmno = w1.artnr

            w11 = query(w11_list, filters=(lambda w11: w11.main_code == 800 and w11.artnr == rmno), first=True)

            w12 = query(w12_list, filters=(lambda w12: w12.main_code == 180 and w12.artnr == rmno), first=True)

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.datum >= datum1) & (Zinrstat.datum <= to_date) & (Zinrstat.zinr == to_string(rmno))).order_by(Zinrstat._recid).all():

            if foreign_flag:
                find_exrate(zinrstat.datum)

                if exrate:
                    frate =  to_decimal(exrate.betrag)

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
                         (Zinrstat.datum >= datum1) & (Zinrstat.datum <= lto_date) & (Zinrstat.zinr == to_string(rmno))).order_by(Zinrstat._recid).all():

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
                         (Zinrstat.datum >= pfrom_date) & (Zinrstat.datum <= pto_date) & (Zinrstat.zinr == to_string(rmno))).order_by(Zinrstat._recid).all():

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

        w1.done = True

        if w11:
            w11.done = True

        if w12:
            w12.done = True

        if w13:
            w13.done = True


    def fill_value1(recid1_w1:int, recid2_w1:int, val_sign:int):

        nonlocal error_nr, msg_str, lvcarea, frate, prog_error, serv_vat, price_decimal, segmentstat, htparam, zimmer, zimkateg, zkstat, zinrstat, h_umsatz, segment, uebertrag, artikel, h_artikel, umsatz, budget
        nonlocal pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, pfrom_date, pto_date, lytoday_flag, lytoday, foreign_flag, budget_flag, w1_list, w2_list
        nonlocal segmbuff


        nonlocal w1, w2, segmbuff, curr_child, ww1, ww2, w11, w12, w13, w11, w12, w11, tbuff, w1a, w11, w12, w13, w22, w11, w12, w11, w12, w11, w12, w11, w22, w753, w754, w755, w11, w11, w11, w11, w12, w13, w756, w757, w758, w11, w12, w13, parent, child, curr_child, curr_w2

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
        parent.lastmon =  to_decimal(parent.lastmon) + to_decimal(val_sign) * to_decimal(child.lastmon)
        parent.lm_budget =  to_decimal(parent.lm_budget) + to_decimal(val_sign) * to_decimal(child.lm_budget)
        parent.lastyr =  to_decimal(parent.lastyr) + to_decimal(val_sign) * to_decimal(child.lastyr)
        parent.ly_budget =  to_decimal(parent.ly_budget) + to_decimal(val_sign) * to_decimal(child.ly_budget)
        parent.ytd_saldo =  to_decimal(parent.ytd_saldo) + to_decimal(val_sign) * to_decimal(child.ytd_saldo)
        parent.ytd_budget =  to_decimal(parent.ytd_budget) + to_decimal(val_sign) * to_decimal(child.ytd_budget)
        parent.lytd_saldo =  to_decimal(parent.lytd_saldo) + to_decimal(val_sign) * to_decimal(child.lytd_saldo)
        parent.lytd_budget =  to_decimal(parent.lytd_budget) + to_decimal(val_sign) * to_decimal(child.lytd_budget)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
    serv_vat = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger
    fill_value()

    return generate_output()