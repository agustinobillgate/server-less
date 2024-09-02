from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Segment, Segmentstat

def segmstat_1_listbl(from_date:date, to_date:date):
    segmstat_list_list = []
    black_list:int = 0
    price_decimal:int = 0
    room:int = 0
    person:int = 0
    broom:int = 0
    bperson:int = 0
    proz1:decimal = 0
    proz2:decimal = 0
    proz3:decimal = 0
    lodging:decimal = 0
    blodging:decimal = 0
    t_room:int = 0
    t_broom:decimal = 0
    t_person:int = 0
    t_bperson:decimal = 0
    t_lodging:decimal = 0
    t_blodging:decimal = 0
    htparam = segment = segmentstat = None

    segmstat_list = t_segmstat_list = None

    segmstat_list_list, Segmstat_list = create_model("Segmstat_list", {"segmentcode":int, "descrip":str, "room":int, "budget":int, "percent":str, "g_room":int, "g_budget":int, "g_percent":str, "t_room":decimal, "t_budget":decimal, "t_percent":str, "room_ytd":int, "budget_ytd":int, "percent_ytd":str, "g_room_ytd":int, "g_budget_ytd":int, "g_percent_ytd":str, "t_room_ytd":decimal, "t_budget_ytd":decimal, "t_percent_ytd":str})
    t_segmstat_list_list, T_segmstat_list = create_model("T_segmstat_list", {"descrip":str, "room_ytd":int, "budget_ytd":int, "percent_ytd":str, "g_room_ytd":int, "g_budget_ytd":int, "g_percent_ytd":str, "t_room_ytd":decimal, "t_budget_ytd":decimal, "t_percent_ytd":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal segmstat_list_list, black_list, price_decimal, room, person, broom, bperson, proz1, proz2, proz3, lodging, blodging, t_room, t_broom, t_person, t_bperson, t_lodging, t_blodging, htparam, segment, segmentstat


        nonlocal segmstat_list, t_segmstat_list
        nonlocal segmstat_list_list, t_segmstat_list_list
        return {"segmstat-list": segmstat_list_list}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 709)).first()
    black_list = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    for segment in db_session.query(Segment).filter(
            (Segmentcode != black_list) &  (not Segment.bezeich.op("~")(".*\$\$0.*"))).all():
        room = 0
        person = 0
        broom = 0
        bperson = 0
        lodging = 0
        blodging = 0
        proz1 = 0
        proz2 = 0
        proz3 = 0
        segmstat_list = Segmstat_list()
        segmstat_list_list.append(segmstat_list)

        segmstat_list.segmentcode = segmentcode
        segmstat_list.descrip = to_string(segmentcode, ">>9") + " - " + to_string(entry(0, segment.bezeich, "$$0") , "x(21)")

        for segmentstat in db_session.query(Segmentstat).filter(
                (Segmentstat.segmentcode == segmentcode) &  (Segmentstat.datum >= from_date) &  (Segmentstat.datum <= to_date)).all():
            t_room = t_room + segmentstat.zimmeranz
            t_broom = t_broom + segmentstat.budzimmeranz
            t_person = t_person + segmentstat.persanz +\
                    segmentstat.kind1 + segmentstat.kind2 +\
                    segmentstat.gratis
            t_bperson = t_bperson + segmentstat.budpersanz
            t_lodging = t_lodging + segmentstat.logis
            t_blodging = t_blodging + segmentstat.budlogis
            room = room + segmentstat.zimmeranz
            person = person + segmentstat.persanz +\
                    segmentstat.kind1 + segmentstat.kind2 +\
                    segmentstat.gratis
            broom = broom + segmentstat.budzimmeranz
            bperson = bperson + segmentstat.budpersanz
            lodging = lodging + segmentstat.logis
            blodging = blodging + segmentstat.budlogis

        if broom != 0:
            proz1 = room / broom * 100

        if bperson != 0:
            proz2 = person / bperson * 100

        if blodging != 0:
            proz3 = lodging / blodging * 100
        segmstat_list.room = room
        segmstat_list.budget = broom
        segmstat_list.g_room = person
        segmstat_list.g_budget = bperson


        segmstat_list.t_room = lodging
        segmstat_list.t_budget = blodging
        segmstat_list.percent = to_string(proz1, ">,>>9.99")
        segmstat_list.g_percent = to_string(proz2, ">,>>9.99")
        segmstat_list.t_percent = to_string(proz3, ">,>>9.99")


    segmstat_list = Segmstat_list()
    segmstat_list_list.append(segmstat_list)

    segmstat_list.descrip = "T O T A L"
    segmstat_list.room = t_room
    segmstat_list.budget = t_broom
    segmstat_list.percent = ""
    segmstat_list.g_room = t_person
    segmstat_list.g_budget = t_bperson
    segmstat_list.g_percent = ""
    segmstat_list.t_percent = ""


    segmstat_list.t_room = t_lodging
    segmstat_list.t_budget = t_blodging


    t_room = 0
    t_broom = 0
    t_person = 0
    t_bperson = 0
    t_lodging = 0
    t_blodging = 0

    for segment in db_session.query(Segment).filter(
            (Segmentcode != black_list)).all():
        t_segmstat_list = T_segmstat_list()
        t_segmstat_list_list.append(t_segmstat_list)

        room = 0
        person = 0
        broom = 0
        bperson = 0
        lodging = 0
        blodging = 0
        proz1 = 0
        proz2 = 0
        proz3 = 0
        t_segmstat_list.descrip = to_string(segmentcode, ">>9") + " - " + to_string(entry(0, segment.bezeich, "$$0") , "x(21)")
        from_date = date_mdy(1, 1, get_year(to_date))

        for segmentstat in db_session.query(Segmentstat).filter(
                (Segmentstat.segmentcode == segmentcode) &  (Segmentstat.datum >= from_date) &  (Segmentstat.datum <= to_date)).all():
            t_room = t_room + segmentstat.zimmeranz
            t_broom = t_broom + segmentstat.budzimmeranz
            t_person = t_person + segmentstat.persanz +\
                    segmentstat.kind1 + segmentstat.kind2 +\
                    segmentstat.gratis
            t_bperson = t_bperson + segmentstat.budpersanz
            t_lodging = t_lodging + segmentstat.logis
            t_blodging = t_blodging + segmentstat.budlogis
            room = room + segmentstat.zimmeranz
            person = person + segmentstat.persanz +\
                    segmentstat.kind1 + segmentstat.kind2 +\
                    segmentstat.gratis
            broom = broom + segmentstat.budzimmeranz
            bperson = bperson + segmentstat.budpersanz
            lodging = lodging + segmentstat.logis
            blodging = blodging + segmentstat.budlogis

        if broom != 0:
            proz1 = room / broom * 100

        if bperson != 0:
            proz2 = person / bperson * 100

        if blodging != 0:
            proz3 = lodging / blodging * 100
        t_segmstat_list.room_ytd = room
        t_segmstat_list.budget_ytd = broom
        t_segmstat_list.g_room_ytd = person
        t_segmstat_list.g_budget_ytd = bperson


        t_segmstat_list.t_room_ytd = lodging
        t_segmstat_list.t_budget_ytd = blodging
        t_segmstat_list.percent_ytd = to_string(proz1, ">>>9.99")
        t_segmstat_list.t_percent_ytd = to_string(proz2, ">>>9.99")
        t_segmstat_list.g_percent_ytd = to_string(proz3, ">>>9.99")


    t_segmstat_list = T_segmstat_list()
    t_segmstat_list_list.append(t_segmstat_list)

    t_segmstat_list.descrip = "T O T A L"
    t_segmstat_list.room_ytd = t_room
    t_segmstat_list.budget_ytd = t_broom
    t_segmstat_list.percent_ytd = ""
    t_segmstat_list.g_room_ytd = t_person
    t_segmstat_list.g_budget_ytd = t_bperson
    t_segmstat_list.g_percent_ytd = ""
    t_segmstat_list.t_percent_ytd = ""


    t_segmstat_list.t_room_ytd = t_lodging
    t_segmstat_list.t_budget_ytd = t_blodging

    for t_segmstat_list in query(t_segmstat_list_list):
        segmstat_list = db_session.query(Segmstat_list).filter((Segmstat_list.descrip == t_Segmstat_list.descrip)).first()
        if not segmstat_list:
            continue

        segmstat_list.room_ytd = t_segmstat_list.room_ytd
        segmstat_list.budget_ytd = t_segmstat_list.budget_ytd
        segmstat_list.percent_ytd = t_segmstat_list.percent_ytd
        segmstat_list.g_room_ytd = t_segmstat_list.g_room_ytd
        segmstat_list.g_budget_ytd = t_segmstat_list.g_budget_ytd
        segmstat_list.g_percent_ytd = t_segmstat_list.g_percent_ytd
        segmstat_list.t_percent_ytd = t_segmstat_list.t_percent_ytd
        segmstat_list.t_room_ytd = t_segmstat_list.t_room_ytd
        segmstat_list.t_budget_ytd = t_segmstat_list.t_budget_ytd

    return generate_output()