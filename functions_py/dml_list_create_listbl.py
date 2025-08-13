#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd 13/8/2025
# num_entries
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Reslin_queasy, Hoteldpt, Dml_art, Dml_artdep

def dml_list_create_listbl(curr_dept:int, selected_date:date):

    prepare_cache ([Reslin_queasy, Hoteldpt, Dml_art, Dml_artdep])

    dml_list_data = []
    nr:int = 1
    reslin_queasy = hoteldpt = dml_art = dml_artdep = None

    dml_list = rqueasy = None

    dml_list_data, Dml_list = create_model("Dml_list", {"counter":int, "dml_nr":string, "dept":string, "id":string, "approved":bool})

    Rqueasy = create_buffer("Rqueasy",Reslin_queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal dml_list_data, nr, reslin_queasy, hoteldpt, dml_art, dml_artdep
        nonlocal curr_dept, selected_date
        nonlocal rqueasy


        nonlocal dml_list, rqueasy
        nonlocal dml_list_data

        return {"dml-list": dml_list_data}

    reslin_queasy = db_session.query(Reslin_queasy).filter(
             (Reslin_queasy.key == ("DML").lower()) & (Reslin_queasy.date1 == selected_date) & (to_int(entry(1, Reslin_queasy.char1, ";")) == curr_dept)).first()

    if reslin_queasy:

        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})

        if curr_dept == 0:
            # Rd 13/8/2025
            # dml_art = db_session.query(Dml_art).filter(
            #          (Dml_art.datum == selected_date) & (num_entries(Dml_art.chginit, ";") > 1) & (entry(1, Dml_art.chginit, ";") != "")).first()
            dml_art = db_session.query(Dml_art).filter(
                     (Dml_art.datum == selected_date) & 
                     
                     (entry(1, Dml_art.chginit, ";") != "")).first()
            if (num_entries(dml_art.chginit, ";") > 1):
                if not dml_art:

                    dml_art = get_cache (Dml_art, {"datum": [(eq, selected_date)]})

                if dml_art:
                    dml_list = Dml_list()
                    dml_list_data.append(dml_list)

                    counter = 1
                    dept = hoteldpt.depart
                    id = dml_art.userinit

                    if num_entries(dml_art.chginit, ";") > 1:
                        dml_nr = entry(1, dml_art.chginit, ";")
                    else:
                        dml_nr = ""

                    if matches(dml_art.chginit,r"*!*"):
                        approved = True
                    else:
                        approved = False
        else:
            # Rd 13/8/2025
            # dml_artdep = db_session.query(Dml_artdep).filter(
            #          (Dml_artdep.datum == selected_date) & (Dml_artdep.departement == curr_dept) & (num_entries(Dml_artdep.chginit, ";") > 1) & (entry(1, Dml_artdep.chginit, ";") != "") & (Dml_artdep.anzahl > 0)).first()
            dml_artdep = db_session.query(Dml_artdep).filter(
                     (Dml_artdep.datum == selected_date) & 
                     (Dml_artdep.departement == curr_dept) & 
                     (entry(1, Dml_artdep.chginit, ";") != "") & (Dml_artdep.anzahl > 0)).first()
            if (num_entries(dml_artdep.chginit, ";") > 1):
                if not dml_artdep:

                    dml_artdep = get_cache (Dml_artdep, {"datum": [(eq, selected_date)],"departement": [(eq, curr_dept)],"anzahl": [(gt, 0)]})

                if dml_artdep:
                    dml_list = Dml_list()
                    dml_list_data.append(dml_list)

                    counter = 1
                    dept = hoteldpt.depart
                    id = dml_artdep.userinit

                    if num_entries(dml_artdep.chginit, ";") > 1:
                        dml_nr = entry(1, dml_artdep.chginit, ";")
                    else:
                        dml_nr = ""

                    if matches(dml_artdep.chginit,r"*!*"):
                        approved = True
                    else:
                        approved = False

        for rqueasy in db_session.query(Rqueasy).filter(
                 (Rqueasy.key == ("DML").lower()) & (Rqueasy.date1 == selected_date) & (to_int(entry(1, Rqueasy.char1, ";")) == curr_dept)).order_by(Rqueasy._recid).all():

            if rqueasy.number2 != nr:
                nr = rqueasy.number2
                dml_list = Dml_list()
                dml_list_data.append(dml_list)

                counter = rqueasy.number2
                dml_nr = entry(1, rqueasy.char3, ";")
                dept = hoteldpt.depart
                id = rqueasy.char2

                if matches(rqueasy.char3,r"*!*"):
                    approved = True
                else:
                    approved = False

    return generate_output()