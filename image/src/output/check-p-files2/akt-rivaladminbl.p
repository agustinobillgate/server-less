
DEFINE TEMP-TABLE t-akt-code LIKE akt-code.

DEF INPUT  PARAMETER pvILanguage    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER case-type      AS INT.
DEF INPUT  PARAMETER TABLE FOR t-akt-code.
DEF INPUT  PARAMETER aktionscode    AS INTEGER.
DEF INPUT  PARAMETER aktiongrup     AS INTEGER.
DEF INPUT  PARAMETER bezeich        AS CHAR.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER success-flag   AS LOGICAL INIT NO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "akt-rivaladmin". 

DEFINE buffer akt-code1 FOR akt-code. 

FIND FIRST t-akt-code.
RUN validate-it.
IF case-type = 1 THEN       /** add **/
DO :
    create akt-code. 
    RUN fill-akt-code.
    success-flag = YES.
END.
ELSE IF case-type = 2 THEN  /** chg **/
DO:
    FIND FIRST akt-code WHERE akt-code.aktiongrup = aktiongrup AND 
        akt-code.aktionscode = aktionscode
        AND akt-code.bezeich = bezeich EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE akt-code THEN
    DO:
        RUN fill-akt-code.
        success-flag = YES.
        FIND CURRENT akt-code NO-LOCK.
    END.
END.


PROCEDURE fill-akt-code:
  akt-code.aktiongrup   = 4.
  akt-code.aktionscode  = t-akt-code.aktionscode. 
  akt-code.bezeich      = t-akt-code.bezeich. 
  akt-code.bemerkung    = t-akt-code.bemerkung. 
END. 

PROCEDURE validate-it:
  FIND FIRST akt-code1 WHERE akt-code1.bezeich = t-akt-code.bezeich 
     AND akt-code1.aktionscode NE t-akt-code.aktionscode NO-LOCK NO-ERROR. 
  IF AVAILABLE akt-code1 THEN 
  DO: 
    msg-str = msg-str + CHR(2) + "&W"
            + translateExtended ("Other Competitor Name exists with the same description.",lvCAREA,"").
  END.

  FIND FIRST akt-code1 WHERE akt-code1.bezeich = t-akt-code.bezeich 
     AND akt-code1.aktionscode NE t-akt-code.aktionscode NO-LOCK NO-ERROR. 
  IF AVAILABLE akt-code1 THEN 
  DO: 
    msg-str = msg-str + CHR(2) + "&W"
            + translateExtended ("Other Competitor Name exists with the same description.",lvCAREA,"").
  END. 
END.
