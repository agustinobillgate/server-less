from functions.additional_functions import *
import decimal
from datetime import date
from functions.mnstart_arch import mnstart_arch
from sqlalchemy import func
from models import Htparam, Nitehist, Nightaudit

def mn_del_nitehistbl():
    datum1:date = None
    ci_date:date = None
    htparam = nitehist = nightaudit = None

    nbuff = None

    Nbuff = Nitehist

    db_session = local_storage.db_session

    def generate_output():
        nonlocal datum1, ci_date, htparam, nitehist, nightaudit
        nonlocal nbuff


        nonlocal nbuff
        return {}

    def del_nitehist():

        nonlocal datum1, ci_date, htparam, nitehist, nightaudit
        nonlocal nbuff


        nonlocal nbuff

        store_flag:bool = False
        anz:int = 0
        curr_date:date = None
        Nbuff = Nitehist

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 230)).first()

        if htparam.feldtyp == 4 and htparam.flogical:
            store_flag = True

        if not store_flag:

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 238)).first()
        anz = htparam.finteger

        if anz == 0:
            anz = 60

        if CONNECTED ("vhparch"):
            datum1 = ci_date - anz
            get_output(mnstart_arch('del_nitehist', 0, datum1))
        else:

            nitehist = db_session.query(Nitehist).first()
            while None != nitehist:

                if nitehist.datum > (ci_date - anz):
                    return

                nbuff = db_session.query(Nbuff).filter(
                            (Nbuff._recid == nitehist._recid)).first()
                db_session.delete(nbuff)

                nitehist = db_session.query(Nitehist).first()

        nightaudit = db_session.query(Nightaudit).filter(
                (func.lower(Nightaudit.programm) == "nt_onlinetax.p") |  (func.lower(Nightaudit.programm) == "nt_aiirevenue.p")).first()

        if not nightaudit:

            return

        nitehist = db_session.query(Nitehist).filter(
                (Nitehist.reihenfolge == nightaudit.reihenfolge)).first()
        while None != nitehist:

            if nitehist.datum > (ci_date - 65):
                return

            nbuff = db_session.query(Nbuff).filter(
                        (Nbuff._recid == nitehist._recid)).first()
            db_session.delete(nbuff)

            nitehist = db_session.query(Nitehist).filter(
                    (Nitehist.reihenfolge == nightaudit.reihenfolge)).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    del_nitehist()

    return generate_output()