#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Debitor, Artikel, Guest, Bill, Bediener, Waehrung, Res_line

def ar_debtlist_webbl(from_name:string, to_name:string, from_date:date, to_date:date, from_art:int, to_art:int, tot_flag:bool, lesspay:bool, show_inv:bool, case_type:int):

    prepare_cache ([Debitor, Artikel, Guest, Bill, Bediener, Waehrung, Res_line])

    d_rechnr = 0
    output_list_data = []
    edit_list_data = []
    debitor = artikel = guest = bill = bediener = waehrung = res_line = None

    output_list = edit_list = None

    output_list_data, Output_list = create_model("Output_list", {"ar_recid":int, "info":string, "wabkurz":string, "maildate":date, "inv_no":string, "datum":date, "mflag":string, "bill_no":string, "rm_no":string, "receiver":string, "saldo":string, "fsaldo":string, "userinit":string, "vesrcod":string, "ref_no1":string, "ref_no2":string, "ci_date":date, "co_date":date, "nights":string, "verstat":int, "selected":bool, "ref_no3":int})
    edit_list_data, Edit_list = create_model("Edit_list", {"rechnr":int, "datum":date, "zinr":string, "billname":string, "lamt":Decimal, "famt":Decimal, "fcurr":string, "ar_recid":int, "amt_change":bool, "curr_change":bool, "curr_nr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal d_rechnr, output_list_data, edit_list_data, debitor, artikel, guest, bill, bediener, waehrung, res_line
        nonlocal from_name, to_name, from_date, to_date, from_art, to_art, tot_flag, lesspay, show_inv, case_type


        nonlocal output_list, edit_list
        nonlocal output_list_data, edit_list_data

        return {"d_rechnr": d_rechnr, "output-list": output_list_data, "edit-list": edit_list_data}

    def create_list():

        nonlocal d_rechnr, output_list_data, edit_list_data, debitor, artikel, guest, bill, bediener, waehrung, res_line
        nonlocal from_name, to_name, from_date, to_date, from_art, to_art, tot_flag, lesspay, show_inv, case_type


        nonlocal output_list, edit_list
        nonlocal output_list_data, edit_list_data

        artnr:int = 0
        t_debit:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        i:int = 0
        j:int = 0
        receiver:string = ""
        saldo:Decimal = to_decimal("0.0")
        bill_str:string = ""
        debt = None
        curr_gastnr:int = 0
        tot_saldo:Decimal = to_decimal("0.0")
        tf_saldo:Decimal = to_decimal("0.0")
        tf_debit:Decimal = to_decimal("0.0")
        ttf_debit:Decimal = to_decimal("0.0")
        fsaldo:Decimal = to_decimal("0.0")
        fcurr:string = ""
        resnr:int = 0
        Debt =  create_buffer("Debt",Debitor)
        output_list_data.clear()
        edit_list_data.clear()

        debitor_obj_list = {}
        debitor = Debitor()
        artikel = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.vesrdep, debitor.counter, debitor.debref, debitor.rechnr, debitor.rgdatum, debitor.zinr, debitor.bediener_nr, debitor.verstat, debitor.vesrcod, debitor._recid, debitor.versanddat, debitor.betrieb_gastmem, debitor.betriebsnr, artikel.artnr, artikel.bezeich, artikel._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest.firmen_nr, guest.steuernr, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.vesrdep, Debitor.counter, Debitor.debref, Debitor.rechnr, Debitor.rgdatum, Debitor.zinr, Debitor.bediener_nr, Debitor.verstat, Debitor.vesrcod, Debitor._recid, Debitor.versanddat, Debitor.betrieb_gastmem, Debitor.betriebsnr, Artikel.artnr, Artikel.bezeich, Artikel._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest.firmen_nr, Guest.steuernr, Guest._recid).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr) & (Guest.name >= (from_name).lower()) & (Guest.name <= (to_name).lower())).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto == 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            if curr_gastnr == 0:
                curr_gastnr = debitor.gastnr

            if curr_gastnr != debitor.gastnr:
                curr_gastnr = debitor.gastnr

                if tot_saldo != 0 and tot_flag:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1,29 + 1) :
                        output_list.receiver = output_list.receiver + " "
                    output_list.receiver = output_list.receiver + "Sub-Total"
                    output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                    output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tf_saldo =  to_decimal("0")
            saldo =  to_decimal(debitor.saldo)
            fsaldo =  to_decimal(debitor.vesrdep)

            if debitor.counter > 0 and lesspay:

                for debt in db_session.query(Debt).filter(
                         (Debt.counter == debitor.counter) & (Debt.opart >= 1) & (Debt.zahlkonto > 0)).order_by(Debt._recid).all():
                    saldo =  to_decimal(saldo) + to_decimal(debt.saldo)
                    fsaldo =  to_decimal(fsaldo) + to_decimal(debt.vesrdep)


            if (saldo >= -0.05) and (saldo <= 0.05):
                saldo =  to_decimal("0")

            if saldo != 0:

                if artnr != artikel.artnr:

                    if artnr != 0:
                        curr_gastnr = debitor.gastnr

                        if tot_saldo != 0 and tot_flag:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            for i in range(1,29 + 1) :
                                output_list.receiver = output_list.receiver + " "
                            output_list.receiver = output_list.receiver + "Sub-Total"
                            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                            tot_saldo =  to_decimal("0")
                            tf_saldo =  to_decimal("0")
                            output_list = Output_list()
                            output_list_data.append(output_list)

                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1,29 + 1) :
                            output_list.receiver = output_list.receiver + " "

                        if tot_flag:
                            output_list.receiver = output_list.receiver + "T O T A L"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        else:
                            output_list.receiver = output_list.receiver + "Sub-Total"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_debit =  to_decimal("0")
                        tf_debit =  to_decimal("0")
                        tot_saldo =  to_decimal("0")
                        tf_saldo =  to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.receiver = to_string(artikel.artnr, ">>>>>9") + " - " + to_string(artikel.bezeich, "x(30)")
                    artnr = artikel.artnr
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.ref_no1 = to_string(guest.firmen_nr)
                output_list.ref_no2 = guest.steuernr
                output_list.ref_no3 = debitor.debref

                bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)]})

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

                bediener = get_cache (Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.userinit = bediener.userinit
                else:
                    output_list.userinit = " "
                output_list.fsaldo = to_string(fsaldo, "->,>>>,>>>,>>>,>>9.99")
                output_list.verstat = debitor.verstat
                for j in range(1,38 + 1) :

                    if substring(debitor.vesrcod, j - 1, 1) == chr_unicode(10):
                        output_list.vesrcod = " "
                    else:
                        output_list.vesrcod = output_list.vesrcod + substring(debitor.vesrcod, j - 1, 1)
                output_list.ar_recid = debitor._recid
                output_list.info = debitor.vesrcod

                if debitor.versanddat != None:
                    output_list.maildate = debitor.versanddat

                if debitor.betrieb_gastmem != 0:

                    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                    if waehrung:
                        output_list.wabkurz = waehrung.wabkurz

                if debitor.betriebsnr == 0:

                    bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)],"resnr": [(gt, 0)],"gastnr": [(eq, debitor.gastnr)]})

                    if bill:

                        if bill.reslinnr == 0:

                            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"resstatus": [(eq, 8)]})

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                        else:

                            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                    else:

                        if debitor.vesrcod != " " and matches(debitor.vesrcod,r"*Deposit Payment*"):
                            resnr = to_int(entry(1, entry(0, debitor.vesrcod, ";") , ":"))

                            res_line = get_cache (Res_line, {"resnr": [(eq, resnr)]})

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                edit_list = Edit_list()
                edit_list_data.append(edit_list)

                edit_list.rechnr = debitor.rechnr
                edit_list.ar_recid = debitor._recid
                edit_list.datum = debitor.rgdatum
                edit_list.zinr = debitor.zinr
                edit_list.billname = receiver
                edit_list.famt =  to_decimal(debitor.vesrdep)
                edit_list.fcurr = output_list.wabkurz
                edit_list.curr_nr = debitor.betrieb_gastmem


                t_debit =  to_decimal(t_debit) + to_decimal(saldo)
                tot_debit =  to_decimal(tot_debit) + to_decimal(saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(saldo)
                tf_debit =  to_decimal(tf_debit) + to_decimal(fsaldo)
                ttf_debit =  to_decimal(ttf_debit) + to_decimal(fsaldo)
                tf_saldo =  to_decimal(tf_saldo) + to_decimal(fsaldo)

        if tot_saldo != 0 and tot_flag:
            output_list = Output_list()
            output_list_data.append(output_list)

            for i in range(1,29 + 1) :
                output_list.receiver = output_list.receiver + " "
            output_list.receiver = output_list.receiver + "Sub-Total"
            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


            output_list = Output_list()
            output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1,29 + 1) :
            output_list.receiver = output_list.receiver + " "

        if tot_flag:
            output_list.receiver = output_list.receiver + "T O T A L"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        else:
            output_list.receiver = output_list.receiver + "Sub-Total"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1,27 + 1) :
            output_list.receiver = output_list.receiver + " "
        output_list.receiver = output_list.receiver + "Grand TOTAL"
        output_list.saldo = to_string(tot_debit, "->,>>>,>>>,>>>,>>9.99")
        output_list.fsaldo = to_string(ttf_debit, "->,>>>,>>>,>>>,>>9.99")


    def create_lista():

        nonlocal d_rechnr, output_list_data, edit_list_data, debitor, artikel, guest, bill, bediener, waehrung, res_line
        nonlocal from_name, to_name, from_date, to_date, from_art, to_art, tot_flag, lesspay, show_inv, case_type


        nonlocal output_list, edit_list
        nonlocal output_list_data, edit_list_data

        artnr:int = 0
        t_debit:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        i:int = 0
        j:int = 0
        receiver:string = ""
        saldo:Decimal = to_decimal("0.0")
        bill_str:string = ""
        debt = None
        curr_gastnr:int = 0
        tot_saldo:Decimal = to_decimal("0.0")
        tf_saldo:Decimal = to_decimal("0.0")
        tf_debit:Decimal = to_decimal("0.0")
        ttf_debit:Decimal = to_decimal("0.0")
        fsaldo:Decimal = to_decimal("0.0")
        resnr:int = 0
        Debt =  create_buffer("Debt",Debitor)
        output_list_data.clear()

        debitor_obj_list = {}
        debitor = Debitor()
        artikel = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.vesrdep, debitor.counter, debitor.debref, debitor.rechnr, debitor.rgdatum, debitor.zinr, debitor.bediener_nr, debitor.verstat, debitor.vesrcod, debitor._recid, debitor.versanddat, debitor.betrieb_gastmem, debitor.betriebsnr, artikel.artnr, artikel.bezeich, artikel._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest.firmen_nr, guest.steuernr, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.vesrdep, Debitor.counter, Debitor.debref, Debitor.rechnr, Debitor.rgdatum, Debitor.zinr, Debitor.bediener_nr, Debitor.verstat, Debitor.vesrcod, Debitor._recid, Debitor.versanddat, Debitor.betrieb_gastmem, Debitor.betriebsnr, Artikel.artnr, Artikel.bezeich, Artikel._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest.firmen_nr, Guest.steuernr, Guest._recid).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr) & (Guest.name >= (from_name).lower())).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto == 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            if curr_gastnr == 0:
                curr_gastnr = debitor.gastnr

            if curr_gastnr != debitor.gastnr:
                curr_gastnr = debitor.gastnr

                if tot_saldo != 0 and tot_flag:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1,29 + 1) :
                        output_list.receiver = output_list.receiver + " "
                    output_list.receiver = output_list.receiver + "Sub-Total"
                    output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                    output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tf_saldo =  to_decimal("0")
            saldo =  to_decimal(debitor.saldo)
            fsaldo =  to_decimal(debitor.vesrdep)

            if debitor.counter > 0 and lesspay:

                for debt in db_session.query(Debt).filter(
                         (Debt.counter == debitor.counter) & (Debt.opart >= 1) & (Debt.zahlkonto > 0)).order_by(Debt._recid).all():
                    saldo =  to_decimal(saldo) + to_decimal(debt.saldo)
                    fsaldo =  to_decimal(fsaldo) + to_decimal(debt.vesrdep)


            if (saldo >= -0.05) and (saldo <= 0.05):
                saldo =  to_decimal("0")

            if saldo != 0:

                if artnr != artikel.artnr:

                    if artnr != 0:
                        curr_gastnr = debitor.gastnr

                        if tot_saldo != 0 and tot_flag:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            for i in range(1,29 + 1) :
                                output_list.receiver = output_list.receiver + " "
                            output_list.receiver = output_list.receiver + "Sub-Total"
                            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                            tot_saldo =  to_decimal("0")
                            tf_saldo =  to_decimal("0")
                            output_list = Output_list()
                            output_list_data.append(output_list)

                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1,29 + 1) :
                            output_list.receiver = output_list.receiver + " "

                        if tot_flag:
                            output_list.receiver = output_list.receiver + "T O T A L"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        else:
                            output_list.receiver = output_list.receiver + "Sub-Total"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_debit =  to_decimal("0")
                        tf_debit =  to_decimal("0")
                        tot_saldo =  to_decimal("0")
                        tf_saldo =  to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.receiver = to_string(artikel.artnr, ">>>>>9") + " - " + to_string(artikel.bezeich, "x(30)")
                    artnr = artikel.artnr
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.ref_no1 = to_string(guest.firmen_nr)
                output_list.ref_no2 = guest.steuernr
                output_list.ref_no3 = debitor.debref

                bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)]})

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

                bediener = get_cache (Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.userinit = bediener.userinit
                else:
                    output_list.userinit = " "
                output_list.fsaldo = to_string(fsaldo, "->,>>>,>>>,>>>,>>9.99")
                output_list.verstat = debitor.verstat
                for j in range(1,38 + 1) :

                    if substring(debitor.vesrcod, j - 1, 1) == chr_unicode(10):
                        output_list.vesrcod = " "
                    else:
                        output_list.vesrcod = output_list.vesrcod + substring(debitor.vesrcod, j - 1, 1)
                output_list.ar_recid = debitor._recid
                output_list.info = debitor.vesrcod

                if debitor.versanddat != None:
                    output_list.maildate = debitor.versanddat

                if debitor.betrieb_gastmem != 0:

                    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                    if waehrung:
                        output_list.wabkurz = waehrung.wabkurz

                if debitor.betriebsnr == 0:

                    bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)],"resnr": [(gt, 0)],"gastnr": [(eq, debitor.gastnr)]})

                    if bill:

                        if bill.reslinnr == 0:

                            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"resstatus": [(eq, 8)]})

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                        else:

                            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                    else:

                        if debitor.vesrcod != " " and matches(debitor.vesrcod,r"*Deposit Payment*"):
                            resnr = to_int(entry(1, entry(0, debitor.vesrcod, ";") , ":"))

                            res_line = get_cache (Res_line, {"resnr": [(eq, resnr)]})

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                edit_list = Edit_list()
                edit_list_data.append(edit_list)

                edit_list.rechnr = debitor.rechnr
                edit_list.ar_recid = debitor._recid
                edit_list.datum = debitor.rgdatum
                edit_list.zinr = debitor.zinr
                edit_list.billname = receiver
                edit_list.famt =  to_decimal(debitor.vesrdep)
                edit_list.fcurr = output_list.wabkurz
                edit_list.curr_nr = debitor.betrieb_gastmem


                t_debit =  to_decimal(t_debit) + to_decimal(saldo)
                tot_debit =  to_decimal(tot_debit) + to_decimal(saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(saldo)
                tf_debit =  to_decimal(tf_debit) + to_decimal(fsaldo)
                ttf_debit =  to_decimal(ttf_debit) + to_decimal(fsaldo)
                tf_saldo =  to_decimal(tf_saldo) + to_decimal(fsaldo)

        if tot_saldo != 0 and tot_flag:
            output_list = Output_list()
            output_list_data.append(output_list)

            for i in range(1,29 + 1) :
                output_list.receiver = output_list.receiver + " "
            output_list.receiver = output_list.receiver + "Sub-Total"
            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


            output_list = Output_list()
            output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1,29 + 1) :
            output_list.receiver = output_list.receiver + " "

        if tot_flag:
            output_list.receiver = output_list.receiver + "T O T A L"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        else:
            output_list.receiver = output_list.receiver + "Sub-Total"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1,27 + 1) :
            output_list.receiver = output_list.receiver + " "
        output_list.receiver = output_list.receiver + "Grand TOTAL"
        output_list.saldo = to_string(tot_debit, "->,>>>,>>>,>>>,>>9.99")
        output_list.fsaldo = to_string(ttf_debit, "->,>>>,>>>,>>>,>>9.99")


    def create_list1():

        nonlocal d_rechnr, output_list_data, edit_list_data, debitor, artikel, guest, bill, bediener, waehrung, res_line
        nonlocal from_name, to_name, from_date, to_date, from_art, to_art, tot_flag, lesspay, show_inv, case_type


        nonlocal output_list, edit_list
        nonlocal output_list_data, edit_list_data

        artnr:int = 0
        t_debit:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        i:int = 0
        j:int = 0
        receiver:string = ""
        saldo:Decimal = to_decimal("0.0")
        bill_str:string = ""
        debt = None
        curr_gastnr:int = 0
        tot_saldo:Decimal = to_decimal("0.0")
        tf_saldo:Decimal = to_decimal("0.0")
        tf_debit:Decimal = to_decimal("0.0")
        ttf_debit:Decimal = to_decimal("0.0")
        fsaldo:Decimal = to_decimal("0.0")
        fcurr:string = ""
        resnr:int = 0
        Debt =  create_buffer("Debt",Debitor)
        output_list_data.clear()
        edit_list_data.clear()

        debitor_obj_list = {}
        debitor = Debitor()
        artikel = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.vesrdep, debitor.counter, debitor.debref, debitor.rechnr, debitor.rgdatum, debitor.zinr, debitor.bediener_nr, debitor.verstat, debitor.vesrcod, debitor._recid, debitor.versanddat, debitor.betrieb_gastmem, debitor.betriebsnr, artikel.artnr, artikel.bezeich, artikel._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest.firmen_nr, guest.steuernr, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.vesrdep, Debitor.counter, Debitor.debref, Debitor.rechnr, Debitor.rgdatum, Debitor.zinr, Debitor.bediener_nr, Debitor.verstat, Debitor.vesrcod, Debitor._recid, Debitor.versanddat, Debitor.betrieb_gastmem, Debitor.betriebsnr, Artikel.artnr, Artikel.bezeich, Artikel._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest.firmen_nr, Guest.steuernr, Guest._recid).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr) & (Guest.name >= (from_name).lower()) & (Guest.name <= (to_name).lower())).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto == 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.verstat == 9)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            if curr_gastnr == 0:
                curr_gastnr = debitor.gastnr

            if curr_gastnr != debitor.gastnr:
                curr_gastnr = debitor.gastnr

                if tot_saldo != 0 and tot_flag:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1,29 + 1) :
                        output_list.receiver = output_list.receiver + " "
                    output_list.receiver = output_list.receiver + "Sub-Total"
                    output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                    output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tf_saldo =  to_decimal("0")
            saldo =  to_decimal(debitor.saldo)
            fsaldo =  to_decimal(debitor.vesrdep)

            if debitor.counter > 0 and lesspay:

                for debt in db_session.query(Debt).filter(
                         (Debt.counter == debitor.counter) & (Debt.opart >= 1) & (Debt.zahlkonto > 0)).order_by(Debt._recid).all():
                    saldo =  to_decimal(saldo) + to_decimal(debt.saldo)
                    fsaldo =  to_decimal(fsaldo) + to_decimal(debt.vesrdep)


            if (saldo >= -0.05) and (saldo <= 0.05):
                saldo =  to_decimal("0")

            if saldo != 0:

                if artnr != artikel.artnr:

                    if artnr != 0:
                        curr_gastnr = debitor.gastnr

                        if tot_saldo != 0 and tot_flag:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            for i in range(1,29 + 1) :
                                output_list.receiver = output_list.receiver + " "
                            output_list.receiver = output_list.receiver + "Sub-Total"
                            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                            tot_saldo =  to_decimal("0")
                            tf_saldo =  to_decimal("0")
                            output_list = Output_list()
                            output_list_data.append(output_list)

                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1,29 + 1) :
                            output_list.receiver = output_list.receiver + " "

                        if tot_flag:
                            output_list.receiver = output_list.receiver + "T O T A L"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        else:
                            output_list.receiver = output_list.receiver + "Sub-Total"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_debit =  to_decimal("0")
                        tf_debit =  to_decimal("0")
                        tot_saldo =  to_decimal("0")
                        tf_saldo =  to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.receiver = to_string(artikel.artnr, ">>>>>9") + " - " + to_string(artikel.bezeich, "x(30)")
                    artnr = artikel.artnr
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.ref_no1 = to_string(guest.firmen_nr)
                output_list.ref_no2 = guest.steuernr
                output_list.ref_no3 = debitor.debref

                bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)]})

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

                bediener = get_cache (Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.userinit = bediener.userinit
                else:
                    output_list.userinit = " "
                output_list.fsaldo = to_string(fsaldo, "->,>>>,>>>,>>>,>>9.99")
                output_list.verstat = debitor.verstat
                for j in range(1,38 + 1) :

                    if substring(debitor.vesrcod, j - 1, 1) == chr_unicode(10):
                        output_list.vesrcod = " "
                    else:
                        output_list.vesrcod = output_list.vesrcod + substring(debitor.vesrcod, j - 1, 1)
                output_list.ar_recid = debitor._recid
                output_list.info = debitor.vesrcod

                if debitor.versanddat != None:
                    output_list.maildate = debitor.versanddat

                if debitor.betrieb_gastmem != 0:

                    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                    if waehrung:
                        output_list.wabkurz = waehrung.wabkurz

                if debitor.betriebsnr == 0:

                    bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)],"resnr": [(gt, 0)],"gastnr": [(eq, debitor.gastnr)]})

                    if bill:

                        if bill.reslinnr == 0:

                            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"resstatus": [(eq, 8)]})

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                        else:

                            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                    else:

                        if debitor.vesrcod != " " and matches(debitor.vesrcod,r"*Deposit Payment*"):
                            resnr = to_int(entry(1, entry(0, debitor.vesrcod, ";") , ":"))

                            res_line = get_cache (Res_line, {"resnr": [(eq, resnr)]})

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                edit_list = Edit_list()
                edit_list_data.append(edit_list)

                edit_list.rechnr = debitor.rechnr
                edit_list.ar_recid = debitor._recid
                edit_list.datum = debitor.rgdatum
                edit_list.zinr = debitor.zinr
                edit_list.billname = receiver
                edit_list.famt =  to_decimal(debitor.vesrdep)
                edit_list.fcurr = output_list.wabkurz
                edit_list.curr_nr = debitor.betrieb_gastmem


                t_debit =  to_decimal(t_debit) + to_decimal(saldo)
                tot_debit =  to_decimal(tot_debit) + to_decimal(saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(saldo)
                tf_debit =  to_decimal(tf_debit) + to_decimal(fsaldo)
                ttf_debit =  to_decimal(ttf_debit) + to_decimal(fsaldo)
                tf_saldo =  to_decimal(tf_saldo) + to_decimal(fsaldo)

        if tot_saldo != 0 and tot_flag:
            output_list = Output_list()
            output_list_data.append(output_list)

            for i in range(1,29 + 1) :
                output_list.receiver = output_list.receiver + " "
            output_list.receiver = output_list.receiver + "Sub-Total"
            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


            output_list = Output_list()
            output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1,29 + 1) :
            output_list.receiver = output_list.receiver + " "

        if tot_flag:
            output_list.receiver = output_list.receiver + "T O T A L"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        else:
            output_list.receiver = output_list.receiver + "Sub-Total"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1,27 + 1) :
            output_list.receiver = output_list.receiver + " "
        output_list.receiver = output_list.receiver + "Grand TOTAL"
        output_list.saldo = to_string(tot_debit, "->,>>>,>>>,>>>,>>9.99")
        output_list.fsaldo = to_string(ttf_debit, "->,>>>,>>>,>>>,>>9.99")


    def create_list1a():

        nonlocal d_rechnr, output_list_data, edit_list_data, debitor, artikel, guest, bill, bediener, waehrung, res_line
        nonlocal from_name, to_name, from_date, to_date, from_art, to_art, tot_flag, lesspay, show_inv, case_type


        nonlocal output_list, edit_list
        nonlocal output_list_data, edit_list_data

        artnr:int = 0
        t_debit:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        i:int = 0
        j:int = 0
        receiver:string = ""
        saldo:Decimal = to_decimal("0.0")
        bill_str:string = ""
        debt = None
        curr_gastnr:int = 0
        tot_saldo:Decimal = to_decimal("0.0")
        tf_saldo:Decimal = to_decimal("0.0")
        tf_debit:Decimal = to_decimal("0.0")
        ttf_debit:Decimal = to_decimal("0.0")
        fsaldo:Decimal = to_decimal("0.0")
        resnr:int = 0
        Debt =  create_buffer("Debt",Debitor)
        output_list_data.clear()

        debitor_obj_list = {}
        debitor = Debitor()
        artikel = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.vesrdep, debitor.counter, debitor.debref, debitor.rechnr, debitor.rgdatum, debitor.zinr, debitor.bediener_nr, debitor.verstat, debitor.vesrcod, debitor._recid, debitor.versanddat, debitor.betrieb_gastmem, debitor.betriebsnr, artikel.artnr, artikel.bezeich, artikel._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest.firmen_nr, guest.steuernr, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.vesrdep, Debitor.counter, Debitor.debref, Debitor.rechnr, Debitor.rgdatum, Debitor.zinr, Debitor.bediener_nr, Debitor.verstat, Debitor.vesrcod, Debitor._recid, Debitor.versanddat, Debitor.betrieb_gastmem, Debitor.betriebsnr, Artikel.artnr, Artikel.bezeich, Artikel._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest.firmen_nr, Guest.steuernr, Guest._recid).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr) & (Guest.name >= (from_name).lower())).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto == 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.verstat == 9)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            if curr_gastnr == 0:
                curr_gastnr = debitor.gastnr

            if curr_gastnr != debitor.gastnr:
                curr_gastnr = debitor.gastnr

                if tot_saldo != 0 and tot_flag:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1,29 + 1) :
                        output_list.receiver = output_list.receiver + " "
                    output_list.receiver = output_list.receiver + "Sub-Total"
                    output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                    output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tf_saldo =  to_decimal("0")
            saldo =  to_decimal(debitor.saldo)
            fsaldo =  to_decimal(debitor.vesrdep)

            if debitor.counter > 0 and lesspay:

                for debt in db_session.query(Debt).filter(
                         (Debt.counter == debitor.counter) & (Debt.opart >= 1) & (Debt.zahlkonto > 0)).order_by(Debt._recid).all():
                    saldo =  to_decimal(saldo) + to_decimal(debt.saldo)
                    fsaldo =  to_decimal(fsaldo) + to_decimal(debt.vesrdep)


            if (saldo >= -0.05) and (saldo <= 0.05):
                saldo =  to_decimal("0")

            if saldo != 0:

                if artnr != artikel.artnr:

                    if artnr != 0:
                        curr_gastnr = debitor.gastnr

                        if tot_saldo != 0 and tot_flag:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            for i in range(1,29 + 1) :
                                output_list.receiver = output_list.receiver + " "
                            output_list.receiver = output_list.receiver + "Sub-Total"
                            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                            tot_saldo =  to_decimal("0")
                            tf_saldo =  to_decimal("0")
                            output_list = Output_list()
                            output_list_data.append(output_list)

                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1,29 + 1) :
                            output_list.receiver = output_list.receiver + " "

                        if tot_flag:
                            output_list.receiver = output_list.receiver + "T O T A L"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        else:
                            output_list.receiver = output_list.receiver + "Sub-Total"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_debit =  to_decimal("0")
                        tf_debit =  to_decimal("0")
                        tot_saldo =  to_decimal("0")
                        tf_saldo =  to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.receiver = to_string(artikel.artnr, ">>>>>9") + " - " + to_string(artikel.bezeich, "x(30)")
                    artnr = artikel.artnr
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.ref_no1 = to_string(guest.firmen_nr)
                output_list.ref_no2 = guest.steuernr
                output_list.ref_no3 = debitor.debref

                bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)]})

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

                bediener = get_cache (Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.userinit = bediener.userinit
                else:
                    output_list.userinit = " "
                output_list.fsaldo = to_string(fsaldo, "->,>>>,>>>,>>>,>>9.99")
                output_list.verstat = debitor.verstat
                for j in range(1,38 + 1) :

                    if substring(debitor.vesrcod, j - 1, 1) == chr_unicode(10):
                        output_list.vesrcod = " "
                    else:
                        output_list.vesrcod = output_list.vesrcod + substring(debitor.vesrcod, j - 1, 1)
                output_list.ar_recid = debitor._recid
                output_list.info = debitor.vesrcod

                if debitor.versanddat != None:
                    output_list.maildate = debitor.versanddat

                if debitor.betrieb_gastmem != 0:

                    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                    if waehrung:
                        output_list.wabkurz = waehrung.wabkurz

                if debitor.betriebsnr == 0:

                    bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)],"resnr": [(gt, 0)],"gastnr": [(eq, debitor.gastnr)]})

                    if bill:

                        if bill.reslinnr == 0:

                            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"resstatus": [(eq, 8)]})

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                        else:

                            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                    else:

                        if debitor.vesrcod != " " and matches(debitor.vesrcod,r"*Deposit Payment*"):
                            resnr = to_int(entry(1, entry(0, debitor.vesrcod, ";") , ":"))

                            res_line = get_cache (Res_line, {"resnr": [(eq, resnr)]})

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                edit_list = Edit_list()
                edit_list_data.append(edit_list)

                edit_list.rechnr = debitor.rechnr
                edit_list.ar_recid = debitor._recid
                edit_list.datum = debitor.rgdatum
                edit_list.zinr = debitor.zinr
                edit_list.billname = receiver
                edit_list.famt =  to_decimal(debitor.vesrdep)
                edit_list.fcurr = output_list.wabkurz
                edit_list.curr_nr = debitor.betrieb_gastmem


                t_debit =  to_decimal(t_debit) + to_decimal(saldo)
                tot_debit =  to_decimal(tot_debit) + to_decimal(saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(saldo)
                tf_debit =  to_decimal(tf_debit) + to_decimal(fsaldo)
                ttf_debit =  to_decimal(ttf_debit) + to_decimal(fsaldo)
                tf_saldo =  to_decimal(tf_saldo) + to_decimal(fsaldo)

        if tot_saldo != 0 and tot_flag:
            output_list = Output_list()
            output_list_data.append(output_list)

            for i in range(1,29 + 1) :
                output_list.receiver = output_list.receiver + " "
            output_list.receiver = output_list.receiver + "Sub-Total"
            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


            output_list = Output_list()
            output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1,29 + 1) :
            output_list.receiver = output_list.receiver + " "

        if tot_flag:
            output_list.receiver = output_list.receiver + "T O T A L"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        else:
            output_list.receiver = output_list.receiver + "Sub-Total"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1,27 + 1) :
            output_list.receiver = output_list.receiver + " "
        output_list.receiver = output_list.receiver + "Grand TOTAL"
        output_list.saldo = to_string(tot_debit, "->,>>>,>>>,>>>,>>9.99")
        output_list.fsaldo = to_string(ttf_debit, "->,>>>,>>>,>>>,>>9.99")


    def create_list2():

        nonlocal d_rechnr, output_list_data, edit_list_data, debitor, artikel, guest, bill, bediener, waehrung, res_line
        nonlocal from_name, to_name, from_date, to_date, from_art, to_art, tot_flag, lesspay, show_inv, case_type


        nonlocal output_list, edit_list
        nonlocal output_list_data, edit_list_data

        artnr:int = 0
        t_debit:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        i:int = 0
        j:int = 0
        receiver:string = ""
        saldo:Decimal = to_decimal("0.0")
        bill_str:string = ""
        debt = None
        curr_gastnr:int = 0
        tot_saldo:Decimal = to_decimal("0.0")
        tf_saldo:Decimal = to_decimal("0.0")
        tf_debit:Decimal = to_decimal("0.0")
        ttf_debit:Decimal = to_decimal("0.0")
        fsaldo:Decimal = to_decimal("0.0")
        fcurr:string = ""
        resnr:int = 0
        Debt =  create_buffer("Debt",Debitor)
        output_list_data.clear()
        edit_list_data.clear()

        debitor_obj_list = {}
        debitor = Debitor()
        artikel = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.vesrdep, debitor.counter, debitor.debref, debitor.rechnr, debitor.rgdatum, debitor.zinr, debitor.bediener_nr, debitor.verstat, debitor.vesrcod, debitor._recid, debitor.versanddat, debitor.betrieb_gastmem, debitor.betriebsnr, artikel.artnr, artikel.bezeich, artikel._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest.firmen_nr, guest.steuernr, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.vesrdep, Debitor.counter, Debitor.debref, Debitor.rechnr, Debitor.rgdatum, Debitor.zinr, Debitor.bediener_nr, Debitor.verstat, Debitor.vesrcod, Debitor._recid, Debitor.versanddat, Debitor.betrieb_gastmem, Debitor.betriebsnr, Artikel.artnr, Artikel.bezeich, Artikel._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest.firmen_nr, Guest.steuernr, Guest._recid).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr) & (Guest.name >= (from_name).lower()) & (Guest.name <= (to_name).lower())).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto == 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.verstat != 9)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            if curr_gastnr == 0:
                curr_gastnr = debitor.gastnr

            if curr_gastnr != debitor.gastnr:
                curr_gastnr = debitor.gastnr

                if tot_saldo != 0 and tot_flag:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1,29 + 1) :
                        output_list.receiver = output_list.receiver + " "
                    output_list.receiver = output_list.receiver + "Sub-Total"
                    output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                    output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tf_saldo =  to_decimal("0")
            saldo =  to_decimal(debitor.saldo)
            fsaldo =  to_decimal(debitor.vesrdep)

            if debitor.counter > 0 and lesspay:

                for debt in db_session.query(Debt).filter(
                         (Debt.counter == debitor.counter) & (Debt.opart >= 1) & (Debt.zahlkonto > 0)).order_by(Debt._recid).all():
                    saldo =  to_decimal(saldo) + to_decimal(debt.saldo)
                    fsaldo =  to_decimal(fsaldo) + to_decimal(debt.vesrdep)


            if (saldo >= -0.05) and (saldo <= 0.05):
                saldo =  to_decimal("0")

            if saldo != 0:

                if artnr != artikel.artnr:

                    if artnr != 0:
                        curr_gastnr = debitor.gastnr

                        if tot_saldo != 0 and tot_flag:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            for i in range(1,29 + 1) :
                                output_list.receiver = output_list.receiver + " "
                            output_list.receiver = output_list.receiver + "Sub-Total"
                            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                            tot_saldo =  to_decimal("0")
                            tf_saldo =  to_decimal("0")
                            output_list = Output_list()
                            output_list_data.append(output_list)

                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1,29 + 1) :
                            output_list.receiver = output_list.receiver + " "

                        if tot_flag:
                            output_list.receiver = output_list.receiver + "T O T A L"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        else:
                            output_list.receiver = output_list.receiver + "Sub-Total"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_debit =  to_decimal("0")
                        tf_debit =  to_decimal("0")
                        tot_saldo =  to_decimal("0")
                        tf_saldo =  to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.receiver = to_string(artikel.artnr, ">>>>>9") + " - " + to_string(artikel.bezeich, "x(30)")
                    artnr = artikel.artnr
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.ref_no1 = to_string(guest.firmen_nr)
                output_list.ref_no2 = guest.steuernr
                output_list.ref_no3 = debitor.debref

                bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)]})

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

                bediener = get_cache (Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.userinit = bediener.userinit
                else:
                    output_list.userinit = " "
                output_list.fsaldo = to_string(fsaldo, "->,>>>,>>>,>>>,>>9.99")
                output_list.verstat = debitor.verstat
                for j in range(1,38 + 1) :

                    if substring(debitor.vesrcod, j - 1, 1) == chr_unicode(10):
                        output_list.vesrcod = " "
                    else:
                        output_list.vesrcod = output_list.vesrcod + substring(debitor.vesrcod, j - 1, 1)
                output_list.ar_recid = debitor._recid
                output_list.info = debitor.vesrcod

                if debitor.versanddat != None:
                    output_list.maildate = debitor.versanddat

                if debitor.betrieb_gastmem != 0:

                    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                    if waehrung:
                        output_list.wabkurz = waehrung.wabkurz

                if debitor.betriebsnr == 0:

                    bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)],"resnr": [(gt, 0)],"gastnr": [(eq, debitor.gastnr)]})

                    if bill:

                        if bill.reslinnr == 0:

                            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"resstatus": [(eq, 8)]})

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                        else:

                            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                    else:

                        if debitor.vesrcod != " " and matches(debitor.vesrcod,r"*Deposit Payment*"):
                            resnr = to_int(entry(1, entry(0, debitor.vesrcod, ";") , ":"))

                            res_line = get_cache (Res_line, {"resnr": [(eq, resnr)]})

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                edit_list = Edit_list()
                edit_list_data.append(edit_list)

                edit_list.rechnr = debitor.rechnr
                edit_list.ar_recid = debitor._recid
                edit_list.datum = debitor.rgdatum
                edit_list.zinr = debitor.zinr
                edit_list.billname = receiver
                edit_list.famt =  to_decimal(debitor.vesrdep)
                edit_list.fcurr = output_list.wabkurz
                edit_list.curr_nr = debitor.betrieb_gastmem


                t_debit =  to_decimal(t_debit) + to_decimal(saldo)
                tot_debit =  to_decimal(tot_debit) + to_decimal(saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(saldo)
                tf_debit =  to_decimal(tf_debit) + to_decimal(fsaldo)
                ttf_debit =  to_decimal(ttf_debit) + to_decimal(fsaldo)
                tf_saldo =  to_decimal(tf_saldo) + to_decimal(fsaldo)

        if tot_saldo != 0 and tot_flag:
            output_list = Output_list()
            output_list_data.append(output_list)

            for i in range(1,29 + 1) :
                output_list.receiver = output_list.receiver + " "
            output_list.receiver = output_list.receiver + "Sub-Total"
            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


            output_list = Output_list()
            output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1,29 + 1) :
            output_list.receiver = output_list.receiver + " "

        if tot_flag:
            output_list.receiver = output_list.receiver + "T O T A L"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        else:
            output_list.receiver = output_list.receiver + "Sub-Total"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1,27 + 1) :
            output_list.receiver = output_list.receiver + " "
        output_list.receiver = output_list.receiver + "Grand TOTAL"
        output_list.saldo = to_string(tot_debit, "->,>>>,>>>,>>>,>>9.99")
        output_list.fsaldo = to_string(ttf_debit, "->,>>>,>>>,>>>,>>9.99")


    def create_list2a():

        nonlocal d_rechnr, output_list_data, edit_list_data, debitor, artikel, guest, bill, bediener, waehrung, res_line
        nonlocal from_name, to_name, from_date, to_date, from_art, to_art, tot_flag, lesspay, show_inv, case_type


        nonlocal output_list, edit_list
        nonlocal output_list_data, edit_list_data

        artnr:int = 0
        t_debit:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        i:int = 0
        j:int = 0
        receiver:string = ""
        saldo:Decimal = to_decimal("0.0")
        bill_str:string = ""
        debt = None
        curr_gastnr:int = 0
        tot_saldo:Decimal = to_decimal("0.0")
        tf_saldo:Decimal = to_decimal("0.0")
        tf_debit:Decimal = to_decimal("0.0")
        ttf_debit:Decimal = to_decimal("0.0")
        fsaldo:Decimal = to_decimal("0.0")
        resnr:int = 0
        Debt =  create_buffer("Debt",Debitor)
        output_list_data.clear()

        debitor_obj_list = {}
        debitor = Debitor()
        artikel = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.vesrdep, debitor.counter, debitor.debref, debitor.rechnr, debitor.rgdatum, debitor.zinr, debitor.bediener_nr, debitor.verstat, debitor.vesrcod, debitor._recid, debitor.versanddat, debitor.betrieb_gastmem, debitor.betriebsnr, artikel.artnr, artikel.bezeich, artikel._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest.firmen_nr, guest.steuernr, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.vesrdep, Debitor.counter, Debitor.debref, Debitor.rechnr, Debitor.rgdatum, Debitor.zinr, Debitor.bediener_nr, Debitor.verstat, Debitor.vesrcod, Debitor._recid, Debitor.versanddat, Debitor.betrieb_gastmem, Debitor.betriebsnr, Artikel.artnr, Artikel.bezeich, Artikel._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest.firmen_nr, Guest.steuernr, Guest._recid).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr) & (Guest.name >= (from_name).lower())).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto == 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.verstat != 9)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            if curr_gastnr == 0:
                curr_gastnr = debitor.gastnr

            if curr_gastnr != debitor.gastnr:
                curr_gastnr = debitor.gastnr

                if tot_saldo != 0 and tot_flag:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1,29 + 1) :
                        output_list.receiver = output_list.receiver + " "
                    output_list.receiver = output_list.receiver + "Sub-Total"
                    output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                    output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tf_saldo =  to_decimal("0")
            saldo =  to_decimal(debitor.saldo)
            fsaldo =  to_decimal(debitor.vesrdep)

            if debitor.counter > 0 and lesspay:

                for debt in db_session.query(Debt).filter(
                         (Debt.counter == debitor.counter) & (Debt.opart >= 1) & (Debt.zahlkonto > 0)).order_by(Debt._recid).all():
                    saldo =  to_decimal(saldo) + to_decimal(debt.saldo)
                    fsaldo =  to_decimal(fsaldo) + to_decimal(debt.vesrdep)


            if (saldo >= -0.05) and (saldo <= 0.05):
                saldo =  to_decimal("0")

            if saldo != 0:

                if artnr != artikel.artnr:

                    if artnr != 0:
                        curr_gastnr = debitor.gastnr

                        if tot_saldo != 0 and tot_flag:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            for i in range(1,29 + 1) :
                                output_list.receiver = output_list.receiver + " "
                            output_list.receiver = output_list.receiver + "Sub-Total"
                            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


                            tot_saldo =  to_decimal("0")
                            tf_saldo =  to_decimal("0")
                            output_list = Output_list()
                            output_list_data.append(output_list)

                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1,29 + 1) :
                            output_list.receiver = output_list.receiver + " "

                        if tot_flag:
                            output_list.receiver = output_list.receiver + "T O T A L"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        else:
                            output_list.receiver = output_list.receiver + "Sub-Total"
                            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_debit =  to_decimal("0")
                        tf_debit =  to_decimal("0")
                        tot_saldo =  to_decimal("0")
                        tf_saldo =  to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.receiver = to_string(artikel.artnr, ">>>>>9") + " - " + to_string(artikel.bezeich, "x(30)")
                    artnr = artikel.artnr
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.ref_no1 = to_string(guest.firmen_nr)
                output_list.ref_no2 = guest.steuernr
                output_list.ref_no3 = debitor.debref

                bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)]})

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

                bediener = get_cache (Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.userinit = bediener.userinit
                else:
                    output_list.userinit = " "
                output_list.fsaldo = to_string(fsaldo, "->,>>>,>>>,>>>,>>9.99")
                output_list.verstat = debitor.verstat
                for j in range(1,38 + 1) :

                    if substring(debitor.vesrcod, j - 1, 1) == chr_unicode(10):
                        output_list.vesrcod = " "
                    else:
                        output_list.vesrcod = output_list.vesrcod + substring(debitor.vesrcod, j - 1, 1)
                output_list.ar_recid = debitor._recid
                output_list.info = debitor.vesrcod

                if debitor.versanddat != None:
                    output_list.maildate = debitor.versanddat

                if debitor.betrieb_gastmem != 0:

                    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                    if waehrung:
                        output_list.wabkurz = waehrung.wabkurz

                if debitor.betriebsnr == 0:

                    bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)],"resnr": [(gt, 0)],"gastnr": [(eq, debitor.gastnr)]})

                    if bill:

                        if bill.reslinnr == 0:

                            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"resstatus": [(eq, 8)]})

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                        else:

                            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                    else:

                        if debitor.vesrcod != " " and matches(debitor.vesrcod,r"*Deposit Payment*"):
                            resnr = to_int(entry(1, entry(0, debitor.vesrcod, ";") , ":"))

                            res_line = get_cache (Res_line, {"resnr": [(eq, resnr)]})

                            if res_line:
                                output_list.ci_date = res_line.ankunft
                                output_list.co_date = res_line.abreise
                                output_list.nights = to_string(to_int(res_line.abreise - res_line.ankunft) , ">>9")


                edit_list = Edit_list()
                edit_list_data.append(edit_list)

                edit_list.rechnr = debitor.rechnr
                edit_list.ar_recid = debitor._recid
                edit_list.datum = debitor.rgdatum
                edit_list.zinr = debitor.zinr
                edit_list.billname = receiver
                edit_list.famt =  to_decimal(debitor.vesrdep)
                edit_list.fcurr = output_list.wabkurz
                edit_list.curr_nr = debitor.betrieb_gastmem


                t_debit =  to_decimal(t_debit) + to_decimal(saldo)
                tot_debit =  to_decimal(tot_debit) + to_decimal(saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(saldo)
                tf_debit =  to_decimal(tf_debit) + to_decimal(fsaldo)
                ttf_debit =  to_decimal(ttf_debit) + to_decimal(fsaldo)
                tf_saldo =  to_decimal(tf_saldo) + to_decimal(fsaldo)

        if tot_saldo != 0 and tot_flag:
            output_list = Output_list()
            output_list_data.append(output_list)

            for i in range(1,29 + 1) :
                output_list.receiver = output_list.receiver + " "
            output_list.receiver = output_list.receiver + "Sub-Total"
            output_list.saldo = to_string(tot_saldo, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_saldo, "->,>>>,>>>,>>>,>>9.99")


            output_list = Output_list()
            output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1,29 + 1) :
            output_list.receiver = output_list.receiver + " "

        if tot_flag:
            output_list.receiver = output_list.receiver + "T O T A L"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        else:
            output_list.receiver = output_list.receiver + "Sub-Total"
            output_list.saldo = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            output_list.fsaldo = to_string(tf_debit, "->,>>>,>>>,>>>,>>9.99")


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1,27 + 1) :
            output_list.receiver = output_list.receiver + " "
        output_list.receiver = output_list.receiver + "Grand TOTAL"
        output_list.saldo = to_string(tot_debit, "->,>>>,>>>,>>>,>>9.99")
        output_list.fsaldo = to_string(ttf_debit, "->,>>>,>>>,>>>,>>9.99")

    if case_type == 0:

        if substring(to_name, 0, 2) == ("zz").lower() :
            create_lista()
        else:
            create_list()
    elif case_type == 1:

        if substring(to_name, 0, 2) == ("zz").lower() :
            create_list1a()
        else:
            create_list1()
    elif case_type == 2:

        if substring(to_name, 0, 2) == ("zz").lower() :
            create_list2a()
        else:
            create_list2()

    return generate_output()