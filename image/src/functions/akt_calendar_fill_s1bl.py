from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Akt_code, Akt_line, Guest

def akt_calendar_fill_s1bl(user_init:str, curr_month:int, curr_year:int, all_flag:bool):
    tt_s1_list = []
    tt_s2_list = []
    s1:[str] = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    s2:[str] = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    i:int = 0
    j:int = 0
    start_ind:int = 0
    anz_day:int = 0
    first_day:date = None
    last_day:date = None
    month1:int = 0
    year1:int = 0
    lname:str = ""
    akt_code = akt_line = guest = None

    tt_s1 = tt_s2 = None

    tt_s1_list, Tt_s1 = create_model("Tt_s1", {"curr_i":int, "s1":str})
    tt_s2_list, Tt_s2 = create_model("Tt_s2", {"curr_i":int, "s2":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tt_s1_list, tt_s2_list, s1, s2, i, j, start_ind, anz_day, first_day, last_day, month1, year1, lname, akt_code, akt_line, guest


        nonlocal tt_s1, tt_s2
        nonlocal tt_s1_list, tt_s2_list
        return {"tt-s1": tt_s1_list, "tt-s2": tt_s2_list}

    i = 1
    while i <= 42:
        s1[i - 1] = "  "
        s2[i - 1] = "  "
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
    last_day = date (month1, 1, year1) - 1
    i = start_ind
    j = 1
    while j <= get_day(last_day) :

        if all_flag == False:

            akt_line_obj_list = []
            for akt_line, akt_code in db_session.query(Akt_line, Akt_code).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).filter(
                    (Akt_line.flag == 0) &  (func.lower(Akt_line.userinit) == (user_init).lower()) &  (get_day(Akt_line.datum) == j) &  (get_month(Akt_line.datum) == curr_month) &  (get_year(Akt_line.datum) == curr_year)).all():
                if akt_line._recid in akt_line_obj_list:
                    continue
                else:
                    akt_line_obj_list.append(akt_line._recid)

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == akt_line.gastnr)).first()

                if guest:
                    lname = guest.name + ", " + guest.anredefirma
                s2[i - 1] = to_string(akt_code.bezeich) + chr(10) + "<" + to_string(akt_line.kontakt) + "/" + to_string(lname) + ">" + chr(10) + chr(10) + s2[i - 1]
        else:

            akt_line_obj_list = []
            for akt_line, akt_code in db_session.query(Akt_line, Akt_code).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).filter(
                    (Akt_line.flag == 0) &  (get_day(Akt_line.datum) == j) &  (get_month(Akt_line.datum) == curr_month) &  (get_year(Akt_line.datum) == curr_year)).all():
                if akt_line._recid in akt_line_obj_list:
                    continue
                else:
                    akt_line_obj_list.append(akt_line._recid)

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == akt_line.gastnr)).first()

                if guest:
                    lname = guest.name + ", " + guest.anredefirma
                s2[i - 1] = to_string(akt_code.bezeich) + chr(10) + "<" + to_string(akt_line.kontakt) + "/" + to_string(lname) + ">" + chr(10) + chr(10) + s2[i - 1]
        s1[i - 1] = to_string(j, "99")

        if subSTRING (s1[i - 1], 1, 1) == "0":
            s1[i - 1] = " " + subSTRING (s1[i - 1], 2, 1)
        i = i + 1
        j = j + 1
    for i in range(1,42 + 1) :
        tt_s1 = Tt_s1()
        tt_s1_list.append(tt_s1)

        tt_s1.curr_i = i
        tt_s1.s1 = s1[i - 1]


    for i in range(1,42 + 1) :
        tt_s2 = Tt_s2()
        tt_s2_list.append(tt_s2)

        tt_s2.curr_i = i
        tt_s2.s2 = s2[i - 1]

    return generate_output()