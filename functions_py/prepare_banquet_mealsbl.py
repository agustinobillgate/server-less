#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Bk_raum, Bk_func, Bk_setup, Ba_typ

def prepare_banquet_mealsbl(resnr:int, reslinno:int):

    prepare_cache ([Bk_raum, Bk_func, Bk_setup, Ba_typ])

    venue_list_data = []
    meal_list_data = []
    event_list_data = []
    setup_list_data = []
    menu1 = ""
    str:string = ""
    tokcounter:int = 0
    gpdelimiter:string = ";"
    mestoken:string = ""
    mesvalue:string = ""
    stringcount:int = 0
    getstring:string = ""
    bk_raum = bk_func = bk_setup = ba_typ = None

    venue_list = meal_list = event_list = setup_list = None

    venue_list_data, Venue_list = create_model("Venue_list", {"venuecode":string, "venue":string, "pax":int})
    meal_list_data, Meal_list = create_model("Meal_list", {"nr":int, "meals":string, "times":string, "venue":string, "pax":int, "setup":string})
    event_list_data, Event_list = create_model("Event_list", {"eventcode":string, "eventname":string})
    setup_list_data, Setup_list = create_model("Setup_list", {"setupcode":string, "setupname":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal venue_list_data, meal_list_data, event_list_data, setup_list_data, menu1, str, tokcounter, gpdelimiter, mestoken, mesvalue, stringcount, getstring, bk_raum, bk_func, bk_setup, ba_typ
        nonlocal resnr, reslinno


        nonlocal venue_list, meal_list, event_list, setup_list
        nonlocal venue_list_data, meal_list_data, event_list_data, setup_list_data

        return {"venue-list": venue_list_data, "meal-list": meal_list_data, "event-list": event_list_data, "setup-list": setup_list_data, "menu1": menu1}


    for bk_raum in db_session.query(Bk_raum).order_by(Bk_raum._recid).all():
        venue_list = Venue_list()
        venue_list_data.append(venue_list)

        venue_list.venuecode = bk_raum.raum
        venue_list.venue = bk_raum.bezeich
        venue_list.pax = bk_raum.personen

    bk_func = get_cache (Bk_func, {"veran_nr": [(eq, resnr)],"veran_seite": [(eq, reslinno)]})

    if bk_func:

        if num_entries(bk_func.f_menu[0], "$") > 1:
            str = entry(1, bk_func.f_menu[0], "$")
            menu1 = entry(0, bk_func.f_menu[0], "$")


    for tokcounter in range(1,num_entries(str, "|")  + 1) :
        mestoken = entry(tokcounter - 1, str, "|")
        meal_list = Meal_list()
        meal_list_data.append(meal_list)


        if mestoken != "":
            for stringcount in range(1,num_entries(mestoken, gpdelimiter)  + 1) :
                getstring = entry(stringcount - 1, mestoken, gpdelimiter)

                if getstring == "":
                    break

                if stringcount == 1:
                    meal_list.nr = to_int(getstring)
                elif stringcount == 2:
                    meal_list.meals = getstring
                elif stringcount == 3:
                    meal_list.times = getstring
                elif stringcount == 4:
                    meal_list.venue = getstring
                elif stringcount == 5:
                    meal_list.pax = to_int(getstring)
                elif stringcount == 6:
                    meal_list.setup = getstring

    for bk_setup in db_session.query(Bk_setup).order_by(Bk_setup.setup_id).all():
        setup_list = Setup_list()
        setup_list_data.append(setup_list)

        setup_list.setupcode = to_string(bk_setup.setup_id)
        setup_list.setupname = bk_setup.bezeichnung

    for ba_typ in db_session.query(Ba_typ).order_by(Ba_typ.typ_id).all():
        event_list = Event_list()
        event_list_data.append(event_list)

        event_list.eventcode = to_string(ba_typ.typ_id)
        event_list.eventname = ba_typ.bezeichnung

    return generate_output()