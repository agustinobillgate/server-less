#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Mc_guest, Mc_types, Mc_cardhis, Mc_fee, Mc_aclub

g_list_list, G_list = create_model_like(Mc_guest)

def mc_gcf0bl(g_list_list:[G_list], curr_mode:string, user_init:string, gastno:int):

    prepare_cache ([Mc_guest, Mc_types, Mc_cardhis, Mc_fee, Mc_aclub])

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

        return {}

    def create_mcfee():

        nonlocal mc_guest, mc_types, mc_cardhis, mc_fee, mc_aclub
        nonlocal curr_mode, user_init, gastno
        nonlocal tbuff, mcbuff


        nonlocal g_list, tbuff, mcbuff

        mc_types = get_cache (Mc_types, {"nr": [(eq, g_list.nr)]})

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


        pass


    def fill_mc_guest():

        nonlocal mc_guest, mc_types, mc_cardhis, mc_fee, mc_aclub
        nonlocal curr_mode, user_init, gastno
        nonlocal tbuff, mcbuff


        nonlocal g_list, tbuff, mcbuff


        buffer_copy(g_list, mc_guest)


    g_list = query(g_list_list, first=True)

    if curr_mode.lower()  == ("new").lower() :
        mc_guest = Mc_guest()
        db_session.add(mc_guest)

        fill_mc_guest()
        mc_guest.userinit = user_init


        create_mcfee()

    elif curr_mode.lower()  == ("chg").lower() :

        mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gastno)]})

        mc_types = get_cache (Mc_types, {"nr": [(eq, g_list.nr)]})

        tbuff = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

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

            mc_fee = get_cache (Mc_fee, {"key": [(eq, 1)],"gastnr": [(eq, gastno)],"von_datum": [(eq, mc_guest.fdate)],"bis_datum": [(eq, mc_guest.tdate)]})

            if mc_fee:
                mc_fee.von_datum = g_list.fdate
                mc_fee.bis_datum = g_list.tdate


                pass

        if g_list.activeflag != mc_guest.activeflag and tbuff.bezeich.lower()  == ("THE ONE").lower() :

            mc_aclub = get_cache (Mc_aclub, {"key": [(eq, mc_types.nr)],"cardnum": [(eq, mc_guest.cardnum)]})

            if mc_aclub:
                mc_aclub.logi1 = not g_list.activeflag
                mc_aclub.date1 = get_current_date()
                mc_aclub.char1 = user_init

        if g_list.cardnum != mc_guest.cardnum and tbuff.bezeich.lower()  == ("THE ONE").lower() :

            for mc_aclub in db_session.query(Mc_aclub).filter(
                         (Mc_aclub.key == mc_types.nr) & (Mc_aclub.cardnum == mc_guest.cardnum)).order_by(Mc_aclub._recid).all():

                mcbuff = get_cache (Mc_aclub, {"_recid": [(eq, mc_aclub._recid)]})
                mcbuff.cardnum = g_list.cardnum
                pass
        pass
        fill_mc_guest()
        mc_guest.changed = user_init + " - " + to_string(get_current_date()) +\
                " " + to_string(get_current_time_in_seconds(), "HH:MM:SS")


        pass

    return generate_output()