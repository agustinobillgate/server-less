DEFINE TEMP-TABLE margt-list   LIKE prmarket.
DEFINE TEMP-TABLE hargt-list   LIKE prmarket.
DEFINE TEMP-TABLE hrmcat-list  LIKE prmarket.
DEFINE TEMP-TABLE mrmcat-list  LIKE prmarket.
DEFINE TEMP-TABLE t-pricecod   LIKE pricecod.
DEFINE TEMP-TABLE t-ratecode   LIKE ratecode.

DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER TABLE FOR margt-list.
DEF OUTPUT PARAMETER TABLE FOR hargt-list.
DEF OUTPUT PARAMETER TABLE FOR hrmcat-list.
DEF OUTPUT PARAMETER TABLE FOR mrmcat-list.
DEF OUTPUT PARAMETER TABLE FOR t-pricecod.
DEF OUTPUT PARAMETER TABLE FOR t-ratecode.


FIND FIRST prtable WHERE RECID(prtable) = rec-id NO-ERROR.
IF NOT AVAILABLE prtable THEN RETURN.

RUN check-array.

FOR EACH pricecod WHERE pricecod.marknr = prtable.nr NO-LOCK:
    CREATE t-pricecod.
    BUFFER-COPY pricecod TO t-pricecod.
END.

FOR EACH ratecode WHERE ratecode.marknr = prtable.nr NO-LOCK:
    CREATE t-ratecode.
    BUFFER-COPY ratecode TO t-ratecode.
END.


PROCEDURE check-array:
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE array AS INTEGER EXTENT 99. 
 
  FOR EACH hrmcat-list: 
    delete hrmcat-list. 
  END. 
  FOR EACH mrmcat-list: 
    delete mrmcat-list. 
  END. 
  DO i = 1 TO 99: 
    array[i] = prtable.zikatnr[i]. 
  END. 
  FOR EACH zimkateg: 
    create hrmcat-list. 
    hrmcat-list.nr = zimkateg.zikatnr. 
    hrmcat-list.bezeich = zimkateg.bezeich. 
  END. 
 
  DO i = 1 TO 99: 
    IF array[i] NE 0 THEN 
    DO: 
      FIND FIRST zimkateg WHERE zimkateg.zikatnr = array[i] NO-LOCK NO-ERROR. 
      IF AVAILABLE zimkateg THEN 
      DO: 
        create mrmcat-list. 
        mrmcat-list.nr = zimkateg.zikatnr. 
        mrmcat-list.bezeich = zimkateg.bezeich. 
      END. 
      FIND FIRST hrmcat-list WHERE hrmcat-list.nr = mrmcat-list.nr NO-ERROR. 
      IF AVAILABLE hrmcat-list THEN delete hrmcat-list. 
    END. 
  END. 
  
  FOR EACH hargt-list: 
    delete hargt-list. 
  END. 
  FOR EACH margt-list: 
    delete margt-list. 
  END.

  DO i = 1 TO 99: 
    array[i] = prtable.argtnr[i]. 
  END. 
  FOR EACH arrangement WHERE arrangement.segmentcode = 0 NO-LOCK: 
    create hargt-list. 
    hargt-list.nr = arrangement.argtnr. 
    hargt-list.bezeich = arrangement.argt-bez. 
  END. 
 
  DO i = 1 TO 99: 
    IF array[i] NE 0 THEN 
    DO: 
      FIND FIRST arrangement WHERE arrangement.argtnr = array[i] 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE arrangement THEN 
      DO: 
        create margt-list. 
        margt-list.nr = arrangement.argtnr. 
        margt-list.bezeich = arrangement.argt-bez. 
      END. 
      FIND FIRST hargt-list WHERE hargt-list.nr = margt-list.nr NO-ERROR. 
      IF AVAILABLE hargt-list THEN delete hargt-list. 
    END. 
  END.
END. 
