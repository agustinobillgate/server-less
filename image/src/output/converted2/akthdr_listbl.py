from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Guest, Akt_code, Akt_kont, Akthdr

def akthdr_listbl(inp_gastnr:int, next_date:date, to_date:date, all_flag:bool, sflag:int, user_init:str):
    guest_name = ""
    q1_list_list = []
    guest = akt_code = akt_kont = akthdr = None

    q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"guest_name":str, "anredefirma":str, "akt_kont_name":str, "vorname":str, "anrede":str, "flag":int, "akthdr_bezeich":str, "akt_code_bezeich":str, "t_betrag":decimal, "erl_datum":date, "userinit":str, "chg_id":str, "chg_datum":date, "aktnr":int, "next_datum":date, "erledigt":bool, "akthdr_recid":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest_name, q1_list_list, guest, akt_code, akt_kont, akthdr
        nonlocal inp_gastnr, next_date, to_date, all_flag, sflag, user_init


        nonlocal q1_list
        nonlocal q1_list_list
        return {"guest_name": guest_name, "q1-list": q1_list_list}

    def disp_all():

        nonlocal guest_name, q1_list_list, guest, akt_code, akt_kont, akthdr
        nonlocal inp_gastnr, next_date, to_date, all_flag, sflag, user_init


        nonlocal q1_list
        nonlocal q1_list_list

        if inp_gastnr == 0:

            if all_flag:

                if sflag == 1:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             (Akthdr.flag == 1)).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()


                elif sflag == 2:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             ((Akthdr.flag == 2) | (Akthdr.flag == 3))).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()


                elif sflag == 3:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             (Akthdr.flag == 4)).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()

            else:

                if sflag == 1:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             (Akthdr.flag == 1) & (func.lower(Akthdr.userinit) == (user_init).lower())).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()


                elif sflag == 2:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             ((Akthdr.flag == 2) | (Akthdr.flag == 3)) & (func.lower(Akthdr.userinit) == (user_init).lower())).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()


                elif sflag == 3:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             (Akthdr.flag == 4) & (func.lower(Akthdr.userinit) == (user_init).lower())).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()

        else:

            if all_flag:

                if sflag == 1:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             (Akthdr.flag == 1) & (Akthdr.gastnr == inp_gastnr)).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()


                elif sflag == 2:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             ((Akthdr.flag == 2) | (Akthdr.flag == 3)) & (Akthdr.gastnr == inp_gastnr)).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()


                elif sflag == 3:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             (Akthdr.flag == 4) & (Akthdr.gastnr == inp_gastnr)).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()

            else:

                if sflag == 1:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             (Akthdr.flag == 1) & (func.lower(Akthdr.userinit) == (user_init).lower()) & (Akthdr.gastnr == inp_gastnr)).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()


                elif sflag == 2:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             ((Akthdr.flag == 2) | (Akthdr.flag == 3)) & (Akthdr.gastnr == inp_gastnr) & (func.lower(Akthdr.userinit) == (user_init).lower())).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()


                elif sflag == 3:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             (Akthdr.flag == 4) & (Akthdr.gastnr == inp_gastnr) & (func.lower(Akthdr.userinit) == (user_init).lower())).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()

    def disp_it():

        nonlocal guest_name, q1_list_list, guest, akt_code, akt_kont, akthdr
        nonlocal inp_gastnr, next_date, to_date, all_flag, sflag, user_init


        nonlocal q1_list
        nonlocal q1_list_list

        if inp_gastnr == 0:

            if all_flag:

                if sflag == 1:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             (Akthdr.flag == 1) & (Akthdr.next_datum >= next_date) & (Akthdr.next_datum <= to_date)).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()


                elif sflag == 2:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             ((Akthdr.flag == 2) | (Akthdr.flag == 3)) & (Akthdr.erl_datum >= next_date) & (Akthdr.erl_datum <= to_date)).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()


                elif sflag == 3:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             (Akthdr.flag == 4) & (Akthdr.next_datum >= next_date) & (Akthdr.next_datum <= to_date)).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()

            else:

                if sflag == 1:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             (Akthdr.flag == 1) & (func.lower(Akthdr.userinit) == (user_init).lower()) & (Akthdr.next_datum >= next_date) & (Akthdr.next_datum <= to_date)).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()


                elif sflag == 2:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             ((Akthdr.flag == 2) | (Akthdr.flag == 3)) & (func.lower(Akthdr.userinit) == (user_init).lower()) & (Akthdr.erl_datum >= next_date) & (Akthdr.erl_datum <= to_date)).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()


                elif sflag == 3:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             (Akthdr.flag == 4) & (func.lower(Akthdr.userinit) == (user_init).lower()) & (Akthdr.next_datum >= next_date) & (Akthdr.next_datum <= to_date)).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()

        else:

            if all_flag:

                if sflag == 1:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             (Akthdr.flag == 1) & (Akthdr.gastnr == inp_gastnr) & (Akthdr.next_datum >= next_date) & (Akthdr.next_datum <= to_date)).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()


                elif sflag == 2:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             ((Akthdr.flag == 2) | (Akthdr.flag == 3)) & (Akthdr.gastnr == inp_gastnr) & (Akthdr.erl_datum >= next_date) & (Akthdr.erl_datum <= to_date)).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()


                elif sflag == 3:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             (Akthdr.flag == 4) & (Akthdr.gastnr == inp_gastnr) & (Akthdr.next_datum >= next_date) & (Akthdr.next_datum <= to_date)).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()

            else:

                if sflag == 1:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             (Akthdr.flag == 1) & (func.lower(Akthdr.userinit) == (user_init).lower()) & (Akthdr.gastnr == inp_gastnr) & (Akthdr.next_datum >= next_date) & (Akthdr.next_datum <= to_date)).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()


                elif sflag == 2:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             ((Akthdr.flag == 2) | (Akthdr.flag == 3)) & (Akthdr.gastnr == inp_gastnr) & (func.lower(Akthdr.userinit) == (user_init).lower()) & (Akthdr.erl_datum >= next_date) & (Akthdr.erl_datum <= to_date)).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()


                elif sflag == 3:

                    akthdr_obj_list = []
                    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                             (Akthdr.flag == 4) & (Akthdr.gastnr == inp_gastnr) & (func.lower(Akthdr.userinit) == (user_init).lower()) & (Akthdr.next_datum >= next_date) & (Akthdr.next_datum <= to_date)).order_by(Guest.name, Akthdr.next_datum.desc()).all():
                        if akthdr._recid in akthdr_obj_list:
                            continue
                        else:
                            akthdr_obj_list.append(akthdr._recid)


                        create_it()

    def create_it():

        nonlocal guest_name, q1_list_list, guest, akt_code, akt_kont, akthdr
        nonlocal inp_gastnr, next_date, to_date, all_flag, sflag, user_init


        nonlocal q1_list
        nonlocal q1_list_list


        q1_list = Q1_list()
        q1_list_list.append(q1_list)

        q1_list.guest_name = guest.name
        q1_list.anredefirma = guest.anredefirma
        q1_list.akt_kont_name = akt_kont.name
        q1_list.vorname = akt_kont.vorname
        q1_list.anrede = akt_kont.anrede
        q1_list.flag = akthdr.flag
        q1_list.akthdr_bezeich = akthdr.bezeich
        q1_list.akt_code_bezeich = akt_code.bezeich
        q1_list.t_betrag =  to_decimal(akthdr.t_betrag)
        q1_list.erl_datum = akthdr.erl_datum
        q1_list.userinit = akthdr.userinit
        q1_list.chg_id = akthdr.chg_id
        q1_list.chg_datum = akthdr.chg_datum
        q1_list.aktnr = akthdr.aktnr
        q1_list.akthdr_recid = akthdr._recid


    if inp_gastnr != 0:

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == inp_gastnr)).first()
        guest_name = guest.name

    if next_date == None:
        disp_all()
    else:
        disp_it()

    return generate_output()