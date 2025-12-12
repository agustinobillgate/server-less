#using conversion tools version: 1.0.0.117

#------------------------------------------
# Rulita, 19/08/2025
# New Compile program IF Invinity IPTV
# ticket: 9DAA21

# Rulita, 10-12-2025
# - Added with_for_update before delete query
#--------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Interface, Res_line, Reservation, Guest, History

def if_infiniti_tv_1bl():

    prepare_cache ([Res_line, Guest, History])

    t_guest_data = []
    gastnr_ind:int = 0
    gastnr_wi:int = 0
    interface = res_line = reservation = guest = history = None

    t_guest = t_interface = bufflist = None

    t_guest_data, T_guest = create_model("T_guest", {"firstname":string, "lastname":string, "guesttitle":string, "ci_date":date, "ci_time":int, "co_date":date, "co_time":int, "ci_status":string, "gender":string, "roomnr":string, "oldroomnr":string, "resid":string, "irecid":int, "itype":string, "update_date":string, "update_time":string, "parameters":string, "birthday":string, "telefon":string, "email_adr":string, "gdpr_flag":string})

    T_interface = create_buffer("T_interface",Interface)
    Bufflist = T_guest
    bufflist_data = t_guest_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_guest_data, gastnr_ind, gastnr_wi, interface, res_line, reservation, guest, history
        nonlocal t_interface, bufflist


        nonlocal t_guest, t_interface, bufflist
        nonlocal t_guest_data

        return {"t-guest": t_guest_data}

    def update_tguest(create_flag:bool):

        nonlocal t_guest_data, gastnr_ind, gastnr_wi, interface, res_line, reservation, guest, history
        nonlocal t_interface, bufflist


        nonlocal t_guest, t_interface, bufflist
        nonlocal t_guest_data

        res_line = get_cache (Res_line, {"resnr": [(eq, interface.resnr)],"reslinnr": [(eq, interface.reslinnr)]})

        if res_line:

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

            if guest:

                if create_flag:
                    t_guest = T_guest()
                    t_guest_data.append(t_guest)

                t_guest.parameters = interface.parameters
                t_guest.firstname = guest.vorname1
                t_guest.lastname = guest.name
                t_guest.guesttitle = guest.anrede1
                t_guest.ci_status = "true"
                t_guest.email_adr = to_string(guest.email_adr)

                if (guest.geschlecht.lower()  == ("M").lower()  or guest.geschlecht.lower()  == ("Male").lower()):
                    t_guest.gender = "male"

                elif (guest.geschlecht.lower()  == ("F").lower()  or guest.geschlecht.lower()  == ("Female").lower()):
                    t_guest.gender = "female"

                if to_string(guest.mobil_telefon) != "":
                    t_guest.telefon = to_string(guest.mobil_telefon)
                else:
                    t_guest.telefon = to_string(guest.telefon)
                t_guest.ci_date = res_line.ankunft
                t_guest.ci_time = res_line.ankzeit
                t_guest.co_date = res_line.abreise
                t_guest.co_time = res_line.abreisezeit
                t_guest.resid = to_string(interface.resnr) + to_string(interface.reslinnr)
                t_guest.irecid = interface._recid
                t_guest.roomnr = interface.zinr
                t_guest.oldroomnr = ""
                t_guest.update_date = to_string(get_year(get_current_date()) , "9999") + "/" +\
                        to_string(get_month(get_current_date()) , "99") + "/" +\
                        to_string(get_day(get_current_date()) , "99")
                t_guest.update_time = to_string(get_current_time_in_seconds(), "HH:MM:SS")

                if guest.geburtdatum1 != None:
                    t_guest.birthday = to_string(get_day(guest.geburtdatum1) , "99") + "-" + to_string(get_month(guest.geburtdatum1) , "99") + "-" + to_string(get_year(guest.geburtdatum1) , "9999")
                else:
                    t_guest.birthday = ""

                if matches(res_line.zimmer_wunsch,r"*GDPRyes*"):
                    t_guest.gdpr_flag = "true"


                else:
                    t_guest.gdpr_flag = "false"

                if matches(t_guest.parameters,r"*Move in*"):

                    for history in db_session.query(History).filter(
                             (History.resnr == res_line.resnr) & (History.ankunft <= date_mdy(res_line.abreise)) & (History.abreise >= date_mdy(res_line.ankunft)) & (History.zi_wechsel) & (substring(History.bemerk, 0, 8) >= to_string(res_line.ankunft)) & (substring(History.bemerk, 0, 8) <= to_string(res_line.abreise)) & (matches(History.bemerk,"*: Moved To*"))).order_by(History.abreisezeit.desc()).all():
                        t_guest.oldroomnr = history.zinr
                        break

                    bufflist = query(bufflist_data, filters=(lambda bufflist: matches(bufflist.parameters,r"*DataExchange*") and bufflist.roomnr == t_guest.oldroomnr), first=True)

                    if bufflist:
                        t_guest_data.remove(t_guest)


    interface = db_session.query(Interface).filter(
             ((Interface.key == 3)) & (matches((Interface.parameters,"*Checkin*")) | (matches(Interface.parameters,"*Checkout*")) | (matches(Interface.parameters,"*Move in*")) | (matches(Interface.parameters,"*Move out*")) | (matches(Interface.parameters,"*Change Guestname*")) | (matches(Interface.parameters,"*DataExchange*")))).with_for_update().first()
    while None != interface:

        t_guest = query(t_guest_data, filters=(lambda t_guest: t_guest.roomnr == interface.zinr), first=True)

        if not t_guest:
            update_tguest(True)

        elif t_guest:

            if (interface.intdate == t_guest.ci_date and interface.int_time > t_guest.ci_time) or interface.intdate > t_guest.ci_date:

                t_interface = db_session.query(T_interface).filter(
                         (T_interface._recid == t_guest.irecid)).first()

                if t_interface:
                    db_session.delete(t_interface)
                    pass
                update_tguest(False)
            else:
                pass
                db_session.delete(interface)
                pass

        curr_recid = interface._recid
        interface = db_session.query(Interface).filter(
                 ((Interface.key == 3)) & (matches((Interface.parameters,"*Checkin*")) | (matches(Interface.parameters,"*Checkout*")) | (matches(Interface.parameters,"*Move in*")) | (matches(Interface.parameters,"*Move out*")) | (matches(Interface.parameters,"*Change Guestname*")) | (matches(Interface.parameters,"*DataExchange*"))) & (Interface._recid > curr_recid)).first()

    return generate_output()