from functions.additional_functions import *
import decimal
from models import Htparam, Queasy, Waehrung

def nt_exchangerate():
    htparam = queasy = waehrung = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam, queasy, waehrung

        return {}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 190) & (Queasy.date1 == htparam.fdate)).order_by(Queasy._recid).all():

        waehrung = db_session.query(Waehrung).filter(
                 (Waehrung.waehrungsnr == queasy.number1)).first()

        if waehrung:

            if waehrung.ankauf != queasy.deci2 or waehrung.geaendert != htparam.fdate:
                waehrung.ankauf =  to_decimal(queasy.deci2)
                waehrung.geaendert = htparam.fdate


                pass

    return generate_output()