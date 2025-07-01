#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Kontline, Bediener, Zimkateg, Res_line

def allotmentbl(case_type:int, gastnr:int, kon_gastnr:int, kontcode:string, ankunft:date, abreise:date, zimmeranz:int):

    prepare_cache ([Bediener, Zimkateg, Res_line])

    allotment_list_list = []
    check_resline_list_list = []
    allot_list_list = []
    s_list_list = []
    d1:date = None
    d2:date = None
    datum:date = None
    d:date = None
    kontline = bediener = zimkateg = res_line = None

    allotment_list = check_resline_list = allot_list = s_list = None

    allotment_list_list, Allotment_list = create_model_like(Kontline, {"kurzbez":string, "userinit":string})
    check_resline_list_list, Check_resline_list = create_model("Check_resline_list", {"resnr":int, "name":string, "abreise":date, "ankunft":date})
    allot_list_list, Allot_list = create_model("Allot_list", {"datum":date, "anz":int})
    s_list_list, S_list = create_model("S_list", {"datum":date, "tag":string, "qty":int, "occ":int, "vac":int, "ovb":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal allotment_list_list, check_resline_list_list, allot_list_list, s_list_list, d1, d2, datum, d, kontline, bediener, zimkateg, res_line
        nonlocal case_type, gastnr, kon_gastnr, kontcode, ankunft, abreise, zimmeranz


        nonlocal allotment_list, check_resline_list, allot_list, s_list
        nonlocal allotment_list_list, check_resline_list_list, allot_list_list, s_list_list

        return {"allotment-list": allotment_list_list, "check-resline-list": check_resline_list_list, "allot-list": allot_list_list, "s-list": s_list_list}

    def assign_it():

        nonlocal allotment_list_list, check_resline_list_list, allot_list_list, s_list_list, d1, d2, datum, d, kontline, bediener, zimkateg, res_line
        nonlocal case_type, gastnr, kon_gastnr, kontcode, ankunft, abreise, zimmeranz


        nonlocal allotment_list, check_resline_list, allot_list, s_list
        nonlocal allotment_list_list, check_resline_list_list, allot_list_list, s_list_list

        kontline_obj_list = {}
        for kontline, bediener in db_session.query(Kontline, Bediener).join(Bediener,(Bediener.nr == Kontline.bediener_nr)).filter(
                 (Kontline.gastnr == gastnr) & (Kontline.kontignr > 0) & (Kontline.betriebsnr == 0) & (Kontline.kontstatus == 1)).order_by(Kontline.kontcode, Kontline.ankunft).all():
            if kontline_obj_list.get(kontline._recid):
                continue
            else:
                kontline_obj_list[kontline._recid] = True

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, kontline.zikatnr)]})
            allotment_list = Allotment_list()
            allotment_list_list.append(allotment_list)

            buffer_copy(kontline, allotment_list)
            allotment_list.userinit = bediener.userinit

            if zimkateg:
                allotment_list.kurzbez = zimkateg.kurzbez


    def check_resline():

        nonlocal allotment_list_list, check_resline_list_list, allot_list_list, s_list_list, d1, d2, datum, d, kontline, bediener, zimkateg, res_line
        nonlocal case_type, gastnr, kon_gastnr, kontcode, ankunft, abreise, zimmeranz


        nonlocal allotment_list, check_resline_list, allot_list, s_list
        nonlocal allotment_list_list, check_resline_list_list, allot_list_list, s_list_list

        res_line_obj_list = {}
        for res_line, kontline in db_session.query(Res_line, Kontline).join(Kontline,(Kontline.kontignr == Res_line.kontignr) & (Kontline.kontcode == (kontcode).lower()) & (Kontline.kontstatus == 1)).filter(
                 (Res_line.kontignr != 0) & (Res_line.gastnr == kon_gastnr) & (Res_line.active_flag < 2) & (Res_line.resstatus < 11)).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            if res_line.abreise <= kontline.ankunft or res_line.ankunft > kontline.abreise:
                pass
            else:
                check_resline_list = Check_resline_list()
                check_resline_list_list.append(check_resline_list)

                check_resline_list.resnr = res_line.resnr
                check_resline_list.name = res_line.name
                check_resline_list.abreise = res_line.abreise
                check_resline_list.ankunft = res_line.ankunft


    def check_allotment():

        nonlocal allotment_list_list, check_resline_list_list, allot_list_list, s_list_list, d1, d2, datum, d, kontline, bediener, zimkateg, res_line
        nonlocal case_type, gastnr, kon_gastnr, kontcode, ankunft, abreise, zimmeranz


        nonlocal allotment_list, check_resline_list, allot_list, s_list
        nonlocal allotment_list_list, check_resline_list_list, allot_list_list, s_list_list

        res_line_obj_list = {}
        for res_line, kontline in db_session.query(Res_line, Kontline).join(Kontline,(Kontline.kontignr == Res_line.kontignr) & (Kontline.kontcode == (kontcode).lower()) & (Kontline.kontstatus == 1)).filter(
                 (Res_line.kontignr != 0) & (Res_line.gastnr == gastnr) & (Res_line.active_flag < 2) & (Res_line.resstatus < 11) & (not_ (Res_line.ankunft > abreise)) & (not_ (Res_line.abreise < ankunft))).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            if res_line.ankunft >= ankunft:
                d1 = res_line.ankunft
            else:
                d1 = ankunft

            if res_line.abreise <= abreise:
                d2 = res_line.abreise - timedelta(days=1)
            else:
                d2 = abreise
            for datum in date_range(d1,d2) :

                allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.datum == datum), first=True)

                if not allot_list:
                    allot_list = Allot_list()
                    allot_list_list.append(allot_list)

                    allot_list.datum = datum
                    allot_list.anz = zimmeranz
                allot_list.anz = allot_list.anz - res_line.zimmeranz


    def create_slist():

        nonlocal allotment_list_list, check_resline_list_list, allot_list_list, s_list_list, d1, d2, datum, d, kontline, bediener, zimkateg, res_line
        nonlocal case_type, gastnr, kon_gastnr, kontcode, ankunft, abreise, zimmeranz


        nonlocal allotment_list, check_resline_list, allot_list, s_list
        nonlocal allotment_list_list, check_resline_list_list, allot_list_list, s_list_list

        weekdays:List[string] = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for d in date_range(ankunft,abreise) :
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.datum = d
            s_list.qty = zimmeranz
            s_list.vac = zimmeranz


            s_list.tag = weekdays[get_weekday(s_list.datum) - 1]

        res_line_obj_list = {}
        for res_line, kontline in db_session.query(Res_line, Kontline).join(Kontline,(Kontline.kontignr == Res_line.kontignr) & (Kontline.kontcode == (kontcode).lower()) & (Kontline.kontstatus == 1)).filter(
                 (Res_line.kontignr != 0) & (Res_line.gastnr == gastnr) & (Res_line.active_flag < 2) & (Res_line.resstatus < 11)).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            if res_line.abreise <= ankunft or res_line.ankunft > abreise:
                pass
            else:
                for d in date_range(res_line.ankunft,(res_line.abreise - 1)) :

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.datum == d), first=True)

                    if s_list:
                        s_list.vac = s_list.vac - res_line.zimmeranz
                        s_list.occ = s_list.occ + res_line.zimmeranz

    if case_type == 1:
        assign_it()

    elif case_type == 2:
        check_resline()

    elif case_type == 3:
        check_allotment()

    elif case_type == 4:
        create_slist()

    return generate_output()