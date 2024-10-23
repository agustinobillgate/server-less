DEF TEMP-TABLE t-zimkateg
    FIELD kurzbez LIKE zimkateg.kurzbez.
    
DEF TEMP-TABLE queasy2
    FIELD char1 LIKE queasy.char1.
    
DEFINE TEMP-TABLE t-guest-pr LIKE guest-pr.
DEFINE TEMP-TABLE t-queasy159 LIKE queasy.
DEFINE TEMP-TABLE t-queasy160 LIKE queasy.

DEFINE TEMP-TABLE t-queasy201 LIKE queasy.

DEFINE INPUT PARAMETER booken-selected  AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER ci-date            AS DATE NO-UNDO.
DEF OUTPUT PARAMETER i-param439         AS INT NO-UNDO.
DEF OUTPUT PARAMETER cUsername          AS CHARACTER.
DEF OUTPUT PARAMETER cPassword          AS CHARACTER.
DEF OUTPUT PARAMETER vcWSAgent          AS CHARACTER.
DEF OUTPUT PARAMETER htl-code           AS CHARACTER.
DEF OUTPUT PARAMETER pushRate           AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR queasy2.
DEF OUTPUT PARAMETER TABLE FOR t-zimkateg.
DEFINE OUTPUT PARAMETER TABLE FOR t-guest-pr.
DEFINE OUTPUT PARAMETER TABLE FOR t-queasy159.
define output parameter table for t-queasy160.
define output parameter table for t-queasy201.

DEFINE VARIABLE gastnr AS INTEGER NO-UNDO.

RUN htpdate.p(87, OUTPUT ci-date).
RUN htpint.p(439, OUTPUT i-param439).

FIND FIRST queasy WHERE queasy.key = 159
    AND queasy.number1 = booken-selected NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    gastnr = queasy.number2.
END.    

FOR EACH queasy WHERE queasy.KEY = 2 AND queasy.logi2 NO-LOCK 
    BY queasy.char1:

    CREATE queasy2.
    ASSIGN
    queasy2.char1 = queasy.char1.
END.

FOR EACH zimkateg NO-LOCK:
    CREATE t-zimkateg.
    ASSIGN t-zimkateg.kurzbez = zimkateg.kurzbez.
END.

FOR EACH guest-pr WHERE guest-pr.gastnr = gastnr NO-LOCK:
    CREATE t-guest-pr.
    BUFFER-COPY guest-pr TO t-guest-pr.
END.

FOR EACH queasy WHERE queasy.key = 159 NO-LOCK:
    CREATE t-queasy159.
    BUFFER-COPY queasy TO t-queasy159.
END.

FOR EACH queasy WHERE queasy.key = 160 NO-LOCK:
    CREATE t-queasy160.
    BUFFER-COPY queasy TO t-queasy160.
END.

FOR EACH queasy WHERE queasy.key = 201 NO-LOCK:
    CREATE t-queasy201.
    BUFFER-COPY queasy TO t-queasy201.
END.
/*Move From UI for vhpWeb Based*/
FIND FIRST t-queasy160 WHERE t-queasy160.number1 EQ 3 NO-LOCK NO-ERROR. /*hardcode number1*/
IF AVAILABLE t-queasy160 THEN
DO:            
    cUsername   = ENTRY(3,ENTRY(9,t-queasy160.char1,";"),"$").
    cPassword   = ENTRY(3,ENTRY(10,t-queasy160.char1,";"),"$").
    vcWSAgent   = ENTRY(18,ENTRY(7,t-queasy160.char1,";"),"=").
    htl-code    = ENTRY(3,ENTRY(8,t-queasy160.char1,";"),"$").
    pushRate    = LOGICAL(ENTRY(3,ENTRY(11,t-queasy160.char1,";"),"$")).
END.  
