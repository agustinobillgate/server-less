#using conversion tools version: 1.0.0.117
"""_yusufwijasena_28/10/2025

    Ticket ID: 8A0408
        _remark_:   - fix python indentation
                    - fix var declaration
                    - changed string to str
                    - fix ("string").lower() to "string"
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Zimmer, Outorder, Res_line, Guest, Reslin_queasy, Guestseg, Segment

def hk_zimaid_webbl(pvilanguage:int):

    prepare_cache ([Htparam, Zimmer, Outorder, Res_line, Guest, Reslin_queasy, Guestseg, Segment])

    output_list_data = []
    lvcarea:str = "hk-zimaid"
    stat_list:List[str] = create_empty_list(10,"")
    stat_list1:List[str] = ["VC", "VU", "VD", "ED", "OD", "OC", "OO", "OM", "DD", "OS", "EA"]
    vip_nr:List[int] = create_empty_list(10,0)
    resbemerk = ""
    htparam = zimmer = outorder = res_line = guest = reslin_queasy = guestseg = segment = None

    output_list = out_list = None

    output_list_data, Output_list = create_model(
        "Output_list", {
            "personal":bool, 
            "reihenfolge":int, 
            "selected":bool, 
            "cleanflag":bool, 
            "odd_even":int, 
            "flag":int, 
            "zinr":str, 
            "rstat":str, 
            "rstat1":str, 
            "departed":str, 
            "gstat":str, 
            "floor":int, 
            "code":str, 
            "inactive":str, 
            "ldry":str, 
            "towel":str, 
            "kbezeich":str, 
            "arrival":bool, 
            "ankunft":date, 
            "abreise":date, 
            "nation":str, 
            "zistatus":int, 
            "gname":str, 
            "resname":str,
            "bemerk":str,
            "rsv_flag":bool,
            "co_time":str,
            "vip":str,
            "flight_nr":str,
            "segm_type":int
            }, {
                "flag": 1
                })

    Out_list = Output_list
    out_list_data = output_list_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, lvcarea, stat_list, stat_list1, vip_nr, resbemerk, htparam, zimmer, outorder, res_line, guest, reslin_queasy, guestseg, segment
        nonlocal pvilanguage
        nonlocal out_list
        nonlocal output_list, out_list
        nonlocal output_list_data

        return {
            "output-list": output_list_data
            }

    def fill_vipnr():
        nonlocal output_list_data, lvcarea, stat_list, stat_list1, vip_nr, resbemerk, htparam, zimmer, outorder, res_line, guest, reslin_queasy, guestseg, segment
        nonlocal pvilanguage
        nonlocal out_list
        nonlocal output_list, out_list
        nonlocal output_list_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})
        vip_nr[0] = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})
        vip_nr[1] = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})
        vip_nr[2] = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})
        vip_nr[3] = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})
        vip_nr[4] = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})
        vip_nr[5] = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})
        vip_nr[6] = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})
        vip_nr[7] = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})
        vip_nr[8] = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 712)]})
        vip_nr[9] = htparam.finteger


    def fill_list():
        nonlocal output_list_data, lvcarea, stat_list, stat_list1, vip_nr, resbemerk, htparam, zimmer, outorder, res_line, guest, reslin_queasy, guestseg, segment
        nonlocal pvilanguage
        nonlocal out_list
        nonlocal output_list, out_list
        nonlocal output_list_data

        anz:int = 0
        ci_date:date 
        off_market:bool = False
        ldry:int = 0
        towel:int = 0
        c_vip = ""
        vip_type:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
        ci_date = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 159)]})
        ldry = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 218)]})
        towel = htparam.finteger

        for zimmer in db_session.query(Zimmer).filter(
                (((Zimmer.zistatus >= 0) & (Zimmer.zistatus <= 6)) | (Zimmer.zistatus == 8))).order_by(Zimmer.zinr).all():
            off_market = False

            outorder = get_cache (Outorder, {
                "zinr": [(eq, zimmer.zinr)],
                "betriebsnr": [(eq, 2)],
                "gespstart": [(le, ci_date)],
                "gespende": [(ge, ci_date)]})

            if outorder:
                off_market = True
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.reihenfolge = zimmer.reihenfolge
            output_list.personal = zimmer.personal
            output_list.floor = zimmer.etage
            output_list.zinr = zimmer.zinr
            output_list.zistatus = zimmer.zistatus
            output_list.kbezeich = zimmer.kbezeich
            output_list.code = zimmer.code

            if output_list.reihenfolge == 0:
                output_list.reihenfolge = 1

            if substring(zimmer.zinr, length(zimmer.zinr) - 1, 1) == "1"  or substring(zimmer.zinr, length(zimmer.zinr) - 1, 1) == "3"  or substring(zimmer.zinr, length(zimmer.zinr) - 1, 1) == "5"  or substring(zimmer.zinr, length(zimmer.zinr) - 1, 1) == "7"  or substring(zimmer.zinr, length(zimmer.zinr) - 1, 1) == "9" :
                output_list.odd_even = 1

            elif substring(zimmer.zinr, length(zimmer.zinr) - 1, 1) == "0"  or substring(zimmer.zinr, length(zimmer.zinr) - 1, 1) == "2"  or substring(zimmer.zinr, length(zimmer.zinr) - 1, 1) == "4"  or substring(zimmer.zinr, length(zimmer.zinr) - 1, 1) == "6"  or substring(zimmer.zinr, length(zimmer.zinr) - 1, 1) == "8" :
                output_list.odd_even = 2

            if off_market:
                output_list.zistatus = 7
                output_list.rstat = stat_list[7]
                output_list.rstat1 = stat_list1[7]

            else:
                # output_list.rstat = stat_list[zimmer.zistatus + 1 - 1]
                # output_list.rstat1 = stat_list1[zimmer.zistatus + 1 - 1]
                output_list.rstat = stat_list[zimmer.zistatus]
                output_list.rstat1 = stat_list1[zimmer.zistatus]

            if output_list.zistatus == 6:
                outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)]})

                if outorder:
                    output_list.gname = outorder.gespgrund

                if outorder and (outorder.betriebsnr == 3 or outorder.betriebsnr == 4):
                    output_list.zistatus = 9
                    output_list.rstat = stat_list[9]
                    output_list.rstat1 = stat_list1[9]

            if not zimmer.sleeping:
                output_list.inactive = "i"

            if zimmer.zistatus == 0:
                output_list.cleanflag = True
                output_list.flag = 0

            if (zimmer.zistatus >= 3 and zimmer.zistatus <= 5) or zimmer.zistatus == 8:

                res_line = get_cache (Res_line, {
                    "resstatus": [(eq, 6)],
                    "zinr": [(eq, zimmer.zinr)]})

                if res_line:
                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                    output_list.resnam = guest.name
                    output_list.co_time = to_string(res_line.abreisezeit, "HH:MM:SS")

                    reslin_queasy = get_cache (Reslin_queasy, {
                        # "key": [(eq, "specialrequest")],
                        "key": [(eq, "specialRequest")],
                        "resnr": [(eq, res_line.resnr)],
                        "reslinnr": [(eq, res_line.reslinnr)]})

                    if reslin_queasy:
                        output_list.code = output_list.code + "," + reslin_queasy.char3

                    if length(output_list.code) > 0 and substring(output_list.code, length(output_list.code) - 1, 1) == "," :
                        output_list.code = substring(output_list.code, 0, length(output_list.code) - 1)

                    if ldry != 0 and ci_date > res_line.ankunft:
                        if (ci_date - res_line.ankunft) % ldry == 0:
                            output_list.ldry = "LD"

                    if towel != 0 and ci_date > res_line.ankunft:
                        if (ci_date - res_line.ankunft) % towel == 0:
                            output_list.towel = "TW"

                    output_list = query(output_list_data, filters=(lambda output_list: output_list.zinr == res_line.zinr), first=True)

                    if output_list:
                        output_list.bemerk = replace_str(res_line.bemerk, chr_unicode(10) , " ")
                        output_list.flag = 1
                        output_list.flight_nr = res_line.flight_nr

                        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                        if guest.vorname1 != "":
                            output_list.resname = guest.name + ", " + guest.vorname1
                        else:
                            output_list.resnam = guest.name

                        if output_list.gname == "":
                            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                            c_vip, vip_type = check_vip_guest()
                            output_list.gname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                            output_list.nation = guest.nation1

                            if c_vip != "":
                                output_list.vip = c_vip

                            output_list.segm_type = vip_type
                            
                        output_list.ankunft = res_line.ankunft
                        output_list.abreise = res_line.abreise

                        if res_line.ankunft == res_line.abreise:
                            anz = res_line.erwachs + res_line.gratis

                            if anz <= 2:
                                for i in range(1,anz + 1) :
                                    output_list.gstat = output_list.gstat + "U"
                            else:
                                output_list.gstat = to_string(anz) + "U"
                            anz = res_line.kind1 + res_line.l_zuordnung[3]

                            if anz <= 2:
                                for i in range(1,anz + 1) :
                                    output_list.gstat = output_list.gstat + "u"
                            else:
                                output_list.gstat = output_list.gstat + to_string(anz) + "u"
                            for i in range(1,res_line.kind2 + 1) :
                                output_list.gstat = output_list.gstat + "C"

                        elif res_line.abreise == ci_date:
                            output_list.zistatus = 3
                            output_list.rstat = stat_list[3]
                            output_list.rstat1 = stat_list1[3]

                            anz = res_line.erwachs + res_line.gratis

                            if anz <= 2:
                                for i in range(1,anz + 1) :
                                    output_list.gstat = output_list.gstat + "D"
                            else:
                                output_list.gstat = to_string(anz) + "D"
                            anz = res_line.kind1 + res_line.l_zuordnung[3]

                            if anz <= 2:
                                for i in range(1,anz + 1) :
                                    output_list.gstat = output_list.gstat + "d"
                            else:
                                output_list.gstat = output_list.gstat + to_string(anz) + "d"
                            for i in range(1,res_line.kind2 + 1) :
                                output_list.gstat = output_list.gstat + "C"
                        else:
                            anz = res_line.erwachs + res_line.gratis

                            if anz <= 2:
                                for i in range(1,anz + 1) :
                                    output_list.gstat = output_list.gstat + "R"
                            else:
                                output_list.gstat = to_string(anz) + "R"
                            anz = res_line.kind1 + res_line.l_zuordnung[3]

                            if anz <= 2:
                                for i in range(1,anz + 1) :
                                    output_list.gstat = output_list.gstat + "r"
                            else:
                                output_list.gstat = output_list.gstat + to_string(anz) + "r"
                            for i in range(1,res_line.kind2 + 1) :
                                output_list.gstat = output_list.gstat + "C"

            elif zimmer.zistatus <= 2:
                if zimmer.zistatus == 2:
                    if ldry != 0:
                        output_list.ldry = "LD"

                    if towel != 0:
                        output_list.towel = "TW"

                    res_line = get_cache (Res_line, {
                        "resstatus": [(eq, 8)],
                        "active_flag": [(eq, 2)],
                        "abreise": [(eq, ci_date)],
                        "zinr": [(eq, zimmer.zinr)]})

                    if res_line:
                        output_list.gstat = output_list.gstat + "*"

                res_line = db_session.query(Res_line).filter(
                        ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5)) & (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & (Res_line.zinr == zimmer.zinr)).first()

                if res_line:
                    output_list = query(output_list_data, filters=(lambda output_list: output_list.zinr == res_line.zinr), first=True)

                    if output_list:
                        output_list.bemerk = replace_str(res_line.bemerk, chr_unicode(10) , " ")
                        output_list.flag = 1
                        output_list.flight_nr = res_line.flight_nr

                        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                        if guest.vorname1 != "":
                            output_list.resname = guest.name + ", " + guest.vorname1
                        else:
                            output_list.resnam = guest.name

                        if output_list.gname == "":
                            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                            c_vip, vip_type = check_vip_guest()
                            output_list.gname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                            output_list.nation = guest.nation1

                            if c_vip != "":
                                output_list.vip = c_vip

                            output_list.segm_type = vip_type
                            
                        output_list.ankunft = res_line.ankunft
                        output_list.abreise = res_line.abreise
                        output_list.arrival = True
                        anz = res_line.erwachs + res_line.gratis

                        # if anz <= 2:
                        #     for i in range(1,anz + 1) :
                        #         output_list.gstat = output_list.gstat + "A"
                        # else:
                        #     output_list.gstat = output_list.gstat + to_string(anz) + "A"
                        # anz = res_line.kind1 + res_line.l_zuordnung[3]

                        # if anz <= 2:
                        #     for i in range(1,anz + 1) :
                        #         output_list.gstat = output_list.gstat + "a"
                        # else:
                        #     output_list.gstat = output_list.gstat + to_string(anz) + "a"
                        if anz <= 2:
                            for i in range(1,anz + 1) :
                                # output_list.gstat = output_list.gstat + "A"
                                output_list.gstat = output_list.gstat + "a"
                                
                        else:
                            # output_list.gstat = output_list.gstat + to_string(anz) + "A"
                            output_list.gstat = output_list.gstat + to_string(anz) + "a"
                        anz = res_line.kind1 + res_line.l_zuordnung[3]
                            
                        for i in range(1,res_line.kind2 + 1) :
                            output_list.gstat = output_list.gstat + "C"

                        reslin_queasy = get_cache (Reslin_queasy, {
                            # "key": [(eq, "specialrequest")],
                            "key": [(eq, "specialRequest")],
                            "resnr": [(eq, res_line.resnr)],
                            "reslinnr": [(eq, res_line.reslinnr)]})

                        if reslin_queasy:
                            output_list.code = output_list.code + "," + reslin_queasy.char3

                        if length(output_list.code) > 0 and substring(output_list.code, length(output_list.code) - 1, 1) == ",":
                            output_list.code = substring(output_list.code, 0, length(output_list.code) - 1)

            if output_list.zistatus == 3:
                res_line = db_session.query(Res_line).filter(
                        ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5)) & (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & (Res_line.zinr == zimmer.zinr)).first()

                if res_line:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.reihenfolge = 0
                    output_list.personal = zimmer.personal
                    output_list.floor = zimmer.etage
                    output_list.zinr = zimmer.zinr
                    output_list.zistatus = zimmer.zistatus
                    output_list.kbezeich = zimmer.kbezeich
                    output_list.code = zimmer.code

                    out_list = query(out_list_data, filters=(lambda out_list: out_list.zinr == res_line.zinr and out_list.abreise == res_line.ankunft), first=True)

                    if out_list:
                        output_list.zinr = zimmer.zinr + "*"

                    if substring(zimmer.zinr, length(zimmer.zinr) - 1, 1) == "1"  or substring(zimmer.zinr, length(zimmer.zinr) - 1, 1) == "3"  or substring(zimmer.zinr, length(zimmer.zinr) - 1, 1) == "5"  or substring(zimmer.zinr, length(zimmer.zinr) - 1, 1) == "7"  or substring(zimmer.zinr, length(zimmer.zinr) - 1, 1) == "9" :
                        output_list.odd_even = 1

                    elif substring(zimmer.zinr, length(zimmer.zinr) - 1, 1) == "0"  or substring(zimmer.zinr, length(zimmer.zinr) - 1, 1) == "2"  or substring(zimmer.zinr, length(zimmer.zinr) - 1, 1) == "4"  or substring(zimmer.zinr, length(zimmer.zinr) - 1, 1) == "6"  or substring(zimmer.zinr, length(zimmer.zinr) - 1, 1) == "8" :
                        output_list.odd_even = 2
                        
                    output_list.bemerk = replace_str(res_line.bemerk, chr_unicode(10) , " ")
                    output_list.flag = 1
                    output_list.rsv_flag = True
                    output_list.flight_nr = res_line.flight_nr

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                    if guest.vorname1 != "":
                        output_list.resname = guest.name + ", " + guest.vorname1
                    else:
                        output_list.resnam = guest.name

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                    c_vip, vip_type = check_vip_guest()
                    output_list.gname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                    output_list.nation = guest.nation1
                    output_list.ankunft = res_line.ankunft
                    output_list.abreise = res_line.abreise
                    output_list.arrival = True
                    anz = res_line.erwachs + res_line.gratis

                    if c_vip != "":
                        output_list.vip = c_vip

                    output_list.segm_type = vip_type

                    if anz <= 2:
                        for i in range(1,anz + 1) :
                            # output_list.gstat = output_list.gstat + "A"
                            output_list.gstat = output_list.gstat + "a"
                            
                    else:
                        # output_list.gstat = output_list.gstat + to_string(anz) + "A"
                        output_list.gstat = output_list.gstat + to_string(anz) + "a"
                        
                    anz = res_line.kind1 + res_line.l_zuordnung[3]

                    for i in range(1,res_line.kind2 + 1) :
                        output_list.gstat = output_list.gstat + "C"

                    reslin_queasy = get_cache (Reslin_queasy, {
                        "key": [(eq, "specialrequest")],
                        "resnr": [(eq, res_line.resnr)],
                        "reslinnr": [(eq, res_line.reslinnr)]})

                    if reslin_queasy:
                        output_list.code = output_list.code + "," + reslin_queasy.char3

                    if length(output_list.code) > 0 and substring(output_list.code, length(output_list.code) - 1, 1) == "," :
                        output_list.code = substring(output_list.code, 0, length(output_list.code) - 1)

    def check_vip_guest():
        nonlocal output_list_data, lvcarea, stat_list, stat_list1, vip_nr, resbemerk, htparam, zimmer, outorder, res_line, guest, reslin_queasy, guestseg, segment
        nonlocal pvilanguage
        nonlocal out_list
        nonlocal output_list, out_list
        nonlocal output_list_data

        c_vip = ""
        vip_type = 0

        def generate_inner_output():
            return (c_vip, vip_type)

        guestseg = db_session.query(Guestseg).filter(
                (Guestseg.gastnr == guest.gastnr) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).first()

        if guestseg:
            segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})

            if segment:
                c_vip = segment.bezeich + " "
                vip_type = segment.betriebsnr

        return generate_inner_output()
    
    stat_list[0] = translateExtended ("Vacant Clean Checked", lvcarea, "")
    stat_list[1] = translateExtended ("Vac. Clean Unchecked", lvcarea, "")
    stat_list[2] = translateExtended ("Vacant Dirty", lvcarea, "")
    stat_list[3] = translateExtended ("Expected Departure", lvcarea, "")
    stat_list[4] = translateExtended ("Occupied Dirty", lvcarea, "")
    stat_list[5] = translateExtended ("Occupied Cleaned", lvcarea, "")
    stat_list[6] = translateExtended ("Out-of-Order", lvcarea, "")
    stat_list[7] = translateExtended ("Off-Market", lvcarea, "")
    stat_list[8] = translateExtended ("Do not Disturb", lvcarea, "")
    stat_list[9] = translateExtended ("Out of Service", lvcarea, "")
    fill_vipnr()
    fill_list()

    for output_list in query(output_list_data):
        resbemerk = ""
        resbemerk = output_list.bemerk
        resbemerk = replace_str(resbemerk, chr_unicode(10) , "")
        resbemerk = replace_str(resbemerk, chr_unicode(13) , "")
        resbemerk = replace_str(resbemerk, "~n", "")
        resbemerk = replace_str(resbemerk, "\\n", "")
        resbemerk = replace_str(resbemerk, "~r", "")
        resbemerk = replace_str(resbemerk, "~r~n", "")
        resbemerk = replace_str(resbemerk, chr_unicode(10) + chr_unicode(13) , "")

        if length(resbemerk) < 3:
            resbemerk = replace_str(resbemerk, chr_unicode(32) , "")

        if length(resbemerk) == None:
            resbemerk = ""
            
        output_list.bemerk = trim(resbemerk)
        resbemerk = ""

    return generate_output()