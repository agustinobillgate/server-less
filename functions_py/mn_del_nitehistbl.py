#using conversion tools version: 1.0.0.117

#------------------------------------------
# Rd, 21/10/2025
# mnstart_arch -> diremark, khusus Archi
#------------------------------------------

# =============================================
# Rulita, 10-12-2025
# - Added with_for_update before delete query
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
# from functions.mnstart_arch import mnstart_arch
from models import Htparam, Nitehist, Nightaudit

def mn_del_nitehistbl():

    prepare_cache ([Htparam, Nightaudit])

    datum1:date = None
    ci_date:date = None
    htparam = nitehist = nightaudit = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal datum1, ci_date, htparam, nitehist, nightaudit

        return {}

    def del_nitehist():

        nonlocal datum1, ci_date, htparam, nitehist, nightaudit

        store_flag:bool = False
        anz:int = 0
        curr_date:date = None
        nbuff = None
        Nbuff =  create_buffer("Nbuff",Nitehist)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 230)]})

        if htparam.feldtyp == 4 and htparam.flogical:
            store_flag = True

        if not store_flag:

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 238)]})
        anz = htparam.finteger

        if anz == 0:
            anz = 60

        # if CONNECTED ("vhparch"):
        #     datum1 = ci_date - timedelta(days=anz)
        #     get_output(mnstart_arch('del-nitehist', 0, datum1))
        # else:

        nitehist = db_session.query(Nitehist).first()
        while None != nitehist:

            if nitehist.datum > (ci_date - timedelta(days=anz)):
                return

            nbuff = db_session.query(Nbuff).filter(
                            (Nbuff._recid == nitehist._recid)).with_for_update().first()
            db_session.delete(nbuff)
            pass

            curr_recid = nitehist._recid
            nitehist = db_session.query(Nitehist).filter(Nitehist._recid > curr_recid).first()

        nightaudit = db_session.query(Nightaudit).filter(
                 (Nightaudit.programm == ("nt-onlinetax.p")) | (Nightaudit.programm == ("nt-aiirevenue.p"))).first()

        if not nightaudit:

            return

        nitehist = get_cache (Nitehist, {"reihenfolge": [(eq, nightaudit.reihenfolge)]})
        while None != nitehist:

            if nitehist.datum > (ci_date - timedelta(days=65)):
                return

            nbuff = db_session.query(Nbuff).filter(
                         (Nbuff._recid == nitehist._recid)).with_for_update().first()
            db_session.delete(nbuff)
            pass

            curr_recid = nitehist._recid
            nitehist = db_session.query(Nitehist).filter(
                     (Nitehist.reihenfolge == nightaudit.reihenfolge) & (Nitehist._recid > curr_recid)).first()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    del_nitehist()

    return generate_output()