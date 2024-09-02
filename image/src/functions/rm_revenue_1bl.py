from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Zimmer, Zinrstat, Zimkateg, Genstat

def rm_revenue_1bl(m_ftd:bool, m_ytd:bool, f_date:date, t_date:date, to_date:date, rm_no:str, sorttype:int, lod__rev:bool):
    output_list_list = []
    i:int = 0
    anz:int = 0
    manz:int = 0
    yanz:int = 0
    pax:int = 0
    mpax:int = 0
    ypax:int = 0
    mnet:decimal = 0
    ynet:decimal = 0
    net:decimal = 0
    t_anz:int = 0
    t_manz:int = 0
    t_yanz:int = 0
    t_pax:int = 0
    t_mpax:int = 0
    t_ypax:int = 0
    t_net:decimal = 0
    t_mnet:decimal = 0
    t_ynet:decimal = 0
    from_bez:str = ""
    to_bez:str = ""
    price_decimal:int = 0
    from_date:date = None
    zimmer = zinrstat = zimkateg = genstat = None

    output_list = cl_list = None

    output_list_list, Output_list = create_model("Output_list", {"rmno":str, "flag":str, "str":str})
    cl_list_list, Cl_list = create_model("Cl_list", {"flag":str, "zinr":str, "rmcat":str, "anz":int, "pax":int, "net":decimal, "proz":decimal, "manz":int, "mpax":int, "mnet":decimal, "proz1":decimal, "yanz":int, "ypax":int, "ynet":decimal, "proz2":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, i, anz, manz, yanz, pax, mpax, ypax, mnet, ynet, net, t_anz, t_manz, t_yanz, t_pax, t_mpax, t_ypax, t_net, t_mnet, t_ynet, from_bez, to_bez, price_decimal, from_date, zimmer, zinrstat, zimkateg, genstat


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list
        return {"output-list": output_list_list}

    def create_zinrstat():

        nonlocal output_list_list, i, anz, manz, yanz, pax, mpax, ypax, mnet, ynet, net, t_anz, t_manz, t_yanz, t_pax, t_mpax, t_ypax, t_net, t_mnet, t_ynet, from_bez, to_bez, price_decimal, from_date, zimmer, zinrstat, zimkateg, genstat


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        mm:int = 0
        yy:int = 0
        datum:date = None
        last_zikatnr:int = 0
        anz = 0
        pax = 0
        net = 0
        manz = 0
        mpax = 0
        mnet = 0
        yanz = 0
        ypax = 0
        ynet = 0
        t_anz = 0
        t_pax = 0
        t_manz = 0
        t_mpax = 0
        t_mnet = 0
        t_yanz = 0
        t_ypax = 0
        t_ynet = 0

        if m_ftd  and m_ytd == False:
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)

        elif m_ftd == False and m_ytd :
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
        output_list_list.clear()
        cl_list_list.clear()

        if rm_no != "":

            zimmer = db_session.query(Zimmer).filter(
                    (func.lower(Zimmer.zinr) == (rm_no).lower())).first()

            if zimmer:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.zinr = rm_no
                cl_list.rmcat = zimmer.kbezeich
                for datum in range(from_date,to_date + 1) :

                    zinrstat = db_session.query(Zinrstat).filter(
                            (func.lower(Zinrstat.zinr) == (rm_no).lower()) &  (Zinrstat.datum == datum) &  (Zinrstat.zimmeranz > 0)).first()

                    if zinrstat:

                        if datum == to_date:
                            cl_list.anz = cl_list.anz + zinrstat.zimmeranz
                            cl_list.net = cl_list.net + zinrstat.argtumsatz
                            cl_list.pax = cl_list.pax + zinrstat.person
                            anz = anz + zinrstat.zimmeranz
                            pax = pax + zinrstat.person
                            net = net + zinrstat.argtumsatz

                        if get_month(zinrstat.datum) == mm and get_year(zinrstat.datum) == yy:
                            cl_list.manz = cl_list.manz + zinrstat.zimmeranz
                            cl_list.mnet = cl_list.mnet + zinrstat.argtumsatz
                            cl_list.mpax = cl_list.mpax + zinrstat.person
                            manz = manz + zinrstat.zimmeranz
                            mpax = mpax + zinrstat.person
                            mnet = mnet + zinrstat.argtumsatz
                        cl_list.yanz = cl_list.yanz + zinrstat.zimmeranz
                        cl_list.ypax = cl_list.ypax + zinrstat.person
                        cl_list.ynet = cl_list.ynet + zinrstat.argtumsatz
                        yanz = yanz + zinrstat.zimmeranz
                        ypax = ypax + zinrstat.person
                        ynet = ynet + zinrstat.argtumsatz
        else:
            rm_no = ""

            if sorttype == 1:

                zimmer_obj_list = []
                for zimmer, zimkateg in db_session.query(Zimmer, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).all():
                    if zimmer._recid in zimmer_obj_list:
                        continue
                    else:
                        zimmer_obj_list.append(zimmer._recid)


                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.zinr = zimmer.zinr
                    cl_list.rmcat = zimkateg.kurzbez
                    for datum in range(from_date,to_date + 1) :

                        zinrstat = db_session.query(Zinrstat).filter(
                                (Zinrstat.zinr == zimmer.zinr) &  (Zinrstat.datum == datum) &  (Zinrstat.zimmeranz > 0)).first()

                        if zinrstat:

                            if datum == to_date:
                                cl_list.anz = cl_list.anz + zinrstat.zimmeranz
                                cl_list.net = cl_list.net + zinrstat.argtumsatz
                                cl_list.pax = cl_list.pax + zinrstat.person
                                anz = anz + zinrstat.zimmeranz
                                pax = pax + zinrstat.person
                                net = net + zinrstat.argtumsatz

                            if get_month(zinrstat.datum) == mm and get_year(zinrstat.datum) == yy:
                                cl_list.manz = cl_list.manz + zinrstat.zimmeranz
                                cl_list.mnet = cl_list.mnet + zinrstat.argtumsatz
                                cl_list.mpax = cl_list.mpax + zinrstat.person
                                manz = manz + zinrstat.zimmeranz
                                mpax = mpax + zinrstat.person
                                mnet = mnet + zinrstat.argtumsatz
                            cl_list.yanz = cl_list.yanz + zinrstat.zimmeranz
                            cl_list.ypax = cl_list.ypax + zinrstat.person
                            cl_list.ynet = cl_list.ynet + zinrstat.argtumsatz
                            yanz = yanz + zinrstat.zimmeranz
                            ypax = ypax + zinrstat.person
                            ynet = ynet + zinrstat.argtumsatz


            elif sorttype == 2:

                zimmer_obj_list = []
                for zimmer, zimkateg in db_session.query(Zimmer, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).all():
                    if zimmer._recid in zimmer_obj_list:
                        continue
                    else:
                        zimmer_obj_list.append(zimmer._recid)

                    if last_zikatnr == 0:
                        last_zikatnr = zimmer.zikatnr

                    if last_zikatnr != zimmer.zikatnr:
                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        cl_list.rmcat = "Total"
                        cl_list.anz = t_anz
                        cl_list.pax = t_pax
                        cl_list.net = t_net
                        cl_list.manz = t_manz
                        cl_list.mnet = t_mnet
                        cl_list.mpax = t_mpax
                        cl_list.yanz = t_yanz
                        cl_list.ypax = t_ypax
                        cl_list.ynet = t_ynet
                        t_anz = 0
                        t_pax = 0
                        t_net = 0
                        t_manz = 0
                        t_mnet = 0
                        t_mpax = 0
                        t_yanz = 0
                        t_ynet = 0
                        t_ypax = 0


                        last_zikatnr = zimmer.zikatnr
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.zinr = zimmer.zinr
                    cl_list.rmcat = zimkateg.kurzbez
                    for datum in range(from_date,to_date + 1) :

                        zinrstat = db_session.query(Zinrstat).filter(
                                (Zinrstat.zinr == zimmer.zinr) &  (Zinrstat.datum == datum) &  (Zinrstat.zimmeranz > 0)).first()

                        if zinrstat:

                            if datum == to_date:
                                cl_list.anz = cl_list.anz + zinrstat.zimmeranz
                                cl_list.net = cl_list.net + zinrstat.argtumsatz
                                cl_list.pax = cl_list.pax + zinrstat.person
                                anz = anz + zinrstat.zimmeranz
                                pax = pax + zinrstat.person
                                net = net + zinrstat.argtumsatz
                                t_anz = t_anz + zinrstat.zimmeranz
                                t_pax = t_pax + zinrstat.person
                                t_net = t_net + zinrstat.argtumsatz

                            if get_month(zinrstat.datum) == mm:
                                cl_list.manz = cl_list.manz + zinrstat.zimmeranz
                                cl_list.mnet = cl_list.mnet + zinrstat.argtumsatz
                                cl_list.mpax = cl_list.mpax + zinrstat.person
                                manz = manz + zinrstat.zimmeranz
                                mpax = mpax + zinrstat.person
                                mnet = mnet + zinrstat.argtumsatz
                                t_manz = t_manz + zinrstat.zimmeranz
                                t_mpax = t_mpax + zinrstat.person
                                t_mnet = t_mnet + zinrstat.argtumsatz
                            cl_list.yanz = cl_list.yanz + zinrstat.zimmeranz
                            cl_list.ypax = cl_list.ypax + zinrstat.person
                            cl_list.ynet = cl_list.ynet + zinrstat.argtumsatz
                            yanz = yanz + zinrstat.zimmeranz
                            ypax = ypax + zinrstat.person
                            ynet = ynet + zinrstat.argtumsatz
                            t_yanz = t_yanz + zinrstat.zimmeranz
                            t_ypax = t_ypax + zinrstat.person
                            t_ynet = t_ynet + zinrstat.argtumsatz


            if sorttype == 2:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.rmcat = "Total"
                cl_list.anz = t_anz
                cl_list.pax = t_pax
                cl_list.net = t_net
                cl_list.manz = t_manz
                cl_list.mnet = t_mnet
                cl_list.mpax = t_mpax
                cl_list.yanz = t_yanz
                cl_list.ypax = t_ypax
                cl_list.ynet = t_ynet


                t_anz = 0
                t_pax = 0
                t_net = 0
                t_manz = 0
                t_mnet = 0
                t_mpax = 0
                t_yanz = 0
                t_ynet = 0
                t_ypax = 0

        for cl_list in query(cl_list_list):

            if net != 0:
                cl_list.proz = cl_list.net / net * 100

            if mnet != 0:
                cl_list.proz1 = cl_list.mnet / mnet * 100

            if ynet != 0:
                cl_list.proz2 = cl_list.ynet / ynet * 100
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = "*"
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.zinr = ""
        cl_list.rmcat = "GTOTAL"
        cl_list.anz = anz
        cl_list.pax = pax
        cl_list.net = net

        if net != 0:
            cl_list.proz1 = 100
        cl_list.manz = manz
        cl_list.mpax = mpax
        cl_list.mnet = mnet

        if mnet != 0:
            cl_list.proz1 = 100
        cl_list.yanz = yanz
        cl_list.ypax = ypax
        cl_list.ynet = ynet

        if ynet != 0:
            cl_list.proz2 = 100

        for cl_list in query(cl_list_list):
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = cl_list.flag
            output_list.rmNo = cl_list.zinr

            if cl_list.flag.lower()  == "*":
                output_list.str = fill("-", 115)
            else:

                if price_decimal == 0:
                    output_list.str = to_string(cl_list.zinr, "x(6)") + to_string(cl_list.rmcat, "x(6)") + to_string(cl_list.manz, ">>,>>9") + to_string(cl_list.mpax, ">>,>>9") + to_string(cl_list.mnet, "->,>>>,>>>,>>>,>>9") + to_string(cl_list.proz1, "->>9.99") + to_string(cl_list.yanz, ">>>,>>9") + to_string(cl_list.ypax, ">>>,>>9") + to_string(cl_list.ynet, "->,>>>,>>>,>>>,>>9") + to_string(cl_list.proz2, "->>9.99") + to_string(cl_list.anz, ">>9") + to_string(cl_list.pax, ">>9") + to_string(cl_list.net, "->>,>>>,>>>,>>9") + to_string(cl_list.proz, "->>9.99")
                else:
                    output_list.str = to_string(cl_list.zinr, "x(6)") + to_string(cl_list.rmcat, "x(6)") + to_string(cl_list.manz, ">>,>>9") + to_string(cl_list.mpax, ">>,>>9") + to_string(cl_list.mnet, "->>,>>>,>>>,>>9.99") + to_string(cl_list.proz1, "->>9.99") + to_string(cl_list.yanz, ">>>,>>9") + to_string(cl_list.ypax, ">>>,>>9") + to_string(cl_list.ynet, "->>,>>>,>>>,>>9.99") + to_string(cl_list.proz2, "->>9.99") + to_string(cl_list.anz, ">>9") + to_string(cl_list.pax, ">>9") + to_string(cl_list.net, "->>>,>>>,>>9.99") + to_string(cl_list.proz, "->>9.99")

    def create_genstat():

        nonlocal output_list_list, i, anz, manz, yanz, pax, mpax, ypax, mnet, ynet, net, t_anz, t_manz, t_yanz, t_pax, t_mpax, t_ypax, t_net, t_mnet, t_ynet, from_bez, to_bez, price_decimal, from_date, zimmer, zinrstat, zimkateg, genstat


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        mm:int = 0
        yy:int = 0
        datum:date = None
        last_zikatnr:int = 0
        anz = 0
        pax = 0
        net = 0
        manz = 0
        mpax = 0
        mnet = 0
        yanz = 0
        ypax = 0
        ynet = 0
        t_anz = 0
        t_pax = 0
        t_manz = 0
        t_mpax = 0
        t_mnet = 0
        t_yanz = 0
        t_ypax = 0
        t_ynet = 0

        if m_ftd :
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
        else:
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
        output_list_list.clear()
        cl_list_list.clear()

        if rm_no != "":

            zimmer = db_session.query(Zimmer).filter(
                    (func.lower(Zimmer.zinr) == (rm_no).lower())).first()

            if zimmer:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.zinr = rm_no
                cl_list.rmcat = zimmer.kbezeich
                for datum in range(from_date,to_date + 1) :

                    for genstat in db_session.query(Genstat).filter(
                            (func.lower(Genstat.zinr) == (rm_no).lower()) &  (Genstat.datum == datum) &  ((Genstat.resstatus == 6) |  (Genstat.resstatus == 8))).all():

                        if datum == to_date:
                            cl_list.anz = cl_list.anz + 1
                            cl_list.net = cl_list.net + genstat.logis
                            cl_list.pax = cl_list.pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                            anz = anz + 1
                            pax = pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                            net = net + genstat.logis

                        if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:
                            cl_list.manz = cl_list.manz + 1
                            cl_list.mnet = cl_list.mnet + genstat.logis
                            cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                            manz = manz + 1
                            mpax = mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                            mnet = mnet + genstat.logis
                        cl_list.yanz = cl_list.yanz + 1
                        cl_list.ypax = cl_list.ypax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                        cl_list.ynet = cl_list.ynet + genstat.logis
                        yanz = yanz + 1
                        ypax = ypax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                        ynet = ynet + genstat.logis
        else:
            rm_no = ""

            if sorttype == 1:

                zimmer_obj_list = []
                for zimmer, zimkateg in db_session.query(Zimmer, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).all():
                    if zimmer._recid in zimmer_obj_list:
                        continue
                    else:
                        zimmer_obj_list.append(zimmer._recid)


                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.zinr = zimmer.zinr
                    cl_list.rmcat = zimkateg.kurzbez
                    for datum in range(from_date,to_date + 1) :

                        for genstat in db_session.query(Genstat).filter(
                                (Genstat.zinr == zimmer.zinr) &  (Genstat.datum == datum) &  ((Genstat.resstatus == 6) |  (Genstat.resstatus == 8))).all():

                            if datum == to_date:
                                cl_list.anz = cl_list.anz + 1
                                cl_list.net = cl_list.net + genstat.logis
                                cl_list.pax = cl_list.pax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                anz = anz + 1
                                pax = pax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                net = net + genstat.logis

                            if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:
                                cl_list.manz = cl_list.manz + 1
                                cl_list.mnet = cl_list.mnet + genstat.logis
                                cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                manz = manz + 1
                                mpax = mpax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                mnet = mnet + genstat.logis


                            cl_list.yanz = cl_list.yanz + 1
                            cl_list.ypax = cl_list.ypax + genstat.erwachs + genstat.gratis +\
                                    genstat.kind1 + genstat.kind2 + genstat.kind3
                            cl_list.ynet = cl_list.ynet + genstat.logis
                            yanz = yanz + 1
                            ypax = ypax + genstat.erwachs + genstat.gratis +\
                                    genstat.kind1 + genstat.kind2 + genstat.kind3
                            ynet = ynet + genstat.logis


            elif sorttype == 2:

                zimmer_obj_list = []
                for zimmer, zimkateg in db_session.query(Zimmer, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).all():
                    if zimmer._recid in zimmer_obj_list:
                        continue
                    else:
                        zimmer_obj_list.append(zimmer._recid)

                    if last_zikatnr == 0:
                        last_zikatnr = zimmer.zikatnr

                    if last_zikatnr != zimmer.zikatnr:
                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        cl_list.rmcat = "Total"
                        cl_list.anz = t_anz
                        cl_list.pax = t_pax
                        cl_list.net = t_net
                        cl_list.manz = t_manz
                        cl_list.mnet = t_mnet
                        cl_list.mpax = t_mpax
                        cl_list.yanz = t_yanz
                        cl_list.ypax = t_ypax
                        cl_list.ynet = t_ynet
                        t_anz = 0
                        t_pax = 0
                        t_net = 0
                        t_manz = 0
                        t_mnet = 0
                        t_mpax = 0
                        t_yanz = 0
                        t_ynet = 0
                        t_ypax = 0


                        last_zikatnr = zimmer.zikatnr
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.zinr = zimmer.zinr
                    cl_list.rmcat = zimkateg.kurzbez
                    for datum in range(from_date,to_date + 1) :

                        for genstat in db_session.query(Genstat).filter(
                                (Genstat.zinr == zimmer.zinr) &  (Genstat.datum == datum) &  ((Genstat.resstatus == 6) |  (Genstat.resstatus == 8))).all():

                            if datum == to_date:
                                cl_list.anz = cl_list.anz + 1
                                cl_list.net = cl_list.net + genstat.logis
                                cl_list.pax = cl_list.pax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                anz = anz + 1
                                pax = pax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                net = net + genstat.logis
                                t_anz = t_anz + 1
                                t_pax = t_pax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                t_net = t_net + genstat.logis

                            if get_month(genstat.datum) == mm:
                                cl_list.manz = cl_list.manz + 1
                                cl_list.mnet = cl_list.mnet + genstat.logis
                                cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                manz = manz + 1
                                mpax = mpax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                mnet = mnet + genstat.logis
                                t_manz = t_manz + 1
                                t_mpax = t_mpax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                t_mnet = t_mnet + genstat.logis


                            cl_list.yanz = cl_list.yanz + 1
                            cl_list.ypax = cl_list.ypax + genstat.erwachs + genstat.gratis +\
                                    genstat.kind1 + genstat.kind2 + genstat.kind3
                            cl_list.ynet = cl_list.ynet + genstat.logis
                            yanz = yanz + 1
                            ypax = ypax + genstat.erwachs + genstat.gratis +\
                                    genstat.kind1 + genstat.kind2 + genstat.kind3
                            ynet = ynet + genstat.logis
                            t_yanz = t_yanz + 1
                            t_ypax = t_ypax + genstat.erwachs + genstat.gratis +\
                                    genstat.kind1 + genstat.kind2 + genstat.kind3
                            t_ynet = t_ynet + genstat.logis


            if sorttype == 2:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.rmcat = "Total"
                cl_list.anz = t_anz
                cl_list.pax = t_pax
                cl_list.net = t_net
                cl_list.manz = t_manz
                cl_list.mnet = t_mnet
                cl_list.mpax = t_mpax
                cl_list.yanz = t_yanz
                cl_list.ypax = t_ypax
                cl_list.ynet = t_ynet


                t_anz = 0
                t_pax = 0
                t_net = 0
                t_manz = 0
                t_mnet = 0
                t_mpax = 0
                t_yanz = 0
                t_ynet = 0
                t_ypax = 0

        for cl_list in query(cl_list_list):

            if net != 0:
                cl_list.proz = cl_list.net / net * 100

            if mnet != 0:
                cl_list.proz1 = cl_list.mnet / mnet * 100

            if ynet != 0:
                cl_list.proz2 = cl_list.ynet / ynet * 100
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = "*"
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.zinr = ""
        cl_list.rmcat = "GTOTAL"
        cl_list.anz = anz
        cl_list.pax = pax
        cl_list.net = net

        if net != 0:
            cl_list.proz1 = 100
        cl_list.manz = manz
        cl_list.mpax = mpax
        cl_list.mnet = mnet

        if mnet != 0:
            cl_list.proz1 = 100
        cl_list.yanz = yanz
        cl_list.ypax = ypax
        cl_list.ynet = ynet

        if ynet != 0:
            cl_list.proz2 = 100

        for cl_list in query(cl_list_list):
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = cl_list.flag
            output_list.rmNo = cl_list.zinr

            if cl_list.flag.lower()  == "*":
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