#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.del_gcfbl import del_gcfbl
from models import Guest, History, Guestseg

def gcfs_deletebl(deltype:int, sorttype:int, adr1:string, city:string, cntry:string, email:string, last_stay:date, min_sales:Decimal, age_history:int):
    f_anz = 0
    d_anz = 0
    error_code:int = 0
    last_history:date = None
    guest = history = guestseg = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_anz, d_anz, error_code, last_history, guest, history, guestseg
        nonlocal deltype, sorttype, adr1, city, cntry, email, last_stay, min_sales, age_history

        return {"f_anz": f_anz, "d_anz": d_anz}

    def del_deltype1():

        nonlocal f_anz, d_anz, error_code, last_history, guest, history, guestseg
        nonlocal deltype, sorttype, adr1, city, cntry, email, last_stay, min_sales, age_history

        i:int = 0
        do_it:bool = False

        for guest in db_session.query(Guest).filter(
                 (Guest.karteityp == sorttype) & (Guest.gastnr > 0)).order_by(Guest._recid).all():
            f_anz = f_anz + 1
            do_it = True

            if do_it and (adr1).lower()  != "" and guest.adresse1.lower()  != (adr1).lower() :
                do_it = False

            if do_it and (city).lower()  != "" and guest.wohnort.lower()  != (city).lower() :
                do_it = False

            if do_it and (cntry).lower()  != "" and guest.land.lower()  != (cntry).lower() :
                do_it = False

            if do_it and (email).lower()  != "" and guest.email_adr.lower()  != (email).lower() :
                do_it = False

            if do_it and guest.date2 > last_stay:
                do_it = False

            if do_it and guest.gesamtumsatz > min_sales:
                do_it = False

            if do_it and age_history > 0:

                for history in db_session.query(History).filter(
                         (History.gastnr == guest.gastnr)).order_by(History.abreise.desc()).yield_per(100):

                    if history.abreise > (get_current_date() - age_history * 365):
                        do_it = False
                    break

            if do_it:
                error_code = get_output(del_gcfbl(guest.gastnr))

                if error_code == 0:
                    d_anz = d_anz + 1

        return


    def del_deltype2():

        nonlocal f_anz, d_anz, error_code, last_history, guest, history, guestseg
        nonlocal deltype, sorttype, adr1, city, cntry, email, last_stay, min_sales, age_history

        i:int = 0
        do_it:bool = False

        for guest in db_session.query(Guest).filter(
                 (Guest.karteityp == sorttype) & (Guest.gastnr > 0)).order_by(Guest._recid).all():
            f_anz = f_anz + 1
            do_it = True

            history = get_cache (History, {"gastnr": [(eq, guest.gastnr)]})
            do_it = not None != history

            if do_it and (adr1).lower()  != "" and guest.adresse1.lower()  != (adr1).lower() :
                do_it = False

            if do_it and (city).lower()  != "" and guest.wohnort.lower()  != (city).lower() :
                do_it = False

            if do_it and (cntry).lower()  != "" and guest.land.lower()  != (cntry).lower() :
                do_it = False

            if do_it and (email).lower()  != "" and guest.email_adr.lower()  != (email).lower() :
                do_it = False

            if do_it and guest.date2 > last_stay:
                do_it = False

            if do_it and guest.gesamtumsatz > min_sales:
                do_it = False

            if do_it:
                error_code = get_output(del_gcfbl(guest.gastnr))

                if error_code == 0:
                    d_anz = d_anz + 1

        return


    def del_deltype3():

        nonlocal f_anz, d_anz, error_code, last_history, guest, history, guestseg
        nonlocal deltype, sorttype, adr1, city, cntry, email, last_stay, min_sales, age_history

        i:int = 0
        do_it:bool = False

        for guest in db_session.query(Guest).filter(
                 (Guest.karteityp == sorttype) & (Guest.gastnr > 0)).order_by(Guest._recid).all():
            f_anz = f_anz + 1
            do_it = True

            guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)]})
            do_it = not None != guestseg

            if do_it and (adr1).lower()  != "" and guest.adresse1.lower()  != (adr1).lower() :
                do_it = False

            if do_it and (city).lower()  != "" and guest.wohnort.lower()  != (city).lower() :
                do_it = False

            if do_it and (cntry).lower()  != "" and guest.land.lower()  != (cntry).lower() :
                do_it = False

            if do_it and (email).lower()  != "" and guest.email_adr.lower()  != (email).lower() :
                do_it = False

            if do_it and guest.date2 > last_stay:
                do_it = False

            if do_it and guest.gesamtumsatz > min_sales:
                do_it = False

            if do_it and age_history > 0:

                for history in db_session.query(History).filter(
                         (History.gastnr == guest.gastnr)).order_by(History.abreise.desc()).yield_per(100):

                    if history.abreise > (get_current_date() - age_history * 365):
                        do_it = False
                    break

            if do_it:
                error_code = get_output(del_gcfbl(guest.gastnr))

                if error_code == 0:
                    d_anz = d_anz + 1

        return


    def del_deltype4():

        nonlocal f_anz, d_anz, error_code, last_history, guest, history, guestseg
        nonlocal deltype, sorttype, adr1, city, cntry, email, last_stay, min_sales, age_history

        hbuff = None
        Hbuff =  create_buffer("Hbuff",History)
        last_history = date_mdy(get_month(get_current_date()) , get_day(get_current_date()) , (get_year(get_current_date()) - timedelta(days=age_history)))

        history = get_cache (History, {"gastnr": [(gt, 0)],"abreise": [(lt, last_history)]})
        while None != history:
            f_anz = f_anz + 1

            guest = get_cache (Guest, {"gastnr": [(eq, history.gastnr)]})

            if guest and guest.karteityp == sorttype:

                hbuff = db_session.query(Hbuff).filter(
                         (Hbuff._recid == history._recid)).first()
                db_session.delete(hbuff)
                pass
                d_anz = d_anz + 1

        return

    if deltype == 1:
        del_deltype1()

    elif deltype == 2:
        del_deltype2()

    elif deltype == 3:
        del_deltype3()

    elif deltype == 4:
        del_deltype4()

    return generate_output()