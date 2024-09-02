from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from models import Zimmer, Outorder, Guest, Res_line, Htparam, Paramtext

def rminfobl(pvilanguage:int, rmno:str):
    o_str = ""
    s_str = ""
    rm_col = ""
    bcol = 0
    fcol = 0
    fr_title = ""
    rm_stat = ""
    finteger = 0
    room_list = []
    inhouse_list = []
    arrival_list = []
    t_outorder_list = []
    lvcarea:str = "rminfo"
    stat_list:[str] = ["", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    zimmer = outorder = guest = res_line = htparam = paramtext = None

    room = inhouse = arrival = t_outorder = guest1 = reslin1 = rbuff = None

    room_list, Room = create_model_like(Zimmer, {"rmtype":str})
    inhouse_list, Inhouse = create_model("Inhouse", {"gname":str, "arrival":date, "depart":date, "adult":int, "child":int})
    arrival_list, Arrival = create_model("Arrival", {"gname":str, "arrival":date, "depart":date, "adult":int, "child":int, "resstatus":str})
    t_outorder_list, T_outorder = create_model_like(Outorder)

    Guest1 = Guest
    Reslin1 = Res_line
    Rbuff = Zimmer

    db_session = local_storage.db_session

    def generate_output():
        nonlocal o_str, s_str, rm_col, bcol, fcol, fr_title, rm_stat, finteger, room_list, inhouse_list, arrival_list, t_outorder_list, lvcarea, stat_list, zimmer, outorder, guest, res_line, htparam, paramtext
        nonlocal guest1, reslin1, rbuff


        nonlocal room, inhouse, arrival, t_outorder, guest1, reslin1, rbuff
        nonlocal room_list, inhouse_list, arrival_list, t_outorder_list
        return {"o_str": o_str, "s_str": s_str, "rm_col": rm_col, "bcol": bcol, "fcol": fcol, "fr_title": fr_title, "rm_stat": rm_stat, "finteger": finteger, "room": room_list, "inhouse": inhouse_list, "arrival": arrival_list, "t-outorder": t_outorder_list}

    def create_room():

        nonlocal o_str, s_str, rm_col, bcol, fcol, fr_title, rm_stat, finteger, room_list, inhouse_list, arrival_list, t_outorder_list, lvcarea, stat_list, zimmer, outorder, guest, res_line, htparam, paramtext
        nonlocal guest1, reslin1, rbuff


        nonlocal room, inhouse, arrival, t_outorder, guest1, reslin1, rbuff
        nonlocal room_list, inhouse_list, arrival_list, t_outorder_list

        curr_date:date = None
        Guest1 = Guest
        Reslin1 = Res_line
        Rbuff = Zimmer

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zinr == rmno)).first()

        if zimmer:
            buffer_copy(zimmer, room)

        room = query(room_list, first=True)

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 87)).first()
        curr_date = htparam.fdate

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 230) &  (Paramtext.sprachcode == room.typ)).first()

        if paramtext:
            o_str = paramtext.ptext
        else:
            o_str = ""

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == (room.setup + 9200))).first()

        if paramtext:
            s_str = paramtext.ptext
        else:
            s_str = ""
        create_status(room.zistatus)
        inhouse = Inhouse()
        inhouse_list.append(inhouse)


        reslin1 = db_session.query(Reslin1).filter(
                (Reslin1.zinr == rmno) &  (Reslin1.active_flag == 1)).first()

        if reslin1:

            guest1 = db_session.query(Guest1).filter(
                    (Guest1.gastnr == reslin1.gastnrmember)).first()

            if guest1:
                inhouse.gname = guest1.name + " " + guest1.vorname1 + guest1.anredefirma
            inhouse.arrival = reslin1.ankunft
            inhouse.depart = reslin1.abreise
            inhouse.adult = reslin1.erwachs
            inhouse.child = reslin1.kind1

        for outorder in db_session.query(Outorder).filter(
                (Outorder.zinr == rmno) &  (Outorder.gespende >= curr_date)).all():
            t_outorder = T_outorder()
            t_outorder_list.append(t_outorder)

            buffer_copy(outorder, t_outorder)

        for reslin1 in db_session.query(Reslin1).filter(
                (Reslin1.zinr == rmno) &  (Reslin1.active_flag == 0)).all():

            guest1 = db_session.query(Guest1).filter(
                    (Guest1.gastnr == reslin1.gastnrmember)).first()
            arrival = Arrival()
            arrival_list.append(arrival)

            arrival.gname = guest1.name + " " + guest1.vorname1 +\
                    guest1.anredefirma
            arrival.arrival = reslin1.ankunft
            arrival.depart = reslin1.abreise
            arrival.adult = reslin1.erwachs
            arrival.child = reslin1.kind1
            arrival.resstatus = stat_list[reslin1.resstatus - 1]


        fr_title = translateExtended ("Room Info", lvcarea, "") + " (" + rmno + ")"

    def create_status(zistatus:int):

        nonlocal o_str, s_str, rm_col, bcol, fcol, fr_title, rm_stat, finteger, room_list, inhouse_list, arrival_list, t_outorder_list, lvcarea, stat_list, zimmer, outorder, guest, res_line, htparam, paramtext
        nonlocal guest1, reslin1, rbuff


        nonlocal room, inhouse, arrival, t_outorder, guest1, reslin1, rbuff
        nonlocal room_list, inhouse_list, arrival_list, t_outorder_list

        stat:str = ""
        item_fgcol:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        if zistatus == 0:
            bcol = 8
            rm_col = " VC "
            rm_stat = translateExtended ("Vacant Clean", lvcarea, "")

        elif zistatus == 1:
            bcol = 11
            rm_col = " CU "
            rm_stat = translateExtended ("Clean Unchecked", lvcarea, "")

        elif zistatus == 2:
            bcol = 2
            rm_col = " VD "
            rm_stat = translateExtended ("Vacant Dirty", lvcarea, "")

        elif zistatus == 3:
            bcol = 1
            rm_col = " ED "
            rm_stat = translateExtended ("Expected Departure", lvcarea, "")

        elif zistatus == 4:
            bcol = 14
            rm_col = " OD "
            rm_stat = translateExtended ("Occupied Dirty", lvcarea, "")

        elif zistatus == 5:
            bcol = 15
            rm_col = " OC "
            rm_stat = translateExtended ("Occupied Clean", lvcarea, "")

        elif zistatus == 6:
            bcol = 12
            rm_col = " OO "
            rm_stat = translateExtended ("Out Of Order", lvcarea, "")

        elif zistatus == 7:
            bcol = 4
            rm_col = " OM "
            rm_stat = translateExtended ("Off Market", lvcarea, "")

        elif zistatus == 8:
            bcol = 5
            rm_col = " DD "
            rm_stat = translateExtended ("Do not Disturb", lvcarea, "")

        elif zistatus == 9:
            bcol = 13
            rm_col = " OS "
            rm_stat = translateExtended ("Out Of Service", lvcarea, "")


        fcol = item_fgcol[bcol - 1]

    stat_list[0] = translateExtended ("Guaranted", lvcarea, "")
    stat_list[1] = translateExtended ("6 PM", lvcarea, "")
    stat_list[2] = translateExtended ("Tentative", lvcarea, "")
    stat_list[3] = translateExtended ("WaitList", lvcarea, "")
    stat_list[4] = translateExtended ("OralConfirm", lvcarea, "")
    stat_list[5] = translateExtended ("Inhouse", lvcarea, "")
    stat_list[6] = ""
    stat_list[7] = translateExtended ("Departed", lvcarea, "")
    stat_list[8] = translateExtended ("Cancelled", lvcarea, "")
    stat_list[9] = translateExtended ("NoShow", lvcarea, "")
    stat_list[10] = translateExtended ("ShareRes", lvcarea, "")
    stat_list[11] = ""
    stat_list[12] = translateExtended ("RmSharer", lvcarea, "")
    finteger = get_output(htpint(297))
    room = Room()
    room_list.append(room)

    create_room()

    return generate_output()