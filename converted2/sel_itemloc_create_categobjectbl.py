#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_property, Queasy

def sel_itemloc_create_categobjectbl(chrzinr:string, intlocation:int):

    prepare_cache ([Eg_property, Queasy])

    categobjectlist_data = []
    cobjectlist_data = []
    categlist_data = []
    eg_property = queasy = None

    categobjectlist = cobjectlist = categlist = None

    categobjectlist_data, Categobjectlist = create_model("Categobjectlist", {"categ_nr":int, "categ_nm":string, "object_nr":int, "object_nm":string, "item_nr":int, "item_nm":string})
    cobjectlist_data, Cobjectlist = create_model("Cobjectlist", {"categ_nr":int, "object_nr":int, "object_nm":string})
    categlist_data, Categlist = create_model("Categlist", {"categ_nr":int, "categ_nm":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal categobjectlist_data, cobjectlist_data, categlist_data, eg_property, queasy
        nonlocal chrzinr, intlocation


        nonlocal categobjectlist, cobjectlist, categlist
        nonlocal categobjectlist_data, cobjectlist_data, categlist_data

        return {"CategObjectList": categobjectlist_data, "cObjectList": cobjectlist_data, "CategList": categlist_data}

    def create_categobject():

        nonlocal categobjectlist_data, cobjectlist_data, categlist_data, eg_property, queasy
        nonlocal chrzinr, intlocation


        nonlocal categobjectlist, cobjectlist, categlist
        nonlocal categobjectlist_data, cobjectlist_data, categlist_data

        propertybuff = None
        quesbuff = None
        quesbuff1 = None
        intcategob:int = 0
        intobjectnr:int = 0
        intcategex_nr:int = 0
        intobjectex_nr:int = 0
        Propertybuff =  create_buffer("Propertybuff",Eg_property)
        Quesbuff =  create_buffer("Quesbuff",Queasy)
        Quesbuff1 =  create_buffer("Quesbuff1",Queasy)

        if chrzinr == "":

            for propertybuff in db_session.query(Propertybuff).filter(
                     (Propertybuff.location == intlocation) & (Propertybuff.activeflag)).order_by(Propertybuff._recid).all():

                quesbuff = get_cache (Queasy, {"key": [(eq, 133)],"number1": [(eq, propertybuff.maintask)]})

                if quesbuff:

                    quesbuff1 = get_cache (Queasy, {"key": [(eq, 132)],"number1": [(eq, quesbuff.number2)]})

                    if quesbuff1:

                        if intcategex_nr == 0:
                            intcategex_nr = quesbuff1.number1
                            intcategob = quesbuff1.number1
                            categlist = Categlist()
                            categlist_data.append(categlist)

                            categlist.categ_nr = quesbuff1.number1
                            categlist.categ_nm = quesbuff1.char1


                        else:
                            intcategob = quesbuff1.number1

                            if intcategex_nr != quesbuff1.number1:
                                intcategex_nr = quesbuff1.number1

                                categlist = query(categlist_data, filters=(lambda categlist: categlist.categList.categ_nr == quesbuff1.number1), first=True)

                                if categList:
                                    pass
                                else:
                                    categlist = Categlist()
                                    categlist_data.append(categlist)

                                    categlist.categ_nr = quesbuff1.number1
                                    categlist.categ_nm = quesbuff1.char1


                            else:
                                pass
                    else:
                        pass

                    if intobjectex_nr == 0:
                        intobjectex_nr = quesbuff.number1
                        intobjectnr = quesbuff.number1
                        cobjectlist = Cobjectlist()
                        cobjectlist_data.append(cobjectlist)

                        cobjectlist.categ_nr = intcategob
                        cobjectlist.object_nr = quesbuff.number1
                        cobjectlist.object_nm = quesbuff.char1


                    else:

                        if intobjectex_nr != quesbuff.number1:
                            intobjectex_nr = quesbuff.number1
                            intobjectnr = quesbuff.number1

                            cobjectlist = query(cobjectlist_data, filters=(lambda cobjectlist: cobjectlist.cObjectList.Object_nr == quesbuff.number1), first=True)

                            if cObjectList:
                                pass
                            else:
                                cobjectlist = Cobjectlist()
                                cobjectlist_data.append(cobjectlist)

                                cobjectlist.categ_nr = intcategob
                                cobjectlist.object_nr = quesbuff.number1
                                cobjectlist.object_nm = quesbuff.char1


                        else:
                            pass
                else:
                    pass
                categobjectlist = Categobjectlist()
                categobjectlist_data.append(categobjectlist)

                categobjectlist.categ_nr = intcategob
                categobjectlist.object_nr = intobjectnr
                categobjectlist.item_nr = propertybuff.nr
                categobjectlist.item_nm = propertybuff.bezeich


        else:

            for propertybuff in db_session.query(Propertybuff).filter(
                     (propertyBuff.location == intlocation) & (propertyBuff.zinr == chrzinr) & (Propertybuff.activeflag)).order_by(Propertybuff._recid).all():

                quesbuff = get_cache (Queasy, {"key": [(eq, 133)],"number1": [(eq, propertybuff.maintask)]})

                if quesbuff:

                    quesbuff1 = get_cache (Queasy, {"key": [(eq, 132)],"number1": [(eq, quesbuff.number2)]})

                    if quesbuff1:

                        if intcategex_nr == 0:
                            intcategex_nr = quesbuff1.number1
                            intcategob = quesbuff1.number1
                            categlist = Categlist()
                            categlist_data.append(categlist)

                            categlist.categ_nr = quesbuff1.number1
                            categlist.categ_nm = quesbuff1.char1


                        else:
                            intcategob = quesbuff1.number1

                            if intcategex_nr != quesbuff1.number1:
                                intcategex_nr = quesbuff1.number1

                                categlist = query(categlist_data, filters=(lambda categlist: categlist.categList.categ_nr == quesbuff1.number1), first=True)

                                if categList:
                                    pass
                                else:
                                    categlist = Categlist()
                                    categlist_data.append(categlist)

                                    categlist.categ_nr = quesbuff1.number1
                                    categlist.categ_nm = quesbuff1.char1


                            else:
                                pass
                    else:
                        pass

                    if intobjectex_nr == 0:
                        intobjectex_nr = quesbuff.number1
                        intobjectnr = quesbuff.number1
                        cobjectlist = Cobjectlist()
                        cobjectlist_data.append(cobjectlist)

                        cobjectlist.categ_nr = intcategob
                        cobjectlist.object_nr = quesbuff.number1
                        cobjectlist.object_nm = quesbuff.char1


                    else:

                        if intobjectex_nr != quesbuff.number1:
                            intobjectex_nr = quesbuff.number1
                            intobjectnr = quesbuff.number1

                            cobjectlist = query(cobjectlist_data, filters=(lambda cobjectlist: cobjectlist.cObjectList.Object_nr == quesbuff.number1), first=True)

                            if cObjectList:
                                pass
                            else:
                                cobjectlist = Cobjectlist()
                                cobjectlist_data.append(cobjectlist)

                                cobjectlist.categ_nr = intcategob
                                cobjectlist.object_nr = quesbuff.number1
                                cobjectlist.object_nm = quesbuff.char1


                        else:
                            pass
                else:
                    pass
                categobjectlist = Categobjectlist()
                categobjectlist_data.append(categobjectlist)

                categobjectlist.categ_nr = intcategob
                categobjectlist.object_nr = intobjectnr
                categobjectlist.item_nr = propertybuff.nr
                categobjectlist.item_nm = propertybuff.bezeich

    create_categobject()

    return generate_output()