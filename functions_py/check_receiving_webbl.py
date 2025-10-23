#using conversion tools version: 1.0.0.117
# pyright: reportAttributeAccessIssue=false

"""_yusufwijasena_

    TICKET ID:
    ISSUE:  - fix definition variabel
            - fix python indentation
            - add type ignore to avoid warning 
            - activate model L_kredit & Fa_op
"""

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_kredit, L_op, L_artikel, L_lieferant, Queasy, Fa_artikel, Fa_op

def check_receiving_webbl(from_date:date, to_date:date, ref_no:string):

    prepare_cache ([L_kredit, L_op, Queasy, Fa_op])

    flag_dif = False
    output_list_data = []
    curr_pay = to_decimal("0.0")
    d:date 
    mon:int = 0
    art1:int = 0
    art2:int = 0
    fibu:string 
    ct:int = 0
    tot_vat = to_decimal("0.0")
    l_op = l_artikel = l_lieferant = fa_artikel = None
    l_kredit = L_kredit() 
    fa_op = Fa_op()
    queasy = Queasy()

    output_list = l_ap = None

    output_list_data, Output_list = create_model(
        "Output_list", {
            "datum":date, 
            "rcv_amount":Decimal, 
            "ap_amount":Decimal, 
            "diff":Decimal, 
            "flag_diff_rcv":bool, 
            "flag_diff_ap":bool
            }
        )

    L_ap = create_buffer("L_ap",L_kredit)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag_dif, output_list_data, curr_pay, d, mon, art1, art2, fibu, ct, tot_vat, l_kredit, l_op, l_artikel, l_lieferant, queasy, fa_artikel, fa_op
        nonlocal from_date, to_date, ref_no
        nonlocal l_ap


        nonlocal output_list, l_ap
        nonlocal output_list_data

        return {
            "flag_dif": flag_dif, 
            "output-list": output_list_data
        }

    l_op = get_cache (L_op, {
        "datum": [(ge, from_date),(le, from_date)]})

    if l_op:
        for d in date_range(from_date,to_date) :
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.datum = d 

            l_op_obj_list = {}
            for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
            (L_op.artnr >= 1000000) & (L_op.artnr <= 9999999) & (L_op.lief_nr > 0) & (L_op.datum == d) & (L_op.op_art <= 2) & (L_op.loeschflag <= 1)).order_by(L_lieferant.firma, L_op.datum, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                queasy = get_cache (Queasy, {
                    "key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],
                    "number1": [(eq, l_op.artnr)]})

                if queasy:
                    tot_vat =  to_decimal(l_op.warenwert + l_op.warenwert * queasy.deci1 / 100) 


                else:
                    tot_vat =  to_decimal(l_op.warenwert)
                
                tot_vat = to_decimal(round(tot_vat , 2))  # type: ignore round(tot_vat)
                
                output_list.rcv_amount =  to_decimal(Decimal(str(output_list.rcv_amount)) + Decimal(str(tot_vat)))   

    fa_op_obj_list = {}
    for fa_op, l_lieferant, fa_artikel in db_session.query(Fa_op, L_lieferant, Fa_artikel).join(L_lieferant,(L_lieferant.lief_nr == Fa_op.lief_nr)).join(Fa_artikel,(Fa_artikel.nr == Fa_op.nr)).filter(
    (Fa_op.anzahl != 0) & (Fa_op.loeschflag < 2) & (Fa_op.opart == 1) & (Fa_op.datum >= from_date) & (Fa_op.datum <= to_date)).order_by(Fa_op.lscheinnr).all():
        if fa_op_obj_list.get(fa_op._recid):
            continue
        else:
            fa_op_obj_list[fa_op._recid] = True

        output_list = query(output_list_data, filters=(lambda output_list: output_list.datum == fa_op.datum), first=True)

        if output_list:
            output_list.rcv_amount = to_decimal(output_list.rcv_amount + fa_op.warenwert) 
    l_kredit_obj_list = {}
    for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
    (L_kredit.lscheinnr != "") & (L_kredit.lief_nr > 0) & (L_kredit.zahlkonto == 0) & (L_kredit.opart <= 2) & (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.counter >= 0) & (L_kredit.netto != 0) & (L_kredit.steuercode == 0)).order_by(L_lieferant.firma, L_kredit.rgdatum).all():
        if l_kredit_obj_list.get(l_kredit._recid):
            continue
        else:
            l_kredit_obj_list[l_kredit._recid] = True

        l_op = get_cache (L_op, {
            "lscheinnr": [(eq, l_kredit.lscheinnr)]})

        if l_op:
            curr_pay =  to_decimal("0")

            if l_kredit.counter > 0:
                for l_ap in db_session.query(L_ap).filter(
                (L_ap.counter == l_kredit.counter) & (L_ap.zahlkonto > 0) & (L_ap.opart > 0)).order_by(L_ap.rgdatum).all():
                    curr_pay =  to_decimal(curr_pay - l_ap.saldo) 
            output_list = query(output_list_data, filters=(lambda output_list: output_list.datum == l_kredit.rgdatum), first=True)

            if output_list:
                if l_kredit.opart == 2:
                    output_list.ap_amount =  to_decimal(output_list.ap_amount + l_kredit.netto) 
                    
                else:
                    output_list.ap_amount =  to_decimal(output_list.ap_amount + (l_kredit.netto - curr_pay))

        fa_op = get_cache (Fa_op, {
            "lscheinnr": [(eq, l_kredit.lscheinnr)]})

        if fa_op:
            curr_pay =  to_decimal("0")

            if l_kredit.counter > 0:
                for l_ap in db_session.query(L_ap).filter(
                (L_ap.counter == l_kredit.counter) & (L_ap.zahlkonto > 0) & (L_ap.opart > 0)).order_by(L_ap.rgdatum).all():
                    curr_pay =  to_decimal(curr_pay - l_ap.saldo)  

            output_list = query(output_list_data, filters=(lambda output_list: output_list.datum == l_kredit.rgdatum), first=True)

            if output_list:
                if l_kredit.opart == 2:
                    output_list.ap_amount =  to_decimal(output_list.ap_amount + l_kredit.netto)  

                else:
                    output_list.ap_amount =  to_decimal(output_list.ap_amount + (l_kredit.netto - curr_pay))  

    for output_list in query(output_list_data):  # type: ignore output list data belum terisi

        if output_list.rcv_amount > output_list.ap_amount:
            output_list.flag_diff_ap = True

        if output_list.rcv_amount < output_list.ap_amount:
            output_list.flag_diff_rcv = True
        output_list.diff = to_decimal(round(output_list.rcv_amount , 2) - round(output_list.ap_amount , 2))

        if int(str(output_list.diff)) != 0:  
            flag_dif = True
        pass

    if not flag_dif:

        queasy = get_cache (Queasy, {
            "key": [(eq, 331)],
            "char1": [(eq, ref_no)],
            "char2": [(eq, "inv-cek reciving")]})

        if not queasy:
            queasy.key = 331
            queasy.char1 = ref_no
            queasy.char2 = "Inv-Cek Reciving"
            queasy.char3 = "yes"
            
            db_session.add(queasy)

    return generate_output()