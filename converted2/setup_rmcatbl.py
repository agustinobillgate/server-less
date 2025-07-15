#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Zimkateg, Ratecode, Zimmer

t_queasy_data, T_queasy = create_model_like(Queasy)

def setup_rmcatbl(i_case:int, t_queasy_data:[T_queasy], t_bezeich:[string], t_code:[string]):

    prepare_cache ([Ratecode, Zimmer])

    error_code = 0
    msg_str = ""
    queasy = zimkateg = ratecode = zimmer = None

    t_queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_code, msg_str, queasy, zimkateg, ratecode, zimmer
        nonlocal i_case, t_bezeich, t_code


        nonlocal t_queasy

        return {"error_code": error_code, "msg_str": msg_str}

    def add_rmcat():

        nonlocal error_code, msg_str, queasy, zimkateg, ratecode, zimmer
        nonlocal i_case, t_bezeich, t_code


        nonlocal t_queasy

        curr_i:int = 0
        curr_zikat:int = 0
        curr_categ:int = 1
        zbuff = None
        Zbuff =  create_buffer("Zbuff",Zimkateg)

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 152) & ((Queasy.char1 == t_queasy.char1)) | ((Queasy.char3 == t_queasy.char3))).first()

        if queasy:
            msg_str = queasy.char3 + " - " + queasy.char1
            error_code = 1

            return
        for curr_i in range(1,8 + 1) :

            if t_bezeich[curr_i - 1] != "":

                zimkateg = db_session.query(Zimkateg).filter(
                         ((Zimkateg.bezeichnung == t_bezeich[curr_i - 1])) | ((Zimkateg.kurzbez == t_code[curr_i - 1]))).first()

                if zimkateg:
                    msg_str = zimkateg.bezeichnung + " - " + zimkateg.kurzbez
                    error_code = 2

                    return

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 152)).order_by(Queasy.number1.desc()).yield_per(100):
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

                    curr_recid = zbuff._recid
                    zbuff = db_session.query(Zbuff).filter(
                             (Zbuff.zikatnr == curr_zikat) & (Zbuff._recid > curr_recid)).first()
                zimkateg = Zimkateg()
                db_session.add(zimkateg)

                zimkateg.zikatnr = curr_zikat
                zimkateg.kurzbez = t_code[curr_i - 1]
                zimkateg.bezeichnung = t_bezeich[curr_i - 1]
                zimkateg.typ = curr_categ
                zimkateg.overbooking = 0
                zimkateg.verfuegbarkeit = True
                zimkateg.active = True
                zimkateg.zibelstat = True


    def modify_rmcat():

        nonlocal error_code, msg_str, queasy, zimkateg, ratecode, zimmer
        nonlocal i_case, t_bezeich, t_code


        nonlocal t_queasy

        curr_i:int = 0
        curr_zikat:int = 0
        foundflag:bool = False
        currcode:string = None
        zbuff = None
        Zbuff =  create_buffer("Zbuff",Zimkateg)

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 152) & (((Queasy.char1 == t_queasy.char1)) | ((Queasy.char3 == t_queasy.char3))) & ((Queasy.number1 != t_queasy.number1))).first()

        if queasy:
            msg_str = queasy.char3 + " - " + queasy.char1
            error_code = 11

            return
        for curr_i in range(1,8 + 1) :

            if t_bezeich[curr_i - 1] != "":

                zimkateg = db_session.query(Zimkateg).filter(
                         (((Zimkateg.bezeichnung == t_bezeich[curr_i - 1])) | ((Zimkateg.kurzbez == t_code[curr_i - 1]))) & (Zimkateg.typ != t_queasy.number1)).first()

                if zimkateg:
                    msg_str = zimkateg.bezeichnung + " - " + zimkateg.kurzbez
                    error_code = 12

                    return

        ratecode_obj_list = {}
        for ratecode, zimkateg in db_session.query(Ratecode, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Ratecode.zikatnr) & (Zimkateg.typ == t_queasy.number1)).order_by(Ratecode.code).all():
            if ratecode_obj_list.get(ratecode._recid):
                continue
            else:
                ratecode_obj_list[ratecode._recid] = True

            if currcode != ratecode.code:
                currcode = ratecode.code
                foundflag = False


                for curr_i in range(1,8 + 1) :

                    if zimkateg.kurzbez == t_code[curr_i - 1]:
                        foundflag = True
                        break

                if not foundflag:
                    msg_str = zimkateg.kurzbez + " - " + ratecode.code
                    error_code = 13

                    return

        for zimkateg in db_session.query(Zimkateg).filter(
                 (Zimkateg.typ == queasy.number1)).order_by(Zimkateg._recid).all():
            foundflag = False


            for curr_i in range(1,8 + 1) :

                if zimkateg.kurzbez == t_code[curr_i - 1]:
                    foundflag = True
                    break

            if foundflag:

                zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zimkateg.zikatnr)]})

                if zimmer:
                    msg_str = zimkateg.kurzbez + " - " + zimmer.zinr
                    error_code = 14

                    return

        queasy = get_cache (Queasy, {"key": [(eq, 152)],"number1": [(eq, t_queasy.number1)]})

        if queasy:
            buffer_copy(t_queasy, queasy)
            pass

        zimkateg = get_cache (Zimkateg, {"typ": [(eq, queasy.number1)]})
        while None != zimkateg:

            zbuff = db_session.query(Zbuff).filter(
                         (Zbuff._recid == zimkateg._recid)).first()
            db_session.delete(zbuff)
            pass

            curr_recid = zimkateg._recid
            zimkateg = db_session.query(Zimkateg).filter(
                     (Zimkateg.typ == queasy.number1) & (Zimkateg._recid > curr_recid)).first()
        for curr_i in range(1,8 + 1) :

            if t_bezeich[curr_i - 1] != "":
                curr_zikat = 1

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, curr_zikat)]})
                while None != zimkateg:
                    curr_zikat = curr_zikat + 1

                    curr_recid = zimkateg._recid
                    zimkateg = db_session.query(Zimkateg).filter(
                             (Zimkateg.zikatnr == curr_zikat) & (Zimkateg._recid > curr_recid)).first()
                zimkateg = Zimkateg()
                db_session.add(zimkateg)

                zimkateg.zikatnr = curr_zikat
                zimkateg.kurzbez = t_code[curr_i - 1]
                zimkateg.bezeichnung = t_bezeich[curr_i - 1]
                zimkateg.typ = t_queasy.number1
                zimkateg.overbooking = 0
                zimkateg.verfuegbarkeit = True
                zimkateg.active = True
                zimkateg.zibelstat = True


                pass
                pass


    def delete_rmcat():

        nonlocal error_code, msg_str, queasy, zimkateg, ratecode, zimmer
        nonlocal i_case, t_bezeich, t_code


        nonlocal t_queasy

        curr_i:int = 0
        curr_zikat:int = 0
        foundflag:bool = False
        currcode:string = None
        zbuff = None
        Zbuff =  create_buffer("Zbuff",Zimkateg)

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 152) & ((Queasy.char1 == t_queasy.char1)) | ((Queasy.char3 == t_queasy.char3))).first()

        if not queasy:

            return

        for zimkateg in db_session.query(Zimkateg).filter(
                 (Zimkateg.typ == queasy.number1)).order_by(Zimkateg._recid).all():

            zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zimkateg.zikatnr)]})

            if zimmer:
                error_code = 21
                msg_str = zimkateg.kurzbez + " - " + zimmer.zinr

                return

        ratecode_obj_list = {}
        for ratecode, zimkateg in db_session.query(Ratecode, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Ratecode.zikatnr) & (Zimkateg.typ == t_queasy.number1)).order_by(Ratecode.code).all():
            if ratecode_obj_list.get(ratecode._recid):
                continue
            else:
                ratecode_obj_list[ratecode._recid] = True

            if currcode != ratecode.code:
                currcode = ratecode.code
                foundflag = False


                for curr_i in range(1,8 + 1) :

                    if zimkateg.kurzbez == t_code[curr_i - 1]:
                        foundflag = True
                        break

                if foundflag:
                    msg_str = zimkateg.kurzbez + " - " + ratecode.code
                    error_code = 22

                    return

        zimkateg = get_cache (Zimkateg, {"typ": [(eq, queasy.number1)]})
        while None != zimkateg:

            zbuff = db_session.query(Zbuff).filter(
                         (Zbuff._recid == zimkateg._recid)).first()
            db_session.delete(zbuff)
            pass

            curr_recid = zimkateg._recid
            zimkateg = db_session.query(Zimkateg).filter(
                     (Zimkateg.typ == queasy.number1) & (Zimkateg._recid > curr_recid)).first()
        pass
        db_session.delete(queasy)
        pass


    t_queasy = query(t_queasy_data, first=True)

    if i_case == 1:
        add_rmcat()
    elif i_case == 2:
        modify_rmcat()
    elif i_case == 3:
        delete_rmcat()

    return generate_output()