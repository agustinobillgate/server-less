from functions.additional_functions import *
import decimal
from models import Mc_guest, Mc_types, Mc_cardhis, Mc_fee, Mc_aclub

g_list_list, G_list = create_model_like(Mc_guest)

def mc_gcf0bl(g_list_list:[G_list], curr_mode:str, user_init:str, gastno:int):
    mc_guest = mc_types = mc_cardhis = mc_fee = mc_aclub = None

    g_list = tbuff = mcbuff = None

    Tbuff = create_buffer("Tbuff",Mc_types)
    Mcbuff = create_buffer("Mcbuff",Mc_aclub)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mc_guest, mc_types, mc_cardhis, mc_fee, mc_aclub
        nonlocal curr_mode, user_init, gastno
        nonlocal tbuff, mcbuff

        nonlocal g_list, tbuff, mcbuff
        nonlocal g_list_list
        return {}

    def create_mcfee():

        nonlocal mc_guest, mc_types, mc_cardhis, mc_fee, mc_aclub
        nonlocal curr_mode, user_init, gastno
        nonlocal tbuff, mcbuff


        nonlocal g_list, tbuff, mcbuff
        nonlocal g_list_list

        if not mc_types or not(mc_types.nr == g_list.nr):
            mc_types = db_session.query(Mc_types).filter(
                (Mc_types.nr == g_list.nr)).first()

        if mc_types.joinfee == 0:

            return
        mc_fee = Mc_fee()
        db_session.add(mc_fee)

        mc_fee.key = 1
        mc_fee.nr = g_list.nr
        mc_fee.gastnr = gastno
        mc_fee.betrag =  to_decimal(mc_types.joinfee)
        mc_fee.von_datum = g_list.fdate
        mc_fee.bis_datum = g_list.tdate


    def fill_mc_guest():

        nonlocal mc_guest, mc_types, mc_cardhis, mc_fee, mc_aclub
        nonlocal curr_mode, user_init, gastno
        nonlocal tbuff, mcbuff


        nonlocal g_list, tbuff, mcbuff
        nonlocal g_list_list


        buffer_copy(g_list, mc_guest)


    if not g_list:
        g_list = query(g_list_list, first=True)

    if curr_mode.lower()  == ("new").lower() :
        mc_guest = Mc_guest()
        db_session.add(mc_guest)

        fill_mc_guest()
        mc_guest.userinit = user_init


        create_mcfee()

    elif curr_mode.lower()  == ("chg").lower() :

        if not mc_guest or not(mc_guest.gastnr == gastno):
            mc_guest = db_session.query(Mc_guest).filter(
                    (Mc_guest.gastnr == gastno)).first()

        if not mc_types or not(mc_types.nr == g_list.nr):
            mc_types = db_session.query(Mc_types).filter(
                    (Mc_types.nr == g_list.nr)).first()

        if not tbuff or not(tbuff.nr == mc_guest.nr):
            tbuff = db_session.query(Tbuff).filter(
                    (Tbuff.nr == mc_guest.nr)).first()

        if g_list.cardnum != mc_guest.cardnum:
            mc_cardhis = Mc_cardhis()
            db_session.add(mc_cardhis)

            mc_cardhis.gastnr = gastno
            mc_cardhis.old_card = mc_guest.cardnum
            mc_cardhis.new_card = g_list.cardnum
            mc_cardhis.old_nr = mc_guest.nr
            mc_cardhis.new_nr = g_list.nr
            mc_cardhis.zeit = get_current_time_in_seconds()
            mc_cardhis.userinit = user_init

        if (g_list.fdate != mc_guest.fdate) or (g_list.tdate != mc_guest.tdate):

            if not mc_fee or not(mc_fee.key == 1 and mc_fee.gastnr == gastno and mc_fee.von_datum == mc_guest.fdate and mc_fee.bis_datum == mc_guest.tdate):
                mc_fee = db_session.query(Mc_fee).filter(
                        (Mc_fee.key == 1) &  
                        (Mc_fee.gastnr == gastno) &  
                        (Mc_fee.von_datum == mc_guest.fdate) &  
                        (Mc_fee.bis_datum == mc_guest.tdate)
                        ).first()

            if mc_fee:
                mc_fee.von_datum = g_list.fdate
                mc_fee.bis_datum = g_list.tdate

        if g_list.activeflag != mc_guest.activeflag and tbuff.bezeich.lower()  == ("THE ONE").lower() :

            if not mc_aclub or not(mc_aclub.key == mc_types.nr and mc_aclub.cardnum == mc_guest.cardnum):
                mc_aclub = db_session.query(Mc_aclub).filter(
                        (Mc_aclub.key == mc_types.nr) &  
                        (Mc_aclub.cardnum == mc_guest.cardnum)
                        ).first()

            if mc_aclub:
                mc_aclub.logi1 = not g_list.activeflag
                mc_aclub.date1 = get_current_date()
                mc_aclub.char1 = user_init

        if g_list.cardnum != mc_guest.cardnum and tbuff.bezeich.lower()  == ("THE ONE").lower() :

            for mc_aclub in db_session.query(Mc_aclub).filter(
                        (Mc_aclub.key == mc_types.nr) &  
                        (Mc_aclub.cardnum == mc_guest.cardnum)
                        ).order_by(Mc_aclub._recid).all():

                if not mcbuff or not(mcbuff._recid == mc_aclub._recid):
                    mcbuff = db_session.query(Mcbuff).filter(
                            (Mcbuff._recid == mc_aclub._recid)).first()
                mcbuff.cardnum = g_list.cardnum
        fill_mc_guest()
        mc_guest.changed = user_init + " - " + to_string(get_current_date()) +\
                " " + to_string(get_current_time_in_seconds(), "HH:MM:SS")


    return generate_output()