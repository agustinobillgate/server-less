from functions.additional_functions import *
import decimal
from datetime import date
import re
from functions.calc_servvat import calc_servvat
from models import Parameters, Exrate, Htparam, Artikel, Umsatz, Budget, Genstat, Segmentstat

def gl_parxls1_combobl(foreign_flag:bool, from_date:date, to_date:date, t_parameters:[T_parameters]):
    w1_list = []
    prev_str:str = ""
    done_segment:bool = False
    datum1:date = None
    jan1:date = None
    ljan1:date = None
    lfrom_date:date = None
    lto_date:date = None
    do_it:bool = True
    curr_date:date = None
    serv:decimal = 0
    vat:decimal = 0
    fact:decimal = 0
    n_betrag:decimal = 0
    frate:decimal = 1
    price_decimal:int = 0
    parameters = exrate = htparam = artikel = umsatz = budget = genstat = segmentstat = None

    t_parameters = w1 = buff_exrate = s_param = w_rev = w_pers = w_room = None

    t_parameters_list, T_parameters = create_model_like(Parameters)
    w1_list, W1 = create_model("W1", {"nr":int, "varname":str, "main_code":int, "s_artnr":str, "artnr":int, "dept":int, "grpflag":int, "done":bool, "bezeich":str, "int_flag":bool, "tday":decimal, "tday_serv":decimal, "tday_tax":decimal, "mtd_serv":decimal, "mtd_tax":decimal, "ytd_serv":decimal, "ytd_tax":decimal, "yesterday":decimal, "saldo":decimal, "lastmon":decimal, "pmtd_serv":decimal, "pmtd_tax":decimal, "lmtd_serv":decimal, "lmtd_tax":decimal, "lastyr":decimal, "lytoday":decimal, "ytd_saldo":decimal, "lytd_saldo":decimal, "year_saldo":[decimal, 12], "mon_saldo":[decimal, 31], "mon_budget":[decimal, 31], "mon_lmtd":[decimal, 31], "tbudget":decimal, "budget":decimal, "lm_budget":decimal, "lm_today":decimal, "lm_today_serv":decimal, "lm_today_tax":decimal, "lm_mtd":decimal, "lm_ytd":decimal, "ly_budget":decimal, "ny_budget":decimal, "ytd_budget":decimal, "nytd_budget":decimal, "nmtd_budget":decimal, "lytd_budget":decimal})

    Buff_exrate = Exrate
    S_param = T_parameters
    s_param_list = t_parameters_list

    W_rev = W1
    w_rev_list = w1_list

    W_pers = W1
    w_pers_list = w1_list

    W_room = W1
    w_room_list = w1_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal w1_list, prev_str, done_segment, datum1, jan1, ljan1, lfrom_date, lto_date, do_it, curr_date, serv, vat, fact, n_betrag, frate, price_decimal, parameters, exrate, htparam, artikel, umsatz, budget, genstat, segmentstat
        nonlocal buff_exrate, s_param, w_rev, w_pers, w_room


        nonlocal t_parameters, w1, buff_exrate, s_param, w_rev, w_pers, w_room
        nonlocal t_parameters_list, w1_list
        return {"w1": w1_list}

    def fill_revenue():

        nonlocal w1_list, prev_str, done_segment, datum1, jan1, ljan1, lfrom_date, lto_date, do_it, curr_date, serv, vat, fact, n_betrag, frate, price_decimal, parameters, exrate, htparam, artikel, umsatz, budget, genstat, segmentstat
        nonlocal buff_exrate, s_param, w_rev, w_pers, w_room


        nonlocal t_parameters, w1, buff_exrate, s_param, w_rev, w_pers, w_room
        nonlocal t_parameters_list, w1_list

        prev_param:str = ""
        ytd_flag:bool = False
        lytd_flag:bool = False
        lmtd_flag:bool = False
        ytd_budget_flag:bool = False
        mtd_budget_flag:bool = False
        mm:int = 0
        S_param = T_parameters

        for s_param in query(s_param_list, filters=(lambda s_param :num_entries(s_param.vstring, ":") == 1 and num_entries(s_param.varname, "-") == 3 and entry(2, s_param.varname, "-") == "comboREV")):

            if prev_param != s_param.varname:
                prev_param = s_param.varname

                w1 = query(w1_list, filters=(lambda w1 :w1.nr == 4 and w1.s_artnr == s_param.vstring), first=True)

                if not w1:
                    w1 = W1()
                    w1_list.append(w1)

                    w1.nr = 4
                    w1.s_artnr = s_param.vstring

                if s_param.vtype == 24:
                    ytd_flag = True

                if s_param.vtype == 84:
                    mtd_budget_flag = True

                if s_param.vtype == 85:
                    ytd_budget_flag = True

                if s_param.vtype == 86:
                    lmtd_flag = True

                if s_param.vtype == 87:
                    lytd_flag = True

        for w1 in query(w1_list, filters=(lambda w1 :w1.nr == 4)):

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == to_int(substring(w1.s_artnr, 2))) &  (Artikel.departement == to_int(substring(w1.s_artnr, 0, 2)))).first()

            if artikel:

                if ytd_flag:
                    datum1 = jan1
                else:
                    datum1 = from_date
                mm = get_month(to_date)

                for umsatz in db_session.query(Umsatz).filter(
                        (Umsatz.datum >= datum1) &  (Umsatz.datum <= to_date) &  (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.departement)).all():
                    serv = 0
                    vat = 0


                    serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                    fact = 1.00 + serv + vat
                    n_betrag = 0

                    if foreign_flag:
                        find_exrate(curr_date)

                        if buff_exrate:
                            frate = buff_exrate.betrag
                    n_betrag = umsatz.betrag / (fact * frate)
                    n_betrag = round(n_betrag, 2)

                    if umsatz.datum == to_date:
                        w1.tday = w1.tday + n_betrag

                    if get_month(umsatz.datum) == mm:
                        w1.saldo = w1.saldo + n_betrag
                    w1.ytd_saldo = w1.ytd_saldo + n_betrag

                if lmtd_flag or lytd_flag:

                    if lytd_flag:
                        datum1 = ljan1
                    else:
                        datum1 = lfrom_date
                    mm = get_month(lto_date)

                    for umsatz in db_session.query(Umsatz).filter(
                            (Umsatz.datum >= datum1) &  (Umsatz.datum <= lto_date) &  (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.departement)).all():
                        serv = 0
                        vat = 0


                        serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                        fact = 1.00 + serv + vat
                        n_betrag = 0

                        if foreign_flag:
                            find_exrate(curr_date)

                            if buff_exrate:
                                frate = buff_exrate.betrag
                        n_betrag = umsatz.betrag / (fact * frate)
                        n_betrag = round(n_betrag, 2)

                        if get_month(umsatz.datum) == mm:
                            w1.lastyr = w1.lastyr + n_betrag
                        w1.lytd_saldo = w1.lytd_saldo + n_betrag

                if mtd_budget_flag or ytd_budget_flag:

                    if ytd_budget_flag:
                        datum1 = jan1
                    else:
                        datum1 = from_date
                    mm = get_month(to_date)

                    for budget in db_session.query(Budget).filter(
                            (Budget.artnr == artikel.artnr) &  (Budget.departement == artikel.departement) &  (Budget.datum >= datum1) &  (Budget.datum <= to_date)).all():

                        if budget.datum == to_date:
                            w1.tbudget = w1.tbudget + budget.betrag

                        if get_month(budget.datum) == mm:
                            w1.budget = w1.budget + budget.betrag
                        w1.ytd_budget = w1.ytd_budget + budget.betrag

    def fill_segment():

        nonlocal w1_list, prev_str, done_segment, datum1, jan1, ljan1, lfrom_date, lto_date, do_it, curr_date, serv, vat, fact, n_betrag, frate, price_decimal, parameters, exrate, htparam, artikel, umsatz, budget, genstat, segmentstat
        nonlocal buff_exrate, s_param, w_rev, w_pers, w_room


        nonlocal t_parameters, w1, buff_exrate, s_param, w_rev, w_pers, w_room
        nonlocal t_parameters_list, w1_list

        prev_param:str = ""
        ytd_flag:bool = False
        lytd_flag:bool = False
        lmtd_flag:bool = False
        ytd_budget_flag:bool = False
        mtd_budget_flag:bool = False
        nr:int = 0
        segm:int = 0
        mm:int = 0
        prev_segm:int = 0
        S_param = T_parameters
        W_rev = W1
        W_pers = W1
        W_room = W1

        for s_param in query(s_param_list, filters=(lambda s_param :num_entries(s_param.vstring, ":") == 1 and num_entries(s_param.varname, "-") == 3 and entry(2, s_param.varname, "-") == "comboFO" and substring(s_param.vstring, 0, 4) == "segm")):

            if prev_param != s_param.varname:
                prev_param = s_param.varname

                if entry(0, s_param.vstring, "-") == "segmrev":
                    nr = 1

                elif entry(0, s_param.vstring, "-") == "segmpers":
                    nr = 2

                elif entry(0, s_param.vstring, "-") == "segmroom":
                    nr = 3

                if num_entries(s_param.vstring, "-") > 1:
                    segm = to_int(entry(1, s_param.vstring, "-"))

                w1 = query(w1_list, filters=(lambda w1 :w1.nr == nr and w1.artnr == segm), first=True)

                if not w1:
                    w1 = W1()
                    w1_list.append(w1)

                    w1.nr = nr
                    w1.artnr = segm

                if s_param.vtype == 24:
                    ytd_flag = True

                if s_param.vtype == 84:
                    mtd_budget_flag = True

                if s_param.vtype == 85:
                    ytd_budget_flag = True

                if s_param.vtype == 86:
                    lmtd_flag = True

                if s_param.vtype == 87:
                    lytd_flag = True

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date
        mm = get_month(to_date)

        for genstat in db_session.query(Genstat).filter(
                (Genstat.datum >= datum1) &  (Genstat.datum <= to_date) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():

            if prev_segm != genstat.segmentcode:
                prev_segm = genstat.segmentcode

                w_rev = query(w_rev_list, filters=(lambda w_rev :w_rev.nr == 1 and w_rev.artnr == genstat.segmentcode), first=True)

                w_pers = query(w_pers_list, filters=(lambda w_pers :w_pers.nr == 2 and w_pers.artnr == genstat.segmentcode), first=True)

                w_room = query(w_room_list, filters=(lambda w_room :w_room.nr == 3 and w_room.artnr == genstat.segmentcode), first=True)

            if genstat.datum == to_date:

                if w_rev:
                    w_rev.tday = w_rev.tday + genstat.logis

                if w_pers:
                    w_pers.tday = w_pers.tday + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                if w_room:
                    w_room.tday = w_room.tday + 1

            if get_month(genstat.datum) == mm:

                if w_rev:
                    w_rev.saldo = w_rev.saldo + genstat.logis

                if w_pers:
                    w_pers.saldo = w_pers.saldo + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                if w_room:
                    w_room.saldo = w_room.saldo + 1

            if w_rev:
                w_rev.ytd_saldo = w_rev.ytd_saldo + genstat.logis

            if w_pers:
                w_pers.ytd_saldo = w_pers.ytd_saldo + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

            if w_room:
                w_room.ytd_saldo = w_room.ytd_saldo + 1

        if lmtd_flag or lytd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date
            mm = get_month(lto_date)
            prev_segm = 0

            for genstat in db_session.query(Genstat).filter(
                    (Genstat.datum >= datum1) &  (Genstat.datum <= lto_date) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():

                if prev_segm != genstat.segmentcode:
                    prev_segm = genstat.segmentcode

                    w_rev = query(w_rev_list, filters=(lambda w_rev :w_rev.nr == 1 and w_rev.artnr == genstat.segmentcode), first=True)

                    w_pers = query(w_pers_list, filters=(lambda w_pers :w_pers.nr == 2 and w_pers.artnr == genstat.segmentcode), first=True)

                    w_room = query(w_room_list, filters=(lambda w_room :w_room.nr == 3 and w_room.artnr == genstat.segmentcode), first=True)

                if genstat.datum == to_date:

                    if w_rev:
                        w_rev.lytoday = w_rev.lytoday + genstat.logis

                    if w_pers:
                        w_pers.lytoday = w_pers.lytoday + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                    if w_room:
                        w_room.lytoday = w_room.lytoday + 1

                if get_month(genstat.datum) == mm:

                    if w_rev:
                        w_rev.lastyr = w_rev.lastyr + genstat.logis

                    if w_pers:
                        w_pers.lastyr = w_pers.lastyr + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                    if w_room:
                        w_room.lastyr = w_room.lastyr + 1

                if w_rev:
                    w_rev.lytd_saldo = w_rev.lytd_saldo + genstat.logis

                if w_pers:
                    w_pers.lytd_saldo = w_pers.lytd_saldo + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                if w_room:
                    w_room.lytd_saldo = w_room.lytd_saldo + 1

        if mtd_budget_flag or ytd_budget_flag:

            if ytd_budget_flag:
                datum1 = jan1
            else:
                datum1 = from_date
            mm = get_month(to_date)
            prev_segm = 0

            for segmentstat in db_session.query(Segmentstat).filter(
                    (Segmentstat.datum >= datum1) &  (Segmentstat.datum <= to_date)).all():

                if prev_segm != segmentstat.segmentcode:
                    prev_segm = segmentstat.segmentcode

                    w_rev = query(w_rev_list, filters=(lambda w_rev :w_rev.nr == 1 and w_rev.artnr == segmentstat.segmentcode), first=True)

                    w_pers = query(w_pers_list, filters=(lambda w_pers :w_pers.nr == 2 and w_pers.artnr == segmentstat.segmentcode), first=True)

                    w_room = query(w_room_list, filters=(lambda w_room :w_room.nr == 3 and w_room.artnr == segmentstat.segmentcode), first=True)

                if segmentstat.datum == to_date:

                    if w_rev:
                        w_rev.tbudget = w_rev.tbudget + segmentstat.budlogis

                    if w_pers:
                        w_pers.tbudget = w_pers.tbudget + segmentstat.budpersanz

                    if w_room:
                        w_room.tbudget = w_room.tbudget + 1

                if get_month(segmentstat.datum) == mm:

                    if w_rev:
                        w_rev.budget = w_rev.budget + segmentstat.budlogis

                    if w_pers:
                        w_pers.budget = w_pers.budget + segmentstat.budpersanz

                    if w_room:
                        w_room.budget = w_room.budget + 1

                if w_rev:
                    w_rev.ytd_budget = w_rev.ytd_budget + segmentstat.budlogis

                if w_pers:
                    w_pers.ytd_budget = w_pers.ytd_budget + segmentstat.budpersanz

                if w_room:
                    w_room.ytd_budget = w_room.ytd_budget + 1


    if (get_month(to_date) != 2) or (get_day(to_date) != 29):
        lto_date = date_mdy(get_month(to_date) , get_day(to_date) , get_year(to_date) - 1)
    else:
        lto_date = date_mdy(get_month(to_date) , 28, get_year(to_date) - 1)
    jan1 = date_mdy(1, 1, get_year(to_date))
    ljan1 = date_mdy(1, 1, get_year(to_date) - 1)
    lfrom_date = date_mdy(get_month(to_date) , 1, get_year(to_date) - 1)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    t_parameters = query(t_parameters_list, filters=(lambda t_parameters :num_entries(t_parameters.varname, "-") == 3 and entry(2, t_parameters.varname, "-") == "comboREV"), first=True)

    if t_parameters:
        fill_revenue()

    t_parameters = query(t_parameters_list, filters=(lambda t_parameters :(re.match(".*segmrev.*",t_parameters.vstring) or re.match(".*segmpers.*",t_parameters.vstring) or re.match(".*segmroom.*",t_parameters.vstring)) and num_entries(t_parameters.varname, "-") == 3 and entry(2, t_parameters.varname, "-") == "comboFO"), first=True)

    if t_parameters:
        fill_segment()

    return generate_output()