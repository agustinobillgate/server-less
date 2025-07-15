#using conversion tools version: 1.0.0.29

from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Genstat, Segment, Zimmer

def nt_tauziarpt_gen_otbmseg_gsheetbl(ddate:date):
    totroom = 0
    u_list_list = []
    w_int:int = 0
    indv:int = 0
    htparam = genstat = segment = zimmer = None

    u_list = None

    u_list_list, U_list = create_model("U_list", {"rmsegmt":int, "rmrev":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal totroom, u_list_list, w_int, indv, htparam, genstat, segment, zimmer
        nonlocal ddate


        nonlocal u_list
        nonlocal u_list_list

        return {"totroom": totroom, "u-list": u_list_list}

    def calc_room():

        nonlocal totroom, u_list_list, w_int, indv, htparam, genstat, segment, zimmer
        nonlocal ddate


        nonlocal u_list
        nonlocal u_list_list

        room_count = 0

        def generate_inner_output():
            return (room_count)


        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer._recid).all():
            room_count = room_count + 1

        return generate_inner_output()

    totroom = calc_room()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 109)).first()

    if htparam:
        w_int = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 123)).first()

    if htparam:
        indv = htparam.finteger

    for genstat in db_session.query(Genstat).filter(
             (Genstat.datum == ddate) & (Genstat.gastnr != w_int) & (Genstat.gastnr != indv) & (Genstat.gastnr > 0) & (Genstat.zipreis != 0) & (Genstat.resstatus != 8) & (Genstat.resstatus != 13) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():

        segment = db_session.query(Segment).filter(
                     (Segment.segmentcode == genstat.segmentcode)).first()

        if segment:
            u_list = U_list()
            u_list_list.append(u_list)

            u_list.rmsegmt = segment.segmentcode
            u_list.rmrev =  to_decimal(genstat.logis)

    return generate_output()