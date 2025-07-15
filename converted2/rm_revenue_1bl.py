#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zimmer, Zinrstat, Zimkateg, Genstat

def rm_revenue_1bl(m_ftd:bool, m_ytd:bool, f_date:date, t_date:date, to_date:date, rm_no:string, sorttype:int, lod__rev:bool):

    prepare_cache ([Zimmer, Zinrstat, Zimkateg, Genstat])

    output_list_data = []
    i:int = 0
    anz:int = 0
    manz:int = 0
    yanz:int = 0
    pax:int = 0
    mpax:int = 0
    ypax:int = 0
    mnet:Decimal = to_decimal("0.0")
    ynet:Decimal = to_decimal("0.0")
    net:Decimal = to_decimal("0.0")
    t_anz:int = 0
    t_manz:int = 0
    t_yanz:int = 0
    t_pax:int = 0
    t_mpax:int = 0
    t_ypax:int = 0
    t_net:Decimal = to_decimal("0.0")
    t_mnet:Decimal = to_decimal("0.0")
    t_ynet:Decimal = to_decimal("0.0")
    from_bez:string = ""
    to_bez:string = ""
    price_decimal:int = 0
    from_date:date = None
    zimmer = zinrstat = zimkateg = genstat = None

    output_list = cl_list = None

    output_list_data, Output_list = create_model("Output_list", {"rmno":string, "flag":string, "str":string})
    cl_list_data, Cl_list = create_model("Cl_list", {"flag":string, "zinr":string, "rmcat":string, "anz":int, "pax":int, "net":Decimal, "proz":Decimal, "manz":int, "mpax":int, "mnet":Decimal, "proz1":Decimal, "yanz":int, "ypax":int, "ynet":Decimal, "proz2":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, i, anz, manz, yanz, pax, mpax, ypax, mnet, ynet, net, t_anz, t_manz, t_yanz, t_pax, t_mpax, t_ypax, t_net, t_mnet, t_ynet, from_bez, to_bez, price_decimal, from_date, zimmer, zinrstat, zimkateg, genstat
        nonlocal m_ftd, m_ytd, f_date, t_date, to_date, rm_no, sorttype, lod__rev


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        return {"output-list": output_list_data}

    def create_zinrstat():

        nonlocal output_list_data, i, anz, manz, yanz, pax, mpax, ypax, mnet, ynet, net, t_anz, t_manz, t_yanz, t_pax, t_mpax, t_ypax, t_net, t_mnet, t_ynet, from_bez, to_bez, price_decimal, from_date, zimmer, zinrstat, zimkateg, genstat
        nonlocal m_ftd, m_ytd, f_date, t_date, to_date, rm_no, sorttype, lod__rev


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        mm:int = 0
        yy:int = 0
        datum:date = None
        last_zikatnr:int = 0
        anz = 0
        pax = 0
        net =  to_decimal("0")
        manz = 0
        mpax = 0
        mnet =  to_decimal("0")
        yanz = 0
        ypax = 0
        ynet =  to_decimal("0")
        t_anz = 0
        t_pax = 0
        t_manz = 0
        t_mpax = 0
        t_mnet =  to_decimal("0")
        t_yanz = 0
        t_ypax = 0
        t_ynet =  to_decimal("0")

        if m_ftd  and m_ytd == False:
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)

        elif m_ftd == False and m_ytd :
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
        output_list_data.clear()
        cl_list_data.clear()

        if rm_no != "":

            zimmer = get_cache (Zimmer, {"zinr": [(eq, rm_no)]})

            if zimmer:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.zinr = rm_no
                cl_list.rmcat = zimmer.kbezeich
                for datum in date_range(from_date,to_date) :

                    zinrstat = get_cache (Zinrstat, {"zinr": [(eq, rm_no)],"datum": [(eq, datum)],"zimmeranz": [(gt, 0)]})

                    if zinrstat:

                        if datum == to_date:
                            cl_list.anz = cl_list.anz + zinrstat.zimmeranz
                            cl_list.net =  to_decimal(cl_list.net) + to_decimal(zinrstat.argtumsatz)
                            cl_list.pax = cl_list.pax + zinrstat.person
                            anz = anz + zinrstat.zimmeranz
                            pax = pax + zinrstat.person
                            net =  to_decimal(net) + to_decimal(zinrstat.argtumsatz)

                        if get_month(zinrstat.datum) == mm and get_year(zinrstat.datum) == yy:
                            cl_list.manz = cl_list.manz + zinrstat.zimmeranz
                            cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(zinrstat.argtumsatz)
                            cl_list.mpax = cl_list.mpax + zinrstat.person
                            manz = manz + zinrstat.zimmeranz
                            mpax = mpax + zinrstat.person
                            mnet =  to_decimal(mnet) + to_decimal(zinrstat.argtumsatz)
                        cl_list.yanz = cl_list.yanz + zinrstat.zimmeranz
                        cl_list.ypax = cl_list.ypax + zinrstat.person
                        cl_list.ynet =  to_decimal(cl_list.ynet) + to_decimal(zinrstat.argtumsatz)
                        yanz = yanz + zinrstat.zimmeranz
                        ypax = ypax + zinrstat.person
                        ynet =  to_decimal(ynet) + to_decimal(zinrstat.argtumsatz)
        else:
            rm_no = ""

            if sorttype == 1:

                zimmer_obj_list = {}
                zimmer = Zimmer()
                zimkateg = Zimkateg()
                for zimmer.kbezeich, zimmer.zinr, zimmer.zikatnr, zimmer._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Zimmer.kbezeich, Zimmer.zinr, Zimmer.zikatnr, Zimmer._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).order_by(Zimmer.zinr).all():
                    if zimmer_obj_list.get(zimmer._recid):
                        continue
                    else:
                        zimmer_obj_list[zimmer._recid] = True


                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.zinr = zimmer.zinr
                    cl_list.rmcat = zimkateg.kurzbez
                    for datum in date_range(from_date,to_date) :

                        zinrstat = get_cache (Zinrstat, {"zinr": [(eq, zimmer.zinr)],"datum": [(eq, datum)],"zimmeranz": [(gt, 0)]})

                        if zinrstat:

                            if datum == to_date:
                                cl_list.anz = cl_list.anz + zinrstat.zimmeranz
                                cl_list.net =  to_decimal(cl_list.net) + to_decimal(zinrstat.argtumsatz)
                                cl_list.pax = cl_list.pax + zinrstat.person
                                anz = anz + zinrstat.zimmeranz
                                pax = pax + zinrstat.person
                                net =  to_decimal(net) + to_decimal(zinrstat.argtumsatz)

                            if get_month(zinrstat.datum) == mm and get_year(zinrstat.datum) == yy:
                                cl_list.manz = cl_list.manz + zinrstat.zimmeranz
                                cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(zinrstat.argtumsatz)
                                cl_list.mpax = cl_list.mpax + zinrstat.person
                                manz = manz + zinrstat.zimmeranz
                                mpax = mpax + zinrstat.person
                                mnet =  to_decimal(mnet) + to_decimal(zinrstat.argtumsatz)
                            cl_list.yanz = cl_list.yanz + zinrstat.zimmeranz
                            cl_list.ypax = cl_list.ypax + zinrstat.person
                            cl_list.ynet =  to_decimal(cl_list.ynet) + to_decimal(zinrstat.argtumsatz)
                            yanz = yanz + zinrstat.zimmeranz
                            ypax = ypax + zinrstat.person
                            ynet =  to_decimal(ynet) + to_decimal(zinrstat.argtumsatz)


            elif sorttype == 2:

                zimmer_obj_list = {}
                zimmer = Zimmer()
                zimkateg = Zimkateg()
                for zimmer.kbezeich, zimmer.zinr, zimmer.zikatnr, zimmer._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Zimmer.kbezeich, Zimmer.zinr, Zimmer.zikatnr, Zimmer._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).order_by(Zimkateg.zikatnr, Zimmer.zinr).all():
                    if zimmer_obj_list.get(zimmer._recid):
                        continue
                    else:
                        zimmer_obj_list[zimmer._recid] = True

                    if last_zikatnr == 0:
                        last_zikatnr = zimmer.zikatnr

                    if last_zikatnr != zimmer.zikatnr:
                        cl_list = Cl_list()
                        cl_list_data.append(cl_list)

                        cl_list.rmcat = "Total"
                        cl_list.anz = t_anz
                        cl_list.pax = t_pax
                        cl_list.net =  to_decimal(t_net)
                        cl_list.manz = t_manz
                        cl_list.mnet =  to_decimal(t_mnet)
                        cl_list.mpax = t_mpax
                        cl_list.yanz = t_yanz
                        cl_list.ypax = t_ypax
                        cl_list.ynet =  to_decimal(t_ynet)
                        t_anz = 0
                        t_pax = 0
                        t_net =  to_decimal("0")
                        t_manz = 0
                        t_mnet =  to_decimal("0")
                        t_mpax = 0
                        t_yanz = 0
                        t_ynet =  to_decimal("0")
                        t_ypax = 0


                        last_zikatnr = zimmer.zikatnr
                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.zinr = zimmer.zinr
                    cl_list.rmcat = zimkateg.kurzbez
                    for datum in date_range(from_date,to_date) :

                        zinrstat = get_cache (Zinrstat, {"zinr": [(eq, zimmer.zinr)],"datum": [(eq, datum)],"zimmeranz": [(gt, 0)]})

                        if zinrstat:

                            if datum == to_date:
                                cl_list.anz = cl_list.anz + zinrstat.zimmeranz
                                cl_list.net =  to_decimal(cl_list.net) + to_decimal(zinrstat.argtumsatz)
                                cl_list.pax = cl_list.pax + zinrstat.person
                                anz = anz + zinrstat.zimmeranz
                                pax = pax + zinrstat.person
                                net =  to_decimal(net) + to_decimal(zinrstat.argtumsatz)
                                t_anz = t_anz + zinrstat.zimmeranz
                                t_pax = t_pax + zinrstat.person
                                t_net =  to_decimal(t_net) + to_decimal(zinrstat.argtumsatz)

                            if get_month(zinrstat.datum) == mm:
                                cl_list.manz = cl_list.manz + zinrstat.zimmeranz
                                cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(zinrstat.argtumsatz)
                                cl_list.mpax = cl_list.mpax + zinrstat.person
                                manz = manz + zinrstat.zimmeranz
                                mpax = mpax + zinrstat.person
                                mnet =  to_decimal(mnet) + to_decimal(zinrstat.argtumsatz)
                                t_manz = t_manz + zinrstat.zimmeranz
                                t_mpax = t_mpax + zinrstat.person
                                t_mnet =  to_decimal(t_mnet) + to_decimal(zinrstat.argtumsatz)
                            cl_list.yanz = cl_list.yanz + zinrstat.zimmeranz
                            cl_list.ypax = cl_list.ypax + zinrstat.person
                            cl_list.ynet =  to_decimal(cl_list.ynet) + to_decimal(zinrstat.argtumsatz)
                            yanz = yanz + zinrstat.zimmeranz
                            ypax = ypax + zinrstat.person
                            ynet =  to_decimal(ynet) + to_decimal(zinrstat.argtumsatz)
                            t_yanz = t_yanz + zinrstat.zimmeranz
                            t_ypax = t_ypax + zinrstat.person
                            t_ynet =  to_decimal(t_ynet) + to_decimal(zinrstat.argtumsatz)


            if sorttype == 2:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.rmcat = "Total"
                cl_list.anz = t_anz
                cl_list.pax = t_pax
                cl_list.net =  to_decimal(t_net)
                cl_list.manz = t_manz
                cl_list.mnet =  to_decimal(t_mnet)
                cl_list.mpax = t_mpax
                cl_list.yanz = t_yanz
                cl_list.ypax = t_ypax
                cl_list.ynet =  to_decimal(t_ynet)


                t_anz = 0
                t_pax = 0
                t_net =  to_decimal("0")
                t_manz = 0
                t_mnet =  to_decimal("0")
                t_mpax = 0
                t_yanz = 0
                t_ynet =  to_decimal("0")
                t_ypax = 0

        for cl_list in query(cl_list_data):

            if net != 0:
                cl_list.proz =  to_decimal(cl_list.net) / to_decimal(net) * to_decimal("100")

            if mnet != 0:
                cl_list.proz1 =  to_decimal(cl_list.mnet) / to_decimal(mnet) * to_decimal("100")

            if ynet != 0:
                cl_list.proz2 =  to_decimal(cl_list.ynet) / to_decimal(ynet) * to_decimal("100")
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = "*"
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.zinr = ""
        cl_list.rmcat = "GTOTAL"
        cl_list.anz = anz
        cl_list.pax = pax
        cl_list.net =  to_decimal(net)

        if net != 0:
            cl_list.proz1 =  to_decimal("100")
        cl_list.manz = manz
        cl_list.mpax = mpax
        cl_list.mnet =  to_decimal(mnet)

        if mnet != 0:
            cl_list.proz1 =  to_decimal("100")
        cl_list.yanz = yanz
        cl_list.ypax = ypax
        cl_list.ynet =  to_decimal(ynet)

        if ynet != 0:
            cl_list.proz2 =  to_decimal("100")

        for cl_list in query(cl_list_data):
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = cl_list.flag
            output_list.rmno = cl_list.zinr

            if cl_list.flag.lower()  == ("*").lower() :
                output_list.str = fill("-", 115)
            else:

                if price_decimal == 0:
                    output_list.str = to_string(cl_list.zinr, "x(6)") + to_string(cl_list.rmcat, "x(6)") + to_string(cl_list.manz, ">>,>>9") + to_string(cl_list.mpax, ">>,>>9") + to_string(cl_list.mnet, "->,>>>,>>>,>>>,>>9") + to_string(cl_list.proz1, "->>9.99") + to_string(cl_list.yanz, ">>>,>>9") + to_string(cl_list.ypax, ">>>,>>9") + to_string(cl_list.ynet, "->,>>>,>>>,>>>,>>9") + to_string(cl_list.proz2, "->>9.99") + to_string(cl_list.anz, ">>9") + to_string(cl_list.pax, ">>9") + to_string(cl_list.net, "->>,>>>,>>>,>>9") + to_string(cl_list.proz, "->>9.99")
                else:
                    output_list.str = to_string(cl_list.zinr, "x(6)") + to_string(cl_list.rmcat, "x(6)") + to_string(cl_list.manz, ">>,>>9") + to_string(cl_list.mpax, ">>,>>9") + to_string(cl_list.mnet, "->>,>>>,>>>,>>9.99") + to_string(cl_list.proz1, "->>9.99") + to_string(cl_list.yanz, ">>>,>>9") + to_string(cl_list.ypax, ">>>,>>9") + to_string(cl_list.ynet, "->>,>>>,>>>,>>9.99") + to_string(cl_list.proz2, "->>9.99") + to_string(cl_list.anz, ">>9") + to_string(cl_list.pax, ">>9") + to_string(cl_list.net, "->>>,>>>,>>9.99") + to_string(cl_list.proz, "->>9.99")


    def create_genstat():

        nonlocal output_list_data, i, anz, manz, yanz, pax, mpax, ypax, mnet, ynet, net, t_anz, t_manz, t_yanz, t_pax, t_mpax, t_ypax, t_net, t_mnet, t_ynet, from_bez, to_bez, price_decimal, from_date, zimmer, zinrstat, zimkateg, genstat
        nonlocal m_ftd, m_ytd, f_date, t_date, to_date, rm_no, sorttype, lod__rev


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        mm:int = 0
        yy:int = 0
        datum:date = None
        last_zikatnr:int = 0
        anz = 0
        pax = 0
        net =  to_decimal("0")
        manz = 0
        mpax = 0
        mnet =  to_decimal("0")
        yanz = 0
        ypax = 0
        ynet =  to_decimal("0")
        t_anz = 0
        t_pax = 0
        t_manz = 0
        t_mpax = 0
        t_mnet =  to_decimal("0")
        t_yanz = 0
        t_ypax = 0
        t_ynet =  to_decimal("0")

        if m_ftd :
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
        else:
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
        output_list_data.clear()
        cl_list_data.clear()

        if rm_no != "":

            zimmer = get_cache (Zimmer, {"zinr": [(eq, rm_no)]})

            if zimmer:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.zinr = rm_no
                cl_list.rmcat = zimmer.kbezeich
                for datum in date_range(from_date,to_date) :

                    for genstat in db_session.query(Genstat).filter(
                             (Genstat.zinr == (rm_no).lower()) & (Genstat.datum == datum) & ((Genstat.resstatus == 6) | (Genstat.resstatus == 8))).order_by(Genstat._recid).all():

                        if datum == to_date:
                            cl_list.anz = cl_list.anz + 1
                            cl_list.net =  to_decimal(cl_list.net) + to_decimal(genstat.logis)
                            cl_list.pax = cl_list.pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                            anz = anz + 1
                            pax = pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                            net =  to_decimal(net) + to_decimal(genstat.logis)

                        if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:
                            cl_list.manz = cl_list.manz + 1
                            cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(genstat.logis)
                            cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                            manz = manz + 1
                            mpax = mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                            mnet =  to_decimal(mnet) + to_decimal(genstat.logis)
                        cl_list.yanz = cl_list.yanz + 1
                        cl_list.ypax = cl_list.ypax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                        cl_list.ynet =  to_decimal(cl_list.ynet) + to_decimal(genstat.logis)
                        yanz = yanz + 1
                        ypax = ypax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                        ynet =  to_decimal(ynet) + to_decimal(genstat.logis)
        else:
            rm_no = ""

            if sorttype == 1:

                zimmer_obj_list = {}
                zimmer = Zimmer()
                zimkateg = Zimkateg()
                for zimmer.kbezeich, zimmer.zinr, zimmer.zikatnr, zimmer._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Zimmer.kbezeich, Zimmer.zinr, Zimmer.zikatnr, Zimmer._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).order_by(Zimmer.zinr).all():
                    if zimmer_obj_list.get(zimmer._recid):
                        continue
                    else:
                        zimmer_obj_list[zimmer._recid] = True


                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.zinr = zimmer.zinr
                    cl_list.rmcat = zimkateg.kurzbez
                    for datum in date_range(from_date,to_date) :

                        for genstat in db_session.query(Genstat).filter(
                                 (Genstat.zinr == zimmer.zinr) & (Genstat.datum == datum) & ((Genstat.resstatus == 6) | (Genstat.resstatus == 8))).order_by(Genstat._recid).all():

                            if datum == to_date:
                                cl_list.anz = cl_list.anz + 1
                                cl_list.net =  to_decimal(cl_list.net) + to_decimal(genstat.logis)
                                cl_list.pax = cl_list.pax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                anz = anz + 1
                                pax = pax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                net =  to_decimal(net) + to_decimal(genstat.logis)

                            if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:
                                cl_list.manz = cl_list.manz + 1
                                cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(genstat.logis)
                                cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                manz = manz + 1
                                mpax = mpax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                mnet =  to_decimal(mnet) + to_decimal(genstat.logis)


                            cl_list.yanz = cl_list.yanz + 1
                            cl_list.ypax = cl_list.ypax + genstat.erwachs + genstat.gratis +\
                                    genstat.kind1 + genstat.kind2 + genstat.kind3
                            cl_list.ynet =  to_decimal(cl_list.ynet) + to_decimal(genstat.logis)
                            yanz = yanz + 1
                            ypax = ypax + genstat.erwachs + genstat.gratis +\
                                    genstat.kind1 + genstat.kind2 + genstat.kind3
                            ynet =  to_decimal(ynet) + to_decimal(genstat.logis)


            elif sorttype == 2:

                zimmer_obj_list = {}
                zimmer = Zimmer()
                zimkateg = Zimkateg()
                for zimmer.kbezeich, zimmer.zinr, zimmer.zikatnr, zimmer._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Zimmer.kbezeich, Zimmer.zinr, Zimmer.zikatnr, Zimmer._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).order_by(Zimkateg.zikatnr, Zimmer.zinr).all():
                    if zimmer_obj_list.get(zimmer._recid):
                        continue
                    else:
                        zimmer_obj_list[zimmer._recid] = True

                    if last_zikatnr == 0:
                        last_zikatnr = zimmer.zikatnr

                    if last_zikatnr != zimmer.zikatnr:
                        cl_list = Cl_list()
                        cl_list_data.append(cl_list)

                        cl_list.rmcat = "Total"
                        cl_list.anz = t_anz
                        cl_list.pax = t_pax
                        cl_list.net =  to_decimal(t_net)
                        cl_list.manz = t_manz
                        cl_list.mnet =  to_decimal(t_mnet)
                        cl_list.mpax = t_mpax
                        cl_list.yanz = t_yanz
                        cl_list.ypax = t_ypax
                        cl_list.ynet =  to_decimal(t_ynet)
                        t_anz = 0
                        t_pax = 0
                        t_net =  to_decimal("0")
                        t_manz = 0
                        t_mnet =  to_decimal("0")
                        t_mpax = 0
                        t_yanz = 0
                        t_ynet =  to_decimal("0")
                        t_ypax = 0


                        last_zikatnr = zimmer.zikatnr
                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.zinr = zimmer.zinr
                    cl_list.rmcat = zimkateg.kurzbez
                    for datum in date_range(from_date,to_date) :

                        for genstat in db_session.query(Genstat).filter(
                                 (Genstat.zinr == zimmer.zinr) & (Genstat.datum == datum) & ((Genstat.resstatus == 6) | (Genstat.resstatus == 8))).order_by(Genstat._recid).all():

                            if datum == to_date:
                                cl_list.anz = cl_list.anz + 1
                                cl_list.net =  to_decimal(cl_list.net) + to_decimal(genstat.logis)
                                cl_list.pax = cl_list.pax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                anz = anz + 1
                                pax = pax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                net =  to_decimal(net) + to_decimal(genstat.logis)
                                t_anz = t_anz + 1
                                t_pax = t_pax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                t_net =  to_decimal(t_net) + to_decimal(genstat.logis)

                            if get_month(genstat.datum) == mm:
                                cl_list.manz = cl_list.manz + 1
                                cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(genstat.logis)
                                cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                manz = manz + 1
                                mpax = mpax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                mnet =  to_decimal(mnet) + to_decimal(genstat.logis)
                                t_manz = t_manz + 1
                                t_mpax = t_mpax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                t_mnet =  to_decimal(t_mnet) + to_decimal(genstat.logis)


                            cl_list.yanz = cl_list.yanz + 1
                            cl_list.ypax = cl_list.ypax + genstat.erwachs + genstat.gratis +\
                                    genstat.kind1 + genstat.kind2 + genstat.kind3
                            cl_list.ynet =  to_decimal(cl_list.ynet) + to_decimal(genstat.logis)
                            yanz = yanz + 1
                            ypax = ypax + genstat.erwachs + genstat.gratis +\
                                    genstat.kind1 + genstat.kind2 + genstat.kind3
                            ynet =  to_decimal(ynet) + to_decimal(genstat.logis)
                            t_yanz = t_yanz + 1
                            t_ypax = t_ypax + genstat.erwachs + genstat.gratis +\
                                    genstat.kind1 + genstat.kind2 + genstat.kind3
                            t_ynet =  to_decimal(t_ynet) + to_decimal(genstat.logis)


            if sorttype == 2:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.rmcat = "Total"
                cl_list.anz = t_anz
                cl_list.pax = t_pax
                cl_list.net =  to_decimal(t_net)
                cl_list.manz = t_manz
                cl_list.mnet =  to_decimal(t_mnet)
                cl_list.mpax = t_mpax
                cl_list.yanz = t_yanz
                cl_list.ypax = t_ypax
                cl_list.ynet =  to_decimal(t_ynet)


                t_anz = 0
                t_pax = 0
                t_net =  to_decimal("0")
                t_manz = 0
                t_mnet =  to_decimal("0")
                t_mpax = 0
                t_yanz = 0
                t_ynet =  to_decimal("0")
                t_ypax = 0

        for cl_list in query(cl_list_data):

            if net != 0:
                cl_list.proz =  to_decimal(cl_list.net) / to_decimal(net) * to_decimal("100")

            if mnet != 0:
                cl_list.proz1 =  to_decimal(cl_list.mnet) / to_decimal(mnet) * to_decimal("100")

            if ynet != 0:
                cl_list.proz2 =  to_decimal(cl_list.ynet) / to_decimal(ynet) * to_decimal("100")
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = "*"
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.zinr = ""
        cl_list.rmcat = "GTOTAL"
        cl_list.anz = anz
        cl_list.pax = pax
        cl_list.net =  to_decimal(net)

        if net != 0:
            cl_list.proz1 =  to_decimal("100")
        cl_list.manz = manz
        cl_list.mpax = mpax
        cl_list.mnet =  to_decimal(mnet)

        if mnet != 0:
            cl_list.proz1 =  to_decimal("100")
        cl_list.yanz = yanz
        cl_list.ypax = ypax
        cl_list.ynet =  to_decimal(ynet)

        if ynet != 0:
            cl_list.proz2 =  to_decimal("100")

        for cl_list in query(cl_list_data):
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = cl_list.flag
            output_list.rmno = cl_list.zinr

            if cl_list.flag.lower()  == ("*").lower() :
                output_list.str = fill("-", 115)
            else:

                if price_decimal == 0:
                    output_list.str = to_string(cl_list.zinr, "x(6)") + to_string(cl_list.rmcat, "x(6)") + to_string(cl_list.manz, ">>,>>9") + to_string(cl_list.mpax, ">>,>>9") + to_string(cl_list.mnet, "->,>>>,>>>,>>>,>>9") + to_string(cl_list.proz1, "->>9.99") + to_string(cl_list.yanz, ">>>,>>9") + to_string(cl_list.ypax, ">>>,>>9") + to_string(cl_list.ynet, "->,>>>,>>>,>>>,>>9") + to_string(cl_list.proz2, "->>9.99") + to_string(cl_list.anz, ">>9") + to_string(cl_list.pax, ">>9") + to_string(cl_list.net, "->>,>>>,>>>,>>9") + to_string(cl_list.proz, "->>9.99")
                else:
                    output_list.str = to_string(cl_list.zinr, "x(6)") + to_string(cl_list.rmcat, "x(6)") + to_string(cl_list.manz, ">>,>>9") + to_string(cl_list.mpax, ">>,>>9") + to_string(cl_list.mnet, "->>,>>>,>>>,>>9.99") + to_string(cl_list.proz1, "->>9.99") + to_string(cl_list.yanz, ">>>,>>9") + to_string(cl_list.ypax, ">>>,>>9") + to_string(cl_list.ynet, "->>,>>>,>>>,>>9.99") + to_string(cl_list.proz2, "->>9.99") + to_string(cl_list.anz, ">>9") + to_string(cl_list.pax, ">>9") + to_string(cl_list.net, "->>>,>>>,>>9.99") + to_string(cl_list.proz, "->>9.99")

    if lod__rev :
        create_genstat()
    else:
        create_zinrstat()

    return generate_output()