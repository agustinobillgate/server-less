from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import History, Guest, Segment

def history_listbl(from_name:str, zinr:str, disptype:int, sorttype:int, all_flag:bool, f_date:date, t_date:date):
    history_list_list = []
    zeit:int = 0
    counter:int = 0
    history = guest = segment = None

    history_list = h_list = i_list = hbuff = None

    history_list_list, History_list = create_model("History_list", {"gastinfo":str, "ankunft":date, "abreise":date, "abreisezeit":str, "zikateg":str, "zinr":str, "zipreis":decimal, "zimmeranz":int, "arrangement":str, "resnr":int, "gesamtumsatz":decimal, "zahlungsart":int, "segmentcode":int, "bemerk":str, "betriebsnr":int, "reslinnr":int, "gastnr":int, "address":str, "telefon":str, "vip":str})
    h_list_list, H_list = create_model_like(History, {"address":str, "telefon":str})
    i_list_list, I_list = create_model("I_list", {"s_recid":int, "ind":int})

    Hbuff = History

    db_session = local_storage.db_session

    def generate_output():
        nonlocal history_list_list, zeit, counter, history, guest, segment
        nonlocal hbuff


        nonlocal history_list, h_list, i_list, hbuff
        nonlocal history_list_list, h_list_list, i_list_list
        return {"history-list": history_list_list}

    def disp_it():

        nonlocal history_list_list, zeit, counter, history, guest, segment
        nonlocal hbuff


        nonlocal history_list, h_list, i_list, hbuff
        nonlocal history_list_list, h_list_list, i_list_list

        curr_date:int = 0

        if sorttype == 0:

            if zinr == "":

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr > 0) &  (func.lower(Guest.name) >= (from_name).lower()) &  (Guest.karteityp == disptype)).first()
                while None != guest:

                    for history in db_session.query(History).filter(
                            (History.betriebsnr <= 1) &  (History.gastnr == guest.gastnr) &  (History.ankunft >= f_date) &  (History.ankunft <= t_date)).all():
                        assign_it()

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr > 0) &  (func.lower(Guest.name) >= (from_name).lower()) &  (Guest.karteityp == disptype)).first()
            else:

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr > 0) &  (func.lower(Guest.name) >= (from_name).lower()) &  (Guest.karteityp == disptype)).first()
                while None != guest:

                    for history in db_session.query(History).filter(
                            (History.betriebsnr <= 1) &  (History.ankunft >= f_date) &  (History.ankunft <= t_date) &  (func.lower(History.(zinr).lower()) == (zinr).lower()) &  (History.gastnr == guest.gastnr)).all():
                        assign_it()

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr > 0) &  (func.lower(Guest.name) >= (from_name).lower()) &  (Guest.karteityp == disptype)).first()

        elif sorttype == 1:

            if zinr == "":

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr > 0) &  (func.lower(Guest.name) >= (from_name).lower()) &  (Guest.karteityp == disptype)).first()
                while None != guest:

                    for history in db_session.query(History).filter(
                            (History.betriebsnr <= 1) &  (History.abreise >= f_date) &  (History.abreise <= t_date) &  (History.gastnr == guest.gastnr)).all():
                        assign_it()

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr > 0) &  (func.lower(Guest.name) >= (from_name).lower()) &  (Guest.karteityp == disptype)).first()
            else:

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr > 0) &  (func.lower(Guest.name) >= (from_name).lower()) &  (Guest.karteityp == disptype)).first()
                while None != guest:

                    for history in db_session.query(History).filter(
                            (History.betriebsnr <= 1) &  (History.abreise >= f_date) &  (History.abreise <= t_date) &  (func.lower(History.(zinr).lower()) == (zinr).lower()) &  (History.gastnr == guest.gastnr)).all():
                        assign_it()

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr > 0) &  (func.lower(Guest.name) >= (from_name).lower()) &  (Guest.karteityp == disptype)).first()

    def disp_ita():

        nonlocal history_list_list, zeit, counter, history, guest, segment
        nonlocal hbuff


        nonlocal history_list, h_list, i_list, hbuff
        nonlocal history_list_list, h_list_list, i_list_list

        if sorttype == 0:

            if zinr == "":

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr > 0) &  (func.lower(Guest.name) >= (from_name).lower()) &  (Guest.karteityp == disptype)).first()
                while None != guest:

                    for history in db_session.query(History).filter(
                            (History.betriebsnr <= 1) &  (History.ankunft >= f_date) &  (History.ankunft <= t_date) &  (History.gastnr == guest.gastnr)).all():
                        assign_it()

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr > 0) &  (func.lower(Guest.name) >= (from_name).lower()) &  (Guest.karteityp == disptype)).first()
            else:

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr > 0) &  (func.lower(Guest.name) >= (from_name).lower()) &  (Guest.karteityp == disptype)).first()
                while None != guest:

                    for history in db_session.query(History).filter(
                            (History.betriebsnr <= 1) &  (History.ankunft >= f_date) &  (History.ankunft <= t_date) &  (func.lower(History.(zinr).lower()) == (zinr).lower()) &  (History.gastnr == guest.gastnr)).all():
                        assign_it()

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr > 0) &  (func.lower(Guest.name) >= (from_name).lower()) &  (Guest.karteityp == disptype)).first()

        elif sorttype == 1:

            if zinr == "":

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr > 0) &  (func.lower(Guest.name) >= (from_name).lower()) &  (Guest.karteityp == disptype)).first()
                while None != guest:

                    for history in db_session.query(History).filter(
                            (History.betriebsnr <= 1) &  (History.abreise >= f_date) &  (History.abreise <= t_date) &  (History.gastnr == guest.gastnr)).all():
                        assign_it()

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr > 0) &  (func.lower(Guest.name) >= (from_name).lower()) &  (Guest.karteityp == disptype)).first()
            else:

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr > 0) &  (func.lower(Guest.name) >= (from_name).lower()) &  (Guest.karteityp == disptype)).first()
                while None != guest:

                    for history in db_session.query(History).filter(
                            (History.betriebsnr <= 1) &  (History.abreise >= f_date) &  (History.abreise <= t_date) &  (func.lower(History.(zinr).lower()) == (zinr).lower()) &  (History.gastnr == guest.gastnr)).all():
                        assign_it()

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr > 0) &  (func.lower(Guest.name) >= (from_name).lower()) &  (Guest.karteityp == disptype)).first()

    def disp_itb():

        nonlocal history_list_list, zeit, counter, history, guest, segment
        nonlocal hbuff


        nonlocal history_list, h_list, i_list, hbuff
        nonlocal history_list_list, h_list_list, i_list_list

        curr_i:int = 0
        Hbuff = History
        h_list_list.clear()
        i_list_list.clear()

        if sorttype == 0:

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr > 0) &  (func.lower(Guest.name) >= (from_name).lower()) &  (Guest.karteityp == disptype)).first()
            while None != guest:

                for history in db_session.query(History).filter(
                        (History.betriebsnr <= 1) &  (History.ankunft >= f_date) &  (History.ankunft <= t_date) &  (History.gastnr == guest.gastnr)).all():
                    curr_i = curr_i + 1
                    h_list = H_list()
                    h_list_list.append(h_list)

                    buffer_copy(history, h_list,except_fields=["history.gastinfo"])
                    h_list.gastinfo = guest.name + ", " + guest.anredefirma +\
                            " - " + guest.wohnort
                    h_list.betriebsnr = 1
                    h_list.address = guest.adresse1
                    h_list.telefon = guest.telefon


                    i_list = I_list()
                    i_list_list.append(i_list)

                    i_list.s_recid = h_list._recid
                    i_list.ind = curr_i

                    for hbuff in db_session.query(Hbuff).filter(
                            (Hbuff.resnr == history.resnr) &  (Hbuff.reslinnr > 0) &  (Hbuff.gastnr != history.gastnr) &  (not Hbuff.zi_wechsel)).all():
                        curr_i = curr_i + 1
                        h_list = H_list()
                        h_list_list.append(h_list)

                        buffer_copy(hbuff, h_list)
                        i_list = I_list()
                        i_list_list.append(i_list)

                        i_list.s_recid = h_list._recid
                        i_list.ind = curr_i

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr > 0) &  (func.lower(Guest.name) >= (from_name).lower()) &  (Guest.karteityp == disptype)).first()

        elif sorttype == 1:

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr > 0) &  (func.lower(Guest.name) >= (from_name).lower()) &  (Guest.karteityp == disptype)).first()
            while None != guest:

                for history in db_session.query(History).filter(
                        (History.betriebsnr <= 1) &  (History.abreise >= f_date) &  (History.abreise <= t_date) &  (History.gastnr == guest.gastnr)).all():
                    curr_i = curr_i + 1
                    h_list = H_list()
                    h_list_list.append(h_list)

                    buffer_copy(history, h_list,except_fields=["history.gastinfo"])
                    h_list.gastinfo = guest.name + ", " + guest.anredefirma +\
                            " - " + guest.wohnort
                    h_list.betriebsnr = 1
                    h_list.address = guest.adresse1
                    h_list.telefon = guest.telefon


                    i_list = I_list()
                    i_list_list.append(i_list)

                    i_list.s_recid = h_list._recid
                    i_list.ind = curr_i

                    for hbuff in db_session.query(Hbuff).filter(
                            (Hbuff.resnr == history.resnr) &  (Hbuff.reslinnr > 0) &  (Hbuff.gastnr != history.gastnr) &  (not Hbuff.zi_wechsel)).all():
                        curr_i = curr_i + 1
                        h_list = H_list()
                        h_list_list.append(h_list)

                        buffer_copy(hbuff, h_list)
                        i_list = I_list()
                        i_list_list.append(i_list)

                        i_list.s_recid = h_list._recid
                        i_list.ind = curr_i

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr > 0) &  (func.lower(Guest.name) >= (from_name).lower()) &  (Guest.karteityp == disptype)).first()

        for h_list in query(h_list_list):
            i_list = db_session.query(I_list).filter((I_list.s_recid == to_int(h_list._recid))).first()
            if not i_list:
                continue

            assign_it2()

    def disp_it1():

        nonlocal history_list_list, zeit, counter, history, guest, segment
        nonlocal hbuff


        nonlocal history_list, h_list, i_list, hbuff
        nonlocal history_list_list, h_list_list, i_list_list

        if sorttype == 0:

            if zinr == "":

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr > 0) &  (Guest.name.op("~")(from_name)) &  (Guest.karteityp == disptype)).first()
                while None != guest:

                    for history in db_session.query(History).filter(
                            (History.betriebsnr <= 1) &  (History.ankunft >= f_date) &  (History.ankunft <= t_date) &  (History.gastnr == guest.gastnr)).all():
                        assign_it()

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr > 0) &  (Guest.name.op("~")(from_name)) &  (Guest.karteityp == disptype)).first()
            else:

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr > 0) &  (Guest.name.op("~")(from_name)) &  (Guest.karteityp == disptype)).first()
                while None != guest:

                    for history in db_session.query(History).filter(
                            (History.betriebsnr <= 1) &  (History.ankunft >= f_date) &  (History.ankunft <= t_date) &  (func.lower(History.(zinr).lower()) == (zinr).lower()) &  (History.gastnr == guest.gastnr)).all():
                        assign_it()

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr > 0) &  (Guest.name.op("~")(from_name)) &  (Guest.karteityp == disptype)).first()

        elif sorttype == 1:

            if zinr == "":

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr > 0) &  (Guest.name.op("~")(from_name)) &  (Guest.karteityp == disptype)).first()
                while None != guest:

                    for history in db_session.query(History).filter(
                            (History.betriebsnr <= 1) &  (History.abreise >= f_date) &  (History.abreise <= t_date) &  (History.gastnr == guest.gastnr)).all():
                        assign_it()

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr > 0) &  (Guest.name.op("~")(from_name)) &  (Guest.karteityp == disptype)).first()
            else:

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr > 0) &  (Guest.name.op("~")(from_name)) &  (Guest.karteityp == disptype)).first()
                while None != guest:

                    for history in db_session.query(History).filter(
                            (History.betriebsnr <= 1) &  (History.abreise >= f_date) &  (History.abreise <= t_date) &  (func.lower(History.(zinr).lower()) == (zinr).lower()) &  (History.gastnr == guest.gastnr)).all():
                        assign_it()

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr > 0) &  (Guest.name.op("~")(from_name)) &  (Guest.karteityp == disptype)).first()

    def disp_it1a():

        nonlocal history_list_list, zeit, counter, history, guest, segment
        nonlocal hbuff


        nonlocal history_list, h_list, i_list, hbuff
        nonlocal history_list_list, h_list_list, i_list_list

        if sorttype == 0:

            if zinr == "":

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr > 0) &  (Guest.name.op("~")(from_name)) &  (Guest.karteityp == disptype)).first()
                while None != guest:

                    for history in db_session.query(History).filter(
                            (History.betriebsnr <= 1) &  (History.ankunft >= f_date) &  (History.ankunft <= t_date) &  (History.gastnr == guest.gastnr)).all():
                        assign_it()

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr > 0) &  (Guest.name.op("~")(from_name)) &  (Guest.karteityp == disptype)).first()
            else:

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr > 0) &  (Guest.name.op("~")(from_name)) &  (Guest.karteityp == disptype)).first()
                while None != guest:

                    for history in db_session.query(History).filter(
                            (History.betriebsnr <= 1) &  (History.ankunft >= f_date) &  (History.ankunft <= t_date) &  (func.lower(History.(zinr).lower()) == (zinr).lower()) &  (History.gastnr == guest.gastnr)).all():
                        assign_it()

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr > 0) &  (Guest.name.op("~")(from_name)) &  (Guest.karteityp == disptype)).first()

        elif sorttype == 1:

            if zinr == "":

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr > 0) &  (Guest.name.op("~")(from_name)) &  (Guest.karteityp == disptype)).first()
                while None != guest:

                    for history in db_session.query(History).filter(
                            (History.betriebsnr <= 1) &  (History.abreise >= f_date) &  (History.abreise <= t_date) &  (History.gastnr == guest.gastnr)).all():
                        assign_it()

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr > 0) &  (Guest.name.op("~")(from_name)) &  (Guest.karteityp == disptype)).first()
            else:

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr > 0) &  (Guest.name.op("~")(from_name)) &  (Guest.karteityp == disptype)).first()
                while None != guest:

                    for history in db_session.query(History).filter(
                            (History.betriebsnr <= 1) &  (History.abreise >= f_date) &  (History.abreise <= t_date) &  (func.lower(History.(zinr).lower()) == (zinr).lower()) &  (History.gastnr == guest.gastnr)).all():
                        assign_it()

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr > 0) &  (Guest.name.op("~")(from_name)) &  (Guest.karteityp == disptype)).first()

    def disp_it1b():

        nonlocal history_list_list, zeit, counter, history, guest, segment
        nonlocal hbuff


        nonlocal history_list, h_list, i_list, hbuff
        nonlocal history_list_list, h_list_list, i_list_list

        curr_i:int = 0
        Hbuff = History
        h_list_list.clear()

        if sorttype == 0:

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr > 0) &  (Guest.name.op("~")(from_name)) &  (Guest.karteityp == disptype)).first()
            while None != guest:

                for history in db_session.query(History).filter(
                        (History.betriebsnr <= 1) &  (History.ankunft >= f_date) &  (History.ankunft <= t_date) &  (History.gastnr == guest.gastnr)).all():
                    curr_i = curr_i + 1
                    h_list = H_list()
                    h_list_list.append(h_list)

                    buffer_copy(history, h_list,except_fields=["history.gastinfo"])
                    h_list.gastinfo = guest.name + ", " + guest.anredefirma +\
                            " - " + guest.wohnort
                    h_list.betriebsnr = 1
                    h_list.address = guest.adresse1
                    h_list.telefon = guest.telefon


                    i_list = I_list()
                    i_list_list.append(i_list)

                    i_list.s_recid = h_list._recid
                    i_list.ind = curr_i

                    for hbuff in db_session.query(Hbuff).filter(
                            (Hbuff.resnr == history.resnr) &  (Hbuff.reslinnr > 0) &  (Hbuff.gastnr != history.gastnr) &  (not Hbuff.zi_wechsel)).all():
                        curr_i = curr_i + 1
                        h_list = H_list()
                        h_list_list.append(h_list)

                        buffer_copy(hbuff, h_list)
                        i_list = I_list()
                        i_list_list.append(i_list)

                        i_list.s_recid = h_list._recid
                        i_list.ind = curr_i

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr > 0) &  (Guest.name.op("~")(from_name)) &  (Guest.karteityp == disptype)).first()

        elif sorttype == 1:

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr > 0) &  (Guest.name.op("~")(from_name)) &  (Guest.karteityp == disptype)).first()
            while None != guest:

                for history in db_session.query(History).filter(
                        (History.betriebsnr <= 1) &  (History.abreise >= f_date) &  (History.abreise <= t_date) &  (History.gastnr > guest.gastnr)).all():
                    curr_i = curr_i + 1
                    h_list = H_list()
                    h_list_list.append(h_list)

                    buffer_copy(history, h_list,except_fields=["history.gastinfo"])
                    h_list.gastinfo = guest.name + ", " + guest.anredefirma +\
                            " - " + guest.wohnort
                    h_list.betriebsnr = 1
                    h_list.address = guest.adresse1
                    h_list.telefon = guest.telefon


                    i_list = I_list()
                    i_list_list.append(i_list)

                    i_list.s_recid = h_list._recid
                    i_list.ind = curr_i

                    for hbuff in db_session.query(Hbuff).filter(
                            (Hbuff.resnr == history.resnr) &  (Hbuff.reslinnr > 0) &  (Hbuff.gastnr != history.gastnr) &  (not Hbuff.zi_wechsel)).all():
                        h_list = H_list()
                        h_list_list.append(h_list)

                        buffer_copy(hbuff, h_list)
                        curr_i = curr_i + 1
                        i_list = I_list()
                        i_list_list.append(i_list)

                        i_list.s_recid = h_list._recid
                        i_list.ind = curr_i

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr > 0) &  (Guest.name.op("~")(from_name)) &  (Guest.karteityp == disptype)).first()

        for h_list in query(h_list_list):
            i_list = db_session.query(I_list).filter((I_list.s_recid == to_int(h_list._recid))).first()
            if not i_list:
                continue

            assign_it2()

    def assign_it():

        nonlocal history_list_list, zeit, counter, history, guest, segment
        nonlocal hbuff


        nonlocal history_list, h_list, i_list, hbuff
        nonlocal history_list_list, h_list_list, i_list_list


        history_list = History_list()
        history_list_list.append(history_list)

        history_list.gastinfo = entry(0, history.gastinfo, "-")
        history_list.ankunft = history.ankunft
        history_list.abreise = history.abreise
        history_list.abreisezeit = history.abreisezeit
        history_list.zikateg = history.zikateg
        history_list.zinr = history.zinr
        history_list.zipreis = history.zipreis
        history_list.zimmeranz = history.zimmeranz
        history_list.arrangement = history.arrangement
        history_list.resnr = history.resnr
        history_list.gesamtumsatz = history.gesamtumsatz
        history_list.zahlungsart = history.zahlungsart
        history_list.segmentcode = history.segmentcode
        history_list.bemerk = history.bemerk
        history_list.betriebsnr = history.betriebsnr
        history_list.reslinnr = history.reslinnr
        history_list.gastnr = history.gastnr
        history_list.address = guest.adresse1
        history_list.telefon = guest.telefon

        segment = db_session.query(Segment).filter(
                (Segment.segmentcode == history.segmentcode) &  (Segment.betriebsnr == 3)).first()

        if segment:
            history_list.vip = "VIP"
        else:
            history_list.vip = "non_VIP"

    def assign_it2():

        nonlocal history_list_list, zeit, counter, history, guest, segment
        nonlocal hbuff


        nonlocal history_list, h_list, i_list, hbuff
        nonlocal history_list_list, h_list_list, i_list_list


        history_list = History_list()
        history_list_list.append(history_list)

        history_list.gastinfo = h_list.gastinfo
        history_list.ankunft = h_list.ankunft
        history_list.abreise = h_list.abreise
        history_list.abreisezeit = h_list.abreisezeit
        history_list.zikateg = h_list.zikateg
        history_list.zinr = h_list.zinr
        history_list.zipreis = h_list.zipreis
        history_list.zimmeranz = h_list.zimmeranz
        history_list.arrangement = h_list.arrangement
        history_list.resnr = h_list.resnr
        history_list.gesamtumsatz = h_list.gesamtumsatz
        history_list.zahlungsart = h_list.zahlungsart
        history_list.segmentcode = h_list.segmentcode
        history_list.bemerk = h_list.bemerk
        history_list.betriebsnr = h_list.betriebsnr
        history_list.reslinnr = h_list.reslinnr
        history_list.gastnr = h_list.gastnr
        history_list.address = h_list.address
        history_list.telefon = h_list.telefon

        segment = db_session.query(Segment).filter(
                (Segment.segmentcode == h_list.segmentcode) &  (Segment.betriebsnr == 3)).first()

        if segment:
            history_list.vip = "VIP"
        else:
            history_list.vip = "non_VIP"

    if substring(from_name, 0, 1) == "*":

        if substring(from_name, len(from_name) - 1, 1) != "*":
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