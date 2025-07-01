#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.clcount_expired import clcount_expired
from functions.create_ar_membershipbl import create_ar_membershipbl
from models import Htparam, Cl_memtype, Cl_class, Cl_member, Cl_histci, Guest, Cl_locker, Queasy, Cl_histvisit, Mc_fee, Cl_log, Cl_histstatus, Cl_enroll, Cl_checkin

def clclosing():

    prepare_cache ([Htparam, Cl_memtype, Cl_class, Cl_member, Guest, Cl_locker, Queasy, Mc_fee, Cl_log, Cl_histstatus])

    lvcarea:string = "clclosing"
    curr_bezeich:string = ""
    curr_bezeich1:string = ""
    billdate:date = None
    store_dur:int = 360
    htparam = cl_memtype = cl_class = cl_member = cl_histci = guest = cl_locker = queasy = cl_histvisit = mc_fee = cl_log = cl_histstatus = cl_enroll = cl_checkin = None

    visit = checkin = clhist = None

    Visit = create_buffer("Visit",Cl_histvisit)
    Checkin = create_buffer("Checkin",Cl_checkin)
    Clhist = create_buffer("Clhist",Cl_histci)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lvcarea, curr_bezeich, curr_bezeich1, billdate, store_dur, htparam, cl_memtype, cl_class, cl_member, cl_histci, guest, cl_locker, queasy, cl_histvisit, mc_fee, cl_log, cl_histstatus, cl_enroll, cl_checkin
        nonlocal visit, checkin, clhist


        nonlocal visit, checkin, clhist

        return {}

    def check_memtype():

        nonlocal lvcarea, curr_bezeich, curr_bezeich1, billdate, store_dur, htparam, cl_memtype, cl_class, cl_member, cl_histci, guest, cl_locker, queasy, cl_histvisit, mc_fee, cl_log, cl_histstatus, cl_enroll, cl_checkin
        nonlocal visit, checkin, clhist


        nonlocal visit, checkin, clhist

        memtype = None
        Memtype =  create_buffer("Memtype",Cl_memtype)
        curr_bezeich = translateExtended ("Checking active memberships type...", lvcarea, "")

        for cl_memtype in db_session.query(Cl_memtype).order_by(Cl_memtype._recid).all():

            if cl_memtype.tdate < get_current_date() and cl_memtype.activeflag :

                memtype = get_cache (Cl_memtype, {"_recid": [(eq, cl_memtype._recid)]})

                if memtype:
                    memtype.activeflag = False
                    pass

            elif cl_memtype.activeflag == False and cl_memtype.tdate > get_current_date():

                memtype = get_cache (Cl_memtype, {"_recid": [(eq, cl_memtype._recid)]})

                if memtype:
                    memtype.activeflag = True
                    pass
            curr_bezeich1 = cl_memtype.DESCRIPT
            pass


    def check_class():

        nonlocal lvcarea, curr_bezeich, curr_bezeich1, billdate, store_dur, htparam, cl_memtype, cl_class, cl_member, cl_histci, guest, cl_locker, queasy, cl_histvisit, mc_fee, cl_log, cl_histstatus, cl_enroll, cl_checkin
        nonlocal visit, checkin, clhist


        nonlocal visit, checkin, clhist

        class = None
        Class =  create_buffer("Class",Cl_class)
        curr_bezeich = translateExtended ("Checking active classes...", lvcarea, "")

        for cl_class in db_session.query(Cl_class).order_by(Cl_class._recid).all():

            if cl_class.end_date < get_current_date() and cl_class.activeflag :

                class = get_cache (Cl_class, {"_recid": [(eq, cl_class._recid)]})

                if class:
                    class.activeflag = False
                    pass

            elif cl_class.activeflag == False and cl_class.start_date <= get_current_date():

                class = get_cache (Cl_class, {"_recid": [(eq, cl_class._recid)]})

                if class:
                    class.activeflag = True
                    pass
            curr_bezeich1 = cl_class.name
            pass


    def check_inhouse():

        nonlocal lvcarea, curr_bezeich, curr_bezeich1, billdate, store_dur, htparam, cl_memtype, cl_class, cl_member, cl_histci, guest, cl_locker, queasy, cl_histvisit, mc_fee, cl_log, cl_histstatus, cl_enroll, cl_checkin
        nonlocal visit, checkin, clhist


        nonlocal visit, checkin, clhist

        membr = None
        Membr =  create_buffer("Membr",Cl_member)
        curr_bezeich = translateExtended ("Checking inhouse members...", lvcarea, "")

        for cl_member in db_session.query(Cl_member).filter(
                 (Cl_member.checked_in) & (Cl_member.last_visit < TODAY)).order_by(Cl_member._recid).all():

            membr = get_cache (Cl_member, {"_recid": [(eq, cl_member._recid)]})

            if membr:
                membr.checked_in = False
                membr.co_time = get_current_time_in_seconds()
                pass

            cl_histci = get_cache (Cl_histci, {"codenum": [(eq, cl_member.codenum)],"datum": [(eq, cl_member.last_visit)],"starttime": [(eq, cl_member.ci_time)]})

            if cl_histci:
                cl_histci.endtime = cl_member.co_time
                pass

            guest = get_cache (Guest, {"gastnr": [(eq, cl_member.gastnr)]})

            if guest:
                curr_bezeich1 = guest.name + ", " + guest.vorname1 + guest.anrede1
            pass


    def check_others():

        nonlocal lvcarea, curr_bezeich, curr_bezeich1, billdate, store_dur, htparam, cl_memtype, cl_class, cl_member, cl_histci, guest, cl_locker, queasy, cl_histvisit, mc_fee, cl_log, cl_histstatus, cl_enroll, cl_checkin
        nonlocal visit, checkin, clhist


        nonlocal visit, checkin, clhist

        hbuff = None
        Hbuff =  create_buffer("Hbuff",Cl_histci)

        for cl_histci in db_session.query(Cl_histci).filter(
                 (Cl_histci.datum < get_current_date()) & (Cl_histci.num1 == 2) & (Cl_histci.voucherno != "")).order_by(Cl_histci._recid).all():

            hbuff = db_session.query(Hbuff).filter(
                     (Hbuff._recid == cl_histci._recid)).first()
            hbuff.num1 = 5


            pass


    def check_locker():

        nonlocal lvcarea, curr_bezeich, curr_bezeich1, billdate, store_dur, htparam, cl_memtype, cl_class, cl_member, cl_histci, guest, cl_locker, queasy, cl_histvisit, mc_fee, cl_log, cl_histstatus, cl_enroll, cl_checkin
        nonlocal visit, checkin, clhist


        nonlocal visit, checkin, clhist


        curr_bezeich = translateExtended ("Checking occupied lockers...", lvcarea, "")

        for cl_locker in db_session.query(Cl_locker).filter(
                 (Cl_locker.valid_flag) & (Cl_locker.to_date < get_current_date()) & (Cl_locker.locknum != "")).order_by(Cl_locker._recid).all():
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 118
            queasy.char1 = cl_locker.locknum
            queasy.number1 = cl_locker.location
            queasy.date1 = cl_locker.from_date
            queasy.date2 = cl_locker.to_date
            queasy.number2 = cl_locker.from_time
            queasy.number3 = cl_locker.to_time


            curr_bezeich1 = cl_locker.locknum
            pass


    def check_visit():

        nonlocal lvcarea, curr_bezeich, curr_bezeich1, billdate, store_dur, htparam, cl_memtype, cl_class, cl_member, cl_histci, guest, cl_locker, queasy, cl_histvisit, mc_fee, cl_log, cl_histstatus, cl_enroll, cl_checkin
        nonlocal visit, checkin, clhist


        nonlocal visit, checkin, clhist

        visit = None
        gbuff = None
        mbuff = None
        Visit =  create_buffer("Visit",Cl_histvisit)
        Gbuff =  create_buffer("Gbuff",Guest)
        Mbuff =  create_buffer("Mbuff",Cl_member)
        curr_bezeich = translateExtended ("Checking inhouse members in classes/service area...", lvcarea, "")

        for cl_histvisit in db_session.query(Cl_histvisit).filter(
                 (Cl_histvisit.datum < get_current_date()) & (Cl_histvisit.endtime == None)).order_by(Cl_histvisit._recid).all():

            cl_class = get_cache (Cl_class, {"nr": [(eq, cl_histvisit.service)]})

            if cl_histvisit.trainflag:

                visit = db_session.query(Visit).filter(
                         (Visit._recid == cl_histvisit._recid)).first()

                if visit:
                    visit.endtime = (Integer (substring(cl_class.end_time, 0, 2)) * 3600) + (to_int(substring(cl_class.end_time, 2, 2)) * 60)
                    pass
            else:

                visit = db_session.query(Visit).filter(
                         (Visit._recid == cl_histvisit._recid)).first()

                if visit:
                    visit.endtime = get_current_time_in_seconds()
                    pass

            mbuff = get_cache (Cl_member, {"codenum": [(eq, cl_histvisit.codenum)]})

            if mbuff:

                gbuff = get_cache (Guest, {"gastnr": [(eq, mbuff.gastnr)]})

                if gbuff:
                    curr_bezeich1 = gbuff.name + ", " + gbuff.vorname1 + gbuff.anrede1
            pass


    def create_renewal():

        nonlocal lvcarea, curr_bezeich, curr_bezeich1, billdate, store_dur, htparam, cl_memtype, cl_class, cl_member, cl_histci, guest, cl_locker, queasy, cl_histvisit, mc_fee, cl_log, cl_histstatus, cl_enroll, cl_checkin
        nonlocal visit, checkin, clhist


        nonlocal visit, checkin, clhist

        ndays:int = 30
        curr_date:date = None
        exp_date:date = None
        mfee:Decimal = to_decimal("0.0")
        init_fee:Decimal = to_decimal("0.0")
        gbuff = None
        mbuff = None
        mbuff1 = None
        Gbuff =  create_buffer("Gbuff",Guest)
        Mbuff =  create_buffer("Mbuff",Cl_member)
        Mbuff1 =  create_buffer("Mbuff1",Cl_member)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1049)]})

        if (not htparam) or (htparam and htparam.finteger > 0):
            ndays = htparam.finteger


        curr_bezeich = translateExtended ("Create new bill for renewal...", lvcarea, "")

        for mbuff in db_session.query(Mbuff).filter(
                 (Mbuff.memstatus == 1) & ((Mbuff.expired_date - billdate) == ndays)).order_by(Mbuff._recid).all():

            cl_memtype = get_cache (Cl_memtype, {"nr": [(eq, mbuff.membertype)]})
            exp_date = get_output(clcount_expired(mbuff.codenum))
            mfee =  to_decimal(cl_memtype.fee1)

            if mbuff.deci2 != 0 or mbuff.logi1:
                mfee =  to_decimal(mbuff.deci2)

            for mc_fee in db_session.query(Mc_fee).filter(
                         (Mc_fee.key == 2) & (Mc_fee.gastnr == mbuff.gastnr) & (Mc_fee.activeflag == 1)).order_by(Mc_fee._recid).all():
                mc_fee.activeflag = 2

            mc_fee = get_cache (Mc_fee, {"key": [(eq, 2)],"nr": [(eq, mbuff.membertype)],"gastnr": [(eq, mbuff.gastnr)],"bis_datum": [(eq, exp_date)]})

            if not mc_fee:
                mc_fee = Mc_fee()
                db_session.add(mc_fee)

            mc_fee.key = 2
            mc_fee.usr_init = "$$"
            mc_fee.bez_datum2 = billdate
            mc_fee.von_datum = mbuff.expired_date + timedelta(days=1)
            mc_fee.bis_datum = exp_date
            mc_fee.nr = mbuff.membertype
            mc_fee.gastnr = mbuff.gastnr
            mc_fee.betrag =  to_decimal(mfee)

            if mbuff.memstatus == 0:

                if mbuff.deci2 != 0 or mbuff.logi1:
                    init_fee =  to_decimal(mbuff.deci1)
                else:
                    init_fee =  to_decimal(cl_memtype.fee)
            get_output(create_ar_membershipbl(mc_fee.gastnr, init_fee, mfee, user_init))

            gbuff = get_cache (Guest, {"gastnr": [(eq, mbuff.gastnr)]})

            if gbuff:
                curr_bezeich1 = gbuff.name + ", " + gbuff.vorname1
        pass


    def check_expired():

        nonlocal lvcarea, curr_bezeich, curr_bezeich1, billdate, store_dur, htparam, cl_memtype, cl_class, cl_member, cl_histci, guest, cl_locker, queasy, cl_histvisit, mc_fee, cl_log, cl_histstatus, cl_enroll, cl_checkin
        nonlocal visit, checkin, clhist


        nonlocal visit, checkin, clhist

        max_freeze:int = 0
        curr_status:int = 0
        add_days:int = 0
        guest1 = None
        mbuff = None
        Guest1 =  create_buffer("Guest1",Guest)
        Mbuff =  create_buffer("Mbuff",Cl_member)
        curr_bezeich = translateExtended ("Checking expired members...", lvcarea, "")

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1040)]})
        max_freeze = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1066)]})
        add_days = htparam.finteger

        for cl_member in db_session.query(Cl_member).filter(
                 (Cl_member.memstatus == 1) & ((billdate - Cl_member.expired_date - add_days) >= 0)).order_by(Cl_member._recid).all():
            curr_status = 2

            guest1 = get_cache (Guest, {"gastnr": [(eq, cl_member.gastnr)]})
            cl_log = Cl_log()
            db_session.add(cl_log)

            cl_log.codenum = cl_member.codenum
            cl_log.datum = get_current_date()
            cl_log.zeit = get_current_time_in_seconds()
            cl_log.user_init = " "
            cl_log.char1 = to_string(cl_member.membertype) + " ; " + to_string(cl_member.membertype) +\
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

            mbuff = get_cache (Cl_member, {"_recid": [(eq, cl_member._recid)]})
            mbuff.memstatus = curr_status


            pass

            guest = get_cache (Guest, {"gastnr": [(eq, cl_member.gastnr)]})

            if guest:
                curr_bezeich1 = guest.name + " " + guest.vorname1
            cl_histstatus = Cl_histstatus()
            db_session.add(cl_histstatus)

            cl_histstatus.datum = get_current_date()
            cl_histstatus.codenum = mbuff.codenum
            cl_histstatus.memstatus = mbuff.memstatus
            cl_histstatus.user_init = "Night Audit"
            cl_histstatus.zeit = get_current_time_in_seconds()

            for cl_enroll in db_session.query(Cl_enroll).filter(
                         (Cl_enroll.codenum == cl_member.codenum)).order_by(Cl_enroll._recid).all():
                db_session.delete(cl_enroll)
        pass


    DEFINE FRAME Frame1 curr_bezeich AT ROW 1.5 COLUMN 3 LABEL "Activity" FGCOLOR 12 SKIP (0.5) curr_bezeich1 AT ROW 3 COLUMN 5.5 LABEL "Item" FGCOLOR 15 BGCOL 1 SKIP (0.5) skip (0.5) WITH SIDE_LABELS CENTERED OVERLAY WIDTH 55 THREE_D VIEW_AS DIALOG_BOX TITLE "Checking...."
    VIEW FRAME frame1
    translatewidgetwinctx(FRAME frame1:HANDLE, lvcarea)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate
    check_class()
    check_inhouse()
    check_locker()
    check_visit()
    create_renewal()
    check_expired()
    delete_history()
    check_others()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1057)]})

    if htparam:
        store_dur = htparam.finteger
    curr_bezeich = translateExtended ("Deleting old history..", lvcarea, "")

    for cl_checkin in db_session.query(Cl_checkin).filter(
             ((Cl_checkin.datum - get_current_date()) > store_dur)).order_by(Cl_checkin._recid).all():

        checkin = db_session.query(Checkin).filter(
                 (Checkin._recid == cl_checkin._recid)).first()
        db_session.delete(checkin)
        pass

    for cl_histci in db_session.query(Cl_histci).filter(
             ((Cl_histci.datum - get_current_date()) > store_dur)).order_by(Cl_histci._recid).all():

        clhist = db_session.query(Clhist).filter(
                 (Clhist._recid == cl_histci._recid)).first()
        db_session.delete(clhist)
        pass

    for cl_histvisit in db_session.query(Cl_histvisit).filter(
             ((Cl_histvisit.datum - get_current_date()) > store_dur)).order_by(Cl_histvisit._recid).all():

        visit = db_session.query(Visit).filter(
                 (Visit._recid == cl_histvisit._recid)).first()
        db_session.delete(visit)
        pass

    return generate_output()