#using conversion tools version: 1.0.0.62

from functions.additional_functions import *
import decimal
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Guest, Genstat, Nation, Htparam, Arrangement, Artikel

def ta_nationstat_go_listbl(from_date:str, last_period:str, sorttype:int, text2:str, text3:str):
    ta_nat_stat_list = []
    sub_mrm:int = 0
    sub_mlod:decimal = to_decimal("0.0")
    sub_margt:decimal = to_decimal("0.0")
    sub_yrm:int = 0
    sub_ylod:decimal = to_decimal("0.0")
    sub_yargt:decimal = to_decimal("0.0")
    grand_mrm:int = 0
    grand_mlod:decimal = to_decimal("0.0")
    grand_margt:decimal = to_decimal("0.0")
    grand_yrm:int = 0
    grand_ylod:decimal = to_decimal("0.0")
    grand_yargt:decimal = to_decimal("0.0")
    guest = genstat = nation = htparam = arrangement = artikel = None

    ta_nat_stat = tmp_list = None

    ta_nat_stat_list, Ta_nat_stat = create_model("Ta_nat_stat", {"nr":int, "ta_name":str, "nation":str, "rmnite":str, "logiumz":str, "argtumz":str, "ytd_rmnite":str, "ytd_logi":str, "ytd_argt":str})
    tmp_list_list, Tmp_list = create_model("Tmp_list", {"gastnr":int, "ta_name":str, "nation":str, "rmnite":int, "argtumz":decimal, "logiumz":decimal, "ytd_rmnite":int, "ytd_argt":decimal, "ytd_logi":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ta_nat_stat_list, sub_mrm, sub_mlod, sub_margt, sub_yrm, sub_ylod, sub_yargt, grand_mrm, grand_mlod, grand_margt, grand_yrm, grand_ylod, grand_yargt, guest, genstat, nation, htparam, arrangement, artikel
        nonlocal from_date, last_period, sorttype, text2, text3


        nonlocal ta_nat_stat, tmp_list
        nonlocal ta_nat_stat_list, tmp_list_list

        return {"ta-nat-stat": ta_nat_stat_list}

    def create_list():

        nonlocal ta_nat_stat_list, sub_mrm, sub_mlod, sub_margt, sub_yrm, sub_ylod, sub_yargt, grand_mrm, grand_mlod, grand_margt, grand_yrm, grand_ylod, grand_yargt, guest, genstat, nation, htparam, arrangement, artikel
        nonlocal from_date, last_period, sorttype, text2, text3


        nonlocal ta_nat_stat, tmp_list
        nonlocal ta_nat_stat_list, tmp_list_list

        argt_ums:decimal = to_decimal("0.0")
        nat:str = ""
        yr:int = 0
        mm:int = 0
        status_vat:bool = False
        vat:decimal = to_decimal("0.0")
        service:decimal = to_decimal("0.0")
        vat2:decimal = to_decimal("0.0")
        fact:decimal = to_decimal("0.0")
        mm = to_int(to_string(substring(from_date, 0, 2) , "99"))
        yr = to_int(to_string(substring(from_date, 2, 4) , "9999"))
        tmp_list_list.clear()

        genstat_obj_list = []
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                 (get_year(Genstat.datum) == yr) & (get_month(Genstat.datum) <= mm) & (Genstat.zinr != "") & (Genstat.karteityp == 2) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            nation = db_session.query(Nation).filter(
                     (Nation.kurzbez == guest.land)).first()

            if nation:
                nat = nation.kurzbez
            else:
                nat = "***"

            tmp_list = query(tmp_list_list, filters=(lambda tmp_list: tmp_list.gastnr == genstat.gastnr and tmp_list.nation.lower()  == (nat).lower()), first=True)

            if not tmp_list:
                tmp_list = Tmp_list()
                tmp_list_list.append(tmp_list)

                tmp_list.gastnr = genstat.gastnr
                tmp_list.ta_name = guest.name + ", " + guest.anredefirma
                tmp_list.nation = guest.land


            service =  to_decimal("0")
            vat =  to_decimal("0")

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 127)).first()
            status_vat = htparam.flogical

            arrangement = db_session.query(Arrangement).filter(
                     (Arrangement.arrangement == genstat.argt)).first()

            if arrangement:

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == arrangement.artnr_logis) & (Artikel.departement == 0)).first()

            if artikel and status_vat :
                service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))
                vat =  to_decimal(vat) + to_decimal(vat2)

            if genstat.resstatus != 13:
                tmp_list.ytd_rmnite = tmp_list.ytd_rmnite + 1
            tmp_list.ytd_logi =  to_decimal(tmp_list.ytd_logi) + to_decimal(genstat.logis)
            tmp_list.ytd_argt =  to_decimal(tmp_list.argtumz) + to_decimal((genstat.ratelocal) / to_decimal((1) + to_decimal(vat) + to_decimal(service)))

            if get_month(genstat.datum) == mm and get_year(genstat.datum) == yr:

                if genstat.resstatus != 13:
                    tmp_list.rmnite = tmp_list.rmnite + 1
                tmp_list.logiumz =  to_decimal(tmp_list.logiumz) + to_decimal(genstat.logis)
                tmp_list.argtumz =  to_decimal(tmp_list.argtumz) + to_decimal((genstat.ratelocal) / to_decimal((1) + to_decimal(vat) + to_decimal(service)))


    def create_browse():

        nonlocal ta_nat_stat_list, sub_mrm, sub_mlod, sub_margt, sub_yrm, sub_ylod, sub_yargt, grand_mrm, grand_mlod, grand_margt, grand_yrm, grand_ylod, grand_yargt, guest, genstat, nation, htparam, arrangement, artikel
        nonlocal from_date, last_period, sorttype, text2, text3


        nonlocal ta_nat_stat, tmp_list
        nonlocal ta_nat_stat_list, tmp_list_list

        i:int = 0
        curr_gastnr:int = 0
        it_exists:bool = False
        s:str = ""
        ta_nat_stat_list.clear()
        sub_mrm = 0
        sub_mlod =  to_decimal("0")
        sub_margt =  to_decimal("0")
        sub_yrm = 0
        sub_ylod =  to_decimal("0")
        sub_yargt =  to_decimal("0")
        grand_mrm = 0
        grand_mlod =  to_decimal("0")
        grand_margt =  to_decimal("0")
        grand_yrm = 0
        grand_ylod =  to_decimal("0")
        grand_yargt =  to_decimal("0")

        for tmp_list in query(tmp_list_list, sort_by=[("gastnr",False)]):

            if curr_gastnr != 0 and curr_gastnr != tmp_list.gastnr:
                i = i + 1
                ta_nat_stat = Ta_nat_stat()
                ta_nat_stat_list.append(ta_nat_stat)

                ta_nat_stat.nr = i


                i = i + 1
                ta_nat_stat = Ta_nat_stat()
                ta_nat_stat_list.append(ta_nat_stat)

                ta_nat_stat.nr = i
                ta_nat_stat.ta_name = text2
                ta_nat_stat.rmnite = to_string(sub_mrm, ">,>>9")
                ta_nat_stat.logiumz = to_string(sub_mlod, "->>>,>>>,>>9.99")
                ta_nat_stat.argtumz = to_string(sub_margt, "->>>,>>>,>>9.99")
                ta_nat_stat.ytd_rmnite = to_string(sub_yrm, ">>>,>>9")
                ta_nat_stat.ytd_logi = to_string(sub_ylod, "->>,>>>,>>>,>>9.99")
                ta_nat_stat.ytd_argt = to_string(sub_yargt, "->>,>>>,>>>,>>9.99")


                i = i + 1
                ta_nat_stat = Ta_nat_stat()
                ta_nat_stat_list.append(ta_nat_stat)

                ta_nat_stat.nr = i


                sub_mrm = 0
                sub_mlod =  to_decimal("0")
                sub_margt =  to_decimal("0")
                sub_yrm = 0
                sub_ylod =  to_decimal("0")
                sub_yargt =  to_decimal("0")


            i = i + 1
            ta_nat_stat = Ta_nat_stat()
            ta_nat_stat_list.append(ta_nat_stat)

            ta_nat_stat.nr = i
            ta_nat_stat.ta_name = to_string(tmp_list.ta_name, "x(36)")
            ta_nat_stat.nation = to_string(tmp_list.nation, "x(3)")
            ta_nat_stat.rmnite = to_string(tmp_list.rmnite, ">,>>9")
            ta_nat_stat.logiumz = to_string(tmp_list.logiumz, "->>>,>>>,>>9.99")
            ta_nat_stat.argtumz = to_string(tmp_list.argtumz, "->>>,>>>,>>9.99")
            ta_nat_stat.ytd_rmnite = to_string(tmp_list.ytd_rmnite, ">>>,>>9")
            ta_nat_stat.ytd_logi = to_string(tmp_list.ytd_logi, "->>,>>>,>>>,>>9.99")
            ta_nat_stat.ytd_argt = to_string(tmp_list.ytd_argt, "->>,>>>,>>>,>>9.99")


            sub_mrm = sub_mrm + tmp_list.rmnite
            sub_mlod =  to_decimal(sub_mlod) + to_decimal(tmp_list.logiumz)
            sub_margt =  to_decimal(sub_margt) + to_decimal(tmp_list.argtumz)
            sub_yrm = sub_yrm + tmp_list.ytd_rmnite
            sub_ylod =  to_decimal(sub_ylod) + to_decimal(tmp_list.ytd_logi)
            sub_yargt =  to_decimal(sub_yargt) + to_decimal(tmp_list.ytd_argt)
            grand_mrm = grand_mrm + tmp_list.rmnite
            grand_mlod =  to_decimal(grand_mlod) + to_decimal(tmp_list.logiumz)
            grand_margt =  to_decimal(grand_margt) + to_decimal(tmp_list.argtumz)
            grand_yrm = grand_yrm + tmp_list.ytd_rmnite
            grand_ylod =  to_decimal(grand_ylod) + to_decimal(tmp_list.ytd_logi)
            grand_yargt =  to_decimal(grand_yargt) + to_decimal(tmp_list.ytd_argt)
            it_exists = True
            curr_gastnr = tmp_list.gastnr


        if it_exists:
            i = i + 1
            ta_nat_stat = Ta_nat_stat()
            ta_nat_stat_list.append(ta_nat_stat)

            ta_nat_stat.nr = i


            i = i + 1
            ta_nat_stat = Ta_nat_stat()
            ta_nat_stat_list.append(ta_nat_stat)

            ta_nat_stat.nr = i
            ta_nat_stat.ta_name = text2
            ta_nat_stat.rmnite = to_string(sub_mrm, ">,>>9")
            ta_nat_stat.logiumz = to_string(sub_mlod, "->>>,>>>,>>9.99")
            ta_nat_stat.argtumz = to_string(sub_margt, "->>>,>>>,>>9.99")
            ta_nat_stat.ytd_rmnite = to_string(sub_yrm, ">>>,>>9")
            ta_nat_stat.ytd_logi = to_string(sub_ylod, "->>,>>>,>>>,>>9.99")
            ta_nat_stat.ytd_argt = to_string(sub_yargt, "->>,>>>,>>>,>>9.99")


            i = i + 1
            ta_nat_stat = Ta_nat_stat()
            ta_nat_stat_list.append(ta_nat_stat)

            ta_nat_stat.nr = i


            i = i + 1
            ta_nat_stat = Ta_nat_stat()
            ta_nat_stat_list.append(ta_nat_stat)

            ta_nat_stat.nr = i
            ta_nat_stat.ta_name = text3
            ta_nat_stat.rmnite = to_string(grand_mrm, ">,>>9")
            ta_nat_stat.logiumz = to_string(grand_mlod, "->>>,>>>,>>9.99")
            ta_nat_stat.argtumz = to_string(grand_margt, "->>>,>>>,>>9.99")
            ta_nat_stat.ytd_rmnite = to_string(grand_yrm, ">>>,>>9")
            ta_nat_stat.ytd_logi = to_string(grand_ylod, "->>,>>>,>>>,>>9.99")
            ta_nat_stat.ytd_argt = to_string(grand_yargt, "->>,>>>,>>>,>>9.99")


    def create_browse1():

        nonlocal ta_nat_stat_list, sub_mrm, sub_mlod, sub_margt, sub_yrm, sub_ylod, sub_yargt, grand_mrm, grand_mlod, grand_margt, grand_yrm, grand_ylod, grand_yargt, guest, genstat, nation, htparam, arrangement, artikel
        nonlocal from_date, last_period, sorttype, text2, text3


        nonlocal ta_nat_stat, tmp_list
        nonlocal ta_nat_stat_list, tmp_list_list

        s:str = ""
        i:int = 0
        curr_nat:str = ""
        it_exists:bool = False
        ta_nat_stat_list.clear()
        sub_mrm = 0
        sub_mlod =  to_decimal("0")
        sub_margt =  to_decimal("0")
        sub_yrm = 0
        sub_ylod =  to_decimal("0")
        sub_yargt =  to_decimal("0")
        grand_mrm = 0
        grand_mlod =  to_decimal("0")
        grand_margt =  to_decimal("0")
        grand_yrm = 0
        grand_ylod =  to_decimal("0")
        grand_yargt =  to_decimal("0")

        for tmp_list in query(tmp_list_list, sort_by=[("nation",False)]):

            if curr_nat != "" and curr_nat != tmp_list.nation:
                i = i + 1
                ta_nat_stat = Ta_nat_stat()
                ta_nat_stat_list.append(ta_nat_stat)

                ta_nat_stat.nr = i


                i = i + 1
                ta_nat_stat = Ta_nat_stat()
                ta_nat_stat_list.append(ta_nat_stat)

                ta_nat_stat.nr = i
                ta_nat_stat.ta_name = text2
                ta_nat_stat.rmnite = to_string(sub_mrm, ">,>>9")
                ta_nat_stat.logiumz = to_string(sub_mlod, "->>>,>>>,>>9.99")
                ta_nat_stat.argtumz = to_string(sub_margt, "->>>,>>>,>>9.99")
                ta_nat_stat.ytd_rmnite = to_string(sub_yrm, ">>>,>>9")
                ta_nat_stat.ytd_logi = to_string(sub_ylod, "->>,>>>,>>>,>>9.99")
                ta_nat_stat.ytd_argt = to_string(sub_yargt, "->>,>>>,>>>,>>9.99")


                i = i + 1
                ta_nat_stat = Ta_nat_stat()
                ta_nat_stat_list.append(ta_nat_stat)

                ta_nat_stat.nr = i


                sub_mrm = 0
                sub_mlod =  to_decimal("0")
                sub_margt =  to_decimal("0")
                sub_yrm = 0
                sub_ylod =  to_decimal("0")
                sub_yargt =  to_decimal("0")


            i = i + 1
            ta_nat_stat = Ta_nat_stat()
            ta_nat_stat_list.append(ta_nat_stat)

            ta_nat_stat.nr = i
            ta_nat_stat.ta_name = to_string(tmp_list.ta_name, "x(36)")
            ta_nat_stat.nation = to_string(tmp_list.nation, "x(3)")
            ta_nat_stat.rmnite = to_string(tmp_list.rmnite, ">,>>9")
            ta_nat_stat.logiumz = to_string(tmp_list.logiumz, "->>>,>>>,>>9.99")
            ta_nat_stat.argtumz = to_string(tmp_list.argtumz, "->>>,>>>,>>9.99")
            ta_nat_stat.ytd_rmnite = to_string(tmp_list.ytd_rmnite, ">>>,>>9")
            ta_nat_stat.ytd_logi = to_string(tmp_list.ytd_logi, "->>,>>>,>>>,>>9.99")
            ta_nat_stat.ytd_argt = to_string(tmp_list.ytd_argt, "->>,>>>,>>>,>>9.99")


            sub_mrm = sub_mrm + tmp_list.rmnite
            sub_mlod =  to_decimal(sub_mlod) + to_decimal(tmp_list.logiumz)
            sub_margt =  to_decimal(sub_margt) + to_decimal(tmp_list.argtumz)
            sub_yrm = sub_yrm + tmp_list.ytd_rmnite
            sub_ylod =  to_decimal(sub_ylod) + to_decimal(tmp_list.ytd_logi)
            sub_yargt =  to_decimal(sub_yargt) + to_decimal(tmp_list.ytd_argt)
            grand_mrm = grand_mrm + tmp_list.rmnite
            grand_mlod =  to_decimal(grand_mlod) + to_decimal(tmp_list.logiumz)
            grand_margt =  to_decimal(grand_margt) + to_decimal(tmp_list.argtumz)
            grand_yrm = grand_yrm + tmp_list.ytd_rmnite
            grand_ylod =  to_decimal(grand_ylod) + to_decimal(tmp_list.ytd_logi)
            grand_yargt =  to_decimal(grand_yargt) + to_decimal(tmp_list.ytd_argt)
            it_exists = True
            curr_nat = tmp_list.nation


        if it_exists:
            i = i + 1
            ta_nat_stat = Ta_nat_stat()
            ta_nat_stat_list.append(ta_nat_stat)

            ta_nat_stat.nr = i


            i = i + 1
            ta_nat_stat = Ta_nat_stat()
            ta_nat_stat_list.append(ta_nat_stat)

            ta_nat_stat.nr = i
            ta_nat_stat.ta_name = text2
            ta_nat_stat.rmnite = to_string(sub_mrm, ">,>>9")
            ta_nat_stat.logiumz = to_string(sub_mlod, "->>>,>>>,>>9.99")
            ta_nat_stat.argtumz = to_string(sub_margt, "->>>,>>>,>>9.99")
            ta_nat_stat.ytd_rmnite = to_string(sub_yrm, ">>>,>>9")
            ta_nat_stat.ytd_logi = to_string(sub_ylod, "->>,>>>,>>>,>>9.99")
            ta_nat_stat.ytd_argt = to_string(sub_yargt, "->>,>>>,>>>,>>9.99")


            i = i + 1
            ta_nat_stat = Ta_nat_stat()
            ta_nat_stat_list.append(ta_nat_stat)

            ta_nat_stat.nr = i


            i = i + 1
            ta_nat_stat = Ta_nat_stat()
            ta_nat_stat_list.append(ta_nat_stat)

            ta_nat_stat.nr = i
            ta_nat_stat.ta_name = text3
            ta_nat_stat.rmnite = to_string(grand_mrm, ">,>>9")
            ta_nat_stat.logiumz = to_string(grand_mlod, "->>>,>>>,>>9.99")
            ta_nat_stat.argtumz = to_string(grand_margt, "->>>,>>>,>>9.99")
            ta_nat_stat.ytd_rmnite = to_string(grand_yrm, ">>>,>>9")
            ta_nat_stat.ytd_logi = to_string(grand_ylod, "->>,>>>,>>>,>>9.99")
            ta_nat_stat.ytd_argt = to_string(grand_yargt, "->>,>>>,>>>,>>9.99")

    if from_date.lower()  != (last_period).lower() :
        create_list()

    if sorttype == 1:
        create_browse()
    else:
        create_browse1()

    return generate_output()