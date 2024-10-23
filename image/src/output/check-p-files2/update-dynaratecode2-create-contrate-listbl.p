
DEFINE TEMP-TABLE t-list
    FIELD mesValue AS CHAR.

DEFINE TEMP-TABLE ratecode-list
    FIELD rcode AS CHAR.

DEF VAR ifTask      AS CHAR.
DEF VAR tokcounter  AS INT.
DEF VAR mesToken    AS CHAR NO-UNDO.
DEF VAR mesValue    AS CHAR NO-UNDO.
DEF VAR rCode AS CHAR.

DEF INPUT PARAMETER currcode AS CHAR.
DEF INPUT PARAMETER rmtype   AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR ratecode-list.
DEF OUTPUT PARAMETER TABLE FOR t-list.

DEF VARIABLE doit AS LOGICAL NO-UNDO.

FOR EACH ratecode WHERE ratecode.code = currcode NO-LOCK:
   
    ifTask = ratecode.char1[5].
    DO tokcounter = 1 TO NUM-ENTRIES(ifTask, ";") - 1:
      mesToken = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 1, 2).
      mesValue = TRIM(SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 3)).
      CASE mesToken:
          WHEN "RT" THEN rCode   = mesValue.
      END CASE.
    END.
    IF rCode = rmtype THEN
    DO:
      ASSIGN doit = YES.
      FIND FIRST queasy WHERE queasy.KEY = 264
            AND queasy.char1 = mesValue NO-LOCK NO-ERROR.
      IF AVAILABLE queasy THEN ASSIGN doit = NOT queasy.logi1.

      IF doit THEN DO:
          FIND FIRST ratecode-list WHERE ratecode-list.rcode = mesValue
            NO-ERROR.
          IF NOT AVAILABLE ratecode-list THEN
          DO:
            CREATE t-list.
            ASSIGN t-list.mesValue = mesValue.
            /*MTcontrate:ADD-LAST(mesValue) IN FRAME frame1.*/
            CREATE ratecode-list.
            ASSIGN ratecode-list.rcode = mesValue.
          END.
      END.
    END.
END.
