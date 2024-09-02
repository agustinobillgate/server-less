from functions.additional_functions import *
import decimal
from datetime import date
from functions.clcount_expiredbl import clcount_expiredbl
from models import Htparam, Cl_memtype, Cl_class, Cl_member, Cl_histci, Cl_locker, Queasy, Cl_histvisit, Guest, Mc_fee, Cl_log, Cl_histstatus, Cl_enroll, Cl_checkin

def clclosingbl():
    billdate:date = None
    store_dur:int = 360
    htparam = cl_memtype = cl_class = cl_member = cl_histci = cl_locker = queasy = cl_histvisit = guest = mc_fee = cl_log = cl_histstatus = cl_enroll = cl_checkin = None

    memtype = class = membr = hbuff = visit = gbuff = mbuff = mbuff1 = guest1 = checkin = clhist = None

    Memtype = Cl_memtype
    Class = Cl_class
    Membr = Cl_member
    Hbuff = Cl_histci
    Visit = Cl_histvisit
    Gbuff = Guest
    Mbuff = Cl_member
    Mbuff1 = Cl_member
    Guest1 = Guest
    Checkin = Cl_checkin
    Clhist = Cl_histci

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, store_dur, htparam, cl_memtype, cl_class, cl_member, cl_histci, cl_locker, queasy, cl_histvisit, guest, mc_fee, cl_log, cl_histstatus, cl_enroll, cl_checkin
        nonlocal memtype, class, membr, hbuff, visit, gbuff, mbuff, mbuff1, guest1, checkin, clhist


        nonlocal memtype, class, membr, hbuff, visit, gbuff, mbuff, mbuff1, guest1, checkin, clhist
        return {}

    def check_memtype():

        nonlocal billdate, store_dur, htparam, cl_memtype, cl_class, cl_member, cl_histci, cl_locker, queasy, cl_histvisit, guest, mc_fee, cl_log, cl_histstatus, cl_enroll, cl_checkin
        nonlocal memtype, class, membr, hbuff, visit, gbuff, mbuff, mbuff1, guest1, checkin, clhist


        nonlocal memtype, class, membr, hbuff, visit, gbuff, mbuff, mbuff1, guest1, checkin, clhist


        Memtype = Cl_memtype

        for cl_memtype in db_session.query(Cl_memtype).all():

            if cl_memtype.tdate < get_current_date() and cl_memtype.activeflag :

                memtype = db_session.query(Memtype).filter(
                        (Memtype._recid == cl_Memtype._recid)).first()

                if memtype:
                    memtype.activeflag = False

                    memtype = db_session.query(Memtype).first()

            elif cl_memtype.activeflag == False and cl_memtype.tdate > get_current_date():

                memtype = db_session.query(Memtype).filter(
                        (Memtype._recid == cl_Memtype._recid)).first()

                if memtype:
                    memtype.activeflag = True

                    memtype = db_session.query(Memtype).first()

    def check_class():

        nonlocal billdate, store_dur, htparam, cl_memtype, cl_class, cl_member, cl_histci, cl_locker, queasy, cl_histvisit, guest, mc_fee, cl_log, cl_histstatus, cl_enroll, cl_checkin
        nonlocal memtype, class, membr, hbuff, visit, gbuff, mbuff, mbuff1, guest1, checkin, clhist


        nonlocal memtype, class, membr, hbuff, visit, gbuff, mbuff, mbuff1, guest1, checkin, clhist


        Class = Cl_class

        for cl_class in db_session.query(Cl_class).all():

            if cl_class.end_date < get_current_date() and cl_class.activeflag :

                class = db_session.query(Class).filter(
                        (Class._recid == cl_Class._recid)).first()

                if class:
                    class.activeflag = False

                    class = db_session.query(Class).first()

            elif cl_class.activeflag == False and cl_class.start_date <= get_current_date():

                class = db_session.query(Class).filter(
                        (Class._recid == cl_Class._recid)).first()

                if class:
                    class.activeflag = True

                    class = db_session.query(Class).first()

    def check_inhouse():

        nonlocal billdate, store_dur, htparam, cl_memtype, cl_class, cl_member, cl_histci, cl_locker, queasy, cl_histvisit, guest, mc_fee, cl_log, cl_histstatus, cl_enroll, cl_checkin
        nonlocal memtype, class, membr, hbuff, visit, gbuff, mbuff, mbuff1, guest1, checkin, clhist


        nonlocal memtype, class, membr, hbuff, visit, gbuff, mbuff, mbuff1, guest1, checkin, clhist


        Membr = Cl_member

        for cl_member in db_session.query(Cl_member).filter(
                (checked_in) &  (Cl_member.last_visit < TODAY)).all():

            membr = db_session.query(Membr).filter(
                    (Membr._recid == cl_member._recid)).first()

            if membr:
                membr.checked_in = False
                membr.co_time = get_current_time_in_seconds()

                membr = db_session.query(Membr).first()

            cl_histci = db_session.query(Cl_histci).filter(
                    (Cl_histci.codenum == cl_member.codenum) &  (Cl_histci.datum == cl_member.last_visit) &  (Cl_histci.starttime == cl_member.ci_time)).first()

            if cl_histci:
                cl_histci.endtime = cl_member.co_time

                cl_histci = db_session.query(Cl_histci).first()

    def check_others():

        nonlocal billdate, store_dur, htparam, cl_memtype, cl_class, cl_member, cl_histci, cl_locker, queasy, cl_histvisit, guest, mc_fee, cl_log, cl_histstatus, cl_enroll, cl_checkin
        nonlocal memtype, class, membr, hbuff, visit, gbuff, mbuff, mbuff1, guest1, checkin, clhist


        nonlocal memtype, class, membr, hbuff, visit, gbuff, mbuff, mbuff1, guest1, checkin, clhist


        Hbuff = Cl_histci

        for cl_histci in db_session.query(Cl_histci).filter(
                (Cl_histci.datum < get_current_date()) &  (Cl_histci.num1 == 2) &  (Cl_histci.voucherno != "")).all():

            hbuff = db_session.query(Hbuff).filter(
                    (Hbuff._recid == cl_histci._recid)).first()
            hbuff.num1 = 5


    def check_locker():

        nonlocal billdate, store_dur, htparam, cl_memtype, cl_class, cl_member, cl_histci, cl_locker, queasy, cl_histvisit, guest, mc_fee, cl_log, cl_histstatus, cl_enroll, cl_checkin
        nonlocal memtype, class, membr, hbuff, visit, gbuff, mbuff, mbuff1, guest1, checkin, clhist


        nonlocal memtype, class, membr, hbuff, visit, gbuff, mbuff, mbuff1, guest1, checkin, clhist

        for cl_locker in db_session.query(Cl_locker).filter(
                (valid_flag) &  (Cl_locker.to_date < get_current_date()) &  (Cl_locker.locknum != "")).all():
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 118
            queasy.char1 = cl_locker.locknum
            queasy.number1 = cl_locker.location
            queasy.date1 = cl_locker.from_date
            queasy.date2 = cl_locker.to_date
            queasy.number2 = cl_locker.from_time
            queasy.number3 = cl_locker.to_time

            queasy = db_session.query(Queasy).first()

    def check_visit():

        nonlocal billdate, store_dur, htparam, cl_memtype, cl_class, cl_member, cl_histci, cl_locker, queasy, cl_histvisit, guest, mc_fee, cl_log, cl_histstatus, cl_enroll, cl_checkin
        nonlocal memtype, class, membr, hbuff, visit, gbuff, mbuff, mbuff1, guest1, checkin, clhist


        nonlocal memtype, class, membr, hbuff, visit, gbuff, mbuff, mbuff1, guest1, checkin, clhist


        Visit = Cl_histvisit
        Gbuff = Guest
        Mbuff = Cl_member

        for cl_histvisit in db_session.query(Cl_histvisit).filter(
                (Cl_histvisit.datum < get_current_date()) &  (Cl_histvisit.endtime == None)).all():

            cl_class = db_session.query(Cl_class).filter(
                    (Cl_class.nr == cl_histvisit.service)).first()

            if cl_histvisit.trainflag:

                visit = db_session.query(Visit).filter(
                        (Visit._recid == cl_histVisit._recid)).first()

                if visit:
                    visit.endtime = (Integer (substring(cl_class.end_time, 0, 2)) * 3600) + (to_int(substring(cl_class.end_time, 2, 2)) * 60)

                    visit = db_session.query(Visit).first()
            else:

                visit = db_session.query(Visit).filter(
                        (Visit._recid == cl_histVisit._recid)).first()

                if visit:
                    visit.endtime = get_current_time_in_seconds()

                    visit = db_session.query(Visit).first()

            mbuff = db_session.query(Mbuff).filter(
                    (Mbuff.codenum == cl_histvisit.codenum)).first()

            if mbuff:
                pass

    def create_renewal():

        nonlocal billdate, store_dur, htparam, cl_memtype, cl_class, cl_member, cl_histci, cl_locker, queasy, cl_histvisit, guest, mc_fee, cl_log, cl_histstatus, cl_enroll, cl_checkin
        nonlocal memtype, class, membr, hbuff, visit, gbuff, mbuff, mbuff1, guest1, checkin, clhist


        nonlocal memtype, class, membr, hbuff, visit, gbuff, mbuff, mbuff1, guest1, checkin, clhist

        ndays:int = 30
        curr_date:date = None
        exp_date:date = None
        mfee:decimal = 0
        Gbuff = Guest
        Mbuff = Cl_member
        Mbuff1 = Cl_member

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1049)).first()

        if (not htparam) or (htparam and htparam.finteger > 0):
            ndays = htparam.finteger

        for mbuff in db_session.query(Mbuff).filter(
                (Mbuff.memstatus == 1) &  ((Mbuff.expired_date - billdate) == ndays)).all():

            cl_memtype = db_session.query(Cl_memtype).filter(
                    (Cl_memtype.nr == mbuff.membertype)).first()
            exp_date = get_output(clcount_expiredbl(mbuff.codenum))
            mfee = cl_memtype.fee1

            if mbuff.deci2 != 0 or mbuff.logi1:
                mfee = mbuff.deci2

            for mc_fee in db_session.query(Mc_fee).filter(
                        (Mc_fee.key == 2) &  (Mc_fee.gastnr == mbuff.gastnr) &  (Mc_fee.activeflag == 1)).all():
                mc_fee.activeflag = 2

            mc_fee = db_session.query(Mc_fee).filter(
                        (Mc_fee.key == 2) &  (Mc_fee.nr == mbuff.membertype) &  (Mc_fee.gastnr == mbuff.gastnr) &  (Mc_fee.bis_datum == exp_date)).first()

            if not mc_fee:
                mc_fee = Mc_fee()
            db_session.add(mc_fee)

            mc_fee.key = 2
            mc_fee.usr_init = "$$"
            mc_fee.bez_datum2 = billdate
            mc_fee.von_datum = mbuff.expired_date + 1
            mc_fee.bis_datum = exp_date
            mc_fee.nr = mbuff.membertype
            mc_fee.gastnr = mbuff.gastnr
            mc_fee.betrag = mfee

    def check_expired():

        nonlocal billdate, store_dur, htparam, cl_memtype, cl_class, cl_member, cl_histci, cl_locker, queasy, cl_histvisit, guest, mc_fee, cl_log, cl_histstatus, cl_enroll, cl_checkin
        nonlocal memtype, class, membr, hbuff, visit, gbuff, mbuff, mbuff1, guest1, checkin, clhist


        nonlocal memtype, class, membr, hbuff, visit, gbuff, mbuff, mbuff1, guest1, checkin, clhist

        max_freeze:int = 0
        curr_status:int = 0
        add_days:int = 0
        Guest1 = Guest
        Mbuff = Cl_member

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1040)).first()
        max_freeze = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1066)).first()
        add_days = htparam.finteger

        for cl_member in db_session.query(Cl_member).filter(
                (Cl_member.memstatus == 1) &  ((billdate - Cl_member.expired_date - add_days) >= 0)).all():
            curr_status = 2

            guest1 = db_session.query(Guest1).filter(
                        (Guest1.gastnr == cl_member.gastnr)).first()
            cl_log = Cl_log()
            db_session.add(cl_log)

            cl_log.codenum = cl_member.codenum
            cl_log.datum = get_current_date()
            cl_log.zeit = get_current_time_in_seconds()
            cl_log.user_init = " "
            cl_log.CHAR1 = to_string(cl_member.membertype) + " ; " + to_string(cl_member.membertype) +\
                    " ; " + to_string(cl_member.memstatus) + " ; " + to_string(curr_status) +\
                    " ; " + cl_member.pict_file + " ; " + cl_member.pict_file +\
                    " ; " + cl_member.load_by + " ; " + cl_member.load_by +\
                    " ; " + to_string(cl_member.billgastnr, ">>>>>9") + " ; " + to_string(cl_member.billgastnr, ">>>>>9") +\
                    " ; " + to_string(guest1.kreditlimit, ">>,>>>,>>>,>>9") + " ; " + to_string(guest1.kreditlimit, ">>,>>>,>>>,>>9") +\
                    " ; " + to_string(cl_member.paysched) + " ; " + to_string(cl_member.paysched) +\
                    " ; " + to_string(cl_member.billcycle) + " ; " + to_string(cl_member.billcycle) +\
                    " ; " + to_string(cl_member.expired) + " ; " + to_string(get_current_date()) +\
                    " ; " + cl_member.user_init1 + " ; " + " " +\
                    " ; " + to_string(cl_member.main_gastnr) + " ; " + to_string(cl_member.gastnr)

            mbuff = db_session.query(Mbuff).filter(
                        (Mbuff._recid == cl_member._recid)).first()
            mbuff.memstatus = curr_status

            mbuff = db_session.query(Mbuff).first()
            cl_histstatus = Cl_histstatus()
            db_session.add(cl_histstatus)

            cl_histstatus.datum = get_current_date()
            cl_histstatus.codenum = mbuff.codenum
            cl_histstatus.memstatus = mbuff.memstatus
            cl_histstatus.user_init = "Night Audit"
            cl_histstatus.zeit = get_current_time_in_seconds()

            for cl_enroll in db_session.query(Cl_enroll).filter(
                        (Cl_enroll.codenum == cl_member.codenum)).all():
                db_session.delete(cl_enroll)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()

    if htparam:
        billdate = htparam.fdate
    check_class()
    check_inhouse()
    check_locker()
    check_visit()
    create_renewal()
    check_expired()
    delete_history()
    check_others()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1057)).first()

    if htparam:
        store_dur = htparam.finteger

    for cl_checkin in db_session.query(Cl_checkin).filter(
            ((Cl_checkin.datum - get_current_date()) > store_dur)).all():

        checkin = db_session.query(Checkin).filter(
                (Checkin._recid == cl_Checkin._recid)).first()
        db_session.delete(checkin)


    for cl_histci in db_session.query(Cl_histci).filter(
            ((Cl_histci.datum - get_current_date()) > store_dur)).all():

        clhist = db_session.query(Clhist).filter(
                (Clhist._recid == cl_histci._recid)).first()
        db_session.delete(clhist)


    for cl_histvisit in db_session.query(Cl_histvisit).filter(
            ((Cl_histvisit.datum - get_current_date()) > store_dur)).all():

        visit = db_session.query(Visit).filter(
                (Visit._recid == cl_histVisit._recid)).first()
        db_session.delete(visit)


    return generate_output()