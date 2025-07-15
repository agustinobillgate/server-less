#using conversion tools version: 1.0.0.61

from functions.additional_functions import *
import decimal
from functions.calc_servtaxesbl_big import calc_servtaxesbl_big
from functions.htpdate import htpdate
from functions.htplogic import htplogic
from models import Guest, Genstat, Nation, Htparam, Arrangement, Artikel
from sqlalchemy.inspection import inspect


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
    artikel_cache = {}
    calc_cache = {}
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

    def get_cached_output(artikel_artnr, artikel_departement, genstat_datum, bill_date, 
                        serv_vat, tax_vat, rm_vat, rm_serv, incl_service, incl_mwst):
        """Retrieve cached calculation result or compute and store it if not found."""

        # Create a unique key from function parameters
        key = (artikel_artnr, artikel_departement, genstat_datum, bill_date, 
            serv_vat, tax_vat, rm_vat, rm_serv, incl_service, incl_mwst)

        if key in calc_cache:
            return calc_cache[key]  # Return cached result if available

        # Compute the values if not cached
        result = get_output(calc_servtaxesbl_big(1, *key))

        calc_cache[key] = result  # Cache the result for later use
        return result
    
    def get_artikel_from_arrangement(genstat_argt):
        if genstat_argt in artikel_cache:
            return artikel_cache[genstat_argt]  # Return cached value if available

        artikel = (
            db_session.query(Artikel)
            .join(Arrangement, Arrangement.artnr_logis == Artikel.artnr)
            .filter((Arrangement.arrangement == genstat_argt) & (Artikel.departement == 0))
            .first()
        )

        if artikel:
            artikel_cache[genstat_argt] = artikel  # Cache the result for later use

        return artikel  # Return None if no record is found

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
        htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 127)).first()
        if htparam:
            status_vat = htparam.flogical

        bill_date = get_output(htpdate(110))
        serv_vat = get_output(htplogic(479))
        tax_vat = get_output(htplogic(483))
        rm_vat = get_output(htplogic(127))
        rm_serv = get_output(htplogic(128))
        incl_service = get_output(htplogic(135))
        incl_mwst = get_output(htplogic(134))
        
        recs = (
            db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                 (get_year(Genstat.datum) == yr) & (get_month(Genstat.datum) <= mm) & (Genstat.zinr != "") & (Genstat.karteityp == 2) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all()
        )
        # sql = """
        #     SELECT g.*, gs.*
        #     FROM genstat g
        #     INNER JOIN guest gs ON gs.gastnr = g.gastnr
        #     WHERE 
        #         EXTRACT(YEAR FROM g.datum) = :yr
        #         AND EXTRACT(MONTH FROM g.datum) <= :mm
        #         AND g.zinr != ''
        #         AND g.karteityp = 2
        #         AND g.res_logic[:inc_value]
        #     ORDER BY g._recid
        # """

        # Execute the query
        # result = db_session.execute(text(sql), {"yr": yr, "mm": mm, "inc_value": inc_value(1)})

        # # ✅ Step 3: Get Column Names Dynamically
        # column_names = result.keys()
        # recs = [dict(zip(column_names, row)) for row in result.fetchall()]

        # ✅ Step 4: Get Column Names for Each Table from SQLAlchemy Metadata
        # genstat_columns = {col.name for col in inspect(Genstat).c}
        # guest_columns = {col.name for col in inspect(Guest).c}
        # print(genstat_columns)
        # print(guest_columns)
        """
        {'gratis', 'ratelocal', '_recid', 'zikatnr', 'ankflag', 'erwachs', 'res_logic', 'domestic', 'datum', 'kind1', 'karteityp', 'res_date', 'gastnr', 'argt', 'kind2', 'kind3', 'zipreis', 'res_deci', 'resnr', 'wahrungsnr', 'logis', 'res_int', 'resident', 'segmentcode', 'nationnr', 'resstatus', 'source', 'zinr', 'res_char', 'gastnrmember', 'kontcode'}
        {'geburt_ort1', 'segment2', 'noshows', 'vorname2', 'stornos', 'betriebsnr', 'zahlungsart', 'fax', 'startkur', 'anrede2', 'erstaufent', 'f_b_umsatz', 'telex', 'mahnsperre', 'sonst_umsatz', 'adresse2', 'argtumsatz', 'endperiode', 'geburtdatum2', 'geschlecht2', 'zimmer_min', 'logier_min', 'segment1', 'deci1', '_recid', 'tv_checkout', 'gesamtumsatz_old', 'aufenthalte', 'code', 'master_gastnr', 'trans_datum', 'namekontakt', 'gastnr', 'adresse3', 'vorname_haupt', 'ausweis_art', 'logi2', 'mobil_telefon', 'com_argt', 'deci2', 'interessen', 'logisumsatz', 'number1', 'geschlecht', 'phonetik2', 'number2', 'plz', 'massnr2', 'com_sonst', 'gesamtumsatz', 'wohnort', 'logi1', 'blumen', 'kreditlimit', 'betrieb_gastmaster', 'kreditlimit_old', 'resflag', 'groesse', 'letzte_abreise', 'logiernachte', 'arzt2', 'steuernr', 'preis_doppel', 'briefanrede', 'credablauf', 'karteityp', 'nation1', 'argt_einzel', 'pass_aust2', 'telefon', 'ausweis_nr1', 'notizen', 'zimmeranz', 'startperiode', 'telefon_privat', 'point_gastnr', 'com_f_b', 'geburtkind', 'phonetik3', 'endkur', 'phonetik1', 'preis_einzel', 'autonr', 'geburt_ort2', 'email_adr', 'kontaktdat', 'tv_pay', 'modif_datum', 'geburtdatum1', 'name', 'groesse2', 'betrieb_gastpoint', 'gewicht', 'sprachcode', 'bemerkung', 'argt_doppel', 'date1', 'erste_res', 'segment3', 'sternzeichen', 'beruf', 'anlage_datum', 'anrede1', 'arzt1', 'vornamekind', 'char2', 'date2', 'vorname1', 'rabatt', 'tv_see_bill', 'cardnr', 'pass_aust1', 'com_logis', 'massnr', 'champagner', 'anredefirma', 'gewicht2', 'naechste_res', 'nation2', 'adresse1', 'firmen_nr', 'char1', 'ausweis_nr2', 'finanzamt', 'letzte_res', 'land'}
        """
        
        # recs = [dict(zip(column_names, row)) for row in result]
        local_storage.debugging = local_storage.debugging + ", nRec:" + to_string(len(recs)) + ",BillDate:" + to_string(bill_date)
        nations = db_session.query(Nation).all()  # Load all records into a lis
        for genstat, guest in recs:
        # for row in recs:
        #     genstat = {key: row[key] for key in row if key in genstat_columns}
        #     guest = {key: row[key] for key in row if key in guest_columns}
        
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            # nation = db_session.query(Nation).filter(
            #          (Nation.kurzbez == guest.land)).first()
            nation = next((n for n in nations if n.kurzbez == guest.land), None)
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

            # htparam = db_session.query(Htparam).filter(
            #          (Htparam.paramnr == 127)).first()
            # if htparam:
            #     status_vat = htparam.flogical

            # arrangement = db_session.query(Arrangement).filter(
            #          (Arrangement.arrangement == genstat.argt)).first()

            # if arrangement:
            #     artikel = db_session.query(Artikel).filter(
            #              (Artikel.artnr == arrangement.artnr_logis) & (Artikel.departement == 0)).first()

            # artikel = (
            #         db_session.query(Artikel)
            #         .join(Arrangement, Arrangement.artnr_logis == Artikel.artnr)
            #         .filter((Arrangement.arrangement == genstat.argt) & (Artikel.departement == 0))
            #         .first()
            #     )
            
            artikel = get_artikel_from_arrangement(genstat.argt)

            if artikel and status_vat :
                    # bill_date = get_output(htpdate(110))
                    # serv_vat = get_output(htplogic(479))
                    # tax_vat = get_output(htplogic(483))
                    # rm_vat = get_output(htplogic(127))
                    # rm_serv = get_output(htplogic(128))
                    # incl_service = get_output(htplogic(135))
                    # incl_mwst = get_output(htplogic(134))
                # service, vat, vat2, fact = get_output(calc_servtaxesbl_big(1, artikel.artnr, artikel.departement, genstat.datum,
                #                                                            bill_date, serv_vat, tax_vat, rm_vat, rm_serv, incl_service, incl_mwst
                #                                                            )
                #                                       )
                service, vat, vat2, fact = get_cached_output(
                                                artikel.artnr, artikel.departement, genstat.datum, bill_date,
                                                serv_vat, tax_vat, rm_vat, rm_serv, incl_service, incl_mwst
                                            )
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