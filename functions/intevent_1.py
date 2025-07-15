#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.htpchar import htpchar
from functions.i_intevent_1 import i_intevent_1
from functions.htplogic import htplogic
from models import Res_line, Htparam, Nightaudit, Interface

def intevent_1(ev_type:int, zinr:string, parms:string, resno:int, reslinno:int):

    prepare_cache ([Htparam, Interface])

    doevent:bool = False
    do_it:bool = False
    parms_mapping:string = ""
    chdoevent:string = ""
    chardoevent:string = ""
    parms_flag:string = ""
    progname:string = "nt-custom-emailtrigger.r"
    res_line = htparam = nightaudit = interface = None

    res_line1 = None

    Res_line1 = create_buffer("Res_line1",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal doevent, do_it, parms_mapping, chdoevent, chardoevent, parms_flag, progname, res_line, htparam, nightaudit, interface
        nonlocal ev_type, zinr, parms, resno, reslinno
        nonlocal res_line1


        nonlocal res_line1

        return {}


    if num_entries(parms) > 1:

        if entry(0, parms, ";") == ("Activate!").lower() :
            parms_mapping = "My Checkin!"

        elif entry(0, parms, ";") == ("Manual Checkin!").lower() :
            parms_mapping = "My Checkin!"

        elif entry(0, parms, ";") == ("Deactivate!").lower() :
            parms_mapping = "My Checkout!"

        elif entry(0, parms, ";") == ("Manual Checkout!").lower() :
            parms_mapping = "My Checkout!"
        else:
            parms_mapping = entry(0, parms, ";")
        parms_flag = entry(1, parms, ";")
    else:

        if parms.lower()  == ("Activate!").lower() :
            parms_mapping = "My Checkin!"

        elif parms.lower()  == ("Manual Checkin!").lower() :
            parms_mapping = "My Checkin!"

        elif parms.lower()  == ("Deactivate!").lower() :
            parms_mapping = "My Checkout!"

        elif parms.lower()  == ("Manual Checkout!").lower() :
            parms_mapping = "My Checkout!"
        else:
            parms_mapping = parms
        parms_flag = ""

    if parms.lower()  != ("Priscilla").lower()  and parms.lower()  != ("Loyalty").lower()  and parms.lower()  != ("newgcf").lower()  and parms.lower()  != ("closemonth").lower() :

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

        if res_line:

            res_line1 = db_session.query(Res_line1).filter(
                     (Res_line1.active_flag == 1) & ((Res_line1.resstatus == 6) | (Res_line1.resstatus == 13)) & (Res_line1.zinr == res_line.zinr) & (Res_line1.l_zuordnung[inc_value(2)] == 0) & (Res_line1._recid != res_line._recid)).first()
        chardoevent = get_output(htpchar(341))

        if matches(chardoevent,r"*nettify*"):

            if res_line1:

                res_line1 = db_session.query(Res_line1).filter(
                         (Res_line1.active_flag == 1) & (Res_line1.resstatus == 11) & (Res_line1.zinr == res_line.zinr) & (Res_line1.l_zuordnung[inc_value(2)] == 0) & (Res_line1._recid != res_line._recid) & (Res_line1.reslinnr != res_line.reslinnr)).first()

        if parms.lower()  == ("My Checkin!").lower()  or parms.lower()  == ("My Checkout!").lower() :
            do_it = not None != res_line1
        else:
            do_it = True

        if do_it:
            get_output(i_intevent_1(39, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno))

            if parms_flag.lower()  == ("PABX").lower() :
                doevent = get_output(htplogic(398))

                if doevent:
                    get_output(i_intevent_1(2, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno))

            if matches(parms_flag,r"*WIFI*"):
                chardoevent = get_output(htpchar(341))

                if chardoevent != "":
                    get_output(i_intevent_1(9, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno))

            if parms_flag == "":
                doevent = get_output(htplogic(398))

                if doevent:
                    get_output(i_intevent_1(2, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno))
                chardoevent = get_output(htpchar(341))

                if chardoevent != "":
                    get_output(i_intevent_1(9, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno))
            doevent = get_output(htplogic(358))

            if doevent and ev_type >= 1 and ev_type <= 3:
                get_output(i_intevent_1(4, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno))

            htparam = get_cache (Htparam, {"paramnr": [(eq, 1070)]})

            if htparam.flogical and htparam.feldtyp == 4 and ev_type >= 1 and ev_type <= 3:
                get_output(i_intevent_1(6, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno))

        htparam = get_cache (Htparam, {"paramnr": [(eq, 249)]})

        if htparam.flogical and htparam.paramgruppe == 6 and ev_type >= 1 and ev_type <= 3:

            nightaudit = get_cache (Nightaudit, {"programm": [(eq, progname)]})

            if nightaudit:

                if nightaudit.selektion:
                    pass
                else:
                    get_output(i_intevent_1(7, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno))

            elif not nightaudit:
                get_output(i_intevent_1(7, ev_type, zinr, parms_mapping, zinr, 0, resno, reslinno))
        doevent = get_output(htplogic(359))

        if doevent:
            get_output(i_intevent_1(3, ev_type, zinr, parms, zinr, 0, resno, reslinno))
            get_output(i_intevent_1(33, ev_type, zinr, parms, zinr, 0, resno, reslinno))

    if parms.lower()  == ("newgcf").lower() :
        get_output(i_intevent_1(36, ev_type, zinr, parms, zinr, 0, resno, reslinno))

    if parms.lower()  == ("closemonth").lower() :
        get_output(i_intevent_1(37, ev_type, zinr, parms, zinr, 0, resno, reslinno))

    if parms.lower()  == ("Loyalty").lower() :

        if ev_type == 1:
            DO
            interface = Interface()
            db_session.add(interface)

            interface.key = 11
            interface.zinr = zinr
            interface.nebenstelle = ""
            interface.intfield = 0
            interface.decfield =  to_decimal(ev_type)
            interface.int_time = get_current_time_in_seconds()
            interface.intdate = get_current_date()
            interface.parameters = "newbill"
            interface.resnr = resno
            interface.reslinnr = reslinno


            pass
            pass

    if parms.lower()  == ("Priscilla").lower() :

        if ev_type == 1:
            get_output(i_intevent_1(10, ev_type, zinr, 'checkin', '', 0, resno, reslinno))

        elif ev_type == 2:
            get_output(i_intevent_1(10, ev_type, zinr, 'checkout', '', 0, resno, reslinno))

        elif ev_type == 9:
            get_output(i_intevent_1(10, ev_type, zinr, 'modify', '', 0, resno, reslinno))

        elif ev_type == 10:
            get_output(i_intevent_1(10, ev_type, zinr, 'qci', '', 0, resno, reslinno))

        elif ev_type == 11:
            get_output(i_intevent_1(10, ev_type, zinr, 'insert', '', 0, resno, reslinno))

        elif ev_type == 12:
            get_output(i_intevent_1(10, ev_type, zinr, 'new', '', 0, resno, reslinno))

        elif ev_type == 13:
            get_output(i_intevent_1(10, ev_type, zinr, 'split', '', 0, resno, reslinno))

        elif ev_type == 14:
            get_output(i_intevent_1(10, ev_type, zinr, 'cancel', '', 0, resno, reslinno))

        elif ev_type == 15:
            get_output(i_intevent_1(10, ev_type, zinr, 'delete', '', 0, resno, reslinno))

    if parms.lower()  == ("bridge").lower() :

        if ev_type == 1:
            get_output(i_intevent_1(11, ev_type, zinr, 'generalledger', '', 0, resno, reslinno))

        elif ev_type == 2:
            get_output(i_intevent_1(11, ev_type, zinr, 'checkout', '', 0, resno, reslinno))

        elif ev_type == 9:
            get_output(i_intevent_1(11, ev_type, zinr, 'modify', '', 0, resno, reslinno))

        elif ev_type == 10:
            get_output(i_intevent_1(11, ev_type, zinr, 'qci', '', 0, resno, reslinno))

        elif ev_type == 11:
            get_output(i_intevent_1(11, ev_type, zinr, 'insert', '', 0, resno, reslinno))

        elif ev_type == 12:
            get_output(i_intevent_1(11, ev_type, zinr, 'new', '', 0, resno, reslinno))

        elif ev_type == 13:
            get_output(i_intevent_1(11, ev_type, zinr, 'split', '', 0, resno, reslinno))

        elif ev_type == 14:
            get_output(i_intevent_1(11, ev_type, zinr, 'cancel', '', 0, resno, reslinno))

        elif ev_type == 15:
            get_output(i_intevent_1(11, ev_type, zinr, 'delete', '', 0, resno, reslinno))
    doevent = get_output(htplogic(298))

    if doevent:

        if ev_type == 9:
            get_output(i_intevent_1(38, ev_type, zinr, 'modify', '', 0, resno, reslinno))

        elif ev_type == 10:
            get_output(i_intevent_1(38, ev_type, zinr, 'qci', '', 0, resno, reslinno))

        elif ev_type == 11:
            get_output(i_intevent_1(38, ev_type, zinr, 'insert', '', 0, resno, reslinno))

        elif ev_type == 12:
            get_output(i_intevent_1(38, ev_type, zinr, 'new', '', 0, resno, reslinno))

        elif ev_type == 13:
            get_output(i_intevent_1(38, ev_type, zinr, 'split', '', 0, resno, reslinno))

        elif ev_type == 14:
            get_output(i_intevent_1(38, ev_type, zinr, 'cancel', '', 0, resno, reslinno))

        elif ev_type == 15:
            get_output(i_intevent_1(38, ev_type, zinr, 'delete', '', 0, resno, reslinno))
        else:
            get_output(i_intevent_1(38, ev_type, zinr, parms, zinr, 0, resno, reslinno))

    return generate_output()