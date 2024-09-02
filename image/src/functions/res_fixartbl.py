from functions.additional_functions import *
import decimal
from datetime import date
from models import Fixleist, Res_line

def res_fixartbl(fixleist_list:[Fixleist_list], pvilanguage:int, rec_id:int, resnr:int, reslinnr:int, case_type:int):
    msg_str = ""
    lvcarea:str = "res_fixart"
    fixleist = res_line = None

    fixleist_list = fixleist1 = None

    fixleist_list_list, Fixleist_list = create_model_like(Fixleist)

    Fixleist1 = Fixleist

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, fixleist, res_line
        nonlocal fixleist1


        nonlocal fixleist_list, fixleist1
        nonlocal fixleist_list_list
        return {"msg_str": msg_str}

    def fill_fixleist():

        nonlocal msg_str, lvcarea, fixleist, res_line
        nonlocal fixleist1


        nonlocal fixleist_list, fixleist1
        nonlocal fixleist_list_list


        fixleist.resnr = resnr
        fixleist.reslinnr = reslinnr
        fixleist.departement = fixleist_list.departement
        fixleist.artnr = fixleist_list.artnr
        fixleist.number = fixleist_list.number
        fixleist.sequenz = fixleist_list.sequenz
        fixleist.dekade = fixleist_list.dekade
        fixleist.lfakt = fixleist_list.lfakt
        fixleist.betrag = fixleist_list.betrag
        fixleist.bezeich = fixleist_list.bezeich

    def check_article(fix_recid:int):

        nonlocal msg_str, lvcarea, fixleist, res_line
        nonlocal fixleist1


        nonlocal fixleist_list, fixleist1
        nonlocal fixleist_list_list

        b_date:date = None
        e_date:date = None
        b1_date:date = None
        e1_date:date = None
        warn_it:bool = False
        Fixleist1 = Fixleist

        if fixleist_list.sequenz == 1:
            b_date = res_line.ankunft
            e_date = res_line.abreise - 1

        elif fixleist_list.sequenz == 2:
            b_date = res_line.ankunft
            e_date = res_line.ankunft

        elif fixleist_list.sequenz == 6:

            if fixleist_list.lfakt == None:
                b_date = res_line.ankunft
            else:
                b_date = fixleist_list.lfakt
            e_date = b_date + fixleist_list.dekade - 1

        for fixleist1 in db_session.query(Fixleist1).filter(
                (Fixleist1.resnr == resnr) &  (Fixleist1.reslinnr == reslinnr) &  (Fixleist1.artnr == fixleist.artnr) &  (Fixleist1.departement == fixleist.departement) &  (Fixleist1._recid != fix_recid)).all():

            if fixleist1.sequenz == 1:
                b1_date = res_line.ankunft
                e1_date = res_line.abreise - 1

            elif fixleist1.sequenz == 2:
                b1_date = res_line.ankunft
                e1_date = res_line.ankunft

            elif fixleist1.sequenz == 6:

                if fixleist1.lfakt == None:
                    b1_date = res_line.ankunft
                else:
                    b1_date = fixleist1.lfakt
                e1_date = b1_date + fixleist1.dekade - 1

            if (b_date >= b1_date and b_date <= e1_date) or (e_date >= b1_date and e_date <= e1_date) or (b1_date >= b_date and b1_date <= e_date) or (e1_date >= b_date and e1_date <= e_date):
                warn_it = True

            if warn_it:
                msg_str = msg_str + chr(2) + "&W" + translateExtended ("Overlapping posting found for", lvcarea, "") + " " + to_string(fixleist_list.artnr) + " - " + fixleist_list.bezeich + chr(10) + translateExtended ("Posting Date", lvcarea, "") + " " + to_string(b1_date) + " - " + to_string(e1_date) + chr(10) + translateExtended ("Please recheck to avoid N/A double posting error.", lvcarea, "")

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

    fixleist_list = query(fixleist_list_list, first=True)

    if case_type == 1:
        fixleist = Fixleist()
        db_session.add(fixleist)

        fill_fixleist()
        check_article(fixleist._recid)

    elif case_type == 2:

        fixleist = db_session.query(Fixleist).filter(
                (Fixleist._recid == rec_id)).first()
        fill_fixleist()
        check_article(fixleist._recid)

        fixleist = db_session.query(Fixleist).first()

    return generate_output()