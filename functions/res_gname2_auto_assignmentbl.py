#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Zimmer, Outorder

s_list_data, S_list = create_model("S_list", {"res_recid":int, "resstatus":int, "active_flag":int, "flag":int, "karteityp":int, "zimmeranz":int, "erwachs":int, "kind1":int, "kind2":int, "old_zinr":string, "name":string, "nat":string, "land":string, "zinr":string, "eta":string, "etd":string, "flight1":string, "flight2":string, "rmcat":string, "ankunft":date, "abreise":date, "zipreis":Decimal, "bemerk":string})

def res_gname2_auto_assignmentbl(s_list_data:[S_list], location:string, froom:string, troom:string):

    prepare_cache ([Res_line])

    res_line = zimmer = outorder = None

    s_list = s1_list = s2_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_line, zimmer, outorder
        nonlocal location, froom, troom


        nonlocal s_list, s1_list, s2_list

        return {"s-list": s_list_data}

    def auto_assignment():

        nonlocal res_line, zimmer, outorder
        nonlocal location, froom, troom


        nonlocal s_list, s1_list, s2_list

        rline = None
        resline = None
        last_zinr:string = ""
        do_it:bool = False
        found:bool = False
        S1_list = S_list
        s1_list_data = s_list_data
        S2_list = S_list
        s2_list_data = s_list_data
        Rline =  create_buffer("Rline",Res_line)
        Resline =  create_buffer("Resline",Res_line)

        for s1_list in query(s1_list_data, filters=(lambda s1_list: s1_list.zinr == "" and s1_list.resstatus != 11 and s1_list.zimmeranz == 1)):

            rline = get_cache (Res_line, {"_recid": [(eq, s1_list.res_recid)]})
            found = False

            if location != "":

                zimmer = get_cache (Zimmer, {"code": [(eq, location)],"zinr": [(ge, froom),(le, troom),(gt, last_zinr)],"zikatnr": [(eq, rline.zikatnr)],"setup": [(eq, rline.setup)]})
            else:

                zimmer = get_cache (Zimmer, {"zinr": [(ge, froom),(le, troom),(gt, last_zinr)],"zikatnr": [(eq, rline.zikatnr)],"setup": [(eq, rline.setup)]})
            while None != zimmer and not found:
                do_it = True

                if zimmer.etage > 0 and (zimmer.etage != zimmer.etage):
                    do_it = False

                if do_it:

                    outorder = db_session.query(Outorder).filter(
                             (Outorder.zinr == zimmer.zinr) & (Outorder.betriebsnr != rline.resnr) & (((rline.ankunft >= gespstart) & (rline.ankunft <= Outorder.gespende)) | ((rline.abreise > gespstart) & (rline.abreise <= Outorder.gespende)) | ((Outorder.gespstart >= rline.ankunft) & (Outorder.gespstart < rline.abreise)) | ((Outorder.gespende >= rline.ankunft) & (Outorder.gespende <= rline.abreise)))).first()

                    if outorder:
                        do_it = False

                if do_it:

                    resline = db_session.query(Resline).filter(
                             (Resline._recid != rline._recid) & (Resline.resstatus <= 6) & (Resline.active_flag <= 1) & (Resline.zinr == zimmer.zinr) & (((rline.ankunft >= Resline.ankunft) & (rline.ankunft < Resline.abreise)) | ((rline.abreise > Resline.ankunft) & (rline.abreise <= Resline.abreise)) | ((Resline.ankunft >= rline.ankunft) & (Resline.ankunft < rline.abreise)) | ((Resline.abreise > rline.ankunft) & (Resline.abreise <= rline.abreise)))).first()

                    if resline:
                        do_it = False

                if do_it:
                    s1_list.zinr = zimmer.zinr
                    last_zinr = zimmer.zinr
                    found = True
                else:

                    if location != "":

                        curr_recid = zimmer._recid
                        zimmer = db_session.query(Zimmer).filter(
                                 (Zimmer.code == (location).lower()) & (Zimmer.zinr >= (froom).lower()) & (Zimmer.zinr <= (troom).lower()) & (Zimmer.zikatnr == rline.zikatnr) & (Zimmer.setup == rline.setup) & (Zimmer.zinr > (last_zinr).lower()) & (Zimmer._recid > curr_recid)).first()
                    else:

                        curr_recid = zimmer._recid
                        zimmer = db_session.query(Zimmer).filter(
                                 (Zimmer.zinr >= (froom).lower()) & (Zimmer.zinr <= (troom).lower()) & (Zimmer.zikatnr == rline.zikatnr) & (Zimmer.setup == rline.setup) & (Zimmer.zinr > (last_zinr).lower()) & (Zimmer._recid > curr_recid)).first()
        last_zinr = ""

        for s1_list in query(s1_list_data, filters=(lambda s1_list: s1_list.zinr == "" and s1_list.active_flag == 0 and s1_list.resstatus != 11)):

            rline = get_cache (Res_line, {"_recid": [(eq, s1_list.res_recid)]})
            found = False

            if location != "":

                zimmer = get_cache (Zimmer, {"code": [(eq, location)],"zinr": [(ge, froom),(le, troom),(gt, last_zinr)],"zikatnr": [(eq, rline.zikatnr)],"setup": [(ne, rline.setup)]})
            else:

                zimmer = get_cache (Zimmer, {"zinr": [(ge, froom),(le, troom),(gt, last_zinr)],"zikatnr": [(eq, rline.zikatnr)],"setup": [(ne, rline.setup)]})
            while None != zimmer and not found:
                do_it = True

                if zimmer.etage > 0 and (zimmer.etage != zimmer.etage):
                    do_it = False

                if do_it:

                    outorder = db_session.query(Outorder).filter(
                             (Outorder.zinr == zimmer.zinr) & (Outorder.betriebsnr != rline.resnr) & (((rline.ankunft >= gespstart) & (rline.ankunft <= Outorder.gespende)) | ((rline.abreise > gespstart) & (rline.abreise <= Outorder.gespende)) | ((Outorder.gespstart >= rline.ankunft) & (Outorder.gespstart < rline.abreise)) | ((Outorder.gespende >= rline.ankunft) & (Outorder.gespende <= rline.abreise)))).first()

                    if outorder:
                        do_it = False

                if do_it:

                    resline = db_session.query(Resline).filter(
                             (Resline._recid != rline._recid) & (Resline.resstatus <= 6) & (Resline.active_flag <= 1) & (Resline.zinr == zimmer.zinr) & (((rline.ankunft >= Resline.ankunft) & (rline.ankunft < Resline.abreise)) | ((rline.abreise > Resline.ankunft) & (rline.abreise <= Resline.abreise)) | ((Resline.ankunft >= rline.ankunft) & (Resline.ankunft < rline.abreise)) | ((Resline.abreise > rline.ankunft) & (Resline.abreise <= rline.abreise)))).first()

                    if resline:
                        do_it = False

                if do_it:

                    s2_list = query(s2_list_data, filters=(lambda s2_list: s2_list.zinr == zimmer.zinr), first=True)

                    if s2_list:
                        do_it = False

                if do_it:
                    s1_list.zinr = zimmer.zinr
                    last_zinr = zimmer.zinr
                    found = True
                else:

                    if location != "":

                        curr_recid = zimmer._recid
                        zimmer = db_session.query(Zimmer).filter(
                                 (Zimmer.code == (location).lower()) & (Zimmer.zinr >= (froom).lower()) & (Zimmer.zinr <= (troom).lower()) & (Zimmer.zikatnr == rline.zikatnr) & (Zimmer.setup != rline.setup) & (Zimmer.zinr > (last_zinr).lower()) & (Zimmer._recid > curr_recid)).first()
                    else:

                        curr_recid = zimmer._recid
                        zimmer = db_session.query(Zimmer).filter(
                                 (Zimmer.zinr >= (froom).lower()) & (Zimmer.zinr <= (troom).lower()) & (Zimmer.zikatnr == rline.zikatnr) & (Zimmer.setup != rline.setup) & (Zimmer.zinr > (last_zinr).lower()) & (Zimmer._recid > curr_recid)).first()

    auto_assignment()

    return generate_output()