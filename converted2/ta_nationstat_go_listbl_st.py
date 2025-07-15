#using conversion tools version: 1.0.0.93

from functions.additional_functions import *
from decimal import Decimal
from functions.calc_servtaxesbl_st import calc_servtaxesbl_st
from models import Guest, Genstat, Nation, Htparam, Arrangement, Artikel, Kontplan
import sqlalchemy

def ta_nationstat_go_listbl_st(from_date:string, last_period:string, sorttype:int, text2:string, text3:string):

    # prepare_cache ([Guest, Genstat, Nation, Htparam, Arrangement, Artikel])
    prepare_cache ([Guest, Genstat, Nation, Htparam, Arrangement, Artikel])

    ta_nat_stat_list = []
    sub_mrm:int = 0
    sub_mlod:Decimal = to_decimal("0.0")
    sub_margt:Decimal = to_decimal("0.0")
    sub_yrm:int = 0
    sub_ylod:Decimal = to_decimal("0.0")
    sub_yargt:Decimal = to_decimal("0.0")
    grand_mrm:int = 0
    grand_mlod:Decimal = to_decimal("0.0")
    grand_margt:Decimal = to_decimal("0.0")
    grand_yrm:int = 0
    grand_ylod:Decimal = to_decimal("0.0")
    grand_yargt:Decimal = to_decimal("0.0")
    guest = genstat = nation = htparam = arrangement = artikel = kontplan = None

    ta_nat_stat = tmp_list = None

    ta_nat_stat_list, Ta_nat_stat = create_model("Ta_nat_stat", {"nr":int, "ta_name":string, "nation":string, "rmnite":string, "logiumz":string, "argtumz":string, "ytd_rmnite":string, "ytd_logi":string, "ytd_argt":string})
    tmp_list_list, Tmp_list = create_model("Tmp_list", {"gastnr":int, "ta_name":string, "nation":string, "rmnite":int, "argtumz":Decimal, "logiumz":Decimal, "ytd_rmnite":int, "ytd_argt":Decimal, "ytd_logi":Decimal})


    set_cache(Kontplan, None,[["betriebsnr", "kontignr", "datum"]], True)

    session = local_storage.db_session

    def generate_output():
        nonlocal ta_nat_stat_list

        return {"ta-nat-stat": ta_nat_stat_list}

    def create_list():
        nonlocal tmp_list_list
       
        yr:int = 0
        mm:int = 0
        status_vat:bool = False
        mm = to_int(to_string(substring(from_date, 0, 2) , "99"))
        yr = to_int(to_string(substring(from_date, 2, 4) , "9999"))
        tmp_list_list.clear()

        genstat_obj_list = {}
        stmtHtparam = sqlalchemy.select(
            Htparam.flogical, Htparam.fdate, Htparam.paramnr, Htparam.fchar
        ).where(Htparam.paramnr.in_([110, 479, 483, 127, 128, 135, 134]))
        stmt = (
            sqlalchemy.select(
                Genstat.gastnr,
                Genstat.argt,
                Genstat.datum,
                Genstat.logis,
                Genstat.ratelocal,
                Genstat.resstatus,
                Genstat._recid,
                Guest.land,
                Guest.name,
                Guest.anredefirma,
                Guest._recid,
            )
            .join(Guest, (Guest.gastnr == Genstat.gastnr))
            .filter(
                get_month(Genstat.datum) <= mm,
                get_year(Genstat.datum) == yr,
                Genstat.zinr != "",
                Genstat.karteityp == 2,
                Genstat.res_logic[2],
            )
            .order_by(Genstat._recid)
        )
        print("start get data")
        data = session.execute(stmt).mappings().all()
        htparams = session.execute(stmtHtparam).mappings().all()
        bill_date = next((x for x in htparams if x.paramnr == 110), None).fdate
        status_vat = serv_vat = next((x for x in htparams if x.paramnr == 479), None).flogical
        tax_vat = next((x for x in htparams if x.paramnr == 483), None).flogical
        rm_vat = next((x for x in htparams if x.paramnr == 127), None).flogical
        rm_serv = next((x for x in htparams if x.paramnr == 128), None).flogical
        incl_service = next((x for x in htparams if x.paramnr == 135), None).flogical
        incl_mwst = next((x for x in htparams if x.paramnr == 134), None).flogical
        def calculate(record):
            nonlocal tmp_list_list, tmp_list
            filteredNation = get_cache_st (Nation, {"kurzbez": record.land}, ['kurzbez', '_recid'])
            if filteredNation:
                nat = filteredNation.kurzbez
            else:
                nat = "***"
            tmp_list = next(
                (
                    x
                    for x in tmp_list_list
                    if x.gastnr == record.gastnr
                    and x.nation.lower() == nat.lower()
                ),
                None,
            )

            if not tmp_list:
                tmp_list = Tmp_list()
                tmp_list_list.append(tmp_list)
                
                tmp_list.gastnr = record.gastnr
                tmp_list.nation = nat
                tmp_list.ta_name = record.name + ", " + record.anredefirma

            service =  to_decimal("0")
            vat =  to_decimal("0")
            
            arrangement = get_cache_st (Arrangement, {"arrangement": record.argt}, ['artnr_logis', '_recid'])

            if arrangement:
                artikel = get_cache_st (Artikel, {"artnr": arrangement.artnr_logis, "departement": 0}, ['artnr', 'departement', '_recid'])

            if artikel and status_vat :
                service, vat, vat2, fact = get_output(calc_servtaxesbl_st(
                    # Articles,
                    1,
                    artikel.artnr,
                    artikel.departement,
                    record.datum,
                    bill_date,
                    serv_vat,
                    tax_vat,
                    rm_vat,
                    rm_serv,
                    incl_service,
                    incl_mwst
                    ))
                vat =  to_decimal(vat) + to_decimal(vat2)

            if record.resstatus != 13:
                tmp_list.ytd_rmnite = tmp_list.ytd_rmnite + 1
            tmp_list.ytd_logi =  to_decimal(tmp_list.ytd_logi) + to_decimal(record.logis)
            tmp_list.ytd_argt =  to_decimal(tmp_list.argtumz) + to_decimal((record.ratelocal) / to_decimal((1) + to_decimal(vat) + to_decimal(service)))
            
            if get_month(record.datum) == mm and get_year(record.datum) == yr:

                if record.resstatus != 13:
                    tmp_list.rmnite = tmp_list.rmnite + 1
                tmp_list.logiumz =  to_decimal(tmp_list.logiumz) + to_decimal(record.logis)
                tmp_list.argtumz =  to_decimal(tmp_list.argtumz) + to_decimal((record.ratelocal) / to_decimal((1) + to_decimal(vat) + to_decimal(service)))
        list(map(calculate, data))

    def create_browse():

        nonlocal ta_nat_stat_list, sub_mrm, sub_mlod, sub_margt, sub_yrm, sub_ylod, sub_yargt, grand_mrm, grand_mlod, grand_margt, grand_yrm, grand_ylod, grand_yargt, guest, genstat, nation, htparam, arrangement, artikel, kontplan
        nonlocal from_date, last_period, sorttype, text2, text3


        nonlocal ta_nat_stat, tmp_list
        nonlocal ta_nat_stat_list, tmp_list_list

        i:int = 0
        curr_gastnr:int = 0
        it_exists:bool = False
        s:string = ""
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

        nonlocal ta_nat_stat_list, sub_mrm, sub_mlod, sub_margt, sub_yrm, sub_ylod, sub_yargt, grand_mrm, grand_mlod, grand_margt, grand_yrm, grand_ylod, grand_yargt, guest, genstat, nation, htparam, arrangement, artikel, kontplan
        nonlocal from_date, last_period, sorttype, text2, text3


        nonlocal ta_nat_stat, tmp_list
        nonlocal ta_nat_stat_list, tmp_list_list

        s:string = ""
        i:int = 0
        curr_nat:string = ""
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