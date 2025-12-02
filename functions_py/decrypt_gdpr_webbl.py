#using conversion tools version: 1.0.0.119
#------------------------------------------
# Rd, 26/11/2025, with_for_update, skip, temp-table
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Guest, Res_line, H_bill, History, Bill, Billhis, Paramtext, Htparam, Nation, Queasy, Bediener, Res_history
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

import tempfile as tp
import os
import re
import shutil


payload_list_data, Payload_list = create_model("Payload_list", {"from_co_date":date, "to_co_date":date, "non_europe_validation":bool, "case_type":int, "user_init":string})

def decrypt_gdpr_webbl(payload_list_data:[Payload_list]):

    prepare_cache ([Guest, Res_line, H_bill, History, Bill, Billhis, Paramtext, Htparam, Nation, Queasy, Bediener, Res_history])

    response_list_data = []
    from_co_date:date = None
    to_co_date:date = None
    non_europe_validation:bool = False
    case_type:int = 0
    user_init:string = ""
    count_data:int = 0
    count_data_processed:int = 0
    lic_nr:string = ""
    start_key:string = ""
    decrypt_data:string = ""
    count_data_failed_decrypt:int = 0
    count_data_failed_already_decrypt:int = 0
    loopi:int = 0
    str:string = ""
    ct:string = ""
    htl_name:string = ""
    count_region:int = 0
    status_txt:string = ""
    guest = res_line = h_bill = history = bill = billhis = paramtext = htparam = nation = queasy = bediener = res_history = None

    payload_list = europe_region_list = response_list = bguest = presline = phbill = phistory = pbill = pbillhis = pguest = None

    europe_region_list_data, Europe_region_list = create_model("Europe_region_list", {"region_nr":int})
    response_list_data, Response_list = create_model("Response_list", {"status_process":string})

    Bguest = create_buffer("Bguest",Guest)
    Presline = create_buffer("Presline",Res_line)
    Phbill = create_buffer("Phbill",H_bill)
    Phistory = create_buffer("Phistory",History)
    Pbill = create_buffer("Pbill",Bill)
    Pbillhis = create_buffer("Pbillhis",Billhis)
    Pguest = create_buffer("Pguest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal response_list_data, from_co_date, to_co_date, non_europe_validation, case_type, user_init, count_data, count_data_processed, lic_nr, start_key, decrypt_data, count_data_failed_decrypt, count_data_failed_already_decrypt, loopi, str, ct, htl_name, count_region, status_txt, guest, res_line, h_bill, history, bill, billhis, paramtext, htparam, nation, queasy, bediener, res_history
        nonlocal bguest, presline, phbill, phistory, pbill, pbillhis, pguest


        nonlocal payload_list, europe_region_list, response_list, bguest, presline, phbill, phistory, pbill, pbillhis, pguest
        nonlocal europe_region_list_data, response_list_data

        return {"response-list": response_list_data}

    def is_integer(cval:string):

        nonlocal response_list_data, from_co_date, to_co_date, non_europe_validation, case_type, user_init, count_data, count_data_processed, lic_nr, start_key, decrypt_data, count_data_failed_decrypt, count_data_failed_already_decrypt, loopi, str, ct, htl_name, count_region, status_txt, guest, res_line, h_bill, history, bill, billhis, paramtext, htparam, nation, queasy, bediener, res_history
        nonlocal bguest, presline, phbill, phistory, pbill, pbillhis, pguest


        nonlocal payload_list, europe_region_list, response_list, bguest, presline, phbill, phistory, pbill, pbillhis, pguest
        nonlocal europe_region_list_data, response_list_data

        # i:int = 0
        # ch:string = ""
        # len_:int = 0
        # cval = trim(cval)
        # len_ = length(cval)

        # if len_ == 0:
        #     return False

        # if substring(cval, 0, 1) == ("-").lower() :

        #     if len_ == 1:
        #         return False
        #     cval = substring(cval, 1)
        # for i in range(1,length(cval)  + 1) :
        #     ch = substring(cval, i - 1, 1)

        #     if get_index("0123456789", ch) == 0:
        #         return False
        # return True

        try:
            int(cval)
            return True
        except ValueError:
            return False


    def get_decrypted_data():

        nonlocal response_list_data, from_co_date, to_co_date, non_europe_validation, case_type, user_init, count_data, count_data_processed, lic_nr, start_key, decrypt_data, count_data_failed_decrypt, count_data_failed_already_decrypt, loopi, str, ct, htl_name, count_region, status_txt, guest, res_line, h_bill, history, bill, billhis, paramtext, htparam, nation, queasy, bediener, res_history
        nonlocal bguest, presline, phbill, phistory, pbill, pbillhis, pguest


        nonlocal payload_list, europe_region_list, response_list, bguest, presline, phbill, phistory, pbill, pbillhis, pguest
        nonlocal europe_region_list_data, response_list_data

        count_i:int = 0
        infile:string = ""
        outfile:string = ""
        tempfile:string = ""
        line:string = ""
        updated:bool = False
        allowed_region:bool = False
        isrunning:bool = False
        infile = "/usr1/serverless/src/additional_files/status-" + htl_name + ".txt"
        tempfile = tp.gettempdir() + "status_tmp-" + htl_name + ".txt"
        outfile = tempfile
        updated = False
        isrunning = False

        open(infile, 'a').close()
        open(outfile, 'a').close()

        # file_info:file_name = infile

        # if matches(FILE_INFO:FILE_TYPE,r"F*"):
        #     INPUT FROM VALUE (infile) NO_ECHO
        #     OUTPUT TO VALUE (outfile)
        #     while True:
        #         IMPORT UNFORMATTED line

        #         if matches(line,r"status=*"):

        #             if matches(line,r"status=running*"):
        #                 isrunning = True
        #             updated = True
        #         else:
        #         INPUT CLOSE
        #     OUTPUT CLOSE

        # if not updated:
        #     OUTPUT TO VALUE (outfile)
        #     OUTPUT CLOSE
        # OS_DELETE VALUE (infile)
        # OS_RENAME VALUE (outfile) VALUE (infile)

        if os.path.exists(infile):
            with open(infile, "r") as f:
                line = f.readline() 
                if re.match(r"status=.*", line):
                    if re.match(r"status=running.*"):
                        isrunning = True

                    f.write("status=running")
                    updated = True

        if not updated:
            if os.path.exists(outfile):
                with open(outfile, "r+") as f:
                    f.write("status=running")

        if os.path.exists(infile):
            os.remove(infile)

        shutil.copy(outfile, infile)

        if not isrunning:

            paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

            if paramtext:
                lic_nr = paramtext.ptexte


            start_key = retrieve_start_key()

            res_line_obj_list = {}
            res_line = Res_line()
            guest = Guest()
            nation = Nation()

            for res_line._recid, res_line.reslinnr, res_line.resnr, res_line.name, guest.vornamekind, guest.name, guest.gastnr, guest._recid, guest.anrede1, guest.vorname1, guest.adresse1, guest.adresse2, guest.adresse3, guest.geburtdatum1, guest.telefon, guest.mobil_telefon, guest.geschlecht, guest.email_adr, guest.geburt_ort1, guest.ausweis_nr1, guest.plz, guest.geburt_ort2, guest.telex, guest.beruf, guest.fax, guest.geburtdatum2, nation.untergruppe, nation._recid in db_session.query(Res_line._recid, Res_line.reslinnr, Res_line.resnr, Res_line.name, Guest.vornamekind, Guest.name, Guest.gastnr, Guest._recid, Guest.anrede1, Guest.vorname1, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.geburtdatum1, Guest.telefon, Guest.mobil_telefon, Guest.geschlecht, Guest.email_adr, Guest.geburt_ort1, Guest.ausweis_nr1, Guest.plz, Guest.geburt_ort2, Guest.telex, Guest.beruf, Guest.fax, Guest.geburtdatum2, Nation.untergruppe, Nation._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).join(Nation,(Nation.kurzbez == Guest.nation1)).filter(
                     ((((Res_line.resstatus == 8) | (Res_line.resstatus == 9)) | (Res_line.resstatus == 10)) | (Res_line.resstatus == 99)) & (Res_line.abreise >= from_co_date) & (Res_line.abreise <= to_co_date) & (Res_line.abreise != None)).order_by(Res_line._recid).all():
                
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                allowed_region = True

                europe_region_list = query(europe_region_list_data, filters=(lambda europe_region_list: europe_region_list.region_nr == nation.untergruppe), first=True)

                if europe_region_list:
                    allowed_region = False

                if ((non_europe_validation and allowed_region) or not non_europe_validation) and (matches(res_line.name,(start_key + r"*")) or matches(guest.name,start_key + r"*") or guest.vornamekind[5] == None or guest.vornamekind[5] != " "):
                    decrypt_data = multi_level_decrypt_guest(guest.name)

                    if decrypt_data != None:

                        presline = get_cache (Res_line, {"_recid": [(eq, res_line._recid)]})

                        if presline:
                            presline.name = entry(1, decrypt_data, "=")
                            pass
                            pass

                    for h_bill in db_session.query(H_bill).filter(
                             (matches((H_bill.bilname,(start_key + "*"))) | (H_bill.bilname == None)) & 
                             (H_bill.reslinnr == res_line.reslinnr) & (H_bill.resnr == res_line.resnr)).order_by(H_bill._recid).with_for_update().all():
                        decrypt_data = multi_level_decrypt_guest(guest.name)

                        if decrypt_data != None:
                            h_bill.bilname = entry(1, decrypt_data, "=")
                        pass

                    for history in db_session.query(History).filter(
                             (matches((History.gastinfo,(start_key + "*"))) | (History.gastinfo == None)) & 
                             (History.gastnr == guest.gastnr) & (History.resnr == res_line.resnr)).order_by(History._recid).with_for_update().all():
                        decrypt_data = multi_level_decrypt_guest(guest.name)

                        if decrypt_data != None:
                            history.gastinfo = entry(1, decrypt_data, "=")
                        pass

                    for bill in db_session.query(Bill).filter(
                             (matches((Bill.bilname,(start_key + "*"))) | (Bill.bilname == None)) & 
                             (Bill.resnr == res_line.resnr) & (Bill.reslinnr == res_line.reslinnr)).order_by(Bill._recid).with_for_update().all():
                        decrypt_data = multi_level_decrypt_guest(guest.name)

                        if decrypt_data != None:
                            bill.bilname = entry(1, decrypt_data, "=")
                        pass

                    for billhis in db_session.query(Billhis).filter(
                             (matches((Billhis.name,(start_key + "*"))) | (Billhis.name == None)) & 
                             (Billhis.resnr == res_line.resnr) & (Billhis.reslinnr == res_line.reslinnr)).order_by(Billhis._recid).with_for_update().all():
                        decrypt_data = multi_level_decrypt_guest(guest.name)

                        if decrypt_data != None:
                            billhis.name = entry(1, decrypt_data, "=")
                        pass

            res_line_obj_list = {}
            res_line = Res_line()
            guest = Guest()
            nation = Nation()

            for res_line._recid, res_line.reslinnr, res_line.resnr, res_line.name, guest.vornamekind, guest.name, guest.gastnr, guest._recid, guest.anrede1, guest.vorname1, guest.adresse1, guest.adresse2, guest.adresse3, guest.geburtdatum1, guest.telefon, guest.mobil_telefon, guest.geschlecht, guest.email_adr, guest.geburt_ort1, guest.ausweis_nr1, guest.plz, guest.geburt_ort2, guest.telex, guest.beruf, guest.fax, guest.geburtdatum2, nation.untergruppe, nation._recid in db_session.query(Res_line._recid, Res_line.reslinnr, Res_line.resnr, Res_line.name, Guest.vornamekind, Guest.name, Guest.gastnr, Guest._recid, Guest.anrede1, Guest.vorname1, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.geburtdatum1, Guest.telefon, Guest.mobil_telefon, Guest.geschlecht, Guest.email_adr, Guest.geburt_ort1, Guest.ausweis_nr1, Guest.plz, Guest.geburt_ort2, Guest.telex, Guest.beruf, Guest.fax, Guest.geburtdatum2, Nation.untergruppe, Nation._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).join(Nation,(Nation.kurzbez == Guest.nation1)).filter(
                     ((((Res_line.resstatus == 8) | (Res_line.resstatus == 9)) | (Res_line.resstatus == 10)) | (Res_line.resstatus == 99)) & (Res_line.abreise >= from_co_date) & (Res_line.abreise <= to_co_date) & (Res_line.abreise != None)).order_by(Res_line._recid).all():
                
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                allowed_region = True

                europe_region_list = query(europe_region_list_data, filters=(lambda europe_region_list: europe_region_list.region_nr == nation.untergruppe), first=True)

                if europe_region_list:
                    allowed_region = False

                if ((non_europe_validation and allowed_region) or not non_europe_validation) and (matches(guest.name,(start_key + r"*")) or guest.vornamekind[5] == None or guest.vornamekind[5] != " "):

                    if guest.vornamekind[5] != None:
                        decrypt_data = multi_level_decrypt_guest(guest.vornamekind[5])

                        # pguest = get_cache (Guest, {"_recid": [(eq, guest._recid)]})
                        pguest = db_session.query(Guest).filter(
                                 (Guest._recid == guest._recid)).with_for_update().first()

                        if decrypt_data != None:

                            if pguest:
                                for loopi in range(1,num_entries(decrypt_data, chr_unicode(2))  + 1) :
                                    str = entry(loopi - 1, decrypt_data, chr_unicode(2))

                                    if entry(0, str, "=") == ("billname").lower() :
                                        pguest.anrede1 = entry(1, str, "=")

                                    elif entry(0, str, "=") == ("firstname").lower() :
                                        pguest.vorname1 = entry(1, str, "=")

                                    elif entry(0, str, "=") == ("address1").lower() :
                                        pguest.adresse1 = entry(1, str, "=")

                                    elif entry(0, str, "=") == ("address2").lower() :
                                        pguest.adresse2 = entry(1, str, "=")

                                    elif entry(0, str, "=") == ("address3").lower() :
                                        pguest.adresse3 = entry(1, str, "=")

                                    elif entry(0, str, "=") == ("birthdate").lower() :

                                        if num_entries(str, "=") > 1:

                                            if trim(entry(1, str, "=")) != "":
                                                pguest.geburtdatum1 = date_mdy(to_int(entry(1, entry(1, str, "=") , "/")) , to_int(entry(0, entry(1, str, "=") , "/")) , to_int(entry(2, entry(1, str, "=") , "/")))
                                            else:
                                                pguest.geburtdatum1 = None
                                        else:
                                            pguest.geburtdatum1 = None

                                    elif entry(0, str, "=") == ("phone").lower() :
                                        pguest.telefon = entry(1, str, "=")

                                    elif entry(0, str, "=") == ("mobile").lower() :
                                        pguest.mobil_telefon = entry(1, str, "=")

                                    elif entry(0, str, "=") == ("gender").lower() :
                                        pguest.geschlecht = entry(1, str, "=")

                                    elif entry(0, str, "=") == ("email").lower() :
                                        pguest.email_adr = entry(1, str, "=")

                                    elif entry(0, str, "=") == ("idcard").lower() :

                                        if pguest.geburt_ort1 == " ":
                                            pguest.geburt_ort1 = entry(1, str, "=")
                                        else:
                                            pguest.ausweis_nr1 = entry(1, str, "=")

                                    elif entry(0, str, "=") == ("city").lower() :
                                        pguest.plz = entry(1, str, "=")

                                    elif entry(0, str, "=") == ("prov").lower() :
                                        pguest.geburt_ort2 = entry(1, str, "=")

                                    elif entry(0, str, "=") == ("birthplace").lower() :
                                        pguest.telex = entry(1, str, "=")

                                    elif entry(0, str, "=") == ("occupancy").lower() :
                                        pguest.beruf = entry(1, str, "=")

                                    elif entry(0, str, "=") == ("telefax").lower() :
                                        pguest.fax = entry(1, str, "=")

                                    elif entry(0, str, "=") == ("expiredate").lower() :

                                        if num_entries(str, "=") > 1:

                                            if trim(entry(1, str, "=")) != "":
                                                pguest.geburtdatum2 = date_mdy(to_int(entry(1, entry(1, str, "=") , "/")) , to_int(entry(0, entry(1, str, "=") , "/")) , to_int(entry(2, entry(1, str, "=") , "/")))
                                            else:
                                                pguest.geburtdatum2 = None
                                        else:
                                            pguest.geburtdatum2 = None


                                pguest.vornamekind[5] = " "

                                # queasy = get_cache (Queasy, {"key": [(eq, 378)],"number1": [(eq, pguest.gastnr)],"number2": [(eq, res_line.resnr)],"number3": [(eq, res_line.reslinnr)]})
                                queasy = db_session.query(Queasy).filter(
                                         (Queasy.key == 378) & (Queasy.number1 == pguest.gastnr) & (Queasy.number2 == res_line.resnr) & 
                                         (Queasy.number3 == res_line.reslinnr)).with_for_update().first()
                                

                                if not queasy:
                                    queasy = Queasy()
                                    db_session.add(queasy)

                                    queasy.key = 378
                                    queasy.number1 = pguest.gastnr
                                    queasy.number2 = res_line.resnr
                                    queasy.number3 = res_line.reslinnr
                                    queasy.logi1 = True


                                else:
                                    pass

                                    if queasy.logi1 == False:
                                        queasy.logi1 = True


                                    pass
                                    pass
                                pass
                                pass
                        else:

                            if pguest:
                                pguest.vornamekind[5] = " "

                                # queasy = get_cache (Queasy, {"key": [(eq, 378)],"number1": [(eq, pguest.gastnr)],"number2": [(eq, res_line.resnr)],"number3": [(eq, res_line.reslinnr)]})
                                queasy = db_session.query(Queasy).filter(
                                         (Queasy.key == 378) & (Queasy.number1 == pguest.gastnr) & (Queasy.number2 == res_line.resnr) & 
                                         (Queasy.number3 == res_line.reslinnr)).with_for_update().first

                                if not queasy:
                                    queasy = Queasy()
                                    db_session.add(queasy)

                                    queasy.key = 378
                                    queasy.number1 = pguest.gastnr
                                    queasy.number2 = res_line.resnr
                                    queasy.number3 = res_line.reslinnr
                                    queasy.logi1 = True


                                else:
                                    pass

                                    if queasy.logi1 == False:
                                        queasy.logi1 = True


                                    pass
                                    pass
                                pass
                                pass
                    else:

                        pguest = get_cache (Guest, {"_recid": [(eq, guest._recid)]})

                        if pguest:
                            pguest.vornamekind[5] = " "

                            # queasy = get_cache (Queasy, {"key": [(eq, 378)],"number1": [(eq, pguest.gastnr)],"number2": [(eq, res_line.resnr)],"number3": [(eq, res_line.reslinnr)]})
                            queasy = db_session.query(Queasy).filter(
                                     (Queasy.key == 378) & (Queasy.number1 == pguest.gastnr) & (Queasy.number2 == res_line.resnr) & 
                                     (Queasy.number3 == res_line.reslinnr)).with_for_update().first

                            if not queasy:
                                queasy = Queasy()
                                db_session.add(queasy)

                                queasy.key = 378
                                queasy.number1 = pguest.gastnr
                                queasy.number2 = res_line.resnr
                                queasy.number3 = res_line.reslinnr
                                queasy.logi1 = True


                            else:
                                pass

                                if queasy.logi1 == False:
                                    queasy.logi1 = True


                                pass
                                pass
                            pass
                    decrypt_data = multi_level_decrypt_guest(guest.name)

                    if decrypt_data != None:

                        # pguest = get_cache (Guest, {"_recid": [(eq, guest._recid)]})
                        pguest = db_session.query(Guest).filter(
                                 (Guest._recid == guest._recid)).with_for_update().first()

                        if pguest:
                            pguest.name = entry(1, decrypt_data, "=")
                            pass
                            pass

                    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

                    if bediener:
                        res_history = Res_history()
                        db_session.add(res_history)

                        res_history.nr = bediener.nr
                        res_history.datum = get_current_date()
                        res_history.zeit = get_current_time_in_seconds()
                        res_history.aenderung = "Decrypt GDPR - Reservation Number: " + to_string(res_line.resnr, ">>>>>>>9") +\
                                ", Resline Number: " + to_string(res_line.reslinnr, ">>>>>>9") +\
                                ", Guest Number: " + to_string(res_line.gastnr, ">>>>>>9")
                        res_history.action = "Decrypt GDPR"

        updated = True

        # file_info:file_name = infile

        # if matches(FILE_INFO:FILE_TYPE,r"F*"):
        #     INPUT FROM VALUE (infile) NO_ECHO
        #     OUTPUT TO VALUE (outfile)
        #     while True:
        #         IMPORT UNFORMATTED line

        #         if matches(line,r"status=*"):
        #             updated = True
        #         else:
        #         INPUT CLOSE
        #     OUTPUT CLOSE

        # if not updated:
        #     OUTPUT TO VALUE (outfile)
        #     OUTPUT CLOSE

        # OS_DELETE VALUE (infile)
        # OS_RENAME VALUE (outfile) VALUE (infile)

        if os.path.exists(infile):
            with open(infile, "r+") as f:
                line = f.readline() 
                if re.match(r"status=.*", line):
                    f.write("status=done")
                    updated = True

        if not updated:
            if os.path.exists(outfile):
                with open(outfile, "r+") as f:
                    f.write("status=done")

        if os.path.exists(infile):
            os.remove(infile)

        shutil.copy(outfile, infile)


    def get_status_decrypt():

        nonlocal response_list_data, from_co_date, to_co_date, non_europe_validation, case_type, user_init, count_data, count_data_processed, lic_nr, start_key, decrypt_data, count_data_failed_decrypt, count_data_failed_already_decrypt, loopi, str, ct, htl_name, count_region, status_txt, guest, res_line, h_bill, history, bill, billhis, paramtext, htparam, nation, queasy, bediener, res_history
        nonlocal bguest, presline, phbill, phistory, pbill, pbillhis, pguest


        nonlocal payload_list, europe_region_list, response_list, bguest, presline, phbill, phistory, pbill, pbillhis, pguest
        nonlocal europe_region_list_data, response_list_data

        cline:string = ""
        ckey:string = ""
        cvalue:string = ""
        cfile:string = ""
        cfile = "/usr1/serverless/src/additional_files/status-" + htl_name + ".txt"

        # file_info:file_name = cfile
        # if not matches(FILE_INFO:FILE_TYPE,r"F*"):
        #     return
        
        # INPUT FROM VALUE (cfile) NO_ECHO
        # while True:
        #     IMPORT UNFORMATTED cline
        #     ckey = entry(0, cline, "=")
        #     cvalue = entry(1, cline, "=")

        #     if ckey == "status":
        #         status_txt = cvalue
        # INPUT CLOSE

        # if status_txt.lower()  == ("done").lower() :
        #     file_info:file_name = cfile

        #     if matches(FILE_INFO:FILE_TYPE,r"F*"):
        #         OS_DELETE VALUE (cfile)

        if not os.path.exists(cfile):
            return

        if os.path.exists(cfile):
            with open(cfile, "r") as f:
                cline = f.readline() 

                ckey = cline.split('=')[0]
                cvalue = cline.splite('=')[1]

                if ckey == 'status':
                    status_txt = cvalue

        if status_txt == 'done':
            os.remove(cfile)

    def first_check_running():

        nonlocal response_list_data, from_co_date, to_co_date, non_europe_validation, case_type, user_init, count_data, count_data_processed, lic_nr, start_key, decrypt_data, count_data_failed_decrypt, count_data_failed_already_decrypt, loopi, str, ct, htl_name, count_region, status_txt, guest, res_line, h_bill, history, bill, billhis, paramtext, htparam, nation, queasy, bediener, res_history
        nonlocal bguest, presline, phbill, phistory, pbill, pbillhis, pguest


        nonlocal payload_list, europe_region_list, response_list, bguest, presline, phbill, phistory, pbill, pbillhis, pguest
        nonlocal europe_region_list_data, response_list_data

        cline:string = ""
        ckey:string = ""
        cvalue:string = ""
        cfile:string = ""
        cfile = "/usr1/serverless/src/additional_files/status-" + htl_name + ".txt"

        # file_info:file_name = cfile
        # if not matches(FILE_INFO:FILE_TYPE,r"F*"):
        #     return

        # INPUT FROM VALUE (cfile) NO_ECHO
        # while True:
        #     IMPORT UNFORMATTED cline
        #     ckey = entry(0, cline, "=")
        #     cvalue = entry(1, cline, "=")

        #     if ckey == "status":
        #         status_txt = cvalue
        # INPUT CLOSE

        # if status_txt.lower()  == ("done").lower() :
        #     file_info:file_name = cfile

        #     if matches(FILE_INFO:FILE_TYPE,r"F*"):
        #         OS_DELETE VALUE (cfile)

        if not os.path.exists(cfile):
            return

        if os.path.exists(cfile):
            with open(cfile, "r") as f:
                cline = f.readline() 

                ckey = cline.split('=')[0]
                cvalue = cline.splite('=')[1]

                if ckey == 'status':
                    status_txt = cvalue

        if status_txt == 'done':
            os.remove(cfile)


    def retrieve_start_key():

        nonlocal response_list_data, from_co_date, to_co_date, non_europe_validation, case_type, user_init, count_data, count_data_processed, lic_nr, start_key, decrypt_data, count_data_failed_decrypt, count_data_failed_already_decrypt, loopi, str, ct, htl_name, count_region, status_txt, guest, res_line, h_bill, history, bill, billhis, paramtext, htparam, nation, queasy, bediener, res_history
        nonlocal bguest, presline, phbill, phistory, pbill, pbillhis, pguest


        nonlocal payload_list, europe_region_list, response_list, bguest, presline, phbill, phistory, pbill, pbillhis, pguest
        nonlocal europe_region_list_data, response_list_data

        cencryptedtext = ""
        ccleartext:string = ""
        rencryptedvalue:bytes = None

        def generate_inner_output():
            return (cencryptedtext)

        ccleartext = "billname="

        symmetric_encryption_key = create_cipher_suite(lic_nr)
        symmetric_encryption_iv = os.urandom(16)

        encryptor = Cipher(algorithms.AES(symmetric_encryption_key), modes.OFB(symmetric_encryption_iv), backend=default_backend()).encryptor()
        

        rencryptedvalue = encryptor.update(ccleartext) + encryptor.finalize()
        cencryptedtext = base64_encode(rencryptedvalue)

        return generate_inner_output()


    def proc_dekripsi(rencrypted:string):

        nonlocal response_list_data, from_co_date, to_co_date, non_europe_validation, case_type, user_init, count_data, count_data_processed, lic_nr, start_key, decrypt_data, count_data_failed_decrypt, count_data_failed_already_decrypt, loopi, str, ct, htl_name, count_region, status_txt, guest, res_line, h_bill, history, bill, billhis, paramtext, htparam, nation, queasy, bediener, res_history
        nonlocal bguest, presline, phbill, phistory, pbill, pbillhis, pguest


        nonlocal payload_list, europe_region_list, response_list, bguest, presline, phbill, phistory, pbill, pbillhis, pguest
        nonlocal europe_region_list_data, response_list_data

        cdecrypted = ""
        rdecryptedvalue:bytes = None

        def generate_inner_output():
            return (cdecrypted)

        symmetric_encryption_key = create_cipher_suite(lic_nr)
        symmetric_encryption_iv = os.urandom(16)

        decryptor = Cipher(algorithms.AES(symmetric_encryption_key), modes.OFB(symmetric_encryption_iv), backend=default_backend()).decryptor()

        rdecryptedvalue = base64_decode(rencrypted)
        cdecrypted = decryptor.update(rdecryptedvalue) + decryptor.finalize()

        return generate_inner_output()


    def multi_level_decrypt_guest(encrypted_name:string):

        nonlocal response_list_data, from_co_date, to_co_date, non_europe_validation, case_type, user_init, count_data, count_data_processed, lic_nr, start_key, decrypt_data, count_data_failed_decrypt, count_data_failed_already_decrypt, loopi, str, ct, htl_name, count_region, status_txt, guest, res_line, h_bill, history, bill, billhis, paramtext, htparam, nation, queasy, bediener, res_history
        nonlocal bguest, presline, phbill, phistory, pbill, pbillhis, pguest


        nonlocal payload_list, europe_region_list, response_list, bguest, presline, phbill, phistory, pbill, pbillhis, pguest
        nonlocal europe_region_list_data, response_list_data

        decrypted_name = ""
        temp_str:string = ""
        loop:int = 0

        def generate_inner_output():
            return (decrypted_name)

        decrypted_name = proc_dekripsi(encrypted_name)

        if matches(decrypted_name,r"billname=*"):

            if matches(entry(1, decrypted_name, "="),start_key + r"*"):
                for loop in range(2,num_entries(decrypted_name, "=")  + 1) :
                    temp_str = temp_str + entry(loop - 1, decrypted_name, "=") + "="

                temp_str = substring(temp_str, 0, length(temp_str) - 1)
                decrypted_name = multi_level_decrypt_guest(temp_str)
            else:

                return generate_inner_output()
        else:
            if decrypted_name != None:
                decrypted_name = multi_level_decrypt_guest(decrypted_name)
            else:

                return generate_inner_output()

        return generate_inner_output()


    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})

    if paramtext:
        htl_name = paramtext.ptexte

    htparam = get_cache (Htparam, {"paramnr": [(eq, 448)]})

    if htparam:

        if num_entries(htparam.fchar, ";") > 1:
            for count_region in range(1,num_entries(htparam.fchar, ";")  + 1) :

                if is_integer (entry(count_region - 1, htparam.fchar, ";")):
                    europe_region_list = Europe_region_list()
                    europe_region_list_data.append(europe_region_list)

                    europe_region_list.region_nr = to_int(entry(count_region - 1, htparam.fchar, ";"))

        elif htparam.fchar != None and trim(htparam.fchar) != "":

            if is_integer (htparam.fchar):
                europe_region_list = Europe_region_list()
                europe_region_list_data.append(europe_region_list)

                europe_region_list.region_nr = to_int(htparam.fchar)

    payload_list = query(payload_list_data, first=True)

    if payload_list:
        from_co_date = payload_list.from_co_date
        to_co_date = payload_list.to_co_date
        non_europe_validation = payload_list.non_europe_validation
        case_type = payload_list.case_type
        user_init = payload_list.user_init

        if case_type == 0:
            first_check_running()

        elif case_type == 1:
            get_decrypted_data()

        elif case_type == 2:
            get_status_decrypt()
            
        response_list = Response_list()
        response_list_data.append(response_list)

        response_list.status_process = status_txt

    return generate_output()