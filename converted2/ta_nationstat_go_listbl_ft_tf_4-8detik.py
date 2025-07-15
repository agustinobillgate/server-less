#using conversion tools version: 1.0.0.70

from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htplogic import htplogic
from models import Htparam, Genstat, Guest, Arrangement, Artikel, Kontplan

def ta_nationstat_go_listbl(from_date:str, last_period:str, sorttype:int, text2:str, text3:str):

    prepare_cache ([Htparam, Genstat, Guest, Arrangement, Artikel, Kontplan])

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
    bill_date:date = None
    serv_vat:bool = False
    tax_vat:bool = False
    rm_serv:bool = False
    rm_vat:bool = False
    incl_service:bool = False
    htparam = genstat = guest = arrangement = artikel = kontplan = None

    ta_nat_stat = tmp_list = argt_list = htp_list = kont_list = calc_list = art_list = None

    ta_nat_stat_list, Ta_nat_stat = create_model("Ta_nat_stat", {"nr":int, "ta_name":str, "nation":str, "rmnite":str, "logiumz":str, "argtumz":str, "ytd_rmnite":str, "ytd_logi":str, "ytd_argt":str})
    tmp_list_list, Tmp_list = create_model("Tmp_list", {"gastnr":int, "ta_name":str, "nation":str, "rmnite":int, "argtumz":decimal, "logiumz":decimal, "ytd_rmnite":int, "ytd_argt":decimal, "ytd_logi":decimal})
    argt_list_list, Argt_list = create_model("Argt_list", {"arrangement":str, "artnr":int})
    htp_list_list, Htp_list = create_model("Htp_list", {"paramnr":int, "fdecimal":decimal, "fchar":str})
    kont_list_list, Kont_list = create_model("Kont_list", {"deptno":int, "artno":int, "datum":date, "anzkont":decimal, "anzconf":decimal})
    calc_list_list, Calc_list = create_model("Calc_list", {"artnr":int, "datum":date, "service":decimal, "vat":decimal, "vat2":decimal})
    art_list_list, Art_list = create_model("Art_list", {"artnr":int, "dept":int, "serv_code":int, "vat_code":int, "prov_code":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ta_nat_stat_list, sub_mrm, sub_mlod, sub_margt, sub_yrm, sub_ylod, sub_yargt, grand_mrm, grand_mlod, grand_margt, grand_yrm, grand_ylod, grand_yargt, bill_date, serv_vat, tax_vat, rm_serv, rm_vat, incl_service, htparam, genstat, guest, arrangement, artikel, kontplan
        nonlocal from_date, last_period, sorttype, text2, text3


        nonlocal ta_nat_stat, tmp_list, argt_list, htp_list, kont_list, calc_list, art_list
        nonlocal ta_nat_stat_list, tmp_list_list, argt_list_list, htp_list_list, kont_list_list, calc_list_list, art_list_list

        return {"ta-nat-stat": ta_nat_stat_list}

    def create_list():

        nonlocal ta_nat_stat_list, sub_mrm, sub_mlod, sub_margt, sub_yrm, sub_ylod, sub_yargt, grand_mrm, grand_mlod, grand_margt, grand_yrm, grand_ylod, grand_yargt, bill_date, serv_vat, tax_vat, rm_serv, rm_vat, incl_service, htparam, genstat, guest, arrangement, artikel, kontplan
        nonlocal from_date, last_period, sorttype, text2, text3


        nonlocal ta_nat_stat, tmp_list, argt_list, htp_list, kont_list, calc_list, art_list
        nonlocal ta_nat_stat_list, tmp_list_list, argt_list_list, htp_list_list, kont_list_list, calc_list_list, art_list_list

        argt_ums:decimal = to_decimal("0.0")
        nat:str = ""
        yr:int = 0
        mm:int = 0
        status_vat:bool = False
        vat:decimal = to_decimal("0.0")
        service:decimal = to_decimal("0.0")
        vat2:decimal = to_decimal("0.0")
        fact:decimal = to_decimal("0.0")
        curr_artnr:int = 0
        avail_argt:bool = False
        avail_article:bool = False
        mm = to_int(to_string(substring(from_date, 0, 2) , "99"))
        yr = to_int(to_string(substring(from_date, 2, 4) , "9999"))
        tmp_list_list.clear()

        htparam = get_cache (Htparam, {"paramnr": 127}, ['flogical', 'fchar', 'fdecimal', '_recid'])
        status_vat = htparam.flogical
        bill_date = get_output(htpdate(110))
        serv_vat = get_output(htplogic(479))
        tax_vat = get_output(htplogic(483))
        rm_vat = get_output(htplogic(127))
        rm_serv = get_output(htplogic(128))
        incl_service = get_output(htplogic(135))

        genstat = Genstat()
        for genstat.gastnr, genstat.argt, genstat.datum, genstat.logis, genstat.ratelocal, genstat._recid in db_session.query(Genstat.gastnr, Genstat.argt, Genstat.datum, Genstat.logis, Genstat.ratelocal, Genstat._recid).filter(
                 (get_year(Genstat.datum) == yr) & (get_month(Genstat.datum) <= mm) & (Genstat.zinr != "") & (Genstat.karteityp == 2) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.gastnr).all():

            tmp_list = query(tmp_list_list, filters=(lambda tmp_list: tmp_list.gastnr == genstat.gastnr), first=True)

            if not tmp_list:

                guest = get_cache (Guest, {"gastnr": genstat.gastnr}, ['land', 'name', 'anredefirma', '_recid'])

                if guest:

                    if guest.land == None or guest.land == "":
                        nat = "***"
                    else:
                        nat = guest.land
                    tmp_list = Tmp_list()
                    tmp_list_list.append(tmp_list)

                    tmp_list.gastnr = genstat.gastnr
                    tmp_list.ta_name = guest.name + ", " + guest.anredefirma
                    tmp_list.nation = nat


            service =  to_decimal("0")
            vat =  to_decimal("0")
            curr_artnr = 0
            avail_argt = True
            avail_article = True

            argt_list = query(argt_list_list, filters=(lambda argt_list: argt_list.arrangement == genstat.argt), first=True)

            if not argt_list:

                arrangement = get_cache (Arrangement, {"arrangement": genstat.argt}, ['artnr_logis', '_recid'])

                if arrangement:
                    argt_list = Argt_list()
                    argt_list_list.append(argt_list)

                    argt_list.arrangement = genstat.argt
                    argt_list.artnr = arrangement.artnr_logis


                else:
                    avail_argt = False

            if avail_argt:
                curr_artnr = argt_list.artnr

            art_list = query(art_list_list, filters=(lambda art_list: art_list.artnr == curr_artnr), first=True)

            if not art_list:

                artikel = get_cache (Artikel, {"artnr": curr_artnr, "departement": 0}, ['artnr', 'departement', 'service_code', 'prov_code', 'mwst_code', '_recid'])

                if artikel and status_vat :
                    art_list = Art_list()
                    art_list_list.append(art_list)

                    art_list.artnr = artikel.artnr
                    art_list.dept = artikel.departement
                    art_list.serv_code = artikel.service_code
                    art_list.prov_code = artikel.prov_code
                    art_list.vat_code = artikel.mwst_code


                else:
                    avail_article = False

            if avail_article:

                calc_list = query(calc_list_list, filters=(lambda calc_list: calc_list.artnr == curr_artnr and calc_list.datum == genstat.datum), first=True)

                if not calc_list:
                    service, vat, vat2, fact = calc_servtax(art_list.artnr, art_list.dept, genstat.datum, art_list.serv_code, art_list.prov_code, art_list.vat_code)
                    vat =  to_decimal(vat) + to_decimal(vat2)


                    calc_list = Calc_list()
                    calc_list_list.append(calc_list)

                    calc_list.artnr = curr_artnr
                    calc_list.datum = genstat.datum
                    calc_list.service =  to_decimal(service)
                    calc_list.vat =  to_decimal(vat)
                    calc_list.vat2 =  to_decimal(vat2)


                service =  to_decimal(calc_list.service)
                vat =  to_decimal(calc_list.vat)
                vat2 =  to_decimal(calc_list.vat2)

            if genstat.resstatus != 13:
                tmp_list.ytd_rmnite = tmp_list.ytd_rmnite + 1
            tmp_list.ytd_logi =  to_decimal(tmp_list.ytd_logi) + to_decimal(genstat.logis)
            tmp_list.ytd_argt =  to_decimal(tmp_list.argtumz) + to_decimal((genstat.ratelocal) / to_decimal((1) + to_decimal(vat) + to_decimal(service)))

            if get_month(genstat.datum) == mm and get_year(genstat.datum) == yr:

                if genstat.resstatus != 13:
                    tmp_list.rmnite = tmp_list.rmnite + 1
                tmp_list.logiumz =  to_decimal(tmp_list.logiumz) + to_decimal(genstat.logis)
                tmp_list.argtumz =  to_decimal(tmp_list.argtumz) + to_decimal((genstat.ratelocal) / to_decimal((1) + to_decimal(vat) + to_decimal(service)))


    def calc_servtax(inp_artno:int, inp_deptno:int, inp_date:date, service_code:int, tax_code:int, vat_code:int):

        nonlocal ta_nat_stat_list, sub_mrm, sub_mlod, sub_margt, sub_yrm, sub_ylod, sub_yargt, grand_mrm, grand_mlod, grand_margt, grand_yrm, grand_ylod, grand_yargt, bill_date, serv_vat, tax_vat, rm_serv, rm_vat, incl_service, htparam, genstat, guest, arrangement, artikel, kontplan
        nonlocal from_date, last_period, sorttype, text2, text3


        nonlocal ta_nat_stat, tmp_list, argt_list, htp_list, kont_list, calc_list, art_list
        nonlocal ta_nat_stat_list, tmp_list_list, argt_list_list, htp_list_list, kont_list_list, calc_list_list, art_list_list

        out_serv = to_decimal("0.0")
        out_vat = to_decimal("0.0")
        out_vat2 = to_decimal("0.0")
        fact_scvat = 1
        ct:str = ""
        l_deci:int = 2
        returnflag:bool = False
        avail_kontplan:bool = True

        def generate_inner_output():
            return (out_serv, out_vat, out_vat2, fact_scvat)


        if inp_date != None and inp_date < bill_date:
            avail_kontplan = True

            kont_list = query(kont_list_list, filters=(lambda kont_list: kont_list.deptno == inp_deptno and kont_list.artno == inp_artno and kont_list.datum == inp_date), first=True)

            if not kont_list:

                kontplan = get_cache (Kontplan, {"betriebsnr": inp_deptno, "kontignr": inp_artno, "datum": inp_date}, ['anzkont', 'anzconf', '_recid'])

                if kontplan:
                    kont_list = Kont_list()
                    kont_list_list.append(kont_list)

                    kont_list.deptno = inp_deptno
                    kont_list.artno = inp_artno
                    kont_list.datum = inp_date
                    kont_list.anzkont =  to_decimal(kontplan.anzkont)
                    kont_list.anzconf =  to_decimal(kontplan.anzconf)

                elif not kontplan:
                    avail_kontplan = False

            if avail_kontplan:

                if kont_list.anzkont >= 100000:
                    out_serv =  to_decimal(kont_list.anzkont) / to_decimal("10000000")
                    out_vat =  to_decimal(kont_list.anzconf) / to_decimal("10000000")


                else:
                    out_serv =  to_decimal(kont_list.anzkont) / to_decimal("10000")
                    out_vat =  to_decimal(kont_list.anzconf) / to_decimal("10000")

                kont_list = query(kont_list_list, filters=(lambda kont_list: kont_list.deptno == inp_deptno + 100 and kont_list.artno == inp_artno and kont_list.datum == inp_date), first=True)

                if not kont_list:

                    kontplan = get_cache (Kontplan, {"betriebsnr": inp_deptno + 100, "kontignr": inp_artno, "datum": inp_date}, ['anzkont', 'anzconf', '_recid'])

                    if kontplan:
                        kont_list = Kont_list()
                        kont_list_list.append(kont_list)

                        kont_list.deptno = inp_deptno + 100
                        kont_list.artno = inp_artno
                        kont_list.datum = inp_date
                        kont_list.anzkont =  to_decimal(kontplan.anzkont)
                        kont_list.anzconf =  to_decimal(kontplan.anzconf)

                    if not kontplan:
                        avail_kontplan = False

                if avail_kontplan:
                    out_vat2 =  to_decimal(kont_list.anzconf) / to_decimal("10000000")


                fact_scvat =  to_decimal("1") + to_decimal(out_serv) + to_decimal(out_vat) + to_decimal(out_vat2)

                if out_vat == 1:
                    fact_scvat =  to_decimal("1")
                    out_serv =  to_decimal("0")
                    out_vat2 =  to_decimal("0")

                elif out_vat2 == 1:
                    fact_scvat =  to_decimal("1")
                    out_serv =  to_decimal("0")
                    out_vat =  to_decimal("0")

                elif out_serv == 1:
                    fact_scvat =  to_decimal("1")
                    out_vat =  to_decimal("0")
                    out_vat2 =  to_decimal("0")

                return generate_inner_output()

        if service_code != 0:

            htp_list = query(htp_list_list, filters=(lambda htp_list: htp_list.paramnr == service_code), first=True)

            if not htp_list:
                htp_list = Htp_list()
                htp_list_list.append(htp_list)

                htp_list.paramnr = service_code

                htparam = get_cache (Htparam, {"paramnr": service_code}, ['flogical', 'fchar', 'fdecimal', '_recid'])

                if htparam:
                    htp_list.fchar = htparam.fchar
                    htp_list.fdecimal =  to_decimal(htparam.fdecimal)

            if htp_list.fdecimal != 0:

                if num_entries(htp_list.fchar, chr_unicode(2)) >= 2:
                    out_serv =  to_decimal(to_decimal(entry(1 , htp_list.fchar , chr_unicode(2)))) / to_decimal("10000")


                else:
                    out_serv =  to_decimal(htp_list.fdecimal)

        if tax_code != 0:

            htp_list = query(htp_list_list, filters=(lambda htp_list: htp_list.paramnr == tax_code), first=True)

            if not htp_list:
                htp_list = Htp_list()
                htp_list_list.append(htp_list)

                htp_list.paramnr = tax_code

                htparam = get_cache (Htparam, {"paramnr": tax_code}, ['flogical', 'fchar', 'fdecimal', '_recid'])

                if htparam:
                    htp_list.fchar = htparam.fchar
                    htp_list.fdecimal =  to_decimal(htparam.fdecimal)

            if htp_list.fdecimal != 0:

                if num_entries(htp_list.fchar, chr_unicode(2)) >= 2:
                    out_vat2 =  to_decimal(to_decimal(entry(1 , htp_list.fchar , chr_unicode(2)))) / to_decimal("10000")


                else:
                    out_vat2 =  to_decimal(htp_list.fdecimal)

                if serv_vat:
                    out_vat2 =  to_decimal(out_vat2) + (to_decimal(out_vat2) * to_decimal(out_serv)) / to_decimal("100")
                ct = replace_str(to_string(out_vat2) , ".", ",")
                l_deci = length(entry(1, ct, ","))

                if l_deci <= 2:
                    out_vat2 = to_decimal(round(out_vat2 , 2))

                elif l_deci == 3:
                    out_vat2 = to_decimal(round(out_vat2 , 3))
                else:
                    out_vat2 = to_decimal(round(out_vat2 , 4))

        if vat_code != 0:

            htp_list = query(htp_list_list, filters=(lambda htp_list: htp_list.paramnr == vat_code), first=True)

            if not htp_list:
                htp_list = Htp_list()
                htp_list_list.append(htp_list)

                htp_list.paramnr = vat_code

                htparam = get_cache (Htparam, {"paramnr": vat_code}, ['flogical', 'fchar', 'fdecimal', '_recid'])

                if htparam:
                    htp_list.fchar = htparam.fchar
                    htp_list.fdecimal =  to_decimal(htparam.fdecimal)

            if htp_list.fdecimal != 0:

                if num_entries(htp_list.fchar, chr_unicode(2)) >= 2:
                    out_vat =  to_decimal(to_decimal(entry(1 , htp_list.fchar , chr_unicode(2)))) / to_decimal("10000")


                else:
                    out_vat =  to_decimal(htp_list.fdecimal)

                if serv_vat and not tax_vat:
                    out_vat =  to_decimal(out_vat) + to_decimal(out_vat) * to_decimal(out_serv) / to_decimal("100")

                elif serv_vat and tax_vat:
                    out_vat =  to_decimal(out_vat) + to_decimal(out_vat) * to_decimal((out_serv) + to_decimal(out_vat2)) / to_decimal("100")

                elif not serv_vat and tax_vat:
                    out_vat =  to_decimal(out_vat) + to_decimal(out_vat) * to_decimal(out_vat2) / to_decimal("100")
                ct = replace_str(to_string(out_vat) , ".", ",")
                l_deci = length(entry(1, ct, ","))

                if l_deci <= 2:
                    out_vat = to_decimal(round(out_vat , 2))

                elif l_deci == 3:
                    out_vat = to_decimal(round(out_vat , 3))
                else:
                    out_vat = to_decimal(round(out_vat , 4))
        out_serv =  to_decimal(out_serv) / to_decimal("100")
        out_vat =  to_decimal(out_vat) / to_decimal("100")
        out_vat2 =  to_decimal(out_vat2) / to_decimal("100")


        fact_scvat =  to_decimal("1") + to_decimal(out_serv) + to_decimal(out_vat) + to_decimal(out_vat2)

        if out_vat == 1:
            fact_scvat =  to_decimal("1")
            out_serv =  to_decimal("0")
            out_vat2 =  to_decimal("0")

        elif out_vat2 == 1:
            fact_scvat =  to_decimal("1")
            out_serv =  to_decimal("0")
            out_vat =  to_decimal("0")

        elif out_serv == 1:
            fact_scvat =  to_decimal("1")
            out_vat =  to_decimal("0")
            out_vat2 =  to_decimal("0")

        return generate_inner_output()


    def create_browse():

        nonlocal ta_nat_stat_list, sub_mrm, sub_mlod, sub_margt, sub_yrm, sub_ylod, sub_yargt, grand_mrm, grand_mlod, grand_margt, grand_yrm, grand_ylod, grand_yargt, bill_date, serv_vat, tax_vat, rm_serv, rm_vat, incl_service, htparam, genstat, guest, arrangement, artikel, kontplan
        nonlocal from_date, last_period, sorttype, text2, text3


        nonlocal ta_nat_stat, tmp_list, argt_list, htp_list, kont_list, calc_list, art_list
        nonlocal ta_nat_stat_list, tmp_list_list, argt_list_list, htp_list_list, kont_list_list, calc_list_list, art_list_list

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

        nonlocal ta_nat_stat_list, sub_mrm, sub_mlod, sub_margt, sub_yrm, sub_ylod, sub_yargt, grand_mrm, grand_mlod, grand_margt, grand_yrm, grand_ylod, grand_yargt, bill_date, serv_vat, tax_vat, rm_serv, rm_vat, incl_service, htparam, genstat, guest, arrangement, artikel, kontplan
        nonlocal from_date, last_period, sorttype, text2, text3


        nonlocal ta_nat_stat, tmp_list, argt_list, htp_list, kont_list, calc_list, art_list
        nonlocal ta_nat_stat_list, tmp_list_list, argt_list_list, htp_list_list, kont_list_list, calc_list_list, art_list_list

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