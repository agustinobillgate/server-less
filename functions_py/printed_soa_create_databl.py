#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 21/8/2025
# search receiever, perlu tambahan char \ufff
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from datetime import date
from models import Bill, Debitor, Guest, Hoteldpt, H_bill

def printed_soa_create_databl(invno:int, from_name:string, to_name:string, from_date:date, to_date:date):

    prepare_cache ([Bill, Debitor, Guest, Hoteldpt, H_bill])

    s_list_data = []
    bill = debitor = guest = hoteldpt = h_bill = None

    s_list = sbuff = None

    s_list_data, S_list = create_model("S_list", {"invstr":string, "deptstr":string, "deptnr":int, "gname":string, "receiver":string, "ggastnr":int, "rgastnr":int, "rechnr":int, "refnr":int, "prdate":date, "saldo":Decimal, "bill_date":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_data, bill, debitor, guest, hoteldpt, h_bill
        nonlocal invno, from_name, to_name, from_date, to_date


        nonlocal s_list, sbuff
        nonlocal s_list_data

        return {"s-list": s_list_data}

    def create_data():

        nonlocal s_list_data, bill, debitor, guest, hoteldpt, h_bill
        nonlocal invno, from_name, to_name, from_date, to_date


        nonlocal s_list, sbuff
        nonlocal s_list_data

        curr_ref:int = 0
        do_it:bool = False
        prdate:date = None
        Sbuff = S_list
        sbuff_data = s_list_data
        sbuff_data.clear()
        from_name = from_name.strip()
        to_name = to_name.strip()
        to_name = to_name + "\uffff"
        low_from = from_name.lower()
        low_to   = (to_name).lower()  
        if invno != 0:

            debitor_obj_list = {}
            debitor = Debitor()
            bill = Bill()
            for debitor.name, debitor.gastnr, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.saldo, debitor.betriebsnr, debitor._recid, bill.logidat, bill._recid in db_session.query(Debitor.name, Debitor.gastnr, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.saldo, Debitor.betriebsnr, Debitor._recid, Bill.logidat, Bill._recid).join(Bill,(Bill.rechnr == Debitor.rechnr) & (Bill.logidat >= from_date) & (Bill.logidat <= to_date)).filter(
                     (Debitor.debref > 0) & (Debitor.debref == invno) & (Debitor.betriebsnr == 0) & 
                    #  (Debitor.name >= (from_name).lower()) & 
                    #  (Debitor.name <= (to_name).lower())
                    (func.lower(Debitor.name) >= (from_name).lower()) & 
                    (func.lower(Debitor.name) <= (to_name).lower())
                     ).order_by(Debitor.debref).all():
                if debitor_obj_list.get(debitor._recid):
                    continue
                else:
                    debitor_obj_list[debitor._recid] = True

                if debitor.name.lower()  >= (from_name).lower()  and debitor.name.lower()  <= (to_name).lower() :

                    s_list = query(s_list_data, filters=(lambda s_list: s_list.deptnr == 0 and s_list.rgastnr == debitor.gastnr and s_list.rechnr == debitor.rechnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.deptnr = 0
                    s_list.rechnr = debitor.rechnr
                    s_list.rgastnr = debitor.gastnr
                    s_list.refnr = debitor.debref
                    s_list.prdate = bill.logidat
                    s_list.bill_date = debitor.rgdatum

                    guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})

                    if guest:
                        s_list.receiver = guest.name + " " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                    if guest:
                        s_list.gname = guest.name + " " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, 0)]})

                    if hoteldpt:
                        s_list.deptstr = hoteldpt.depart
                s_list.saldo =  to_decimal(s_list.saldo) + to_decimal(debitor.saldo)
                curr_ref = debitor.debref
            curr_ref = 0

            debitor_obj_list = {}
            debitor = Debitor()
            h_bill = H_bill()
            
            for debitor.name, debitor.gastnr, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.saldo, debitor.betriebsnr, debitor._recid, h_bill.service, h_bill._recid in db_session.query(Debitor.name, Debitor.gastnr, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.saldo, Debitor.betriebsnr, Debitor._recid, H_bill.service, H_bill._recid).join(H_bill,(H_bill.rechnr == Debitor.rechnr) & (H_bill.departement == Debitor.betriebsnr)).filter(
                     (Debitor.debref > 0) & (Debitor.debref == invno) & (Debitor.betriebsnr > 0) & 
                     #  (Debitor.name >= (from_name).lower()) & 
                     #  (Debitor.name <= (to_name).lower())
                    (func.lower(Debitor.name) >= (from_name).lower()) & 
                    (func.lower(Debitor.name) <= (to_name).lower())
                     ).order_by(Debitor.debref).all():
                if debitor_obj_list.get(debitor._recid):
                    continue
                else:
                    debitor_obj_list[debitor._recid] = True


                do_it = False

                if length(to_string(h_bill.service[6])) == 8:
                    prdate = date_mdy(to_int(substring(to_string(h_bill.service[6]) , 0, 2)) , to_int(substring(to_string(h_bill.service[6]) , 2, 2)) , to_int(substring(to_string(h_bill.service[6]) , 4, 4)))

                elif length(to_string(h_bill.service[6])) == 7:
                    prdate = date_mdy(to_int(substring(to_string(h_bill.service[6]) , 0, 1)) , to_int(substring(to_string(h_bill.service[6]) , 1, 2)) , to_int(substring(to_string(h_bill.service[6]) , 3, 4)))

                if prdate >= from_date and prdate <= to_date:
                    do_it = True
                else:
                    do_it = False

                if do_it:

                    s_list = query(s_list_data, filters=(lambda s_list: s_list.deptnr == debitor.betriebsnr and s_list.rgastnr == debitor.gastnr and s_list.rechnr == debitor.rechnr), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_data.append(s_list)

                        s_list.deptnr = debitor.betriebsnr
                        s_list.rechnr = debitor.rechnr
                        s_list.rgastnr = debitor.gastnr
                        s_list.refnr = debitor.debref
                        s_list.prdate = prdate
                        s_list.bill_date = debitor.rgdatum

                        guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})

                        if guest:
                            s_list.receiver = guest.name + " " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                        guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                        if guest:
                            s_list.gname = guest.name + " " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, debitor.betriebsnr)]})

                        if hoteldpt:
                            s_list.deptstr = hoteldpt.depart
                    s_list.saldo =  to_decimal(s_list.saldo) + to_decimal(debitor.saldo)
                    curr_ref = debitor.debref
        else:
            print("invno:0")
            debitor_obj_list = {}
            debitor = Debitor()
            bill = Bill()
            for debitor.name, debitor.gastnr, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.saldo, debitor.betriebsnr, debitor._recid, bill.logidat, bill._recid in db_session.query(Debitor.name, Debitor.gastnr, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.saldo, Debitor.betriebsnr, Debitor._recid, Bill.logidat, Bill._recid).join(Bill,(Bill.rechnr == Debitor.rechnr) & (Bill.logidat >= from_date) & (Bill.logidat <= to_date)).filter(
                        (Debitor.debref > 0) & (Debitor.betriebsnr == 0) & 
                        #  (Debitor.name >= (from_name).lower()) & 
                        #  (Debitor.name <= (to_name).lower())
                        (func.lower(Debitor.name) >= low_from) &
                        (func.lower(Debitor.name) <= low_to)
                    ).order_by(Debitor.debref).all():
                if debitor_obj_list.get(debitor._recid):
                    continue
                else:
                    debitor_obj_list[debitor._recid] = True

                s_list = query(s_list_data, filters=(lambda s_list: s_list.deptnr == 0 and s_list.rgastnr == debitor.gastnr and s_list.rechnr == debitor.rechnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.deptnr = 0
                    s_list.rechnr = debitor.rechnr
                    s_list.rgastnr = debitor.gastnr
                    s_list.refnr = debitor.debref
                    s_list.prdate = bill.logidat
                    s_list.bill_date = debitor.rgdatum

                    guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})

                    if guest:
                        s_list.receiver = guest.name + " " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                    if guest:
                        s_list.gname = guest.name + " " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, 0)]})

                    if hoteldpt:
                        s_list.deptstr = hoteldpt.depart
                s_list.saldo =  to_decimal(s_list.saldo) + to_decimal(debitor.saldo)
                curr_ref = debitor.debref
            curr_ref = 0

            debitor_obj_list = {}
            debitor = Debitor()
            h_bill = H_bill()
            for debitor.name, debitor.gastnr, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.saldo, debitor.betriebsnr, debitor._recid, h_bill.service, h_bill._recid in db_session.query(Debitor.name, Debitor.gastnr, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.saldo, Debitor.betriebsnr, Debitor._recid, H_bill.service, H_bill._recid).join(H_bill,(H_bill.rechnr == Debitor.rechnr) & (H_bill.departement == Debitor.betriebsnr)).filter(
                        (Debitor.debref > 0) & (Debitor.betriebsnr > 0) & 
                        #  (Debitor.name >= (from_name).lower()) & 
                        #  (Debitor.name <= (to_name).lower())
                        (func.lower(Debitor.name) >= (from_name).lower()) & 
                        (func.lower(Debitor.name) <= (to_name).lower())
                        ).order_by(Debitor.debref).all():
                if debitor_obj_list.get(debitor._recid):
                    continue
                else:
                    debitor_obj_list[debitor._recid] = True


                do_it = False

                if length(to_string(h_bill.service[6])) == 8:
                    prdate = date_mdy(to_int(substring(to_string(h_bill.service[6]) , 0, 2)) , to_int(substring(to_string(h_bill.service[6]) , 2, 2)) , to_int(substring(to_string(h_bill.service[6]) , 4, 4)))

                elif length(to_string(h_bill.service[6])) == 7:
                    prdate = date_mdy(to_int(substring(to_string(h_bill.service[6]) , 0, 1)) , to_int(substring(to_string(h_bill.service[6]) , 1, 2)) , to_int(substring(to_string(h_bill.service[6]) , 3, 4)))

                if prdate >= from_date and prdate <= to_date:
                    do_it = True
                else:
                    do_it = False

                if do_it:

                    s_list = query(s_list_data, filters=(lambda s_list: s_list.deptnr == debitor.betriebsnr and s_list.rgastnr == debitor.gastnr and s_list.rechnr == debitor.rechnr), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_data.append(s_list)

                        s_list.deptnr = debitor.betriebsnr
                        s_list.rechnr = debitor.rechnr
                        s_list.rgastnr = debitor.gastnr
                        s_list.refnr = debitor.debref
                        s_list.prdate = prdate
                        s_list.bill_date = debitor.rgdatum

                        guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})

                        if guest:
                            s_list.receiver = guest.name + " " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                        guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                        if guest:
                            s_list.gname = guest.name + " " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, debitor.betriebsnr)]})

                        if hoteldpt:
                            s_list.deptstr = hoteldpt.depart
                    s_list.saldo =  to_decimal(s_list.saldo) + to_decimal(debitor.saldo)
                    curr_ref = debitor.debref
        curr_ref = 0

        for sbuff in query(sbuff_data, sort_by=[("refnr",False)]):

            if curr_ref == 0 or curr_ref != sbuff.refnr:
                sbuff.invstr = to_string(sbuff.refnr, "9999999")


            curr_ref = sbuff.refnr

    create_data()

    return generate_output()