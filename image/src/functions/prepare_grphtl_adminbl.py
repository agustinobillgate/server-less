from functions.additional_functions import *
import decimal
from sqlalchemy import and_, not_, inspect
from models import Queasy

def prepare_grphtl_adminbl():
    t_queasy_list = []
    queasy = None

    t_queasy = queasy1 = None

    t_queasy_list, T_queasy = create_model_like(Queasy, {"rec_id":int})

    Queasy1 = Queasy

    db_session = local_storage.db_session
    current_database = db_session.bind.url.database
    current_schema = db_session.bind.dialect.default_schema_name

    # print("Current Database:", current_database)
    # print("Current Schema:", current_schema)

    def generate_output():
        nonlocal t_queasy_list, queasy
        nonlocal queasy1


        nonlocal t_queasy, queasy1
        nonlocal t_queasy_list
        return {"t-queasy": t_queasy_list}

    def check_queasy136():

        nonlocal t_queasy_list, queasy
        nonlocal queasy1

        nonlocal t_queasy, queasy1
        nonlocal t_queasy_list
        current_database = db_session.bind.url.database
        result = db_session.execute(sa.text("SELECT current_schema();"))
        current_schema = result.scalar()

        print("45.Current Database/Schema:", current_database, current_schema)

        queasy = db_session.query(Queasy)\
            .filter(Queasy.key == 136)\
            .filter(~Queasy.char1.op("~")(".*:.*"))\
            .first()
        
        while None != queasy:

            queasy1 = db_session.query(Queasy1).filter(
                        (Queasy1._recid == queasy._recid)).first()
            queasy.char1 = queasy.char2 + ":" + queasy.char1
            queasy.char2 = ""

            queasy1 = db_session.query(Queasy1).first()
            queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 136) &  (not Queasy.char1.op("~")(".*:.*"))).first()

    check_queasy136()

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 136)).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)
        t_queasy.rec_id = queasy._recid

    return generate_output()