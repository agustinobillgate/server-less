from functions.additional_functions import *
import decimal
from datetime import date
from models import Bediener, Htparam, Gc_pi, Gc_pitype

def prepare_gc_pilistbl(sorttype:int, notclearing:bool, fromname:str, toname:str):
    billdate = None
    fromdate = None
    todate = None
    b1_list_list = []
    bediener = htparam = gc_pi = gc_pitype = None

    b1_list = ubuff = gbuff = None

    b1_list_list, B1_list = create_model("B1_list", {"username":str, "userinit":str, "datum":date, "bezeich":str, "docu_nr":str, "betrag":decimal, "pay_datum":date, "postdate":date, "chequeno":str, "datum2":date, "pay_type":int, "returnamt":decimal, "bemerk":str, "pi_status":int, "rcvid":str})

    Ubuff = Bediener
    Gbuff = Gc_pi

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, fromdate, todate, b1_list_list, bediener, htparam, gc_pi, gc_pitype
        nonlocal ubuff, gbuff


        nonlocal b1_list, ubuff, gbuff
        nonlocal b1_list_list
        return {"billdate": billdate, "fromdate": fromdate, "todate": todate, "b1-list": b1_list_list}

    def check_rcvname():

        nonlocal billdate, fromdate, todate, b1_list_list, bediener, htparam, gc_pi, gc_pitype
        nonlocal ubuff, gbuff


        nonlocal b1_list, ubuff, gbuff
        nonlocal b1_list_list


        Gbuff = Gc_pi

        gc_pi = db_session.query(Gc_pi).filter(
                (Gc_pi.rcvname == '')).first()
        while None != gc_pi:

            bediener = db_session.query(Bediener).filter(
                    (Bediener.userinit == gc_pi.rcvID)).first()

            if bediener:

                gbuff = db_session.query(Gbuff).filter(
                        (Gbuff._recid == gc_pi._recid)).first()
                gbuff.rcvname = bediener.username

                gbuff = db_session.query(Gbuff).first()


            gc_pi = db_session.query(Gc_pi).filter(
                    (Gc_pi.rcvname == "")).first()

    def disp_it():

        nonlocal billdate, fromdate, todate, b1_list_list, bediener, htparam, gc_pi, gc_pitype
        nonlocal ubuff, gbuff


        nonlocal b1_list, ubuff, gbuff
        nonlocal b1_list_list

        if sorttype == 1:

            if notclearing:

                gc_pi_obj_list = []
                for gc_pi, ubuff, gc_pitype in db_session.query(Gc_pi, Ubuff, Gc_pitype).join(Ubuff,(Ubuff.userinit == Gc_pi.rcvID) &  (Ubuff.username >= fromname) &  (Ubuff.username <= toname)).join(Gc_pitype,(Gc_pitype.nr == Gc_pi.pi_type)).filter(
                        (Gc_pi.pay_datum >= fromdate) &  (Gc_pi.pay_datum <= todate) &  (Gc_pi.pi_status == sorttype) &  (Gc_pi.pay_type == 2) &  (Gc_pi.chequeNo != "") &  (Gc_pi.postDate == None)).all():
                    if gc_pi._recid in gc_pi_obj_list:
                        continue
                    else:
                        gc_pi_obj_list.append(gc_pi._recid)


                    assign_it()

            else:

                gc_pi_obj_list = []
                for gc_pi, ubuff, gc_pitype in db_session.query(Gc_pi, Ubuff, Gc_pitype).join(Ubuff,(Ubuff.userinit == Gc_pi.rcvid) &  (Ubuff.username >= fromname) &  (Ubuff.username <= toname)).join(Gc_pitype,(Gc_pitype.nr == Gc_pi.pi_type)).filter(
                        (Gc_pi.pay_datum >= fromdate) &  (Gc_pi.pay_datum <= todate) &  (Gc_pi.pi_status == sorttype)).all():
                    if gc_pi._recid in gc_pi_obj_list:
                        continue
                    else:
                        gc_pi_obj_list.append(gc_pi._recid)


                    assign_it()


        elif sorttype == 2:

            if notclearing:

                gc_pi_obj_list = []
                for gc_pi, ubuff, gc_pitype in db_session.query(Gc_pi, Ubuff, Gc_pitype).join(Ubuff,(Ubuff.userinit == Gc_pi.rcvID) &  (Ubuff.username >= fromname) &  (Ubuff.username <= toname)).join(Gc_pitype,(Gc_pitype.nr == Gc_pi.pi_type)).filter(
                        (Gc_pi.datum2 >= fromdate) &  (Gc_pi.datum2 <= todate) &  (Gc_pi.pi_status == sorttype) &  (Gc_pi.pay_type == 2) &  (Gc_pi.chequeNo != "") &  (Gc_pi.postDate == None)).all():
                    if gc_pi._recid in gc_pi_obj_list:
                        continue
                    else:
                        gc_pi_obj_list.append(gc_pi._recid)


                    assign_it()

            else:

                gc_pi_obj_list = []
                for gc_pi, ubuff, gc_pitype in db_session.query(Gc_pi, Ubuff, Gc_pitype).join(Ubuff,(Ubuff.userinit == Gc_pi.rcvID) &  (Ubuff.username >= fromname) &  (Ubuff.username <= toname)).join(Gc_pitype,(Gc_pitype.nr == Gc_pi.pi_type)).filter(
                        (Gc_pi.datum2 >= fromdate) &  (Gc_pi.datum2 <= todate) &  (Gc_pi.pi_status == sorttype)).all():
                    if gc_pi._recid in gc_pi_obj_list:
                        continue
                    else:
                        gc_pi_obj_list.append(gc_pi._recid)


                    assign_it()


        elif sorttype == 9 or sorttype == 10:

            gc_pi_obj_list = []
            for gc_pi, ubuff, gc_pitype in db_session.query(Gc_pi, Ubuff, Gc_pitype).join(Ubuff,(Ubuff.userinit == Gc_pi.rcvID) &  (Ubuff.username >= fromname) &  (Ubuff.username <= toname)).join(Gc_pitype,(Gc_pitype.nr == Gc_pi.pi_type)).filter(
                    (Gc_pi.datum >= fromdate) &  (Gc_pi.datum <= todate) &  (Gc_pi.pi_status == 9)).all():
                if gc_pi._recid in gc_pi_obj_list:
                    continue
                else:
                    gc_pi_obj_list.append(gc_pi._recid)


                assign_it()
        else:

            gc_pi_obj_list = []
            for gc_pi, ubuff, gc_pitype in db_session.query(Gc_pi, Ubuff, Gc_pitype).join(Ubuff,(Ubuff.userinit == Gc_pi.rcvID) &  (Ubuff.username >= fromname) &  (Ubuff.username <= toname)).join(Gc_pitype,(Gc_pitype.nr == Gc_pi.pi_type)).filter(
                    (Gc_pi.datum >= fromdate) &  (Gc_pi.datum <= todate) &  (Gc_pi.pi_status == sorttype)).all():
                if gc_pi._recid in gc_pi_obj_list:
                    continue
                else:
                    gc_pi_obj_list.append(gc_pi._recid)


                assign_it()

    def assign_it():

        nonlocal billdate, fromdate, todate, b1_list_list, bediener, htparam, gc_pi, gc_pitype
        nonlocal ubuff, gbuff


        nonlocal b1_list, ubuff, gbuff
        nonlocal b1_list_list


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.username = ubuff.username
        b1_list.userinit = ubuff.userinit
        b1_list.datum = gc_pi.datum
        b1_list.bezeich = gc_pitype.bezeich
        b1_list.docu_nr = gc_pi.docu_nr
        b1_list.betrag = gc_pi.betrag
        b1_list.pay_datum = gc_pi.pay_datum
        b1_list.postDate = gc_pi.postDate
        b1_list.chequeNo = gc_pi.chequeNo
        b1_list.datum2 = gc_pi.datum2
        b1_list.pay_type = gc_pi.pay_type
        b1_list.returnAmt = gc_pi.returnAmt
        b1_list.bemerk = gc_pi.bemerk
        b1_list.pi_status = gc_pi.pi_status
        b1_list.rcvID = gc_pi.rcvID

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    billdate = htparam.fdate
    fromdate = billdate - timedelta(days=30)
    todate = billdate


    check_rcvname()
    disp_it()

    return generate_output()