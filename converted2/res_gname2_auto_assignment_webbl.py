#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zimmer, Res_line, Queasy, Outorder

s_list_data, S_list = create_model("S_list", {"res_recid":int, "resstatus":int, "active_flag":int, "flag":int, "karteityp":int, "zimmeranz":int, "erwachs":int, "kind1":int, "kind2":int, "old_zinr":string, "name":string, "nat":string, "land":string, "zinr":string, "eta":string, "etd":string, "flight1":string, "flight2":string, "rmcat":string, "ankunft":date, "abreise":date, "zipreis":Decimal, "bemerk":string, "user_init":string})
active_roomlist_data, Active_roomlist = create_model_like(Zimmer, {"room_selected":bool})

def res_gname2_auto_assignment_webbl(s_list_data:[S_list], active_roomlist_data:[Active_roomlist], v_mode:int, location:string, froom:string, troom:string):

    prepare_cache ([Res_line])

    time_stamp_str:string = ""
    vbilldate:date = None
    zimmer = res_line = queasy = outorder = None

    s_list = active_roomlist = s1_list = s2_list = s1_list = s2_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal time_stamp_str, vbilldate, zimmer, res_line, queasy, outorder
        nonlocal v_mode, location, froom, troom


        nonlocal s_list, active_roomlist, s1_list, s2_list, s1_list, s2_list

        return {"s-list": s_list_data}

    def gettimestampwithms():

        nonlocal time_stamp_str, vbilldate, zimmer, res_line, queasy, outorder
        nonlocal v_mode, location, froom, troom


        nonlocal s_list, active_roomlist, s1_list, s2_list, s1_list, s2_list

        vdatetime:string = ""
        dtz1:datetime = None
        dtz2:datetime = None
        dtz1_str:string = ""
        epoch_millisecond:int = 0
        human_date:datetime = None
        dtz1 = get_current_datetime()
        dtz2 = 1970_01_01T00:00:00.000
        epoch_millisecond = get_interval(dtz1, dtz2, "milliseconds")
        human_date = add_interval(dtz2, epoch_millisecond, "milliseconds")
        time_stamp_str = to_string(human_date)
        return time_stamp_str


    def auto_assignment():

        nonlocal time_stamp_str, vbilldate, zimmer, res_line, queasy, outorder
        nonlocal v_mode, location, froom, troom


        nonlocal s_list, active_roomlist, s1_list, s2_list, s1_list, s2_list

        rline = None
        resline = None
        queasy_359 = None
        last_zinr:string = ""
        do_it:bool = False
        found:bool = False
        S1_list = S_list
        s1_list_data = s_list_data
        S2_list = S_list
        s2_list_data = s_list_data
        Rline =  create_buffer("Rline",Res_line)
        Resline =  create_buffer("Resline",Res_line)
        Queasy_359 =  create_buffer("Queasy_359",Queasy)

        for s1_list in query(s1_list_data, filters=(lambda s1_list: s1_list.zinr == "" and s1_list.resstatus != 11 and s1_list.zimmeranz == 1)):

            rline = get_cache (Res_line, {"_recid": [(eq, s1_list.res_recid)]})
            found = False

            if location != "":

                zimmer = get_cache (Zimmer, {"code": [(eq, location)],"zinr": [(ge, froom),(le, troom),(gt, last_zinr)],"zikatnr": [(eq, rline.zikatnr)],"setup": [(eq, rline.setup)]})
            else:

                zimmer = get_cache (Zimmer, {"zinr": [(ge, froom),(le, troom),(gt, last_zinr)],"zikatnr": [(eq, rline.zikatnr)],"setup": [(eq, rline.setup)]})
            while None != zimmer and not found:
                do_it = True

                if etage > 0 and (etage != zimmer.etage):
                    do_it = False

                if do_it:

                    outorder = db_session.query(Outorder).filter(
                             (Outorder.zinr == zimmer.zinr) & (Outorder.betriebsnr != rline.resnr) & (((rline.ankunft >= gespstart) & (rline.ankunft <= Outorder.gespende)) | ((rline.abreise > gespstart) & (rline.abreise <= Outorder.gespende)) | ((Outorder.gespstart >= rline.ankunft) & (Outorder.gespstart < rline.abreise)) | ((Outorder.gespende >= rline.ankunft) & (Outorder.gespende <= rline.abreise)))).first()

                    if outorder:
                        do_it = False

                if do_it:

                    resline = db_session.query(Resline).filter(
                             (Resline._recid != rline._recid) & (Resline.resstatus <= 6) & (Resline.active_flag <= 1) & (Resline.zinr == zimmer.zinr) & (((rline.ankunft >= Resline.ankunft) & (rline.ankunft < Resline.abreise)) | ((rline.abreise > Resline.ankunft) & (rline.abreise <= Resline.abreise)) | ((Resline.ankunft >= rline.ankunft) & (Resline.ankunft < rline.abreise)) | ((Resline.abreise > rline.ankunft) & (Resline.abreise <= rline.abreise)))).first()

                    if resline:
                        do_it = False

                if do_it:
                    s1_list.zinr = zimmer.zinr
                    last_zinr = zimmer.zinr
                    found = True

                    if s1_list.resstatus <= 5:

                        queasy_359 = db_session.query(Queasy_359).filter(
                                 (Queasy_359.key == 359) & (Queasy_359.number1 == rline.resnr) & (Queasy_359.number2 == rline.reslinnr) & (Queasy_359.number3 == 1)).first()

                        if queasy_359:
                            db_session.delete(queasy_359)
                            pass

                        queasy = get_cache (Queasy, {"key": [(eq, 359)],"char1": [(eq, s1_list.zinr)],"number1": [(eq, rline.resnr)],"number2": [(eq, rline.reslinnr)],"number3": [(eq, 1)]})

                        if not queasy:
                            queasy = Queasy()
                            db_session.add(queasy)

                            queasy.key = 359
                            queasy.char1 = s1_list.zinr
                            queasy.char2 = s1_list.user_init
                            queasy.char3 = getTimestampWithMs()
                            queasy.number1 = rline.resnr
                            queasy.number2 = rline.reslinnr
                            queasy.number3 = 1
                            queasy.date1 = rline.ankunft
                            queasy.date2 = rline.abreise
                            queasy.logi1 = True


                else:

                    if location != "":

                        curr_recid = zimmer._recid
                        zimmer = db_session.query(Zimmer).filter(
                                 (Zimmer.code == (location).lower()) & (Zimmer.zinr >= (froom).lower()) & (Zimmer.zinr <= (troom).lower()) & (Zimmer.zikatnr == rline.zikatnr) & (Zimmer.setup == rline.setup) & (Zimmer.zinr > (last_zinr).lower()) & (Zimmer._recid > curr_recid)).first()
                    else:

                        curr_recid = zimmer._recid
                        zimmer = db_session.query(Zimmer).filter(
                                 (Zimmer.zinr >= (froom).lower()) & (Zimmer.zinr <= (troom).lower()) & (Zimmer.zikatnr == rline.zikatnr) & (Zimmer.setup == rline.setup) & (Zimmer.zinr > (last_zinr).lower()) & (Zimmer._recid > curr_recid)).first()
        last_zinr = ""

        for s1_list in query(s1_list_data, filters=(lambda s1_list: s1_list.zinr == "" and s1_list.active_flag == 0 and s1_list.resstatus != 11)):

            rline = get_cache (Res_line, {"_recid": [(eq, s1_list.res_recid)]})
            found = False

            if location != "":

                zimmer = get_cache (Zimmer, {"code": [(eq, location)],"zinr": [(ge, froom),(le, troom),(gt, last_zinr)],"zikatnr": [(eq, rline.zikatnr)],"setup": [(ne, rline.setup)]})
            else:

                zimmer = get_cache (Zimmer, {"zinr": [(ge, froom),(le, troom),(gt, last_zinr)],"zikatnr": [(eq, rline.zikatnr)],"setup": [(ne, rline.setup)]})
            while None != zimmer and not found:
                do_it = True

                if etage > 0 and (etage != zimmer.etage):
                    do_it = False

                if do_it:

                    outorder = db_session.query(Outorder).filter(
                             (Outorder.zinr == zimmer.zinr) & (Outorder.betriebsnr != rline.resnr) & (((rline.ankunft >= gespstart) & (rline.ankunft <= Outorder.gespende)) | ((rline.abreise > gespstart) & (rline.abreise <= Outorder.gespende)) | ((Outorder.gespstart >= rline.ankunft) & (Outorder.gespstart < rline.abreise)) | ((Outorder.gespende >= rline.ankunft) & (Outorder.gespende <= rline.abreise)))).first()

                    if outorder:
                        do_it = False

                if do_it:

                    resline = db_session.query(Resline).filter(
                             (Resline._recid != rline._recid) & (Resline.resstatus <= 6) & (Resline.active_flag <= 1) & (Resline.zinr == zimmer.zinr) & (((rline.ankunft >= Resline.ankunft) & (rline.ankunft < Resline.abreise)) | ((rline.abreise > Resline.ankunft) & (rline.abreise <= Resline.abreise)) | ((Resline.ankunft >= rline.ankunft) & (Resline.ankunft < rline.abreise)) | ((Resline.abreise > rline.ankunft) & (Resline.abreise <= rline.abreise)))).first()

                    if resline:
                        do_it = False

                if do_it:

                    s2_list = query(s2_list_data, filters=(lambda s2_list: s2_list.zinr == zimmer.zinr), first=True)

                    if s2_list:
                        do_it = False

                if do_it:
                    s1_list.zinr = zimmer.zinr
                    last_zinr = zimmer.zinr
                    found = True

                    if s1_list.resstatus <= 5:

                        queasy_359 = db_session.query(Queasy_359).filter(
                                 (Queasy_359.key == 359) & (Queasy_359.number1 == rline.resnr) & (Queasy_359.number2 == rline.reslinnr) & (Queasy_359.number3 == 1)).first()

                        if queasy_359:
                            db_session.delete(queasy_359)
                            pass

                        queasy = get_cache (Queasy, {"key": [(eq, 359)],"char1": [(eq, s1_list.zinr)],"number1": [(eq, rline.resnr)],"number2": [(eq, rline.reslinnr)],"number3": [(eq, 1)]})

                        if not queasy:
                            queasy = Queasy()
                            db_session.add(queasy)

                            queasy.key = 359
                            queasy.char1 = s1_list.zinr
                            queasy.char2 = s1_list.user_init
                            queasy.char3 = getTimestampWithMs()
                            queasy.number1 = rline.resnr
                            queasy.number2 = rline.reslinnr
                            queasy.number3 = 1
                            queasy.date1 = rline.ankunft
                            queasy.date2 = rline.abreise
                            queasy.logi1 = True


                else:

                    if location != "":

                        curr_recid = zimmer._recid
                        zimmer = db_session.query(Zimmer).filter(
                                 (Zimmer.code == (location).lower()) & (Zimmer.zinr >= (froom).lower()) & (Zimmer.zinr <= (troom).lower()) & (Zimmer.zikatnr == rline.zikatnr) & (Zimmer.setup != rline.setup) & (Zimmer.zinr > (last_zinr).lower()) & (Zimmer._recid > curr_recid)).first()
                    else:

                        curr_recid = zimmer._recid
                        zimmer = db_session.query(Zimmer).filter(
                                 (Zimmer.zinr >= (froom).lower()) & (Zimmer.zinr <= (troom).lower()) & (Zimmer.zikatnr == rline.zikatnr) & (Zimmer.setup != rline.setup) & (Zimmer.zinr > (last_zinr).lower()) & (Zimmer._recid > curr_recid)).first()


    def auto_assignmen_with_selectedroom():

        nonlocal time_stamp_str, vbilldate, zimmer, res_line, queasy, outorder
        nonlocal v_mode, location, froom, troom


        nonlocal s_list, active_roomlist, s1_list, s2_list, s1_list, s2_list

        rline = None
        resline = None
        queasy_359 = None
        last_zinr:string = ""
        do_it:bool = False
        found:bool = False
        S1_list = S_list
        s1_list_data = s_list_data
        S2_list = S_list
        s2_list_data = s_list_data
        Rline =  create_buffer("Rline",Res_line)
        Resline =  create_buffer("Resline",Res_line)
        Queasy_359 =  create_buffer("Queasy_359",Queasy)

        for s1_list in query(s1_list_data, filters=(lambda s1_list: s1_list.zinr == "" and s1_list.resstatus != 11 and s1_list.zimmeranz == 1)):

            rline = get_cache (Res_line, {"_recid": [(eq, s1_list.res_recid)]})
            found = False

            active_roomlist = query(active_roomlist_data, filters=(lambda active_roomlist: active_roomlist.zikatnr == rline.zikatnr and active_roomlist.room_selected and active_roomlist.setup == rline.setup and active_roomlist.zinr.lower()  > (last_zinr).lower()), first=True)
            while None != active_roomlist and not found:
                do_it = True

                if do_it:

                    outorder = db_session.query(Outorder).filter(
                             (Outorder.zinr == active_roomlist.zinr) & (Outorder.betriebsnr != rline.resnr) & (((rline.ankunft >= gespstart) & (rline.ankunft <= Outorder.gespende)) | ((rline.abreise > gespstart) & (rline.abreise <= Outorder.gespende)) | ((Outorder.gespstart >= rline.ankunft) & (Outorder.gespstart < rline.abreise)) | ((Outorder.gespende >= rline.ankunft) & (Outorder.gespende <= rline.abreise)))).first()

                    if outorder:
                        do_it = False

                if do_it:

                    resline = db_session.query(Resline).filter(
                             (Resline._recid != rline._recid) & (Resline.resstatus <= 6) & (Resline.active_flag <= 1) & (Resline.zinr == active_roomlist.zinr) & (((rline.ankunft >= Resline.ankunft) & (rline.ankunft < Resline.abreise)) | ((rline.abreise > Resline.ankunft) & (rline.abreise <= Resline.abreise)) | ((Resline.ankunft >= rline.ankunft) & (Resline.ankunft < rline.abreise)) | ((Resline.abreise > rline.ankunft) & (Resline.abreise <= rline.abreise)))).first()

                    if resline:
                        do_it = False

                if do_it:
                    s1_list.zinr = active_roomlist.zinr
                    last_zinr = active_roomlist.zinr
                    found = True

                    if s1_list.resstatus <= 5:

                        queasy_359 = db_session.query(Queasy_359).filter(
                                 (Queasy_359.key == 359) & (Queasy_359.number1 == rline.resnr) & (Queasy_359.number2 == rline.reslinnr) & (Queasy_359.number3 == 1)).first()

                        if queasy_359:
                            db_session.delete(queasy_359)
                            pass

                        queasy = get_cache (Queasy, {"key": [(eq, 359)],"char1": [(eq, s1_list.zinr)],"number1": [(eq, rline.resnr)],"number2": [(eq, rline.reslinnr)],"number3": [(eq, 1)]})

                        if not queasy:
                            queasy = Queasy()
                            db_session.add(queasy)

                            queasy.key = 359
                            queasy.char1 = s1_list.zinr
                            queasy.char2 = s1_list.user_init
                            queasy.char3 = getTimestampWithMs()
                            queasy.number1 = rline.resnr
                            queasy.number2 = rline.reslinnr
                            queasy.number3 = 1
                            queasy.date1 = rline.ankunft
                            queasy.date2 = rline.abreise
                            queasy.logi1 = True


                else:

                    active_roomlist = query(active_roomlist_data, filters=(lambda active_roomlist: active_roomlist.zikatnr == rline.zikatnr and active_roomlist.room_selected and active_roomlist.setup == rline.setup and active_roomlist.zinr.lower()  > (last_zinr).lower()), next=True)
        last_zinr = ""

        for s1_list in query(s1_list_data, filters=(lambda s1_list: s1_list.zinr == "" and s1_list.active_flag == 0 and s1_list.resstatus != 11)):

            rline = get_cache (Res_line, {"_recid": [(eq, s1_list.res_recid)]})
            found = False

            active_roomlist = query(active_roomlist_data, filters=(lambda active_roomlist: active_roomlist.zikatnr == rline.zikatnr and active_roomlist.room_selected and active_roomlist.setup != rline.setup and active_roomlist.zinr.lower()  > (last_zinr).lower()), first=True)
            while None != active_roomlist and not found:
                do_it = True

                if do_it:

                    outorder = db_session.query(Outorder).filter(
                             (Outorder.zinr == active_roomlist.zinr) & (Outorder.betriebsnr != rline.resnr) & (((rline.ankunft >= gespstart) & (rline.ankunft <= Outorder.gespende)) | ((rline.abreise > gespstart) & (rline.abreise <= Outorder.gespende)) | ((Outorder.gespstart >= rline.ankunft) & (Outorder.gespstart < rline.abreise)) | ((Outorder.gespende >= rline.ankunft) & (Outorder.gespende <= rline.abreise)))).first()

                    if outorder:
                        do_it = False

                if do_it:

                    resline = db_session.query(Resline).filter(
                             (Resline._recid != rline._recid) & (Resline.resstatus <= 6) & (Resline.active_flag <= 1) & (Resline.zinr == active_roomlist.zinr) & (((rline.ankunft >= Resline.ankunft) & (rline.ankunft < Resline.abreise)) | ((rline.abreise > Resline.ankunft) & (rline.abreise <= Resline.abreise)) | ((Resline.ankunft >= rline.ankunft) & (Resline.ankunft < rline.abreise)) | ((Resline.abreise > rline.ankunft) & (Resline.abreise <= rline.abreise)))).first()

                    if resline:
                        do_it = False

                if do_it:

                    s2_list = query(s2_list_data, filters=(lambda s2_list: s2_list.zinr == active_roomlist.zinr), first=True)

                    if s2_list:
                        do_it = False

                if do_it:
                    s1_list.zinr = active_roomlist.zinr
                    last_zinr = active_roomlist.zinr
                    found = True

                    if s1_list.resstatus <= 5:

                        queasy_359 = db_session.query(Queasy_359).filter(
                                 (Queasy_359.key == 359) & (Queasy_359.number1 == rline.resnr) & (Queasy_359.number2 == rline.reslinnr) & (Queasy_359.number3 == 1)).first()

                        if queasy_359:
                            db_session.delete(queasy_359)
                            pass

                        queasy = get_cache (Queasy, {"key": [(eq, 359)],"char1": [(eq, s1_list.zinr)],"number1": [(eq, rline.resnr)],"number2": [(eq, rline.reslinnr)],"number3": [(eq, 1)]})

                        if not queasy:
                            queasy = Queasy()
                            db_session.add(queasy)

                            queasy.key = 359
                            queasy.char1 = s1_list.zinr
                            queasy.char2 = s1_list.user_init
                            queasy.char3 = getTimestampWithMs()
                            queasy.number1 = rline.resnr
                            queasy.number2 = rline.reslinnr
                            queasy.number3 = 1
                            queasy.date1 = rline.ankunft
                            queasy.date2 = rline.abreise
                            queasy.logi1 = True


                else:

                    active_roomlist = query(active_roomlist_data, filters=(lambda active_roomlist: active_roomlist.zikatnr == rline.zikatnr and active_roomlist.room_selected and active_roomlist.setup != rline.setup and active_roomlist.zinr.lower()  > (last_zinr).lower()), next=True)

    if v_mode == 1:
        auto_assignment()
    else:
        auto_assignmen_with_selectedroom()

    return generate_output()