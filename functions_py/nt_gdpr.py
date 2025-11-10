#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Guest, Res_line, Bill, H_bill, Billhis, Queasy, Htparam, Paramtext, Nation, Guestbook, History
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

import tempfile as tp
import os
import re
import shutil

def nt_gdpr():

    prepare_cache ([Guest, Res_line, Bill, H_bill, Billhis, Queasy, Htparam, Paramtext, Nation, History])

    bill_date:date = None
    do_it:bool = False
    curr_nat:string = ""
    curr_gastnr:int = 0
    enskrip_str:string = ""
    enskrip_str2:string = ""
    lic_nr:string = ""
    p_466:int = 0
    list_region:string = ""
    list_nat:string = ""
    loopi:int = 0
    last_gastnr:int = 0
    encrypt_guest:bool = False
    guest = res_line = bill = h_bill = billhis = queasy = htparam = paramtext = nation = guestbook = history = None

    nation_list = guest_list = t_resline = breslin = preslin = reslin = bguest = pguest = mguest = bbill = bhbill = bbillhis = treslin = bqueasy = None

    nation_list_data, Nation_list = create_model("Nation_list", {"nr":int, "kurzbez":string, "bezeich":string})
    guest_list_data, Guest_list = create_model_like(Guest)
    t_resline_data, T_resline = create_model("T_resline", {"resnr":int, "reslinnr":int, "gastnr":int, "arrival":date, "depart":date})

    Breslin = create_buffer("Breslin",Res_line)
    Preslin = create_buffer("Preslin",Res_line)
    Reslin = create_buffer("Reslin",Res_line)
    Bguest = create_buffer("Bguest",Guest)
    Pguest = create_buffer("Pguest",Guest)
    Mguest = create_buffer("Mguest",Guest)
    Bbill = create_buffer("Bbill",Bill)
    Bhbill = create_buffer("Bhbill",H_bill)
    Bbillhis = create_buffer("Bbillhis",Billhis)
    Treslin = create_buffer("Treslin",Res_line)
    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, do_it, curr_nat, curr_gastnr, enskrip_str, enskrip_str2, lic_nr, p_466, list_region, list_nat, loopi, last_gastnr, encrypt_guest, guest, res_line, bill, h_bill, billhis, queasy, htparam, paramtext, nation, guestbook, history
        nonlocal breslin, preslin, reslin, bguest, pguest, mguest, bbill, bhbill, bbillhis, treslin, bqueasy


        nonlocal nation_list, guest_list, t_resline, breslin, preslin, reslin, bguest, pguest, mguest, bbill, bhbill, bbillhis, treslin, bqueasy
        nonlocal nation_list_data, guest_list_data, t_resline_data

        return {}

    def proc_historynbill():

        nonlocal bill_date, do_it, curr_nat, curr_gastnr, enskrip_str, lic_nr, p_466, list_region, list_nat, loopi, last_gastnr, encrypt_guest, guest, res_line, bill, h_bill, billhis, queasy, htparam, paramtext, nation, guestbook, history
        nonlocal breslin, preslin, reslin, bguest, pguest, mguest, bbill, bhbill, bbillhis, treslin, bqueasy


        nonlocal nation_list, guest_list, t_resline, breslin, preslin, reslin, bguest, pguest, mguest, bbill, bhbill, bbillhis, treslin, bqueasy
        nonlocal nation_list_data, guest_list_data, t_resline_data

        curr_info:string = ""
        enskrip_str1:string = ""
        enskrip_str2:string = ""

        for t_resline in query(t_resline_data):

            history = get_cache (History, {"gastnr": [(eq, t_resline.gastnr)],"resnr": [(eq, t_resline.resnr)]})

            if history:
                enskrip_str1 = reencrypt_billname(history.gastinfo)

                if enskrip_str1 != " ":
                    pass
                    history.gastinfo = enskrip_str1


                    pass
                    pass

            h_bill = get_cache (H_bill, {"resnr": [(eq, t_resline.resnr)],"reslinnr": [(eq, t_resline.reslinnr)]})
            while None != h_bill:
                enskrip_str2 = reencrypt_billname(h_bill.bilname)

                if enskrip_str2 != " ":

                    bhbill = get_cache (H_bill, {"_recid": [(eq, h_bill._recid)]})
                    bhbill.bilname = enskrip_str2


                    pass
                    pass

                curr_recid = h_bill._recid
                h_bill = db_session.query(H_bill).filter(
                         (H_bill.resnr == t_resline.resnr) & (H_bill.reslinnr == t_resline.reslinnr) & (H_bill._recid > curr_recid)).first()


    def reencrypt_billname(input_str:string):

        nonlocal bill_date, do_it, curr_nat, curr_gastnr, enskrip_str, enskrip_str2, lic_nr, p_466, list_region, list_nat, loopi, last_gastnr, encrypt_guest, guest, res_line, bill, h_bill, billhis, queasy, htparam, paramtext, nation, guestbook, history
        nonlocal breslin, preslin, reslin, bguest, pguest, mguest, bbill, bhbill, bbillhis, treslin, bqueasy


        nonlocal nation_list, guest_list, t_resline, breslin, preslin, reslin, bguest, pguest, mguest, bbill, bhbill, bbillhis, treslin, bqueasy
        nonlocal nation_list_data, guest_list_data, t_resline_data

        lname = ""
        is_original_str:bool = False
        was_encrypted:bool = False
        i:int = 0

        def generate_inner_output():
            return (lname)

        while not is_original_str:
            i = i + 1
            lname, is_original_str = decrypt_name(input_str)
            input_str = lname

            if i > 1:
                was_encrypted = True

        lname = proc_enkripsi_bill(lname)

        return generate_inner_output()


    def decrypt_name(cencryptedtext:string):

        nonlocal bill_date, do_it, curr_nat, curr_gastnr, enskrip_str, enskrip_str2, lic_nr, p_466, list_region, list_nat, loopi, last_gastnr, encrypt_guest, guest, res_line, bill, h_bill, billhis, queasy, htparam, paramtext, nation, guestbook, history
        nonlocal breslin, preslin, reslin, bguest, pguest, mguest, bbill, bhbill, bbillhis, treslin, bqueasy


        nonlocal nation_list, guest_list, t_resline, breslin, preslin, reslin, bguest, pguest, mguest, bbill, bhbill, bbillhis, treslin, bqueasy
        nonlocal nation_list_data, guest_list_data, t_resline_data

        lname = ""
        is_original_str = False
        rencryptedvalue:bytes = None
        ccleartext:string = ""

        def generate_inner_output():
            return (lname, is_original_str)

        symmetric_encryption_key = create_cipher_suite(lic_nr)
        symmetric_encryption_iv = os.urandom(16)

        decryptor = Cipher(algorithms.AES(symmetric_encryption_key), modes.OFB(symmetric_encryption_iv), backend=default_backend()).decryptor()

        rencryptedvalue = base64_decode(cencryptedtext)
        ccleartext = decryptor.update(rencryptedvalue) + decryptor.finalize()

        if matches(ccleartext,r"billname=*"):
            lname = replace_str(ccleartext, "billname=", "")
        else:
            lname = cencryptedtext
            is_original_str = True

        return generate_inner_output()


    def proc_enkripsi_bill(lname:string):

        nonlocal bill_date, do_it, curr_nat, curr_gastnr, enskrip_str, enskrip_str2, lic_nr, p_466, list_region, list_nat, loopi, last_gastnr, encrypt_guest, guest, res_line, bill, h_bill, billhis, queasy, htparam, paramtext, nation, guestbook, history
        nonlocal breslin, preslin, reslin, bguest, pguest, mguest, bbill, bhbill, bbillhis, treslin, bqueasy


        nonlocal nation_list, guest_list, t_resline, breslin, preslin, reslin, bguest, pguest, mguest, bbill, bhbill, bbillhis, treslin, bqueasy
        nonlocal nation_list_data, guest_list_data, t_resline_data

        cencryptedtext = ""
        ccleartext:string = ""
        rencryptedvalue:bytes = None

        def generate_inner_output():
            return (cencryptedtext)

        ccleartext = "billname=" + lname

        symmetric_encryption_key = create_cipher_suite(lic_nr)
        symmetric_encryption_iv = os.urandom(16)

        encryptor = Cipher(algorithms.AES(symmetric_encryption_key), modes.OFB(symmetric_encryption_iv), backend=default_backend()).encryptor()

        rencryptedvalue = encryptor.update(ccleartext) + encryptor.finalize()
        cencryptedtext = base64_encode(rencryptedvalue)

        return generate_inner_output()


    def proc_enkripsi(lname:string, fname:string, addr1:string, addr2:string, addr3:string, birth_date:date, phone:string, mobile:string, email:string, gender:string, idcard:string, city:string, prov:string, bplace:string, occupancy:string, fax:string, id_card:string, exp_date:date, ccard:string):

        nonlocal bill_date, do_it, curr_nat, curr_gastnr, enskrip_str, enskrip_str2, lic_nr, p_466, list_region, list_nat, loopi, last_gastnr, encrypt_guest, guest, res_line, bill, h_bill, billhis, queasy, htparam, paramtext, nation, guestbook, history
        nonlocal breslin, preslin, reslin, bguest, pguest, mguest, bbill, bhbill, bbillhis, treslin, bqueasy


        nonlocal nation_list, guest_list, t_resline, breslin, preslin, reslin, bguest, pguest, mguest, bbill, bhbill, bbillhis, treslin, bqueasy
        nonlocal nation_list_data, guest_list_data, t_resline_data

        cencryptedtext = ""
        ccleartext:string = ""
        rencryptedvalue:bytes = None
        birthdatestr:string = ""
        expdatestr:string = ""

        def generate_inner_output():
            return (cencryptedtext)


        if lname == None:
            lname = ""

        if fname == None:
            fname = ""

        if to_string(birth_date) == None:
            birthdatestr = ""
        else:
            birthdatestr = to_string(birth_date)

        if gender == None:
            gender = ""

        if addr1 == None:
            addr1 = ""

        if addr2 == None:
            addr2 = ""

        if addr3 == None:
            addr3 = ""

        if phone == None:
            phone = ""

        if mobile == None:
            mobile = ""

        if email == None:
            email = ""

        if idcard == None:
            idcard = ""

        if city == None:
            city = ""

        if prov == None:
            prov = ""

        if bplace == None:
            bplace = ""

        if occupancy == None:
            occupancy = ""

        if fax == None:
            fax = ""

        if id_card == None:
            id_card = ""

        if to_string(exp_date) == None:
            expdatestr = ""
        else:
            expdatestr = to_string(exp_date)

        if ccard == None:
            ccard = ""
            
        ccleartext = "billname=" + lname + chr_unicode(2) +\
                "firstname=" + fname + chr_unicode(2) +\
                "birthdate=" + birthdatestr + chr_unicode(2) +\
                "gender=" + gender + chr_unicode(2) +\
                "address1=" + addr1 + chr_unicode(2) +\
                "address2=" + addr2 + chr_unicode(2) +\
                "address3=" + addr3 + chr_unicode(2) +\
                "phone=" + phone + chr_unicode(2) +\
                "mobile=" + mobile + chr_unicode(2) +\
                "email=" + email + chr_unicode(2) +\
                "idcard=" + idcard + chr_unicode(2) +\
                "city=" + city + chr_unicode(2) +\
                "prov=" + prov + chr_unicode(2) +\
                "birthplace=" + bplace + chr_unicode(2) +\
                "occupancy=" + occupancy + chr_unicode(2) +\
                "telefax=" + fax + chr_unicode(2) +\
                "idcard=" + id_card + chr_unicode(2) +\
                "expiredate=" + expdatestr + chr_unicode(2) +\
                "ccard=" + ccard


        symmetric_encryption_key = create_cipher_suite(lic_nr)
        symmetric_encryption_iv = os.urandom(16)

        encryptor = Cipher(algorithms.AES(symmetric_encryption_key), modes.OFB(symmetric_encryption_iv), backend=default_backend()).encryptor()

        rencryptedvalue = encryptor.update(ccleartext) + encryptor.finalize()
        cencryptedtext = base64_encode(rencryptedvalue)

        return generate_inner_output()


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()

    if htparam:
        bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 466)).first()

    if htparam:
        p_466 = htparam.finteger

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 243)).first()

    if paramtext:
        lic_nr = paramtext.ptexte

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 448)).first()

    if htparam:
        list_region = htparam.fchar

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 449)).first()

    if htparam:
        list_nat = htparam.fchar

    if list_region != "":
        for loopi in range(1,num_entries(list_region, ";")  + 1) :

            for nation in db_session.query(Nation).filter(
                     (Nation.natcode == 0) & (Nation.untergruppe == to_int(entry(loopi - 1, list_region, ";")))).order_by(Nation.kurzbez).all():

                nation_list = query(nation_list_data, filters=(lambda nation_list: nation_list.nr == nation.nationnr), first=True)

                if not nation_list:
                    nation_list = Nation_list()
                    nation_list_data.append(nation_list)

                    nation_list.nr = nation.nationnr
                    nation_list.kurzbez = nation.kurzbez
                    nation_list.bezeich = entry(0, nation.bezeich, ";")


    else:

        nation_obj_list = {}
        nation = Nation()
        queasy = Queasy()
        for nation, queasy in db_session.query(Nation, Queasy).join(Queasy,(Queasy.key == 6) & (Queasy.number1 == Nation.untergruppe) & (func.lower(Queasy.char1).op("~")(("*europe*".lower().replace("*",".*"))))).filter((Nation.natcode == 0)).order_by(Nation.kurzbez).all():

            if nation_obj_list.get(nation._recid):
                continue
            else:
                nation_obj_list[nation._recid] = True

            nation_list = query(nation_list_data, filters=(lambda nation_list: nation_list.nr == nation.nationnr), first=True)

            if not nation_list:
                nation_list = Nation_list()
                nation_list_data.append(nation_list)

                nation_list.nr = nation.nationnr
                nation_list.kurzbez = nation.kurzbez
                nation_list.bezeich = entry(0, nation.bezeich, ";")

    if list_nat != "":
        for loopi in range(1,num_entries(list_nat, ";")  + 1) :

            for nation in db_session.query(Nation).filter(
                     (Nation.natcode == 0) & (Nation.nationnr == to_int(entry(loopi - 1, list_nat, ";")))).order_by(Nation.kurzbez).all():

                nation_list = query(nation_list_data, filters=(lambda nation_list: nation_list.nr == nation.nationnr), first=True)

                if not nation_list:
                    nation_list = Nation_list()
                    nation_list_data.append(nation_list)

                    nation_list.nr = nation.nationnr
                    nation_list.kurzbez = nation.kurzbez
                    nation_list.bezeich = entry(0, nation.bezeich, ";")

    if p_466 != 0:

        for res_line in db_session.query(Res_line).filter((Res_line.resstatus == 8) & (Res_line.abreise == bill_date - timedelta(days=p_466)) & (matches(Res_line.zimmer_wunsch,"*GDPRyes*"))).order_by(Res_line._recid).all():

            t_resline = query(t_resline_data, filters=(lambda t_resline: t_resline.resnr == res_line.resnr and t_resline.reslinnr == res_line.reslinnr), first=True)

            if not t_resline:
                t_resline = T_resline()
                t_resline_data.append(t_resline)

                t_resline.resnr = res_line.resnr
                t_resline.reslinnr = res_line.reslinnr
                t_resline.arrival = res_line.ankunft
                t_resline.depart = res_line.abreise
                t_resline.gastnr = res_line.gastnrmember

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 378) & (Queasy.logi1)).order_by(Queasy._recid).all():

            t_resline = query(t_resline_data, filters=(lambda t_resline: t_resline.resnr == queasy.number2 and t_resline.reslinnr == queasy.number3), first=True)

            if not t_resline:

                res_line = get_cache (Res_line, {"resnr": [(eq, queasy.number2)],"reslinnr": [(eq, queasy.number3)]})

                if res_line:
                    t_resline = T_resline()
                    t_resline_data.append(t_resline)

                    t_resline.resnr = res_line.resnr
                    t_resline.reslinnr = res_line.reslinnr
                    t_resline.arrival = res_line.ankunft
                    t_resline.depart = res_line.abreise
                    t_resline.gastnr = res_line.gastnrmember

            bqueasy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})
            bqueasy.logi1 = False


            pass
            pass

    t_resline = query(t_resline_data, first=True)

    if t_resline:

        for t_resline in query(t_resline_data):

            res_line = get_cache (Res_line, {"resnr": [(eq, t_resline.resnr)],"reslinnr": [(eq, t_resline.reslinnr)]})

            if res_line:

                if matches(res_line.zimmer_wunsch,r"*GDPRyes*"):
                    do_it = True
                else:
                    do_it = False

                if do_it:

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    if guest:
                        curr_gastnr = guest.gastnr

                        if guest.vornamekind[5] == " ":

                            guest_list = query(guest_list_data, filters=(lambda guest_list: guest_list.gastnr == guest.gastnr), first=True)

                            if not guest_list:
                                guest_list = Guest_list()
                                guest_list_data.append(guest_list)

                                buffer_copy(guest, guest_list)
                            enskrip_str = ""


                            enskrip_str = proc_enkripsi(guest.anrede1, guest.vorname1, guest.adresse1, guest.adresse2, guest.adresse3, guest.geburtdatum1, guest.telefon, guest.mobil_telefon, guest.email_adr, guest.geschlecht, guest.geburt_ort1, guest.plz, guest.geburt_ort2, guest.telex, guest.beruf, guest.fax, guest.ausweis_nr1, guest.geburtdatum2, guest.ausweis_nr2)

                            if enskrip_str != "":

                                mguest = get_cache (Guest, {"gastnr": [(eq, guest.gastnr)]})
                                mguest.name = enskrip_str
                                mguest.anrede1 = " "
                                mguest.vorname1 = " "
                                mguest.adresse1 = " "
                                mguest.adresse2 = " "
                                mguest.adresse3 = " "
                                mguest.geburtdatum1 = None
                                mguest.telefon = " "
                                mguest.mobil_telefon = " "
                                mguest.email_adr = " "
                                mguest.geschlecht = " "
                                mguest.geschlecht = " "
                                mguest.geburt_ort1 = " "
                                mguest.plz = " "
                                mguest.geburt_ort2 = " "
                                mguest.telex = " "
                                mguest.beruf = " "
                                mguest.fax = " "
                                mguest.ausweis_nr1 = " "
                                mguest.geburtdatum2 = None
                                mguest.ausweis_nr2 = " "
                                mguest.vornamekind[5] = enskrip_str


                                pass
                                pass

                    guestbook = get_cache (Guestbook, {"gastnr": [(eq, curr_gastnr)]})

                    if guestbook:
                        pass
                        db_session.delete(guestbook)
                        pass

                    for bill in db_session.query(Bill).filter(
                             (Bill.resnr == res_line.resnr) & (Bill.reslinnr == res_line.reslinnr)).order_by(Bill._recid).all():
                        enskrip_str = ""


                        enskrip_str = reencrypt_billname(bill.bilname)

                        bbill = get_cache (Bill, {"_recid": [(eq, bill._recid)]})
                        bbill.bilname = enskrip_str


                        pass
                        pass

                    for billhis in db_session.query(Billhis).filter(
                             (Billhis.resnr == res_line.resnr) & (Billhis.reslinnr == res_line.reslinnr)).order_by(Billhis._recid).all():
                        enskrip_str = ""


                        enskrip_str = reencrypt_billname(billhis.NAME)

                        bbillhis = get_cache (Billhis, {"_recid": [(eq, billhis._recid)]})
                        bbillhis.name = enskrip_str


                        pass
                        pass

                    treslin = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                    if treslin:
                        enskrip_str2 = ""


                        enskrip_str2 = reencrypt_billname(treslin.NAME)
                        pass
                        treslin.name = enskrip_str2


                        pass
                        pass

    guest_list = query(guest_list_data, first=True)

    if guest_list:

        for guest_list in query(guest_list_data):

            bguest = db_session.query(Bguest).filter(
                     (Bguest.gastnr != None)).order_by(Bguest._recid.desc()).first()

            if bguest:
                last_gastnr = bguest.gastnr + 1
            pguest = Guest()
            db_session.add(pguest)

            buffer_copy(guest_list, pguest,except_fields=["guest_list.gastnr"])
            pguest.gastnr = last_gastnr

            for reslin in db_session.query(Reslin).filter(
                     (Reslin.gastnrmember == guest_list.gastnr) & (Reslin.resstatus != 8) & (Reslin.resstatus != 9) & (Reslin.resstatus != 10) & (Reslin.resstatus != 12) & (Reslin.resstatus != 13) & (Reslin.resstatus != 99)).order_by(Reslin._recid).all():

                preslin = get_cache (Res_line, {"_recid": [(eq, reslin._recid)]})

                if preslin:
                    pass
                    preslin.gastnrmember = last_gastnr


                    pass
                    pass

    proc_historynbill()

    return generate_output()