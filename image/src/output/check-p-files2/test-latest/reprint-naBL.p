

DEFINE TEMP-TABLE b1-list
    FIELD reihenfolge   LIKE nightaudit.reihenfolge
    FIELD hogarest      LIKE nightaudit.hogarest
    FIELD bezeichnun    LIKE nightaudit.bezeichnun
    FIELD rec-id        AS INTEGER.

DEFINE OUTPUT PARAMETER TABLE FOR b1-list.

FOR EACH nightaudit WHERE selektion = YES NO-LOCK 
  BY (1 - hogarest) BY nightaudit.reihenfolge:
    CREATE b1-list.
    ASSIGN
      b1-list.reihenfolge   = nightaudit.reihenfolge
      b1-list.hogarest      = nightaudit.hogarest
      b1-list.bezeichnun    = nightaudit.bezeichnun
      b1-list.rec-id        = RECID(nightaudit).
END.
