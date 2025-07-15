#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, Htparam, Gc_pi, Gc_pitype

def prepare_gc_pilistbl(sorttype:int, notclearing:bool, fromname:string, toname:string):

    prepare_cache ([Bediener, Htparam, Gc_pitype])

    billdate = None
    fromdate = None
    todate = None
    b1_list_data = []
    bediener = htparam = gc_pi = gc_pitype = None

    b1_list = ubuff = None

    b1_list_data, B1_list = create_model("B1_list", {"username":string, "userinit":string, "datum":date, "bezeich":string, "docu_nr":string, "betrag":Decimal, "pay_datum":date, "postdate":date, "chequeno":string, "datum2":date, "pay_type":int, "returnamt":Decimal, "bemerk":string, "pi_status":int, "rcvid":string})

    Ubuff = create_buffer("Ubuff",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, fromdate, todate, b1_list_data, bediener, htparam, gc_pi, gc_pitype
        nonlocal sorttype, notclearing, fromname, toname
        nonlocal ubuff


        nonlocal b1_list, ubuff
        nonlocal b1_list_data

        return {"billdate": billdate, "fromdate": fromdate, "todate": todate, "b1-list": b1_list_data}

    def check_rcvname():

        nonlocal billdate, fromdate, todate, b1_list_data, bediener, htparam, gc_pi, gc_pitype
        nonlocal sorttype, notclearing, fromname, toname
        nonlocal ubuff


        nonlocal b1_list, ubuff
        nonlocal b1_list_data

        gbuff = None
        Gbuff =  create_buffer("Gbuff",Gc_pi)

        gc_pi = get_cache (Gc_pi, {"rcvname": [(eq, "")]})
        while None != gc_pi:

            bediener = get_cache (Bediener, {"userinit": [(eq, gc_pi.rcvid)]})

            if bediener:

                gbuff = db_session.query(Gbuff).filter(
                         (Gbuff._recid == gc_pi._recid)).first()
                gbuff.rcvname = bediener.username


                pass
                pass

            curr_recid = gc_pi._recid
            gc_pi = db_session.query(Gc_pi).filter(
                     (Gc_pi.rcvname == "") & (Gc_pi._recid > curr_recid)).first()


    def disp_it():

        nonlocal billdate, fromdate, todate, b1_list_data, bediener, htparam, gc_pi, gc_pitype
        nonlocal sorttype, notclearing, fromname, toname
        nonlocal ubuff


        nonlocal b1_list, ubuff
        nonlocal b1_list_data

        if sorttype == 1:

            if notclearing:

                gc_pi_obj_list = {}
                for gc_pi, ubuff, gc_pitype in db_session.query(Gc_pi, Ubuff, Gc_pitype).join(Ubuff,(Ubuff.userinit == Gc_pi.rcvid) & (Ubuff.username >= fromname) & (Ubuff.username <= toname)).join(Gc_pitype,(Gc_pitype.nr == Gc_pi.pi_type)).filter(
                         (Gc_pi.pay_datum >= fromdate) & (Gc_pi.pay_datum <= todate) & (Gc_pi.pi_status == sorttype) & (Gc_pi.pay_type == 2) & (Gc_pi.chequeno != "") & (Gc_pi.postdate == None)).order_by(Gc_pi.pay_datum, Ubuff.username, Gc_pi.docu_nr).all():
                    if gc_pi_obj_list.get(gc_pi._recid):
                        continue
                    else:
                        gc_pi_obj_list[gc_pi._recid] = True


                    assign_it()

            else:

                gc_pi_obj_list = {}
                for gc_pi, ubuff, gc_pitype in db_session.query(Gc_pi, Ubuff, Gc_pitype).join(Ubuff,(Ubuff.userinit == Gc_pi.rcvid) & (Ubuff.username >= fromname) & (Ubuff.username <= toname)).join(Gc_pitype,(Gc_pitype.nr == Gc_pi.pi_type)).filter(
                         (Gc_pi.pay_datum >= fromdate) & (Gc_pi.pay_datum <= todate) & (Gc_pi.pi_status == sorttype)).order_by(Gc_pi.pay_datum, Ubuff.username, Gc_pi.docu_nr).all():
                    if gc_pi_obj_list.get(gc_pi._recid):
                        continue
                    else:
                        gc_pi_obj_list[gc_pi._recid] = True


                    assign_it()


        elif sorttype == 2:

            if notclearing:

                gc_pi_obj_list = {}
                for gc_pi, ubuff, gc_pitype in db_session.query(Gc_pi, Ubuff, Gc_pitype).join(Ubuff,(Ubuff.userinit == Gc_pi.rcvid) & (Ubuff.username >= fromname) & (Ubuff.username <= toname)).join(Gc_pitype,(Gc_pitype.nr == Gc_pi.pi_type)).filter(
                         (Gc_pi.datum2 >= fromdate) & (Gc_pi.datum2 <= todate) & (Gc_pi.pi_status == sorttype) & (Gc_pi.pay_type == 2) & (Gc_pi.chequeno != "") & (Gc_pi.postdate == None)).order_by(Gc_pi.datum2, Ubuff.username, Gc_pi.docu_nr).all():
                    if gc_pi_obj_list.get(gc_pi._recid):
                        continue
                    else:
                        gc_pi_obj_list[gc_pi._recid] = True


                    assign_it()

            else:

                gc_pi_obj_list = {}
                for gc_pi, ubuff, gc_pitype in db_session.query(Gc_pi, Ubuff, Gc_pitype).join(Ubuff,(Ubuff.userinit == Gc_pi.rcvid) & (Ubuff.username >= fromname) & (Ubuff.username <= toname)).join(Gc_pitype,(Gc_pitype.nr == Gc_pi.pi_type)).filter(
                         (Gc_pi.datum2 >= fromdate) & (Gc_pi.datum2 <= todate) & (Gc_pi.pi_status == sorttype)).order_by(Gc_pi.datum2, Ubuff.username, Gc_pi.docu_nr).all():
                    if gc_pi_obj_list.get(gc_pi._recid):
                        continue
                    else:
                        gc_pi_obj_list[gc_pi._recid] = True


                    assign_it()


        elif sorttype == 9 or sorttype == 10:

            gc_pi_obj_list = {}
            for gc_pi, ubuff, gc_pitype in db_session.query(Gc_pi, Ubuff, Gc_pitype).join(Ubuff,(Ubuff.userinit == Gc_pi.rcvid) & (Ubuff.username >= fromname) & (Ubuff.username <= toname)).join(Gc_pitype,(Gc_pitype.nr == Gc_pi.pi_type)).filter(
                     (Gc_pi.datum >= fromdate) & (Gc_pi.datum <= todate) & (Gc_pi.pi_status == 9)).order_by(Ubuff.username, Gc_pi.pi_status, Gc_pi.docu_nr).all():
                if gc_pi_obj_list.get(gc_pi._recid):
                    continue
                else:
                    gc_pi_obj_list[gc_pi._recid] = True


                assign_it()
        else:

            gc_pi_obj_list = {}
            for gc_pi, ubuff, gc_pitype in db_session.query(Gc_pi, Ubuff, Gc_pitype).join(Ubuff,(Ubuff.userinit == Gc_pi.rcvid) & (Ubuff.username >= fromname) & (Ubuff.username <= toname)).join(Gc_pitype,(Gc_pitype.nr == Gc_pi.pi_type)).filter(
                     (Gc_pi.datum >= fromdate) & (Gc_pi.datum <= todate) & (Gc_pi.pi_status == sorttype)).order_by(Ubuff.username, Gc_pi.pi_status, Gc_pi.docu_nr).all():
                if gc_pi_obj_list.get(gc_pi._recid):
                    continue
                else:
                    gc_pi_obj_list[gc_pi._recid] = True


                assign_it()


    def assign_it():

        nonlocal billdate, fromdate, todate, b1_list_data, bediener, htparam, gc_pi, gc_pitype
        nonlocal sorttype, notclearing, fromname, toname
        nonlocal ubuff


        nonlocal b1_list, ubuff
        nonlocal b1_list_data


        b1_list = B1_list()
        b1_list_data.append(b1_list)

        b1_list.username = ubuff.username
        b1_list.userinit = ubuff.userinit
        b1_list.datum = gc_pi.datum
        b1_list.bezeich = gc_pitype.bezeich
        b1_list.docu_nr = gc_pi.docu_nr
        b1_list.betrag =  to_decimal(gc_pi.betrag)
        b1_list.pay_datum = gc_pi.pay_datum
        b1_list.postdate = gc_pi.postdate
        b1_list.chequeno = gc_pi.chequeno
        b1_list.datum2 = gc_pi.datum2
        b1_list.pay_type = gc_pi.pay_type
        b1_list.returnamt =  to_decimal(gc_pi.returnamt)
        b1_list.bemerk = gc_pi.bemerk
        b1_list.pi_status = gc_pi.pi_status
        b1_list.rcvid = gc_pi.rcvid


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate
    fromdate = billdate - timedelta(days=30)
    todate = billdate


    check_rcvname()
    disp_it()

    return generate_output()