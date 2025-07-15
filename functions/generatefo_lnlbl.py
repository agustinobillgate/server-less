from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Zimmer, Paramtext, Zinrstat, Zkstat, Segment, Segmentstat, Genstat

def generatefo_lnlbl(fdate:date, tdate:date):
    hname = ""
    drr_list_list = []
    datum:date = None
    anz0:int = 0
    anz:int = 0
    curr_today:decimal = to_decimal("0.0")
    curr_month:decimal = to_decimal("0.0")
    curr_year:decimal = to_decimal("0.0")
    jan1:date = None
    zimmer = paramtext = zinrstat = zkstat = segment = segmentstat = genstat = None

    drr_list = bdrr = None

    drr_list_list, Drr_list = create_model("Drr_list", {"bezeich":str, "flag":int, "curr_today":decimal, "curr_mtd":decimal, "curr_ytd":decimal})

    Bdrr = Drr_list
    bdrr_list = drr_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal hname, drr_list_list, datum, anz0, anz, curr_today, curr_month, curr_year, jan1, zimmer, paramtext, zinrstat, zkstat, segment, segmentstat, genstat
        nonlocal fdate, tdate
        nonlocal bdrr


        nonlocal drr_list, bdrr
        nonlocal drr_list_list

        return {"hname": hname, "drr-list": drr_list_list}

    def decode_string(in_str:str):

        nonlocal hname, drr_list_list, datum, anz0, anz, curr_today, curr_month, curr_year, jan1, zimmer, paramtext, zinrstat, zkstat, segment, segmentstat, genstat
        nonlocal fdate, tdate
        nonlocal bdrr


        nonlocal drr_list, bdrr
        nonlocal drr_list_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()

    jan1 = date_mdy(1, 1, get_year(tdate))


    anz0 = 0

    for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
        anz0 = anz0 + 1

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 240)).first()

    if paramtext and paramtext.ptexte != "":
        hname = decode_string(paramtext.ptexte)
    drr_list = Drr_list()
    drr_list_list.append(drr_list)

    drr_list.flag = 1
    drr_list.bezeich = "TOTAL ROOM"


    for datum in date_range(fdate,tdate) :

        zinrstat = db_session.query(Zinrstat).filter(
                 (Zinrstat.datum == datum) & (func.lower(Zinrstat.zinr) == ("tot-rm").lower())).first()

        if zinrstat:
            anz = zinrstat.zimmeranz
        else:
            anz = anz0

        drr_list = query(drr_list_list, filters=(lambda drr_list: drr_list.flag == 1), first=True)

        if drr_list:

            if zinrstat and (get_month(zinrstat.datum) == get_month(tdate) and get_year(zinrstat.datum) == get_year(tdate)):
                drr_list.curr_mtd =  to_decimal(drr_list.curr_mtd) + to_decimal(anz)

            if datum == tdate:
                drr_list.curr_today =  to_decimal(drr_list.curr_today) + to_decimal(anz)


            drr_list.curr_ytd =  to_decimal(drr_list.curr_ytd) + to_decimal(anz)


    drr_list = Drr_list()
    drr_list_list.append(drr_list)

    drr_list.flag = 2
    drr_list.bezeich = "ACTIVE ROOM"

    for zkstat in db_session.query(Zkstat).filter(
             (Zkstat.datum >= fdate) & (Zkstat.datum <= tdate)).order_by(Zkstat._recid).all():

        drr_list = query(drr_list_list, filters=(lambda drr_list: drr_list.flag == 2), first=True)

        if drr_list:

            if zkstat.datum == tdate:
                drr_list.curr_today =  to_decimal(drr_list.curr_today) + to_decimal(zkstat.anz100)

            if get_month(zkstat.datum) == get_month(tdate) and get_year(zkstat.datum) == get_year(tdate):
                drr_list.curr_mtd =  to_decimal(drr_list.curr_mtd) + to_decimal(zkstat.anz100)


            drr_list.curr_ytd =  to_decimal(drr_list.curr_ytd) + to_decimal(zkstat.anz100)


    drr_list = Drr_list()
    drr_list_list.append(drr_list)

    drr_list.flag = 3
    drr_list.bezeich = "OUT OF ORDER ROOM"

    for zinrstat in db_session.query(Zinrstat).filter(
             (Zinrstat.datum >= fdate) & (Zinrstat.datum <= tdate) & (func.lower(Zinrstat.zinr) == ("ooo").lower())).order_by(Zinrstat._recid).all():

        drr_list = query(drr_list_list, filters=(lambda drr_list: drr_list.flag == 3), first=True)

        if drr_list:

            if zinrstat.datum == tdate:
                drr_list.curr_today =  to_decimal(drr_list.curr_today) + to_decimal(zinrstat.zimmeranz)

            if get_month(zinrstat.datum) == get_month(tdate) and get_year(zinrstat.datum) == get_year(tdate):
                drr_list.curr_mtd =  to_decimal(drr_list.curr_mtd) + to_decimal(zinrstat.zimmeranz)


            drr_list.curr_ytd =  to_decimal(drr_list.curr_ytd) + to_decimal(zinrstat.zimmeranz)


    drr_list = Drr_list()
    drr_list_list.append(drr_list)

    drr_list.flag = 4
    drr_list.bezeich = "OUT OF SERVICE ROOM"

    for zinrstat in db_session.query(Zinrstat).filter(
             (Zinrstat.datum >= fdate) & (Zinrstat.datum <= tdate) & (func.lower(Zinrstat.zinr) == ("oos").lower())).order_by(Zinrstat._recid).all():

        drr_list = query(drr_list_list, filters=(lambda drr_list: drr_list.flag == 4), first=True)

        if drr_list:

            if zinrstat.datum == tdate:
                drr_list.curr_today =  to_decimal(drr_list.curr_today) + to_decimal(zinrstat.zimmeranz)

            if get_month(zinrstat.datum) == get_month(tdate) and get_year(zinrstat.datum) == get_year(tdate):
                drr_list.curr_mtd =  to_decimal(drr_list.curr_mtd) + to_decimal(zinrstat.zimmeranz)


            drr_list.curr_ytd =  to_decimal(drr_list.curr_ytd) + to_decimal(zinrstat.zimmeranz)


    drr_list = Drr_list()
    drr_list_list.append(drr_list)

    drr_list.flag = 5
    drr_list.bezeich = "ROOM SALEABLE"

    bdrr = query(bdrr_list, filters=(lambda bdrr: bdrr.flag == 2), first=True)

    if bdrr:
        drr_list.curr_today =  to_decimal(drr_list.curr_today) + to_decimal(bdrr.curr_today)
        drr_list.curr_mtd =  to_decimal(drr_list.curr_mtd) + to_decimal(bdrr.curr_mtd)
        drr_list.curr_ytd =  to_decimal(drr_list.curr_ytd) + to_decimal(bdrr.curr_ytd)

    bdrr = query(bdrr_list, filters=(lambda bdrr: bdrr.flag == 3), first=True)

    if bdrr:
        drr_list.curr_today =  to_decimal(drr_list.curr_today) - to_decimal(bdrr.curr_today)
        drr_list.curr_mtd =  to_decimal(drr_list.curr_mtd) - to_decimal(bdrr.curr_mtd)
        drr_list.curr_ytd =  to_decimal(drr_list.curr_ytd) - to_decimal(bdrr.curr_ytd)

    bdrr = query(bdrr_list, filters=(lambda bdrr: bdrr.flag == 4), first=True)

    if bdrr:
        drr_list.curr_today =  to_decimal(drr_list.curr_today) - to_decimal(bdrr.curr_today)
        drr_list.curr_mtd =  to_decimal(drr_list.curr_mtd) - to_decimal(bdrr.curr_mtd)
        drr_list.curr_ytd =  to_decimal(drr_list.curr_ytd) - to_decimal(bdrr.curr_ytd)


    drr_list = Drr_list()
    drr_list_list.append(drr_list)

    drr_list.flag = 6
    drr_list.bezeich = "ROOM OCCUPIED"

    for segment in db_session.query(Segment).order_by(Segment._recid).all():

        for segmentstat in db_session.query(Segmentstat).filter(
                 (Segmentstat.datum >= fdate) & (Segmentstat.datum <= tdate) & (Segmentstat.segmentcode == segment.segmentcode)).order_by(Segmentstat._recid).all():

            drr_list = query(drr_list_list, filters=(lambda drr_list: drr_list.flag == 6), first=True)

            if drr_list:

                if segmentstat.datum == tdate:
                    drr_list.curr_today =  to_decimal(drr_list.curr_today) + to_decimal(segmentstat.zimmeranz)

                if get_month(segmentstat.datum) == get_month(tdate) and get_year(segmentstat.datum) == get_year(tdate):
                    drr_list.curr_mtd =  to_decimal(drr_list.curr_mtd) + to_decimal(segmentstat.zimmeranz)


                drr_list.curr_ytd =  to_decimal(drr_list.curr_ytd) + to_decimal(segmentstat.zimmeranz)


    drr_list = Drr_list()
    drr_list_list.append(drr_list)

    drr_list.flag = 7
    drr_list.bezeich = "COMPLIMENT"

    genstat_obj_list = []
    for genstat, segment in db_session.query(Genstat, Segment).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).filter(
             (Genstat.datum >= fdate) & (Genstat.datum <= tdate) & (Genstat.zipreis == 0) & (Genstat.resstatus == 6) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
        if genstat._recid in genstat_obj_list:
            continue
        else:
            genstat_obj_list.append(genstat._recid)

        if segment.betriebsnr == 1:

            drr_list = query(drr_list_list, filters=(lambda drr_list: drr_list.flag == 7), first=True)

            if drr_list:

                if genstat.datum == tdate:
                    drr_list.curr_today =  to_decimal(drr_list.curr_today) + to_decimal("1")

                if get_month(genstat.datum) == get_month(tdate) and get_year(genstat.datum) == get_year(tdate):
                    drr_list.curr_mtd =  to_decimal(drr_list.curr_mtd) + to_decimal("1")


                drr_list.curr_ytd =  to_decimal(drr_list.curr_ytd) + to_decimal("1")


    drr_list = Drr_list()
    drr_list_list.append(drr_list)

    drr_list.flag = 8
    drr_list.bezeich = "COMPLIMENT PAYING"

    genstat_obj_list = []
    for genstat, segment in db_session.query(Genstat, Segment).join(Segment,(Segment.segmentcode == Genstat.segmentcode) & (Segment.betriebsnr != 1) & (Segment.betriebsnr != 2)).filter(
             (Genstat.datum >= fdate) & (Genstat.datum <= tdate) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)]) & (Genstat.zipreis == 0)).order_by(Genstat._recid).all():
        if genstat._recid in genstat_obj_list:
            continue
        else:
            genstat_obj_list.append(genstat._recid)

        drr_list = query(drr_list_list, filters=(lambda drr_list: drr_list.flag == 8), first=True)

        if drr_list:

            if genstat.datum == tdate:
                drr_list.curr_today =  to_decimal(drr_list.curr_today) + to_decimal("1")

            if get_month(genstat.datum) == get_month(tdate) and get_year(genstat.datum) == get_year(tdate):
                drr_list.curr_mtd =  to_decimal(drr_list.curr_mtd) + to_decimal("1")


            drr_list.curr_ytd =  to_decimal(drr_list.curr_ytd) + to_decimal("1")


    drr_list = Drr_list()
    drr_list_list.append(drr_list)

    drr_list.flag = 9
    drr_list.bezeich = "HOUSE USE"

    for segment in db_session.query(Segment).filter(
             (Segment.betriebsnr == 2)).order_by(Segment._recid).all():

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.segmentcode == segment.segmentcode) & (Genstat.datum >= fdate) & (Genstat.datum <= tdate) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():

            drr_list = query(drr_list_list, filters=(lambda drr_list: drr_list.flag == 9), first=True)

            if drr_list:

                if genstat.datum == tdate:
                    drr_list.curr_today =  to_decimal(drr_list.curr_today) + to_decimal("1")

                if get_month(genstat.datum) == get_month(tdate) and get_year(genstat.datum) == get_year(tdate):
                    drr_list.curr_mtd =  to_decimal(drr_list.curr_mtd) + to_decimal("1")


                drr_list.curr_ytd =  to_decimal(drr_list.curr_ytd) + to_decimal("1")


    drr_list = Drr_list()
    drr_list_list.append(drr_list)

    drr_list.flag = 10
    drr_list.bezeich = "VACANT ROOM"


    curr_today =  to_decimal("0")
    curr_month =  to_decimal("0")
    curr_year =  to_decimal("0")

    for bdrr in query(bdrr_list, filters=(lambda bdrr: bdrr.flag == 2 or bdrr.flag == 6), sort_by=[("flag",False)]):

        if bdrr.flag == 2:
            curr_today =  to_decimal(bdrr.curr_today)
            curr_month =  to_decimal(bdrr.curr_mtd)
            curr_year =  to_decimal(bdrr.curr_ytd)

        elif bdrr.flag == 6:
            curr_today =  to_decimal(curr_today) - to_decimal(bdrr.curr_today)
            curr_month =  to_decimal(curr_month) - to_decimal(bdrr.curr_mtd)
            curr_year =  to_decimal(curr_year) - to_decimal(bdrr.curr_ytd)

    drr_list = query(drr_list_list, filters=(lambda drr_list: drr_list.flag == 10), first=True)

    if drr_list:
        drr_list.curr_today =  to_decimal(curr_today)
        drr_list.curr_mtd =  to_decimal(curr_month)
        drr_list.curr_ytd =  to_decimal(curr_year)


    drr_list = Drr_list()
    drr_list_list.append(drr_list)

    drr_list.flag = 11
    drr_list.bezeich = "BONUS NIGHT"

    genstat_obj_list = []
    for genstat, segment in db_session.query(Genstat, Segment).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).filter(
             (Genstat.datum >= fdate) & (Genstat.datum <= tdate) & (Genstat.zipreis == 0) & (Genstat.resstatus == 6) & (Genstat.res_logic[inc_value(1)]) & (Genstat.res_logic[2])).order_by(Genstat._recid).all():
        if genstat._recid in genstat_obj_list:
            continue
        else:
            genstat_obj_list.append(genstat._recid)

        drr_list = query(drr_list_list, filters=(lambda drr_list: drr_list.flag == 11), first=True)

        if drr_list:

            if genstat.datum == tdate:
                drr_list.curr_today =  to_decimal(drr_list.curr_today) + to_decimal("1")

            if get_month(genstat.datum) == get_month(tdate) and get_year(genstat.datum) == get_year(tdate):
                drr_list.curr_mtd =  to_decimal(drr_list.curr_mtd) + to_decimal("1")


            drr_list.curr_ytd =  to_decimal(drr_list.curr_ytd) + to_decimal("1")


    drr_list = Drr_list()
    drr_list_list.append(drr_list)

    drr_list.flag = 12
    drr_list.bezeich = "ROOM SOLD"


    curr_today =  to_decimal("0")
    curr_month =  to_decimal("0")
    curr_year =  to_decimal("0")

    for bdrr in query(bdrr_list, filters=(lambda bdrr: bdrr.flag == 6 or bdrr.flag == 7 or bdrr.flag == 9), sort_by=[("flag",False)]):

        if bdrr.flag == 6:
            curr_today =  to_decimal(bdrr.curr_today)
            curr_month =  to_decimal(bdrr.curr_mtd)
            curr_year =  to_decimal(bdrr.curr_ytd)

        elif bdrr.flag == 7 or bdrr.flag == 9:
            curr_today =  to_decimal(curr_today) - to_decimal(bdrr.curr_today)
            curr_month =  to_decimal(curr_month) - to_decimal(bdrr.curr_mtd)
            curr_year =  to_decimal(curr_year) - to_decimal(bdrr.curr_ytd)

    drr_list = query(drr_list_list, filters=(lambda drr_list: drr_list.flag == 12), first=True)

    if drr_list:
        drr_list.curr_today =  to_decimal(curr_today)
        drr_list.curr_mtd =  to_decimal(curr_month)
        drr_list.curr_ytd =  to_decimal(curr_year)


    drr_list = Drr_list()
    drr_list_list.append(drr_list)

    drr_list.flag = 13
    drr_list.bezeich = "ROOM SOLD EXCLUDE BONUS NIGHT"

    bdrr = query(bdrr_list, filters=(lambda bdrr: bdrr.flag == 12), first=True)

    if bdrr:
        drr_list.curr_today =  to_decimal(drr_list.curr_today) + to_decimal(bdrr.curr_today)
        drr_list.curr_mtd =  to_decimal(drr_list.curr_mtd) + to_decimal(bdrr.curr_mtd)
        drr_list.curr_ytd =  to_decimal(drr_list.curr_ytd) + to_decimal(bdrr.curr_ytd)

    bdrr = query(bdrr_list, filters=(lambda bdrr: bdrr.flag == 11), first=True)

    if bdrr:
        drr_list.curr_today =  to_decimal(drr_list.curr_today) - to_decimal(bdrr.curr_today)
        drr_list.curr_mtd =  to_decimal(drr_list.curr_mtd) - to_decimal(bdrr.curr_mtd)
        drr_list.curr_ytd =  to_decimal(drr_list.curr_ytd) - to_decimal(bdrr.curr_ytd)


    drr_list = Drr_list()
    drr_list_list.append(drr_list)

    drr_list.flag = 14
    drr_list.bezeich = "ROOM SOLD EXCLUDE COMPLIMENT PAYING"

    bdrr = query(bdrr_list, filters=(lambda bdrr: bdrr.flag == 12), first=True)

    if bdrr:
        drr_list.curr_today =  to_decimal(drr_list.curr_today) + to_decimal(bdrr.curr_today)
        drr_list.curr_mtd =  to_decimal(drr_list.curr_mtd) + to_decimal(bdrr.curr_mtd)
        drr_list.curr_ytd =  to_decimal(drr_list.curr_ytd) + to_decimal(bdrr.curr_ytd)

    genstat_obj_list = []
    for genstat, segment in db_session.query(Genstat, Segment).join(Segment,(Segment.segmentcode == Genstat.segmentcode) & (Segment.betriebsnr != 1) & (Segment.betriebsnr != 2)).filter(
             (Genstat.datum >= fdate) & (Genstat.datum <= tdate) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)]) & (Genstat.zipreis == 0)).order_by(Genstat._recid).all():
        if genstat._recid in genstat_obj_list:
            continue
        else:
            genstat_obj_list.append(genstat._recid)

        drr_list = query(drr_list_list, filters=(lambda drr_list: drr_list.flag == 14), first=True)

        if drr_list:

            if genstat.datum == tdate:
                drr_list.curr_today =  to_decimal(drr_list.curr_today) - to_decimal("1")

            if get_month(genstat.datum) == get_month(tdate) and get_year(genstat.datum) == get_year(tdate):
                drr_list.curr_mtd =  to_decimal(drr_list.curr_mtd) - to_decimal("1")


            drr_list.curr_ytd =  to_decimal(drr_list.curr_ytd) - to_decimal("1")


    drr_list = Drr_list()
    drr_list_list.append(drr_list)

    drr_list.flag = 15
    drr_list.bezeich = "ROOM OCCUPIED EXCLUDE BN AND HU"

    bdrr = query(bdrr_list, filters=(lambda bdrr: bdrr.flag == 6), first=True)

    if bdrr:
        drr_list.curr_today =  to_decimal(drr_list.curr_today) + to_decimal(bdrr.curr_today)
        drr_list.curr_mtd =  to_decimal(drr_list.curr_mtd) + to_decimal(bdrr.curr_mtd)
        drr_list.curr_ytd =  to_decimal(drr_list.curr_ytd) + to_decimal(bdrr.curr_ytd)

    bdrr = query(bdrr_list, filters=(lambda bdrr: bdrr.flag == 11), first=True)

    if bdrr:
        drr_list.curr_today =  to_decimal(drr_list.curr_today) - to_decimal(bdrr.curr_today)
        drr_list.curr_mtd =  to_decimal(drr_list.curr_mtd) - to_decimal(bdrr.curr_mtd)
        drr_list.curr_ytd =  to_decimal(drr_list.curr_ytd) - to_decimal(bdrr.curr_ytd)

    bdrr = query(bdrr_list, filters=(lambda bdrr: bdrr.flag == 9), first=True)

    if bdrr:
        drr_list.curr_today =  to_decimal(drr_list.curr_today) - to_decimal(bdrr.curr_today)
        drr_list.curr_mtd =  to_decimal(drr_list.curr_mtd) - to_decimal(bdrr.curr_mtd)
        drr_list.curr_ytd =  to_decimal(drr_list.curr_ytd) - to_decimal(bdrr.curr_ytd)

    return generate_output()