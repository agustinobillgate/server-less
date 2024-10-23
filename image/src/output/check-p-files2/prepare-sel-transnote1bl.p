
DEFINE TEMP-TABLE t-l-ophdr
    FIELD datum     LIKE l-ophdr.datum
    FIELD lager-nr  LIKE l-ophdr.lager-nr
    FIELD lscheinnr LIKE l-ophdr.lscheinnr
    FIELD docu-nr   LIKE l-ophdr.docu-nr.

DEF INPUT PARAMETER f-lager AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-l-ophdr.

FOR EACH l-ophdr WHERE l-ophdr.op-typ = "STT" 
    AND l-ophdr.lager-nr = f-lager NO-LOCK BY l-ophdr.lscheinnr:
    CREATE t-l-ophdr.
    ASSIGN
    t-l-ophdr.datum     = l-ophdr.datum
    t-l-ophdr.lager-nr  = l-ophdr.lager-nr
    t-l-ophdr.lscheinnr = l-ophdr.lscheinnr
    t-l-ophdr.docu-nr   = l-ophdr.docu-nr.
END.
