
DEF INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF INPUT PARAMETER dept AS INT.
DEF INPUT PARAMETER zinr AS CHAR.
DEF OUTPUT PARAMETER avail-resline AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER avail-outorder AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER res-activeflag AS INT.
DEF OUTPUT PARAMETER msg-str AS CHAR.
DEF OUTPUT PARAMETER resname AS CHAR.
DEF OUTPUT PARAMETER from-date AS DATE.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "hk-statadmin".

FIND FIRST res-line WHERE res-line.resnr = dept 
  AND res-line.zinr = zinr NO-LOCK NO-ERROR. 
IF AVAILABLE res-line THEN
DO:
    avail-resline = YES.
    IF res-line.active-flag = 1 THEN
    DO:
        res-activeflag = res-line.active-flag.
        RETURN NO-APPLY. 
    END.
END.


FIND FIRST outorder WHERE outorder.zinr = zinr AND outorder.betriebsnr 
  = dept NO-LOCK NO-ERROR. 
IF AVAILABLE outorder THEN
DO:
    msg-str = translateExtended ("Room already blocked from",lvCAREA,"") 
            + " " + STRING(outorder.gespstart) 
            + " " + translateExtended ("to",lvCAREA,"") + " " 
            + STRING(outorder.gespend).
    RETURN NO-APPLY.
END.

IF AVAILABLE res-line THEN
DO:
    resname = res-line.name. 
    from-date = res-line.ankunft. 
END.
