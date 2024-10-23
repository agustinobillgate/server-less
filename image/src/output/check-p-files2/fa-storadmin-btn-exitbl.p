DEFINE TEMP-TABLE fa-list LIKE fa-lager.

DEF INPUT PARAMETER TABLE FOR fa-list.
DEF INPUT PARAMETER case-type   AS INT.
DEF INPUT PARAMETER rec-id      AS INT.

FIND FIRST fa-list.
IF case-type = 1 THEN   /* create */
DO:
    create fa-lager. 
    RUN fill-new-fa-lager. 
END.
ELSE    /* change */
DO:
    FIND FIRST fa-lager WHERE RECID(fa-lager) = rec-id.
    RUN update-name.
    FIND CURRENT fa-lager NO-LOCK.
END.

PROCEDURE fill-new-fa-lager: 
  fa-lager.lager-nr = fa-list.lager-nr. 
  fa-lager.bezeich = fa-list.bezeich. 
END. 


PROCEDURE update-name:
DEF BUFFER mbuff FOR mathis.
  IF fa-lager.bezeich = fa-list.bezeich THEN RETURN.
  DO TRANSACTION:
    FIND FIRST mathis WHERE mathis.location = fa-lager.bezeich NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE mathis:
      FIND FIRST mbuff WHERE RECID(mbuff) = RECID(mathis) EXCLUSIVE-LOCK.
      ASSIGN mbuff.location = fa-list.bezeich.
      FIND CURRENT mbuff NO-LOCK.
      FIND NEXT mathis WHERE mathis.location = fa-lager.bezeich NO-LOCK NO-ERROR.
    END.
    FIND CURRENT fa-lager EXCLUSIVE-LOCK. 
    fa-lager.bezeich = fa-list.bezeich. 
  END.
END.
