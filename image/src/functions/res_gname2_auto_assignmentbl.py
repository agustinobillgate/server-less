from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Zimmer, Outorder

def res_gname2_auto_assignmentbl(s_list:[S_list], location:str, froom:str, troom:str):
    res_line = zimmer = outorder = None

    s_list = s1_list = s2_list = rline = resline = None

    s_list_list, S_list = create_model("S_list", {"res_recid":int, "resstatus":int, "active_flag":int, "flag":int, "karteityp":int, "zimmeranz":int, "erwachs":int, "kind1":int, "kind2":int, "old_zinr":str, "name":str, "nat":str, "land":str, "zinr":str, "eta":str, "etd":str, "flight1":str, "flight2":str, "rmcat":str, "ankunft":date, "abreise":date, "zipreis":decimal, "bemerk":str})

    S1_list = S_list
    s1_list_list = s_list_list

    S2_list = S_list
    s2_list_list = s_list_list

    Rline = Res_line
    Resline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_line, zimmer, outorder
        nonlocal s1_list, s2_list, rline, resline


        nonlocal s_list, s1_list, s2_list, rline, resline
        nonlocal s_list_list
        return {}

    def auto_assignment():

        nonlocal res_line, zimmer, outorder
        nonlocal s1_list, s2_list, rline, resline


        nonlocal s_list, s1_list, s2_list, rline, resline
        nonlocal s_list_list

        last_zinr:str = ""
        do_it:bool = False
        found:bool = False
        S1_list = S_list
        S2_list = S_list
        Rline = Res_line
        Resline = Res_line

        for s1_list in query(s1_list_list, filters=(lambda s1_list :s1_list.zinr == "" and s1_list.resstatus != 11 and s1_list.zimmeranz == 1)):

            rline = db_session.query(Rline).filter(
                    (Rline._recid == s1_list.res_recid)).first()
            found = False

            if location != "":

                zimmer = db_session.query(Zimmer).filter(
                        (func.lower(Zimmer.code) == (location).lower()) &  (func.lower(Zimmer.zinr) >= (froom).lower()) &  (func.lower(Zimmer.zinr) <= (troom).lower()) &  (Zimmer.zikatnr == rline.zikatnr) &  (Zimmer.setup == rline.setup) &  (func.lower(Zimmer.zinr) > (last_zinr).lower())).first()
            else:

                zimmer = db_session.query(Zimmer).filter(
                        (func.lower(Zimmer.zinr) >= (froom).lower()) &  (func.lower(Zimmer.zinr) <= (troom).lower()) &  (Zimmer.zikatnr == rline.zikatnr) &  (Zimmer.setup == rline.setup) &  (func.lower(Zimmer.zinr) > (last_zinr).lower())).first()
            while None != zimmer and not found:
                do_it = True

                if zimmer.etage > 0 and (zimmer.etage != zimmer.etage):
                    do_it = False

                if do_it:

                    outorder = db_session.query(Outorder).filter(
                            (Outorder.zinr == zimmer.zinr) &  (Outorder.betriebsnr != rline.resnr) &  (((rline.ankunft >= gespstart) &  (rline.ankunft <= gespende)) |  ((rline.abreise > gespstart) &  (rline.abreise <= gespende)) |  ((Outorder.gespstart >= rline.ankunft) &  (Outorder.gespstart < rline.abreise)) |  ((Outorder.gespende >= rline.ankunft) &  (Outorder.gespende <= rline.abreise)))).first()

                    if outorder:
                        do_it = False

                if do_it:

                    resline = db_session.query(Resline).filter(
                            (Resline._recid != rline._recid) &  (Resline.resstatus <= 6) &  (Resline.active_flag <= 1) &  (Resline.zinr == zimmer.zinr) &  (((rline.ankunft >= Resline.ankunft) &  (rline.ankunft < Resline.abreise)) |  ((rline.abreise > Resline.ankunft) &  (rline.abreise <= Resline.abreise)) |  ((Resline.ankunft >= rline.ankunft) &  (Resline.ankunft < rline.abreise)) |  ((Resline.abreise > rline.ankunft) &  (Resline.abreise <= rline.abreise)))).first()

                    if resline:
                        do_it = False

                if do_it:
                    s1_list.zinr = zimmer.zinr
                    last_zinr = zimmer.zinr
                    found = True
                else:

                    if location != "":

                        zimmer = db_session.query(Zimmer).filter(
                                (func.lower(Zimmer.code) == (location).lower()) &  (func.lower(Zimmer.zinr) >= (froom).lower()) &  (func.lower(Zimmer.zinr) <= (troom).lower()) &  (Zimmer.zikatnr == rline.zikatnr) &  (Zimmer.setup == rline.setup) &  (func.lower(Zimmer.zinr) > (last_zinr).lower())).first()
                    else:

                        zimmer = db_session.query(Zimmer).filter(
                                (func.lower(Zimmer.zinr) >= (froom).lower()) &  (func.lower(Zimmer.zinr) <= (troom).lower()) &  (Zimmer.zikatnr == rline.zikatnr) &  (Zimmer.setup == rline.setup) &  (func.lower(Zimmer.zinr) > (last_zinr).lower())).first()
        last_zinr = ""

        for s1_list in query(s1_list_list, filters=(lambda s1_list :s1_list.zinr == "" and s1_list.active_flag == 0 and s1_list.resstatus != 11)):

            rline = db_session.query(Rline).filter(
                    (Rline._recid == s1_list.res_recid)).first()
            found = False

            if location != "":

                zimmer = db_session.query(Zimmer).filter(
                        (func.lower(Zimmer.code) == (location).lower()) &  (func.lower(Zimmer.zinr) >= (froom).lower()) &  (func.lower(Zimmer.zinr) <= (troom).lower()) &  (Zimmer.zikatnr == rline.zikatnr) &  (Zimmer.setup != rline.setup) &  (func.lower(Zimmer.zinr) > (last_zinr).lower())).first()
            else:

                zimmer = db_session.query(Zimmer).filter(
                        (func.lower(Zimmer.zinr) >= (froom).lower()) &  (func.lower(Zimmer.zinr) <= (troom).lower()) &  (Zimmer.zikatnr == rline.zikatnr) &  (Zimmer.setup != rline.setup) &  (func.lower(Zimmer.zinr) > (last_zinr).lower())).first()
            while None != zimmer and not found:
                do_it = True

                if zimmer.etage > 0 and (zimmer.etage != zimmer.etage):
                    do_it = False

                if do_it:

                    outorder = db_session.query(Outorder).filter(
                            (Outorder.zinr == zimmer.zinr) &  (Outorder.betriebsnr != rline.resnr) &  (((rline.ankunft >= gespstart) &  (rline.ankunft <= gespende)) |  ((rline.abreise > gespstart) &  (rline.abreise <= gespende)) |  ((Outorder.gespstart >= rline.ankunft) &  (Outorder.gespstart < rline.abreise)) |  ((Outorder.gespende >= rline.ankunft) &  (Outorder.gespende <= rline.abreise)))).first()

                    if outorder:
                        do_it = False

                if do_it:

                    resline = db_session.query(Resline).filter(
                            (Resline._recid != rline._recid) &  (Resline.resstatus <= 6) &  (Resline.active_flag <= 1) &  (Resline.zinr == zimmer.zinr) &  (((rline.ankunft >= Resline.ankunft) &  (rline.ankunft < Resline.abreise)) |  ((rline.abreise > Resline.ankunft) &  (rline.abreise <= Resline.abreise)) |  ((Resline.ankunft >= rline.ankunft) &  (Resline.ankunft < rline.abreise)) |  ((Resline.abreise > rline.ankunft) &  (Resline.abreise <= rline.abreise)))).first()

                    if resline:
                        do_it = False

                if do_it:

                    s2_list = query(s2_list_list, filters=(lambda s2_list :s2_list.zinr == zimmer.zinr), first=True)

                    if s2_list:
                        do_it = False

                if do_it:
                    s1_list.zinr = zimmer.zinr
                    last_zinr = zimmer.zinr
                    found = True
                else:

                    if location != "":

                        zimmer = db_session.query(Zimmer).filter(
                                (func.lower(Zimmer.code) == (location).lower()) &  (func.lower(Zimmer.zinr) >= (froom).lower()) &  (func.lower(Zimmer.zinr) <= (troom).lower()) &  (Zimmer.zikatnr == rline.zikatnr) &  (Zimmer.setup != rline.setup) &  (func.lower(Zimmer.zinr) > (last_zinr).lower())).first()
                    else:

                        zimmer = db_session.query(Zimmer).filter(
                                (func.lower(Zimmer.zinr) >= (froom).lower()) &  (func.lower(Zimmer.zinr) <= (troom).lower()) &  (Zimmer.zikatnr == rline.zikatnr) &  (Zimmer.setup != rline.setup) &  (func.lower(Zimmer.zinr) > (last_zinr).lower())).first()


    auto_assignment()

    return generate_output()