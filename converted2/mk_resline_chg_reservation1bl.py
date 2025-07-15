from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Res_line, Zimkateg, Outorder, Queasy, Reslin_queasy, Guest, Nation, Arrangement

reslin_list_list, Reslin_list = create_model_like(Res_line)

def mk_resline_chg_reservation1bl(inp_resnr:int, inp_reslinnr:int, inp_resno:int, oral_flag:bool, reslin_list_list:[Reslin_list]):
    avail_outorder = False
    bill_instruct = 0
    instruct_str = ""
    prog_str = ""
    price_bcol = 0
    accompany_gastnr = 0
    accompany_gastnr2 = 0
    accompany_gastnr3 = 0
    comments = ""
    arrday = ""
    depday = ""
    guestname = ""
    restype = 0
    restype0 = 0
    sharer = False
    billname = ""
    billadress = ""
    billcity = ""
    billland = ""
    name_editor = ""
    zikatstr = ""
    curr_cat = ""
    curr_arg = ""
    reslinno = 0
    curr_resline_list = []
    zimkateg1_list = []
    weekdays:str = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun" - 1]
    res_line = zimkateg = outorder = queasy = reslin_queasy = guest = nation = arrangement = None

    curr_resline = reslin_list = zimkateg1 = buff_curr_resline = resline = None

    curr_resline_list, Curr_resline = create_model_like(Res_line)
    zimkateg1_list, Zimkateg1 = create_model_like(Zimkateg)

    Buff_curr_resline = create_buffer("Buff_curr_resline",Res_line)
    Resline = create_buffer("Resline",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_outorder, bill_instruct, instruct_str, prog_str, price_bcol, accompany_gastnr, accompany_gastnr2, accompany_gastnr3, comments, arrday, depday, guestname, restype, restype0, sharer, billname, billadress, billcity, billland, name_editor, zikatstr, curr_cat, curr_arg, reslinno, curr_resline_list, zimkateg1_list, weekdays, res_line, zimkateg, outorder, queasy, reslin_queasy, guest, nation, arrangement
        nonlocal inp_resnr, inp_reslinnr, inp_resno, oral_flag
        nonlocal buff_curr_resline, resline


        nonlocal curr_resline, reslin_list, zimkateg1, buff_curr_resline, resline
        nonlocal curr_resline_list, reslin_list_list, zimkateg1_list
        return {"avail_outorder": avail_outorder, "bill_instruct": bill_instruct, "instruct_str": instruct_str, "prog_str": prog_str, "price_bcol": price_bcol, "accompany_gastnr": accompany_gastnr, "accompany_gastnr2": accompany_gastnr2, "accompany_gastnr3": accompany_gastnr3, "comments": comments, "arrday": arrday, "depday": depday, "guestname": guestname, "restype": restype, "restype0": restype0, "sharer": sharer, "billname": billname, "billadress": billadress, "billcity": billcity, "billland": billland, "name_editor": name_editor, "zikatstr": zikatstr, "curr_cat": curr_cat, "curr_arg": curr_arg, "reslinno": reslinno, "curr-resline": curr_resline_list, "zimkateg1": zimkateg1_list, "reslin-list": reslin_list_list}

    reslin_list = query(reslin_list_list, first=True)

    res_line = db_session.query(Res_line).filter(
             (Res_line.resnr == inp_resnr) & (Res_line.reslinnr == inp_reslinnr)).first()

    if res_line.resstatus == 1 and res_line.zinr != "":

        outorder = db_session.query(Outorder).filter(
                 (Outorder.zinr == res_line.zinr) & (Outorder.betriebsnr == res_line.resnr)).first()

        if outorder:
            avail_outorder = True

    if res_line.code == "" or res_line.code.lower()  == ("0").lower() :
        bill_instruct = 0
    else:
        bill_instruct = to_int(res_line.code)

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 9) & (Queasy.number1 == bill_instruct)).first()

        if queasy:
            instruct_str = queasy.char1

    resline = db_session.query(Resline).filter(
             (Resline.resnr == res_line.resnr) & (Resline.active_flag <= 1) & (Resline.kontakt_nr == res_line.reslinnr) & (Resline.l_zuordnung[inc_value(2)] == 1)).first()

    if resline:
        accompany_gastnr = resline.gastnrmember

    if resline:

        curr_recid = resline._recid
        resline = db_session.query(Resline).filter(
                 (Resline.resnr == res_line.resnr) & (Resline.active_flag <= 1) & (Resline.kontakt_nr == res_line.reslinnr) & (Resline.l_zuordnung[inc_value(2)] == 1)).filter(Resline._recid > curr_recid).first()

    if resline:
        accompany_gastnr2 = resline.gastnrmember

    if resline:

        curr_recid = resline._recid
        resline = db_session.query(Resline).filter(
                 (Resline.resnr == res_line.resnr) & (Resline.active_flag <= 1) & (Resline.kontakt_nr == res_line.reslinnr) & (Resline.l_zuordnung[inc_value(2)] == 1)).filter(Resline._recid > curr_recid).first()

    if resline:
        accompany_gastnr3 = resline.gastnrmember

    buff_curr_resline = db_session.query(Buff_curr_resline).filter(
             (Buff_curr_resline._recid == res_line._recid)).first()
    curr_resline = Curr_resline()
    curr_resline_list.append(curr_resline)

    buffer_copy(buff_curr_resline, curr_resline)

    reslin_queasy = db_session.query(Reslin_queasy).filter(
             (func.lower(Reslin_queasy.key) == ("rate-prog").lower()) & (Reslin_queasy.number1 == inp_resno) & (Reslin_queasy.number2 == 0) & (Reslin_queasy.char1 == "") & (Reslin_queasy.reslinnr == 1)).first()

    if reslin_queasy:
        prog_str = reslin_queasy.char3
        price_bcol = 12
    else:
        prog_str = ""
        price_bcol = 9
    buffer_copy(res_line, reslin_list)
    comments = res_line.bemerk
    arrday = weekdays[get_weekday(reslin_list.ankunft) - 1]
    depday = weekdays[get_weekday(reslin_list.abreise) - 1]
    guestname = res_line.name

    if oral_flag:
        restype = res_line.resstatus
    else:
        restype0 = res_line.resstatus

    if res_line.resstatus == 11:
        sharer = True
    else:
        sharer = False

    guest = db_session.query(Guest).filter(
             (Guest.gastnr == res_line.gastnrpay)).first()
    billname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
    billadress = guest.adresse1
    billcity = guest.wohnort + " " + guest.plz

    nation = db_session.query(Nation).filter(
             (Nation.kurzbez == guest.land)).first()

    if nation:
        billland = nation.bezeich
    name_editor = billname + chr (10) + chr (10) + billadress + chr (10) + billcity + chr (10) + chr (10) + billland

    arrangement = db_session.query(Arrangement).filter(
             (Arrangement.arrangement == res_line.arrangement)).first()

    zimkateg = db_session.query(Zimkateg).filter(
             (Zimkateg.zikatnr == res_line.zikatnr)).first()
    zikatstr = zimkateg.kurzbez
    curr_cat = zikatstr
    curr_arg = res_line.arrangement
    reslinno = res_line.reslinnr

    zimkateg = db_session.query(Zimkateg).filter(
             (Zimkateg.zikatnr == res_line.l_zuordnung[0)]).first()

    if zimkateg:
        zimkateg1 = Zimkateg1()
        zimkateg1_list.append(zimkateg1)

        buffer_copy(zimkateg, zimkateg1)

    return generate_output()