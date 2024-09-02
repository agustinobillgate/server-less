from functions.additional_functions import *
import decimal
from datetime import date
from models import Zimkateg, Htparam, Zimmer, Res_line, Outorder, Paramtext

def prepare_hk_statadminbl(zinr:str, floor:int, dispsort:int, statsort:int):
    ci_date = None
    z_list_list = []
    om_list_list = []
    bline_list_list = []
    setup_list_list = []
    t_zimkateg_list = []
    zimkateg = htparam = zimmer = res_line = outorder = paramtext = None

    t_zimkateg = z_list = om_list = bline_list = setup_list = None

    t_zimkateg_list, T_zimkateg = create_model_like(Zimkateg)
    z_list_list, Z_list = create_model("Z_list", {"zinr":str, "setup":int, "zikatnr":int, "etage":int, "zistatus":int, "code":str, "bediener_nr_stat":int, "checkout":bool, "str_reason":str})
    om_list_list, Om_list = create_model("Om_list", {"zinr":str, "ind":int})
    bline_list_list, Bline_list = create_model("Bline_list", {"zinr":str, "selected":bool, "bl_recid":int})
    setup_list_list, Setup_list = create_model("Setup_list", {"nr":int, "char":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, z_list_list, om_list_list, bline_list_list, setup_list_list, t_zimkateg_list, zimkateg, htparam, zimmer, res_line, outorder, paramtext


        nonlocal t_zimkateg, z_list, om_list, bline_list, setup_list
        nonlocal t_zimkateg_list, z_list_list, om_list_list, bline_list_list, setup_list_list
        return {"ci_date": ci_date, "z-list": z_list_list, "om-list": om_list_list, "bline-list": bline_list_list, "setup-list": setup_list_list, "t-zimkateg": t_zimkateg_list}

    def bed_setup():

        nonlocal ci_date, z_list_list, om_list_list, bline_list_list, setup_list_list, t_zimkateg_list, zimkateg, htparam, zimmer, res_line, outorder, paramtext


        nonlocal t_zimkateg, z_list, om_list, bline_list, setup_list
        nonlocal t_zimkateg_list, z_list_list, om_list_list, bline_list_list, setup_list_list

        it_exist:bool = False
        setup_list = Setup_list()
        setup_list_list.append(setup_list)

        setup_list.nr = 1
        setup_list.char = " "

        for paramtext in db_session.query(Paramtext).filter(
                (Paramtext.txtnr >= 9201) &  (Paramtext.txtnr <= 9299)).all():
            setup_list = Setup_list()
            setup_list_list.append(setup_list)

            setup_list.nr = paramtext.txtnr - 9199
            setup_list.char = substring(paramtext.notes, 0, 1)
            it_exist = True

    def create_list():

        nonlocal ci_date, z_list_list, om_list_list, bline_list_list, setup_list_list, t_zimkateg_list, zimkateg, htparam, zimmer, res_line, outorder, paramtext


        nonlocal t_zimkateg, z_list, om_list, bline_list, setup_list
        nonlocal t_zimkateg_list, z_list_list, om_list_list, bline_list_list, setup_list_list

        for zimmer in db_session.query(Zimmer).all():
            bline_list = Bline_list()
            bline_list_list.append(bline_list)

            bline_list.zinr = zimmer.zinr


            om_list = Om_list()
            om_list_list.append(om_list)

            om_list.zinr = zimmer.zinr
            om_list.ind = zimmer.zistatus + 1

        for outorder in db_session.query(Outorder).filter(
                (Outorder.betriebsnr >= 2) &  (Outorder.gespstart <= ci_date) &  (Outorder.gespende >= ci_date)).all():

            om_list = query(om_list_list, filters=(lambda om_list :om_list.zinr == outorder.zinr), first=True)

            if outorder.betriebsnr == 3 or outorder.betriebsnr == 4:
                om_list.ind = 10
            else:
                om_list.ind = 8

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    bed_setup()
    create_list()

    for zimmer in db_session.query(Zimmer).all():
        z_list = Z_list()
        z_list_list.append(z_list)

        buffer_copy(zimmer, z_list)

        if zimmer.zistatus == 2:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resstatus == 8) &  (Res_line.zinr == zimmer.zinr) &  (Res_line.abreise == ci_date)).first()

            if res_line:
                z_list.checkout = True

        if zimmer.zistatus == 6:

            outorder = db_session.query(Outorder).filter(
                    (Outorder.zinr == zimmer.zinr) &  (Outorder.betriebsnr <= 2) &  (Outorder.gespstart <= ci_date) &  (Outorder.gespende >= ci_date)).first()

            if outorder:
                z_list.str_reason = entry(0, outorder.gespgrund, "$")


            else:
                z_list.str_reason = " "

    for zimkateg in db_session.query(Zimkateg).all():
        t_zimkateg = T_zimkateg()
        t_zimkateg_list.append(t_zimkateg)

        buffer_copy(zimkateg, t_zimkateg)

    return generate_output()