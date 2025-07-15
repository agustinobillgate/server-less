#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Akt_code, Akt_line, Guest

def akt_calendar_fill_s1bl(user_init:string, curr_month:int, curr_year:int, all_flag:bool):

    prepare_cache ([Akt_code, Akt_line, Guest])

    tt_s1_data = []
    tt_s2_data = []
    s1:List[string] = create_empty_list(42,"")
    s2:List[string] = create_empty_list(42,"")
    i:int = 0
    j:int = 0
    start_ind:int = 0
    anz_day:int = 0
    first_day:date = None
    last_day:date = None
    month1:int = 0
    year1:int = 0
    lname:string = ""
    akt_code = akt_line = guest = None

    tt_s1 = tt_s2 = None

    tt_s1_data, Tt_s1 = create_model("Tt_s1", {"curr_i":int, "s1":string})
    tt_s2_data, Tt_s2 = create_model("Tt_s2", {"curr_i":int, "s2":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tt_s1_data, tt_s2_data, s1, s2, i, j, start_ind, anz_day, first_day, last_day, month1, year1, lname, akt_code, akt_line, guest
        nonlocal user_init, curr_month, curr_year, all_flag


        nonlocal tt_s1, tt_s2
        nonlocal tt_s1_data, tt_s2_data

        return {"tt-s1": tt_s1_data, "tt-s2": tt_s2_data}

    i = 1
    while i <= 42:
        s1[i - 1] = " "
        s2[i - 1] = " "
        i = i + 1
    first_day = date (curr_month, 1, curr_year)
    start_ind = get_weekday(first_day) - 1

    if start_ind == 0:
        start_ind = 7
    month1 = curr_month + 1
    year1 = curr_year

    if month1 == 13:
        month1 = 1
        year1 = year1 + 1
    last_day = date (month1, 1, year1) - timedelta(days=1)
    i = start_ind
    j = 1
    while j <= get_day(last_day) :

        if all_flag == False:

            akt_line_obj_list = {}
            akt_line = Akt_line()
            akt_code = Akt_code()
            for akt_line.gastnr, akt_line.kontakt, akt_line._recid, akt_code.bezeich, akt_code._recid in db_session.query(Akt_line.gastnr, Akt_line.kontakt, Akt_line._recid, Akt_code.bezeich, Akt_code._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).filter(
                     (Akt_line.flag == 0) & (Akt_line.userinit == (user_init).lower()) & (get_day(Akt_line.datum) == j) & (get_month(Akt_line.datum) == curr_month) & (get_year(Akt_line.datum) == curr_year)).order_by(Akt_line._recid).all():
                if akt_line_obj_list.get(akt_line._recid):
                    continue
                else:
                    akt_line_obj_list[akt_line._recid] = True

                guest = get_cache (Guest, {"gastnr": [(eq, akt_line.gastnr)]})

                if guest:
                    lname = guest.name + ", " + guest.anredefirma
                s2[i - 1] = to_string(akt_code.bezeich) + chr_unicode(10) + "<" + to_string(akt_line.kontakt) + "/" + to_string(lname) + ">" + chr_unicode(10) + chr_unicode(10) + s2[i - 1]
        else:

            akt_line_obj_list = {}
            akt_line = Akt_line()
            akt_code = Akt_code()
            for akt_line.gastnr, akt_line.kontakt, akt_line._recid, akt_code.bezeich, akt_code._recid in db_session.query(Akt_line.gastnr, Akt_line.kontakt, Akt_line._recid, Akt_code.bezeich, Akt_code._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).filter(
                     (Akt_line.flag == 0) & (get_day(Akt_line.datum) == j) & (get_month(Akt_line.datum) == curr_month) & (get_year(Akt_line.datum) == curr_year)).order_by(Akt_line._recid).all():
                if akt_line_obj_list.get(akt_line._recid):
                    continue
                else:
                    akt_line_obj_list[akt_line._recid] = True

                guest = get_cache (Guest, {"gastnr": [(eq, akt_line.gastnr)]})

                if guest:
                    lname = guest.name + ", " + guest.anredefirma
                s2[i - 1] = to_string(akt_code.bezeich) + chr_unicode(10) + "<" + to_string(akt_line.kontakt) + "/" + to_string(lname) + ">" + chr_unicode(10) + chr_unicode(10) + s2[i - 1]
        s1[i - 1] = to_string(j, "99")

        if subSTRING (s1[i - 1], 1, 1) == ("0").lower() :
            s1[i - 1] = " " + subSTRING (s1[i - 1], 2, 1)
        i = i + 1
        j = j + 1
    for i in range(1,42 + 1) :
        tt_s1 = Tt_s1()
        tt_s1_data.append(tt_s1)

        tt_s1.curr_i = i
        tt_s1.s1 = s1[i - 1]


    for i in range(1,42 + 1) :
        tt_s2 = Tt_s2()
        tt_s2_data.append(tt_s2)

        tt_s2.curr_i = i
        tt_s2.s2 = s2[i - 1]

    return generate_output()