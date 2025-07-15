#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fbstat, Hoteldpt

def fb_statistic_create_list_webbl(pvilanguage:int, fdept:int, tdept:int, fdate:date, tdate:date, price_decimal:int):

    prepare_cache ([Fbstat, Hoteldpt])

    cl_list_data = []
    tgrev:Decimal = to_decimal("0.0")
    twrev:Decimal = to_decimal("0.0")
    tgpax:int = 0
    tgcost:Decimal = to_decimal("0.0")
    twpax:int = 0
    twcost:Decimal = to_decimal("0.0")
    ttotpax:int = 0
    ttotrev:Decimal = to_decimal("0.0")
    ttotcost:Decimal = to_decimal("0.0")
    tot_gpax:int = 0
    tot_grev:Decimal = to_decimal("0.0")
    tot_gcost:Decimal = to_decimal("0.0")
    tot_wpax:int = 0
    tot_wrev:Decimal = to_decimal("0.0")
    tot_wcost:Decimal = to_decimal("0.0")
    tot_tpax:int = 0
    tot_trev:Decimal = to_decimal("0.0")
    tot_tcost:Decimal = to_decimal("0.0")
    fbstat = hoteldpt = None

    cl_list = None

    cl_list_data, Cl_list = create_model("Cl_list", {"dept":int, "deptname":string, "typ":int, "descrip":string, "grev":Decimal, "gpax":int, "gproz":Decimal, "gcost":Decimal, "gavg":Decimal, "wrev":Decimal, "wpax":int, "wproz":Decimal, "wcost":Decimal, "wavg":Decimal, "totpax":int, "totrev":Decimal, "totcost":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cl_list_data, tgrev, twrev, tgpax, tgcost, twpax, twcost, ttotpax, ttotrev, ttotcost, tot_gpax, tot_grev, tot_gcost, tot_wpax, tot_wrev, tot_wcost, tot_tpax, tot_trev, tot_tcost, fbstat, hoteldpt
        nonlocal pvilanguage, fdept, tdept, fdate, tdate, price_decimal


        nonlocal cl_list
        nonlocal cl_list_data

        return {"cl-list": cl_list_data}

    def create_list():

        nonlocal cl_list_data, tgrev, twrev, tgpax, tgcost, twpax, twcost, ttotpax, ttotrev, ttotcost, tot_gpax, tot_grev, tot_gcost, tot_wpax, tot_wrev, tot_wcost, tot_tpax, tot_trev, tot_tcost, fbstat, hoteldpt
        nonlocal pvilanguage, fdept, tdept, fdate, tdate, price_decimal


        nonlocal cl_list
        nonlocal cl_list_data

        stat = None
        Stat =  create_buffer("Stat",Fbstat)
        cl_list_data.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num > 0) & (Hoteldpt.num >= fdept) & (Hoteldpt.num <= tdept)).order_by(Hoteldpt.num).all():
            tot_gpax = 0
            tot_grev =  to_decimal("0")
            tot_gcost =  to_decimal("0")
            tot_wpax = 0
            tot_wrev =  to_decimal("0")
            tot_wcost =  to_decimal("0")
            tot_tpax = 0
            tot_trev =  to_decimal("0")
            tot_tcost =  to_decimal("0")

            stat = get_cache (Fbstat, {"departement": [(eq, hoteldpt.num)],"datum": [(ge, fdate),(le, tdate)]})

            if stat:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.descrip = to_string(hoteldpt.num) + " - " +\
                        hoteldpt.depart


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.typ = 1
                cl_list.descrip = "Breakfast"


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.typ = 1
                cl_list.descrip = "Lunch"


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.typ = 1
                cl_list.descrip = "Dinner"


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.typ = 1
                cl_list.descrip = "Supper"


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.descrip = "-----"
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.descrip = "FOOD TOTAL"
                cl_list.dept = hoteldpt.num
                cl_list.typ = 1


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.typ = 2
                cl_list.descrip = "Breakfast"


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.typ = 2
                cl_list.descrip = "Lunch"


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.typ = 2
                cl_list.descrip = "Dinner"


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.typ = 2
                cl_list.descrip = "Supper"


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.descrip = "-----"
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.descrip = "BEV TOTAL"
                cl_list.dept = hoteldpt.num
                cl_list.typ = 2


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.typ = 3
                cl_list.descrip = "Breakfast"


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.typ = 3
                cl_list.descrip = "Lunch"


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.typ = 3
                cl_list.descrip = "Dinner"


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.dept = hoteldpt.num
                cl_list.deptname = hoteldpt.depart
                cl_list.typ = 3
                cl_list.descrip = "Supper"


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.descrip = "-----"
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.descrip = "OTHER TOTAL"
                cl_list.dept = hoteldpt.num
                cl_list.typ = 3


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.descrip = "TOTAL"
                cl_list.dept = hoteldpt.num
                cl_list.typ = 4


                cl_list = Cl_list()
                cl_list_data.append(cl_list)


            for fbstat in db_session.query(Fbstat).filter(
                     (Fbstat.datum >= fdate) & (Fbstat.datum <= tdate) & (Fbstat.departement == hoteldpt.num)).order_by(Fbstat._recid).all():

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.typ == 1 and cl_list.descrip.lower()  == ("Breakfast").lower()), first=True)

                if cl_list:
                    cl_list.grev =  to_decimal(cl_list.grev) + to_decimal(fbstat.food_grev[0])
                    cl_list.gpax = cl_list.gpax + fbstat.food_gpax[0]
                    cl_list.gcost =  to_decimal(cl_list.gcost) + to_decimal(fbstat.food_gcost[0])
                    cl_list.wrev =  to_decimal(cl_list.wrev) + to_decimal(fbstat.food_wrev[0])
                    cl_list.wpax = cl_list.wpax + fbstat.food_wpax[0]
                    cl_list.wcost =  to_decimal(cl_list.wcost) + to_decimal(fbstat.food_wcost[0])
                    cl_list.totrev =  to_decimal(cl_list.totrev) + to_decimal(fbstat.food_grev[0] + fbstat.food_wrev[0])
                    cl_list.totpax = cl_list.totpax + fbstat.food_gpax[0] + fbstat.food_wpax[0]
                    cl_list.totcost =  to_decimal(cl_list.totcost) + to_decimal(fbstat.food_gcost[0] + fbstat.food_wcost[0])

                    if cl_list.grev != 0 and cl_list.gpax != 0:
                        cl_list.gavg =  to_decimal(cl_list.grev) / to_decimal(cl_list.gpax)

                    if cl_list.wrev != 0 and cl_list.wpax != 0:
                        cl_list.wavg =  to_decimal(cl_list.wrev) / to_decimal(cl_list.wpax)

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.typ == 1 and cl_list.descrip.lower()  == ("Lunch").lower()), first=True)

                if cl_list:
                    cl_list.grev =  to_decimal(cl_list.grev) + to_decimal(fbstat.food_grev[1])
                    cl_list.gpax = cl_list.gpax + fbstat.food_gpax[1]
                    cl_list.gcost =  to_decimal(cl_list.gcost) + to_decimal(fbstat.food_gcost[1])
                    cl_list.wrev =  to_decimal(cl_list.wrev) + to_decimal(fbstat.food_wrev[1])
                    cl_list.wpax = cl_list.wpax + fbstat.food_wpax[1]
                    cl_list.wcost =  to_decimal(cl_list.wcost) + to_decimal(fbstat.food_wcost[1])
                    cl_list.totrev =  to_decimal(cl_list.totrev) + to_decimal(fbstat.food_grev[1] + fbstat.food_wrev[1])
                    cl_list.totpax = cl_list.totpax + fbstat.food_gpax[1] + fbstat.food_wpax[1]
                    cl_list.totcost =  to_decimal(cl_list.totcost) + to_decimal(fbstat.food_gcost[1] + fbstat.food_wcost[1])

                    if cl_list.grev != 0 and cl_list.gpax != 0:
                        cl_list.gavg =  to_decimal(cl_list.grev) / to_decimal(cl_list.gpax)

                    if cl_list.wrev != 0 and cl_list.wpax != 0:
                        cl_list.wavg =  to_decimal(cl_list.wrev) / to_decimal(cl_list.wpax)

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.typ == 1 and cl_list.descrip.lower()  == ("Dinner").lower()), first=True)

                if cl_list:
                    cl_list.grev =  to_decimal(cl_list.grev) + to_decimal(fbstat.food_grev[2])
                    cl_list.gpax = cl_list.gpax + fbstat.food_gpax[2]
                    cl_list.gcost =  to_decimal(cl_list.gcost) + to_decimal(fbstat.food_gcost[2])
                    cl_list.wrev =  to_decimal(cl_list.wrev) + to_decimal(fbstat.food_wrev[2])
                    cl_list.wpax = cl_list.wpax + fbstat.food_wpax[2]
                    cl_list.wcost =  to_decimal(cl_list.wcost) + to_decimal(fbstat.food_wcost[2])
                    cl_list.totrev =  to_decimal(cl_list.totrev) + to_decimal(fbstat.food_grev[2] + fbstat.food_wrev[2])
                    cl_list.totpax = cl_list.totpax + fbstat.food_gpax[2] + fbstat.food_wpax[2]
                    cl_list.totcost =  to_decimal(cl_list.totcost) + to_decimal(fbstat.food_gcost[2] + fbstat.food_wcost[2])

                    if cl_list.grev != 0 and cl_list.gpax != 0:
                        cl_list.gavg =  to_decimal(cl_list.grev) / to_decimal(cl_list.gpax)

                    if cl_list.wrev != 0 and cl_list.wpax != 0:
                        cl_list.wavg =  to_decimal(cl_list.wrev) / to_decimal(cl_list.wpax)

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.typ == 1 and cl_list.descrip.lower()  == ("Supper").lower()), first=True)

                if cl_list:
                    cl_list.grev =  to_decimal(cl_list.grev) + to_decimal(fbstat.food_grev[3])
                    cl_list.gpax = cl_list.gpax + fbstat.food_gpax[3]
                    cl_list.gcost =  to_decimal(cl_list.gcost) + to_decimal(fbstat.food_gcost[3])
                    cl_list.wrev =  to_decimal(cl_list.wrev) + to_decimal(fbstat.food_wrev[3])
                    cl_list.wpax = cl_list.wpax + fbstat.food_wpax[3]
                    cl_list.wcost =  to_decimal(cl_list.wcost) + to_decimal(fbstat.food_wcost[3])
                    cl_list.totrev =  to_decimal(cl_list.totrev) + to_decimal(fbstat.food_grev[3] + fbstat.food_wrev[3])
                    cl_list.totpax = cl_list.totpax + fbstat.food_gpax[3] + fbstat.food_wpax[3]
                    cl_list.totcost =  to_decimal(cl_list.totcost) + to_decimal(fbstat.food_gcost[3] + fbstat.food_wcost[3])

                    if cl_list.grev != 0 and cl_list.gpax != 0:
                        cl_list.gavg =  to_decimal(cl_list.grev) / to_decimal(cl_list.gpax)

                    if cl_list.wavg != 0 and cl_list.wpax != 0:
                        cl_list.wrev =  to_decimal(cl_list.wrev) / to_decimal(cl_list.wpax)

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.typ == 2 and cl_list.descrip.lower()  == ("Breakfast").lower()), first=True)

                if cl_list:
                    cl_list.grev =  to_decimal(cl_list.grev) + to_decimal(fbstat.bev_grev[0])
                    cl_list.gpax = cl_list.gpax + fbstat.bev_gpax[0]
                    cl_list.gcost =  to_decimal(cl_list.gcost) + to_decimal(fbstat.bev_gcost[0])
                    cl_list.wrev =  to_decimal(cl_list.wrev) + to_decimal(fbstat.bev_wrev[0])
                    cl_list.wpax = cl_list.wpax + fbstat.bev_wpax[0]
                    cl_list.wcost =  to_decimal(cl_list.wcost) + to_decimal(fbstat.bev_wcost[0])
                    cl_list.totrev =  to_decimal(cl_list.totrev) + to_decimal(fbstat.bev_grev[0] + fbstat.bev_wrev[0])
                    cl_list.totpax = cl_list.totpax + fbstat.bev_gpax[0] + fbstat.bev_wpax[0]
                    cl_list.totcost =  to_decimal(cl_list.totcost) + to_decimal(fbstat.bev_gcost[0] + fbstat.bev_wcost[0])

                    if cl_list.grev != 0 and cl_list.gpax != 0:
                        cl_list.gavg =  to_decimal(cl_list.grev) / to_decimal(cl_list.gpax)

                    if cl_list.wrev != 0 and cl_list.wpax != 0:
                        cl_list.wavg =  to_decimal(cl_list.wrev) / to_decimal(cl_list.wpax)

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.typ == 2 and cl_list.descrip.lower()  == ("Lunch").lower()), first=True)

                if cl_list:
                    cl_list.grev =  to_decimal(cl_list.grev) + to_decimal(fbstat.bev_grev[1])
                    cl_list.gpax = cl_list.gpax + fbstat.bev_gpax[1]
                    cl_list.gcost =  to_decimal(cl_list.gcost) + to_decimal(fbstat.bev_gcost[1])
                    cl_list.wrev =  to_decimal(cl_list.wrev) + to_decimal(fbstat.bev_wrev[1])
                    cl_list.wpax = cl_list.wpax + fbstat.bev_wpax[1]
                    cl_list.wcost =  to_decimal(cl_list.wcost) + to_decimal(fbstat.bev_wcost[1])
                    cl_list.totrev =  to_decimal(cl_list.totrev) + to_decimal(fbstat.bev_grev[1] + fbstat.bev_wrev[1])
                    cl_list.totpax = cl_list.totpax + fbstat.bev_gpax[1] + fbstat.bev_wpax[1]
                    cl_list.totcost =  to_decimal(cl_list.totcost) + to_decimal(fbstat.bev_gcost[1] + fbstat.bev_wcost[1])

                    if cl_list.grev != 0 and cl_list.gpax != 0:
                        cl_list.gavg =  to_decimal(cl_list.grev) / to_decimal(cl_list.gpax)

                    if cl_list.wrev != 0 and cl_list.wpax != 0:
                        cl_list.wavg =  to_decimal(cl_list.wrev) / to_decimal(cl_list.wpax)

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.typ == 2 and cl_list.descrip.lower()  == ("Dinner").lower()), first=True)

                if cl_list:
                    cl_list.grev =  to_decimal(cl_list.grev) + to_decimal(fbstat.bev_grev[2])
                    cl_list.gpax = cl_list.gpax + fbstat.bev_gpax[2]
                    cl_list.gcost =  to_decimal(cl_list.gcost) + to_decimal(fbstat.bev_gcost[2])
                    cl_list.wrev =  to_decimal(cl_list.wrev) + to_decimal(fbstat.bev_wrev[2])
                    cl_list.wpax = cl_list.wpax + fbstat.bev_wpax[2]
                    cl_list.wcost =  to_decimal(cl_list.wcost) + to_decimal(fbstat.bev_wcost[2])
                    cl_list.totrev =  to_decimal(cl_list.totrev) + to_decimal(fbstat.bev_grev[2] + fbstat.bev_wrev[2])
                    cl_list.totpax = cl_list.totpax + fbstat.bev_gpax[2] + fbstat.bev_wpax[2]
                    cl_list.totcost =  to_decimal(cl_list.totcost) + to_decimal(fbstat.bev_gcost[2] + fbstat.bev_wcost[2])

                    if cl_list.grev != 0 and cl_list.gpax != 0:
                        cl_list.gavg =  to_decimal(cl_list.grev) / to_decimal(cl_list.gpax)

                    if cl_list.wrev != 0 and cl_list.wpax != 0:
                        cl_list.wavg =  to_decimal(cl_list.wrev) / to_decimal(cl_list.wpax)

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.typ == 2 and cl_list.descrip.lower()  == ("Supper").lower()), first=True)

                if cl_list:
                    cl_list.grev =  to_decimal(cl_list.grev) + to_decimal(fbstat.bev_grev[3])
                    cl_list.gpax = cl_list.gpax + fbstat.bev_gpax[3]
                    cl_list.gcost =  to_decimal(cl_list.gcost) + to_decimal(fbstat.bev_gcost[3])
                    cl_list.wrev =  to_decimal(cl_list.wrev) + to_decimal(fbstat.bev_wrev[3])
                    cl_list.wpax = cl_list.wpax + fbstat.bev_wpax[3]
                    cl_list.wcost =  to_decimal(cl_list.wcost) + to_decimal(fbstat.bev_wcost[3])
                    cl_list.totrev =  to_decimal(cl_list.totrev) + to_decimal(fbstat.bev_grev[3] + fbstat.bev_wrev[3])
                    cl_list.totpax = cl_list.totpax + fbstat.bev_gpax[3] + fbstat.bev_wpax[3]
                    cl_list.totcost =  to_decimal(cl_list.totcost) + to_decimal(fbstat.bev_gcost[3] + fbstat.bev_wcost[3])

                    if cl_list.grev != 0 and cl_list.gpax != 0:
                        cl_list.gavg =  to_decimal(cl_list.grev) / to_decimal(cl_list.gpax)

                    if cl_list.wrev != 0 and cl_list.wpax != 0:
                        cl_list.wavg =  to_decimal(cl_list.wrev) / to_decimal(cl_list.wpax)

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.typ == 3 and cl_list.descrip.lower()  == ("Breakfast").lower()), first=True)
                cl_list.grev =  to_decimal(cl_list.grev) + to_decimal(fbstat.other_grev[0])
                cl_list.gpax = cl_list.gpax + fbstat.other_gpax[0]
                cl_list.gcost =  to_decimal(cl_list.gcost) + to_decimal(fbstat.other_gcost[0])
                cl_list.wrev =  to_decimal(cl_list.wrev) + to_decimal(fbstat.other_wrev[0])
                cl_list.wpax = cl_list.wpax + fbstat.other_wpax[0]
                cl_list.wcost =  to_decimal(cl_list.wcost) + to_decimal(fbstat.other_wcost[0])
                cl_list.totrev =  to_decimal(cl_list.totrev) + to_decimal(fbstat.other_grev[0] + fbstat.other_wrev[0])
                cl_list.totpax = cl_list.totpax + fbstat.other_gpax[0] + fbstat.other_wpax[0]
                cl_list.totcost =  to_decimal(cl_list.totcost) + to_decimal(fbstat.other_gcost[0] + fbstat.other_wcost[0])

                if cl_list.grev != 0 and cl_list.gpax != 0:
                    cl_list.gavg =  to_decimal(cl_list.grev) / to_decimal(cl_list.gpax)

                if cl_list.wrev != 0 and cl_list.wpax != 0:
                    cl_list.wavg =  to_decimal(cl_list.wrev) / to_decimal(cl_list.wpax)

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.typ == 3 and cl_list.descrip.lower()  == ("Lunch").lower()), first=True)
                cl_list.grev =  to_decimal(cl_list.grev) + to_decimal(fbstat.other_grev[1])
                cl_list.gpax = cl_list.gpax + fbstat.other_gpax[1]
                cl_list.gcost =  to_decimal(cl_list.gcost) + to_decimal(fbstat.other_gcost[1])
                cl_list.wrev =  to_decimal(cl_list.wrev) + to_decimal(fbstat.other_wrev[1])
                cl_list.wpax = cl_list.wpax + fbstat.other_wpax[1]
                cl_list.wcost =  to_decimal(cl_list.wcost) + to_decimal(fbstat.other_wcost[1])
                cl_list.totrev =  to_decimal(cl_list.totrev) + to_decimal(fbstat.other_grev[1] + fbstat.other_wrev[1])
                cl_list.totpax = cl_list.totpax + fbstat.other_gpax[1] + fbstat.other_wpax[1]
                cl_list.totcost =  to_decimal(cl_list.totcost) + to_decimal(fbstat.other_gcost[1] + fbstat.other_wcost[1])

                if cl_list.grev != 0 and cl_list.gpax != 0:
                    cl_list.gavg =  to_decimal(cl_list.grev) / to_decimal(cl_list.gpax)

                if cl_list.wrev != 0 and cl_list.wpax != 0:
                    cl_list.wavg =  to_decimal(cl_list.wrev) / to_decimal(cl_list.wpax)

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.typ == 3 and cl_list.descrip.lower()  == ("Dinner").lower()), first=True)
                cl_list.grev =  to_decimal(cl_list.grev) + to_decimal(fbstat.other_grev[2])
                cl_list.gpax = cl_list.gpax + fbstat.other_gpax[2]
                cl_list.gcost =  to_decimal(cl_list.gcost) + to_decimal(fbstat.other_gcost[2])
                cl_list.wrev =  to_decimal(cl_list.wrev) + to_decimal(fbstat.other_wrev[2])
                cl_list.wpax = cl_list.wpax + fbstat.other_wpax[2]
                cl_list.wcost =  to_decimal(cl_list.wcost) + to_decimal(fbstat.other_wcost[2])
                cl_list.totrev =  to_decimal(cl_list.totrev) + to_decimal(fbstat.other_grev[2] + fbstat.other_wrev[2])
                cl_list.totpax = cl_list.totpax + fbstat.other_gpax[2] + fbstat.other_wpax[2]
                cl_list.totcost =  to_decimal(cl_list.totcost) + to_decimal(fbstat.other_gcost[2] + fbstat.other_wcost[2])

                if cl_list.grev != 0 and cl_list.gpax != 0:
                    cl_list.gavg =  to_decimal(cl_list.grev) / to_decimal(cl_list.gpax)

                if cl_list.wrev != 0 and cl_list.wpax != 0:
                    cl_list.wavg =  to_decimal(cl_list.wrev) / to_decimal(cl_list.wpax)

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.typ == 3 and cl_list.descrip.lower()  == ("Supper").lower()), first=True)

                if cl_list:
                    cl_list.grev =  to_decimal(cl_list.grev) + to_decimal(fbstat.other_grev[3])
                    cl_list.gpax = cl_list.gpax + fbstat.other_gpax[3]
                    cl_list.gcost =  to_decimal(cl_list.gcost) + to_decimal(fbstat.other_gcost[3])
                    cl_list.wrev =  to_decimal(cl_list.wrev) + to_decimal(fbstat.other_wrev[3])
                    cl_list.wpax = cl_list.wpax + fbstat.other_wpax[3]
                    cl_list.wcost =  to_decimal(cl_list.wcost) + to_decimal(fbstat.other_wcost[3])
                    cl_list.totrev =  to_decimal(cl_list.totrev) + to_decimal(fbstat.other_grev[3] + fbstat.other_wrev[3])
                    cl_list.totpax = cl_list.totpax + fbstat.other_gpax[3] + fbstat.other_wpax[3]
                    cl_list.totcost =  to_decimal(cl_list.totcost) + to_decimal(fbstat.other_gcost[3] + fbstat.other_wcost[3])

                    if cl_list.grev != 0 and cl_list.gpax != 0:
                        cl_list.gavg =  to_decimal(cl_list.grev) / to_decimal(cl_list.gpax)

                    if cl_list.wrev != 0 and cl_list.wpax != 0:
                        cl_list.wavg =  to_decimal(cl_list.wrev) / to_decimal(cl_list.wpax)
            tgpax = 0
            tgrev =  to_decimal("0")
            tgcost =  to_decimal("0")
            twpax = 0
            twrev =  to_decimal("0")
            twcost =  to_decimal("0")
            ttotpax = 0
            ttotrev =  to_decimal("0")
            ttotcost =  to_decimal("0")

            for cl_list in query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.typ == 1)):
                tgpax = tgpax + cl_list.gpax
                tgrev =  to_decimal(tgrev) + to_decimal(cl_list.grev)
                tgcost =  to_decimal(tgcost) + to_decimal(cl_list.gcost)
                twpax = twpax + cl_list.wpax
                twrev =  to_decimal(twrev) + to_decimal(cl_list.wrev)
                twcost =  to_decimal(twcost) + to_decimal(cl_list.wcost)
                ttotpax = ttotpax + cl_list.totpax
                ttotrev =  to_decimal(ttotrev) + to_decimal(cl_list.totrev)
                ttotcost =  to_decimal(ttotcost) + to_decimal(cl_list.totcost)

            for cl_list in query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.typ == 1)):

                if cl_list.grev != 0 and tgrev != 0:
                    cl_list.gproz =  to_decimal(cl_list.grev) / to_decimal(tgrev) * to_decimal("100")

                if cl_list.wrev != 0 and twrev != 0:
                    cl_list.wproz =  to_decimal(cl_list.wrev) / to_decimal(twrev) * to_decimal("100")

            cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.typ == 1 and cl_list.descrip.lower()  == ("FOOD TOTAL").lower()), first=True)

            if cl_list:
                cl_list.gpax = tgpax
                cl_list.grev =  to_decimal(tgrev)
                cl_list.gcost =  to_decimal(tgcost)
                cl_list.gproz =  to_decimal("100")
                cl_list.wpax = twpax
                cl_list.wrev =  to_decimal(twrev)
                cl_list.wcost =  to_decimal(twcost)
                cl_list.wproz =  to_decimal("100")
                cl_list.totpax = ttotpax
                cl_list.totrev =  to_decimal(ttotrev)
                cl_list.totcost =  to_decimal(ttotcost)

                if tgpax != 0:
                    cl_list.gavg =  to_decimal(tgrev) / to_decimal(tgpax)

                if twpax != 0:
                    cl_list.wavg =  to_decimal(twrev) / to_decimal(twpax)
            tot_gpax = tot_gpax + tgpax
            tot_grev =  to_decimal(tot_grev) + to_decimal(tgrev)
            tot_gcost =  to_decimal(tot_gcost) + to_decimal(tgcost)
            tot_wpax = tot_wpax + twpax
            tot_wrev =  to_decimal(tot_wrev) + to_decimal(twrev)
            tot_wcost =  to_decimal(tot_wcost) + to_decimal(twcost)
            tot_tpax = tot_tpax + ttotpax
            tot_trev =  to_decimal(tot_trev) + to_decimal(ttotrev)
            tot_tcost =  to_decimal(tot_tcost) + to_decimal(ttotcost)


            tgpax = 0
            tgrev =  to_decimal("0")
            tgcost =  to_decimal("0")
            twpax = 0
            twrev =  to_decimal("0")
            twcost =  to_decimal("0")
            ttotpax = 0
            ttotrev =  to_decimal("0")
            ttotcost =  to_decimal("0")

            for cl_list in query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.typ == 2)):
                tgpax = tgpax + cl_list.gpax
                tgrev =  to_decimal(tgrev) + to_decimal(cl_list.grev)
                tgcost =  to_decimal(tgcost) + to_decimal(cl_list.gcost)
                twpax = twpax + cl_list.wpax
                twrev =  to_decimal(twrev) + to_decimal(cl_list.wrev)
                twcost =  to_decimal(twcost) + to_decimal(cl_list.wcost)
                ttotpax = ttotpax + cl_list.totpax
                ttotrev =  to_decimal(ttotrev) + to_decimal(cl_list.totrev)
                ttotcost =  to_decimal(ttotcost) + to_decimal(cl_list.totcost)

            for cl_list in query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.typ == 2)):

                if cl_list.grev != 0 and tgrev != 0:
                    cl_list.gproz =  to_decimal(cl_list.grev) / to_decimal(tgrev) * to_decimal("100")

                if cl_list.wrev != 0 and twrev != 0:
                    cl_list.wproz =  to_decimal(cl_list.wrev) / to_decimal(twrev) * to_decimal("100")

            cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.typ == 2 and cl_list.descrip.lower()  == ("BEV TOTAL").lower()), first=True)

            if cl_list:
                cl_list.gpax = tgpax
                cl_list.grev =  to_decimal(tgrev)
                cl_list.gcost =  to_decimal(tgcost)
                cl_list.gproz =  to_decimal("100")
                cl_list.wpax = twpax
                cl_list.wrev =  to_decimal(twrev)
                cl_list.wcost =  to_decimal(twcost)
                cl_list.wproz =  to_decimal("100")
                cl_list.totpax = ttotpax
                cl_list.totrev =  to_decimal(ttotrev)
                cl_list.totcost =  to_decimal(ttotcost)

                if tgpax != 0:
                    cl_list.gavg =  to_decimal(tgrev) / to_decimal(tgpax)

                if twpax != 0:
                    cl_list.wavg =  to_decimal(twrev) / to_decimal(twpax)
            tot_gpax = tot_gpax + tgpax
            tot_grev =  to_decimal(tot_grev) + to_decimal(tgrev)
            tot_gcost =  to_decimal(tot_gcost) + to_decimal(tgcost)
            tot_wpax = tot_wpax + twpax
            tot_wrev =  to_decimal(tot_wrev) + to_decimal(twrev)
            tot_wcost =  to_decimal(tot_wcost) + to_decimal(twcost)
            tot_tpax = tot_tpax + ttotpax
            tot_trev =  to_decimal(tot_trev) + to_decimal(ttotrev)
            tot_tcost =  to_decimal(tot_tcost) + to_decimal(ttotcost)


            tgpax = 0
            tgrev =  to_decimal("0")
            tgcost =  to_decimal("0")
            twpax = 0
            twrev =  to_decimal("0")
            twcost =  to_decimal("0")
            ttotpax = 0
            ttotrev =  to_decimal("0")
            ttotcost =  to_decimal("0")

            for cl_list in query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.typ == 3)):
                tgpax = tgpax + cl_list.gpax
                tgrev =  to_decimal(tgrev) + to_decimal(cl_list.grev)
                tgcost =  to_decimal(tgcost) + to_decimal(cl_list.gcost)
                twpax = twpax + cl_list.wpax
                twrev =  to_decimal(twrev) + to_decimal(cl_list.wrev)
                twcost =  to_decimal(twcost) + to_decimal(cl_list.wcost)
                ttotpax = ttotpax + cl_list.totpax
                ttotrev =  to_decimal(ttotrev) + to_decimal(cl_list.totrev)
                ttotcost =  to_decimal(ttotcost) + to_decimal(cl_list.totcost)

            for cl_list in query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.typ == 3)):

                if cl_list.grev != 0 and tgrev != 0:
                    cl_list.gproz =  to_decimal(cl_list.grev) / to_decimal(tgrev) * to_decimal("100")

                if cl_list.wrev != 0 and twrev != 0:
                    cl_list.wproz =  to_decimal(cl_list.wrev) / to_decimal(twrev) * to_decimal("100")

            cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.typ == 3 and cl_list.descrip.lower()  == ("OTHER TOTAL").lower()), first=True)

            if cl_list:
                cl_list.gpax = tgpax
                cl_list.grev =  to_decimal(tgrev)
                cl_list.gcost =  to_decimal(tgcost)
                cl_list.gproz =  to_decimal("100")
                cl_list.wpax = twpax
                cl_list.wrev =  to_decimal(twrev)
                cl_list.wcost =  to_decimal(twcost)
                cl_list.wproz =  to_decimal("100")
                cl_list.totpax = ttotpax
                cl_list.totrev =  to_decimal(ttotrev)
                cl_list.totcost =  to_decimal(ttotcost)

                if tgpax != 0:
                    cl_list.gavg =  to_decimal(tgrev) / to_decimal(tgpax)

                if twpax != 0:
                    cl_list.wavg =  to_decimal(twrev) / to_decimal(twpax)
            tot_gpax = tot_gpax + tgpax
            tot_grev =  to_decimal(tot_grev) + to_decimal(tgrev)
            tot_gcost =  to_decimal(tot_gcost) + to_decimal(tgcost)
            tot_wpax = tot_wpax + twpax
            tot_wrev =  to_decimal(tot_wrev) + to_decimal(twrev)
            tot_wcost =  to_decimal(tot_wcost) + to_decimal(twcost)
            tot_tpax = tot_tpax + ttotpax
            tot_trev =  to_decimal(tot_trev) + to_decimal(ttotrev)
            tot_tcost =  to_decimal(tot_tcost) + to_decimal(ttotcost)

            cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num and cl_list.descrip.lower()  == ("TOTAL").lower()), first=True)

            if cl_list:
                cl_list.gpax = tot_gpax
                cl_list.grev =  to_decimal(tot_grev)
                cl_list.gcost =  to_decimal(tot_gcost)
                cl_list.gproz =  to_decimal("100")
                cl_list.wpax = tot_wpax
                cl_list.wrev =  to_decimal(tot_wrev)
                cl_list.wcost =  to_decimal(tot_wcost)
                cl_list.wproz =  to_decimal("100")
                cl_list.totpax = tot_tpax
                cl_list.totrev =  to_decimal(tot_trev)
                cl_list.totcost =  to_decimal(tot_tcost)

                if tot_gpax != 0:
                    cl_list.gavg =  to_decimal(tot_grev) / to_decimal(tot_gpax)

                if twpax != 0:
                    cl_list.wavg =  to_decimal(tot_wrev) / to_decimal(tot_wpax)

    create_list()

    return generate_output()