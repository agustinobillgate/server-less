from functions.additional_functions import *
import decimal
from models import Prmarket, Waehrung, Zimkateg, Htparam, Queasy, Prtable, Arrangement

def prepare_prtable_adminbl():
    new_contrate = False
    f_char = ""
    f_logical = False
    fill_wabkurz = ""
    b1_list_list = []
    t_waehrung1_list = []
    fill_t_waehrung_list = []
    margt_list_list = []
    hargt_list_list = []
    hrmcat_list_list = []
    mrmcat_list_list = []
    prmarket = waehrung = zimkateg = htparam = queasy = prtable = arrangement = None

    margt_list = hargt_list = hrmcat_list = mrmcat_list = b1_list = t_waehrung1 = fill_t_waehrung = t_waehrung2 = t_zimkateg = None

    margt_list_list, Margt_list = create_model_like(Prmarket)
    hargt_list_list, Hargt_list = create_model_like(Prmarket)
    hrmcat_list_list, Hrmcat_list = create_model_like(Prmarket)
    mrmcat_list_list, Mrmcat_list = create_model_like(Prmarket)
    b1_list_list, B1_list = create_model("B1_list", {"nr":int, "marknr":int, "bezeich":str, "char3":str, "logi3":bool, "rec_id":int, "pr_recid":int})
    t_waehrung1_list, T_waehrung1 = create_model_like(Waehrung)
    fill_t_waehrung_list, Fill_t_waehrung = create_model("Fill_t_waehrung", {"wabkurz":str})
    t_waehrung2_list, T_waehrung2 = create_model_like(Waehrung)
    t_zimkateg_list, T_zimkateg = create_model_like(Zimkateg)


    db_session = local_storage.db_session
    result = db_session.execute(sa.text("SELECT current_schema();"))
    current_schema = result.scalar()
    print("Current Schema:", current_schema)

    def generate_output():
        nonlocal new_contrate, f_char, f_logical, fill_wabkurz, b1_list_list, t_waehrung1_list, fill_t_waehrung_list, margt_list_list, hargt_list_list, hrmcat_list_list, mrmcat_list_list, prmarket, waehrung, zimkateg, htparam, queasy, prtable, arrangement


        nonlocal margt_list, hargt_list, hrmcat_list, mrmcat_list, b1_list, t_waehrung1, fill_t_waehrung, t_waehrung2, t_zimkateg
        nonlocal margt_list_list, hargt_list_list, hrmcat_list_list, mrmcat_list_list, b1_list_list, t_waehrung1_list, fill_t_waehrung_list, t_waehrung2_list, t_zimkateg_list
        # return {"new_contrate": new_contrate, "f_char": f_char, "f_logical": f_logical, "fill_wabkurz": fill_wabkurz, "b1-list": b1_list_list, "t-waehrung1": t_waehrung1_list, "fill-t-waehrung": fill_t_waehrung_list, "margt-list": margt_list_list, "hargt-list": hargt_list_list, "hrmcat-list": hrmcat_list_list, "mrmcat-list": mrmcat_list_list}

        return {"new_contrate": new_contrate, "f_char": f_char, "f_logical": f_logical, "fill_wabkurz": fill_wabkurz, "b1-list": b1_list_list, "t-waehrung1": t_waehrung1_list, "fill-t-waehrung": fill_t_waehrung_list, "margt-list": margt_list_list, "hargt-list": hargt_list_list, "hrmcat-list": hrmcat_list_list, "mrmcat-list": mrmcat_list_list}

    def get_currency():

        nonlocal new_contrate, f_char, f_logical, fill_wabkurz, b1_list_list, t_waehrung1_list, fill_t_waehrung_list, margt_list_list, hargt_list_list, hrmcat_list_list, mrmcat_list_list, prmarket, waehrung, zimkateg, htparam, queasy, prtable, arrangement


        nonlocal margt_list, hargt_list, hrmcat_list, mrmcat_list, b1_list, t_waehrung1, fill_t_waehrung, t_waehrung2, t_zimkateg
        nonlocal margt_list_list, hargt_list_list, hrmcat_list_list, mrmcat_list_list, b1_list_list, t_waehrung1_list, fill_t_waehrung_list, t_waehrung2_list, t_zimkateg_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 240)).first()
        f_logical = htparam.flogical

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()
        f_char = htparam.fchar

        for waehrung in db_session.query(Waehrung).all():
            t_waehrung1 = T_waehrung1()
            t_waehrung1_list.append(t_waehrung1)

            buffer_copy(waehrung, t_waehrung1)

    def check_array():

        nonlocal new_contrate, f_char, f_logical, fill_wabkurz, b1_list_list, t_waehrung1_list, fill_t_waehrung_list, margt_list_list, hargt_list_list, hrmcat_list_list, mrmcat_list_list, prmarket, waehrung, zimkateg, htparam, queasy, prtable, arrangement


        nonlocal margt_list, hargt_list, hrmcat_list, mrmcat_list, b1_list, t_waehrung1, fill_t_waehrung, t_waehrung2, t_zimkateg
        nonlocal margt_list_list, hargt_list_list, hrmcat_list_list, mrmcat_list_list, b1_list_list, t_waehrung1_list, fill_t_waehrung_list, t_waehrung2_list, t_zimkateg_list

        i:int = 0
        array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        hrmcat_list_list.clear()
        mrmcat_list_list.clear()
        for i in range(1,99 + 1) :
            array[i - 1] = prtable.zikatnr[i - 1]

        for zimkateg in db_session.query(Zimkateg).all():
            hrmcat_list = Hrmcat_list()
            hrmcat_list_list.append(hrmcat_list)

            hrmcat_list.nr = zimkateg.zikatnr
            hrmcat_list.bezeichnung = zimkateg.bezeichnung
        for i in range(1,99 + 1) :

            if array[i - 1] != 0:

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == array[i - 1])).first()

                if zimkateg:
                    mrmcat_list = Mrmcat_list()
                    mrmcat_list_list.append(mrmcat_list)

                    mrmcat_list.nr = zimkateg.zikatnr
                    mrmcat_list.bezeichnung = zimkateg.bezeichnung

                hrmcat_list = query(hrmcat_list_list, filters=(lambda hrmcat_list :hrmcat_list.nr == mrmcat_list.nr), first=True)

                if hrmcat_list:
                    hrmcat_list_list.remove(hrmcat_list)
        hargt_list_list.clear()
        margt_list_list.clear()
        for i in range(1,99 + 1) :
            array[i - 1] = prtable.argtnr[i - 1]

        for arrangement in db_session.query(Arrangement).filter(
                (Arrangement.segmentcode == 0)).all():
            hargt_list = Hargt_list()
            hargt_list_list.append(hargt_list)

            hargt_list.nr = arrangement.argtnr
            hargt_list.bezeich = arrangement.argt_bez
        for i in range(1,99 + 1) :

            if array[i - 1] != 0:

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement.argtnr == array[i - 1])).first()

                if arrangement:
                    margt_list = Margt_list()
                    margt_list_list.append(margt_list)

                    margt_list.nr = arrangement.argtnr
                    margt_list.bezeich = arrangement.argt_bez

                hargt_list = query(hargt_list_list, filters=(lambda hargt_list :hargt_list.nr == margt_list.nr), first=True)

                if hargt_list:
                    hargt_list_list.remove(hargt_list)

    def fill_currency():

        nonlocal new_contrate, f_char, f_logical, fill_wabkurz, b1_list_list, t_waehrung1_list, fill_t_waehrung_list, margt_list_list, hargt_list_list, hrmcat_list_list, mrmcat_list_list, prmarket, waehrung, zimkateg, htparam, queasy, prtable, arrangement


        nonlocal margt_list, hargt_list, hrmcat_list, mrmcat_list, b1_list, t_waehrung1, fill_t_waehrung, t_waehrung2, t_zimkateg
        nonlocal margt_list_list, hargt_list_list, hrmcat_list_list, mrmcat_list_list, b1_list_list, t_waehrung1_list, fill_t_waehrung_list, t_waehrung2_list, t_zimkateg_list

        double_currency:bool = False

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 240)).first()

        if htparam.flogical:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 144)).first()

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrung.wabkurz == htparam.fchar)).first()

            if waehrung:
                fill_wabkurz = waehrung.wabkurz

            return

        for waehrung in db_session.query(Waehrung).filter(
                (Waehrung.betriebsnr == 0) &  (Waehrung.ankauf > 0)).all():
            fill_t_waehrung = Fill_t_waehrung()
            fill_t_waehrung_list.append(fill_t_waehrung)

            fill_t_waehrung.wabkurz = waehrung.wabkurz

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 550)).first()

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 18)).first()

    if not queasy:

        for prmarket in db_session.query(Prmarket).all():
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 18
            queasy.number1 = prmarket.nr

    prtable_obj_list = []
    for prtable, prmarket, queasy in db_session.query(Prtable, Prmarket, Queasy)\
                                    .join(Prmarket,(Prmarket.nr == Prtable.marknr))\
                                    .join(Queasy,(Queasy.key == 18) &  (Queasy.number1 == Prmarket.nr)).filter(
                                        (Prtable.prcode == '')).order_by(Prtable.nr).all():

        if prtable._recid in prtable_obj_list:
            continue
        else:
            prtable_obj_list.append(prtable._recid)

        b1_list = B1_list()
        b1_list.nr = prtable.nr
        b1_list.marknr = prtable.marknr
        b1_list.bezeichnung = prmarket.bezeich
        b1_list.char3 = queasy.char3
        b1_list.logi3 = queasy.logi3
        b1_list.rec_id = prtable._recid
        b1_list.pr_recid = prmarket._recid
        b1_list_list.append(b1_list)

    # print("B1_list_list:", b1_list_list)
    b1_list = query(b1_list_list, first=True)
    print("B1_list:", b1_list)
    get_currency()
    fill_currency()

    prtable = db_session.query(Prtable).filter(
            (Prtable._recid == b1_list.rec_id)).first()
    check_array()

    return generate_output()