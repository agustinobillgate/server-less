#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Prmarket, Waehrung, Zimkateg, Htparam, Queasy, Prtable, Arrangement

def prepare_prtable_adminbl():

    prepare_cache ([Prmarket, Zimkateg, Htparam, Queasy, Prtable, Arrangement])

    new_contrate = False
    f_char = ""
    f_logical = False
    fill_wabkurz = ""
    b1_list_data = []
    t_waehrung1_data = []
    fill_t_waehrung_data = []
    margt_list_data = []
    hargt_list_data = []
    hrmcat_list_data = []
    mrmcat_list_data = []
    prmarket = waehrung = zimkateg = htparam = queasy = prtable = arrangement = None

    margt_list = hargt_list = hrmcat_list = mrmcat_list = b1_list = t_waehrung1 = fill_t_waehrung = t_waehrung2 = t_zimkateg = None

    margt_list_data, Margt_list = create_model_like(Prmarket)
    hargt_list_data, Hargt_list = create_model_like(Prmarket)
    hrmcat_list_data, Hrmcat_list = create_model_like(Prmarket)
    mrmcat_list_data, Mrmcat_list = create_model_like(Prmarket)
    b1_list_data, B1_list = create_model("B1_list", {"nr":int, "marknr":int, "bezeich":string, "char3":string, "logi3":bool, "rec_id":int, "pr_recid":int})
    t_waehrung1_data, T_waehrung1 = create_model_like(Waehrung)
    fill_t_waehrung_data, Fill_t_waehrung = create_model("Fill_t_waehrung", {"wabkurz":string})
    t_waehrung2_data, T_waehrung2 = create_model_like(Waehrung)
    t_zimkateg_data, T_zimkateg = create_model_like(Zimkateg)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_contrate, f_char, f_logical, fill_wabkurz, b1_list_data, t_waehrung1_data, fill_t_waehrung_data, margt_list_data, hargt_list_data, hrmcat_list_data, mrmcat_list_data, prmarket, waehrung, zimkateg, htparam, queasy, prtable, arrangement


        nonlocal margt_list, hargt_list, hrmcat_list, mrmcat_list, b1_list, t_waehrung1, fill_t_waehrung, t_waehrung2, t_zimkateg
        nonlocal margt_list_data, hargt_list_data, hrmcat_list_data, mrmcat_list_data, b1_list_data, t_waehrung1_data, fill_t_waehrung_data, t_waehrung2_data, t_zimkateg_data

        return {"new_contrate": new_contrate, "f_char": f_char, "f_logical": f_logical, "fill_wabkurz": fill_wabkurz, "b1-list": b1_list_data, "t-waehrung1": t_waehrung1_data, "fill-t-waehrung": fill_t_waehrung_data, "margt-list": margt_list_data, "hargt-list": hargt_list_data, "hrmcat-list": hrmcat_list_data, "mrmcat-list": mrmcat_list_data}

    def get_currency():

        nonlocal new_contrate, f_char, f_logical, fill_wabkurz, b1_list_data, t_waehrung1_data, fill_t_waehrung_data, margt_list_data, hargt_list_data, hrmcat_list_data, mrmcat_list_data, prmarket, waehrung, zimkateg, htparam, queasy, prtable, arrangement


        nonlocal margt_list, hargt_list, hrmcat_list, mrmcat_list, b1_list, t_waehrung1, fill_t_waehrung, t_waehrung2, t_zimkateg
        nonlocal margt_list_data, hargt_list_data, hrmcat_list_data, mrmcat_list_data, b1_list_data, t_waehrung1_data, fill_t_waehrung_data, t_waehrung2_data, t_zimkateg_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
        f_logical = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})
        f_char = htparam.fchar

        for waehrung in db_session.query(Waehrung).order_by(Waehrung._recid).all():
            t_waehrung1 = T_waehrung1()
            t_waehrung1_data.append(t_waehrung1)

            buffer_copy(waehrung, t_waehrung1)


    def check_array():

        nonlocal new_contrate, f_char, f_logical, fill_wabkurz, b1_list_data, t_waehrung1_data, fill_t_waehrung_data, margt_list_data, hargt_list_data, hrmcat_list_data, mrmcat_list_data, prmarket, waehrung, zimkateg, htparam, queasy, prtable, arrangement


        nonlocal margt_list, hargt_list, hrmcat_list, mrmcat_list, b1_list, t_waehrung1, fill_t_waehrung, t_waehrung2, t_zimkateg
        nonlocal margt_list_data, hargt_list_data, hrmcat_list_data, mrmcat_list_data, b1_list_data, t_waehrung1_data, fill_t_waehrung_data, t_waehrung2_data, t_zimkateg_data

        i:int = 0
        array:List[int] = create_empty_list(99,0)
        hrmcat_list_data.clear()
        mrmcat_list_data.clear()
        for i in range(1,99 + 1) :
            array[i - 1] = prtable.zikatnr[i - 1]

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
            hrmcat_list = Hrmcat_list()
            hrmcat_list_data.append(hrmcat_list)

            hrmcat_list.nr = zimkateg.zikatnr
            hrmcat_list.bezeich = zimkateg.bezeichnung
        for i in range(1,99 + 1) :

            if array[i - 1] != 0:

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, array[i - 1])]})

                if zimkateg:
                    mrmcat_list = Mrmcat_list()
                    mrmcat_list_data.append(mrmcat_list)

                    mrmcat_list.nr = zimkateg.zikatnr
                    mrmcat_list.bezeich = zimkateg.bezeichnung

                hrmcat_list = query(hrmcat_list_data, filters=(lambda hrmcat_list: hrmcat_list.nr == mrmcat_list.nr), first=True)

                if hrmcat_list:
                    hrmcat_list_data.remove(hrmcat_list)
        hargt_list_data.clear()
        margt_list_data.clear()
        for i in range(1,99 + 1) :
            array[i - 1] = prtable.argtnr[i - 1]

        for arrangement in db_session.query(Arrangement).filter(
                 (Arrangement.segmentcode == 0)).order_by(Arrangement._recid).all():
            hargt_list = Hargt_list()
            hargt_list_data.append(hargt_list)

            hargt_list.nr = arrangement.argtnr
            hargt_list.bezeich = arrangement.argt_bez
        for i in range(1,99 + 1) :

            if array[i - 1] != 0:

                arrangement = get_cache (Arrangement, {"argtnr": [(eq, array[i - 1])]})

                if arrangement:
                    margt_list = Margt_list()
                    margt_list_data.append(margt_list)

                    margt_list.nr = arrangement.argtnr
                    margt_list.bezeich = arrangement.argt_bez

                hargt_list = query(hargt_list_data, filters=(lambda hargt_list: hargt_list.nr == margt_list.nr), first=True)

                if hargt_list:
                    hargt_list_data.remove(hargt_list)


    def fill_currency():

        nonlocal new_contrate, f_char, f_logical, fill_wabkurz, b1_list_data, t_waehrung1_data, fill_t_waehrung_data, margt_list_data, hargt_list_data, hrmcat_list_data, mrmcat_list_data, prmarket, waehrung, zimkateg, htparam, queasy, prtable, arrangement


        nonlocal margt_list, hargt_list, hrmcat_list, mrmcat_list, b1_list, t_waehrung1, fill_t_waehrung, t_waehrung2, t_zimkateg
        nonlocal margt_list_data, hargt_list_data, hrmcat_list_data, mrmcat_list_data, b1_list_data, t_waehrung1_data, fill_t_waehrung_data, t_waehrung2_data, t_zimkateg_data

        double_currency:bool = False

        htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})

        if htparam.flogical:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

            if waehrung:
                fill_wabkurz = waehrung.wabkurz

            return

        for waehrung in db_session.query(Waehrung).filter(
                 (Waehrung.betriebsnr == 0) & (Waehrung.ankauf > 0)).order_by(Waehrung.wabkurz).all():
            fill_t_waehrung = Fill_t_waehrung()
            fill_t_waehrung_data.append(fill_t_waehrung)

            fill_t_waehrung.wabkurz = waehrung.wabkurz


    htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    queasy = get_cache (Queasy, {"key": [(eq, 18)]})

    if not queasy:

        for prmarket in db_session.query(Prmarket).order_by(Prmarket._recid).all():
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 18
            queasy.number1 = prmarket.nr

    prtable_obj_list = {}
    prtable = Prtable()
    prmarket = Prmarket()
    queasy = Queasy()
    for prtable.zikatnr, prtable.argtnr, prtable.nr, prtable.marknr, prtable._recid, prmarket.nr, prmarket.bezeich, prmarket._recid, queasy.char3, queasy.logi3, queasy.key, queasy.number1, queasy._recid in db_session.query(Prtable.zikatnr, Prtable.argtnr, Prtable.nr, Prtable.marknr, Prtable._recid, Prmarket.nr, Prmarket.bezeich, Prmarket._recid, Queasy.char3, Queasy.logi3, Queasy.key, Queasy.number1, Queasy._recid).join(Prmarket,(Prmarket.nr == Prtable.marknr)).join(Queasy,(Queasy.key == 18) & (Queasy.number1 == Prmarket.nr)).filter(
             (Prtable.prcode == "")).order_by(Prtable.nr).all():
        if prtable_obj_list.get(prtable._recid):
            continue
        else:
            prtable_obj_list[prtable._recid] = True


        b1_list = B1_list()
        b1_list_data.append(b1_list)

        b1_list.nr = prtable.nr
        b1_list.marknr = prtable.marknr
        b1_list.bezeich = prmarket.bezeich
        b1_list.char3 = queasy.char3
        b1_list.logi3 = queasy.logi3
        b1_list.rec_id = prtable._recid
        b1_list.pr_recid = prmarket._recid

    b1_list = query(b1_list_data, first=True)
    get_currency()
    fill_currency()

    prtable = get_cache (Prtable, {"_recid": [(eq, b1_list.rec_id)]})
    check_array()

    return generate_output()