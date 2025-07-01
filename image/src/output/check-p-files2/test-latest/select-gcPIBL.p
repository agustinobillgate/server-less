DEF TEMP-TABLE b1-list
    FIELD datum     LIKE gc-pi.datum
    FIELD docu-nr   LIKE gc-pi.docu-nr
    FIELD betrag    LIKE gc-pi.betrag
    FIELD bemerk    LIKE gc-pi.bemerk
    FIELD username  LIKE bediener.username
    FIELD bezeich   LIKE gc-pitype.bezeich.

DEF OUTPUT PARAMETER TABLE FOR b1-list.

FOR EACH gc-pi WHERE gc-pi.pi-status = 0 NO-LOCK,
    FIRST gc-pitype WHERE gc-pitype.nr = gc-pi.pi-type NO-LOCK,
    FIRST bediener WHERE bediener.userinit = gc-pi.rcvID NO-LOCK
    BY gc-pi.datum BY gc-pi.docu-nr:
    CREATE b1-list.
    ASSIGN
    b1-list.datum     = gc-pi.datum
    b1-list.docu-nr   = gc-pi.docu-nr
    b1-list.betrag    = gc-pi.betrag
    b1-list.bemerk    = gc-pi.bemerk
    b1-list.username  = bediener.username
    b1-list.bezeich   = gc-pitype.bezeich.
END.
