#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Bill, Queasy, Guest

def ts_rzinr_return_zinr_1bl(pvilanguage:int, case_type:int, room:string, dept:int, dept_mbar:int, dept_ldry:int):

    prepare_cache ([Res_line, Bill, Queasy, Guest])

    zinr = ""
    lastzinr = ""
    comments = ""
    resline = False
    q1_list_data = []
    lvcarea:string = "TS-rzinr"
    res_line = bill = queasy = guest = None

    q1_list = rline = bbuff = None

    q1_list_data, Q1_list = create_model("Q1_list", {"resnr":int, "zinr":string, "code":string, "resstatus":int, "erwachs":int, "kind1":int, "gratis":int, "bemerk":string, "billnr":int, "g_name":string, "vorname1":string, "anrede1":string, "anredefirma":string, "bill_name":string, "ankunft":date, "abreise":date, "nation1":string, "parent_nr":int, "reslinnr":int, "resname":string, "name_bg_col":int, "name_fg_col":int, "bill_bg_col":int, "bill_fg_col":int}, {"name_bg_col": 15, "bill_bg_col": 15})

    Rline = create_buffer("Rline",Res_line)
    Bbuff = create_buffer("Bbuff",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal zinr, lastzinr, comments, resline, q1_list_data, lvcarea, res_line, bill, queasy, guest
        nonlocal pvilanguage, case_type, room, dept, dept_mbar, dept_ldry
        nonlocal rline, bbuff


        nonlocal q1_list, rline, bbuff
        nonlocal q1_list_data

        return {"zinr": zinr, "lastzinr": lastzinr, "comments": comments, "resline": resline, "q1-list": q1_list_data}

    if case_type == 1:

        rline = get_cache (Res_line, {"active_flag": [(eq, 1)],"pin_code": [(eq, room)],"resstatus": [(ne, 12)]})

        if not rline:

            queasy = get_cache (Queasy, {"key": [(eq, 16)],"char1": [(eq, room)]})

            if queasy:

                rline = get_cache (Res_line, {"active_flag": [(eq, 1)],"resnr": [(eq, queasy.number1)],"reslinnr": [(eq, queasy.number2)]})

        if rline:
            resline = True
            zinr = rline.zinr
            lastzinr = zinr
            comments = translateExtended ("A/Ch/CO:", lvcarea, "") + " " +\
                    to_string(rline.erwachs) + "/" +\
                    to_string(rline.kind1) + "/" +\
                    to_string(rline.gratis) + chr_unicode(10) +\
                    rline.bemerk

            res_line_obj_list = {}
            res_line = Res_line()
            guest = Guest()
            bbuff = Bill()
            for res_line.resnr, res_line.zinr, res_line.code, res_line.resstatus, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.bemerk, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.nation1, guest._recid, bbuff.billnr, bbuff.name, bbuff.parent_nr, bbuff._recid in db_session.query(Res_line.resnr, Res_line.zinr, Res_line.code, Res_line.resstatus, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.bemerk, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.nation1, Guest._recid, Bbuff.billnr, Bbuff.name, Bbuff.parent_nr, Bbuff._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).join(Bbuff,(Bbuff.resnr == Res_line.resnr) & (Bbuff.parent_nr == rline.reslinnr)).filter(
                     (Res_line.zinr == (zinr).lower()) & (Res_line.active_flag == 1) & (Res_line.resnr == rline.resnr)).order_by(Res_line.reslinnr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                q1_list = Q1_list()
                q1_list_data.append(q1_list)

                q1_list.resnr = res_line.resnr
                q1_list.zinr = res_line.zinr
                q1_list.code = res_line.code
                q1_list.resstatus = res_line.resstatus
                q1_list.erwachs = res_line.erwachs
                q1_list.kind1 = res_line.kind1
                q1_list.gratis = res_line.gratis
                q1_list.bemerk = res_line.bemerk
                q1_list.billnr = bbuff.billnr
                q1_list.g_name = guest.name
                q1_list.vorname1 = guest.vorname1
                q1_list.anrede1 = guest.anrede1
                q1_list.anredefirma = guest.anredefirma
                q1_list.bill_name = bbuff.name
                q1_list.ankunft = res_line.ankunft
                q1_list.abreise = res_line.abreise
                q1_list.nation1 = guest.nation1
                q1_list.parent_nr = bbuff.parent_nr
                q1_list.reslinnr = res_line.reslinnr
                q1_list.resname = res_line.name

                if (dept != dept_mbar and dept != dept_ldry):

                    if res_line.code != "":

                        queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

                        if queasy and queasy.logi1:
                            q1_list.name_bg_col = 12
                            q1_list.name_fg_col = 15

                if res_line.resstatus == 12:
                    q1_list.bill_bg_col = 2
                    q1_list.bill_fg_col = 15

    elif case_type == 2:
        zinr = room
        lastzinr = zinr

        res_line_obj_list = {}
        res_line = Res_line()
        guest = Guest()
        bbuff = Bill()
        for res_line.resnr, res_line.zinr, res_line.code, res_line.resstatus, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.bemerk, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.nation1, guest._recid, bbuff.billnr, bbuff.name, bbuff.parent_nr, bbuff._recid in db_session.query(Res_line.resnr, Res_line.zinr, Res_line.code, Res_line.resstatus, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.bemerk, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.nation1, Guest._recid, Bbuff.billnr, Bbuff.name, Bbuff.parent_nr, Bbuff._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).join(Bbuff,(Bbuff.resnr == Res_line.resnr) & (Bbuff.parent_nr == Res_line.reslinnr)).filter(
                 (Res_line.zinr == (room).lower()) & (Res_line.active_flag == 1)).order_by(Res_line.reslinnr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            resline = True
            q1_list = Q1_list()
            q1_list_data.append(q1_list)

            q1_list.resnr = res_line.resnr
            q1_list.zinr = res_line.zinr
            q1_list.code = res_line.code
            q1_list.resstatus = res_line.resstatus
            q1_list.erwachs = res_line.erwachs
            q1_list.kind1 = res_line.kind1
            q1_list.gratis = res_line.gratis
            q1_list.bemerk = res_line.bemerk
            q1_list.billnr = bbuff.billnr
            q1_list.g_name = guest.name
            q1_list.vorname1 = guest.vorname1
            q1_list.anrede1 = guest.anrede1
            q1_list.anredefirma = guest.anredefirma
            q1_list.bill_name = bbuff.name
            q1_list.ankunft = res_line.ankunft
            q1_list.abreise = res_line.abreise
            q1_list.nation1 = guest.nation1
            q1_list.parent_nr = bbuff.parent_nr
            q1_list.reslinnr = res_line.reslinnr
            q1_list.resname = res_line.name

            if (dept != dept_mbar and dept != dept_ldry):

                if res_line.code != "":

                    queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

                    if queasy and queasy.logi1:
                        q1_list.name_bg_col = 12
                        q1_list.name_fg_col = 15

            if res_line.resstatus == 12:
                q1_list.bill_bg_col = 2
                q1_list.bill_fg_col = 15


            comments = translateExtended ("A/Ch/CO:", lvcarea, "") + " " + to_string(res_line.erwachs) + "/" + to_string(res_line.kind1) + "/" + to_string(res_line.gratis) + chr_unicode(10) + res_line.bemerk

    return generate_output()