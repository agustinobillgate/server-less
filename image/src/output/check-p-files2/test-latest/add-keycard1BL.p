
DEF INPUT PARAMETER resno       AS INTEGER NO-UNDO.
DEF INPUT PARAMETER reslinno    AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER card-type  AS CHAR.

FIND FIRST res-line WHERE res-line.resnr = resno 
      AND res-line.reslinnr = reslinno NO-LOCK NO-ERROR.
DO TRANSACTION:
    FIND CURRENT res-line EXCLUSIVE-LOCK. 
    res-line.betrieb-gast = res-line.betrieb-gast + 1. 
    FIND CURRENT res-line NO-LOCK. 
    card-type = "cardtype=2". 
END.
