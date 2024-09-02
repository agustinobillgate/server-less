from functions.additional_functions import *
import decimal
from datetime import date
from functions.get_vipnrbl import get_vipnrbl
import re
from models import Guest, Paramtext, Htparam, Res_line, Queasy

def precheckin_generator_loaddata_1bl(show_rate:bool, last_sort:int, lresnr:int, long_stay:int, ci_date:date, grpflag:bool, room:str, lname:str, sorttype:int, fdate1:date, fdate2:date, fdate:date, segm1_list:[Segm1_list], argt_list:[Argt_list], zikat_list:[Zikat_list]):
    rmlen = 0
    mail_eng = ""
    mail_oth = ""
    hotel_name = ""
    hotel_telp = ""
    hotel_mail = ""
    arl_list_list = []
    vipnr1:int = 999999999
    vipnr2:int = 999999999
    vipnr3:int = 999999999
    vipnr4:int = 999999999
    vipnr5:int = 999999999
    vipnr6:int = 999999999
    vipnr7:int = 999999999
    vipnr8:int = 999999999
    vipnr9:int = 999999999
    done_flag:bool = False
    curr_resnr:int = 0
    curr_resline:int = 0
    today_str:str = ""
    reserve_str:str = ""
    created_time:int = 0
    do_it:bool = True
    loop_i:int = 0
    comment_str:str = ""
    all_inclusive:str = ""
    res_mode:str = ""
    checkin_flag:bool = False
    stay:int = 0
    en_hotelencrip:str = ""
    oth_hotelencrip:str = ""
    cpersonalkey:str = ""
    rkey:bytes = None
    mmemptrout:bytes = None
    precheckinurl:str = ""
    hotelcode:str = ""
    hotelcode_ok:bool = False
    guest = paramtext = htparam = res_line = queasy = None

    setup_list = gbuff = arl_list = segm1_list = argt_list = zikat_list = gmember = rline = None

    setup_list_list, Setup_list = create_model("Setup_list", {"nr":int, "char":str})
    arl_list_list, Arl_list = create_model("Arl_list", {"resnr":int, "reslinnr":int, "resline_wabkurz":str, "voucher_nr":str, "grpflag":bool, "verstat":int, "l_zuordnung2":int, "kontignr":int, "firmen_nr":int, "steuernr":str, "rsv_name":str, "zinr":str, "setup_list_char":str, "resline_name":str, "waehrung_wabkurz":str, "segmentcode":int, "ankunft":date, "abreise":date, "zimmeranz":int, "kurzbez":str, "arrangement":str, "zipreis":decimal, "anztage":int, "erwachs":int, "kind1":int, "kind2":int, "gratis":int, "l_zuordnung4":int, "resstatus":int, "l_zuordnung3":int, "flight_nr":str, "ankzeit":int, "abreisezeit":int, "betrieb_gast":int, "resdat":date, "useridanlage":str, "reserve_dec":decimal, "cancelled_id":str, "changed_id":str, "groupname":str, "active_flag":int, "gastnr":int, "gastnrmember":int, "karteityp":int, "reserve_int":int, "zikatnr":int, "betrieb_gastmem":int, "pseudofix":bool, "reserve_char":str, "bemerk":str, "depositbez":decimal, "depositbez2":decimal, "bestat_dat":date, "briefnr":int, "rsv_gastnr":int, "rsv_resnr":int, "rsv_bemerk":str, "rsv_grpflag":bool, "recid_resline":int, "address":str, "city":str, "comments":str, "resnr_fgcol":int, "mc_str_fgcol":int, "mc_str_bgcol":int, "rsv_name_fgcol":int, "rsv_name_bgcol":int, "zinr_fgcol":int, "reslin_name_fgcol":int, "ankunft_fgcol":int, "anztage_fgcol":int, "abreise_fgcol":int, "segmentcode_fgcol":int, "reslin_name_bgcol":int, "segmentcode_bgcol":int, "zinr_bgcol":int, "webci":str, "webci_flag":str, "voucher_flag":str, "kontignr_flag":str, "phonenumber":str, "email_address":str, "link_pci_eng":str, "link_pci_oth":str, "selected":bool}, {"resnr_fgcol": -1, "mc_str_fgcol": -1, "mc_str_bgcol": -1, "rsv_name_fgcol": -1, "rsv_name_bgcol": -1, "zinr_fgcol": -1, "reslin_name_fgcol": -1, "ankunft_fgcol": -1, "anztage_fgcol": -1, "abreise_fgcol": -1, "segmentcode_fgcol": -1, "reslin_name_bgcol": -1, "segmentcode_bgcol": -1, "zinr_bgcol": -1})
    segm1_list_list, Segm1_list = create_model("Segm1_list", {"selected":bool, "segm":int, "bezeich":str, "bezeich1":str})
    argt_list_list, Argt_list = create_model("Argt_list", {"selected":bool, "argtnr":int, "argt":str, "bezeich":str})
    zikat_list_list, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":str, "bezeich":str})

    Gbuff = Guest
    Gmember = Guest
    Rline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmlen, mail_eng, mail_oth, hotel_name, hotel_telp, hotel_mail, arl_list_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, done_flag, curr_resnr, curr_resline, today_str, reserve_str, created_time, do_it, loop_i, comment_str, all_inclusive, res_mode, checkin_flag, stay, en_hotelencrip, oth_hotelencrip, cpersonalkey, rkey, mmemptrout, precheckinurl, hotelcode, hotelcode_ok, guest, paramtext, htparam, res_line, queasy
        nonlocal gbuff, gmember, rline


        nonlocal setup_list, gbuff, arl_list, segm1_list, argt_list, zikat_list, gmember, rline
        nonlocal setup_list_list, arl_list_list, segm1_list_list, argt_list_list, zikat_list_list
        return {"rmlen": rmlen, "mail_eng": mail_eng, "mail_oth": mail_oth, "hotel_name": hotel_name, "hotel_telp": hotel_telp, "hotel_mail": hotel_mail, "arl-list": arl_list_list}

    def get_toname(lname:str):

        nonlocal rmlen, mail_eng, mail_oth, hotel_name, hotel_telp, hotel_mail, arl_list_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, done_flag, curr_resnr, curr_resline, today_str, reserve_str, created_time, do_it, loop_i, comment_str, all_inclusive, res_mode, checkin_flag, stay, en_hotelencrip, oth_hotelencrip, cpersonalkey, rkey, mmemptrout, precheckinurl, hotelcode, hotelcode_ok, guest, paramtext, htparam, res_line, queasy
        nonlocal gbuff, gmember, rline


        nonlocal setup_list, gbuff, arl_list, segm1_list, argt_list, zikat_list, gmember, rline
        nonlocal setup_list_list, arl_list_list, segm1_list_list, argt_list_list, zikat_list_list


        return chr(ord(substring(lname, 0, 1)) + 1)

    def fixing_blank_resname():

        nonlocal rmlen, mail_eng, mail_oth, hotel_name, hotel_telp, hotel_mail, arl_list_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, done_flag, curr_resnr, curr_resline, today_str, reserve_str, created_time, do_it, loop_i, comment_str, all_inclusive, res_mode, checkin_flag, stay, en_hotelencrip, oth_hotelencrip, cpersonalkey, rkey, mmemptrout, precheckinurl, hotelcode, hotelcode_ok, guest, paramtext, htparam, res_line, queasy
        nonlocal gbuff, gmember, rline


        nonlocal setup_list, gbuff, arl_list, segm1_list, argt_list, zikat_list, gmember, rline
        nonlocal setup_list_list, arl_list_list, segm1_list_list, argt_list_list, zikat_list_list


        Rline = Res_line

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag <= 1) &  (Res_line.resstatus != 12) &  (Res_line.resname == "")).first()
        while None != res_line:

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnr)).first()

            rline = db_session.query(Rline).filter(
                        (Rline._recid == res_line._recid)).first()

            if rline:
                rline.resname = guest.name

                rline = db_session.query(Rline).first()

            res_line = db_session.query(Res_line).filter(
                    (Res_line.active_flag <= 1) &  (Res_line.resstatus != 12) &  (Res_line.resname == "")).first()


    setup_list = Setup_list()
    setup_list_list.append(setup_list)

    setup_list.nr = 1
    setup_list.char = " "

    for paramtext in db_session.query(Paramtext).filter(
            (Paramtext.txtnr >= 9201) &  (Paramtext.txtnr <= 9299)).all():
        setup_list = Setup_list()
        setup_list_list.append(setup_list)

        setup_list.nr = paramtext.txtnr - 9199
        setup_list.char = substring(paramtext.notes, 0, 1)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 458)).first()

    if htparam:
        stay = htparam.finteger
    fixing_blank_resname()

    if num_entries(room, chr(2)) > 1:
        do_it = False
        curr_resnr = to_int(entry(1, room, chr(2)))
        curr_resline = to_int(entry(2, room, chr(2)))
        today_str = to_string(get_current_date())
        res_mode = trim(entry(3, room, chr(2)))


        room = entry(0, room, chr(2))

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == curr_resnr) &  (Res_line.reslinnr == curr_resline)).first()

        if not res_line:
            do_it = True
        else:

            if res_line.active_flag == 1 and res_mode.lower()  == "modify":
                do_it = True
            else:

                for res_line in db_session.query(Res_line).filter(
                        (Res_line.resnr == curr_resnr) &  (Res_line.active_flag <= 1)).all():
                    reserve_str = res_line.reserve_char

                    if today_str == substring(reserve_str, 0, 8):
                        reserve_str = substring(reserve_str, 8)
                        created_time = to_int(substring(reserve_str, 0, 2)) * 3600 +\
                                to_int(substring(reserve_str, 3, 2)) * 60

                        if created_time >= (get_current_time_in_seconds() - 70):
                            do_it = True
                            break


    if not do_it:

        return generate_output()
    vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9 = get_output(get_vipnrbl())
    disp_arlist1()

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 216) &  (Queasy.number1 == 7) &  (Queasy.number2 == 5)).first()

    if queasy:
        precheckinurl = queasy.char3

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 216) &  (Queasy.number1 == 8)).all():

        if queasy.number2 == 31:
            hotelcode = queasy.char3

        if queasy.number2 == 32:
            mail_eng = queasy.char3

        if queasy.number2 == 33:
            mail_oth = queasy.char3

        if queasy.number2 == 19:
            hotel_name = queasy.char3

        if queasy.number2 == 22:
            hotel_telp = queasy.char3

        if queasy.number2 == 23:
            hotel_mail = queasy.char3

    if hotelcode == "":
        hotelcode_ok = False
    else:
        hotelcode_ok = True

    if not hotelcode_ok:

        for arl_list in query(arl_list_list):
            arl_list.link_pci_eng = "hotelcode Not Configured Yet"
            arl_list.link_pci_oth = "hotelcode Belum Terkonfigurasi Dengan Benar"
    else:

        for arl_list in query(arl_list_list):
            en_hotelencrip = "ENG|" + hotelcode + "|" + to_string(arl_list.ankunft) + "|" + to_string(arl_list.resnr)
            oth_hotelencrip = "IDN|" + hotelcode + "|" + to_string(arl_list.ankunft) + "|" + to_string(arl_list.resnr)
            cpersonalkey = "97038B14732C6AD1C1ED9EC6FB675AAC2698DF86"
            rkey = GENERATE_PBE_KEY (cpersonalkey)
            mmemptrout = ENCRYPT (en_hotelencrip, rkey)
            en_hotelencrip = BASE64_ENCODE (mmemptrout)

            if re.match(".*\$.*",en_hotelencrip):
                en_hotelencrip = replace_str(en_hotelencrip, "$", "%24")

            if re.match(".*&.*",en_hotelencrip):
                en_hotelencrip = replace_str(en_hotelencrip, "&", "%26")

            if re.match(".*\+.*",en_hotelencrip):
                en_hotelencrip = replace_str(en_hotelencrip, "+", "%2B")

            if re.match(".*,.*",en_hotelencrip):
                en_hotelencrip = replace_str(en_hotelencrip, ",", "%2C")

            if re.match(".*",en_hotelencrip):
                en_hotelencrip = replace_str(en_hotelencrip, "/", "%2F")

            if re.match(".*:.*",en_hotelencrip):
                en_hotelencrip = replace_str(en_hotelencrip, ":", "%3A")

            if re.match(".*;.*",en_hotelencrip):
                en_hotelencrip = replace_str(en_hotelencrip, ";", "%3B")

            if re.match(".* ==.*",en_hotelencrip):
                en_hotelencrip = replace_str(en_hotelencrip, " == ", "%3D")

            if re.match(".*?.*",en_hotelencrip):
                en_hotelencrip = replace_str(en_hotelencrip, "?", "%3F")

            if re.match(".*@.*",en_hotelencrip):
                en_hotelencrip = replace_str(en_hotelencrip, "@", "%40")
            arl_list.link_pci_eng = precheckinurl + "?" + en_hotelencrip
            mmemptrout = ENCRYPT (oth_hotelencrip, rkey)
            oth_hotelencrip = BASE64_ENCODE (mmemptrout)

            if re.match(".*\$.*",oth_hotelencrip):
                oth_hotelencrip = replace_str(oth_hotelencrip, "$", "%24")

            if re.match(".*&.*",oth_hotelencrip):
                oth_hotelencrip = replace_str(oth_hotelencrip, "&", "%26")

            if re.match(".*\+.*",oth_hotelencrip):
                oth_hotelencrip = replace_str(oth_hotelencrip, "+", "%2B")

            if re.match(".*,.*",oth_hotelencrip):
                oth_hotelencrip = replace_str(oth_hotelencrip, ",", "%2C")

            if re.match(".*",oth_hotelencrip):
                oth_hotelencrip = replace_str(oth_hotelencrip, "/", "%2F")

            if re.match(".*:.*",oth_hotelencrip):
                oth_hotelencrip = replace_str(oth_hotelencrip, ":", "%3A")

            if re.match(".*;.*",oth_hotelencrip):
                oth_hotelencrip = replace_str(oth_hotelencrip, ";", "%3B")

            if re.match(".* ==.*",oth_hotelencrip):
                oth_hotelencrip = replace_str(oth_hotelencrip, " == ", "%3D")

            if re.match(".*?.*",oth_hotelencrip):
                oth_hotelencrip = replace_str(oth_hotelencrip, "?", "%3F")

            if re.match(".*@.*",oth_hotelencrip):
                oth_hotelencrip = replace_str(oth_hotelencrip, "@", "%40")
            arl_list.link_pci_oth = precheckinurl + "?" + oth_hotelencrip

    return generate_output()