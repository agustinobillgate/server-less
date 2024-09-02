from functions.additional_functions import *
import decimal
import re
from models import Guest, Res_line

def res_checkin_assignbl(case_type:int, resnr:int, reslinnr:int, nat_bez:str, purno:int):
    guest = res_line = None

    gast = res_line1 = rline = res_sharer = None

    Gast = Guest
    Res_line1 = Res_line
    Rline = Res_line
    Res_sharer = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest, res_line
        nonlocal gast, res_line1, rline, res_sharer


        nonlocal gast, res_line1, rline, res_sharer
        return {}


    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

    if case_type == 1:

        gast = db_session.query(Gast).filter(
                (Gast.gastnr == res_line.gastnrmember)).first()

        gast = db_session.query(Gast).first()
        gast.land = nat_bez

        gast = db_session.query(Gast).first()


    elif case_type == 2:

        gast = db_session.query(Gast).filter(
                (Gast.gastnr == res_line.gastnrmember)).first()

        gast = db_session.query(Gast).first()
        gast.nation1 = nat_bez

        gast = db_session.query(Gast).first()


    elif case_type == 3:

        res_line = db_session.query(Res_line).first()
        res_line.zimmer_wunsch = res_line.zimmer_wunsch +\
                "SEGM__PUR" + to_string(purno) + ";"

        res_line = db_session.query(Res_line).first()

        res_line1 = db_session.query(Res_line1).filter(
                    (Res_line1.resnr == res_line.resnr) &  (Res_line1.reslinnr != res_line.reslinnr) &  (Res_line1.active_flag <= 1) &  (Res_line1.resstatus != 12) &  (Res_line1.l_zuordnung[2] == 0)).first()
        while None != res_line1:

            if not re.match(".*SEGM__PUR.*",res_line1.zimmer_wunsch):

                rline = db_session.query(Rline).filter(
                            (Rline._recid == res_line1._recid)).first()

                if rline:
                    rline.zimmer_wunsch = rline.zimmer_wunsch +\
                            "SEGM__PUR" + to_string(purno) + ";"

                    rline = db_session.query(Rline).first()

            res_line1 = db_session.query(Res_line1).filter(
                        (Res_line1.resnr == res_line.resnr) &  (Res_line1.reslinnr != res_line.reslinnr) &  (Res_line1.active_flag <= 1) &  (Res_line1.resstatus != 12) &  (Res_line1.l_zuordnung[2] == 0)).first()


    elif case_type == 4:

        res_line = db_session.query(Res_line).first()

        for res_sharer in db_session.query(Res_sharer).filter(
                (Res_sharer.resnr == resnr) &  (Res_sharer.kontakt_nr == reslinnr) &  (Res_sharer.l_zuordnung[2] == 1)).all():
            res_sharer.zinr = res_line.zinr
            res_sharer.zikatnr = res_line.zikatnr
            res_sharer.setup = res_line.setup

    return generate_output()