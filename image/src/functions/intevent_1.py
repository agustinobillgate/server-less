from functions.additional_functions import *
import decimal, traceback
from functions.htpchar import htpchar
import re
from functions.htplogic import htplogic
from functions.i_intevent_1 import i_intevent_1

from sqlalchemy import func
from models import Res_line, Htparam, Nightaudit, Interface

def intevent_1(ev_type:int, zinr:str, parms:str, resno:int, reslinno:int):
    doevent:bool = False
    do_it:bool = False
    parms_mapping:str = ""
    chdoevent:str = ""
    chardoevent:str = ""
    parms_flag:str = ""
    progname:str = "nt_custom_emailtrigger.r"
    ires_line = htparam = nightaudit = interface = None

    res_line1 = None

    Res_line1 = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal doevent, do_it, parms_mapping, chdoevent, chardoevent, parms_flag, progname, ires_line, htparam, nightaudit, interface
        nonlocal res_line1
        nonlocal res_line1
        return {"empty": "empty"}

    local_storage.debugging = local_storage.debugging + ",Parms:" + parms + ",33"
    try:
        if num_entries(parms, ",") > 1:

            if entry(0, parms, ";") == "Activate!".lower():
                parms_mapping = "My Checkin!"

            elif entry(0, parms, ";") == "Manual Checkin!".lower():
                parms_mapping = "My Checkin!"

            elif entry(0, parms, ";") == "Deactivate!".lower():
                parms_mapping = "My Checkout!"

            elif entry(0, parms, ";") == "Manual Checkout!".lower():
                parms_mapping = "My Checkout!"
            else:
                parms_mapping = entry(0, parms, ";")
            parms_flag = entry(1, parms, ";")
        else:
            local_storage.debugging = local_storage.debugging + ",52"
            if parms.lower()  == "Activate!".lower():
                parms_mapping = "My Checkin!"

            elif parms.lower()  == "Manual Checkin!".lower():
                parms_mapping = "My Checkin!"

            elif parms.lower()  == "Deactivate!".lower():
                parms_mapping = "My Checkout!"

            elif parms.lower()  == "Manual Checkout!".lower():
                parms_mapping = "My Checkout!"
            else:
                parms_mapping = parms
            parms_flag = ""
        local_storage.debugging = local_storage.debugging + ",ParMap:" + parms_mapping
        if (parms.lower()  != "Priscilla".lower() 
                and parms.lower()  != "Loyalty".lower() 
                and parms.lower()  != "newgcf" 
                and parms.lower()  != "closemonth"
            ):

            ires_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == resno) &  
                        (Res_line.reslinnr == reslinno)
                    ).first()
            
            if ires_line:
                local_storage.debugging = local_storage.debugging + ",iResline:" + str(resno)
                res_line1 = db_session.query(Res_line1).filter(
                        (Res_line1.active_flag == 1) &
                        ((Res_line1.resstatus == 6) |  (Res_line1.resstatus == 13)) &  
                        (Res_line1.zinr == ires_line.zinr) &  
                        (Res_line1.l_zuordnung[2] == 0) &  
                        (Res_line1._recid != ires_line._recid)
                        ).first()

                chardoevent = get_output(htpchar(341))
                local_storage.debugging = local_storage.debugging + ",chardoevent:" + chardoevent
                if re.match(".*nettify.*",chardoevent):
                    res_line1 = db_session.query(Res_line1).filter(
                            (Res_line1.active_flag == 1) &  
                            (Res_line1.resstatus == 11) &  
                            (Res_line1.zinr == ires_line.zinr) &  
                            (Res_line1.l_zuordnung[2] == 0) &  
                            (Res_line1._recid != ires_line._recid) &  
                            (Res_line1.reslinnr != ires_line.reslinnr)
                            ).first()

                    # if res_line1:
                    #     local_storage.debugging = local_storage.debugging + ",ada Res_line1"
                        
                    # else:
                    #     local_storage.debugging = local_storage.debugging + ",no res_line1" 
                if parms.lower()  == "My Checkin!".lower() or parms.lower()  == "My Checkout!".lower():
                    do_it = False
                    # do_it = res_line1 is None
                else:
                    do_it = True
                local_storage.debugging = local_storage.debugging + ",DoIt:" + str(do_it)
                if do_it:
                    local_storage.debugging = local_storage.debugging + ",110:parms_flag:" + parms_flag
                    #  {intevent-1.i 39 ev_type zinr parms_mapping zinr 0 resno reslinno} /*Digital First - Trigger Checkin*/      
                    i_intevent_1(39, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno)
                    if parms_flag.lower()  == "PABX".lower():
                        doevent = get_output(htplogic(398))

                        if doevent:
                            # /* 2 = Telephone */
                            i_intevent_1(2, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno)
                            

                    if re.match(".*WIFI.*".lower(),parms_flag):
                        chardoevent = get_output(htpchar(341))
                        if chardoevent != "":
                            # {intevent-1.i 9 ev-type zinr parms-mapping zinr 0 resNo reslinNo} /* 9 = WiFi */
                            i_intevent_1(9, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno)
                            

                    if parms_flag == "":
                        doevent = get_output(htplogic(398))
                        if doevent:
                            # /* 2 = Telephone */
                            i_intevent_1(2, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno)
                            
                        chardoevent = get_output(htpchar(341))
                        if chardoevent != "":
                            i_intevent_1(9, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno)

                    doevent = get_output(htplogic(358))
                    if doevent and ev_type >= 1 and ev_type <= 3:
                        # /* 4 = Internet Billing */
                        i_intevent_1(4, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno)

                    htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == 1070)).first()
                    if htparam:
                        if htparam.flogical and htparam.feldtyp == 4 and ev_type >= 1 and ev_type <= 3:
                            # /* 6 = Voice-Box System */
                            i_intevent_1(6, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno)

            htparam = db_session.query(Htparam).filter((Htparam.paramnr == 249)).first()
            if htparam:
                if (htparam.flogical and htparam.paramgruppe == 6 and ev_type >= 1 and ev_type <= 3):
                    nightaudit = db_session.query(Nightaudit).filter(
                            (func.lower(Nightaudit.programm) == (progname).lower())).first()

                    if nightaudit:
                        if nightaudit.selektion:
                            pass
                        else:
                            #  /* 7 = Greeting Email */
                            i_intevent_1(7, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno)
                    elif not nightaudit:
                        #  /* 7 = Greeting Email */
                        i_intevent_1(7, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno)

            doevent = get_output(htplogic(359))
            if doevent:
                # {intevent-1.i 3 ev-type zinr parms zinr 0 resNo reslinNo} /* 3 = SelectTV */
                # {intevent-1.i 33 ev-type zinr parms zinr 0 resNo reslinNo} /* 3 = SelectTV */
                i_intevent_1(3, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno)
                i_intevent_1(33, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno)

        # /* tambahan untuk GuestProfile Chrondigital (Damien Lee) CRG 23Nov18 */
        if parms.lower()  == "newgcf".lower():
            # {intevent-1.i 36 ev-type zinr parms zinr 0 resNo reslinNo}
            i_intevent_1(36, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno)
        
        # /* Request Tauzia, GL close month trigger CRG 11Sept20 */
        if parms.lower()  == "closemonth".lower():
            i_intevent_1(37, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno)

        if parms.lower()  == "Loyalty".lower():
            if ev_type == 1:
                
                interface = Interface()
                db_session.add(interface)

                interface.key = 11
                interface.zinr = zinr
                interface.nebenstelle = ""
                interface.intfield = 0
                interface.decfield = ev_type
                interface.int_time = get_current_time_in_seconds()
                interface.intdate = get_current_date()
                interface.parameters = "newbill"
                interface.resnr = resno
                interface.reslinnr = reslinno

                interface = db_session.query(Interface).first()

        if parms.lower()  == "Priscilla".lower():
            if ev_type == 1:
                i_intevent_1(10, ev_type, zinr, 'checkin', '' , 0, resno, reslinno)

            elif ev_type == 2:
                i_intevent_1(10, ev_type, zinr, 'checkout', '' , 0, resno, reslinno)
            elif ev_type == 9:
                i_intevent_1(10, ev_type, zinr, 'modify', '' , 0, resno, reslinno)
            elif ev_type == 10:
                i_intevent_1(10, ev_type, zinr, 'qci', '' , 0, resno, reslinno)
            elif ev_type == 11:
                i_intevent_1(10, ev_type, zinr, 'insert', '' , 0, resno, reslinno)
            elif ev_type == 12:
                i_intevent_1(10, ev_type, zinr, 'new', '' , 0, resno, reslinno)
            elif ev_type == 13:
                i_intevent_1(10, ev_type, zinr, 'split', '' , 0, resno, reslinno)
            elif ev_type == 14:
                i_intevent_1(10, ev_type, zinr, 'cancel', '' , 0, resno, reslinno)
            elif ev_type == 15:
                i_intevent_1(10, ev_type, zinr, 'delete', '' , 0, resno, reslinno)

        if parms.lower()  == "bridge".lower():
            if ev_type == 1:
                i_intevent_1(11, ev_type, zinr, 'generalledger', '' , 0, resno, reslinno)

            elif ev_type == 2:
                i_intevent_1(11, ev_type, zinr, 'checkout', '' , 0, resno, reslinno)

            elif ev_type == 9:
                i_intevent_1(11, ev_type, zinr, 'modify', '' , 0, resno, reslinno)

            elif ev_type == 10:
                i_intevent_1(11, ev_type, zinr, 'qci', '' , 0, resno, reslinno)

            elif ev_type == 11:
                i_intevent_1(11, ev_type, zinr, 'insert', '' , 0, resno, reslinno)

            elif ev_type == 12:
                i_intevent_1(11, ev_type, zinr, 'new', '' , 0, resno, reslinno)

            elif ev_type == 13:
                i_intevent_1(11, ev_type, zinr, 'split', '' , 0, resno, reslinno)

            elif ev_type == 14:
                i_intevent_1(11, ev_type, zinr, 'cancel', '' , 0, resno, reslinno)

            elif ev_type == 15:
                i_intevent_1(11, ev_type, zinr, 'delete', '' , 0, resno, reslinno)

    except Exception as e:
        error_message = traceback.format_exc()
        print("Error:", error_message)
        
    local_storage.debugging = local_storage.debugging + ",252"
    return generate_output()