from functions.additional_functions import *
import decimal
from datetime import date
from models import Fbstat, Hoteldpt

def fb_statistic_create_list_webbl(pvilanguage:int, fdept:int, tdept:int, fdate:date, tdate:date, price_decimal:int):
    cl_list_list = []
    tgrev:decimal = 0
    twrev:decimal = 0
    tgpax:int = 0
    tgcost:decimal = 0
    twpax:int = 0
    twcost:decimal = 0
    ttotpax:int = 0
    ttotrev:decimal = 0
    ttotcost:decimal = 0
    tot_gpax:int = 0
    tot_grev:decimal = 0
    tot_gcost:decimal = 0
    tot_wpax:int = 0
    tot_wrev:decimal = 0
    tot_wcost:decimal = 0
    tot_tpax:int = 0
    tot_trev:decimal = 0
    tot_tcost:decimal = 0
    fbstat = hoteldpt = None

    cl_list = stat = None

    cl_list_list, Cl_list = create_model("Cl_list", {"dept":int, "deptname":str, "typ":int, "descrip":str, "grev":decimal, "gpax":int, "gproz":decimal, "gcost":decimal, "gavg":decimal, "wrev":decimal, "wpax":int, "wproz":decimal, "wcost":decimal, "wavg":decimal, "totpax":int, "totrev":decimal, "totcost":decimal})

    Stat = Fbstat

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cl_list_list, tgrev, twrev, tgpax, tgcost, twpax, twcost, ttotpax, ttotrev, ttotcost, tot_gpax, tot_grev, tot_gcost, tot_wpax, tot_wrev, tot_wcost, tot_tpax, tot_trev, tot_tcost, fbstat, hoteldpt
        nonlocal stat


        nonlocal cl_list, stat
        nonlocal cl_list_list
        return {"cl-list": cl_list_list}

    def create_list():

        nonlocal cl_list_list, tgrev, twrev, tgpax, tgcost, twpax, twcost, ttotpax, ttotrev, ttotcost, tot_gpax, tot_grev, tot_gcost, tot_wpax, tot_wrev, tot_wcost, tot_tpax, tot_trev, tot_tcost, fbstat, hoteldpt
        nonlocal stat


        nonlocal cl_list, stat
        nonlocal cl_list_list


        Stat = Fbstat
        cl_list_list.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num > 0) &  (Hoteldpt.num >= fdept) &  (Hoteldpt.num <= tdept)).all():
            tot_gpax = 0
            tot_grev = 0
            tot_gcost = 0
            tot_wpax = 0
            tot_wrev = 0
            tot_wcost = 0
            tot_tpax = 0
            tot_trev = 0
            tot_tcost = 0

            stat = db_session.query(Stat).filter(
                    (Stat.departement == hoteldpt.num) &  (Stat.datum >= fdate) &  (Stat.datum <= tdate)).first()

            if stat:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.descrip = to_string(hoteldpt.num) + " - " +\
                        hoteldpt.depart


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.TYP = 1
                cl_list.descrip = "Breakfast"


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.TYP = 1
                cl_list.descrip = "Lunch"


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.TYP = 1
                cl_list.descrip = "Dinner"


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.TYP = 1
                cl_list.descrip = "Supper"


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.descrip = "-----"
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.descrip = "FOOD TOTAL"
                cl_list.dept = hoteldpt.num
                cl_list.typ = 1


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.typ = 2
                cl_list.descrip = "Breakfast"


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.typ = 2
                cl_list.descrip = "Lunch"


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.typ = 2
                cl_list.descrip = "Dinner"


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.typ = 2
                cl_list.descrip = "Supper"


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.descrip = "-----"
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.descrip = "BEV TOTAL"
                cl_list.dept = hoteldpt.num
                cl_list.typ = 2


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.typ = 3
                cl_list.descrip = "Breakfast"


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.typ = 3
                cl_list.descrip = "Lunch"


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.typ = 3
                cl_list.descrip = "Dinner"


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.typ = 3
                cl_list.descrip = "Supper"


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.descrip = "-----"
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.descrip = "OTHER TOTAL"
                cl_list.dept = hoteldpt.num
                cl_list.typ = 3


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.descrip = "TOTAL"
                cl_list.dept = hoteldpt.num
                cl_list.typ = 4


                cl_list = Cl_list()
                cl_list_list.append(cl_list)


            for fbstat in db_session.query(Fbstat).filter(
                    (Fbstat.datum >= fdate) &  (Fbstat.datum <= tdate) &  (Fbstat.departement == hoteldpt.num)).all():

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.typ == 1 and cl_list.descrip.lower()  == "Breakfast"), first=True)

                if cl_list:
                    cl_list.grev = cl_list.grev + fbstat.food_grev[0]
                    cl_list.gpax = cl_list.gpax + fbstat.food_gpax[0]
                    cl_list.gcost = cl_list.gcost + fbstat.food_gcost[0]
                    cl_list.wrev = cl_list.wrev + fbstat.food_wrev[0]
                    cl_list.wpax = cl_list.wpax + fbstat.food_wpax[0]
                    cl_list.wcost = cl_list.wcost + fbstat.food_wcost[0]
                    cl_list.totrev = cl_list.totrev + fbstat.food_grev[0] + fbstat.food_wrev[0]
                    cl_list.totpax = cl_list.totpax + fbstat.food_gpax[0] + fbstat.food_wpax[0]
                    cl_list.totcost = cl_list.totcost + fbstat.food_gcost[0] + fbstat.food_wcost[0]

                    if cl_list.grev != 0 and cl_list.gpax != 0:
                        cl_list.gavg = cl_list.grev / cl_list.gpax

                    if cl_list.wrev != 0 and cl_list.wpax != 0:
                        cl_list.wavg = cl_list.wrev / cl_list.wpax

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.typ == 1 and cl_list.descrip.lower()  == "Lunch"), first=True)

                if cl_list:
                    cl_list.grev = cl_list.grev + fbstat.food_grev[1]
                    cl_list.gpax = cl_list.gpax + fbstat.food_gpax[1]
                    cl_list.gcost = cl_list.gcost + fbstat.food_gcost[1]
                    cl_list.wrev = cl_list.wrev + fbstat.food_wrev[1]
                    cl_list.wpax = cl_list.wpax + fbstat.food_wpax[1]
                    cl_list.wcost = cl_list.wcost + fbstat.food_wcost[1]
                    cl_list.totrev = cl_list.totrev + fbstat.food_grev[1] + fbstat.food_wrev[1]
                    cl_list.totpax = cl_list.totpax + fbstat.food_gpax[1] + fbstat.food_wpax[1]
                    cl_list.totcost = cl_list.totcost + fbstat.food_gcost[1] + fbstat.food_wcost[1]

                    if cl_list.grev != 0 and cl_list.gpax != 0:
                        cl_list.gavg = cl_list.grev / cl_list.gpax

                    if cl_list.wrev != 0 and cl_list.wpax != 0:
                        cl_list.wavg = cl_list.wrev / cl_list.wpax

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.typ == 1 and cl_list.descrip.lower()  == "Dinner"), first=True)

                if cl_list:
                    cl_list.grev = cl_list.grev + fbstat.food_grev[2]
                    cl_list.gpax = cl_list.gpax + fbstat.food_gpax[2]
                    cl_list.gcost = cl_list.gcost + fbstat.food_gcost[2]
                    cl_list.wrev = cl_list.wrev + fbstat.food_wrev[2]
                    cl_list.wpax = cl_list.wpax + fbstat.food_wpax[2]
                    cl_list.wcost = cl_list.wcost + fbstat.food_wcost[2]
                    cl_list.totrev = cl_list.totrev + fbstat.food_grev[2] + fbstat.food_wrev[2]
                    cl_list.totpax = cl_list.totpax + fbstat.food_gpax[2] + fbstat.food_wpax[2]
                    cl_list.totcost = cl_list.totcost + fbstat.food_gcost[2] + fbstat.food_wcost[2]

                    if cl_list.grev != 0 and cl_list.gpax != 0:
                        cl_list.gavg = cl_list.grev / cl_list.gpax

                    if cl_list.wrev != 0 and cl_list.wpax != 0:
                        cl_list.wavg = cl_list.wrev / cl_list.wpax

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.typ == 1 and cl_list.descrip.lower()  == "Supper"), first=True)

                if cl_list:
                    cl_list.grev = cl_list.grev + fbstat.food_grev[3]
                    cl_list.gpax = cl_list.gpax + fbstat.food_gpax[3]
                    cl_list.gcost = cl_list.gcost + fbstat.food_gcost[3]
                    cl_list.wrev = cl_list.wrev + fbstat.food_wrev[3]
                    cl_list.wpax = cl_list.wpax + fbstat.food_wpax[3]
                    cl_list.wcost = cl_list.wcost + fbstat.food_wcost[3]
                    cl_list.totrev = cl_list.totrev + fbstat.food_grev[3] + fbstat.food_wrev[3]
                    cl_list.totpax = cl_list.totpax + fbstat.food_gpax[3] + fbstat.food_wpax[3]
                    cl_list.totcost = cl_list.totcost + fbstat.food_gcost[3] + fbstat.food_wcost[3]

                    if cl_list.grev != 0 and cl_list.gpax != 0:
                        cl_list.gavg = cl_list.grev / cl_list.gpax

                    if cl_list.wavg != 0 and cl_list.wpax != 0:
                        cl_list.wrev = cl_list.wrev / cl_list.wpax

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.typ == 2 and cl_list.descrip.lower()  == "Breakfast"), first=True)

                if cl_list:
                    cl_list.grev = cl_list.grev + fbstat.bev_grev[0]
                    cl_list.gpax = cl_list.gpax + fbstat.bev_gpax[0]
                    cl_list.gcost = cl_list.gcost + fbstat.bev_gcost[0]
                    cl_list.wrev = cl_list.wrev + fbstat.bev_wrev[0]
                    cl_list.wpax = cl_list.wpax + fbstat.bev_wpax[0]
                    cl_list.wcost = cl_list.wcost + fbstat.bev_wcost[0]
                    cl_list.totrev = cl_list.totrev + fbstat.bev_grev[0] + fbstat.bev_wrev[0]
                    cl_list.totpax = cl_list.totpax + fbstat.bev_gpax[0] + fbstat.bev_wpax[0]
                    cl_list.totcost = cl_list.totcost + fbstat.bev_gcost[0] + fbstat.bev_wcost[0]

                    if cl_list.grev != 0 and cl_list.gpax != 0:
                        cl_list.gavg = cl_list.grev / cl_list.gpax

                    if cl_list.wrev != 0 and cl_list.wpax != 0:
                        cl_list.wavg = cl_list.wrev / cl_list.wpax

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.typ == 2 and cl_list.descrip.lower()  == "Lunch"), first=True)

                if cl_list:
                    cl_list.grev = cl_list.grev + fbstat.bev_grev[1]
                    cl_list.gpax = cl_list.gpax + fbstat.bev_gpax[1]
                    cl_list.gcost = cl_list.gcost + fbstat.bev_gcost[1]
                    cl_list.wrev = cl_list.wrev + fbstat.bev_wrev[1]
                    cl_list.wpax = cl_list.wpax + fbstat.bev_wpax[1]
                    cl_list.wcost = cl_list.wcost + fbstat.bev_wcost[1]
                    cl_list.totrev = cl_list.totrev + fbstat.bev_grev[1] + fbstat.bev_wrev[1]
                    cl_list.totpax = cl_list.totpax + fbstat.bev_gpax[1] + fbstat.bev_wpax[1]
                    cl_list.totcost = cl_list.totcost + fbstat.bev_gcost[1] + fbstat.bev_wcost[1]

                    if cl_list.grev != 0 and cl_list.gpax != 0:
                        cl_list.gavg = cl_list.grev / cl_list.gpax

                    if cl_list.wrev != 0 and cl_list.wpax != 0:
                        cl_list.wavg = cl_list.wrev / cl_list.wpax

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.typ == 2 and cl_list.descrip.lower()  == "Dinner"), first=True)

                if cl_list:
                    cl_list.grev = cl_list.grev + fbstat.bev_grev[2]
                    cl_list.gpax = cl_list.gpax + fbstat.bev_gpax[2]
                    cl_list.gcost = cl_list.gcost + fbstat.bev_gcost[2]
                    cl_list.wrev = cl_list.wrev + fbstat.bev_wrev[2]
                    cl_list.wpax = cl_list.wpax + fbstat.bev_wpax[2]
                    cl_list.wcost = cl_list.wcost + fbstat.bev_wcost[2]
                    cl_list.totrev = cl_list.totrev + fbstat.bev_grev[2] + fbstat.bev_wrev[2]
                    cl_list.totpax = cl_list.totpax + fbstat.bev_gpax[2] + fbstat.bev_wpax[2]
                    cl_list.totcost = cl_list.totcost + fbstat.bev_gcost[2] + fbstat.bev_wcost[2]

                    if cl_list.grev != 0 and cl_list.gpax != 0:
                        cl_list.gavg = cl_list.grev / cl_list.gpax

                    if cl_list.wrev != 0 and cl_list.wpax != 0:
                        cl_list.wavg = cl_list.wrev / cl_list.wpax

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.typ == 2 and cl_list.descrip.lower()  == "Supper"), first=True)

                if cl_list:
                    cl_list.grev = cl_list.grev + fbstat.bev_grev[3]
                    cl_list.gpax = cl_list.gpax + fbstat.bev_gpax[3]
                    cl_list.gcost = cl_list.gcost + fbstat.bev_gcost[3]
                    cl_list.wrev = cl_list.wrev + fbstat.bev_wrev[3]
                    cl_list.wpax = cl_list.wpax + fbstat.bev_wpax[3]
                    cl_list.wcost = cl_list.wcost + fbstat.bev_wcost[3]
                    cl_list.totrev = cl_list.totrev + fbstat.bev_grev[3] + fbstat.bev_wrev[3]
                    cl_list.totpax = cl_list.totpax + fbstat.bev_gpax[3] + fbstat.bev_wpax[3]
                    cl_list.totcost = cl_list.totcost + fbstat.bev_gcost[3] + fbstat.bev_wcost[3]

                    if cl_list.grev != 0 and cl_list.gpax != 0:
                        cl_list.gavg = cl_list.grev / cl_list.gpax

                    if cl_list.wrev != 0 and cl_list.wpax != 0:
                        cl_list.wavg = cl_list.wrev / cl_list.wpax

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.typ == 3 and cl_list.descrip.lower()  == "Breakfast"), first=True)
                cl_list.grev = cl_list.grev + fbstat.other_grev[0]
                cl_list.gpax = cl_list.gpax + fbstat.other_gpax[0]
                cl_list.gcost = cl_list.gcost + fbstat.other_gcost[0]
                cl_list.wrev = cl_list.wrev + fbstat.other_wrev[0]
                cl_list.wpax = cl_list.wpax + fbstat.other_wpax[0]
                cl_list.wcost = cl_list.wcost + fbstat.other_wcost[0]
                cl_list.totrev = cl_list.totrev + fbstat.other_grev[0] + fbstat.other_wrev[0]
                cl_list.totpax = cl_list.totpax + fbstat.other_gpax[0] + fbstat.other_wpax[0]
                cl_list.totcost = cl_list.totcost + fbstat.other_gcost[0] + fbstat.other_wcost[0]

                if cl_list.grev != 0 and cl_list.gpax != 0:
                    cl_list.gavg = cl_list.grev / cl_list.gpax

                if cl_list.wrev != 0 and cl_list.wpax != 0:
                    cl_list.wavg = cl_list.wrev / cl_list.wpax

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.typ == 3 and cl_list.descrip.lower()  == "Lunch"), first=True)
                cl_list.grev = cl_list.grev + fbstat.other_grev[1]
                cl_list.gpax = cl_list.gpax + fbstat.other_gpax[1]
                cl_list.gcost = cl_list.gcost + fbstat.other_gcost[1]
                cl_list.wrev = cl_list.wrev + fbstat.other_wrev[1]
                cl_list.wpax = cl_list.wpax + fbstat.other_wpax[1]
                cl_list.wcost = cl_list.wcost + fbstat.other_wcost[1]
                cl_list.totrev = cl_list.totrev + fbstat.other_grev[1] + fbstat.other_wrev[1]
                cl_list.totpax = cl_list.totpax + fbstat.other_gpax[1] + fbstat.other_wpax[1]
                cl_list.totcost = cl_list.totcost + fbstat.other_gcost[1] + fbstat.other_wcost[1]

                if cl_list.grev != 0 and cl_list.gpax != 0:
                    cl_list.gavg = cl_list.grev / cl_list.gpax

                if cl_list.wrev != 0 and cl_list.wpax != 0:
                    cl_list.wavg = cl_list.wrev / cl_list.wpax

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.typ == 3 and cl_list.descrip.lower()  == "Dinner"), first=True)
                cl_list.grev = cl_list.grev + fbstat.other_grev[2]
                cl_list.gpax = cl_list.gpax + fbstat.other_gpax[2]
                cl_list.gcost = cl_list.gcost + fbstat.other_gcost[2]
                cl_list.wrev = cl_list.wrev + fbstat.other_wrev[2]
                cl_list.wpax = cl_list.wpax + fbstat.other_wpax[2]
                cl_list.wcost = cl_list.wcost + fbstat.other_wcost[2]
                cl_list.totrev = cl_list.totrev + fbstat.other_grev[2] + fbstat.other_wrev[2]
                cl_list.totpax = cl_list.totpax + fbstat.other_gpax[2] + fbstat.other_wpax[2]
                cl_list.totcost = cl_list.totcost + fbstat.other_gcost[2] + fbstat.other_wcost[2]

                if cl_list.grev != 0 and cl_list.gpax != 0:
                    cl_list.gavg = cl_list.grev / cl_list.gpax

                if cl_list.wrev != 0 and cl_list.wpax != 0:
                    cl_list.wavg = cl_list.wrev / cl_list.wpax

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.typ == 3 and cl_list.descrip.lower()  == "Supper"), first=True)

                if cl_list:
                    cl_list.grev = cl_list.grev + fbstat.other_grev[3]
                    cl_list.gpax = cl_list.gpax + fbstat.other_gpax[3]
                    cl_list.gcost = cl_list.gcost + fbstat.other_gcost[3]
                    cl_list.wrev = cl_list.wrev + fbstat.other_wrev[3]
                    cl_list.wpax = cl_list.wpax + fbstat.other_wpax[3]
                    cl_list.wcost = cl_list.wcost + fbstat.other_wcost[3]
                    cl_list.totrev = cl_list.totrev + fbstat.other_grev[3] + fbstat.other_wrev[3]
                    cl_list.totpax = cl_list.totpax + fbstat.other_gpax[3] + fbstat.other_wpax[3]
                    cl_list.totcost = cl_list.totcost + fbstat.other_gcost[3] + fbstat.other_wcost[3]

                    if cl_list.grev != 0 and cl_list.gpax != 0:
                        cl_list.gavg = cl_list.grev / cl_list.gpax

                    if cl_list.wrev != 0 and cl_list.wpax != 0:
                        cl_list.wavg = cl_list.wrev / cl_list.wpax
            tgpax = 0
            tgrev = 0
            tgcost = 0
            twpax = 0
            twrev = 0
            twcost = 0
            ttotpax = 0
            ttotrev = 0
            ttotcost = 0

            for cl_list in query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.TYP == 1)):
                tgpax = tgpax + cl_list.gpax
                tgrev = tgrev + cl_list.grev
                tgcost = tgcost + cl_list.gcost
                twpax = twpax + cl_list.wpax
                twrev = twrev + cl_list.wrev
                twcost = twcost + cl_list.wcost
                ttotpax = ttotpax + cl_list.totpax
                ttotrev = ttotrev + cl_list.totrev
                ttotcost = ttotcost + cl_list.totcost

            for cl_list in query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.typ == 1)):

                if cl_list.grev != 0 and tgrev != 0:
                    cl_list.gproz = cl_list.grev / tgrev * 100

                if cl_list.wrev != 0 and twrev != 0:
                    cl_list.wproz = cl_list.wrev / twrev * 100

            cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.typ == 1 and cl_list.descrip.lower()  == "FOOD TOTAL"), first=True)

            if cl_list:
                cl_list.gpax = tgpax
                cl_list.grev = tgrev
                cl_list.gcost = tgcost
                cl_list.gproz = 100
                cl_list.wpax = twpax
                cl_list.wrev = twrev
                cl_list.wcost = twcost
                cl_list.wproz = 100
                cl_list.totpax = ttotpax
                cl_list.totrev = ttotrev
                cl_list.totcost = ttotcost

                if tgpax != 0:
                    cl_list.gavg = tgrev / tgpax

                if twpax != 0:
                    cl_list.wavg = twrev / twpax
            tot_gpax = tot_gpax + tgpax
            tot_grev = tot_grev + tgrev
            tot_gcost = tot_gcost + tgcost
            tot_wpax = tot_wpax + twpax
            tot_wrev = tot_wrev + twrev
            tot_wcost = tot_wcost + twcost
            tot_tpax = tot_tpax + ttotpax
            tot_trev = tot_trev + ttotrev
            tot_tcost = tot_tcost + ttotcost


            tgpax = 0
            tgrev = 0
            tgcost = 0
            twpax = 0
            twrev = 0
            twcost = 0
            ttotpax = 0
            ttotrev = 0
            ttotcost = 0

            for cl_list in query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.TYP == 2)):
                tgpax = tgpax + cl_list.gpax
                tgrev = tgrev + cl_list.grev
                tgcost = tgcost + cl_list.gcost
                twpax = twpax + cl_list.wpax
                twrev = twrev + cl_list.wrev
                twcost = twcost + cl_list.wcost
                ttotpax = ttotpax + cl_list.totpax
                ttotrev = ttotrev + cl_list.totrev
                ttotcost = ttotcost + cl_list.totcost

            for cl_list in query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.typ == 2)):

                if cl_list.grev != 0 and tgrev != 0:
                    cl_list.gproz = cl_list.grev / tgrev * 100

                if cl_list.wrev != 0 and twrev != 0:
                    cl_list.wproz = cl_list.wrev / twrev * 100

            cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.typ == 2 and cl_list.descrip.lower()  == "BEV TOTAL"), first=True)

            if cl_list:
                cl_list.gpax = tgpax
                cl_list.grev = tgrev
                cl_list.gcost = tgcost
                cl_list.gproz = 100
                cl_list.wpax = twpax
                cl_list.wrev = twrev
                cl_list.wcost = twcost
                cl_list.wproz = 100
                cl_list.totpax = ttotpax
                cl_list.totrev = ttotrev
                cl_list.totcost = ttotcost

                if tgpax != 0:
                    cl_list.gavg = tgrev / tgpax

                if twpax != 0:
                    cl_list.wavg = twrev / twpax
            tot_gpax = tot_gpax + tgpax
            tot_grev = tot_grev + tgrev
            tot_gcost = tot_gcost + tgcost
            tot_wpax = tot_wpax + twpax
            tot_wrev = tot_wrev + twrev
            tot_wcost = tot_wcost + twcost
            tot_tpax = tot_tpax + ttotpax
            tot_trev = tot_trev + ttotrev
            tot_tcost = tot_tcost + ttotcost


            tgpax = 0
            tgrev = 0
            tgcost = 0
            twpax = 0
            twrev = 0
            twcost = 0
            ttotpax = 0
            ttotrev = 0
            ttotcost = 0

            for cl_list in query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.TYP == 3)):
                tgpax = tgpax + cl_list.gpax
                tgrev = tgrev + cl_list.grev
                tgcost = tgcost + cl_list.gcost
                twpax = twpax + cl_list.wpax
                twrev = twrev + cl_list.wrev
                twcost = twcost + cl_list.wcost
                ttotpax = ttotpax + cl_list.totpax
                ttotrev = ttotrev + cl_list.totrev
                ttotcost = ttotcost + cl_list.totcost

            for cl_list in query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.typ == 3)):

                if cl_list.grev != 0 and tgrev != 0:
                    cl_list.gproz = cl_list.grev / tgrev * 100

                if cl_list.wrev != 0 and twrev != 0:
                    cl_list.wproz = cl_list.wrev / twrev * 100

            cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.typ == 3 and cl_list.descrip.lower()  == "OTHER TOTAL"), first=True)

            if cl_list:
                cl_list.gpax = tgpax
                cl_list.grev = tgrev
                cl_list.gcost = tgcost
                cl_list.gproz = 100
                cl_list.wpax = twpax
                cl_list.wrev = twrev
                cl_list.wcost = twcost
                cl_list.wproz = 100
                cl_list.totpax = ttotpax
                cl_list.totrev = ttotrev
                cl_list.totcost = ttotcost

                if tgpax != 0:
                    cl_list.gavg = tgrev / tgpax

                if twpax != 0:
                    cl_list.wavg = twrev / twpax
            tot_gpax = tot_gpax + tgpax
            tot_grev = tot_grev + tgrev
            tot_gcost = tot_gcost + tgcost
            tot_wpax = tot_wpax + twpax
            tot_wrev = tot_wrev + twrev
            tot_wcost = tot_wcost + twcost
            tot_tpax = tot_tpax + ttotpax
            tot_trev = tot_trev + ttotrev
            tot_tcost = tot_tcost + ttotcost

            cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num and cl_list.descrip.lower()  == "TOTAL"), first=True)

            if cl_list:
                cl_list.gpax = tot_gpax
                cl_list.grev = tot_grev
                cl_list.gcost = tot_gcost
                cl_list.gproz = 100
                cl_list.wpax = tot_wpax
                cl_list.wrev = tot_wrev
                cl_list.wcost = tot_wcost
                cl_list.wproz = 100
                cl_list.totpax = tot_tpax
                cl_list.totrev = tot_trev
                cl_list.totcost = tot_tcost

                if tot_gpax != 0:
                    cl_list.gavg = tot_grev / tot_gpax

                if twpax != 0:
                    cl_list.wavg = tot_wrev / tot_wpax


    create_list()

    return generate_output()