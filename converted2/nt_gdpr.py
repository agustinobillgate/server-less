from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Guest, Bill, H_bill, Billhis, Htparam, Paramtext, Nation, Queasy, Guestbook, History

def nt_gdpr():
    bill_date:date = None
    do_it:bool = False
    curr_nat:str = ""
    curr_gastnr:int = 0
    enskrip_str:str = ""
    enskrip_str2:str = ""
    lic_nr:str = ""
    p_466:int = 0
    list_region:str = ""
    list_nat:str = ""
    loopi:int = 0
    res_line = guest = bill = h_bill = billhis = htparam = paramtext = nation = queasy = guestbook = history = None

    nation_list = t_resline = breslin = preslin = reslin = bguest = pguest = mguest = bbill = bhbill = bbillhis = treslin = None

    nation_list_list, Nation_list = create_model("Nation_list", {"nr":int, "kurzbez":str, "bezeich":str})
    t_resline_list, T_resline = create_model("T_resline", {"resnr":int, "reslinnr":int, "gastnr":int, "arrival":date, "depart":date})

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

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, do_it, curr_nat, curr_gastnr, enskrip_str, enskrip_str2, lic_nr, p_466, list_region, list_nat, loopi, res_line, guest, bill, h_bill, billhis, htparam, paramtext, nation, queasy, guestbook, history
        nonlocal breslin, preslin, reslin, bguest, pguest, mguest, bbill, bhbill, bbillhis, treslin


        nonlocal nation_list, t_resline, breslin, preslin, reslin, bguest, pguest, mguest, bbill, bhbill, bbillhis, treslin
        nonlocal nation_list_list, t_resline_list

        return {}

    def proc_enkripsi(lname:str, fname:str, addr1:str, addr2:str, addr3:str, birth_date:date, phone:str, mobile:str, email:str, gender:str, idcard:str, city:str, prov:str, bplace:str, occupancy:str, fax:str, id_card:str, exp_date:date, ccard:str):

        nonlocal bill_date, do_it, curr_nat, curr_gastnr, enskrip_str, enskrip_str2, lic_nr, p_466, list_region, list_nat, loopi, res_line, guest, bill, h_bill, billhis, htparam, paramtext, nation, queasy, guestbook, history
        nonlocal breslin, preslin, reslin, bguest, pguest, mguest, bbill, bhbill, bbillhis, treslin


        nonlocal nation_list, t_resline, breslin, preslin, reslin, bguest, pguest, mguest, bbill, bhbill, bbillhis, treslin
        nonlocal nation_list_list, t_resline_list

        cencryptedtext = ""
        ccleartext:str = ""
        rencryptedvalue:bytes = None

        def generate_inner_output():
            return (cencryptedtext)

        ccleartext = "billname=" + lname + chr(2) +\
                "firstname=" + fname + chr(2) +\
                "birthdate=" + to_string(birth_date) + chr(2) +\
                "gender=" + gender + chr(2) +\
                "address1=" + addr1 + chr(2) +\
                "address2=" + addr2 + chr(2) +\
                "address3=" + addr3 + chr(2) +\
                "phone=" + phone + chr(2) +\
                "mobile=" + mobile + chr(2) +\
                "email=" + email + chr(2) +\
                "idcard=" + idcard + chr(2) +\
                "city=" + city + chr(2) +\
                "prov=" + prov + chr(2) +\
                "birthplace=" + bplace + chr(2) +\
                "occupancy=" + occupancy + chr(2) +\
                "telefax=" + fax + chr(2) +\
                "idcard=" + id_card + chr(2) +\
                "expiredate=" + to_string(exp_date) + chr(2) +\
                "ccard=" + ccard


        security_policy:symmetric_encryption_algorithm = "AES_OFB_128"
        security_policy:symmetric_encryption_key = create_cipher_suite(lic_nr)
        security_policy:symmetric_encryption_iv = None
        rencryptedvalue = Encrypt (ccleartext)
        cencryptedtext = base64_encode(rencryptedvalue)

        return generate_inner_output()


    def proc_enkripsi_bill(lname:str):

        nonlocal bill_date, do_it, curr_nat, curr_gastnr, enskrip_str, enskrip_str2, lic_nr, p_466, list_region, list_nat, loopi, res_line, guest, bill, h_bill, billhis, htparam, paramtext, nation, queasy, guestbook, history
        nonlocal breslin, preslin, reslin, bguest, pguest, mguest, bbill, bhbill, bbillhis, treslin


        nonlocal nation_list, t_resline, breslin, preslin, reslin, bguest, pguest, mguest, bbill, bhbill, bbillhis, treslin
        nonlocal nation_list_list, t_resline_list

        cencryptedtext = ""
        ccleartext:str = ""
        rencryptedvalue:bytes = None

        def generate_inner_output():
            return (cencryptedtext)

        ccleartext = "billname=" + lname


        security_policy:symmetric_encryption_algorithm = "AES_OFB_128"
        security_policy:symmetric_encryption_key = create_cipher_suite(lic_nr)
        security_policy:symmetric_encryption_iv = None
        rencryptedvalue = Encrypt (ccleartext)
        cencryptedtext = base64_encode(rencryptedvalue)

        return generate_inner_output()


    def proc_historynbill():

        nonlocal bill_date, do_it, curr_nat, curr_gastnr, enskrip_str, lic_nr, p_466, list_region, list_nat, loopi, res_line, guest, bill, h_bill, billhis, htparam, paramtext, nation, queasy, guestbook, history
        nonlocal breslin, preslin, reslin, bguest, pguest, mguest, bbill, bhbill, bbillhis, treslin


        nonlocal nation_list, t_resline, breslin, preslin, reslin, bguest, pguest, mguest, bbill, bhbill, bbillhis, treslin
        nonlocal nation_list_list, t_resline_list

        curr_info:str = ""
        enskrip_str1:str = ""
        enskrip_str2:str = ""

        for t_resline in query(t_resline_list):

            history = db_session.query(History).filter(
                     (History.gastnr == t_resline.gastnr) & (History.resnr == t_resline.resnr)).first()

            if history:
                enskrip_str1 = proc_enkripsi_bill(history.gastinfo)

                if enskrip_str1 != " ":
                    history.gastinfo = enskrip_str


                    pass

            h_bill = db_session.query(H_bill).filter(
                     (H_bill.resnr == t_resline.resnr) & (H_bill.reslinnr == t_resline.reslinnr)).first()
            while None != h_bill:
                enskrip_str2 = proc_enkripsi_bill(h_bill.bilname)

                if enskrip_str2 != " ":

                    bhbill = db_session.query(Bhbill).filter(
                             (Bhbill._recid == h_bill._recid)).first()
                    bhbill.bilname = enskrip_str


                    pass

                curr_recid = h_bill._recid
                h_bill = db_session.query(H_bill).filter(
                         (H_bill.resnr == t_resline.resnr) & (H_bill.reslinnr == t_resline.reslinnr) & (H_bill._recid > curr_recid)).first()

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

                nation_list = query(nation_list_list, filters=(lambda nation_list: nation_list.nr == nation.nationnr), first=True)

                if not nation_list:
                    nation_list = Nation_list()
                    nation_list_list.append(nation_list)

                    nation_list.nr = nation.nationnr
                    nation_list.kurzbez = nation.kurzbez
                    nation_list.bezeich = entry(0, nation.bezeich, ";")


    else:

        nation_obj_list = []
        for nation, queasy in db_session.query(Nation, Queasy).join(Queasy,(Queasy.key == 6) & (Queasy.number1 == Nation.untergruppe) & (func.lower(Queasy.char1).op("~")(("*europe*".lower().replace("*",".*"))))).filter(
                 (Nation.natcode == 0)).order_by(Nation.kurzbez).all():
            if nation._recid in nation_obj_list:
                continue
            else:
                nation_obj_list.append(nation._recid)

            nation_list = query(nation_list_list, filters=(lambda nation_list: nation_list.nr == nation.nationnr), first=True)

            if not nation_list:
                nation_list = Nation_list()
                nation_list_list.append(nation_list)

                nation_list.nr = nation.nationnr
                nation_list.kurzbez = nation.kurzbez
                nation_list.bezeich = entry(0, nation.bezeich, ";")

    if list_nat != "":
        for loopi in range(1,num_entries(list_nat, ";")  + 1) :

            for nation in db_session.query(Nation).filter(
                     (Nation.natcode == 0) & (Nation.nationnr == to_int(entry(loopi - 1, list_nat, ";")))).order_by(Nation.kurzbez).all():

                nation_list = query(nation_list_list, filters=(lambda nation_list: nation_list.nr == nation.nationnr), first=True)

                if not nation_list:
                    nation_list = Nation_list()
                    nation_list_list.append(nation_list)

                    nation_list.nr = nation.nationnr
                    nation_list.kurzbez = nation.kurzbez
                    nation_list.bezeich = entry(0, nation.bezeich, ";")

    if p_466 != 0:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resstatus == 8) & (Res_line.abreise <= bill_date - timedelta(days=p_466))).first()
        while None != res_line:

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == res_line.gastnrmember) & (Guest.vornamekind[inc_value(5)] == " ")).first()

            if guest:

                if re.match(r".*GDPRyes.*",res_line.zimmer_wunsch, re.IGNORECASE):
                    do_it = True
                else:
                    do_it = False

                if do_it:

                    reslin = db_session.query(Reslin).filter(
                             (Reslin.gastnrmember == guest.gastnr) & (Reslin.resstatus != 8) & (Reslin.resstatus != 9) & (Reslin.resstatus != 10) & (Reslin.resstatus != 12) & (Reslin.resstatus != 13) & (Reslin.resstatus != 99)).first()

                    if reslin:

                        bguest = db_session.query(Bguest).filter(
                                 (Bguest.gastnr != None)).order_by(Bguest._recid.desc()).first()

                        if bguest:
                            curr_gastnr = bguest.gastnr + 1

                        breslin = db_session.query(Breslin).filter(
                                 (Breslin.gastnrmember == guest.gastnr) & (Breslin.resstatus != 8) & (Breslin.resstatus != 9) & (Breslin.resstatus != 10) & (Breslin.resstatus != 12) & (Breslin.resstatus != 13) & (Breslin.resstatus != 99)).first()
                        while None != breslin:

                            preslin = db_session.query(Preslin).filter(
                                     (Preslin._recid == breslin._recid)).first()

                            if preslin:
                                preslin.gastnrmember = curr_gastnr


                                pass

                            curr_recid = breslin._recid
                            breslin = db_session.query(Breslin).filter(
                                     (Breslin.gastnrmember == guest.gastnr) & (Breslin.resstatus != 8) & (Breslin.resstatus != 9) & (Breslin.resstatus != 10) & (Breslin.resstatus != 12) & (Breslin.resstatus != 13) & (Breslin.resstatus != 99) & (Breslin._recid > curr_recid)).first()
                        pguest = Pguest()
                        db_session.add(pguest)

                        buffer_copy(guest, pguest,except_fields=["guest.gastnr"])
                        pguest.gastnr = curr_gastnr

                    t_resline = query(t_resline_list, filters=(lambda t_resline: t_resline.resnr == res_line.resnr and t_resline.reslinnr == res_line.reslinnr), first=True)

                    if not t_resline:
                        t_resline = T_resline()
                        t_resline_list.append(t_resline)

                        t_resline.resnr = res_line.resnr
                        t_resline.reslinnr = res_line.reslinnr
                        t_resline.arrival = res_line.ankunft
                        t_resline.depart = res_line.abreise
                        t_resline.gastnr = res_line.gastnrmember

                    guestbook = db_session.query(Guestbook).filter(
                             (Guestbook.gastnr == guest.gastnr)).first()

                    if guestbook:
                        db_session.delete(guestbook)
                        pass

                    for bill in db_session.query(Bill).filter(
                             (Bill.resnr == res_line.resnr) & (Bill.reslinnr == res_line.reslinnr)).order_by(Bill._recid).all():
                        enskrip_str = proc_enkripsi_bill(bill.bilname)

                        bbill = db_session.query(Bbill).filter(
                                 (Bbill._recid == bill._recid)).first()
                        bbill.bilname = enskrip_str


                        pass

                    for billhis in db_session.query(Billhis).filter(
                             (Billhis.resnr == res_line.resnr) & (Billhis.reslinnr == res_line.reslinnr)).order_by(Billhis._recid).all():
                        enskrip_str = proc_enkripsi_bill(billhis.name)

                        bbillhis = db_session.query(Bbillhis).filter(
                                 (Bbillhis._recid == billhis._recid)).first()
                        bbillhis.name = enskrip_str


                        pass

                    treslin = db_session.query(Treslin).filter(
                             (Treslin.resnr == res_line.resnr) & (Treslin.reslinnr == res_line.reslinnr)).first()

                    if treslin:
                        enskrip_str2 = proc_enkripsi_bill(treslin.NAME)
                        treslin.name = enskrip_str2


                        pass

                    if guest.vornamekind[5] == " ":
                        enskrip_str = proc_enkripsi(guest.anrede1, guest.vorname1, guest.adresse1, guest.adresse2, guest.adresse3, guest.geburtdatum1, guest.telefon, guest.mobil_telefon, guest.email_adr, guest.geschlecht, guest.geburt_ort1, guest.plz, guest.geburt_ort2, guest.telex, guest.beruf, guest.fax, guest.ausweis_nr1, guest.geburtdatum2, guest.ausweis_nr2)

                        if enskrip_str != "":

                            mguest = db_session.query(Mguest).filter(
                                     (Mguest.gastnr == guest.gastnr)).first()
                            mguest.name = enskrip_str2
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

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.resstatus == 8) & (Res_line.abreise <= bill_date - timedelta(days=p_466)) & (Res_line._recid > curr_recid)).first()
        proc_historynbill()

    return generate_output()