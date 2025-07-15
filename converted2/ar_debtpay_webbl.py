#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Debitor, Artikel, Guest, Bill_line, Bill, Bediener, Waehrung, Reservation, Res_line

def ar_debtpay_webbl(artnr:int, userinit:string, bill_nr:int, temp_art2:int, bill_date:date, bill_name:string, to_name:string, bill_saldo:Decimal, art_selected:int, foutstand:Decimal, outstand:Decimal):

    prepare_cache ([Debitor, Guest, Bill_line, Bill, Bediener, Waehrung, Res_line])

    curr_art = 0
    age_list_data = []
    t_debt_data = []
    t_resnr:int = 0
    t_name:string = ""
    debitor = artikel = guest = bill_line = bill = bediener = waehrung = reservation = res_line = None

    t_debt = age_list = abuff = debt = t_pay = age_list1 = None

    t_debt_data, T_debt = create_model("T_debt", {"t_debt_recid":int, "rgdatum":date})
    age_list_data, Age_list = create_model("Age_list", {"selected":bool, "ar_recid":int, "rechnr":int, "refno":int, "counter":int, "gastnr":int, "billname":string, "gastnrmember":int, "gastname":string, "zinr":string, "rgdatum":date, "user_init":string, "debt":Decimal, "debt_foreign":Decimal, "currency":string, "credit":Decimal, "tot_debt":Decimal, "vouc_nr":string, "prevdate":date, "remarks":string, "b_resname":string, "ci_date":date, "co_date":date, "resnr":int, "mbill":string})

    Abuff = Age_list
    abuff_data = age_list_data

    Debt = create_buffer("Debt",Debitor)
    T_pay = create_buffer("T_pay",Debitor)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_art, age_list_data, t_debt_data, t_resnr, t_name, debitor, artikel, guest, bill_line, bill, bediener, waehrung, reservation, res_line
        nonlocal artnr, userinit, bill_nr, temp_art2, bill_date, bill_name, to_name, bill_saldo, art_selected, foutstand, outstand
        nonlocal abuff, debt, t_pay


        nonlocal t_debt, age_list, abuff, debt, t_pay, age_list1
        nonlocal t_debt_data, age_list_data

        return {"art_selected": art_selected, "foutstand": foutstand, "outstand": outstand, "curr_art": curr_art, "age-list": age_list_data, "t-debt": t_debt_data}

    def create_age_list():

        nonlocal curr_art, age_list_data, t_debt_data, t_resnr, t_name, debitor, artikel, guest, bill_line, bill, bediener, waehrung, reservation, res_line
        nonlocal artnr, userinit, bill_nr, temp_art2, bill_date, bill_name, to_name, bill_saldo, art_selected, foutstand, outstand
        nonlocal abuff, debt, t_pay


        nonlocal t_debt, age_list, abuff, debt, t_pay, age_list1
        nonlocal t_debt_data, age_list_data

        artikel1 = None
        curr_rechnr:int = 0
        curr_saldo:Decimal = to_decimal("0.0")
        opart:int = 1
        i:int = 0
        Artikel1 =  create_buffer("Artikel1",Artikel)
        curr_art = artnr
        age_list_data.clear()
        curr_rechnr = 0
        outstand =  to_decimal("0")
        foutstand =  to_decimal("0")

        if bill_nr != 0:

            for debitor in db_session.query(Debitor).filter(
                         (Debitor.artnr == temp_art2) & (Debitor.rechnr == bill_nr) & (Debitor.rgdatum <= bill_date) & (Debitor.opart < 2)).order_by(Debitor.zahlkonto, Debitor.rgdatum).all():

                if debitor.counter != 0:

                    age_list = query(age_list_data, filters=(lambda age_list: age_list.counter == debitor.counter), first=True)

                if not age_list or debitor.counter == 0:
                    age_list = Age_list()
                    age_list_data.append(age_list)

                    age_list.ar_recid = debitor._recid
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.rechnr = debitor.rechnr
                    age_list.refno = debitor.debref
                    age_list.gastnr = debitor.gastnr
                    age_list.gastnrmember = debitor.gastnrmember
                    age_list.zinr = debitor.zinr
                    disp_guest_debt()

                    guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})
                    age_list.billname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                    if guest:
                        age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    bill_line = get_cache (Bill_line, {"rechnr": [(eq, debitor.rechnr)],"betrag": [(eq, (- debitor.saldo))],"zeit": [(ge, (debitor.transzeit - 2)),(le, debitor.transzeit + 2)]})

                    bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)],"gastnr": [(eq, debitor.gastnr)]})

                    if bill:

                        if bill.reslinnr == 0:
                            age_list.resnr = bill.resnr
                            age_list.mbill = "*"

                if debitor.zahlkonto == 0:

                    bediener = get_cache (Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                    if bediener:
                        age_list.user_init = bediener.userinit
                    age_list.rgdatum = debitor.rgdatum
                    age_list.debt =  to_decimal(age_list.debt) + to_decimal(debitor.saldo)
                    age_list.debt_foreign =  to_decimal(age_list.debt_foreign) + to_decimal(debitor.vesrdep)

                    if debitor.betrieb_gastmem != 0:

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                        if waehrung:
                            age_list.currency = waehrung.wabkurz
                else:
                    age_list.credit =  to_decimal(age_list.credit) - to_decimal(debitor.saldo)
                age_list.tot_debt =  to_decimal(age_list.tot_debt) + to_decimal(debitor.saldo)

        elif (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

            for debitor in db_session.query(Debitor).filter(
                         (Debitor.artnr == temp_art2) & (matches(Debitor.name,("*" + bill_name + "*"))) & (Debitor.name <= (to_name).lower()) & (Debitor.rgdatum <= bill_date) & (Debitor.opart < 2)).order_by(Debitor.zahlkonto, Debitor.debref, Debitor.rgdatum).all():

                if debitor.counter != 0:

                    age_list = query(age_list_data, filters=(lambda age_list: age_list.counter == debitor.counter), first=True)

                if not age_list or debitor.counter == 0:
                    age_list = Age_list()
                    age_list_data.append(age_list)

                    age_list.ar_recid = debitor._recid
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.rechnr = debitor.rechnr
                    age_list.refno = debitor.debref
                    age_list.gastnr = debitor.gastnr
                    age_list.gastnrmember = debitor.gastnrmember
                    age_list.zinr = debitor.zinr
                    disp_guest_debt()

                    guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})
                    age_list.billname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                    if guest:
                        age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    bill_line = get_cache (Bill_line, {"rechnr": [(eq, debitor.rechnr)],"betrag": [(eq, (- debitor.saldo))],"zeit": [(ge, (debitor.transzeit - 2)),(le, debitor.transzeit + 2)]})

                    bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)],"gastnr": [(eq, debitor.gastnr)]})

                    if bill:

                        if bill.reslinnr == 0:
                            age_list.resnr = bill.resnr
                            age_list.mbill = "*"

                    if matches(debitor.vesrcod,r"*resno:*"):

                        if num_entries(debitor.vesrcod, ";") == 1:
                            t_resnr = to_int(trim(entry(1, entry(0, debitor.vesrcod, ";") , ":")))


                        else:
                            t_name = trim(entry(0, debitor.vesrcod, ";"))
                            t_resnr = to_int(trim(entry(1, t_name, ":")))

                        reservation = get_cache (Reservation, {"resnr": [(eq, t_resnr)]})

                        res_line = get_cache (Res_line, {"resnr": [(eq, t_resnr)]})

                        if res_line:

                            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                            age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    if (matches(debitor.vesrcod,r"*;*")):
                        age_list.vouc_nr = trim(entry(1, debitor.vesrcod, ";"))
                        age_list.remarks = trim(entry(0, debitor.vesrcod, ";"))


                    else:
                        age_list.remarks = debitor.vesrcod

                        bill_line = get_cache (Bill_line, {"rechnr": [(eq, debitor.rechnr)],"betrag": [(eq, (- debitor.saldo))],"zeit": [(ge, (debitor.transzeit - 2)),(le, debitor.transzeit + 2)]})

                        if bill_line:
                            for i in range(1,(length(bill_line.bezeich))  + 1) :

                                if substring(bill_line.bezeich, i - 1, 1) == ("/").lower() :
                                    age_list.vouc_nr = substring(bill_line.bezeich, (i + 1) - 1, (length(bill_line.bezeich) - i))
                                    i = length(bill_line.bezeich)

                if debitor.zahlkonto == 0:

                    bediener = get_cache (Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                    if bediener:
                        age_list.user_init = bediener.userinit
                    age_list.rgdatum = debitor.rgdatum
                    age_list.debt =  to_decimal(age_list.debt) + to_decimal(debitor.saldo)
                    age_list.debt_foreign =  to_decimal(age_list.debt_foreign) + to_decimal(debitor.vesrdep)

                    if debitor.betrieb_gastmem != 0:

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                        if waehrung:
                            age_list.currency = waehrung.wabkurz
                else:
                    age_list.credit =  to_decimal(age_list.credit) - to_decimal(debitor.saldo)
                age_list.tot_debt =  to_decimal(age_list.tot_debt) + to_decimal(debitor.saldo)

        elif (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

            for debitor in db_session.query(Debitor).filter(
                         (Debitor.artnr == temp_art2) & (matches(Debitor.name,(bill_name))) & (Debitor.rgdatum <= bill_date) & (Debitor.opart < 2)).order_by(Debitor.zahlkonto, Debitor.debref, Debitor.rgdatum).all():

                if debitor.counter != 0:

                    age_list = query(age_list_data, filters=(lambda age_list: age_list.counter == debitor.counter), first=True)

                if not age_list or debitor.counter == 0:
                    age_list = Age_list()
                    age_list_data.append(age_list)

                    age_list.ar_recid = debitor._recid
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.rechnr = debitor.rechnr
                    age_list.refno = debitor.debref
                    age_list.gastnr = debitor.gastnr
                    age_list.gastnrmember = debitor.gastnrmember
                    age_list.zinr = debitor.zinr
                    disp_guest_debt()

                    guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})
                    age_list.billname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                    if guest:
                        age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    bill_line = get_cache (Bill_line, {"rechnr": [(eq, debitor.rechnr)],"betrag": [(eq, (- debitor.saldo))],"zeit": [(ge, (debitor.transzeit - 2)),(le, debitor.transzeit + 2)]})

                    bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)],"gastnr": [(eq, debitor.gastnr)]})

                    if bill:

                        if bill.reslinnr == 0:
                            age_list.resnr = bill.resnr
                            age_list.mbill = "*"

                    if matches(debitor.vesrcod,r"*resno:*"):

                        if num_entries(debitor.vesrcod, ";") == 1:
                            t_resnr = to_int(trim(entry(1, entry(0, debitor.vesrcod, ";") , ":")))


                        else:
                            t_name = trim(entry(0, debitor.vesrcod, ";"))
                            t_resnr = to_int(trim(entry(1, t_name, ":")))

                        reservation = get_cache (Reservation, {"resnr": [(eq, t_resnr)]})

                        res_line = get_cache (Res_line, {"resnr": [(eq, t_resnr)]})

                        if res_line:

                            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                            age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    if (matches(debitor.vesrcod,r"*;*")):
                        age_list.vouc_nr = trim(entry(1, debitor.vesrcod, ";"))
                        age_list.remarks = trim(entry(0, debitor.vesrcod, ";"))


                    else:
                        age_list.remarks = debitor.vesrcod

                        bill_line = get_cache (Bill_line, {"rechnr": [(eq, debitor.rechnr)],"betrag": [(eq, (- debitor.saldo))],"zeit": [(ge, (debitor.transzeit - 2)),(le, debitor.transzeit + 2)]})

                        if bill_line:
                            for i in range(1,(length(bill_line.bezeich))  + 1) :

                                if substring(bill_line.bezeich, i - 1, 1) == ("/").lower() :
                                    age_list.vouc_nr = substring(bill_line.bezeich, (i + 1) - 1, (length(bill_line.bezeich) - i))
                                    i = length(bill_line.bezeich)

                if debitor.zahlkonto == 0:

                    bediener = get_cache (Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                    if bediener:
                        age_list.user_init = bediener.userinit
                    age_list.rgdatum = debitor.rgdatum
                    age_list.debt =  to_decimal(age_list.debt) + to_decimal(debitor.saldo)
                    age_list.debt_foreign =  to_decimal(age_list.debt_foreign) + to_decimal(debitor.vesrdep)

                    if debitor.betrieb_gastmem != 0:

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                        if waehrung:
                            age_list.currency = waehrung.wabkurz
                else:
                    age_list.credit =  to_decimal(age_list.credit) - to_decimal(debitor.saldo)
                age_list.tot_debt =  to_decimal(age_list.tot_debt) + to_decimal(debitor.saldo)

        elif bill_name == "":

            for debitor in db_session.query(Debitor).filter(
                         (Debitor.artnr == temp_art2) & (Debitor.rgdatum <= bill_date) & (Debitor.opart < 2)).order_by(Debitor.zahlkonto, Debitor.rgdatum).all():

                if debitor.counter != 0:

                    age_list = query(age_list_data, filters=(lambda age_list: age_list.counter == debitor.counter), first=True)

                if not age_list or debitor.counter == 0:
                    age_list = Age_list()
                    age_list_data.append(age_list)

                    age_list.ar_recid = debitor._recid
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.rechnr = debitor.rechnr
                    age_list.refno = debitor.debref
                    age_list.gastnr = debitor.gastnr
                    age_list.gastnrmember = debitor.gastnrmember
                    age_list.zinr = debitor.zinr

                    guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})
                    age_list.billname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                    if guest:
                        age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    bill_line = get_cache (Bill_line, {"rechnr": [(eq, debitor.rechnr)],"betrag": [(eq, (- debitor.saldo))],"zeit": [(ge, (debitor.transzeit - 2)),(le, debitor.transzeit + 2)]})

                    bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)],"gastnr": [(eq, debitor.gastnr)]})

                    if bill:

                        if bill.reslinnr == 0:
                            age_list.resnr = bill.resnr
                            age_list.mbill = "*"

                    if matches(debitor.vesrcod,r"*resno:*"):

                        if num_entries(debitor.vesrcod, ";") == 1:
                            t_resnr = to_int(trim(entry(1, entry(0, debitor.vesrcod, ";") , ":")))


                        else:
                            t_name = trim(entry(0, debitor.vesrcod, ";"))
                            t_resnr = to_int(trim(entry(1, t_name, ":")))

                        reservation = get_cache (Reservation, {"resnr": [(eq, t_resnr)]})

                        res_line = get_cache (Res_line, {"resnr": [(eq, t_resnr)]})

                        if res_line:

                            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                            age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    if (matches(debitor.vesrcod,r"*;*")):
                        age_list.vouc_nr = trim(entry(1, debitor.vesrcod, ";"))
                        age_list.remarks = trim(entry(0, debitor.vesrcod, ";"))


                    else:
                        age_list.remarks = debitor.vesrcod

                        bill_line = get_cache (Bill_line, {"rechnr": [(eq, debitor.rechnr)],"betrag": [(eq, (- debitor.saldo))],"zeit": [(ge, (debitor.transzeit - 2)),(le, debitor.transzeit + 2)]})

                        if bill_line:
                            for i in range(1,(length(bill_line.bezeich))  + 1) :

                                if substring(bill_line.bezeich, i - 1, 1) == ("/").lower() :
                                    age_list.vouc_nr = substring(bill_line.bezeich, (i + 1) - 1, (length(bill_line.bezeich) - i))
                                    i = length(bill_line.bezeich)

                if debitor.zahlkonto == 0:

                    bediener = get_cache (Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                    if bediener:
                        age_list.user_init = bediener.userinit
                    age_list.rgdatum = debitor.rgdatum
                    age_list.debt =  to_decimal(age_list.debt) + to_decimal(debitor.saldo)
                    age_list.debt_foreign =  to_decimal(age_list.debt_foreign) + to_decimal(debitor.vesrdep)
                    disp_guest_debt()

                    if debitor.betrieb_gastmem != 0:

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                        if waehrung:
                            age_list.currency = waehrung.wabkurz
                else:
                    age_list.credit =  to_decimal(age_list.credit) - to_decimal(debitor.saldo)
                age_list.tot_debt =  to_decimal(age_list.tot_debt) + to_decimal(debitor.saldo)
        art_selected = 1

        if bill_saldo != 0:

            for age_list in query(age_list_data, filters=(lambda age_list: age_list.tot_debt != bill_saldo)):
                age_list_data.remove(age_list)

        pass


    def disp_guest_debt():

        nonlocal curr_art, age_list_data, t_debt_data, t_resnr, t_name, debitor, artikel, guest, bill_line, bill, bediener, waehrung, reservation, res_line
        nonlocal artnr, userinit, bill_nr, temp_art2, bill_date, bill_name, to_name, bill_saldo, art_selected, foutstand, outstand
        nonlocal abuff, debt, t_pay


        nonlocal t_debt, age_list, abuff, debt, t_pay, age_list1
        nonlocal t_debt_data, age_list_data

        gastnr:int = 0
        debt = None
        Age_list1 = Age_list
        age_list1_data = age_list_data
        Debt =  create_buffer("Debt",Debitor)
        age_list.b_resname = "Previous Payment Remark:"

        if debitor.counter != 0:
            age_list.b_resname = "Payment Remark:"

            for debt in db_session.query(Debt).filter(
                     (Debt.counter == debitor.counter) & (Debt.opart == 1)).order_by(Debt._recid).all():

                if debt.vesrcod != "":
                    age_list.b_resname = age_list.b_resname + chr_unicode(10) + to_string(debt.rgdatum) + " " + trim(to_string(debt.saldo, "->>>,>>>,>>9.99")) + ": " + debt.vesrcod

        if age_list.b_resname.lower()  == ("Payment Remark:").lower() :
            age_list.b_resname = ""
        else:
            age_list.b_resname = age_list.b_resname + chr_unicode(10) + chr_unicode(10)

        guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})
        age_list.b_resname = age_list.b_resname + guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1 + chr_unicode(10) + guest.adresse1 + chr_unicode(10) + guest.wohnort + " " + guest.plz


    create_age_list()

    debt_obj_list = {}
    for debt in db_session.query(Debt).filter(
             (Debt._recid.in_(list(set([abuff.ar_recid for abuff in abuff_data]))))).order_by(Debt._recid).all():
        if debt_obj_list.get(debt._recid):
            continue
        else:
            debt_obj_list[debt._recid] = True


        t_debt = T_debt()
        t_debt_data.append(t_debt)

        t_debt.t_debt_recid = debt._recid
        t_debt.rgdatum = debt.rgdatum

    for age_list in query(age_list_data):

        for t_pay in db_session.query(T_pay).filter(
                 (T_pay.artnr == temp_art2) & (T_pay.rechnr == age_list.rechnr) & (T_pay.counter == age_list.counter) & (T_pay.counter != 0) & (T_pay.opart < 2) & (T_pay.rgdatum > bill_date)).order_by(T_pay.zahlkonto, T_pay.rgdatum).all():

            if t_pay.zahlkonto > 0:
                age_list.credit =  to_decimal(age_list.credit) - to_decimal(t_pay.saldo)


            age_list.tot_debt =  to_decimal(age_list.tot_debt) + to_decimal(t_pay.saldo)

    return generate_output()