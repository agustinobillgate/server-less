from functions.additional_functions import *
import decimal
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Guest, Genstat, Nation, Htparam, Arrangement, Artikel

def ta_nationstat_go_listbl(from_date:str, last_period:str, sorttype:int, text2:str, text3:str):
    ta_nat_stat_list = []
    sub_mrm:int = 0
    sub_mlod:decimal = 0
    sub_margt:decimal = 0
    sub_yrm:int = 0
    sub_ylod:decimal = 0
    sub_yargt:decimal = 0
    grand_mrm:int = 0
    grand_mlod:decimal = 0
    grand_margt:decimal = 0
    grand_yrm:int = 0
    grand_ylod:decimal = 0
    grand_yargt:decimal = 0
    guest = genstat = nation = htparam = arrangement = artikel = None

    ta_nat_stat = tmp_list = None

    ta_nat_stat_list, Ta_nat_stat = create_model("Ta_nat_stat", {"nr":int, "ta_name":str, "nation":str, "rmnite":str, "logiumz":str, "argtumz":str, "ytd_rmnite":str, "ytd_logi":str, "ytd_argt":str})
    tmp_list_list, Tmp_list = create_model("Tmp_list", {"gastnr":int, "ta_name":str, "nation":str, "rmnite":int, "argtumz":decimal, "logiumz":decimal, "ytd_rmnite":int, "ytd_argt":decimal, "ytd_logi":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ta_nat_stat_list, sub_mrm, sub_mlod, sub_margt, sub_yrm, sub_ylod, sub_yargt, grand_mrm, grand_mlod, grand_margt, grand_yrm, grand_ylod, grand_yargt, guest, genstat, nation, htparam, arrangement, artikel


        nonlocal ta_nat_stat, tmp_list
        nonlocal ta_nat_stat_list, tmp_list_list
        return {"ta-nat-stat": ta_nat_stat_list}

    def create_list():

        nonlocal ta_nat_stat_list, sub_mrm, sub_mlod, sub_margt, sub_yrm, sub_ylod, sub_yargt, grand_mrm, grand_mlod, grand_margt, grand_yrm, grand_ylod, grand_yargt, guest, genstat, nation, htparam, arrangement, artikel


        nonlocal ta_nat_stat, tmp_list
        nonlocal ta_nat_stat_list, tmp_list_list

        argt_ums:decimal = 0
        nat:str = ""
        yr:int = 0
        mm:int = 0
        status_vat:bool = False
        vat:decimal = 0
        service:decimal = 0
        vat2:decimal = 0
        fact:decimal = 0
        mm = to_int(to_string(substring(from_date, 0, 2) , "99"))
        yr = to_int(to_string(substring(from_date, 2, 4) , "9999"))
        tmp_list_list.clear()

        genstat_obj_list = []
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                (get_year(Genstat.datum) == yr) &  (get_month(Genstat.datum) <= mm) &  (Genstat.zinr != "") &  (Genstat.karteityp == 2) &  (Genstat.res_logic[1])).all():
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

            tmp_list = query(tmp_list_list, filters=(lambda tmp_list :tmp_list.gastnr == genstat.gastnr and tmp_list.nation.lower()  == (nat).lower()), first=True)

            if not tmp_list:
                tmp_list = Tmp_list()
                tmp_list_list.append(tmp_list)

                tmp_list.gastnr = genstat.gastnr
                tmp_list.ta_name = guest.name + ", " + guest.anredefirma
                tmp_list.nation = guest.land


            service = 0
            vat = 0

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 127)).first()
            status_vat = htparam.flogical

            arrangement = db_session.query(Arrangement).filter(
                    (Arrangement == genstat.argt)).first()

            if arrangement:

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == arrangement.artnr_logis) &  (Artikel.departement == 0)).first()

            if artikel and status_vat :
                service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))
                vat = vat + vat2

            if genstat.resstatus != 13:
                tmp_list.ytd_rmnite = tmp_list.ytd_rmnite + 1
            tmp_list.ytd_logi = tmp_list.ytd_logi + genstat.logis
            tmp_list.ytd_argt = tmp_list.argt + (genstat.ratelocal / (1 + vat + service))

            if get_month(genstat.datum) == mm and get_year(genstat.datum) == yr:

                if genstat.resstatus != 13:
                    tmp_list.rmnite = tmp_list.rmnite + 1
                tmp_list.logiumz = tmp_list.logiumz + genstat.logis
                tmp_list.argtumz = tmp_list.argtumz + (genstat.ratelocal / (1 + vat + service))

    def create_browse():

        nonlocal ta_nat_stat_list, sub_mrm, sub_mlod, sub_margt, sub_yrm, sub_ylod, sub_yargt, grand_mrm, grand_mlod, grand_margt, grand_yrm, grand_ylod, grand_yargt, guest, genstat, nation, htparam, arrangement, artikel


        nonlocal ta_nat_stat, tmp_list
        nonlocal ta_nat_stat_list, tmp_list_list

        i:int = 0
        curr_gastnr:int = 0
        it_exists:bool = False
        s:str = ""
        ta_nat_stat_list.clear()
        sub_mrm = 0
        sub_mlod = 0
        sub_margt = 0
        sub_yrm = 0
        sub_ylod = 0
        sub_yargt = 0
        grand_mrm = 0
        grand_mlod = 0
        grand_margt = 0
        grand_yrm = 0
        grand_ylod = 0
        grand_yargt = 0

        for tmp_list in query(tmp_list_list):

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
                sub_mlod = 0
                sub_margt = 0
                sub_yrm = 0
                sub_ylod = 0
                sub_yargt = 0


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
            sub_mlod = sub_mlod + tmp_list.logiumz
            sub_margt = sub_margt + tmp_list.argtumz
            sub_yrm = sub_yrm + tmp_list.ytd_rmnite
            sub_ylod = sub_ylod + tmp_list.ytd_logi
            sub_yargt = sub_yargt + tmp_list.ytd_argt
            grand_mrm = grand_mrm + tmp_list.rmnite
            grand_mlod = grand_mlod + tmp_list.logiumz
            grand_margt = grand_margt + tmp_list.argtumz
            grand_yrm = grand_yrm + tmp_list.ytd_rmnite
            grand_ylod = grand_ylod + tmp_list.ytd_logi
            grand_yargt = grand_yargt + tmp_list.ytd_argt
            it_exists = True
            curr_gastnr = tmp_list.gastnr


            pass

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


        nonlocal ta_nat_stat, tmp_list
        nonlocal ta_nat_stat_list, tmp_list_list

        s:str = ""
        i:int = 0
        curr_nat:str = ""
        it_exists:bool = False
        ta_nat_stat_list.clear()
        sub_mrm = 0
        sub_mlod = 0
        sub_margt = 0
        sub_yrm = 0
        sub_ylod = 0
        sub_yargt = 0
        grand_mrm = 0
        grand_mlod = 0
        grand_margt = 0
        grand_yrm = 0
        grand_ylod = 0
        grand_yargt = 0

        for tmp_list in query(tmp_list_list):

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
                sub_mlod = 0
                sub_margt = 0
                sub_yrm = 0
                sub_ylod = 0
                sub_yargt = 0


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
            sub_mlod = sub_mlod + tmp_list.logiumz
            sub_margt = sub_margt + tmp_list.argtumz
            sub_yrm = sub_yrm + tmp_list.ytd_rmnite
            sub_ylod = sub_ylod + tmp_list.ytd_logi
            sub_yargt = sub_yargt + tmp_list.ytd_argt
            grand_mrm = grand_mrm + tmp_list.rmnite
            grand_mlod = grand_mlod + tmp_list.logiumz
            grand_margt = grand_margt + tmp_list.argtumz
            grand_yrm = grand_yrm + tmp_list.ytd_rmnite
            grand_ylod = grand_ylod + tmp_list.ytd_logi
            grand_yargt = grand_yargt + tmp_list.ytd_argt
            it_exists = True
            curr_nat = tmp_list.nation


            pass

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