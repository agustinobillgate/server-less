from functions.additional_functions import *
import decimal
from models import Guest, Htparam, Bill, Res_line, Arrangement, Queasy

def credit_limit_1bl(incl_master:bool, by_room:bool):
    cl_list_list = []
    saldo:decimal = 0
    climit:int = 0
    g_climit:decimal = 0
    loopi:int = 0
    str:str = ""
    guest = htparam = bill = res_line = arrangement = queasy = None

    cl_list = bguest = None

    cl_list_list, Cl_list = create_model("Cl_list", {"flag":str, "rechnr":int, "zinr":str, "receiver":str, "ankunft":date, "abreise":date, "c_limit":decimal, "saldo":decimal, "name":str, "resnr":int, "comp_name":str, "rmrate":decimal, "rate_code":str, "argt_code":str, "pay_type":str, "over":decimal, "remark":str, "stafid":str}, {"ankunft": None, "abreise": None})

    Bguest = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cl_list_list, saldo, climit, g_climit, loopi, str, guest, htparam, bill, res_line, arrangement, queasy
        nonlocal bguest


        nonlocal cl_list, bguest
        nonlocal cl_list_list
        return {"cl-list": cl_list_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 68)).first()

    if htparam.fdecimal != 0:
        g_climit = htparam.fdecimal
    else:
        g_climit = htparam.finteger
    cl_list_list.clear()

    for bill in db_session.query(Bill).filter(
            (Bill.flag == 0) &  (Bill.resnr == 0)).all():

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == bill.gastnr)).first()

        if guest and guest.kreditlimit > 0:
            climit = guest.kreditlimit
        else:
            climit = g_climit

        if bill.saldo > climit:
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.flag = "NS"
            cl_list.name = bill.name
            cl_list.receiver = bill.name
            cl_list.c_limit = climit
            cl_list.rechnr = bill.rechnr
            cl_list.saldo = bill.saldo
            cl_list.ankunft = None
            cl_list.abreise = None
            cl_list.comp_name = guest.name
            cl_list.rmrate = 0
            cl_list.rate_code = " "
            cl_list.argt_code = " "
            cl_list.pay_type = " "
            cl_list.over = bill.saldo - climit
            cl_list.remark = " "
            cl_list.stafid = " "

    if incl_master:

        for bill in db_session.query(Bill).filter(
                (Bill.flag == 0) &  (Bill.resnr > 0) &  (Bill.zinr == "")).all():

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == bill.gastnr)).first()

            if guest and guest.kreditlimit > 0:
                climit = guest.kreditlimit
            else:
                climit = g_climit

            if bill.saldo > climit:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == 1)).first()
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.flag = "M"
                cl_list.name = bill.name
                cl_list.receiver = bill.name
                cl_list.c_limit = climit
                cl_list.rechnr = bill.rechnr
                cl_list.saldo = bill.saldo

                if res_line:
                    cl_list.ankunft = res_line.ankunft
                    cl_list.abreise = res_line.abreise
                    cl_list.rmrate = res_line.zipreis
                    cl_list.over = bill.saldo - climit
                    cl_list.remark = " "
                    cl_list.stafid = " "

                    bguest = db_session.query(Bguest).filter(
                            (Bguest.gastnr == res_line.gastnr)).first()

                    if bguest:
                        cl_list.comp_name = guest.name

                    arrangement = db_session.query(Arrangement).filter(
                            (Arrangement == res_line.arrangement)).first()

                    if arrangement:
                        cl_list.argt_code = arrangement.argt_bez

                    if res_line.code != "" and res_line.CODE.lower()  != "0":

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.code))).first()

                        if queasy:
                            cl_list.pay_type = queasy.char1


                    for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == "$CODE$":
                            cl_list.rate_code = substring(str, 6)
                            break


    if not by_room:

        for bill in db_session.query(Bill).filter(
                (Bill.flag == 0) &  (Bill.resnr > 0) &  (Bill.zinr != "")).all():

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == bill.gastnr)).first()

            if guest and guest.kreditlimit > 0:
                climit = guest.kreditlimit
            else:
                climit = g_climit

            if bill.saldo > climit:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.reslinnr)).first()
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.zinr = bill.zinr
                cl_list.resnr = bill.resnr
                cl_list.receiver = guest.name + ", " + guest.vorname1 + " " +\
                        guest.anrede1 + guest.anredefirma
                cl_list.c_limit = climit
                cl_list.rechnr = bill.rechnr
                cl_list.saldo = bill.saldo
                cl_list.ankunft = res_line.ankunft
                cl_list.abreise = res_line.abreise

                if res_line:
                    cl_list.name = res_line.name
                    cl_list.rmrate = res_line.zipreis
                    cl_list.over = bill.saldo - climit
                    cl_list.remark = " "
                    cl_list.stafid = " "

                    bguest = db_session.query(Bguest).filter(
                            (Bguest.gastnr == res_line.gastnr)).first()

                    if bguest:
                        cl_list.comp_name = guest.name

                    arrangement = db_session.query(Arrangement).filter(
                            (Arrangement == res_line.arrangement)).first()

                    if arrangement:
                        cl_list.argt_code = arrangement.argt_bez

                    if res_line.code != "" and res_line.CODE.lower()  != "0":

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.code))).first()

                        if queasy:
                            cl_list.pay_type = queasy.char1


                    for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == "$CODE$":
                            cl_list.rate_code = substring(str, 6)
                            break

    else:

        for bill in db_session.query(Bill).filter(
                (Bill.flag == 0) &  (Bill.resnr > 0) &  (Bill.zinr != "")).all():

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == bill.gastnr)).first()

            if guest and guest.kreditlimit > 0:
                climit = guest.kreditlimit
            else:
                climit = g_climit

            if bill.saldo > climit:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.reslinnr)).first()
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.zinr = bill.zinr
                cl_list.resnr = bill.resnr
                cl_list.receiver = guest.name + ", " + guest.vorname1 + " " +\
                        guest.anrede1 + guest.anredefirma
                cl_list.c_limit = climit
                cl_list.rechnr = bill.rechnr
                cl_list.saldo = bill.saldo
                cl_list.ankunft = res_line.ankunft
                cl_list.abreise = res_line.abreise

                if res_line:
                    cl_list.name = res_line.name
                    cl_list.rmrate = res_line.zipreis
                    cl_list.over = bill.saldo - climit
                    cl_list.remark = " "
                    cl_list.stafid = " "

                    bguest = db_session.query(Bguest).filter(
                            (Bguest.gastnr == res_line.gastnr)).first()

                    if bguest:
                        cl_list.comp_name = guest.name

                    arrangement = db_session.query(Arrangement).filter(
                            (Arrangement == res_line.arrangement)).first()

                    if arrangement:
                        cl_list.argt_code = arrangement.argt_bez

                    if res_line.code != "" and res_line.CODE.lower()  != "0":

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.code))).first()

                        if queasy:
                            cl_list.pay_type = queasy.char1


                    for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == "$CODE$":
                            cl_list.rate_code = substring(str, 6)
                            break


    return generate_output()