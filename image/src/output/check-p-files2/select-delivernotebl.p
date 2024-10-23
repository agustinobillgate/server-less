DEF TEMP-TABLE t-l-ophdr
    FIELD datum     LIKE l-ophdr.datum
    FIELD lager-nr  LIKE l-ophdr.lager-nr
    FIELD docu-nr   LIKE l-ophdr.docu-nr
    FIELD lscheinnr LIKE l-ophdr.lscheinnr.

DEF OUTPUT PARAMETER TABLE FOR t-l-ophdr.

FOR EACH l-ophdr WHERE l-ophdr.op-typ = "STI" 
    NO-LOCK BY l-ophdr.lager-nr:
    CREATE t-l-ophdr.
    ASSIGN
    t-l-ophdr.datum     = l-ophdr.datum
    t-l-ophdr.lager-nr  = l-ophdr.lager-nr
    t-l-ophdr.docu-nr   = l-ophdr.docu-nr
    t-l-ophdr.lscheinnr = l-ophdr.lscheinnr.
END.
