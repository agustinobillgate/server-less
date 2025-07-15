#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Segment, Guestseg, Guest, History, Res_line

def black_listbl():

    prepare_cache ([Segment, Guestseg, Guest, History, Res_line])

    c_list_data = []
    segment = guestseg = guest = history = res_line = None

    c_list = None

    c_list_data, C_list = create_model("C_list", {"gastnr":int, "name":string, "nat":string, "resnr1":int, "ankunft1":date, "abreise1":date, "zinr1":string, "resnr2":int, "ankunft2":date, "abreise2":date, "zinr2":string, "resnr3":int, "ankunft3":date, "abreise3":date, "zinr3":string}, {"ankunft1": None, "abreise1": None, "ankunft2": None, "abreise2": None, "ankunft3": None, "abreise3": None})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal c_list_data, segment, guestseg, guest, history, res_line


        nonlocal c_list
        nonlocal c_list_data

        return {"c-list": c_list_data}


    c_list_data.clear()

    for segment in db_session.query(Segment).filter(
             (Segment.betriebsnr == 4)).order_by(Segment._recid).all():

        for guestseg in db_session.query(Guestseg).filter(
                 (Guestseg.segmentcode == segment.segmentcode)).order_by(Guestseg._recid).all():

            c_list = query(c_list_data, filters=(lambda c_list: c_list.gastnr == guestseg.gastnr), first=True)

            if not c_list:

                guest = get_cache (Guest, {"gastnr": [(eq, guestseg.gastnr)]})
                c_list = C_list()
                c_list_data.append(c_list)

                c_list.gastnr = guest.gastnr
                c_list.name = guest.name + ", " + guest.vorname1
                c_list.nat = guest.nation1

    for c_list in query(c_list_data):

        for history in db_session.query(History).filter(
                 (History.gastnr == c_list.gastnr) & not_ (History.zi_wechsel)).order_by(History.abreise.desc()).yield_per(100):
            c_list.resnr1 = history.resnr
            c_list.zinr1 = history.zinr
            c_list.ankunft1 = history.ankunft
            c_list.abreise1 = history.abreise


            break

        res_line = db_session.query(Res_line).filter(
                 ((Res_line.gastnr == c_list.gastnr) | (Res_line.gastnrmember == c_list.gastnr)) & (Res_line.active_flag == 1) & (Res_line.resstatus != 12)).first()

        if res_line:
            c_list.resnr2 = res_line.resnr
            c_list.zinr2 = res_line.zinr
            c_list.ankunft2 = res_line.ankunft
            c_list.abreise2 = res_line.abreise

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.gastnrmember == c_list.gastnr) & (Res_line.active_flag == 0)).order_by(Res_line.ankunft).yield_per(100):
            c_list.resnr3 = res_line.resnr
            c_list.zinr3 = res_line.zinr
            c_list.ankunft3 = res_line.ankunft
            c_list.abreise3 = res_line.abreise


            break

    return generate_output()