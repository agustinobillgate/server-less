#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import History, Guest, Reservation, Segment

def history_listbl(from_name:string, zinr:string, disptype:int, sorttype:int, all_flag:bool, f_date:date, t_date:date):

    prepare_cache ([Reservation])

    history_list_data = []
    zeit:int = 0
    counter:int = 0
    history = guest = reservation = segment = None

    history_list = h_list = i_list = None

    history_list_data, History_list = create_model("History_list", {"gastinfo":string, "ankunft":date, "abreise":date, "abreisezeit":string, "zikateg":string, "zinr":string, "zipreis":Decimal, "zimmeranz":int, "arrangement":string, "resnr":int, "gesamtumsatz":Decimal, "zahlungsart":int, "segmentcode":int, "bemerk":string, "betriebsnr":int, "reslinnr":int, "gastnr":int, "address":string, "telefon":string, "vip":string, "resv_name":string})
    h_list_data, H_list = create_model_like(History, {"address":string, "telefon":string})
    i_list_data, I_list = create_model("I_list", {"s_recid":int, "ind":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal history_list_data, zeit, counter, history, guest, reservation, segment
        nonlocal from_name, zinr, disptype, sorttype, all_flag, f_date, t_date


        nonlocal history_list, h_list, i_list
        nonlocal history_list_data, h_list_data, i_list_data

        return {"history-list": history_list_data}

    def disp_it():

        nonlocal history_list_data, zeit, counter, history, guest, reservation, segment
        nonlocal from_name, zinr, disptype, sorttype, all_flag, f_date, t_date


        nonlocal history_list, h_list, i_list
        nonlocal history_list_data, h_list_data, i_list_data

        curr_date:int = 0

        if sorttype == 0:

            if zinr == "":

                history_obj_list = {}
                for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr)).filter(
                         (History.betriebsnr <= 1) & (History.ankunft >= f_date) & (History.ankunft <= t_date) & (History.gastnr > 0)).order_by(History.ankunft, History.gastinfo).all():
                    if history_obj_list.get(history._recid):
                        continue
                    else:
                        history_obj_list[history._recid] = True

                    if guest.name.lower()  >= (from_name).lower()  and guest.karteityp == disptype:

                        reservation = get_cache (Reservation, {"resnr": [(eq, history.resnr)]})

                        if reservation:
                            assign_it()
            else:

                history_obj_list = {}
                for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr)).filter(
                         (History.betriebsnr <= 1) & (History.ankunft >= f_date) & (History.ankunft <= t_date) & (History.zinr == (zinr).lower()) & (History.gastnr > 0)).order_by(History.ankunft, History.gastinfo).all():
                    if history_obj_list.get(history._recid):
                        continue
                    else:
                        history_obj_list[history._recid] = True

                    if guest.name.lower()  >= (from_name).lower()  and guest.karteityp == disptype:

                        reservation = get_cache (Reservation, {"resnr": [(eq, history.resnr)]})

                        if reservation:
                            assign_it()

        elif sorttype == 1:

            if zinr == "":

                history_obj_list = {}
                for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr)).filter(
                         (History.betriebsnr <= 1) & (History.abreise >= f_date) & (History.abreise <= t_date) & (History.gastnr > 0)).order_by(History.abreise, History.gastinfo).all():
                    if history_obj_list.get(history._recid):
                        continue
                    else:
                        history_obj_list[history._recid] = True

                    if guest.name.lower()  >= (from_name).lower()  and guest.karteityp == disptype:

                        reservation = get_cache (Reservation, {"resnr": [(eq, history.resnr)]})

                        if reservation:
                            assign_it()
            else:

                history_obj_list = {}
                for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr)).filter(
                         (History.betriebsnr <= 1) & (History.abreise >= f_date) & (History.abreise <= t_date) & (History.zinr == (zinr).lower()) & (History.gastnr > 0)).order_by(History.abreise, History.gastinfo).all():
                    if history_obj_list.get(history._recid):
                        continue
                    else:
                        history_obj_list[history._recid] = True

                    if guest.name.lower()  >= (from_name).lower()  and guest.karteityp == disptype:

                        reservation = get_cache (Reservation, {"resnr": [(eq, history.resnr)]})

                        if reservation:
                            assign_it()


    def disp_ita():

        nonlocal history_list_data, zeit, counter, history, guest, reservation, segment
        nonlocal from_name, zinr, disptype, sorttype, all_flag, f_date, t_date


        nonlocal history_list, h_list, i_list
        nonlocal history_list_data, h_list_data, i_list_data

        if sorttype == 0:

            if zinr == "":

                history_obj_list = {}
                for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr)).filter(
                         (History.betriebsnr <= 1) & (History.ankunft >= f_date) & (History.ankunft <= t_date) & (History.gastnr > 0)).order_by(History.ankunft, History.gastinfo).all():
                    if history_obj_list.get(history._recid):
                        continue
                    else:
                        history_obj_list[history._recid] = True

                    if guest.name.lower()  >= (from_name).lower()  and guest.karteityp == disptype:

                        reservation = get_cache (Reservation, {"resnr": [(eq, history.resnr)]})

                        if reservation:
                            assign_it()
            else:

                history_obj_list = {}
                for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr)).filter(
                         (History.betriebsnr <= 1) & (History.ankunft >= f_date) & (History.ankunft <= t_date) & (History.zinr == (zinr).lower()) & (History.gastnr > 0)).order_by(History.ankunft, History.gastinfo).all():
                    if history_obj_list.get(history._recid):
                        continue
                    else:
                        history_obj_list[history._recid] = True

                    if guest.name.lower()  >= (from_name).lower()  and guest.karteityp == disptype:

                        reservation = get_cache (Reservation, {"resnr": [(eq, history.resnr)]})

                        if reservation:
                            assign_it()

        elif sorttype == 1:

            if zinr == "":

                history_obj_list = {}
                for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr)).filter(
                         (History.betriebsnr <= 1) & (History.abreise >= f_date) & (History.abreise <= t_date) & (History.gastnr > 0)).order_by(History.abreise, History.gastinfo).all():
                    if history_obj_list.get(history._recid):
                        continue
                    else:
                        history_obj_list[history._recid] = True

                    if guest.name.lower()  >= (from_name).lower()  and guest.karteityp == disptype:

                        reservation = get_cache (Reservation, {"resnr": [(eq, history.resnr)]})

                        if reservation:
                            assign_it()
            else:

                history_obj_list = {}
                for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr)).filter(
                         (History.betriebsnr <= 1) & (History.abreise >= f_date) & (History.abreise <= t_date) & (History.zinr == (zinr).lower()) & (History.gastnr > 0)).order_by(History.abreise, History.gastinfo).all():
                    if history_obj_list.get(history._recid):
                        continue
                    else:
                        history_obj_list[history._recid] = True

                    if guest.name.lower()  >= (from_name).lower()  and guest.karteityp == disptype:

                        reservation = get_cache (Reservation, {"resnr": [(eq, history.resnr)]})

                        if reservation:
                            assign_it()


    def disp_itb():

        nonlocal history_list_data, zeit, counter, history, guest, reservation, segment
        nonlocal from_name, zinr, disptype, sorttype, all_flag, f_date, t_date


        nonlocal history_list, h_list, i_list
        nonlocal history_list_data, h_list_data, i_list_data

        curr_i:int = 0
        hbuff = None
        Hbuff =  create_buffer("Hbuff",History)
        h_list_data.clear()
        i_list_data.clear()

        if sorttype == 0:

            guest = get_cache (Guest, {"gastnr": [(gt, 0)],"name": [(ge, from_name)],"karteityp": [(eq, disptype)]})
            while None != guest:

                for history in db_session.query(History).filter(
                         (History.betriebsnr <= 1) & (History.ankunft >= f_date) & (History.ankunft <= t_date) & (History.gastnr == guest.gastnr)).order_by(History.ankunft).all():
                    curr_i = curr_i + 1
                    h_list = H_list()
                    h_list_data.append(h_list)

                    buffer_copy(history, h_list,except_fields=["history.gastinfo"])
                    h_list.gastinfo = guest.name + ", " + guest.anredefirma +\
                            " - " + guest.wohnort
                    h_list.betriebsnr = 1
                    h_list.address = guest.adresse1
                    h_list.telefon = guest.telefon


                    i_list = I_list()
                    i_list_data.append(i_list)

                    i_list.s_recid = h_list._recid
                    i_list.ind = curr_i

                    for hbuff in db_session.query(Hbuff).filter(
                             (Hbuff.resnr == history.resnr) & (Hbuff.reslinnr > 0) & (Hbuff.gastnr != history.gastnr) & not_ (Hbuff.zi_wechsel)).order_by(Hbuff.ankunft, Hbuff.gastinfo).all():
                        curr_i = curr_i + 1
                        h_list = H_list()
                        h_list_data.append(h_list)

                        buffer_copy(hbuff, h_list)
                        i_list = I_list()
                        i_list_data.append(i_list)

                        i_list.s_recid = h_list._recid
                        i_list.ind = curr_i

                curr_recid = guest._recid
                guest = db_session.query(Guest).filter(
                         (Guest.gastnr > 0) & (Guest.name >= (from_name).lower()) & (Guest.karteityp == disptype) & (Guest._recid > curr_recid)).first()

        elif sorttype == 1:

            guest = get_cache (Guest, {"gastnr": [(gt, 0)],"name": [(ge, from_name)],"karteityp": [(eq, disptype)]})
            while None != guest:

                for history in db_session.query(History).filter(
                         (History.betriebsnr <= 1) & (History.abreise >= f_date) & (History.abreise <= t_date) & (History.gastnr == guest.gastnr)).order_by(History.abreise).all():
                    curr_i = curr_i + 1
                    h_list = H_list()
                    h_list_data.append(h_list)

                    buffer_copy(history, h_list,except_fields=["history.gastinfo"])
                    h_list.gastinfo = guest.name + ", " + guest.anredefirma +\
                            " - " + guest.wohnort
                    h_list.betriebsnr = 1
                    h_list.address = guest.adresse1
                    h_list.telefon = guest.telefon


                    i_list = I_list()
                    i_list_data.append(i_list)

                    i_list.s_recid = h_list._recid
                    i_list.ind = curr_i

                    for hbuff in db_session.query(Hbuff).filter(
                             (Hbuff.resnr == history.resnr) & (Hbuff.reslinnr > 0) & (Hbuff.gastnr != history.gastnr) & not_ (Hbuff.zi_wechsel)).order_by(Hbuff.abreise, Hbuff.gastinfo).all():
                        curr_i = curr_i + 1
                        h_list = H_list()
                        h_list_data.append(h_list)

                        buffer_copy(hbuff, h_list)
                        i_list = I_list()
                        i_list_data.append(i_list)

                        i_list.s_recid = h_list._recid
                        i_list.ind = curr_i

                curr_recid = guest._recid
                guest = db_session.query(Guest).filter(
                         (Guest.gastnr > 0) & (Guest.name >= (from_name).lower()) & (Guest.karteityp == disptype) & (Guest._recid > curr_recid)).first()

        for h_list in query(h_list_data, sort_by=[("ind",False)]):
            i_list = query(i_list_data, (lambda i_list: i_list.s_recid == to_int(h_list._recid)), first=True)
            if not i_list:
                continue

            assign_it2()


    def disp_it1():

        nonlocal history_list_data, zeit, counter, history, guest, reservation, segment
        nonlocal from_name, zinr, disptype, sorttype, all_flag, f_date, t_date


        nonlocal history_list, h_list, i_list
        nonlocal history_list_data, h_list_data, i_list_data

        if sorttype == 0:

            if zinr == "":

                history_obj_list = {}
                for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr)).filter(
                         (History.betriebsnr <= 1) & (History.ankunft >= f_date) & (History.ankunft <= t_date) & (History.gastnr > 0)).order_by(History.ankunft, History.gastinfo).all():
                    if history_obj_list.get(history._recid):
                        continue
                    else:
                        history_obj_list[history._recid] = True

                    if matches(guest.name,from_name) and guest.karteityp == disptype:

                        reservation = get_cache (Reservation, {"resnr": [(eq, history.resnr)]})

                        if reservation:
                            assign_it()
            else:

                history_obj_list = {}
                for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr)).filter(
                         (History.betriebsnr <= 1) & (History.ankunft >= f_date) & (History.ankunft <= t_date) & (History.zinr == (zinr).lower()) & (History.gastnr > 0)).order_by(History.ankunft, History.gastinfo).all():
                    if history_obj_list.get(history._recid):
                        continue
                    else:
                        history_obj_list[history._recid] = True

                    if matches(guest.name,from_name) and guest.karteityp == disptype:

                        reservation = get_cache (Reservation, {"resnr": [(eq, history.resnr)]})

                        if reservation:
                            assign_it()

        elif sorttype == 1:

            if zinr == "":

                history_obj_list = {}
                for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr)).filter(
                         (History.betriebsnr <= 1) & (History.abreise >= f_date) & (History.abreise <= t_date) & (History.gastnr > 0)).order_by(History.abreise, History.gastinfo).all():
                    if history_obj_list.get(history._recid):
                        continue
                    else:
                        history_obj_list[history._recid] = True

                    if matches(guest.name,from_name) and guest.karteityp == disptype:

                        reservation = get_cache (Reservation, {"resnr": [(eq, history.resnr)]})

                        if reservation:
                            assign_it()
            else:

                history_obj_list = {}
                for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr)).filter(
                         (History.betriebsnr <= 1) & (History.abreise >= f_date) & (History.abreise <= t_date) & (History.zinr == (zinr).lower()) & (History.gastnr > 0)).order_by(History.abreise, History.gastinfo).all():
                    if history_obj_list.get(history._recid):
                        continue
                    else:
                        history_obj_list[history._recid] = True

                    if matches(guest.name,from_name) and guest.karteityp == disptype:

                        reservation = get_cache (Reservation, {"resnr": [(eq, history.resnr)]})

                        if reservation:
                            assign_it()


    def disp_it1a():

        nonlocal history_list_data, zeit, counter, history, guest, reservation, segment
        nonlocal from_name, zinr, disptype, sorttype, all_flag, f_date, t_date


        nonlocal history_list, h_list, i_list
        nonlocal history_list_data, h_list_data, i_list_data

        if sorttype == 0:

            if zinr == "":

                history_obj_list = {}
                for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr)).filter(
                         (History.betriebsnr <= 1) & (History.ankunft >= f_date) & (History.ankunft <= t_date) & (History.gastnr > 0)).order_by(History.ankunft, History.gastinfo).all():
                    if history_obj_list.get(history._recid):
                        continue
                    else:
                        history_obj_list[history._recid] = True

                    if matches(guest.name,from_name) and guest.karteityp == disptype:

                        reservation = get_cache (Reservation, {"resnr": [(eq, history.resnr)]})

                        if reservation:
                            assign_it()
            else:

                history_obj_list = {}
                for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr)).filter(
                         (History.betriebsnr <= 1) & (History.ankunft >= f_date) & (History.ankunft <= t_date) & (History.zinr == (zinr).lower()) & (History.gastnr > 0)).order_by(History.ankunft, History.gastinfo).all():
                    if history_obj_list.get(history._recid):
                        continue
                    else:
                        history_obj_list[history._recid] = True

                    if matches(guest.name,from_name) and guest.karteityp == disptype:

                        reservation = get_cache (Reservation, {"resnr": [(eq, history.resnr)]})

                        if reservation:
                            assign_it()

        elif sorttype == 1:

            if zinr == "":

                history_obj_list = {}
                for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr)).filter(
                         (History.betriebsnr <= 1) & (History.abreise >= f_date) & (History.abreise <= t_date) & (History.gastnr > 0)).order_by(History.abreise, History.gastinfo).all():
                    if history_obj_list.get(history._recid):
                        continue
                    else:
                        history_obj_list[history._recid] = True

                    if matches(guest.name,from_name) and guest.karteityp == disptype:

                        reservation = get_cache (Reservation, {"resnr": [(eq, history.resnr)]})

                        if reservation:
                            assign_it()
            else:

                history_obj_list = {}
                for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr)).filter(
                         (History.betriebsnr <= 1) & (History.abreise >= f_date) & (History.abreise <= t_date) & (History.zinr == (zinr).lower()) & (History.gastnr > 0)).order_by(History.abreise, History.gastinfo).all():
                    if history_obj_list.get(history._recid):
                        continue
                    else:
                        history_obj_list[history._recid] = True

                    if matches(guest.name,from_name) and guest.karteityp == disptype:

                        reservation = get_cache (Reservation, {"resnr": [(eq, history.resnr)]})

                        if reservation:
                            assign_it()


    def disp_it1b():

        nonlocal history_list_data, zeit, counter, history, guest, reservation, segment
        nonlocal from_name, zinr, disptype, sorttype, all_flag, f_date, t_date


        nonlocal history_list, h_list, i_list
        nonlocal history_list_data, h_list_data, i_list_data

        curr_i:int = 0
        hbuff = None
        Hbuff =  create_buffer("Hbuff",History)
        h_list_data.clear()

        if sorttype == 0:

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr > 0) & (matches(Guest.name,(from_name))) & (Guest.karteityp == disptype)).first()
            while None != guest:

                for history in db_session.query(History).filter(
                         (History.betriebsnr <= 1) & (History.ankunft >= f_date) & (History.ankunft <= t_date) & (History.gastnr == guest.gastnr)).order_by(History.ankunft).all():
                    curr_i = curr_i + 1
                    h_list = H_list()
                    h_list_data.append(h_list)

                    buffer_copy(history, h_list,except_fields=["history.gastinfo"])
                    h_list.gastinfo = guest.name + ", " + guest.anredefirma +\
                            " - " + guest.wohnort
                    h_list.betriebsnr = 1
                    h_list.address = guest.adresse1
                    h_list.telefon = guest.telefon


                    i_list = I_list()
                    i_list_data.append(i_list)

                    i_list.s_recid = h_list._recid
                    i_list.ind = curr_i

                    for hbuff in db_session.query(Hbuff).filter(
                             (Hbuff.resnr == history.resnr) & (Hbuff.reslinnr > 0) & (Hbuff.gastnr != history.gastnr) & not_ (Hbuff.zi_wechsel)).order_by(Hbuff.ankunft, Hbuff.gastinfo).all():
                        curr_i = curr_i + 1
                        h_list = H_list()
                        h_list_data.append(h_list)

                        buffer_copy(hbuff, h_list)
                        i_list = I_list()
                        i_list_data.append(i_list)

                        i_list.s_recid = h_list._recid
                        i_list.ind = curr_i

                curr_recid = guest._recid
                guest = db_session.query(Guest).filter(
                         (Guest.gastnr > 0) & (matches(Guest.name,(from_name))) & (Guest.karteityp == disptype) & (Guest._recid > curr_recid)).first()

        elif sorttype == 1:

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr > 0) & (matches(Guest.name,(from_name))) & (Guest.karteityp == disptype)).first()
            while None != guest:

                for history in db_session.query(History).filter(
                         (History.betriebsnr <= 1) & (History.abreise >= f_date) & (History.abreise <= t_date) & (History.gastnr > guest.gastnr)).order_by(History.abreise).all():
                    curr_i = curr_i + 1
                    h_list = H_list()
                    h_list_data.append(h_list)

                    buffer_copy(history, h_list,except_fields=["history.gastinfo"])
                    h_list.gastinfo = guest.name + ", " + guest.anredefirma +\
                            " - " + guest.wohnort
                    h_list.betriebsnr = 1
                    h_list.address = guest.adresse1
                    h_list.telefon = guest.telefon


                    i_list = I_list()
                    i_list_data.append(i_list)

                    i_list.s_recid = h_list._recid
                    i_list.ind = curr_i

                    for hbuff in db_session.query(Hbuff).filter(
                             (Hbuff.resnr == history.resnr) & (Hbuff.reslinnr > 0) & (Hbuff.gastnr != history.gastnr) & not_ (Hbuff.zi_wechsel)).order_by(Hbuff.abreise, Hbuff.gastinfo).all():
                        h_list = H_list()
                        h_list_data.append(h_list)

                        buffer_copy(hbuff, h_list)
                        curr_i = curr_i + 1
                        i_list = I_list()
                        i_list_data.append(i_list)

                        i_list.s_recid = h_list._recid
                        i_list.ind = curr_i

                curr_recid = guest._recid
                guest = db_session.query(Guest).filter(
                         (Guest.gastnr > 0) & (matches(Guest.name,(from_name))) & (Guest.karteityp == disptype) & (Guest._recid > curr_recid)).first()

        for h_list in query(h_list_data, sort_by=[("ind",False)]):
            i_list = query(i_list_data, (lambda i_list: i_list.s_recid == to_int(h_list._recid)), first=True)
            if not i_list:
                continue

            assign_it2()


    def assign_it():

        nonlocal history_list_data, zeit, counter, history, guest, reservation, segment
        nonlocal from_name, zinr, disptype, sorttype, all_flag, f_date, t_date


        nonlocal history_list, h_list, i_list
        nonlocal history_list_data, h_list_data, i_list_data


        history_list = History_list()
        history_list_data.append(history_list)

        history_list.gastinfo = entry(0, history.gastinfo, "-")
        history_list.ankunft = history.ankunft
        history_list.abreise = history.abreise
        history_list.abreisezeit = history.abreisezeit
        history_list.zikateg = history.zikateg
        history_list.zinr = history.zinr
        history_list.zipreis =  to_decimal(history.zipreis)
        history_list.zimmeranz = history.zimmeranz
        history_list.arrangement = history.arrangement
        history_list.resnr = history.resnr
        history_list.gesamtumsatz =  to_decimal(history.gesamtumsatz)
        history_list.zahlungsart = history.zahlungsart
        history_list.segmentcode = history.segmentcode
        history_list.bemerk = history.bemerk
        history_list.betriebsnr = history.betriebsnr
        history_list.reslinnr = history.reslinnr
        history_list.gastnr = history.gastnr
        history_list.address = guest.adresse1
        history_list.telefon = guest.telefon
        history_list.resv_name = reservation.name

        segment = get_cache (Segment, {"segmentcode": [(eq, history.segmentcode)],"betriebsnr": [(eq, 3)]})

        if segment:
            history_list.vip = "VIP"
        else:
            history_list.vip = "non-VIP"


    def assign_it2():

        nonlocal history_list_data, zeit, counter, history, guest, reservation, segment
        nonlocal from_name, zinr, disptype, sorttype, all_flag, f_date, t_date


        nonlocal history_list, h_list, i_list
        nonlocal history_list_data, h_list_data, i_list_data


        history_list = History_list()
        history_list_data.append(history_list)

        history_list.gastinfo = h_list.gastinfo
        history_list.ankunft = h_list.ankunft
        history_list.abreise = h_list.abreise
        history_list.abreisezeit = h_list.abreisezeit
        history_list.zikateg = h_list.zikateg
        history_list.zinr = h_list.zinr
        history_list.zipreis =  to_decimal(h_list.zipreis)
        history_list.zimmeranz = h_list.zimmeranz
        history_list.arrangement = h_list.arrangement
        history_list.resnr = h_list.resnr
        history_list.gesamtumsatz =  to_decimal(h_list.gesamtumsatz)
        history_list.zahlungsart = h_list.zahlungsart
        history_list.segmentcode = h_list.segmentcode
        history_list.bemerk = h_list.bemerk
        history_list.betriebsnr = h_list.betriebsnr
        history_list.reslinnr = h_list.reslinnr
        history_list.gastnr = h_list.gastnr
        history_list.address = h_list.address
        history_list.telefon = h_list.telefon

        segment = get_cache (Segment, {"segmentcode": [(eq, h_list.segmentcode)],"betriebsnr": [(eq, 3)]})

        if segment:
            history_list.vip = "VIP"
        else:
            history_list.vip = "non-VIP"


    if substring(from_name, 0, 1) == ("*").lower() :

        if substring(from_name, length(from_name) - 1, 1) != ("*").lower() :
            from_name = from_name + "*"

        if disptype == 0:
            disp_it1()

        elif disptype > 0 and not all_flag:
            disp_it1a()

        elif disptype > 0 and all_flag:
            disp_it1b()
    else:

        if disptype == 0:
            disp_it()

        elif disptype > 0 and not all_flag:
            disp_ita()

        elif disptype > 0 and all_flag:
            disp_itb()

    return generate_output()