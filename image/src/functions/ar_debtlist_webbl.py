from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from models import Debitor, Artikel, Guest, Bill, Bediener, Waehrung, Res_line

def ar_debtlist_webbl(from_name:str, to_name:str, from_date:date, to_date:date, from_art:int, to_art:int, tot_flag:bool, lesspay:bool, show_inv:bool, case_type:int):
    d_rechnr = 0
    output_list_list = []
    edit_list_list = []
    debitor = artikel = guest = bill = bediener = waehrung = res_line = None

    output_list = edit_list = debt = None

    output_list_list, Output_list = create_model("Output_list", {"ar_recid":int, "info":str, "wabkurz":str, "maildate":date, "inv_no":str, "datum":date, "mflag":str, "bill_no":str, "rm_no":str, "receiver":str, "saldo":str, "fsaldo":str, "userinit":str, "vesrcod":str, "ref_no1":str, "ref_no2":str, "ci_date":date, "co_date":date, "nights":str, "verstat":int, "selected":bool, "ref_no3":int})
    edit_list_list, Edit_list = create_model("Edit_list", {"rechnr":int, "datum":date, "zinr":str, "billname":str, "lamt":decimal, "famt":decimal, "fcurr":str, "ar_recid":int, "amt_change":bool, "curr_change":bool, "curr_nr":int})

    Debt = Debitor

    db_session = local_storage.db_session

    def generate_output():
        nonlocal d_rechnr, output_list_list, edit_list_list, debitor, artikel, guest, bill, bediener, waehrung, res_line
        nonlocal debt


        nonlocal output_list, edit_list, debt
        nonlocal output_list_list, edit_list_list
        return {"d_rechnr": d_rechnr, "output-list": output_list_list, "edit-list": edit_list_list}

    def create_list():

        nonlocal d_rechnr, output_list_list, edit_list_list, debitor, artikel, guest, bill, bediener, waehrung, res_line
        nonlocal debt


        nonlocal output_list, edit_list, debt
        nonlocal output_list_list, edit_list_list

        artnr:int = 0
        t_debit:decimal = 0
        tot_debit:decimal = 0
        i:int = 0
        j:int = 0
        receiver:str = ""
        saldo:decimal = 0
        bill_str:str = ""
        curr_gastnr:int = 0
        tot_saldo:decimal = 0
        tf_saldo:decimal = 0
        tf_debit:decimal = 0
        ttf_debit:decimal = 0
        fsaldo:decimal = 0
        fcurr:str = ""
        resnr:int = 0
        Debt = Debitor
        output_list_list.clear()
        edit_list_list.clear()

        debitor_obj_list = []
        for debitor, artikel, guest in db_session.query(Debitor, Artikel, Guest).join(Artikel,(Artikel.artnr == Debitor.artnr) &  (Artikel.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr) &  (func.lower(Guest.name) >= (from_name).lower()) &  (func.lower(Guest.name) <= (to_name).lower())).filter(
                (Debitor.rgdatum >= from_date) &  (Debitor.rgdatum <= to_date) &  (Debitor.zahlkonto == 0) &  (Debitor.artnr >= from_art) &  (Debitor.artnr <= to_art)).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)

            if curr_gastnr == 0:
                curr_gastnr = debitor.gastnr

            if curr_gastnr != debitor.gastnr:
                curr_gastnr = debitor.gastnr

                if tot_saldo != 0 and tot_flag:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,29 + 1) :
                        output_list.receiver = output_list.receiver + " "
                    output_list.receiver = output_list.receiver + "Sub_Total"
                    output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                    output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo = 0
                    tf_saldo = 0
            saldo = debitor.saldo
            fsaldo = debitor.vesrdep

            if debitor.counter > 0 and lesspay:

                for debt in db_session.query(Debt).filter(
                        (Debt.counter == debitor.counter) &  (Debt.opart >= 1) &  (Debt.zahlkonto > 0) &  (Debt.rgdatum >= from_date) &  (Debt.rgdatum <= to_date)).all():
                    saldo = saldo + debt.saldo
                    fsaldo = fsaldo + debt.vesrdep


            if (saldo >= -0.05) and (saldo <= 0.05):
                saldo = 0

            if saldo != 0:

                if artnr != artikel.artnr:

                    if artnr != 0:
                        curr_gastnr = debitor.gastnr

                        if tot_saldo != 0 and tot_flag:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            for i in range(1,29 + 1) :
                                output_list.receiver = output_list.receiver + " "
                            output_list.receiver = output_list.receiver + "Sub_Total"
                            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                            tot_saldo = 0
                            tf_saldo = 0
                            output_list = Output_list()
                            output_list_list.append(output_list)

                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,29 + 1) :
                            output_list.receiver = output_list.receiver + " "

                        if tot_flag:
                            output_list.receiver = output_list.receiver + "T O T A L"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        else:
                            output_list.receiver = output_list.receiver + "Sub_Total"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_debit = 0
                        tf_debit = 0
                        tot_saldo = 0
                        tf_saldo = 0
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.receiver = to_string(artikel.artnr, ">>>>>9") + " - " + to_string(artikel.bezeich, "x(30)")
                    artnr = artikel.artnr
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.ref_no1 = to_string(guest.firmen_nr)
                output_list.ref_no2 = guest.steuernr
                output_list.ref_no3 = debitor.debref

                bill = db_session.query(Bill).filter(
                        (Bill.rechnr == debitor.rechnr)).first()

                if not bill:
                    d_rechnr = debitor.rechnr
                else:
                    output_list.inv_no = to_string(bill.rechnr2, ">>>>>>>>>")

                if debitor.verstat == 1:
                    bill_str = "M" + to_string(debitor.rechnr, ">>,>>>,>>9")
                else:
                    bill_str = to_string(debitor.rechnr, ">>>,>>>,>>9")
                output_list.datum = debitor.rgdatum
                output_list.mflag = substring(bill_str, 0, 1)
                output_list.bill_no = to_string(debitor.rechnr, ">>>,>>>,>>9")
                output_list.rm_no = debitor.zinr
                output_list.receiver = receiver
                output_list.saldo = to_string(saldo, "->,>>>,>>>,>>>,>>9.99")

                bediener = db_session.query(Bediener).filter(
                        (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.userinit = bediener.userinit
                else:
                    output_list.userinit = "  "
                output_list.fsaldo = to_string(fsaldo, "->,>>>,>>>,>>>,>>9.99")
                output_list.verstat = debitor.verstat
                for j in range(1,38 + 1) :

                    if substring(debitor.vesrcod, j - 1, 1) == chr(10):
                        output_list.vesrcod = " "
                    else:
                        output_list.vesrcod = output_list.vesrcod + substring(debitor.vesrcod, j - 1, 1)
                output_list.ar_recid = debitor._recid
                output_list.info = debitor.vesrcod

                if debitor.versanddat != None:
                    output_list.maildate = debitor.versanddat

                if debitor.betrieb_gastmem != 0:

                    waehrung = db_session.query(Waehrung).filter(
                            (Waehrungsnr == debitor.betrieb_gastmem)).first()

                    if waehrung:
                        output_list.wabkurz = waehrung.wabkurz

                if debitor.betriebsnr == 0:

                    bill = db_session.query(Bill).filter(
                            (Bill.rechnr == debitor.rechnr) &  (Bill.resnr > 0) &  (Bill.gastnr == debitor.gastnr)).first()

                    if bill:

                        if bill.reslinnr == 0:

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == bill.resnr) &  (Res_line.resstatus == 8)).first()

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                        else:

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.parent_nr)).first()

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                    else:

                        if debitor.vesrcod != " " and re.match(".*Deposit Payment.*",debitor.vesrcod):
                            resnr = to_int(entry(1, entry(0, debitor.vesrcod, ";") , ":"))

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == resnr)).first()

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                edit_list = Edit_list()
                edit_list_list.append(edit_list)

                edit_list.rechnr = debitor.rechnr
                edit_list.ar_recid = debitor._recid
                edit_list.datum = debitor.rgdatum
                edit_list.zinr = debitor.zinr
                edit_list.billname = receiver
                edit_list.famt = debitor.vesrdep
                edit_list.fcurr = output_list.wabkurz
                edit_list.curr_nr = debitor.betrieb_gastmem


                t_debit = t_debit + saldo
                tot_debit = tot_debit + saldo
                tot_saldo = tot_saldo + saldo
                tf_debit = tf_debit + fsaldo
                ttf_debit = ttf_debit + fsaldo
                tf_saldo = tf_saldo + fsaldo

        if tot_saldo != 0 and tot_flag:
            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,29 + 1) :
                output_list.receiver = output_list.receiver + " "
            output_list.receiver = output_list.receiver + "Sub_Total"
            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


            output_list = Output_list()
            output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,29 + 1) :
            output_list.receiver = output_list.receiver + " "

        if tot_flag:
            output_list.receiver = output_list.receiver + "T O T A L"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        else:
            output_list.receiver = output_list.receiver + "Sub_Total"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,27 + 1) :
            output_list.receiver = output_list.receiver + " "
        output_list.receiver = output_list.receiver + "Grand TOTAL"
        output_list.saldo = to_string(tot_debit, "->,>>>,>>>,>>>,>>9.99")
        output_list.fsaldo = to_string(ttf_debit, "->,>>>,>>>,>>>,>>9.99")

    def create_lista():

        nonlocal d_rechnr, output_list_list, edit_list_list, debitor, artikel, guest, bill, bediener, waehrung, res_line
        nonlocal debt


        nonlocal output_list, edit_list, debt
        nonlocal output_list_list, edit_list_list

        artnr:int = 0
        t_debit:decimal = 0
        tot_debit:decimal = 0
        i:int = 0
        j:int = 0
        receiver:str = ""
        saldo:decimal = 0
        bill_str:str = ""
        curr_gastnr:int = 0
        tot_saldo:decimal = 0
        tf_saldo:decimal = 0
        tf_debit:decimal = 0
        ttf_debit:decimal = 0
        fsaldo:decimal = 0
        resnr:int = 0
        Debt = Debitor
        output_list_list.clear()

        debitor_obj_list = []
        for debitor, artikel, guest in db_session.query(Debitor, Artikel, Guest).join(Artikel,(Artikel.artnr == Debitor.artnr) &  (Artikel.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr) &  (func.lower(Guest.name) >= (from_name).lower())).filter(
                (Debitor.rgdatum >= from_date) &  (Debitor.rgdatum <= to_date) &  (Debitor.zahlkonto == 0) &  (Debitor.artnr >= from_art) &  (Debitor.artnr <= to_art)).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)

            if curr_gastnr == 0:
                curr_gastnr = debitor.gastnr

            if curr_gastnr != debitor.gastnr:
                curr_gastnr = debitor.gastnr

                if tot_saldo != 0 and tot_flag:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,29 + 1) :
                        output_list.receiver = output_list.receiver + " "
                    output_list.receiver = output_list.receiver + "Sub_Total"
                    output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                    output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo = 0
                    tf_saldo = 0
            saldo = debitor.saldo
            fsaldo = debitor.vesrdep

            if debitor.counter > 0 and lesspay:

                for debt in db_session.query(Debt).filter(
                        (Debt.counter == debitor.counter) &  (Debt.opart >= 1) &  (Debt.zahlkonto > 0) &  (Debt.rgdatum >= from_date) &  (Debt.rgdatum <= to_date)).all():
                    saldo = saldo + debt.saldo
                    fsaldo = fsaldo + debt.vesrdep


            if (saldo >= -0.05) and (saldo <= 0.05):
                saldo = 0

            if saldo != 0:

                if artnr != artikel.artnr:

                    if artnr != 0:
                        curr_gastnr = debitor.gastnr

                        if tot_saldo != 0 and tot_flag:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            for i in range(1,29 + 1) :
                                output_list.receiver = output_list.receiver + " "
                            output_list.receiver = output_list.receiver + "Sub_Total"
                            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                            tot_saldo = 0
                            tf_saldo = 0
                            output_list = Output_list()
                            output_list_list.append(output_list)

                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,29 + 1) :
                            output_list.receiver = output_list.receiver + " "

                        if tot_flag:
                            output_list.receiver = output_list.receiver + "T O T A L"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        else:
                            output_list.receiver = output_list.receiver + "Sub_Total"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_debit = 0
                        tf_debit = 0
                        tot_saldo = 0
                        tf_saldo = 0
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.receiver = to_string(artikel.artnr, ">>>>>9") + " - " + to_string(artikel.bezeich, "x(30)")
                    artnr = artikel.artnr
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.ref_no1 = to_string(guest.firmen_nr)
                output_list.ref_no2 = guest.steuernr
                output_list.ref_no3 = debitor.debref

                bill = db_session.query(Bill).filter(
                        (Bill.rechnr == debitor.rechnr)).first()

                if not bill:
                    d_rechnr = debitor.rechnr
                else:
                    output_list.inv_no = to_string(bill.rechnr2, ">>>>>>>>>")

                if debitor.verstat == 1:
                    bill_str = "M" + to_string(debitor.rechnr, ">>,>>>,>>9")
                else:
                    bill_str = to_string(debitor.rechnr, ">>>,>>>,>>9")
                output_list.datum = debitor.rgdatum
                output_list.mflag = substring(bill_str, 0, 1)
                output_list.bill_no = to_string(debitor.rechnr, ">>>,>>>,>>9")
                output_list.rm_no = debitor.zinr
                output_list.receiver = receiver
                output_list.saldo = to_string(saldo, "->,>>>,>>>,>>>,>>9.99")

                bediener = db_session.query(Bediener).filter(
                        (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.userinit = bediener.userinit
                else:
                    output_list.userinit = "  "
                output_list.fsaldo = to_string(fsaldo, "->,>>>,>>>,>>>,>>9.99")
                output_list.verstat = debitor.verstat
                for j in range(1,38 + 1) :

                    if substring(debitor.vesrcod, j - 1, 1) == chr(10):
                        output_list.vesrcod = " "
                    else:
                        output_list.vesrcod = output_list.vesrcod + substring(debitor.vesrcod, j - 1, 1)
                output_list.ar_recid = debitor._recid
                output_list.info = debitor.vesrcod

                if debitor.versanddat != None:
                    output_list.maildate = debitor.versanddat

                if debitor.betrieb_gastmem != 0:

                    waehrung = db_session.query(Waehrung).filter(
                            (Waehrungsnr == debitor.betrieb_gastmem)).first()

                    if waehrung:
                        output_list.wabkurz = waehrung.wabkurz

                if debitor.betriebsnr == 0:

                    bill = db_session.query(Bill).filter(
                            (Bill.rechnr == debitor.rechnr) &  (Bill.resnr > 0) &  (Bill.gastnr == debitor.gastnr)).first()

                    if bill:

                        if bill.reslinnr == 0:

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == bill.resnr) &  (Res_line.resstatus == 8)).first()

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                        else:

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.parent_nr)).first()

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                    else:

                        if debitor.vesrcod != " " and re.match(".*Deposit Payment.*",debitor.vesrcod):
                            resnr = to_int(entry(1, entry(0, debitor.vesrcod, ";") , ":"))

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == resnr)).first()

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                edit_list = Edit_list()
                edit_list_list.append(edit_list)

                edit_list.rechnr = debitor.rechnr
                edit_list.ar_recid = debitor._recid
                edit_list.datum = debitor.rgdatum
                edit_list.zinr = debitor.zinr
                edit_list.billname = receiver
                edit_list.famt = debitor.vesrdep
                edit_list.fcurr = output_list.wabkurz
                edit_list.curr_nr = debitor.betrieb_gastmem


                t_debit = t_debit + saldo
                tot_debit = tot_debit + saldo
                tot_saldo = tot_saldo + saldo
                tf_debit = tf_debit + fsaldo
                ttf_debit = ttf_debit + fsaldo
                tf_saldo = tf_saldo + fsaldo

        if tot_saldo != 0 and tot_flag:
            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,29 + 1) :
                output_list.receiver = output_list.receiver + " "
            output_list.receiver = output_list.receiver + "Sub_Total"
            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


            output_list = Output_list()
            output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,29 + 1) :
            output_list.receiver = output_list.receiver + " "

        if tot_flag:
            output_list.receiver = output_list.receiver + "T O T A L"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        else:
            output_list.receiver = output_list.receiver + "Sub_Total"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,27 + 1) :
            output_list.receiver = output_list.receiver + " "
        output_list.receiver = output_list.receiver + "Grand TOTAL"
        output_list.saldo = to_string(tot_debit, "->,>>>,>>>,>>>,>>9.99")
        output_list.fsaldo = to_string(ttf_debit, "->,>>>,>>>,>>>,>>9.99")

    def create_list1():

        nonlocal d_rechnr, output_list_list, edit_list_list, debitor, artikel, guest, bill, bediener, waehrung, res_line
        nonlocal debt


        nonlocal output_list, edit_list, debt
        nonlocal output_list_list, edit_list_list

        artnr:int = 0
        t_debit:decimal = 0
        tot_debit:decimal = 0
        i:int = 0
        j:int = 0
        receiver:str = ""
        saldo:decimal = 0
        bill_str:str = ""
        curr_gastnr:int = 0
        tot_saldo:decimal = 0
        tf_saldo:decimal = 0
        tf_debit:decimal = 0
        ttf_debit:decimal = 0
        fsaldo:decimal = 0
        fcurr:str = ""
        resnr:int = 0
        Debt = Debitor
        output_list_list.clear()
        edit_list_list.clear()

        debitor_obj_list = []
        for debitor, artikel, guest in db_session.query(Debitor, Artikel, Guest).join(Artikel,(Artikel.artnr == Debitor.artnr) &  (Artikel.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr) &  (func.lower(Guest.name) >= (from_name).lower()) &  (func.lower(Guest.name) <= (to_name).lower())).filter(
                (Debitor.rgdatum >= from_date) &  (Debitor.rgdatum <= to_date) &  (Debitor.zahlkonto == 0) &  (Debitor.artnr >= from_art) &  (Debitor.artnr <= to_art) &  (Debitor.verstat == 9)).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)

            if curr_gastnr == 0:
                curr_gastnr = debitor.gastnr

            if curr_gastnr != debitor.gastnr:
                curr_gastnr = debitor.gastnr

                if tot_saldo != 0 and tot_flag:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,29 + 1) :
                        output_list.receiver = output_list.receiver + " "
                    output_list.receiver = output_list.receiver + "Sub_Total"
                    output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                    output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo = 0
                    tf_saldo = 0
            saldo = debitor.saldo
            fsaldo = debitor.vesrdep

            if debitor.counter > 0 and lesspay:

                for debt in db_session.query(Debt).filter(
                        (Debt.counter == debitor.counter) &  (Debt.opart >= 1) &  (Debt.zahlkonto > 0) &  (Debt.rgdatum >= from_date) &  (Debt.rgdatum <= to_date)).all():
                    saldo = saldo + debt.saldo
                    fsaldo = fsaldo + debt.vesrdep


            if (saldo >= -0.05) and (saldo <= 0.05):
                saldo = 0

            if saldo != 0:

                if artnr != artikel.artnr:

                    if artnr != 0:
                        curr_gastnr = debitor.gastnr

                        if tot_saldo != 0 and tot_flag:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            for i in range(1,29 + 1) :
                                output_list.receiver = output_list.receiver + " "
                            output_list.receiver = output_list.receiver + "Sub_Total"
                            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                            tot_saldo = 0
                            tf_saldo = 0
                            output_list = Output_list()
                            output_list_list.append(output_list)

                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,29 + 1) :
                            output_list.receiver = output_list.receiver + " "

                        if tot_flag:
                            output_list.receiver = output_list.receiver + "T O T A L"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        else:
                            output_list.receiver = output_list.receiver + "Sub_Total"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_debit = 0
                        tf_debit = 0
                        tot_saldo = 0
                        tf_saldo = 0
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.receiver = to_string(artikel.artnr, ">>>>>9") + " - " + to_string(artikel.bezeich, "x(30)")
                    artnr = artikel.artnr
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.ref_no1 = to_string(guest.firmen_nr)
                output_list.ref_no2 = guest.steuernr
                output_list.ref_no3 = debitor.debref

                bill = db_session.query(Bill).filter(
                        (Bill.rechnr == debitor.rechnr)).first()

                if not bill:
                    d_rechnr = debitor.rechnr
                else:
                    output_list.inv_no = to_string(bill.rechnr2, ">>>>>>>>>")

                if debitor.verstat == 1:
                    bill_str = "M" + to_string(debitor.rechnr, ">>,>>>,>>9")
                else:
                    bill_str = to_string(debitor.rechnr, ">>>,>>>,>>9")
                output_list.datum = debitor.rgdatum
                output_list.mflag = substring(bill_str, 0, 1)
                output_list.bill_no = to_string(debitor.rechnr, ">>>,>>>,>>9")
                output_list.rm_no = debitor.zinr
                output_list.receiver = receiver
                output_list.saldo = to_string(saldo, "->,>>>,>>>,>>>,>>9.99")

                bediener = db_session.query(Bediener).filter(
                        (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.userinit = bediener.userinit
                else:
                    output_list.userinit = "  "
                output_list.fsaldo = to_string(fsaldo, "->,>>>,>>>,>>>,>>9.99")
                output_list.verstat = debitor.verstat
                for j in range(1,38 + 1) :

                    if substring(debitor.vesrcod, j - 1, 1) == chr(10):
                        output_list.vesrcod = " "
                    else:
                        output_list.vesrcod = output_list.vesrcod + substring(debitor.vesrcod, j - 1, 1)
                output_list.ar_recid = debitor._recid
                output_list.info = debitor.vesrcod

                if debitor.versanddat != None:
                    output_list.maildate = debitor.versanddat

                if debitor.betrieb_gastmem != 0:

                    waehrung = db_session.query(Waehrung).filter(
                            (Waehrungsnr == debitor.betrieb_gastmem)).first()

                    if waehrung:
                        output_list.wabkurz = waehrung.wabkurz

                if debitor.betriebsnr == 0:

                    bill = db_session.query(Bill).filter(
                            (Bill.rechnr == debitor.rechnr) &  (Bill.resnr > 0) &  (Bill.gastnr == debitor.gastnr)).first()

                    if bill:

                        if bill.reslinnr == 0:

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == bill.resnr) &  (Res_line.resstatus == 8)).first()

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                        else:

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.parent_nr)).first()

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                    else:

                        if debitor.vesrcod != " " and re.match(".*Deposit Payment.*",debitor.vesrcod):
                            resnr = to_int(entry(1, entry(0, debitor.vesrcod, ";") , ":"))

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == resnr)).first()

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                edit_list = Edit_list()
                edit_list_list.append(edit_list)

                edit_list.rechnr = debitor.rechnr
                edit_list.ar_recid = debitor._recid
                edit_list.datum = debitor.rgdatum
                edit_list.zinr = debitor.zinr
                edit_list.billname = receiver
                edit_list.famt = debitor.vesrdep
                edit_list.fcurr = output_list.wabkurz
                edit_list.curr_nr = debitor.betrieb_gastmem


                t_debit = t_debit + saldo
                tot_debit = tot_debit + saldo
                tot_saldo = tot_saldo + saldo
                tf_debit = tf_debit + fsaldo
                ttf_debit = ttf_debit + fsaldo
                tf_saldo = tf_saldo + fsaldo

        if tot_saldo != 0 and tot_flag:
            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,29 + 1) :
                output_list.receiver = output_list.receiver + " "
            output_list.receiver = output_list.receiver + "Sub_Total"
            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


            output_list = Output_list()
            output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,29 + 1) :
            output_list.receiver = output_list.receiver + " "

        if tot_flag:
            output_list.receiver = output_list.receiver + "T O T A L"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        else:
            output_list.receiver = output_list.receiver + "Sub_Total"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,27 + 1) :
            output_list.receiver = output_list.receiver + " "
        output_list.receiver = output_list.receiver + "Grand TOTAL"
        output_list.saldo = to_string(tot_debit, "->,>>>,>>>,>>>,>>9.99")
        output_list.fsaldo = to_string(ttf_debit, "->,>>>,>>>,>>>,>>9.99")

    def create_list1a():

        nonlocal d_rechnr, output_list_list, edit_list_list, debitor, artikel, guest, bill, bediener, waehrung, res_line
        nonlocal debt


        nonlocal output_list, edit_list, debt
        nonlocal output_list_list, edit_list_list

        artnr:int = 0
        t_debit:decimal = 0
        tot_debit:decimal = 0
        i:int = 0
        j:int = 0
        receiver:str = ""
        saldo:decimal = 0
        bill_str:str = ""
        curr_gastnr:int = 0
        tot_saldo:decimal = 0
        tf_saldo:decimal = 0
        tf_debit:decimal = 0
        ttf_debit:decimal = 0
        fsaldo:decimal = 0
        resnr:int = 0
        Debt = Debitor
        output_list_list.clear()

        debitor_obj_list = []
        for debitor, artikel, guest in db_session.query(Debitor, Artikel, Guest).join(Artikel,(Artikel.artnr == Debitor.artnr) &  (Artikel.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr) &  (func.lower(Guest.name) >= (from_name).lower())).filter(
                (Debitor.rgdatum >= from_date) &  (Debitor.rgdatum <= to_date) &  (Debitor.zahlkonto == 0) &  (Debitor.artnr >= from_art) &  (Debitor.artnr <= to_art) &  (Debitor.verstat == 9)).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)

            if curr_gastnr == 0:
                curr_gastnr = debitor.gastnr

            if curr_gastnr != debitor.gastnr:
                curr_gastnr = debitor.gastnr

                if tot_saldo != 0 and tot_flag:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,29 + 1) :
                        output_list.receiver = output_list.receiver + " "
                    output_list.receiver = output_list.receiver + "Sub_Total"
                    output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                    output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo = 0
                    tf_saldo = 0
            saldo = debitor.saldo
            fsaldo = debitor.vesrdep

            if debitor.counter > 0 and lesspay:

                for debt in db_session.query(Debt).filter(
                        (Debt.counter == debitor.counter) &  (Debt.opart >= 1) &  (Debt.zahlkonto > 0) &  (Debt.rgdatum >= from_date) &  (Debt.rgdatum <= to_date)).all():
                    saldo = saldo + debt.saldo
                    fsaldo = fsaldo + debt.vesrdep


            if (saldo >= -0.05) and (saldo <= 0.05):
                saldo = 0

            if saldo != 0:

                if artnr != artikel.artnr:

                    if artnr != 0:
                        curr_gastnr = debitor.gastnr

                        if tot_saldo != 0 and tot_flag:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            for i in range(1,29 + 1) :
                                output_list.receiver = output_list.receiver + " "
                            output_list.receiver = output_list.receiver + "Sub_Total"
                            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                            tot_saldo = 0
                            tf_saldo = 0
                            output_list = Output_list()
                            output_list_list.append(output_list)

                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,29 + 1) :
                            output_list.receiver = output_list.receiver + " "

                        if tot_flag:
                            output_list.receiver = output_list.receiver + "T O T A L"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        else:
                            output_list.receiver = output_list.receiver + "Sub_Total"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_debit = 0
                        tf_debit = 0
                        tot_saldo = 0
                        tf_saldo = 0
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.receiver = to_string(artikel.artnr, ">>>>>9") + " - " + to_string(artikel.bezeich, "x(30)")
                    artnr = artikel.artnr
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.ref_no1 = to_string(guest.firmen_nr)
                output_list.ref_no2 = guest.steuernr
                output_list.ref_no3 = debitor.debref

                bill = db_session.query(Bill).filter(
                        (Bill.rechnr == debitor.rechnr)).first()

                if not bill:
                    d_rechnr = debitor.rechnr
                else:
                    output_list.inv_no = to_string(bill.rechnr2, ">>>>>>>>>")

                if debitor.verstat == 1:
                    bill_str = "M" + to_string(debitor.rechnr, ">>,>>>,>>9")
                else:
                    bill_str = to_string(debitor.rechnr, ">>>,>>>,>>9")
                output_list.datum = debitor.rgdatum
                output_list.mflag = substring(bill_str, 0, 1)
                output_list.bill_no = to_string(debitor.rechnr, ">>>,>>>,>>9")
                output_list.rm_no = debitor.zinr
                output_list.receiver = receiver
                output_list.saldo = to_string(saldo, "->,>>>,>>>,>>>,>>9.99")

                bediener = db_session.query(Bediener).filter(
                        (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.userinit = bediener.userinit
                else:
                    output_list.userinit = "  "
                output_list.fsaldo = to_string(fsaldo, "->,>>>,>>>,>>>,>>9.99")
                output_list.verstat = debitor.verstat
                for j in range(1,38 + 1) :

                    if substring(debitor.vesrcod, j - 1, 1) == chr(10):
                        output_list.vesrcod = " "
                    else:
                        output_list.vesrcod = output_list.vesrcod + substring(debitor.vesrcod, j - 1, 1)
                output_list.ar_recid = debitor._recid
                output_list.info = debitor.vesrcod

                if debitor.versanddat != None:
                    output_list.maildate = debitor.versanddat

                if debitor.betrieb_gastmem != 0:

                    waehrung = db_session.query(Waehrung).filter(
                            (Waehrungsnr == debitor.betrieb_gastmem)).first()

                    if waehrung:
                        output_list.wabkurz = waehrung.wabkurz

                if debitor.betriebsnr == 0:

                    bill = db_session.query(Bill).filter(
                            (Bill.rechnr == debitor.rechnr) &  (Bill.resnr > 0) &  (Bill.gastnr == debitor.gastnr)).first()

                    if bill:

                        if bill.reslinnr == 0:

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == bill.resnr) &  (Res_line.resstatus == 8)).first()

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                        else:

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.parent_nr)).first()

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                    else:

                        if debitor.vesrcod != " " and re.match(".*Deposit Payment.*",debitor.vesrcod):
                            resnr = to_int(entry(1, entry(0, debitor.vesrcod, ";") , ":"))

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == resnr)).first()

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                edit_list = Edit_list()
                edit_list_list.append(edit_list)

                edit_list.rechnr = debitor.rechnr
                edit_list.ar_recid = debitor._recid
                edit_list.datum = debitor.rgdatum
                edit_list.zinr = debitor.zinr
                edit_list.billname = receiver
                edit_list.famt = debitor.vesrdep
                edit_list.fcurr = output_list.wabkurz
                edit_list.curr_nr = debitor.betrieb_gastmem


                t_debit = t_debit + saldo
                tot_debit = tot_debit + saldo
                tot_saldo = tot_saldo + saldo
                tf_debit = tf_debit + fsaldo
                ttf_debit = ttf_debit + fsaldo
                tf_saldo = tf_saldo + fsaldo

        if tot_saldo != 0 and tot_flag:
            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,29 + 1) :
                output_list.receiver = output_list.receiver + " "
            output_list.receiver = output_list.receiver + "Sub_Total"
            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


            output_list = Output_list()
            output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,29 + 1) :
            output_list.receiver = output_list.receiver + " "

        if tot_flag:
            output_list.receiver = output_list.receiver + "T O T A L"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        else:
            output_list.receiver = output_list.receiver + "Sub_Total"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,27 + 1) :
            output_list.receiver = output_list.receiver + " "
        output_list.receiver = output_list.receiver + "Grand TOTAL"
        output_list.saldo = to_string(tot_debit, "->,>>>,>>>,>>>,>>9.99")
        output_list.fsaldo = to_string(ttf_debit, "->,>>>,>>>,>>>,>>9.99")

    def create_list2():

        nonlocal d_rechnr, output_list_list, edit_list_list, debitor, artikel, guest, bill, bediener, waehrung, res_line
        nonlocal debt


        nonlocal output_list, edit_list, debt
        nonlocal output_list_list, edit_list_list

        artnr:int = 0
        t_debit:decimal = 0
        tot_debit:decimal = 0
        i:int = 0
        j:int = 0
        receiver:str = ""
        saldo:decimal = 0
        bill_str:str = ""
        curr_gastnr:int = 0
        tot_saldo:decimal = 0
        tf_saldo:decimal = 0
        tf_debit:decimal = 0
        ttf_debit:decimal = 0
        fsaldo:decimal = 0
        fcurr:str = ""
        resnr:int = 0
        Debt = Debitor
        output_list_list.clear()
        edit_list_list.clear()

        debitor_obj_list = []
        for debitor, artikel, guest in db_session.query(Debitor, Artikel, Guest).join(Artikel,(Artikel.artnr == Debitor.artnr) &  (Artikel.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr) &  (func.lower(Guest.name) >= (from_name).lower()) &  (func.lower(Guest.name) <= (to_name).lower())).filter(
                (Debitor.rgdatum >= from_date) &  (Debitor.rgdatum <= to_date) &  (Debitor.zahlkonto == 0) &  (Debitor.artnr >= from_art) &  (Debitor.artnr <= to_art) &  (Debitor.verstat != 9)).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)

            if curr_gastnr == 0:
                curr_gastnr = debitor.gastnr

            if curr_gastnr != debitor.gastnr:
                curr_gastnr = debitor.gastnr

                if tot_saldo != 0 and tot_flag:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,29 + 1) :
                        output_list.receiver = output_list.receiver + " "
                    output_list.receiver = output_list.receiver + "Sub_Total"
                    output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                    output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo = 0
                    tf_saldo = 0
            saldo = debitor.saldo
            fsaldo = debitor.vesrdep

            if debitor.counter > 0 and lesspay:

                for debt in db_session.query(Debt).filter(
                        (Debt.counter == debitor.counter) &  (Debt.opart >= 1) &  (Debt.zahlkonto > 0) &  (Debt.rgdatum >= from_date) &  (Debt.rgdatum <= to_date)).all():
                    saldo = saldo + debt.saldo
                    fsaldo = fsaldo + debt.vesrdep


            if (saldo >= -0.05) and (saldo <= 0.05):
                saldo = 0

            if saldo != 0:

                if artnr != artikel.artnr:

                    if artnr != 0:
                        curr_gastnr = debitor.gastnr

                        if tot_saldo != 0 and tot_flag:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            for i in range(1,29 + 1) :
                                output_list.receiver = output_list.receiver + " "
                            output_list.receiver = output_list.receiver + "Sub_Total"
                            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                            tot_saldo = 0
                            tf_saldo = 0
                            output_list = Output_list()
                            output_list_list.append(output_list)

                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,29 + 1) :
                            output_list.receiver = output_list.receiver + " "

                        if tot_flag:
                            output_list.receiver = output_list.receiver + "T O T A L"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        else:
                            output_list.receiver = output_list.receiver + "Sub_Total"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_debit = 0
                        tf_debit = 0
                        tot_saldo = 0
                        tf_saldo = 0
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.receiver = to_string(artikel.artnr, ">>>>>9") + " - " + to_string(artikel.bezeich, "x(30)")
                    artnr = artikel.artnr
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.ref_no1 = to_string(guest.firmen_nr)
                output_list.ref_no2 = guest.steuernr
                output_list.ref_no3 = debitor.debref

                bill = db_session.query(Bill).filter(
                        (Bill.rechnr == debitor.rechnr)).first()

                if not bill:
                    d_rechnr = debitor.rechnr
                else:
                    output_list.inv_no = to_string(bill.rechnr2, ">>>>>>>>>")

                if debitor.verstat == 1:
                    bill_str = "M" + to_string(debitor.rechnr, ">>,>>>,>>9")
                else:
                    bill_str = to_string(debitor.rechnr, ">>>,>>>,>>9")
                output_list.datum = debitor.rgdatum
                output_list.mflag = substring(bill_str, 0, 1)
                output_list.bill_no = to_string(debitor.rechnr, ">>>,>>>,>>9")
                output_list.rm_no = debitor.zinr
                output_list.receiver = receiver
                output_list.saldo = to_string(saldo, "->,>>>,>>>,>>>,>>9.99")

                bediener = db_session.query(Bediener).filter(
                        (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.userinit = bediener.userinit
                else:
                    output_list.userinit = "  "
                output_list.fsaldo = to_string(fsaldo, "->,>>>,>>>,>>>,>>9.99")
                output_list.verstat = debitor.verstat
                for j in range(1,38 + 1) :

                    if substring(debitor.vesrcod, j - 1, 1) == chr(10):
                        output_list.vesrcod = " "
                    else:
                        output_list.vesrcod = output_list.vesrcod + substring(debitor.vesrcod, j - 1, 1)
                output_list.ar_recid = debitor._recid
                output_list.info = debitor.vesrcod

                if debitor.versanddat != None:
                    output_list.maildate = debitor.versanddat

                if debitor.betrieb_gastmem != 0:

                    waehrung = db_session.query(Waehrung).filter(
                            (Waehrungsnr == debitor.betrieb_gastmem)).first()

                    if waehrung:
                        output_list.wabkurz = waehrung.wabkurz

                if debitor.betriebsnr == 0:

                    bill = db_session.query(Bill).filter(
                            (Bill.rechnr == debitor.rechnr) &  (Bill.resnr > 0) &  (Bill.gastnr == debitor.gastnr)).first()

                    if bill:

                        if bill.reslinnr == 0:

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == bill.resnr) &  (Res_line.resstatus == 8)).first()

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                        else:

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.parent_nr)).first()

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                    else:

                        if debitor.vesrcod != " " and re.match(".*Deposit Payment.*",debitor.vesrcod):
                            resnr = to_int(entry(1, entry(0, debitor.vesrcod, ";") , ":"))

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == resnr)).first()

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                edit_list = Edit_list()
                edit_list_list.append(edit_list)

                edit_list.rechnr = debitor.rechnr
                edit_list.ar_recid = debitor._recid
                edit_list.datum = debitor.rgdatum
                edit_list.zinr = debitor.zinr
                edit_list.billname = receiver
                edit_list.famt = debitor.vesrdep
                edit_list.fcurr = output_list.wabkurz
                edit_list.curr_nr = debitor.betrieb_gastmem


                t_debit = t_debit + saldo
                tot_debit = tot_debit + saldo
                tot_saldo = tot_saldo + saldo
                tf_debit = tf_debit + fsaldo
                ttf_debit = ttf_debit + fsaldo
                tf_saldo = tf_saldo + fsaldo

        if tot_saldo != 0 and tot_flag:
            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,29 + 1) :
                output_list.receiver = output_list.receiver + " "
            output_list.receiver = output_list.receiver + "Sub_Total"
            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


            output_list = Output_list()
            output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,29 + 1) :
            output_list.receiver = output_list.receiver + " "

        if tot_flag:
            output_list.receiver = output_list.receiver + "T O T A L"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        else:
            output_list.receiver = output_list.receiver + "Sub_Total"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,27 + 1) :
            output_list.receiver = output_list.receiver + " "
        output_list.receiver = output_list.receiver + "Grand TOTAL"
        output_list.saldo = to_string(tot_debit, "->,>>>,>>>,>>>,>>9.99")
        output_list.fsaldo = to_string(ttf_debit, "->,>>>,>>>,>>>,>>9.99")

    def create_list2a():

        nonlocal d_rechnr, output_list_list, edit_list_list, debitor, artikel, guest, bill, bediener, waehrung, res_line
        nonlocal debt


        nonlocal output_list, edit_list, debt
        nonlocal output_list_list, edit_list_list

        artnr:int = 0
        t_debit:decimal = 0
        tot_debit:decimal = 0
        i:int = 0
        j:int = 0
        receiver:str = ""
        saldo:decimal = 0
        bill_str:str = ""
        curr_gastnr:int = 0
        tot_saldo:decimal = 0
        tf_saldo:decimal = 0
        tf_debit:decimal = 0
        ttf_debit:decimal = 0
        fsaldo:decimal = 0
        resnr:int = 0
        Debt = Debitor
        output_list_list.clear()

        debitor_obj_list = []
        for debitor, artikel, guest in db_session.query(Debitor, Artikel, Guest).join(Artikel,(Artikel.artnr == Debitor.artnr) &  (Artikel.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr) &  (func.lower(Guest.name) >= (from_name).lower())).filter(
                (Debitor.rgdatum >= from_date) &  (Debitor.rgdatum <= to_date) &  (Debitor.zahlkonto == 0) &  (Debitor.artnr >= from_art) &  (Debitor.artnr <= to_art) &  (Debitor.verstat != 9)).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)

            if curr_gastnr == 0:
                curr_gastnr = debitor.gastnr

            if curr_gastnr != debitor.gastnr:
                curr_gastnr = debitor.gastnr

                if tot_saldo != 0 and tot_flag:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,29 + 1) :
                        output_list.receiver = output_list.receiver + " "
                    output_list.receiver = output_list.receiver + "Sub_Total"
                    output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                    output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo = 0
                    tf_saldo = 0
            saldo = debitor.saldo
            fsaldo = debitor.vesrdep

            if debitor.counter > 0 and lesspay:

                for debt in db_session.query(Debt).filter(
                        (Debt.counter == debitor.counter) &  (Debt.opart >= 1) &  (Debt.zahlkonto > 0) &  (Debt.rgdatum >= from_date) &  (Debt.rgdatum <= to_date)).all():
                    saldo = saldo + debt.saldo
                    fsaldo = fsaldo + debt.vesrdep


            if (saldo >= -0.05) and (saldo <= 0.05):
                saldo = 0

            if saldo != 0:

                if artnr != artikel.artnr:

                    if artnr != 0:
                        curr_gastnr = debitor.gastnr

                        if tot_saldo != 0 and tot_flag:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            for i in range(1,29 + 1) :
                                output_list.receiver = output_list.receiver + " "
                            output_list.receiver = output_list.receiver + "Sub_Total"
                            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                            tot_saldo = 0
                            tf_saldo = 0
                            output_list = Output_list()
                            output_list_list.append(output_list)

                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,29 + 1) :
                            output_list.receiver = output_list.receiver + " "

                        if tot_flag:
                            output_list.receiver = output_list.receiver + "T O T A L"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        else:
                            output_list.receiver = output_list.receiver + "Sub_Total"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_debit = 0
                        tf_debit = 0
                        tot_saldo = 0
                        tf_saldo = 0
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.receiver = to_string(artikel.artnr, ">>>>>9") + " - " + to_string(artikel.bezeich, "x(30)")
                    artnr = artikel.artnr
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.ref_no1 = to_string(guest.firmen_nr)
                output_list.ref_no2 = guest.steuernr
                output_list.ref_no3 = debitor.debref

                bill = db_session.query(Bill).filter(
                        (Bill.rechnr == debitor.rechnr)).first()

                if not bill:
                    d_rechnr = debitor.rechnr
                else:
                    output_list.inv_no = to_string(bill.rechnr2, ">>>>>>>>>")

                if debitor.verstat == 1:
                    bill_str = "M" + to_string(debitor.rechnr, ">>,>>>,>>9")
                else:
                    bill_str = to_string(debitor.rechnr, ">>>,>>>,>>9")
                output_list.datum = debitor.rgdatum
                output_list.mflag = substring(bill_str, 0, 1)
                output_list.bill_no = to_string(debitor.rechnr, ">>>,>>>,>>9")
                output_list.rm_no = debitor.zinr
                output_list.receiver = receiver
                output_list.saldo = to_string(saldo, "->,>>>,>>>,>>>,>>9.99")

                bediener = db_session.query(Bediener).filter(
                        (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.userinit = bediener.userinit
                else:
                    output_list.userinit = "  "
                output_list.fsaldo = to_string(fsaldo, "->,>>>,>>>,>>>,>>9.99")
                output_list.verstat = debitor.verstat
                for j in range(1,38 + 1) :

                    if substring(debitor.vesrcod, j - 1, 1) == chr(10):
                        output_list.vesrcod = " "
                    else:
                        output_list.vesrcod = output_list.vesrcod + substring(debitor.vesrcod, j - 1, 1)
                output_list.ar_recid = debitor._recid
                output_list.info = debitor.vesrcod

                if debitor.versanddat != None:
                    output_list.maildate = debitor.versanddat

                if debitor.betrieb_gastmem != 0:

                    waehrung = db_session.query(Waehrung).filter(
                            (Waehrungsnr == debitor.betrieb_gastmem)).first()

                    if waehrung:
                        output_list.wabkurz = waehrung.wabkurz

                if debitor.betriebsnr == 0:

                    bill = db_session.query(Bill).filter(
                            (Bill.rechnr == debitor.rechnr) &  (Bill.resnr > 0) &  (Bill.gastnr == debitor.gastnr)).first()

                    if bill:

                        if bill.reslinnr == 0:

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == bill.resnr) &  (Res_line.resstatus == 8)).first()

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                        else:

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.parent_nr)).first()

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                    else:

                        if debitor.vesrcod != " " and re.match(".*Deposit Payment.*",debitor.vesrcod):
                            resnr = to_int(entry(1, entry(0, debitor.vesrcod, ";") , ":"))

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == resnr)).first()

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                edit_list = Edit_list()
                edit_list_list.append(edit_list)

                edit_list.rechnr = debitor.rechnr
                edit_list.ar_recid = debitor._recid
                edit_list.datum = debitor.rgdatum
                edit_list.zinr = debitor.zinr
                edit_list.billname = receiver
                edit_list.famt = debitor.vesrdep
                edit_list.fcurr = output_list.wabkurz
                edit_list.curr_nr = debitor.betrieb_gastmem


                t_debit = t_debit + saldo
                tot_debit = tot_debit + saldo
                tot_saldo = tot_saldo + saldo
                tf_debit = tf_debit + fsaldo
                ttf_debit = ttf_debit + fsaldo
                tf_saldo = tf_saldo + fsaldo

        if tot_saldo != 0 and tot_flag:
            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,29 + 1) :
                output_list.receiver = output_list.receiver + " "
            output_list.receiver = output_list.receiver + "Sub_Total"
            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


            output_list = Output_list()
            output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,29 + 1) :
            output_list.receiver = output_list.receiver + " "

        if tot_flag:
            output_list.receiver = output_list.receiver + "T O T A L"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        else:
            output_list.receiver = output_list.receiver + "Sub_Total"
            output_list.saldo = STRING (t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = STRING (tf_debit, "->,>>>,>>>,>>>,>>9.99")


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,27 + 1) :
            output_list.receiver = output_list.receiver + " "
        output_list.receiver = output_list.receiver + "Grand TOTAL"
        output_list.saldo = to_string(tot_debit, "->,>>>,>>>,>>>,>>9.99")
        output_list.fsaldo = to_string(ttf_debit, "->,>>>,>>>,>>>,>>9.99")


    if case_type == 0:

        if substring(to_name, 0, 2) == "zz":
            create_lista()
        else:
            create_list()
    elif case_type == 1:

        if substring(to_name, 0, 2) == "zz":
            create_list1a()
        else:
            create_list1()
    elif case_type == 2:

        if substring(to_name, 0, 2) == "zz":
            create_list2a()
        else:
            create_list2()

    return generate_output()