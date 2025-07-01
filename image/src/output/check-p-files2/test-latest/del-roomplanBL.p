
DEFINE TEMP-TABLE na-list 
  FIELD reihenfolge AS INTEGER 
  FIELD flag        AS INTEGER 
  FIELD bezeich     LIKE nightaudit.bezeichnung 
  FIELD anz         AS INTEGER FORMAT ">>,>>9". 

DEFINE INPUT-OUTPUT  PARAMETER TABLE FOR na-list.
DEFINE INPUT         PARAMETER ci-date  AS DATE.
DEFINE OUTPUT        PARAMETER i        AS INTEGER.

FIND FIRST htparam WHERE htparam.paramnr = 592.
ASSIGN htparam.flogical = YES.
FIND CURRENT htparam NO-LOCK.

RUN del-roomplan.

PROCEDURE del-roomplan: 

  FIND FIRST resplan WHERE resplan.datum GE ci-date NO-LOCK NO-ERROR. 
  FIND FIRST na-list WHERE na-list.reihenfolge = 1. 
  DO WHILE AVAILABLE resplan:
    DO transaction: 
      i = i + 1. 
      na-list.anz = na-list.anz + 1. 
      FIND CURRENT resplan EXCLUSIVE-LOCK.
        DELETE resplan.
        RELEASE resplan.
    END. 
    FIND NEXT resplan WHERE resplan.datum GE ci-date NO-LOCK NO-ERROR. 
  END. 
  FIND FIRST zimplan WHERE zimplan.datum GE ci-date NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE zimplan: 
    DO transaction: 
      i = i + 1. 
      na-list.anz = na-list.anz + 1. 
      FIND CURRENT zimplan EXCLUSIVE-LOCK. 
      DELETE zimplan.
      RELEASE zimplan.
    END. 
    FIND NEXT zimplan WHERE zimplan.datum GE ci-date NO-LOCK NO-ERROR. 
  END.
END. 
