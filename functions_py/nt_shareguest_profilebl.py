#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, History, Queasy, Res_history

t_guest_data, T_guest = create_model_like(Guest)
t_history_data, T_history = create_model_like(History)

def nt_shareguest_profilebl(hotel_name:string, t_guest_data:[T_guest], t_history_data:[T_history]):

    prepare_cache ([Guest, History, Queasy, Res_history])

    curr_gastnr:int = 0
    guest = history = queasy = res_history = None

    t_guest = t_history = bguest = bhistory = None

    Bguest = create_buffer("Bguest",Guest)
    Bhistory = create_buffer("Bhistory",History)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_gastnr, guest, history, queasy, res_history
        nonlocal hotel_name
        nonlocal bguest, bhistory


        nonlocal t_guest, t_history, bguest, bhistory

        return {}


    for t_guest in query(t_guest_data):

        bguest = get_cache (Guest, {"mobil_telefon": [(eq, t_guest.mobil_telefon),(ne, None),(ne, " ")]})

        if not bguest:

            bguest = get_cache (Guest, {"email_adr": [(eq, t_guest.email_adr),(ne, None),(ne, " ")]})

            if not bguest:

                if (t_guest.mobil_telefon == None or t_guest.mobil_telefon == " ") and (t_guest.email_adr == None or t_guest.email_adr == " "):
                    pass
                else:
                    curr_gastnr = 0

                    bguest = db_session.query(Bguest).order_by(Bguest._recid.desc()).first()

                    if bguest:
                        curr_gastnr = bguest.gastnr + 1


                    bguest = Guest()
                    db_session.add(bguest)

                    buffer_copy(t_guest, bguest,except_fields=["t_guest.gastnr"])
                    bguest.gastnr = curr_gastnr

                    for t_history in query(t_history_data, filters=(lambda t_history: t_history.gastnr == t_guest.gastnr)):
                        bhistory = History()
                        db_session.add(bhistory)

                        buffer_copy(t_history, bhistory,except_fields=["t_history.gastnr"])
                        bhistory.gastnr = curr_gastnr

                        queasy = get_cache (Queasy, {"key": [(eq, 203)],"number1": [(eq, curr_gastnr)],"number2": [(eq, t_history.resnr)],"char1": [(eq, hotel_name)]})

                        if not queasy:
                            queasy = Queasy()
                            db_session.add(queasy)

                            queasy.key = 203
                            queasy.number1 = curr_gastnr
                            queasy.number2 = t_history.resnr
                            queasy.char1 = hotel_name
                            queasy.char2 = t_guest.bemerkung


                        res_history = Res_history()
                        db_session.add(res_history)

                        res_history.nr = 0
                        res_history.datum = get_current_date()
                        res_history.zeit = get_current_time_in_seconds()
                        res_history.action = "SharingGuestProfile"
                        res_history.aenderung = "History of guest number " + to_string(curr_gastnr) + " received from " + hotel_name


                        pass
                        pass

            elif bguest:
                curr_gastnr = bguest.gastnr


                pass
                bguest.zimmeranz = bguest.zimmeranz + 1


                pass

                for t_history in query(t_history_data, filters=(lambda t_history: t_history.gastnr == t_guest.gastnr), sort_by=[("abreise",True)]):
                    bhistory = History()
                    db_session.add(bhistory)

                    buffer_copy(t_history, bhistory,except_fields=["t_history.gastnr"])
                    bhistory.gastnr = curr_gastnr

                    queasy = get_cache (Queasy, {"key": [(eq, 203)],"number1": [(eq, curr_gastnr)],"number2": [(eq, t_history.resnr)],"char1": [(eq, hotel_name)]})

                    if not queasy:
                        queasy = Queasy()
                        db_session.add(queasy)

                        queasy.key = 203
                        queasy.number1 = curr_gastnr
                        queasy.number2 = t_history.resnr
                        queasy.char1 = hotel_name
                        queasy.char2 = t_guest.bemerkung


                pass

        elif bguest:
            curr_gastnr = bguest.gastnr


            pass
            bguest.zimmeranz = bguest.zimmeranz + 1


            pass

            for t_history in query(t_history_data, filters=(lambda t_history: t_history.gastnr == t_guest.gastnr), sort_by=[("abreise",True)]):
                bhistory = History()
                db_session.add(bhistory)

                buffer_copy(t_history, bhistory,except_fields=["t_history.gastnr"])
                bhistory.gastnr = curr_gastnr

                queasy = get_cache (Queasy, {"key": [(eq, 203)],"number1": [(eq, curr_gastnr)],"number2": [(eq, t_history.resnr)],"char1": [(eq, hotel_name)]})

                if not queasy:
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 203
                    queasy.number1 = curr_gastnr
                    queasy.number2 = t_history.resnr
                    queasy.char1 = hotel_name
                    queasy.char2 = t_guest.bemerkung


            pass

    return generate_output()