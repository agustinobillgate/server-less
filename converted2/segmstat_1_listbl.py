#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Segment, Segmentstat

def segmstat_1_listbl(from_date:date, to_date:date):

    prepare_cache ([Htparam, Segment, Segmentstat])

    segmstat_list_data = []
    black_list:int = 0
    price_decimal:int = 0
    room:int = 0
    person:int = 0
    broom:int = 0
    bperson:int = 0
    proz1:Decimal = to_decimal("0.0")
    proz2:Decimal = to_decimal("0.0")
    proz3:Decimal = to_decimal("0.0")
    lodging:Decimal = to_decimal("0.0")
    blodging:Decimal = to_decimal("0.0")
    t_room:int = 0
    t_broom:Decimal = to_decimal("0.0")
    t_person:int = 0
    t_bperson:Decimal = to_decimal("0.0")
    t_lodging:Decimal = to_decimal("0.0")
    t_blodging:Decimal = to_decimal("0.0")
    htparam = segment = segmentstat = None

    segmstat_list = t_segmstat_list = None

    segmstat_list_data, Segmstat_list = create_model("Segmstat_list", {"segmentcode":int, "descrip":string, "room":int, "budget":int, "percent":string, "g_room":int, "g_budget":int, "g_percent":string, "t_room":Decimal, "t_budget":Decimal, "t_percent":string, "room_ytd":int, "budget_ytd":int, "percent_ytd":string, "g_room_ytd":int, "g_budget_ytd":int, "g_percent_ytd":string, "t_room_ytd":Decimal, "t_budget_ytd":Decimal, "t_percent_ytd":string})
    t_segmstat_list_data, T_segmstat_list = create_model("T_segmstat_list", {"descrip":string, "room_ytd":int, "budget_ytd":int, "percent_ytd":string, "g_room_ytd":int, "g_budget_ytd":int, "g_percent_ytd":string, "t_room_ytd":Decimal, "t_budget_ytd":Decimal, "t_percent_ytd":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal segmstat_list_data, black_list, price_decimal, room, person, broom, bperson, proz1, proz2, proz3, lodging, blodging, t_room, t_broom, t_person, t_bperson, t_lodging, t_blodging, htparam, segment, segmentstat
        nonlocal from_date, to_date


        nonlocal segmstat_list, t_segmstat_list
        nonlocal segmstat_list_data, t_segmstat_list_data

        return {"segmstat-list": segmstat_list_data}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 709)]})
    black_list = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    for segment in db_session.query(Segment).filter(
             (Segment.segmentcode != black_list) & (not_(matches(Segment.bezeich,("*$$0*"))))).order_by(Segment.segmentcode).all():
        room = 0
        person = 0
        broom = 0
        bperson = 0
        lodging =  to_decimal("0")
        blodging =  to_decimal("0")
        proz1 =  to_decimal("0")
        proz2 =  to_decimal("0")
        proz3 =  to_decimal("0")
        segmstat_list = Segmstat_list()
        segmstat_list_data.append(segmstat_list)

        segmstat_list.segmentcode = segment.segmentcode
        segmstat_list.descrip = to_string(segment.segmentcode, ">>9") + " - " + to_string(entry(0, segment.bezeich, "$$0") , "x(21)")

        for segmentstat in db_session.query(Segmentstat).filter(
                 (Segmentstat.segmentcode == segment.segmentcode) & (Segmentstat.datum >= from_date) & (Segmentstat.datum <= to_date)).order_by(Segmentstat._recid).all():
            t_room = t_room + segmentstat.zimmeranz
            t_broom =  to_decimal(t_broom) + to_decimal(segmentstat.budzimmeranz)
            t_person = t_person + segmentstat.persanz +\
                    segmentstat.kind1 + segmentstat.kind2 +\
                    segmentstat.gratis
            t_bperson =  to_decimal(t_bperson) + to_decimal(segmentstat.budpersanz)
            t_lodging =  to_decimal(t_lodging) + to_decimal(segmentstat.logis)
            t_blodging =  to_decimal(t_blodging) + to_decimal(segmentstat.budlogis)
            room = room + segmentstat.zimmeranz
            person = person + segmentstat.persanz +\
                    segmentstat.kind1 + segmentstat.kind2 +\
                    segmentstat.gratis
            broom = broom + segmentstat.budzimmeranz
            bperson = bperson + segmentstat.budpersanz
            lodging =  to_decimal(lodging) + to_decimal(segmentstat.logis)
            blodging =  to_decimal(blodging) + to_decimal(segmentstat.budlogis)

        if broom != 0:
            proz1 =  to_decimal(room) / to_decimal(broom) * to_decimal("100")

        if bperson != 0:
            proz2 =  to_decimal(person) / to_decimal(bperson) * to_decimal("100")

        if blodging != 0:
            proz3 =  to_decimal(lodging) / to_decimal(blodging) * to_decimal("100")
        segmstat_list.room = room
        segmstat_list.budget = broom
        segmstat_list.g_room = person
        segmstat_list.g_budget = bperson


        segmstat_list.t_room =  to_decimal(lodging)
        segmstat_list.t_budget =  to_decimal(blodging)
        segmstat_list.percent = to_string(proz1, ">,>>9.99")
        segmstat_list.g_percent = to_string(proz2, ">,>>9.99")
        segmstat_list.t_percent = to_string(proz3, ">,>>9.99")


    segmstat_list = Segmstat_list()
    segmstat_list_data.append(segmstat_list)

    segmstat_list.descrip = "T O T A L"
    segmstat_list.room = t_room
    segmstat_list.budget = t_broom
    segmstat_list.percent = ""
    segmstat_list.g_room = t_person
    segmstat_list.g_budget = t_bperson
    segmstat_list.g_percent = ""
    segmstat_list.t_percent = ""


    segmstat_list.t_room =  to_decimal(t_lodging)
    segmstat_list.t_budget =  to_decimal(t_blodging)


    t_room = 0
    t_broom =  to_decimal("0")
    t_person = 0
    t_bperson =  to_decimal("0")
    t_lodging =  to_decimal("0")
    t_blodging =  to_decimal("0")

    for segment in db_session.query(Segment).filter(
             (Segment.segmentcode != black_list)).order_by(Segment.segmentcode).all():
        t_segmstat_list = T_segmstat_list()
        t_segmstat_list_data.append(t_segmstat_list)

        room = 0
        person = 0
        broom = 0
        bperson = 0
        lodging =  to_decimal("0")
        blodging =  to_decimal("0")
        proz1 =  to_decimal("0")
        proz2 =  to_decimal("0")
        proz3 =  to_decimal("0")
        t_segmstat_list.descrip = to_string(segment.segmentcode, ">>9") + " - " + to_string(entry(0, segment.bezeich, "$$0") , "x(21)")
        from_date = date_mdy(1, 1, get_year(to_date))

        for segmentstat in db_session.query(Segmentstat).filter(
                 (Segmentstat.segmentcode == segment.segmentcode) & (Segmentstat.datum >= from_date) & (Segmentstat.datum <= to_date)).order_by(Segmentstat._recid).all():
            t_room = t_room + segmentstat.zimmeranz
            t_broom =  to_decimal(t_broom) + to_decimal(segmentstat.budzimmeranz)
            t_person = t_person + segmentstat.persanz +\
                    segmentstat.kind1 + segmentstat.kind2 +\
                    segmentstat.gratis
            t_bperson =  to_decimal(t_bperson) + to_decimal(segmentstat.budpersanz)
            t_lodging =  to_decimal(t_lodging) + to_decimal(segmentstat.logis)
            t_blodging =  to_decimal(t_blodging) + to_decimal(segmentstat.budlogis)
            room = room + segmentstat.zimmeranz
            person = person + segmentstat.persanz +\
                    segmentstat.kind1 + segmentstat.kind2 +\
                    segmentstat.gratis
            broom = broom + segmentstat.budzimmeranz
            bperson = bperson + segmentstat.budpersanz
            lodging =  to_decimal(lodging) + to_decimal(segmentstat.logis)
            blodging =  to_decimal(blodging) + to_decimal(segmentstat.budlogis)

        if broom != 0:
            proz1 =  to_decimal(room) / to_decimal(broom) * to_decimal("100")

        if bperson != 0:
            proz2 =  to_decimal(person) / to_decimal(bperson) * to_decimal("100")

        if blodging != 0:
            proz3 =  to_decimal(lodging) / to_decimal(blodging) * to_decimal("100")
        t_segmstat_list.room_ytd = room
        t_segmstat_list.budget_ytd = broom
        t_segmstat_list.g_room_ytd = person
        t_segmstat_list.g_budget_ytd = bperson


        t_segmstat_list.t_room_ytd =  to_decimal(lodging)
        t_segmstat_list.t_budget_ytd =  to_decimal(blodging)
        t_segmstat_list.percent_ytd = to_string(proz1, ">>>9.99")
        t_segmstat_list.t_percent_ytd = to_string(proz2, ">>>9.99")
        t_segmstat_list.g_percent_ytd = to_string(proz3, ">>>9.99")


    t_segmstat_list = T_segmstat_list()
    t_segmstat_list_data.append(t_segmstat_list)

    t_segmstat_list.descrip = "T O T A L"
    t_segmstat_list.room_ytd = t_room
    t_segmstat_list.budget_ytd = t_broom
    t_segmstat_list.percent_ytd = ""
    t_segmstat_list.g_room_ytd = t_person
    t_segmstat_list.g_budget_ytd = t_bperson
    t_segmstat_list.g_percent_ytd = ""
    t_segmstat_list.t_percent_ytd = ""


    t_segmstat_list.t_room_ytd =  to_decimal(t_lodging)
    t_segmstat_list.t_budget_ytd =  to_decimal(t_blodging)

    for t_segmstat_list in query(t_segmstat_list_data):
        segmstat_list = query(segmstat_list_data, (lambda segmstat_list: segmstat_list.descrip == t_segmstat_list.descrip), first=True)
        if not segmstat_list:
            continue

        segmstat_list.room_ytd = t_segmstat_list.room_ytd
        segmstat_list.budget_ytd = t_segmstat_list.budget_ytd
        segmstat_list.percent_ytd = t_segmstat_list.percent_ytd
        segmstat_list.g_room_ytd = t_segmstat_list.g_room_ytd
        segmstat_list.g_budget_ytd = t_segmstat_list.g_budget_ytd
        segmstat_list.g_percent_ytd = t_segmstat_list.g_percent_ytd
        segmstat_list.t_percent_ytd = t_segmstat_list.t_percent_ytd
        segmstat_list.t_room_ytd =  to_decimal(t_segmstat_list.t_room_ytd)
        segmstat_list.t_budget_ytd =  to_decimal(t_segmstat_list.t_budget_ytd)

    return generate_output()