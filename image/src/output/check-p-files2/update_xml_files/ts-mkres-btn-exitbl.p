
DEFINE INPUT PARAMETER pvILanguage      AS INTEGER  NO-UNDO.
DEF INPUT-OUTPUT PARAMETER moved-tisch  AS INTEGER format ">>>9 ".
DEF INPUT PARAMETER s-recid             AS INT.
DEF INPUT PARAMETER curr-dept           AS INT.
DEF INPUT PARAMETER curr-date           AS DATE.
DEF INPUT PARAMETER von-zeit            AS CHAR.
DEF INPUT PARAMETER bis-zeit            AS CHAR.

DEF INPUT PARAMETER pax         AS INT.
DEF INPUT PARAMETER telefon     AS CHAR.
DEF INPUT PARAMETER gname       AS CHAR.
DEF INPUT PARAMETER user-init   AS CHAR.
DEF INPUT PARAMETER comments    AS CHAR.
DEF OUTPUT PARAMETER msg-str    AS CHAR.
DEF OUTPUT PARAMETER done       AS LOGICAL INITIAL NO.

DEFINE BUFFER   qsy      FOR queasy.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-mkres".

IF s-recid EQ 0 THEN
DO:
    FIND FIRST qsy WHERE qsy.KEY = 33 AND qsy.number1 = curr-dept
        AND qsy.number2 = moved-tisch AND qsy.date1 = curr-date
        AND qsy.logi3 = YES
        AND von-zeit GE SUBSTR(qsy.char1,1,4)
        AND von-zeit LE SUBSTR(qsy.char1,5,4) NO-LOCK NO-ERROR.
    IF NOT AVAILABLE qsy THEN
    FIND FIRST qsy WHERE qsy.KEY = 33 AND qsy.number1 = curr-dept
        AND qsy.number2 = moved-tisch AND qsy.date1 = curr-date
        AND qsy.logi3 = YES
        AND bis-zeit GE SUBSTR(qsy.char1,1,4)
        AND bis-zeit LE SUBSTR(qsy.char1,5,4) NO-LOCK NO-ERROR.
    IF NOT AVAILABLE qsy THEN
    FIND FIRST qsy WHERE qsy.KEY = 33 AND qsy.number1 = curr-dept
        AND qsy.number2 = moved-tisch AND qsy.date1 = curr-date
        AND qsy.logi3 = YES
        AND SUBSTR(qsy.char1,1,4) GE von-zeit
        AND SUBSTR(qsy.char1,1,4) LE bis-zeit NO-LOCK NO-ERROR.
    IF NOT AVAILABLE qsy THEN
    FIND FIRST qsy WHERE qsy.KEY = 33 AND qsy.number1 = curr-dept
        AND qsy.number2 = moved-tisch AND qsy.date1 = curr-date
        AND qsy.logi3 = YES
        AND SUBSTR(qsy.char1,5,4) GE von-zeit
        AND SUBSTR(qsy.char1,5,4) LE bis-zeit NO-LOCK NO-ERROR.
END.
ELSE
DO:
    FIND FIRST qsy WHERE qsy.KEY = 33 AND qsy.number1 = curr-dept
        AND qsy.number2 = moved-tisch AND qsy.date1 = curr-date
        AND qsy.logi3 = YES
        AND von-zeit GE SUBSTR(qsy.char1,1,4)
        AND von-zeit LE SUBSTR(qsy.char1,5,4) 
        AND RECID(qsy) NE s-recid NO-LOCK NO-ERROR.
    IF NOT AVAILABLE qsy THEN
    FIND FIRST qsy WHERE qsy.KEY = 33 AND qsy.number1 = curr-dept
        AND qsy.number2 = moved-tisch AND qsy.date1 = curr-date
        AND qsy.logi3 = YES
        AND bis-zeit GE SUBSTR(qsy.char1,1,4)
        AND bis-zeit LE SUBSTR(qsy.char1,5,4)
        AND RECID(qsy) NE s-recid NO-LOCK NO-ERROR.
    IF NOT AVAILABLE qsy THEN
    FIND FIRST qsy WHERE qsy.KEY = 33 AND qsy.number1 = curr-dept
        AND qsy.number2 = moved-tisch AND qsy.date1 = curr-date
        AND qsy.logi3 = YES
        AND SUBSTR(qsy.char1,1,4) GE von-zeit
        AND SUBSTR(qsy.char1,1,4) LE bis-zeit 
        AND RECID(qsy) NE s-recid NO-LOCK NO-ERROR.
    IF NOT AVAILABLE qsy THEN
    FIND FIRST qsy WHERE qsy.KEY = 33 AND qsy.number1 = curr-dept
        AND qsy.number2 = moved-tisch AND qsy.date1 = curr-date
        AND qsy.logi3 = YES
        AND SUBSTR(qsy.char1,5,4) GE von-zeit
        AND SUBSTR(qsy.char1,5,4) LE bis-zeit
        AND RECID(qsy) NE s-recid NO-LOCK NO-ERROR.
END.
IF AVAILABLE qsy THEN
DO:
    msg-str = msg-str + CHR(2)
            + translateExtended ("Overlapping Reservation time found:",lvCAREA,"")
            + CHR(10)
            + ENTRY(1, qsy.char2,"&&") + " " + STRING(SUBSTR(qsy.char1,1,4),"99:99") + " - "
            + STRING(SUBSTR(qsy.char1,5,4),"99:99").
    RETURN NO-APPLY.
END.

IF s-recid EQ 0 THEN /* NEW */
DO:
    CREATE queasy.
    ASSIGN
        queasy.KEY = 33
        queasy.number1 = curr-dept
        queasy.number2 = moved-tisch
        queasy.number3 = pax
        queasy.date1   = curr-date
        queasy.date2   = TODAY
        queasy.char1   = von-zeit + bis-zeit + ";" + telefon
        queasy.char2   = gname + "&&"
        queasy.char3   = user-init + ";" + REPLACE(comments, ";", ",") + ";"
        queasy.logi3   = YES
    .
    FIND CURRENT queasy NO-LOCK.
    done = YES.
END.
ELSE
DO:
    FIND FIRST queasy WHERE RECID(queasy) = s-recid EXCLUSIVE-LOCK.
    ASSIGN
        queasy.number2 = moved-tisch
        queasy.number3 = pax
        queasy.date3   = TODAY
        queasy.char1   = von-zeit + bis-zeit + ";" + telefon
        queasy.char2   = gname + "&&"
        /*queasy.char3   = queasy.char3 + user-init + ";"*/
        queasy.char3   = user-init + ";" + REPLACE(comments, ";", ",") + ";"
    .
    FIND CURRENT queasy NO-LOCK.
    done = YES.
END.
