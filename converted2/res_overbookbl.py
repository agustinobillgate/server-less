#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from sqlalchemy import func
from models import Zimkateg, Zimmer, Res_line, Kontline, Queasy, Outorder

def res_overbookbl(pvilanguage:int, res_mode:string, inp_resnr:int, inp_reslinnr:int, inp_ankunft:date, inp_abreise:date, qty:int, rmcat:string, bed_setup:string, ask_it:bool):

    prepare_cache ([Zimkateg, Zimmer, Res_line, Kontline])

    overbook = False
    overmax = False
    overanz = 0
    overdate = None
    incl_allot = False
    msg_str = ""
    zimkateg_overbook = 0
    origcontcode:string = ""
    statcode:string = ""
    res_argt:string = ""
    curr_date:date = None
    i:int = 0
    anz:int = 0
    anz0:int = 0
    anzooo:int = 0
    anzalot:int = 0
    delta:int = 0
    maxzimmer:int = 0
    ci_date:date = None
    overbook_flag:bool = False
    do_it:bool = False
    lvcarea:string = "res-overbook"
    zimkateg = zimmer = res_line = kontline = queasy = outorder = None

    occ_list = None

    occ_list_data, Occ_list = create_model("Occ_list", {"datum":date, "anz_avail":int, "anz_alot":int, "anz_ooo":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal overbook, overmax, overanz, overdate, incl_allot, msg_str, zimkateg_overbook, origcontcode, statcode, res_argt, curr_date, i, anz, anz0, anzooo, anzalot, delta, maxzimmer, ci_date, overbook_flag, do_it, lvcarea, zimkateg, zimmer, res_line, kontline, queasy, outorder
        nonlocal pvilanguage, res_mode, inp_resnr, inp_reslinnr, inp_ankunft, inp_abreise, qty, rmcat, bed_setup, ask_it


        nonlocal occ_list
        nonlocal occ_list_data

        return {"overbook": overbook, "overmax": overmax, "overanz": overanz, "overdate": overdate, "incl_allot": incl_allot, "msg_str": msg_str, "zimkateg_overbook": zimkateg_overbook}

    def check_allotment_by_ratecode():

        nonlocal overbook, overmax, overanz, overdate, incl_allot, msg_str, zimkateg_overbook, origcontcode, statcode, res_argt, i, anz, anz0, anzooo, anzalot, delta, maxzimmer, ci_date, overbook_flag, do_it, lvcarea, zimkateg, zimmer, res_line, kontline, queasy, outorder
        nonlocal pvilanguage, res_mode, inp_resnr, inp_reslinnr, inp_ankunft, inp_abreise, qty, rmcat, bed_setup, ask_it


        nonlocal occ_list
        nonlocal occ_list_data

        occ_room:int = 0
        allotment:int = 0
        curr_i:int = 0
        rline_origcode:string = ""
        str:string = ""
        ratecode_found:bool = False
        doit_flag:bool = False
        curr_date:date = None
        zbuff = None
        rbuff = None
        Zbuff =  create_buffer("Zbuff",Zimkateg)
        Rbuff =  create_buffer("Rbuff",Res_line)

        if origcontcode == "" or statcode == "":

            return

        res_line = get_cache (Res_line, {"resnr": [(eq, inp_resnr)],"reslinnr": [(eq, inp_reslinnr)]})

        if res_line:

            if zimkateg.typ == 0:

                queasy = get_cache (Queasy, {"char1": [(eq, origcontcode)],"number1": [(eq, zimkateg.zikatnr)],"key": [(eq, 171)],"date1": [(eq, inp_ankunft)],"number3": [(ne, 0)]})
            else:

                queasy = get_cache (Queasy, {"char1": [(eq, origcontcode)],"number1": [(eq, zimkateg.typ)],"key": [(eq, 171)],"date1": [(eq, inp_ankunft)],"number3": [(ne, 0)]})

            if not ratecode_found:

                return
            for curr_date in date_range(inp_ankunft,inp_abreise - 1) :
                occ_room = 0

                for rbuff in db_session.query(Rbuff).filter(
                         (Rbuff.gastnr == res_line.gastnr) & (Rbuff.active_flag <= 1) & (Rbuff.ankunft <= curr_date) & (Rbuff.abreise > curr_date) & ((Rbuff.resstatus <= 6) & (Rbuff.resstatus != 3) & (Rbuff.resstatus != 4)) & (matches(Rbuff.zimmer_wunsch,("*$OrigCode$*")))).order_by(Rbuff._recid).all():
                    doit_flag = (rbuff.resnr != inp_resnr) or (rbuff.reslinnr != inp_reslinnr)

                    if doit_flag and zimkateg.typ == 0:

                        if rbuff.zikatnr != zimkateg.zikatnr:
                            doit_flag = False
                    else:

                        zbuff = get_cache (Zimkateg, {"zikatnr": [(eq, rbuff.zikatnr)]})

                        if zbuff.typ != zimkateg.typ:
                            doit_flag = False

                    if doit_flag:

                        if res_argt != rbuff.arrangement:
                            doit_flag = False

                    if doit_flag:
                        for curr_i in range(1,num_entries(rbuff.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(curr_i - 1, rbuff.zimmer_wunsch, ";")

                            if substring(str, 0, 10) == ("$OrigCode$").lower() :
                                rline_origcode = substring(str, 10)

                                if rline_origcode.lower()  == (origcontcode).lower() :
                                    occ_room = occ_room + rbuff.zimmeranz
                                break

                if (occ_room + qty) > allotment:

                    if msg_str == "":
                        msg_str = "&Q" + translateExtended ("allotment by Rate Code Overbooking found.", lvcarea, "") + chr_unicode(10) + to_string(curr_date) + " - " + translateExtended ("Actual Overbooking:", lvcarea, "") + " " + to_string(occ_room + qty - allotment) + chr_unicode(10)


                    else:
                        msg_str = msg_str + to_string(curr_date) + " - " + translateExtended ("Actual Overbooking:", lvcarea, "") + " " + to_string(occ_room + qty - allotment) + chr_unicode(10)

            if msg_str != "":
                msg_str = msg_str + translateExtended ("Do you wish to continue?", lvcarea, "")

    ci_date = get_output(htpdate(87))

    if num_entries(rmcat, ";") > 1:
        origcontcode = entry(1, rmcat, ";")
        statcode = entry(2, rmcat, ";")
        res_argt = entry(3, rmcat, ";")
        rmcat = entry(0, rmcat, ";")

    zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, rmcat)]})
    zimkateg_overbook = zimkateg.overbooking


    check_allotment_by_ratecode()

    for zimmer in db_session.query(Zimmer).filter(
             (Zimmer.zikatnr == zimkateg.zikatnr) & (Zimmer.sleeping)).order_by(Zimmer._recid).all():
        maxzimmer = maxzimmer + 1


    curr_date = inp_ankunft

    res_line = get_cache (Res_line, {"resnr": [(eq, inp_resnr)],"reslinnr": [(eq, inp_reslinnr)]})

    if res_line:

        if res_line.active_flag == 1:
            curr_date = ci_date
    while curr_date < inp_abreise:

        occ_list = query(occ_list_data, filters=(lambda occ_list: occ_list.datum == curr_date), first=True)

        if not occ_list:
            occ_list = Occ_list()
            occ_list_data.append(occ_list)

            occ_list.datum = curr_date
            occ_list.anz_avail = maxzimmer - qty

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.ankunft <= curr_date) & (Res_line.abreise > curr_date) & (Res_line.zikatnr == zimkateg.zikatnr)).order_by(Res_line._recid).all():

            if (res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("qci").lower()) and (res_line.resnr == inp_resnr and res_line.reslinnr == inp_reslinnr):
                pass
            else:
                do_it = False

            if res_line.zinr != "":

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                do_it = zimmer.sleeping

            if do_it:

                if res_line.kontignr >= 0:

                    if res_line.resnr == inp_resnr and res_line.reslinnr == inp_reslinnr:
                        occ_list.anz_avail = occ_list.anz_avail + res_line.zimmeranz


                    else:
                        occ_list.anz_avail = occ_list.anz_avail - res_line.zimmeranz

                if res_line.kontignr != 0:

                    if res_line.kontignr > 0:

                        kontline = get_cache (Kontline, {"kontignr": [(eq, res_line.kontignr)]})

                        if kontline and curr_date >= (ci_date + timedelta(days=kontline.ruecktage)):

                            queasy = get_cache (Queasy, {"key": [(eq, 147)],"number1": [(eq, kontline.gastnr)],"char1": [(eq, kontline.kontcode)]})

                            if not queasy:
                                occ_list.anz_alot = occ_list.anz_alot - res_line.zimmeranz

        for kontline in db_session.query(Kontline).filter(
                 (Kontline.gastnr > 0) & (Kontline.ankunft <= curr_date) & (Kontline.abreise >= curr_date) & (Kontline.zikatnr == zimkateg.zikatnr) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():

            if kontline.betriebsnr == 1:
                occ_list.anz_avail = occ_list.anz_avail - kontline.zimmeranz
            else:

                queasy = get_cache (Queasy, {"key": [(eq, 147)],"number1": [(eq, kontline.gastnr)],"char1": [(eq, kontline.kontcode)]})

                if not queasy and curr_date >= (ci_date + timedelta(days=kontline.ruecktage)):
                    occ_list.anz_alot = occ_list.anz_alot + kontline.zimmeranz

        outorder_obj_list = {}
        for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping) & (Zimmer.zikatnr == zimkateg.zikatnr)).filter(
                 (Outorder.gespstart <= curr_date) & (Outorder.gespende >= curr_date) & (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
            if outorder_obj_list.get(outorder._recid):
                continue
            else:
                outorder_obj_list[outorder._recid] = True


            occ_list.anz_ooo = occ_list.anz_ooo + 1


        curr_date = curr_date + timedelta(days=1)

    for occ_list in query(occ_list_data, sort_by=[("datum",False)]):

        if (occ_list.anz_avail + zimkateg_overbook - occ_list.anz_ooo) < 0:
            overanz = - (occ_list.anz_avail + zimkateg_overbook - occ_list.anz_ooo)
            overdate = occ_list.datum


            overbook = True

            if not overbook:
                overmax = True
            break

    if overbook:

        return generate_output()

    if not overmax:

        for occ_list in query(occ_list_data, sort_by=[("datum",False)]):

            if (occ_list.anz_avail + zimkateg_overbook - occ_list.anz_ooo - occ_list.anz_alot) < 0:
                overmax = True
                overanz = - (occ_list.anz_avail + zimkateg_overbook - occ_list.anz_ooo - occ_list.anz_alot)
                overdate = occ_list.datum
                incl_allot = True


                break


    return generate_output()