from functions.additional_functions import *
import decimal
from models import Zimmer

def eg_propertylist_rmnobl(rmno:str):
    avail_zimmer = False
    zimmer = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_zimmer, zimmer


        return {"avail_zimmer": avail_zimmer}


    zimmer = db_session.query(Zimmer).filter(
            (Zimmer.zinr == rmno)).first()

    if zimmer:
        avail_zimmer = True

    return generate_output()