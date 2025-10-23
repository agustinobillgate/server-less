from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from sqlalchemy import func
from models import H_bill_line, Queasy, H_bill, H_artikel, Bediener, Hoteldpt, H_journal, Wgrpdep

def kitchen_display_getdata_cld_1bl(casetype:int, kp_number:int):
    kitchen_display_list_list = []
    summary_artlist_list = []
    done_list_list = []
    count_i:int = 0
    spreq:str = ""
    doit:bool = False
    bill_date:date = None
    stime:int = 0
    recount:int = 0
    h_bill_line = queasy = h_bill = h_artikel = bediener = hoteldpt = h_journal = wgrpdep = None

    kitchen_display_list = summary_artlist = summ_list = done_list = void_menu = void_kds = kds_header = kds_line = void_line = kds = qtime = bkds = None

    kitchen_display_list_list, Kitchen_display_list = create_model("Kitchen_display_list", {"count_pos":int, "curr_flag":str, "qhead_recid":int, "qline_recid":int, "recid_hbline":int, "bill_no":int, "dept_no":int, "table_no":int, "user_post_id":str, "user_name":str, "artikel_no":int, "artikel_qty":int, "artikel_name":str, "sp_request":str, "post_date":date, "post_time":int, "post_timestr":str, "status_order":str, "void_menu":bool, "remain_qty":int, "dept_name":str, "system_date":date, "served_time":str})
    summary_artlist_list, Summary_artlist = create_model("Summary_artlist", {"artikel_no":int, "artikel_qty":int, "artikel_name":str, "artikel_dept":int, "subgroup_no":int, "subgroup_name":str, "void_menu":bool})
    summ_list_list, Summ_list = create_model("Summ_list", {"artikel_no":int, "artikel_qty":int, "artikel_name":str, "artikel_dept":int, "subgroup_no":int, "subgroup_name":str})
    done_list_list, Done_list = create_model_like(Summary_artlist)
    void_menu_list, Void_menu = create_model_like(H_bill_line)
    void_kds_list, Void_kds = create_model_like(Kitchen_display_list)
    kds_header_list, Kds_header = create_model_like(Queasy, {"q_recid":int})
    kds_line_list, Kds_line = create_model_like(Queasy, {"q_recid":int})

    Void_line = create_buffer("Void_line",H_bill_line)
    Kds = Kitchen_display_list
    kds_list = kitchen_display_list_list

    Qtime = create_buffer("Qtime",Queasy)
    Bkds = Kitchen_display_list
    bkds_list = kitchen_display_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal kitchen_display_list_list, summary_artlist_list, done_list_list, count_i, spreq, doit, bill_date, stime, recount, h_bill_line, queasy, h_bill, h_artikel, bediener, hoteldpt, h_journal, wgrpdep
        nonlocal casetype, kp_number
        nonlocal void_line, kds, qtime, bkds


        nonlocal kitchen_display_list, summary_artlist, summ_list, done_list, void_menu, void_kds, kds_header, kds_line, void_line, kds, qtime, bkds
        nonlocal kitchen_display_list_list, summary_artlist_list, summ_list_list, done_list_list, void_menu_list, void_kds_list, kds_header_list, kds_line_list
        return {"kitchen-display-list": kitchen_display_list_list, "summary-artlist": summary_artlist_list, "done-list": done_list_list}

    def create_header():

        nonlocal kitchen_display_list_list, summary_artlist_list, done_list_list, count_i, spreq, doit, bill_date, stime, recount, h_bill_line, queasy, h_bill, h_artikel, bediener, hoteldpt, h_journal, wgrpdep
        nonlocal casetype, kp_number
        nonlocal void_line, kds, qtime, bkds


        nonlocal kitchen_display_list, summary_artlist, summ_list, done_list, void_menu, void_kds, kds_header, kds_line, void_line, kds, qtime, bkds
        nonlocal kitchen_display_list_list, summary_artlist_list, summ_list_list, done_list_list, void_menu_list, void_kds_list, kds_header_list, kds_line_list


        count_i = count_i + 1
        kitchen_display_list = Kitchen_display_list()
        kitchen_display_list_list.append(kitchen_display_list)

        kitchen_display_list.count_pos = count_i
        kitchen_display_list.qhead_recid = kds_header.q_recid
        kitchen_display_list.curr_flag = kds_header.char1
        kitchen_display_list.dept_no = kds_header.number1
        kitchen_display_list.bill_no = kds_header.number2
        kitchen_display_list.table_no = kds_header.number3
        kitchen_display_list.user_post_id = kds_header.char2
        kitchen_display_list.post_date = kds_header.date1
        kitchen_display_list.post_time = to_int(kds_header.deci1)
        kitchen_display_list.post_timestr = to_string(kitchen_display_list.post_time, "HH:MM:SS")

        bediener = db_session.query(Bediener).filter(
                 (Bediener.userinit == kds_header.char2)).first()

        if bediener:
            kitchen_display_list.user_name = bediener.username

        if casetype == 2:
            kitchen_display_list.status_order = "DONE"
        else:

            if kds_header.deci2 == 0:
                kitchen_display_list.status_order = "NEW"

            elif kds_header.deci2 == 1:
                kitchen_display_list.status_order = "COOKING"

            elif kds_header.deci2 == 2:
                kitchen_display_list.status_order = "DONE"

            elif kds_header.deci2 == 3:
                kitchen_display_list.status_order = "SERVED"

            elif kds_header.deci2 == 4:
                kitchen_display_list.status_order = "SERVEDBYSYSTEM"

        hoteldpt = db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num == kds_header.number1)).first()

        if hoteldpt:
            kitchen_display_list.dept_name = hoteldpt.depart


    def create_line():

        nonlocal kitchen_display_list_list, summary_artlist_list, done_list_list, count_i, spreq, doit, bill_date, stime, recount, h_bill_line, queasy, h_bill, h_artikel, bediener, hoteldpt, h_journal, wgrpdep
        nonlocal casetype, kp_number
        nonlocal void_line, kds, qtime, bkds


        nonlocal kitchen_display_list, summary_artlist, summ_list, done_list, void_menu, void_kds, kds_header, kds_line, void_line, kds, qtime, bkds
        nonlocal kitchen_display_list_list, summary_artlist_list, summ_list_list, done_list_list, void_menu_list, void_kds_list, kds_header_list, kds_line_list

        h_journal = db_session.query(H_journal).filter(
                 (H_journal.schankbuch == kds_line.number3)).first()

        if h_journal:
            spreq = h_journal.aendertext
        else:
            spreq = ""

        kitchen_display_list = query(kitchen_display_list_list, filters=(lambda kitchen_display_list: kitchen_display_list.recid_hbline == kds_line.number3), first=True)

        qtime = db_session.query(Qtime).filter(
                 (Qtime.key == 302) & (Qtime.betriebsnr == to_int(kds_line.q_recid))).first()

        if not kitchen_display_list:
            kitchen_display_list = Kitchen_display_list()
            kitchen_display_list_list.append(kitchen_display_list)

            kitchen_display_list.count_pos = count_i
            kitchen_display_list.qhead_recid = kds_line.deci2
            kitchen_display_list.qline_recid = kds_line.q_recid
            kitchen_display_list.curr_flag = kds_line.char1
            kitchen_display_list.dept_no = kds_line.number1
            kitchen_display_list.bill_no = kds_line.number2
            kitchen_display_list.recid_hbline = kds_line.number3
            kitchen_display_list.user_post_id = kds_line.char2
            kitchen_display_list.artikel_no = h_artikel.artnr
            kitchen_display_list.artikel_qty = 1
            kitchen_display_list.artikel_name = h_bill_line.bezeich
            kitchen_display_list.sp_request = spreq
            kitchen_display_list.post_date = kds_line.date1
            kitchen_display_list.post_time = kds_line.deci1
            kitchen_display_list.post_timestr = to_string(kitchen_display_list.post_time, "HH:MM:SS")
            kitchen_display_list.remain_qty = 1
            kitchen_display_list.system_date = h_bill_line.sysdate

            if bediener:
                kitchen_display_list.user_name = bediener.username

            if kds_line.char3 == "":
                kitchen_display_list.status_order = "NEW"

            elif kds_line.char3  == ("1") :
                kitchen_display_list.status_order = "COOKING"

            elif kds_line.char3  == ("2") :
                kitchen_display_list.status_order = "DONE"

            elif kds_line.char3  == ("3") :
                kitchen_display_list.status_order = "SERVED"

            elif kds_line.char3  == ("4") :
                kitchen_display_list.status_order = "SERVEDBYSYSTEM"

            if qtime and kds_line.char3  == ("3") :
                kitchen_display_list.served_time = entry(2, qtime.char1, "|")
        else:
            kitchen_display_list.artikel_qty = kitchen_display_list.artikel_qty + 1

        if (kitchen_display_list.status_order  != ("SERVED")  and kitchen_display_list.status_order  != ("SERVEDBYSYSTEM")):

            summary_artlist = query(summary_artlist_list, filters=(lambda summary_artlist: summary_artlist.artikel_no == h_artikel.artnr and summary_artlist.artikel_dept == h_artikel.departement), first=True)

            if not summary_artlist:
                summary_artlist = Summary_artlist()
                summary_artlist_list.append(summary_artlist)

                summary_artlist.artikel_no = h_artikel.artnr
                summary_artlist.artikel_qty = 1
                summary_artlist.artikel_name = h_bill_line.bezeich.upper()
                summary_artlist.artikel_dept = h_artikel.departement
                summary_artlist.subgroup_no = h_artikel.zwkum

                wgrpdep = db_session.query(Wgrpdep).filter(
                         (Wgrpdep.departement == h_artikel.departement) & (Wgrpdep.zknr == h_artikel.zwkum)).first()

                if wgrpdep:
                    summary_artlist.subgroup_name = wgrpdep.bezeich

                kds = query(kds_list, filters=(lambda kds: kds.artikel_no == h_artikel.artnr), first=True)

                if kds:
                    summary_artlist.void_menu = kds.void_menu
            else:
                summary_artlist.artikel_qty = summary_artlist.artikel_qty + 1
                summary_artlist.artikel_name = h_bill_line.bezeich.upper()
                summary_artlist.subgroup_no = h_artikel.zwkum

                wgrpdep = db_session.query(Wgrpdep).filter(
                         (Wgrpdep.departement == h_artikel.departement) & (Wgrpdep.zknr == h_artikel.zwkum)).first()

                if wgrpdep:
                    summary_artlist.subgroup_name = wgrpdep.bezeich

                kds = query(kds_list, filters=(lambda kds: kds.artikel_no == h_artikel.artnr), first=True)

                if kds:
                    summary_artlist.void_menu = kds.void_menu
        pass


    def create_done():

        nonlocal kitchen_display_list_list, summary_artlist_list, done_list_list, count_i, spreq, doit, bill_date, stime, recount, h_bill_line, queasy, h_bill, h_artikel, bediener, hoteldpt, h_journal, wgrpdep
        nonlocal casetype, kp_number
        nonlocal void_line, kds, qtime, bkds


        nonlocal kitchen_display_list, summary_artlist, summ_list, done_list, void_menu, void_kds, kds_header, kds_line, void_line, kds, qtime, bkds
        nonlocal kitchen_display_list_list, summary_artlist_list, summ_list_list, done_list_list, void_menu_list, void_kds_list, kds_header_list, kds_line_list


        count_i = 0

        h_bill_line_obj_list = []
        # Rd, 13/10/2025
        # list dikeluarkan dari for loop
        # for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.departement == H_bill_line.departement) & (H_artikel.artnr == H_bill_line.artnr) & (H_artikel.bondruckernr[inc_value(0)] == kp_number)).filter(
        #          (H_bill_line._recid.in_(list(set([kds_line.number3 for kds_line in kds_line_list if kds_line.logi1]))))).order_by(kds_line.date1, kds_line.deci1).all():
        recid_list = list({kds.number3 for kds in kds_line_list if kds.logi1})
        
        if recid_list:
            results = (
                db_session.query(H_bill_line, H_artikel)
                .join(
                    H_artikel,
                    (H_artikel.departement == H_bill_line.departement)
                    & (H_artikel.artnr == H_bill_line.artnr)
                    & (H_artikel.bondruckernr[inc_value(0)] == kp_number)
                )
                .filter(H_bill_line._recid.in_(recid_list))
                .order_by(H_bill_line.date1, H_bill_line.deci1)  # ✅ fixed
                .all()
            )
        else:
            results = []  # nothing to query if list empty

        for h_bill_line, h_artikel in results:
            if h_bill_line._recid in h_bill_line_obj_list:
                continue
            else:
                h_bill_line_obj_list.append(h_bill_line._recid)

            done_list = query(done_list_list, filters=(lambda done_list: done_list.artikel_no == h_artikel.artnr and done_list.artikel_dept == h_artikel.departement), first=True)

            if not done_list:
                done_list = Done_list()
                done_list_list.append(done_list)

                done_list.artikel_no = h_artikel.artnr
                done_list.artikel_qty = 1
                done_list.artikel_name = h_bill_line.bezeich.upper()
                done_list.artikel_dept = h_artikel.departement
                done_list.subgroup_no = h_artikel.zwkum

                wgrpdep = db_session.query(Wgrpdep).filter(
                         (Wgrpdep.departement == h_artikel.departement) & (Wgrpdep.zknr == h_artikel.zwkum)).first()

                if wgrpdep:
                    done_list.subgroup_name = wgrpdep.bezeich

                void_line = db_session.query(Void_line).filter(
                         (Void_line.rechnr == h_bill_line.rechnr) & (Void_line.artnr == done_list.artikel_no) & (Void_line.anzahl < 0)).first()

                if void_line:
                    done_list.void_menu = True
                else:
                    done_list.void_menu = False
            else:
                done_list.artikel_qty = done_list.artikel_qty + 1
                done_list.artikel_name = h_bill_line.bezeich.upper()
                done_list.subgroup_no = h_artikel.zwkum

                wgrpdep = db_session.query(Wgrpdep).filter(
                         (Wgrpdep.departement == h_artikel.departement) & (Wgrpdep.zknr == h_artikel.zwkum)).first()

                if wgrpdep:
                    done_list.subgroup_name = wgrpdep.bezeich

                void_line = db_session.query(Void_line).filter(
                         (Void_line.rechnr == h_bill_line.rechnr) & (Void_line.artnr == done_list.artikel_no) & (Void_line.anzahl < 0)).first()

                if void_line:
                    done_list.void_menu = True
                else:
                    done_list.void_menu = False


    bill_date = get_output(htpdate(110))

    for h_bill in db_session.query(H_bill).filter(
             (H_bill.flag == 0)).order_by(H_bill._recid).all():

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == h_bill.departement) & (H_bill_line.bill_datum >= bill_date - timedelta(days=1)) & (H_bill_line.bill_datum <= bill_date + timedelta(days=1)) & (H_bill_line.anzahl < 0)).order_by(H_bill_line._recid).all():
            void_menu = Void_menu()
            void_menu_list.append(void_menu)

            buffer_copy(h_bill_line, void_menu)
            void_menu.transferred = False

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 257) & (func.lower(Queasy.char1) == ("kds-header")) & (Queasy.date1 == bill_date) & (not Queasy.logi1)).order_by(Queasy._recid).all():
        kds_header = Kds_header()
        kds_header_list.append(kds_header)

        buffer_copy(queasy, kds_header)
        kds_header.q_recid = queasy._recid

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 255) & (func.lower(Queasy.char1) == ("kds-line")) & (Queasy.date1 == bill_date) & (not Queasy.logi1)).order_by(Queasy._recid).all():
        kds_line = Kds_line()
        kds_line_list.append(kds_line)

        buffer_copy(queasy, kds_line)
        kds_line.q_recid = queasy._recid

    if casetype == 1:
        count_i = 0

        for kds_header in query(kds_header_list, sort_by=[("date1",False),("deci1",False)]):
            create_header()

            for kds_line in query(kds_line_list, filters=(lambda kds_line: kds_line.deci2 == to_decimal(kds_header.q_recid)), sort_by=[("date1",False),("deci1",False)]):

                h_bill_line = db_session.query(H_bill_line).filter(
                         (H_bill_line._recid == kds_line.number3)).first()

                h_artikel = db_session.query(H_artikel).filter(
                         (H_artikel.departement == h_bill_line.departement) & (H_artikel.artnr == h_bill_line.artnr) & (H_artikel.bondruckernr[inc_value(0)] == kp_number)).first()

                if h_artikel:
                    create_line()

        for kitchen_display_list in query(kitchen_display_list_list, filters=(lambda kitchen_display_list: kitchen_display_list.curr_flag  == ("kds-line"))):

            void_menu = query(void_menu_list, filters=(lambda void_menu: void_menu.departemen == kitchen_display_list.dept_no and void_menu.rechnr == kitchen_display_list.bill_no and void_menu.artnr == kitchen_display_list.artikel_no and void_menu.transferred == False), first=True)

            if void_menu:

                summary_artlist = query(summary_artlist_list, filters=(lambda summary_artlist: summary_artlist.artikel_no == kitchen_display_list.artikel_no), first=True)

                if summary_artlist:
                    summary_artlist.artikel_qty = summary_artlist.artikel_qty + void_menu.anzahl

                if void_menu.anzahl == - kitchen_display_list.artikel_qty:
                    kitchen_display_list_list.remove(kitchen_display_list)
                else:
                    kitchen_display_list.artikel_qty = kitchen_display_list.artikel_qty + void_menu.anzahl
                void_menu_list.remove(void_menu)

    elif casetype == 2:
        pass
    
    create_done()

    for bkds in query(bkds_list, filters=(lambda bkds: bkds.curr_flag  == ("kds-header")), sort_by=[("count_pos",False)]):

        kitchen_display_list = query(kitchen_display_list_list, filters=(lambda kitchen_display_list: kitchen_display_list.curr_flag  == ("kds-line")  and kitchen_display_list.qhead_recid == bkds.qhead_recid), first=True)

        if not kitchen_display_list:
            bkds_list.remove(bkds)
        else:
            recount = recount + 1
            bkds.count_pos = recount

            for kitchen_display_list in query(kitchen_display_list_list, filters=(lambda kitchen_display_list: kitchen_display_list.curr_flag  == ("kds-line")  and kitchen_display_list.qhead_recid == bkds.qhead_recid)):
                kitchen_display_list.count_pos = recount

    return generate_output()