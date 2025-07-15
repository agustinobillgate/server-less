#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from models import Parameters, Exrate, Htparam, Artikel, Umsatz, Budget, Genstat, Segmentstat

t_parameters_data, T_parameters = create_model_like(Parameters)

def gl_parxls1_combobl(foreign_flag:bool, from_date:date, to_date:date, t_parameters_data:[T_parameters]):

    prepare_cache ([Exrate, Htparam, Artikel, Umsatz, Budget, Genstat, Segmentstat])

    w1_data = []
    prev_str:string = ""
    done_segment:bool = False
    datum1:date = None
    jan1:date = None
    ljan1:date = None
    lfrom_date:date = None
    lto_date:date = None
    do_it:bool = True
    curr_date:date = None
    serv:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    fact:Decimal = to_decimal("0.0")
    n_betrag:Decimal = to_decimal("0.0")
    frate:Decimal = 1
    price_decimal:int = 0
    parameters = exrate = htparam = artikel = umsatz = budget = genstat = segmentstat = None

    t_parameters = w1 = buff_exrate = s_param = s_param = w_rev = w_pers = w_room = None

    w1_data, W1 = create_model("W1", {"nr":int, "varname":string, "main_code":int, "s_artnr":string, "artnr":int, "dept":int, "grpflag":int, "done":bool, "bezeich":string, "int_flag":bool, "tday":Decimal, "tday_serv":Decimal, "tday_tax":Decimal, "mtd_serv":Decimal, "mtd_tax":Decimal, "ytd_serv":Decimal, "ytd_tax":Decimal, "yesterday":Decimal, "saldo":Decimal, "lastmon":Decimal, "pmtd_serv":Decimal, "pmtd_tax":Decimal, "lmtd_serv":Decimal, "lmtd_tax":Decimal, "lastyr":Decimal, "lytoday":Decimal, "ytd_saldo":Decimal, "lytd_saldo":Decimal, "year_saldo":[Decimal,12], "mon_saldo":[Decimal,31], "mon_budget":[Decimal,31], "mon_lmtd":[Decimal,31], "tbudget":Decimal, "budget":Decimal, "lm_budget":Decimal, "lm_today":Decimal, "lm_today_serv":Decimal, "lm_today_tax":Decimal, "lm_mtd":Decimal, "lm_ytd":Decimal, "ly_budget":Decimal, "ny_budget":Decimal, "ytd_budget":Decimal, "nytd_budget":Decimal, "nmtd_budget":Decimal, "lytd_budget":Decimal})

    Buff_exrate = create_buffer("Buff_exrate",Exrate)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal w1_data, prev_str, done_segment, datum1, jan1, ljan1, lfrom_date, lto_date, do_it, curr_date, serv, vat, fact, n_betrag, frate, price_decimal, parameters, exrate, htparam, artikel, umsatz, budget, genstat, segmentstat
        nonlocal foreign_flag, from_date, to_date
        nonlocal buff_exrate


        nonlocal t_parameters, w1, buff_exrate, s_param, s_param, w_rev, w_pers, w_room
        nonlocal w1_data

        return {"w1": w1_data}

    def fill_revenue():

        nonlocal w1_data, prev_str, done_segment, datum1, jan1, ljan1, lfrom_date, lto_date, do_it, curr_date, serv, vat, fact, n_betrag, frate, price_decimal, parameters, exrate, htparam, artikel, umsatz, budget, genstat, segmentstat
        nonlocal foreign_flag, from_date, to_date
        nonlocal buff_exrate


        nonlocal t_parameters, w1, buff_exrate, s_param, s_param, w_rev, w_pers, w_room
        nonlocal w1_data

        prev_param:string = ""
        ytd_flag:bool = False
        lytd_flag:bool = False
        lmtd_flag:bool = False
        ytd_budget_flag:bool = False
        mtd_budget_flag:bool = False
        mm:int = 0
        S_param = T_parameters
        s_param_data = t_parameters_data

        for s_param in query(s_param_data, filters=(lambda s_param: s_param.num_entries(s_param.vstring, ":") == 1 and num_entries(s_param.varname, "-") == 3 and entry(2, s_param.varname, "-") == ("comboREV").lower()), sort_by=[("varname",False)]):

            if prev_param != s_param.varname:
                prev_param = s_param.varname

                w1 = query(w1_data, filters=(lambda w1: w1.nr == 4 and w1.s_artnr == s_param.vstring), first=True)

                if not w1:
                    w1 = W1()
                    w1_data.append(w1)

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

        for w1 in query(w1_data, filters=(lambda w1: w1.nr == 4), sort_by=[("s_artnr",False)]):

            artikel = get_cache (Artikel, {"artnr": [(eq, to_int(substring(w1.s_artnr, 2)))],"departement": [(eq, to_int(substring(w1.s_artnr, 0, 2)))]})

            if artikel:

                if ytd_flag:
                    datum1 = jan1
                else:
                    datum1 = from_date
                mm = get_month(to_date)

                for umsatz in db_session.query(Umsatz).filter(
                         (Umsatz.datum >= datum1) & (Umsatz.datum <= to_date) & (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement)).order_by(Umsatz._recid).all():
                    serv =  to_decimal("0")
                    vat =  to_decimal("0")


                    serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                    fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)
                    n_betrag =  to_decimal("0")

                    if foreign_flag:
                        find_exrate(curr_date)

                        if buff_exrate:
                            frate =  to_decimal(buff_exrate.betrag)
                    n_betrag =  to_decimal(umsatz.betrag) / to_decimal((fact) * to_decimal(frate))
                    n_betrag = to_decimal(round(n_betrag , 2))

                    if umsatz.datum == to_date:
                        w1.tday =  to_decimal(w1.tday) + to_decimal(n_betrag)

                    if get_month(umsatz.datum) == mm:
                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(n_betrag)
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(n_betrag)

                if lmtd_flag or lytd_flag:

                    if lytd_flag:
                        datum1 = ljan1
                    else:
                        datum1 = lfrom_date
                    mm = get_month(lto_date)

                    for umsatz in db_session.query(Umsatz).filter(
                             (Umsatz.datum >= datum1) & (Umsatz.datum <= lto_date) & (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement)).order_by(Umsatz._recid).all():
                        serv =  to_decimal("0")
                        vat =  to_decimal("0")


                        serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                        fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)
                        n_betrag =  to_decimal("0")

                        if foreign_flag:
                            find_exrate(curr_date)

                            if buff_exrate:
                                frate =  to_decimal(buff_exrate.betrag)
                        n_betrag =  to_decimal(umsatz.betrag) / to_decimal((fact) * to_decimal(frate))
                        n_betrag = to_decimal(round(n_betrag , 2))

                        if get_month(umsatz.datum) == mm:
                            w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(n_betrag)
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(n_betrag)

                if mtd_budget_flag or ytd_budget_flag:

                    if ytd_budget_flag:
                        datum1 = jan1
                    else:
                        datum1 = from_date
                    mm = get_month(to_date)

                    for budget in db_session.query(Budget).filter(
                             (Budget.artnr == artikel.artnr) & (Budget.departement == artikel.departement) & (Budget.datum >= datum1) & (Budget.datum <= to_date)).order_by(Budget._recid).all():

                        if budget.datum == to_date:
                            w1.tbudget =  to_decimal(w1.tbudget) + to_decimal(budget.betrag)

                        if get_month(budget.datum) == mm:
                            w1.budget =  to_decimal(w1.budget) + to_decimal(budget.betrag)
                        w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(budget.betrag)


    def fill_segment():

        nonlocal w1_data, prev_str, done_segment, datum1, jan1, ljan1, lfrom_date, lto_date, do_it, curr_date, serv, vat, fact, n_betrag, frate, price_decimal, parameters, exrate, htparam, artikel, umsatz, budget, genstat, segmentstat
        nonlocal foreign_flag, from_date, to_date
        nonlocal buff_exrate


        nonlocal t_parameters, w1, buff_exrate, s_param, s_param, w_rev, w_pers, w_room
        nonlocal w1_data

        prev_param:string = ""
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
        s_param_data = t_parameters_data
        W_rev = W1
        w_rev_data = w1_data
        W_pers = W1
        w_pers_data = w1_data
        W_room = W1
        w_room_data = w1_data

        for s_param in query(s_param_data, filters=(lambda s_param: s_param.num_entries(s_param.vstring, ":") == 1 and num_entries(s_param.varname, "-") == 3 and entry(2, s_param.varname, "-") == ("comboFO").lower()  and substring(s_param.vstring, 0, 4) == ("segm").lower()), sort_by=[("varname",False)]):

            if prev_param != s_param.varname:
                prev_param = s_param.varname

                if entry(0, s_param.vstring, "-") == ("segmrev").lower() :
                    nr = 1

                elif entry(0, s_param.vstring, "-") == ("segmpers").lower() :
                    nr = 2

                elif entry(0, s_param.vstring, "-") == ("segmroom").lower() :
                    nr = 3

                if num_entries(s_param.vstring, "-") > 1:
                    segm = to_int(entry(1, s_param.vstring, "-"))

                w1 = query(w1_data, filters=(lambda w1: w1.nr == nr and w1.artnr == segm), first=True)

                if not w1:
                    w1 = W1()
                    w1_data.append(w1)

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
                 (Genstat.datum >= datum1) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.segmentcode).all():

            if prev_segm != genstat.segmentcode:
                prev_segm = genstat.segmentcode

                w_rev = query(w_rev_data, filters=(lambda w_rev: w_rev.nr == 1 and w_rev.artnr == genstat.segmentcode), first=True)

                w_pers = query(w_pers_data, filters=(lambda w_pers: w_pers.nr == 2 and w_pers.artnr == genstat.segmentcode), first=True)

                w_room = query(w_room_data, filters=(lambda w_room: w_room.nr == 3 and w_room.artnr == genstat.segmentcode), first=True)

            if genstat.datum == to_date:

                if w_rev:
                    w_rev.tday =  to_decimal(w_rev.tday) + to_decimal(genstat.logis)

                if w_pers:
                    w_pers.tday =  to_decimal(w_pers.tday) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                if w_room:
                    w_room.tday =  to_decimal(w_room.tday) + to_decimal("1")

            if get_month(genstat.datum) == mm:

                if w_rev:
                    w_rev.saldo =  to_decimal(w_rev.saldo) + to_decimal(genstat.logis)

                if w_pers:
                    w_pers.saldo =  to_decimal(w_pers.saldo) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                if w_room:
                    w_room.saldo =  to_decimal(w_room.saldo) + to_decimal("1")

            if w_rev:
                w_rev.ytd_saldo =  to_decimal(w_rev.ytd_saldo) + to_decimal(genstat.logis)

            if w_pers:
                w_pers.ytd_saldo =  to_decimal(w_pers.ytd_saldo) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

            if w_room:
                w_room.ytd_saldo =  to_decimal(w_room.ytd_saldo) + to_decimal("1")

        if lmtd_flag or lytd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date
            mm = get_month(lto_date)
            prev_segm = 0

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum >= datum1) & (Genstat.datum <= lto_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.segmentcode).all():

                if prev_segm != genstat.segmentcode:
                    prev_segm = genstat.segmentcode

                    w_rev = query(w_rev_data, filters=(lambda w_rev: w_rev.nr == 1 and w_rev.artnr == genstat.segmentcode), first=True)

                    w_pers = query(w_pers_data, filters=(lambda w_pers: w_pers.nr == 2 and w_pers.artnr == genstat.segmentcode), first=True)

                    w_room = query(w_room_data, filters=(lambda w_room: w_room.nr == 3 and w_room.artnr == genstat.segmentcode), first=True)

                if genstat.datum == to_date:

                    if w_rev:
                        w_rev.lytoday =  to_decimal(w_rev.lytoday) + to_decimal(genstat.logis)

                    if w_pers:
                        w_pers.lytoday =  to_decimal(w_pers.lytoday) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                    if w_room:
                        w_room.lytoday =  to_decimal(w_room.lytoday) + to_decimal("1")

                if get_month(genstat.datum) == mm:

                    if w_rev:
                        w_rev.lastyr =  to_decimal(w_rev.lastyr) + to_decimal(genstat.logis)

                    if w_pers:
                        w_pers.lastyr =  to_decimal(w_pers.lastyr) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                    if w_room:
                        w_room.lastyr =  to_decimal(w_room.lastyr) + to_decimal("1")

                if w_rev:
                    w_rev.lytd_saldo =  to_decimal(w_rev.lytd_saldo) + to_decimal(genstat.logis)

                if w_pers:
                    w_pers.lytd_saldo =  to_decimal(w_pers.lytd_saldo) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                if w_room:
                    w_room.lytd_saldo =  to_decimal(w_room.lytd_saldo) + to_decimal("1")

        if mtd_budget_flag or ytd_budget_flag:

            if ytd_budget_flag:
                datum1 = jan1
            else:
                datum1 = from_date
            mm = get_month(to_date)
            prev_segm = 0

            for segmentstat in db_session.query(Segmentstat).filter(
                     (Segmentstat.datum >= datum1) & (Segmentstat.datum <= to_date)).order_by(Segmentstat.segmentcode).all():

                if prev_segm != segmentstat.segmentcode:
                    prev_segm = segmentstat.segmentcode

                    w_rev = query(w_rev_data, filters=(lambda w_rev: w_rev.nr == 1 and w_rev.artnr == segmentstat.segmentcode), first=True)

                    w_pers = query(w_pers_data, filters=(lambda w_pers: w_pers.nr == 2 and w_pers.artnr == segmentstat.segmentcode), first=True)

                    w_room = query(w_room_data, filters=(lambda w_room: w_room.nr == 3 and w_room.artnr == segmentstat.segmentcode), first=True)

                if segmentstat.datum == to_date:

                    if w_rev:
                        w_rev.tbudget =  to_decimal(w_rev.tbudget) + to_decimal(segmentstat.budlogis)

                    if w_pers:
                        w_pers.tbudget =  to_decimal(w_pers.tbudget) + to_decimal(segmentstat.budpersanz)

                    if w_room:
                        w_room.tbudget =  to_decimal(w_room.tbudget) + to_decimal("1")

                if get_month(segmentstat.datum) == mm:

                    if w_rev:
                        w_rev.budget =  to_decimal(w_rev.budget) + to_decimal(segmentstat.budlogis)

                    if w_pers:
                        w_pers.budget =  to_decimal(w_pers.budget) + to_decimal(segmentstat.budpersanz)

                    if w_room:
                        w_room.budget =  to_decimal(w_room.budget) + to_decimal("1")

                if w_rev:
                    w_rev.ytd_budget =  to_decimal(w_rev.ytd_budget) + to_decimal(segmentstat.budlogis)

                if w_pers:
                    w_pers.ytd_budget =  to_decimal(w_pers.ytd_budget) + to_decimal(segmentstat.budpersanz)

                if w_room:
                    w_room.ytd_budget =  to_decimal(w_room.ytd_budget) + to_decimal("1")

    if (get_month(to_date) != 2) or (get_day(to_date) != 29):
        lto_date = date_mdy(get_month(to_date) , get_day(to_date) , get_year(to_date) - timedelta(days=1))
    else:
        lto_date = date_mdy(get_month(to_date) , 28, get_year(to_date) - timedelta(days=1))
    jan1 = date_mdy(1, 1, get_year(to_date))
    ljan1 = date_mdy(1, 1, get_year(to_date) - timedelta(days=1))
    lfrom_date = date_mdy(get_month(to_date) , 1, get_year(to_date) - timedelta(days=1))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    t_parameters = query(t_parameters_data, filters=(lambda t_parameters: t_parameters.num_entries(t_parameters.varname, "-") == 3 and entry(2, t_parameters.varname, "-") == ("comboREV").lower()), first=True)

    if t_parameters:
        fill_revenue()

    t_parameters = query(t_parameters_data, filters=(lambda t_parameters: matches((t_parameters.vstring,r"*segmrev*") or matches(t_parameters.vstring,r"*segmpers*") or matches(t_parameters.vstring,r"*segmroom*")) and num_entries(t_parameters.varname, "-") == 3 and entry(2, t_parameters.varname, "-") == ("comboFO").lower()), first=True)

    if t_parameters:
        fill_segment()

    return generate_output()