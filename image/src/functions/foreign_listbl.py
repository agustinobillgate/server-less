from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.read_queasybl import read_queasybl
from models import Queasy, Guest, Res_line

def foreign_listbl(fdate:date, ci_date:date, all_nat:bool, sorttype:int, def_nat:str):
    t_foreign_list_list = []
    queasy = guest = res_line = None

    t_foreign_list = t_queasy = None

    t_foreign_list_list, T_foreign_list = create_model("T_foreign_list", {"name":str, "nation1":str, "ausweis_nr1":str, "geburtdatum1":date, "zinr":str, "ankunft":date, "abreise":date, "adresse1":str, "wohnort":str, "land":str, "email_adr":str, "ankzeit":int, "abreisezeit":int, "resstatus":int, "erwachs":int, "kind1":int, "gratis":int, "remark":str, "i_purpose":str, "gender":str, "telefon":str})
    t_queasy_list, T_queasy = create_model_like(Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_foreign_list_list, queasy, guest, res_line


        nonlocal t_foreign_list, t_queasy
        nonlocal t_foreign_list_list, t_queasy_list
        return {"t-foreign-list": t_foreign_list_list}

    def create_foreign_list():

        nonlocal t_foreign_list_list, queasy, guest, res_line


        nonlocal t_foreign_list, t_queasy
        nonlocal t_foreign_list_list, t_queasy_list

        i:int = 0
        str:str = ""
        purpose:int = 0
        t_foreign_list = T_foreign_list()
        t_foreign_list_list.append(t_foreign_list)

        t_foreign_list.name = res_line.name
        t_foreign_list.nation1 = guest.nation1
        t_foreign_list.ausweis_nr1 = guest.ausweis_nr1
        t_foreign_list.geburtdatum1 = guest.geburtdatum1
        t_foreign_list.zinr = res_line.zinr
        t_foreign_list.ankunft = res_line.ankunft
        t_foreign_list.abreise = res_line.abreise
        t_foreign_list.adresse1 = guest.adresse1
        t_foreign_list.wohnort = guest.wohnort
        t_foreign_list.land = guest.land
        t_foreign_list.email_adr = guest.email_adr
        t_foreign_list.ankzeit = res_line.ankzeit
        t_foreign_list.abreisezeit = res_line.abreisezeit
        t_foreign_list.resstatus = res_line.resstatus
        t_foreign_list.erwachs = res_line.erwachs
        t_foreign_list.kind1 = res_line.kind1
        t_foreign_list.gratis = res_line.gratis
        t_foreign_list.remark = guest.bemerkung
        t_foreign_list.telefon = guest.telefon


        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(i - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 8) == "SEGM__PUR":
                purpose = to_int(substring(str, 8))

            if purpose != 0:
                t_queasy_list = get_output(read_queasybl(1, 143, purpose, None))

                t_queasy = query(t_queasy_list, first=True)

                if t_queasy:
                    t_foreign_list.i_purpose = t_queasy.char3


    if fdate == ci_date:

        if not all_nat:

            if sorttype == 1:

                res_line_obj_list = []
                for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnrmember) &  (func.lower(Guest.nation1) != (def_nat).lower())).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.active_flag == 1)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    create_foreign_list()

            elif sorttype == 2:

                res_line_obj_list = []
                for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnrmember) &  (func.lower(Guest.nation1) != (def_nat).lower())).filter(
                        (Res_line.resstatus == 8) &  (Res_line.active_flag == 2) &  (Res_line.abreise == fdate)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    create_foreign_list()

            elif sorttype == 3:

                res_line_obj_list = []
                for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnrmember) &  (func.lower(Guest.nation1) != (def_nat).lower())).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.active_flag == 1) &  (Res_line.ankunft == fdate)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    create_foreign_list()
        else:

            if sorttype == 1:

                res_line_obj_list = []
                for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.active_flag == 1)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    create_foreign_list()

            elif sorttype == 2:

                res_line_obj_list = []
                for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.resstatus == 8) &  (Res_line.active_flag == 2) &  (Res_line.abreise == fdate)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    create_foreign_list()

            elif sorttype == 3:

                res_line_obj_list = []
                for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.active_flag == 1) &  (Res_line.ankunft == fdate)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    create_foreign_list()
    else:

        if not all_nat:

            if sorttype == 1:

                res_line_obj_list = []
                for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnrmember) &  (func.lower(Guest.nation1) != (def_nat).lower())).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13) |  (Res_line.resstatus == 8)) &  (Res_line.active_flag <= 2) &  (Res_line.ankunft <= fdate) &  (Res_line.abreise > fdate)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    create_foreign_list()

            elif sorttype == 2:

                res_line_obj_list = []
                for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnrmember) &  (func.lower(Guest.nation1) != (def_nat).lower())).filter(
                        (Res_line.resstatus == 8) &  (Res_line.active_flag == 2) &  (Res_line.abreise == fdate)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    create_foreign_list()

            elif sorttype == 3:

                res_line_obj_list = []
                for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnrmember) &  (func.lower(Guest.nation1) != (def_nat).lower())).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13) |  (Res_line.resstatus == 8)) &  (Res_line.active_flag <= 2) &  (Res_line.ankunft == fdate)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    create_foreign_list()
        else:

            if sorttype == 1:

                res_line_obj_list = []
                for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13) |  (Res_line.resstatus == 8)) &  (Res_line.active_flag <= 2) &  (Res_line.ankunft <= fdate) &  (Res_line.abreise > fdate)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    create_foreign_list()

            elif sorttype == 2:

                res_line_obj_list = []
                for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.resstatus == 8) &  (Res_line.active_flag == 2) &  (Res_line.abreise == fdate)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    create_foreign_list()

            elif sorttype == 3:

                res_line_obj_list = []
                for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13) |  (Res_line.resstatus == 8)) &  (Res_line.active_flag <= 2) &  (Res_line.ankunft == fdate)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    create_foreign_list()

    return generate_output()