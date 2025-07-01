#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fixleist, Res_line, Reslin_queasy

fixleist_list_list, Fixleist_list = create_model_like(Fixleist)

def res_fixart_webbl(fixleist_list_list:[Fixleist_list], pvilanguage:int, rec_id:int, resnr:int, reslinnr:int, case_type:int, user_init:string):

    prepare_cache ([Fixleist, Res_line, Reslin_queasy])

    msg_str = ""
    lvcarea:string = "res-fixart"
    is_fixrate:string = "False"
    fixleist = res_line = reslin_queasy = None

    fixleist_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, is_fixrate, fixleist, res_line, reslin_queasy
        nonlocal pvilanguage, rec_id, resnr, reslinnr, case_type, user_init


        nonlocal fixleist_list

        return {"msg_str": msg_str}

    def fill_fixleist():

        nonlocal msg_str, lvcarea, is_fixrate, fixleist, res_line, reslin_queasy
        nonlocal pvilanguage, rec_id, resnr, reslinnr, case_type, user_init


        nonlocal fixleist_list


        fixleist.resnr = resnr
        fixleist.reslinnr = reslinnr
        fixleist.departement = fixleist_list.departement
        fixleist.artnr = fixleist_list.artnr
        fixleist.number = fixleist_list.number
        fixleist.sequenz = fixleist_list.sequenz
        fixleist.dekade = fixleist_list.dekade
        fixleist.lfakt = fixleist_list.lfakt
        fixleist.betrag =  to_decimal(fixleist_list.betrag)
        fixleist.bezeich = fixleist_list.bezeich


    def check_article(fix_recid:int):

        nonlocal msg_str, lvcarea, is_fixrate, fixleist, res_line, reslin_queasy
        nonlocal pvilanguage, rec_id, resnr, reslinnr, case_type, user_init


        nonlocal fixleist_list

        b_date:date = None
        e_date:date = None
        b1_date:date = None
        e1_date:date = None
        warn_it:bool = False
        fixleist1 = None
        Fixleist1 =  create_buffer("Fixleist1",Fixleist)

        if fixleist_list.sequenz == 1:
            b_date = res_line.ankunft
            e_date = res_line.abreise - timedelta(days=1)

        elif fixleist_list.sequenz == 2:
            b_date = res_line.ankunft
            e_date = res_line.ankunft

        elif fixleist_list.sequenz == 6:

            if fixleist_list.lfakt == None:
                b_date = res_line.ankunft
            else:
                b_date = fixleist_list.lfakt
            e_date = b_date + timedelta(days=fixleist_list.dekade - 1)

        for fixleist1 in db_session.query(Fixleist1).filter(
                 (Fixleist1.resnr == resnr) & (Fixleist1.reslinnr == reslinnr) & (Fixleist1.artnr == fixleist.artnr) & (Fixleist1.departement == fixleist.departement) & (Fixleist1._recid != fix_recid)).order_by(Fixleist1._recid).all():

            if fixleist1.sequenz == 1:
                b1_date = res_line.ankunft
                e1_date = res_line.abreise - timedelta(days=1)

            elif fixleist1.sequenz == 2:
                b1_date = res_line.ankunft
                e1_date = res_line.ankunft

            elif fixleist1.sequenz == 6:

                if fixleist1.lfakt == None:
                    b1_date = res_line.ankunft
                else:
                    b1_date = fixleist1.lfakt
                e1_date = b1_date + timedelta(days=fixleist1.dekade - 1)

            if (b_date >= b1_date and b_date <= e1_date) or (e_date >= b1_date and e_date <= e1_date) or (b1_date >= b_date and b1_date <= e_date) or (e1_date >= b_date and e1_date <= e_date):
                warn_it = True

            if warn_it:
                msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("Overlapping posting found for", lvcarea, "") + " " + to_string(fixleist_list.artnr) + " - " + fixleist_list.bezeich + chr_unicode(10) + translateExtended ("Posting Date", lvcarea, "") + " " + to_string(b1_date) + " - " + to_string(e1_date) + chr_unicode(10) + translateExtended ("Please recheck to avoid N/A double posting error.", lvcarea, "")


    def fixcost_changes_add():

        nonlocal msg_str, lvcarea, is_fixrate, fixleist, res_line, reslin_queasy
        nonlocal pvilanguage, rec_id, resnr, reslinnr, case_type, user_init


        nonlocal fixleist_list

        cid:string = ""
        cdate:string = " "
        rqy = None
        Rqy =  create_buffer("Rqy",Reslin_queasy)

        if not res_line:

            return

        if res_line.active_flag == 2:

            return

        if res_line.changed != None:
            cid = res_line.changed_id
            cdate = to_string(res_line.changed)


        rqy = Reslin_queasy()
        db_session.add(rqy)

        rqy.key = "ResChanges"
        rqy.resnr = res_line.resnr
        rqy.reslinnr = res_line.reslinnr
        rqy.date2 = get_current_date()
        rqy.number2 = get_current_time_in_seconds()


        rqy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("ADD Fixcost:") + ";" + to_string(fixleist_list.artnr) + "-" + to_string(fixleist_list.bezeich) + ";" + to_string(is_fixrate, "x(3)") + ";" + to_string(is_fixrate, "x(3)") + ";"
        pass
        pass


    def fixcost_changes_chg():

        nonlocal msg_str, lvcarea, is_fixrate, fixleist, res_line, reslin_queasy
        nonlocal pvilanguage, rec_id, resnr, reslinnr, case_type, user_init


        nonlocal fixleist_list

        cid:string = ""
        cdate:string = " "
        temp_str1:string = ""
        temp_str2:string = ""
        rqy = None
        Rqy =  create_buffer("Rqy",Reslin_queasy)

        if not res_line:

            return

        if res_line.active_flag == 2:

            return

        if res_line.changed != None:
            cid = res_line.changed_id
            cdate = to_string(res_line.changed)

        if fixleist.number != fixleist_list.number:
            rqy = Reslin_queasy()
            db_session.add(rqy)

            rqy.key = "ResChanges"
            rqy.resnr = res_line.resnr
            rqy.reslinnr = res_line.reslinnr
            rqy.date2 = get_current_date()
            rqy.number2 = get_current_time_in_seconds()


            rqy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("CHG Fixcost ") + to_string(fixleist.artnr) + "-" + to_string(fixleist.bezeich) + to_string(" FR:") + ";" + to_string("QTY : ") + to_string(fixleist.number) + ";" + to_string(is_fixrate, "x(3)") + ";" + to_string(is_fixrate, "x(3)") + ";"
            pass
            pass
            rqy = Reslin_queasy()
            db_session.add(rqy)

            rqy.key = "ResChanges"
            rqy.resnr = res_line.resnr
            rqy.reslinnr = res_line.reslinnr
            rqy.date2 = get_current_date()
            rqy.number2 = get_current_time_in_seconds()


            rqy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("CHG Fixcost ") + to_string(fixleist_list.artnr) + "-" + to_string(fixleist_list.bezeich) + to_string(" TO:") + ";" + to_string("QTY : ") + to_string(fixleist_list.number) + ";" + to_string(is_fixrate, "x(3)") + ";" + to_string(is_fixrate, "x(3)") + ";"
            pass
            pass

        if fixleist.betrag != fixleist_list.betrag:
            rqy = Reslin_queasy()
            db_session.add(rqy)

            rqy.key = "ResChanges"
            rqy.resnr = res_line.resnr
            rqy.reslinnr = res_line.reslinnr
            rqy.date2 = get_current_date()
            rqy.number2 = get_current_time_in_seconds()


            rqy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("CHG Fixcost ") + to_string(fixleist.artnr) + "-" + to_string(fixleist.bezeich) + to_string(" FR:") + ";" + to_string("Price : ") + to_string(fixleist.betrag) + ";" + to_string(is_fixrate, "x(3)") + ";" + to_string(is_fixrate, "x(3)") + ";"
            pass
            pass
            rqy = Reslin_queasy()
            db_session.add(rqy)

            rqy.key = "ResChanges"
            rqy.resnr = res_line.resnr
            rqy.reslinnr = res_line.reslinnr
            rqy.date2 = get_current_date()
            rqy.number2 = get_current_time_in_seconds()


            rqy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("CHG Fixcost ") + to_string(fixleist_list.artnr) + "-" + to_string(fixleist_list.bezeich) + to_string(" TO:") + ";" + to_string("Price : ") + to_string(fixleist_list.betrag) + ";" + to_string(is_fixrate, "x(3)") + ";" + to_string(is_fixrate, "x(3)") + ";"
            pass
            pass

        if fixleist.sequenz != fixleist_list.sequenz:
            rqy = Reslin_queasy()
            db_session.add(rqy)

            rqy.key = "ResChanges"
            rqy.resnr = res_line.resnr
            rqy.reslinnr = res_line.reslinnr
            rqy.date2 = get_current_date()
            rqy.number2 = get_current_time_in_seconds()

            if fixleist.sequenz == 6:
                temp_str1 = to_string(fixleist.sequenz) + "-" + to_string(fixleist.dekade) + "|" + to_string(fixleist.lfakt)
            else:
                temp_str1 = to_string(fixleist.sequenz)

            if fixleist_list.sequenz == 6:
                temp_str2 = to_string(fixleist_list.sequenz) + "-" + to_string(fixleist_list.dekade) + "|" + to_string(fixleist_list.lfakt)
            else:
                temp_str2 = to_string(fixleist_list.sequenz)
            rqy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("CHG Fixcost ") + to_string(fixleist.artnr) + "-" + to_string(fixleist.bezeich) + to_string(" FR:") + ";" + to_string("Type : ") + temp_str1 + ";" + to_string(is_fixrate, "x(3)") + ";" + to_string(is_fixrate, "x(3)") + ";"
            pass
            pass
            rqy = Reslin_queasy()
            db_session.add(rqy)

            rqy.key = "ResChanges"
            rqy.resnr = res_line.resnr
            rqy.reslinnr = res_line.reslinnr
            rqy.date2 = get_current_date()
            rqy.number2 = get_current_time_in_seconds()


            rqy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("CHG Fixcost ") + to_string(fixleist_list.artnr) + "-" + to_string(fixleist_list.bezeich) + to_string(" TO:") + ";" + to_string("Type : ") + temp_str2 + ";" + to_string(is_fixrate, "x(3)") + ";" + to_string(is_fixrate, "x(3)") + ";"
            pass
            pass

        elif fixleist.sequenz == 6 and fixleist_list.sequenz == 6 and (fixleist.dekade != fixleist_list.dekade or fixleist.lfakt != fixleist_list.lfakt):
            rqy = Reslin_queasy()
            db_session.add(rqy)

            rqy.key = "ResChanges"
            rqy.resnr = res_line.resnr
            rqy.reslinnr = res_line.reslinnr
            rqy.date2 = get_current_date()
            rqy.number2 = get_current_time_in_seconds()


            rqy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("CHG Fixcost ") + to_string(fixleist.artnr) + "-" + to_string(fixleist.bezeich) + to_string(" FR:") + ";" + to_string("Type : ") + to_string(fixleist.sequenz) + "-" + to_string(fixleist.dekade) + "|" + to_string(fixleist.lfakt) + ";" + to_string(is_fixrate, "x(3)") + ";" + to_string(is_fixrate, "x(3)") + ";"
            pass
            pass
            rqy = Reslin_queasy()
            db_session.add(rqy)

            rqy.key = "ResChanges"
            rqy.resnr = res_line.resnr
            rqy.reslinnr = res_line.reslinnr
            rqy.date2 = get_current_date()
            rqy.number2 = get_current_time_in_seconds()


            rqy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("CHG Fixcost ") + to_string(fixleist_list.artnr) + "-" + to_string(fixleist_list.bezeich) + to_string(" TO:") + ";" + to_string("Type : ") + to_string(fixleist_list.sequenz) + "-" + to_string(fixleist_list.dekade) + "|" + to_string(fixleist_list.lfakt) + ";" + to_string(is_fixrate, "x(3)") + ";" + to_string(is_fixrate, "x(3)") + ";"
            pass
            pass


    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    if reslin_queasy:
        is_fixrate = "YES"

    fixleist_list = query(fixleist_list_list, first=True)

    if user_init == None:
        user_init = " "

    if case_type == 1:
        fixleist = Fixleist()
        db_session.add(fixleist)

        fill_fixleist()
        check_article(fixleist._recid)
        fixcost_changes_add()

    elif case_type == 2:

        fixleist = get_cache (Fixleist, {"_recid": [(eq, rec_id)]})
        fixcost_changes_chg()
        fill_fixleist()
        check_article(fixleist._recid)
        pass

    return generate_output()