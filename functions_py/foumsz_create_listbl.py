#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 20/8/2025
# kolom artikel: TOTAL & GRAND TOTAL
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Htparam, Umsatz, Artikel, Budget, Hoteldpt, Kontplan

def foumsz_create_listbl(from_dept:int, to_dept:int, first_date:date, from_date:date, to_date:date, totvatflag:bool):

    prepare_cache ([Htparam, Umsatz, Artikel, Budget, Hoteldpt])

    umsz_list_data = []
    vhp_limited:bool = False
    vat_str:string = ""
    vat_artnr:int = 0
    serv_artnr:int = 0
    price_decimal:int = 0
    htparam = umsatz = artikel = budget = hoteldpt = kontplan = None

    umsz_list = cl_list = vat_list = gvat_list = not_avail_umstaz = None

    umsz_list_data, Umsz_list = create_model("Umsz_list", {"artnr":string, "bezeich":string, "day_nett":string, "day_serv":string, "day_tax":string, "day_gros":string, "day_persen":string, "mtd_nett":string, "mtd_serv":string, "mtd_tax":string, "mtd_gros":string, "mtd_persen":string, "ytd_nett":string, "ytd_serv":string, "ytd_tax":string, "ytd_gros":string, "ytd_persen":string, "month_bud":string, "dqty":string, "mqty":string, "yqty":string})
    cl_list_data, Cl_list = create_model("Cl_list", {"flag":string, "vat_proz":Decimal, "artnr":int, "dept":int, "bezeich":string, "dnet":Decimal, "proz1":Decimal, "dserv":Decimal, "dtax":Decimal, "dgros":Decimal, "proz2":Decimal, "mnet":Decimal, "mserv":Decimal, "mtax":Decimal, "mgros":Decimal, "proz4":Decimal, "ynet":Decimal, "proz6":Decimal, "yserv":Decimal, "ytax":Decimal, "ygros":Decimal, "mbudget":Decimal, "dqty":int, "mqty":int, "yqty":int})
    vat_list_data, Vat_list = create_model("Vat_list", {"dptnr":int, "vat":Decimal, "dtax":Decimal, "dnet":Decimal, "dgros":Decimal, "dserv":Decimal, "mtax":Decimal, "mnet":Decimal, "mserv":Decimal, "mgros":Decimal, "ytax":Decimal, "yserv":Decimal, "ynet":Decimal, "ygros":Decimal})
    gvat_list_data, Gvat_list = create_model("Gvat_list", {"dptnr":int, "vat":Decimal, "dtax":Decimal, "dnet":Decimal, "dgros":Decimal, "dserv":Decimal, "mtax":Decimal, "mnet":Decimal, "mserv":Decimal, "mgros":Decimal, "ytax":Decimal, "yserv":Decimal, "ynet":Decimal, "ygros":Decimal})
    not_avail_umstaz_data, Not_avail_umstaz = create_model("Not_avail_umstaz", {"artnr":int, "depart":int, "bezeich":string})


    set_cache(Kontplan, (Kontplan.datum >= first_date) & (Kontplan.datum <= to_date),[["betriebsnr", "kontignr", "datum"]], True,[],[])

    db_session = local_storage.db_session

    def generate_output():
        nonlocal umsz_list_data, vhp_limited, vat_str, vat_artnr, serv_artnr, price_decimal, htparam, umsatz, artikel, budget, hoteldpt, kontplan
        nonlocal from_dept, to_dept, first_date, from_date, to_date, totvatflag


        nonlocal umsz_list, cl_list, vat_list, gvat_list, not_avail_umstaz
        nonlocal umsz_list_data, cl_list_data, vat_list_data, gvat_list_data, not_avail_umstaz_data

        return {"umsz-list": umsz_list_data}

    def create_umsatz():

        nonlocal umsz_list_data, vhp_limited, vat_str, vat_artnr, serv_artnr, price_decimal, htparam, umsatz, artikel, budget, hoteldpt, kontplan
        nonlocal from_dept, to_dept, first_date, from_date, to_date, totvatflag


        nonlocal umsz_list, cl_list, vat_list, gvat_list, not_avail_umstaz
        nonlocal umsz_list_data, cl_list_data, vat_list_data, gvat_list_data, not_avail_umstaz_data

        dnet:Decimal = to_decimal("0.0")
        dserv:Decimal = to_decimal("0.0")
        dtax:Decimal = to_decimal("0.0")
        dgros:Decimal = to_decimal("0.0")
        dqty:int = 0
        mnet:Decimal = to_decimal("0.0")
        mserv:Decimal = to_decimal("0.0")
        mtax:Decimal = to_decimal("0.0")
        mgros:Decimal = to_decimal("0.0")
        mqty:int = 0
        ynet:Decimal = to_decimal("0.0")
        yserv:Decimal = to_decimal("0.0")
        ytax:Decimal = to_decimal("0.0")
        ygros:Decimal = to_decimal("0.0")
        yqty:int = 0
        t_dnet:Decimal = to_decimal("0.0")
        t_dserv:Decimal = to_decimal("0.0")
        t_dtax:Decimal = to_decimal("0.0")
        t_dgros:Decimal = to_decimal("0.0")
        t_dqty:int = 0
        t_mnet:Decimal = to_decimal("0.0")
        t_mserv:Decimal = to_decimal("0.0")
        t_mtax:Decimal = to_decimal("0.0")
        t_mgros:Decimal = to_decimal("0.0")
        t_mqty:int = 0
        t_ynet:Decimal = to_decimal("0.0")
        t_yserv:Decimal = to_decimal("0.0")
        t_ytax:Decimal = to_decimal("0.0")
        t_ygros:Decimal = to_decimal("0.0")
        t_yqty:int = 0
        vat:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        all_vat:Decimal = to_decimal("0.0")
        serv:Decimal = to_decimal("0.0")
        it_exist:bool = False
        serv_vat:bool = False
        fact:Decimal = to_decimal("0.0")
        nett_amt:Decimal = to_decimal("0.0")
        nett_serv:Decimal = to_decimal("0.0")
        nett_tax:Decimal = to_decimal("0.0")
        nett_vat:Decimal = to_decimal("0.0")
        mbugdet:Decimal = to_decimal("0.0")
        tbudget:Decimal = to_decimal("0.0")
        gtbudget:Decimal = to_decimal("0.0")
        cr_umsatz:bool = False
        curr_artnr:int = 0
        curr_departement:int = 0
        fact1:Decimal = 1
        do_it:bool = False
        counter:int = 0
        x_sum:Decimal = to_decimal("0.0")
        x_sum2:Decimal = to_decimal("0.0")
        y_sum:Decimal = to_decimal("0.0")
        y_sum2:Decimal = to_decimal("0.0")
        bumsz = None
        Bumsz =  create_buffer("Bumsz",Umsatz)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
        serv_vat = htparam.flogical
        umsz_list_data.clear()
        cl_list_data.clear()
        vat_list_data.clear()
        gvat_list_data.clear()
        t_dnet =  to_decimal("0")


        t_dserv =  to_decimal("0")
        t_dtax =  to_decimal("0")
        t_dgros =  to_decimal("0")
        t_mnet =  to_decimal("0")
        t_mserv =  to_decimal("0")
        t_mtax =  to_decimal("0")
        t_mgros =  to_decimal("0")
        t_ynet =  to_decimal("0")
        t_yserv =  to_decimal("0")
        t_ytax =  to_decimal("0")
        t_ygros =  to_decimal("0")
        gtbudget =  to_decimal("0")

        for artikel in db_session.query(Artikel).filter(
                 ((Artikel.artart == 0) | (Artikel.artart == 8)) & (Artikel.departement >= from_dept) & (Artikel.departement <= to_dept)).order_by(Artikel.artnr).all():

            umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)],"datum": [(ge, from_date),(le, to_date)]})

            if not umsatz:

                not_avail_umstaz = query(not_avail_umstaz_data, filters=(lambda not_avail_umstaz: not_avail_umstaz.artnr == artikel.artnr and not_avail_umstaz.depart == artikel.departement), first=True)

                if not_avail_umstaz:
                    pass
                else:
                    not_avail_umstaz = Not_avail_umstaz()
                    not_avail_umstaz_data.append(not_avail_umstaz)

                    not_avail_umstaz.artnr = artikel.artnr
                    not_avail_umstaz.depart = artikel.departement
                    not_avail_umstaz.bezeich = artikel.bezeich

        for umsatz in db_session.query(Umsatz).filter(
                 (Umsatz.departement >= from_dept) & (Umsatz.departement <= to_dept) & (Umsatz.datum >= from_date) & (Umsatz.datum <= to_date)).order_by(Umsatz.departement, Umsatz.artnr, Umsatz.datum).all():

            if curr_artnr == 0 or curr_artnr != umsatz.artnr or (curr_artnr == umsatz.artnr and curr_departement != umsatz.departement):

                artikel = get_cache (Artikel, {"artnr": [(eq, umsatz.artnr)],"departement": [(eq, umsatz.departement)]})

                if artikel and (artikel.artart == 0 or artikel.artart == 8):

                    if curr_artnr != 0:
                        it_exist = False
                        serv =  to_decimal("0")
                        vat =  to_decimal("0")
                        tbudget =  to_decimal(tbudget) + to_decimal(mbudget)


                    curr_artnr = umsatz.artnr
                    do_it = True


                else:
                    do_it = False

            if do_it :
                counter = counter + 1

                if (curr_departement != umsatz.departement) or counter == 1:

                    if counter != 1:

                        for not_avail_umstaz in query(not_avail_umstaz_data, filters=(lambda not_avail_umstaz: not_avail_umstaz.depart == curr_departement)):

                            budget = db_session.query(Budget).filter(
                                     (get_month(Budget.datum) == get_month(to_date)) & (get_year(Budget.datum) == get_year(to_date)) & (Budget.departement == not_avail_umstaz.depart) & (Budget.artnr == not_avail_umstaz.artnr)).first()

                            if budget and budget.betrag != 0:

                                if not it_exist:
                                    it_exist = True
                                    cl_list = Cl_list()
                                    cl_list_data.append(cl_list)

                                    cl_list.artnr = not_avail_umstaz.artnr
                                    cl_list.dept = not_avail_umstaz.depart
                                    cl_list.bezeich = not_avail_umstaz.bezeich
                                    it_exist = False


                                mbudget = sum_budget(first_date, to_date, not_avail_umstaz.artnr, not_avail_umstaz.depart)
                                mbudget = round(mbudget, 1)
                                cl_list.mbudget =  to_decimal(mbudget)
                                tbudget =  to_decimal(tbudget) + to_decimal(mbudget)


                        tbudget = to_decimal(round(tbudget , 1))

                        for cl_list in query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num)):

                            if dgros != 0:
                                cl_list.proz2 =  to_decimal(cl_list.dgros) / to_decimal(dgros) * to_decimal("100")

                            if mgros != 0:
                                cl_list.proz4 =  to_decimal(cl_list.mgros) / to_decimal(mgros) * to_decimal("100")

                            if ygros != 0:
                                cl_list.proz6 =  to_decimal(cl_list.ygros) / to_decimal(ygros) * to_decimal("100")

                        if totvatflag:

                            for vat_list in query(vat_list_data, filters=(lambda vat_list: vat_list.vat == 0 or (vat_list.ytax == 0))):
                                vat_list_data.remove(vat_list)

                            for vat_list in query(vat_list_data, filters=(lambda vat_list: vat_list.dptnr == hoteldpt.num), sort_by=[("vat",False)]):
                                cl_list = Cl_list()
                                cl_list_data.append(cl_list)

                                cl_list.flag = "**"
                                cl_list.bezeich = "TOTAL vat " + to_string(vat_list.vat * 100, ">>9.99") + " " + "%"
                                cl_list.dnet =  to_decimal(vat_list.dnet)
                                cl_list.dserv =  to_decimal(vat_list.dserv)
                                cl_list.dtax =  to_decimal(vat_list.dtax)
                                cl_list.dgros =  to_decimal(vat_list.dgros)
                                cl_list.mnet =  to_decimal(vat_list.mnet)
                                cl_list.mserv =  to_decimal(vat_list.mserv)
                                cl_list.mtax =  to_decimal(vat_list.mtax)
                                cl_list.mgros =  to_decimal(vat_list.mgros)
                                cl_list.ynet =  to_decimal(vat_list.ynet)
                                cl_list.yserv =  to_decimal(vat_list.yserv)
                                cl_list.ytax =  to_decimal(vat_list.ytax)
                                cl_list.ygros =  to_decimal(vat_list.ygros)


                        cl_list = Cl_list()
                        cl_list_data.append(cl_list)

                        # Rd 20/8/2025
                        cl_list.artnr = ""
                        cl_list.flag = "**"
                        cl_list.bezeich = "T O T A L"
                        cl_list.dnet =  to_decimal(dnet)
                        cl_list.dserv =  to_decimal(dserv)
                        cl_list.dtax =  to_decimal(dtax)
                        cl_list.dgros =  to_decimal(dgros)
                        cl_list.mnet =  to_decimal(mnet)
                        cl_list.mserv =  to_decimal(mserv)
                        cl_list.mtax =  to_decimal(mtax)
                        cl_list.mgros =  to_decimal(mgros)
                        cl_list.ynet =  to_decimal(ynet)
                        cl_list.yserv =  to_decimal(yserv)
                        cl_list.ytax =  to_decimal(ytax)
                        cl_list.ygros =  to_decimal(ygros)
                        cl_list.mbudget =  to_decimal(tbudget)
                        cl_list.dqty = dqty
                        cl_list.mqty = mqty
                        cl_list.yqty = yqty


                        gtbudget =  to_decimal(gtbudget) + to_decimal(tbudget)

                        if dgros != 0:
                            cl_list.proz2 =  to_decimal("100")

                        if mgros != 0:
                            cl_list.proz4 =  to_decimal("100")

                        if ygros != 0:
                            cl_list.proz6 =  to_decimal("100")

                    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, umsatz.departement)]})

                    if hoteldpt:
                        cl_list = Cl_list()
                        cl_list_data.append(cl_list)

                         # Rd 20/8/2025
                        cl_list.artnr = ""
                        cl_list.flag = "*"
                        cl_list.bezeich = to_string(hoteldpt.num) + " - " + hoteldpt.depart
                        dnet =  to_decimal("0")
                        dserv =  to_decimal("0")
                        dtax =  to_decimal("0")
                        dgros =  to_decimal("0")
                        mnet =  to_decimal("0")
                        mserv =  to_decimal("0")
                        mtax =  to_decimal("0")
                        mgros =  to_decimal("0")
                        ynet =  to_decimal("0")
                        yserv =  to_decimal("0")
                        ytax =  to_decimal("0")
                        ygros =  to_decimal("0")
                        tbudget =  to_decimal("0")
                        dqty = 0
                        mqty = 0
                        yqty = 0


                    curr_departement = umsatz.departement


                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, umsatz.artnr, umsatz.departement, umsatz.datum))
                all_vat =  to_decimal(vat) + to_decimal(vat2)

                vat_list = query(vat_list_data, filters=(lambda vat_list: vat_list.vat == vat and vat_list.dptnr == artikel.departement), first=True)

                if not vat_list:
                    vat_list = Vat_list()
                    vat_list_data.append(vat_list)

                    vat_list.vat =  to_decimal(all_vat)
                    vat_list.dptnr = artikel.departement

                if not it_exist:
                    it_exist = True
                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.artnr = umsatz.artnr
                    cl_list.dept = umsatz.departement
                    cl_list.bezeich = artikel.bezeich
                    cl_list.vat_proz =  to_decimal(all_vat)

                if vat == 1 or (artikel.artnr == vat_artnr and artikel.departement == 0):
                    nett_amt =  to_decimal("0")
                    nett_serv =  to_decimal("0")
                    nett_tax =  to_decimal(umsatz.betrag)

                elif matches(vat_str,r"*;" + to_string(artikel.artnr) + r";*") and artikel.departement == 0:
                    nett_amt =  to_decimal("0")
                    nett_serv =  to_decimal("0")
                    nett_tax =  to_decimal(umsatz.betrag)

                elif serv == 1 or (artikel.artnr == serv_artnr and artikel.departement == 0):
                    nett_amt =  to_decimal("0")
                    nett_tax =  to_decimal("0")
                    nett_serv =  to_decimal(umsatz.betrag)


                else:
                    nett_amt =  to_decimal(umsatz.betrag) / to_decimal(fact)
                    nett_serv =  to_decimal(nett_amt) * to_decimal(serv)
                    nett_tax =  to_decimal(nett_amt) * to_decimal(vat)
                    nett_amt =  to_decimal(umsatz.betrag) - to_decimal(nett_serv) - to_decimal(nett_tax)


                mbudget = sum_budget(first_date, to_date, artikel.artnr, artikel.departement)
                mbudget = round(mbudget, 1)
                cl_list.mbudget =  to_decimal(mbudget)

                if umsatz.datum == to_date:
                    cl_list.dnet = ( to_decimal(nett_amt) / to_decimal(fact1) )
                    cl_list.dgros = ( to_decimal(umsatz.betrag) / to_decimal(fact1) )
                    cl_list.dserv = ( to_decimal(nett_serv) / to_decimal(fact1) )
                    cl_list.dtax = ( to_decimal(nett_tax) / to_decimal(fact1) )
                    dnet = to_decimal(dnet + round(cl_list.dnet , price_decimal))
                    dserv = to_decimal(dserv + round(cl_list.dserv , price_decimal))
                    dtax = to_decimal(dtax + round(cl_list.dtax , price_decimal))
                    dgros = to_decimal(dgros + round(cl_list.dgros , price_decimal))
                    t_dnet = to_decimal(t_dnet + round(cl_list.dnet , price_decimal))
                    t_dserv = to_decimal(t_dserv + round(cl_list.dserv , price_decimal))
                    t_dtax = to_decimal(t_dtax + round(cl_list.dtax , price_decimal))
                    t_dgros = to_decimal(t_dgros + round(cl_list.dgros , price_decimal))
                    cl_list.dqty = umsatz.anzahl
                    dqty = dqty + cl_list.dqty
                    t_dqty = t_dqty + cl_list.dqty

                if umsatz.datum == to_date and vat_list:
                    vat_list.dtax =  to_decimal(vat_list.dtax) + to_decimal((nett_tax) / to_decimal(fact1) )
                    vat_list.dnet =  to_decimal(vat_list.dnet) + to_decimal((nett_amt) / to_decimal(fact1) )
                    vat_list.dgros =  to_decimal(vat_list.dgros) + to_decimal((umsatz.betrag) / to_decimal(fact1) )
                    vat_list.dserv =  to_decimal(vat_list.dserv) + to_decimal((nett_serv) / to_decimal(fact1) )

                if umsatz.datum >= first_date and umsatz.datum <= to_date:
                    cl_list.mnet = to_decimal(cl_list.mnet + round((nett_amt / fact1) , price_decimal))
                    cl_list.mserv = to_decimal(cl_list.mserv + round((nett_serv / fact1) , price_decimal))
                    cl_list.mtax = to_decimal(cl_list.mtax + round((nett_tax / fact1) , price_decimal))
                    cl_list.mgros = to_decimal(cl_list.mgros + round((umsatz.betrag / fact1) , price_decimal))
                    mnet = to_decimal(mnet + round((nett_amt / fact1) , price_decimal))
                    mserv = to_decimal(mserv + round((nett_serv / fact1) , price_decimal))
                    mtax = to_decimal(mtax + round((nett_tax / fact1) , price_decimal))
                    mgros = to_decimal(mgros + round((umsatz.betrag / fact1) , price_decimal))
                    t_mnet = to_decimal(t_mnet + round((nett_amt / fact1) , price_decimal))
                    t_mserv = to_decimal(t_mserv + round((nett_serv / fact1) , price_decimal))
                    t_mtax = to_decimal(t_mtax + round((nett_tax / fact1) , price_decimal))
                    t_mgros = to_decimal(t_mgros + round((umsatz.betrag / fact1) , price_decimal))
                    cl_list.mqty = cl_list.mqty + umsatz.anzahl
                    mqty = mqty + umsatz.anzahl
                    t_mqty = t_mqty + umsatz.anzahl

                if umsatz.datum >= first_date and umsatz.datum <= to_date and vat_list:
                    vat_list.mtax =  to_decimal(vat_list.mtax) + to_decimal((nett_tax) / to_decimal(fact1) )
                    vat_list.mnet =  to_decimal(vat_list.mnet) + to_decimal((nett_amt) / to_decimal(fact1) )
                    vat_list.mserv =  to_decimal(vat_list.mserv) + to_decimal((nett_serv) / to_decimal(fact1) )
                    vat_list.mgros =  to_decimal(vat_list.mgros) + to_decimal((umsatz.betrag) / to_decimal(fact1) )


                cl_list.ynet = to_decimal(cl_list.ynet + round((nett_amt / fact1) , price_decimal))
                cl_list.yserv = to_decimal(cl_list.yserv + round((nett_serv / fact1) , price_decimal))
                cl_list.ytax = to_decimal(cl_list.ytax + round((nett_tax / fact1) , price_decimal))
                cl_list.ygros = to_decimal(cl_list.ygros + round((umsatz.betrag / fact1) , price_decimal))
                ynet = to_decimal(ynet + round((nett_amt / fact1) , price_decimal))
                yserv = to_decimal(yserv + round((nett_serv / fact1) , price_decimal))
                ytax = to_decimal(ytax + round((nett_tax / fact1) , price_decimal))
                ygros = to_decimal(ygros + round((umsatz.betrag / fact1) , price_decimal))
                t_ynet = to_decimal(t_ynet + round((nett_amt / fact1) , price_decimal))
                t_yserv = to_decimal(t_yserv + round((nett_serv / fact1) , price_decimal))
                t_ytax = to_decimal(t_ytax + round((nett_tax / fact1) , price_decimal))
                t_ygros = to_decimal(t_ygros + round((umsatz.betrag / fact1) , price_decimal))
                cl_list.yqty = cl_list.yqty + umsatz.anzahl
                yqty = yqty + umsatz.anzahl
                t_yqty = t_yqty + umsatz.anzahl

                if vat_list:
                    vat_list.ytax =  to_decimal(vat_list.ytax) + to_decimal((nett_tax) / to_decimal(fact1) )
                    vat_list.ynet =  to_decimal(vat_list.ynet) + to_decimal((nett_amt) / to_decimal(fact1) )
                    vat_list.yserv =  to_decimal(vat_list.yserv) + to_decimal((nett_serv) / to_decimal(fact1) )
                    vat_list.ygros =  to_decimal(vat_list.ygros) + to_decimal((umsatz.betrag) / to_decimal(fact1) )

        if counter != 1:

            for not_avail_umstaz in query(not_avail_umstaz_data, filters=(lambda not_avail_umstaz: not_avail_umstaz.depart == curr_departement)):

                budget = db_session.query(Budget).filter(
                         (get_month(Budget.datum) == get_month(to_date)) & (get_year(Budget.datum) == get_year(to_date)) & (Budget.departement == not_avail_umstaz.depart) & (Budget.artnr == not_avail_umstaz.artnr)).first()

                if budget and budget.betrag != 0:

                    if not it_exist:
                        it_exist = True
                        cl_list = Cl_list()
                        cl_list_data.append(cl_list)

                        cl_list.artnr = not_avail_umstaz.artnr
                        cl_list.dept = not_avail_umstaz.depart
                        cl_list.bezeich = not_avail_umstaz.bezeich
                        it_exist = False


                    mbudget = sum_budget(first_date, to_date, not_avail_umstaz.artnr, not_avail_umstaz.depart)
                    mbudget = round(mbudget, 1)
                    cl_list.mbudget =  to_decimal(mbudget)
                    tbudget =  to_decimal(tbudget) + to_decimal(mbudget)


            tbudget = to_decimal(round(tbudget , 1))

            for cl_list in query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num)):

                if dgros != 0:
                    cl_list.proz2 =  to_decimal(cl_list.dgros) / to_decimal(dgros) * to_decimal("100")

                if mgros != 0:
                    cl_list.proz4 =  to_decimal(cl_list.mgros) / to_decimal(mgros) * to_decimal("100")

                if ygros != 0:
                    cl_list.proz6 =  to_decimal(cl_list.ygros) / to_decimal(ygros) * to_decimal("100")

            if totvatflag:

                for vat_list in query(vat_list_data, filters=(lambda vat_list: vat_list.vat == 0 or (vat_list.ytax == 0))):
                    vat_list_data.remove(vat_list)

                for vat_list in query(vat_list_data, filters=(lambda vat_list: vat_list.dptnr == hoteldpt.num), sort_by=[("vat",False)]):
                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.flag = "**"
                    cl_list.bezeich = "TOTAL vat " + to_string(vat_list.vat * 100, ">>9.99") + " " + "%"
                    cl_list.dnet =  to_decimal(vat_list.dnet)
                    cl_list.dserv =  to_decimal(vat_list.dserv)
                    cl_list.dtax =  to_decimal(vat_list.dtax)
                    cl_list.dgros =  to_decimal(vat_list.dgros)
                    cl_list.mnet =  to_decimal(vat_list.mnet)
                    cl_list.mserv =  to_decimal(vat_list.mserv)
                    cl_list.mtax =  to_decimal(vat_list.mtax)
                    cl_list.mgros =  to_decimal(vat_list.mgros)
                    cl_list.ynet =  to_decimal(vat_list.ynet)
                    cl_list.yserv =  to_decimal(vat_list.yserv)
                    cl_list.ytax =  to_decimal(vat_list.ytax)
                    cl_list.ygros =  to_decimal(vat_list.ygros)


            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            # Rd 20/8/2025
            cl_list.artnr = ""
            cl_list.flag = "**"
            cl_list.bezeich = "T O T A L"
            cl_list.dnet =  to_decimal(dnet)
            cl_list.dserv =  to_decimal(dserv)
            cl_list.dtax =  to_decimal(dtax)
            cl_list.dgros =  to_decimal(dgros)
            cl_list.mnet =  to_decimal(mnet)
            cl_list.mserv =  to_decimal(mserv)
            cl_list.mtax =  to_decimal(mtax)
            cl_list.mgros =  to_decimal(mgros)
            cl_list.ynet =  to_decimal(ynet)
            cl_list.yserv =  to_decimal(yserv)
            cl_list.ytax =  to_decimal(ytax)
            cl_list.ygros =  to_decimal(ygros)
            cl_list.mbudget =  to_decimal(tbudget)
            cl_list.dqty = dqty
            cl_list.mqty = mqty
            cl_list.yqty = yqty


            gtbudget =  to_decimal(gtbudget) + to_decimal(tbudget)

            if dgros != 0:
                cl_list.proz2 =  to_decimal("100")

            if mgros != 0:
                cl_list.proz4 =  to_decimal("100")

            if ygros != 0:
                cl_list.proz6 =  to_decimal("100")

        for cl_list in query(cl_list_data):

            if cl_list.flag.lower()  == ("*").lower() :
                umsz_list = Umsz_list()
                umsz_list_data.append(umsz_list)

                umsz_list.artnr = to_string(cl_list.artnr, ">>>>")
                umsz_list.bezeich = cl_list.bezeich


            else:

                if price_decimal == 2:
                    umsz_list = Umsz_list()
                    umsz_list_data.append(umsz_list)

                    umsz_list.artnr = to_string(cl_list.artnr, ">>>>")
                    umsz_list.bezeich = cl_list.bezeich
                    umsz_list.day_nett = to_string(round(cl_list.dnet, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.day_serv = to_string(round(cl_list.dserv, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.day_tax = to_string(round(cl_list.dtax, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.day_gros = to_string(round(cl_list.dgros, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.day_persen = to_string(round(cl_list.proz2, price_decimal) , "->>>>9.99")
                    umsz_list.mtd_nett = to_string(round(cl_list.mnet, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.mtd_serv = to_string(round(cl_list.mserv, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.mtd_tax = to_string(round(cl_list.mtax, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.mtd_gros = to_string(round(cl_list.mgros, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.mtd_persen = to_string(round(cl_list.proz4, price_decimal) , "->>>>9.99")
                    umsz_list.ytd_nett = to_string(round(cl_list.ynet, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.ytd_serv = to_string(round(cl_list.yserv, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.ytd_tax = to_string(round(cl_list.ytax, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.ytd_gros = to_string(round(cl_list.ygros, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.ytd_persen = to_string(round(cl_list.proz6, price_decimal) , "->>>>9.99")
                    umsz_list.month_bud = to_string(round(cl_list.mbudget, price_decimal) , "->,>>>,>>>,>>>,>>9.99")


                else:
                    umsz_list = Umsz_list()
                    umsz_list_data.append(umsz_list)

                    umsz_list.artnr = to_string(cl_list.artnr, ">>>>")
                    umsz_list.bezeich = cl_list.bezeich
                    umsz_list.day_nett = to_string(round(cl_list.dnet, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.day_serv = to_string(round(cl_list.dserv, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.day_tax = to_string(round(cl_list.dtax, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.day_gros = to_string(round(cl_list.dgros, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.day_persen = to_string(round(cl_list.proz2, price_decimal) , "->>>>9")
                    umsz_list.mtd_nett = to_string(round(cl_list.mnet, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.mtd_serv = to_string(round(cl_list.mserv, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.mtd_tax = to_string(round(cl_list.mtax, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.mtd_gros = to_string(round(cl_list.mgros, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.mtd_persen = to_string(round(cl_list.proz4, price_decimal) , "->>>>9")
                    umsz_list.ytd_nett = to_string(round(cl_list.ynet, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.ytd_serv = to_string(round(cl_list.yserv, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.ytd_tax = to_string(round(cl_list.ytax, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.ytd_gros = to_string(round(cl_list.ygros, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.ytd_persen = to_string(round(cl_list.proz6, price_decimal) , "->>>>9")
                    umsz_list.month_bud = to_string(round(cl_list.mbudget, price_decimal) , "->,>>>,>>>,>>>,>>9")


                umsz_list.dqty = to_string(cl_list.dqty, "->>>>>>9")
                umsz_list.mqty = to_string(cl_list.mqty, "->>>>>>9")
                umsz_list.yqty = to_string(cl_list.yqty, "->>>>>>9")

        if totvatflag:

            for vat_list in query(vat_list_data, sort_by=[("vat",False)]):

                gvat_list = query(gvat_list_data, filters=(lambda gvat_list: gvat_list.vat == vat_list.vat), first=True)

                if not gvat_list:
                    gvat_list = Gvat_list()
                    gvat_list_data.append(gvat_list)

                    gvat_list.vat =  to_decimal(vat_list.vat)


                gvat_list.dnet =  to_decimal(gvat_list.dnet) + to_decimal(vat_list.dnet)
                gvat_list.dserv =  to_decimal(gvat_list.dserv) + to_decimal(vat_list.dserv)
                gvat_list.dtax =  to_decimal(gvat_list.dtax) + to_decimal(vat_list.dtax)
                gvat_list.dgros =  to_decimal(gvat_list.dgros) + to_decimal(vat_list.dgros)
                gvat_list.mnet =  to_decimal(gvat_list.mnet) + to_decimal(vat_list.mnet)
                gvat_list.mserv =  to_decimal(gvat_list.mserv) + to_decimal(vat_list.mserv)
                gvat_list.mtax =  to_decimal(gvat_list.mtax) + to_decimal(vat_list.mtax)
                gvat_list.mgros =  to_decimal(gvat_list.mgros) + to_decimal(vat_list.mgros)
                gvat_list.ynet =  to_decimal(gvat_list.ynet) + to_decimal(vat_list.ynet)
                gvat_list.yserv =  to_decimal(gvat_list.yserv) + to_decimal(vat_list.yserv)
                gvat_list.ytax =  to_decimal(gvat_list.ytax) + to_decimal(vat_list.ytax)
                gvat_list.ygros =  to_decimal(gvat_list.ygros) + to_decimal(vat_list.ygros)

            for gvat_list in query(gvat_list_data, sort_by=[("vat",False)]):
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.flag = "**"
                cl_list.bezeich = "GTOTAL vat " + to_string(gvat_list.vat * 100, ">>9.99") + " " + "%"
                cl_list.dnet =  to_decimal(gvat_list.dnet)
                cl_list.dserv =  to_decimal(gvat_list.dserv)
                cl_list.dtax =  to_decimal(gvat_list.dtax)
                cl_list.dgros =  to_decimal(gvat_list.dgros)
                cl_list.mnet =  to_decimal(gvat_list.mnet)
                cl_list.mserv =  to_decimal(gvat_list.mserv)
                cl_list.mtax =  to_decimal(gvat_list.mtax)
                cl_list.mgros =  to_decimal(gvat_list.mgros)
                cl_list.ynet =  to_decimal(gvat_list.ynet)
                cl_list.yserv =  to_decimal(gvat_list.yserv)
                cl_list.ytax =  to_decimal(gvat_list.ytax)
                cl_list.ygros =  to_decimal(gvat_list.ygros)


                umsz_list = Umsz_list()
                umsz_list_data.append(umsz_list)


                if price_decimal == 2:
                    umsz_list.artnr = to_string(cl_list.artnr, ">>>>")
                    umsz_list.bezeich = cl_list.bezeich
                    umsz_list.day_nett = to_string(round(cl_list.dnet, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.day_serv = to_string(round(cl_list.dserv, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.day_tax = to_string(round(cl_list.dtax, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.day_gros = to_string(round(cl_list.dgros, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.day_persen = to_string(round(cl_list.proz2, price_decimal) , "->>>>9.99")
                    umsz_list.mtd_nett = to_string(round(cl_list.mnet, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.mtd_serv = to_string(round(cl_list.mserv, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.mtd_tax = to_string(round(cl_list.mtax, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.mtd_gros = to_string(round(cl_list.mgros, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.mtd_persen = to_string(round(cl_list.proz4, price_decimal) , "->>>>9.99")
                    umsz_list.ytd_nett = to_string(round(cl_list.ynet, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.ytd_serv = to_string(round(cl_list.yserv, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.ytd_tax = to_string(round(cl_list.ytax, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.ytd_gros = to_string(round(cl_list.ygros, price_decimal) , "->>>,>>>,>>>,>>9.99")
                    umsz_list.ytd_persen = to_string(round(cl_list.proz6, price_decimal) , "->>>>9.99")
                    umsz_list.month_bud = to_string(round(cl_list.mbudget, price_decimal) , "->,>>>,>>>,>>>,>>9.99")


                else:
                    umsz_list.artnr = to_string(cl_list.artnr, ">>>>")
                    umsz_list.bezeich = cl_list.bezeich
                    umsz_list.day_nett = to_string(round(cl_list.dnet, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.day_serv = to_string(round(cl_list.dserv, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.day_tax = to_string(round(cl_list.dtax, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.day_gros = to_string(round(cl_list.dgros, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.day_persen = to_string(round(cl_list.proz2, price_decimal) , "->>>>9")
                    umsz_list.mtd_nett = to_string(round(cl_list.mnet, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.mtd_serv = to_string(round(cl_list.mserv, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.mtd_tax = to_string(round(cl_list.mtax, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.mtd_gros = to_string(round(cl_list.mgros, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.mtd_persen = to_string(round(cl_list.proz4, price_decimal) , "->>>>9")
                    umsz_list.ytd_nett = to_string(round(cl_list.ynet, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.ytd_serv = to_string(round(cl_list.yserv, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.ytd_tax = to_string(round(cl_list.ytax, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.ytd_gros = to_string(round(cl_list.ygros, price_decimal) , "->>>,>>>,>>>,>>9")
                    umsz_list.ytd_persen = to_string(round(cl_list.proz6, price_decimal) , "->>>>9")
                    umsz_list.month_bud = to_string(round(cl_list.mbudget, price_decimal) , "->,>>>,>>>,>>>,>>9")


        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        # Rd 20/8/2025
        cl_list.artnr = ""
        cl_list.flag = "***"
        cl_list.bezeich = "GRAND TOTAL"
        cl_list.dnet =  to_decimal(t_dnet)
        cl_list.dserv =  to_decimal(t_dserv)
        cl_list.dtax =  to_decimal(t_dtax)
        cl_list.dgros =  to_decimal(t_dgros)
        cl_list.mnet =  to_decimal(t_mnet)
        cl_list.mserv =  to_decimal(t_mserv)
        cl_list.mtax =  to_decimal(t_mtax)
        cl_list.mgros =  to_decimal(t_mgros)
        cl_list.ynet =  to_decimal(t_ynet)
        cl_list.yserv =  to_decimal(t_yserv)
        cl_list.ytax =  to_decimal(t_ytax)
        cl_list.ygros =  to_decimal(t_ygros)
        cl_list.mbudget =  to_decimal(gtbudget)
        cl_list.dqty = t_dqty
        cl_list.mqty = t_mqty
        cl_list.yqty = t_yqty

        if t_dgros != 0:
            cl_list.proz2 =  to_decimal("100")

        if t_mgros != 0:
            cl_list.proz4 =  to_decimal("100")

        if t_ygros != 0:
            cl_list.proz6 =  to_decimal("100")
        umsz_list = Umsz_list()
        umsz_list_data.append(umsz_list)


        if price_decimal == 2:
            umsz_list.artnr = to_string(cl_list.artnr, ">>>>")
            umsz_list.bezeich = cl_list.bezeich
            umsz_list.day_nett = to_string(round(cl_list.dnet, price_decimal) , "->>>,>>>,>>>,>>9.99")
            umsz_list.day_serv = to_string(round(cl_list.dserv, price_decimal) , "->>>,>>>,>>>,>>9.99")
            umsz_list.day_tax = to_string(round(cl_list.dtax, price_decimal) , "->>>,>>>,>>>,>>9.99")
            umsz_list.day_gros = to_string(round(cl_list.dgros, price_decimal) , "->>>,>>>,>>>,>>9.99")
            umsz_list.day_persen = to_string(round(cl_list.proz2, price_decimal) , "->>>>9.99")
            umsz_list.mtd_nett = to_string(round(cl_list.mnet, price_decimal) , "->>>,>>>,>>>,>>9.99")
            umsz_list.mtd_serv = to_string(round(cl_list.mserv, price_decimal) , "->>>,>>>,>>>,>>9.99")
            umsz_list.mtd_tax = to_string(round(cl_list.mtax, price_decimal) , "->>>,>>>,>>>,>>9.99")
            umsz_list.mtd_gros = to_string(round(cl_list.mgros, price_decimal) , "->>>,>>>,>>>,>>9.99")
            umsz_list.mtd_persen = to_string(round(cl_list.proz4, price_decimal) , "->>>>9.99")
            umsz_list.ytd_nett = to_string(round(cl_list.ynet, price_decimal) , "->>>,>>>,>>>,>>9.99")
            umsz_list.ytd_serv = to_string(round(cl_list.yserv, price_decimal) , "->>>,>>>,>>>,>>9.99")
            umsz_list.ytd_tax = to_string(round(cl_list.ytax, price_decimal) , "->>>,>>>,>>>,>>9.99")
            umsz_list.ytd_gros = to_string(round(cl_list.ygros, price_decimal) , "->>>,>>>,>>>,>>9.99")
            umsz_list.ytd_persen = to_string(round(cl_list.proz6, price_decimal) , "->>>>9.99")
            umsz_list.month_bud = to_string(round(cl_list.mbudget, price_decimal) , "->,>>>,>>>,>>>,>>9.99")


        else:
            umsz_list.artnr = to_string(cl_list.artnr, ">>>>")
            umsz_list.bezeich = cl_list.bezeich
            umsz_list.day_nett = to_string(round(cl_list.dnet, price_decimal) , "->>>,>>>,>>>,>>9")
            umsz_list.day_serv = to_string(round(cl_list.dserv, price_decimal) , "->>>,>>>,>>>,>>9")
            umsz_list.day_tax = to_string(round(cl_list.dtax, price_decimal) , "->>>,>>>,>>>,>>9")
            umsz_list.day_gros = to_string(round(cl_list.dgros, price_decimal) , "->>>,>>>,>>>,>>9")
            umsz_list.day_persen = to_string(round(cl_list.proz2, price_decimal) , "->>>>9")
            umsz_list.mtd_nett = to_string(round(cl_list.mnet, price_decimal) , "->>>,>>>,>>>,>>9")
            umsz_list.mtd_serv = to_string(round(cl_list.mserv, price_decimal) , "->>>,>>>,>>>,>>9")
            umsz_list.mtd_tax = to_string(round(cl_list.mtax, price_decimal) , "->>>,>>>,>>>,>>9")
            umsz_list.mtd_gros = to_string(round(cl_list.mgros, price_decimal) , "->>>,>>>,>>>,>>9")
            umsz_list.mtd_persen = to_string(round(cl_list.proz4, price_decimal) , "->>>>9")
            umsz_list.ytd_nett = to_string(round(cl_list.ynet, price_decimal) , "->>>,>>>,>>>,>>9")
            umsz_list.ytd_serv = to_string(round(cl_list.yserv, price_decimal) , "->>>,>>>,>>>,>>9")
            umsz_list.ytd_tax = to_string(round(cl_list.ytax, price_decimal) , "->>>,>>>,>>>,>>9")
            umsz_list.ytd_gros = to_string(round(cl_list.ygros, price_decimal) , "->>>,>>>,>>>,>>9")
            umsz_list.ytd_persen = to_string(round(cl_list.proz6, price_decimal) , "->>>>9")
            umsz_list.month_bud = to_string(round(cl_list.mbudget, price_decimal) , "->,>>>,>>>,>>>,>>9")


        umsz_list.dqty = to_string(cl_list.dqty, "->>>>>>9")
        umsz_list.mqty = to_string(cl_list.mqty, "->>>>>>9")
        umsz_list.yqty = to_string(cl_list.yqty, "->>>>>>9")


    def sum_budget(from_date:date, to_date:date, artnr:int, deptno:int):

        nonlocal umsz_list_data, vhp_limited, vat_str, vat_artnr, serv_artnr, price_decimal, htparam, umsatz, artikel, budget, hoteldpt, kontplan
        nonlocal from_dept, to_dept, first_date, totvatflag


        nonlocal umsz_list, cl_list, vat_list, gvat_list, not_avail_umstaz
        nonlocal umsz_list_data, cl_list_data, vat_list_data, gvat_list_data, not_avail_umstaz_data

        mbudget = to_decimal("0.0")
        tmp_from_date:date = None
        tmp_to_date:date = None

        def generate_inner_output():
            return (mbudget)

        tmp_from_date, tmp_to_date = calculate_date_range(to_date)

        for budget in db_session.query(Budget).filter(
                 (Budget.datum >= tmp_from_date) & (Budget.datum <= tmp_to_date) & (Budget.departement == deptno) & (Budget.artnr == artnr)).order_by(Budget._recid).all():
            mbudget =  to_decimal(mbudget) + to_decimal(budget.betrag)

        return generate_inner_output()


    def calculate_date_range(input_date:date):

        nonlocal umsz_list_data, vhp_limited, vat_str, vat_artnr, serv_artnr, price_decimal, htparam, umsatz, artikel, budget, hoteldpt, kontplan
        nonlocal from_dept, to_dept, first_date, from_date, to_date, totvatflag


        nonlocal umsz_list, cl_list, vat_list, gvat_list, not_avail_umstaz
        nonlocal umsz_list_data, cl_list_data, vat_list_data, gvat_list_data, not_avail_umstaz_data

        from_date = None
        to_date = None

        def generate_inner_output():
            return (from_date, to_date)

        from_date = date_mdy(get_month(input_date) , 1, get_year(input_date))
        to_date = from_date + timedelta(days=31)
        to_date = date_mdy(get_month(to_date) , 1, get_year(to_date))
        to_date = to_date - timedelta(days=1)

        return generate_inner_output()


    htparam = get_cache (Htparam, {"paramnr": [(eq, 132)]})
    vat_artnr = htparam.finteger
    vat_str = htparam.fchar

    if vat_str != "":

        if substring(vat_str, 0, 1) != (";").lower() :
            vat_str = ";" + vat_str

        if substring(vat_str, length(vat_str) - 1, 1) != (";").lower() :
            vat_str = vat_str + ";"
    serv_artnr = get_output(htpint(133))
    price_decimal = get_output(htpint(491))
    create_umsatz()

    return generate_output()