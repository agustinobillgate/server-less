
DEFINE TEMP-TABLE l-list LIKE l-untergrup. 

DEF INPUT PARAMETER TABLE FOR l-list.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER fibukonto AS CHAR.
DEF INPUT PARAMETER engart AS LOGICAL.
DEF INPUT PARAMETER main-nr AS INT.

FIND FIRST l-list NO-ERROR.
IF NOT AVAILABLE l-list THEN RETURN.

IF case-type = 1 THEN        /*add*/
DO:
  create l-untergrup.
  ASSIGN
    l-untergrup.zwkum = l-list.zwkum
    l-untergrup.bezeich = l-list.bezeich 
    l-untergrup.fibukonto = fibukonto
  . 
  IF engart = YES THEN l-untergrup.betriebsnr = 1. 
  ELSE l-untergrup.betriebsnr = 0. 
  FIND FIRST queasy WHERE queasy.KEY = 29 AND queasy.number2 = l-untergrup.zwkum
    EXCLUSIVE-LOCK NO-ERROR.
  IF main-nr GT 0 THEN
  DO:
    IF AVAILABLE queasy THEN queasy.number1 = main-nr.
    ELSE
    DO:
      CREATE queasy.
      ASSIGN
        queasy.KEY = 29
        queasy.number1 = main-nr
        queasy.number2 = l-list.zwkum
      .
    END.
    FIND CURRENT queasy NO-LOCK.
  END.
  ELSE IF AVAILABLE queasy THEN DELETE queasy.
END.
ELSE IF case-type = 2 THEN   /*chg*/
DO:
    FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-list.zwkum.
    FIND CURRENT l-untergrup EXCLUSIVE-LOCK. 
      l-untergrup.bezeich = l-list.bezeich. 
      l-untergrup.fibukonto = fibukonto. 
      IF engart THEN l-untergrup.betriebsnr = 1. 
      ELSE l-untergrup.betriebsnr = 0. 

      FIND FIRST queasy WHERE queasy.KEY = 29 AND queasy.number2 = l-untergrup.zwkum
        EXCLUSIVE-LOCK NO-ERROR.
      IF main-nr GT 0 THEN
      DO:
        IF AVAILABLE queasy THEN queasy.number1 = main-nr.
        ELSE
        DO:
          CREATE queasy.
          ASSIGN
            queasy.KEY = 29
            queasy.number1 = main-nr
            queasy.number2 = l-list.zwkum
          .
        END.
        FIND CURRENT queasy NO-LOCK.
      END.
      ELSE IF AVAILABLE queasy THEN DELETE queasy.
      FIND CURRENT l-untergrup NO-LOCK. 
END.
