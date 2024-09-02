from functions.additional_functions import *
import decimal
from models import Queasy, Zimkateg, Ratecode, Zimmer

def setup_rmcatbl(i_case:int, t_queasy:[T_queasy], t_bezeich:str, t_code:str):
    error_code = 0
    msg_str = ""
    queasy = zimkateg = ratecode = zimmer = None

    t_queasy = zbuff = None

    t_queasy_list, T_queasy = create_model_like(Queasy)

    Zbuff = Zimkateg

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_code, msg_str, queasy, zimkateg, ratecode, zimmer
        nonlocal zbuff


        nonlocal t_queasy, zbuff
        nonlocal t_queasy_list
        return {"error_code": error_code, "msg_str": msg_str}

    def add_rmcat():

        nonlocal error_code, msg_str, queasy, zimkateg, ratecode, zimmer
        nonlocal zbuff


        nonlocal t_queasy, zbuff
        nonlocal t_queasy_list

        curr_i:int = 0
        curr_zikat:int = 0
        curr_categ:int = 1
        Zbuff = Zimkateg

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 152) &  ((Queasy.char1 == t_Queasy.char1)) |  ((Queasy.char3 == t_Queasy.char3))).first()

        if queasy:
            msg_str = queasy.char3 + " - " + queasy.char1
            error_code = 1

            return
        for curr_i in range(1,8 + 1) :

            if t_bezeich[curr_i - 1] != "":

                zimkateg = db_session.query(Zimkateg).filter(
                        ((Zimkateg.bezeichnung == t_bezeich[curr_i - 1])) |  ((Zimkateg.kurzbez == t_code[curr_i - 1]))).first()

                if zimkateg:
                    msg_str = zimkateg.bezeichnung + " - " + zimkateg.kurzbez
                    error_code = 2

                    return

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 152)).all():
            curr_categ = queasy.number1 + 1
            break
        queasy = Queasy()
        db_session.add(queasy)

        buffer_copy(t_queasy, queasy,except_fields=["number1"])
        queasy.number1 = curr_categ


        for curr_i in range(1,8 + 1) :

            if t_bezeich[curr_i - 1] != "":
                curr_zikat = 1

                zbuff = db_session.query(Zbuff).filter(
                        (Zbuff.zikatnr == curr_zikat)).first()
                while None != zbuff:
                    curr_zikat = curr_zikat + 1

                    zbuff = db_session.query(Zbuff).filter(
                            (Zbuff.zikatnr == curr_zikat)).first()
                zimkateg = Zimkateg()
                db_session.add(zimkateg)

                zimkateg.zikatnr = curr_zikat
                zimkateg.kurzbez = t_code[curr_i - 1]
                zimkateg.bezeich = t_bezeich[curr_i - 1]
                zimkateg.typ = curr_categ
                zimkateg.overbooking = 0
                zimkateg.verfuegbarkeit = True
                zimkateg.ACTIVE = True
                zimkateg.zibelstat = True

    def modify_rmcat():

        nonlocal error_code, msg_str, queasy, zimkateg, ratecode, zimmer
        nonlocal zbuff


        nonlocal t_queasy, zbuff
        nonlocal t_queasy_list

        curr_i:int = 0
        curr_zikat:int = 0
        foundflag:bool = False
        currcode:str = None
        Zbuff = Zimkateg

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 152) &  (((Queasy.char1 == t_Queasy.char1)) |  ((Queasy.char3 == t_Queasy.char3))) &  ((Queasy.number1 != t_Queasy.number1))).first()

        if queasy:
            msg_str = queasy.char3 + " - " + queasy.char1
            error_code = 11

            return
        for curr_i in range(1,8 + 1) :

            if t_bezeich[curr_i - 1] != "":

                zimkateg = db_session.query(Zimkateg).filter(
                        (((Zimkateg.bezeichnung == t_bezeich[curr_i - 1])) |  ((Zimkateg.kurzbez == t_code[curr_i - 1]))) &  (Zimkateg.typ != t_queasy.number1)).first()

                if zimkateg:
                    msg_str = zimkateg.bezeichnung + " - " + zimkateg.kurzbez
                    error_code = 12

                    return

        ratecode_obj_list = []
        for ratecode, zimkateg in db_session.query(Ratecode, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Ratecode.zikatnr) &  (Zimkateg.typ == t_queasy.number1)).all():
            if ratecode._recid in ratecode_obj_list:
                continue
            else:
                ratecode_obj_list.append(ratecode._recid)

            if currcode != ratecode.CODE:
                currcode = ratecode.CODE
                foundflag = False


                for curr_i in range(1,8 + 1) :

                    if zimkateg.kurzbez == t_code[curr_i - 1]:
                        foundflag = True
                        break

                if not foundflag:
                    msg_str = zimkateg.kurzbez + " - " + ratecode.CODE
                    error_code = 13

                    return

        for zimkateg in db_session.query(Zimkateg).filter(
                (Zimkateg.typ == queasy.number1)).all():
            foundflag = False


            for curr_i in range(1,8 + 1) :

                if zimkateg.kurzbez == t_code[curr_i - 1]:
                    foundflag = True
                    break

            if foundflag:

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zikatnr == zimkateg.zikatnr)).first()

                if zimmer:
                    msg_str = zimkateg.kurzbez + " - " + zimmer.zinr
                    error_code = 14

                    return

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 152) &  (Queasy.number1 == t_Queasy.number1)).first()

        if queasy:
            buffer_copy(t_queasy, queasy)

            queasy = db_session.query(Queasy).first()

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.typ == queasy.number1)).first()
        while None != zimkateg:

            zbuff = db_session.query(Zbuff).filter(
                        (Zbuff._recid == zimkateg._recid)).first()
            db_session.delete(zbuff)


            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.typ == queasy.number1)).first()
        for curr_i in range(1,8 + 1) :

            if t_bezeich[curr_i - 1] != "":
                curr_zikat = 1

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == curr_zikat)).first()
                while None != zimkateg:
                    curr_zikat = curr_zikat + 1

                    zimkateg = db_session.query(Zimkateg).filter(
                            (Zimkateg.zikatnr == curr_zikat)).first()
                zimkateg = Zimkateg()
                db_session.add(zimkateg)

                zimkateg.zikatnr = curr_zikat
                zimkateg.kurzbez = t_code[curr_i - 1]
                zimkateg.bezeich = t_bezeich[curr_i - 1]
                zimkateg.typ = t_queasy.number1
                zimkateg.overbooking = 0
                zimkateg.verfuegbarkeit = True
                zimkateg.ACTIVE = True
                zimkateg.zibelstat = True

                zimkateg = db_session.query(Zimkateg).first()


    def delete_rmcat():

        nonlocal error_code, msg_str, queasy, zimkateg, ratecode, zimmer
        nonlocal zbuff


        nonlocal t_queasy, zbuff
        nonlocal t_queasy_list

        curr_i:int = 0
        curr_zikat:int = 0
        foundflag:bool = False
        currcode:str = None
        Zbuff = Zimkateg

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 152) &  ((Queasy.char1 == t_Queasy.char1)) |  ((Queasy.char3 == t_Queasy.char3))).first()

        if not queasy:

            return

        for zimkateg in db_session.query(Zimkateg).filter(
                (Zimkateg.typ == queasy.number1)).all():

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zikatnr == zimkateg.zikatnr)).first()

            if zimmer:
                error_code = 21
                msg_str = zimkateg.kurzbez + " - " + zimmer.zinr

                return

        ratecode_obj_list = []
        for ratecode, zimkateg in db_session.query(Ratecode, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Ratecode.zikatnr) &  (Zimkateg.typ == t_queasy.number1)).all():
            if ratecode._recid in ratecode_obj_list:
                continue
            else:
                ratecode_obj_list.append(ratecode._recid)

            if currcode != ratecode.CODE:
                currcode = ratecode.CODE
                foundflag = False


                for curr_i in range(1,8 + 1) :

                    if zimkateg.kurzbez == t_code[curr_i - 1]:
                        foundflag = True
                        break

                if foundflag:
                    msg_str = zimkateg.kurzbez + " - " + ratecode.CODE
                    error_code = 22

                    return

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.typ == queasy.number1)).first()
        while None != zimkateg:

            zbuff = db_session.query(Zbuff).filter(
                        (Zbuff._recid == zimkateg._recid)).first()
            db_session.delete(zbuff)

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.typ == queasy.number1)).first()

        queasy = db_session.query(Queasy).first()
        db_session.delete(queasy)

    t_queasy = query(t_queasy_list, first=True)

    if i_case == 1:
        add_rmcat()
    elif i_case == 2:
        modify_rmcat()
    elif i_case == 3:
        delete_rmcat()

    return generate_output()