#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Reservation, Zimkateg

rline_list_data, Rline_list = create_model_like(Res_line, {"res_char":string, "rsvname":string, "kurzbez":string, "status_str":string})
reschanged_list_data, Reschanged_list = create_model("Reschanged_list", {"reslinnr":int})

def mk_resline_query_q1bl(pvilanguage:int, newflag:bool, chgnameflag:bool, inp_resno:int, rline_list_data:[Rline_list], reschanged_list_data:[Reschanged_list]):

    prepare_cache ([Reservation, Zimkateg])

    lvcarea:string = "mk-resline"
    rstat_list:List[string] = create_empty_list(13,"")
    res_line = reservation = zimkateg = None

    rline_list = reschanged_list = rline = None

    Rline = create_buffer("Rline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lvcarea, rstat_list, res_line, reservation, zimkateg
        nonlocal pvilanguage, newflag, chgnameflag, inp_resno
        nonlocal rline


        nonlocal rline_list, reschanged_list, rline

        return {"rline-list": rline_list_data, "reschanged-list": reschanged_list_data}

    rstat_list[0] = translateExtended ("Guaranted", lvcarea, "")
    rstat_list[1] = translateExtended ("6 PM", lvcarea, "")
    rstat_list[2] = translateExtended ("Tentative", lvcarea, "")
    rstat_list[3] = translateExtended ("WaitList", lvcarea, "")
    rstat_list[4] = ""
    rstat_list[5] = translateExtended ("Inhouse", lvcarea, "")
    rstat_list[6] = ""
    rstat_list[7] = translateExtended ("Departed", lvcarea, "")
    rstat_list[8] = translateExtended ("Cancelled", lvcarea, "")
    rstat_list[9] = translateExtended ("NoShow", lvcarea, "")
    rstat_list[10] = translateExtended ("ShareRes", lvcarea, "")
    rstat_list[11] = ""
    rstat_list[12] = translateExtended ("RmSharer", lvcarea, "")

    if newflag:

        reservation = get_cache (Reservation, {"resnr": [(eq, inp_resno)]})

        for rline in db_session.query(Rline).filter(
                 (Rline.resnr == inp_resno) & (Rline.active_flag <= 1) & (Rline.resstatus != 12) & (Rline.l_zuordnung[inc_value(2)] == 0)).order_by(Rline._recid).all():

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, rline.zikatnr)]})

            rline_list = query(rline_list_data, filters=(lambda rline_list: rline_list.resnr == rline.resnr and rline_list.reslinnr == rline.reslinnr), first=True)

            if not rline_list:
                rline_list = Rline_list()
                rline_list_data.append(rline_list)

            buffer_copy(rline, rline_list)
            rline_list.rsvname = reservation.name
            rline_list.status_str = rstat_list[rline.resstatus - 1]

            if zimkateg:
                rline_list.kurzbez = zimkateg.kurzbez

            reschanged_list = query(reschanged_list_data, filters=(lambda reschanged_list: reschanged_list.reslinnr == rline_list.reslinnr), first=True)

            if reschanged_list:
                rline_list.res_char = "*"

    if chgnameflag:

        for rline_list in query(rline_list_data):

            rline = db_session.query(Rline).filter(
                     (Rline.resnr == inp_resno) & (Rline.reslinnr == rline_list.reslinnr)).first()
            rline_list.name = rline.name


    return generate_output()