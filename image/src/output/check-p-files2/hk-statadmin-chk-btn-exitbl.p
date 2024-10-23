
DEF INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF INPUT PARAMETER resflag AS LOGICAL.
DEF INPUT PARAMETER dept AS INT.
DEF INPUT PARAMETER zinr AS CHAR.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF OUTPUT PARAMETER flag AS INT INIT 0.
DEF OUTPUT PARAMETER msg-str AS CHAR.
DEF OUTPUT PARAMETER resname AS CHAR.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "hk-statadmin".

IF NOT resflag THEN /* OM with reservation */ 
DO: 
  FIND FIRST res-line WHERE res-line.resnr = dept 
      AND res-line.zinr = zinr NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE res-line THEN 
  DO: 
    flag = 1.
    RETURN NO-APPLY. 
  END. 
  IF res-line.active-flag = 1 THEN 
  DO: 
    flag = 2.
    RETURN NO-APPLY. 
  END. 
  resname = res-line.name.
  
  FIND FIRST outorder WHERE outorder.zinr = zinr AND outorder.betriebsnr 
    = dept NO-LOCK NO-ERROR. 
  IF AVAILABLE outorder THEN 
  DO: 
    flag = 3.
    msg-str = translateExtended ("Room already blocked from",lvCAREA,"") + 
            " " + STRING(outorder.gespstart) + " " + 
            translateExtended ("to",lvCAREA,"") + " " + 
            STRING(outorder.gespend).
    RETURN NO-APPLY. 
  END. 
END. 
ELSE /* OM without reservation */ 
DO: 
  FIND FIRST outorder NO-LOCK WHERE outorder.zinr = zinr AND 
    outorder.betriebsnr = dept                           AND 
    NOT outorder.gespstart GT to-date                    AND
    NOT outorder.gespende  LT from-date NO-ERROR. 
  IF AVAILABLE outorder THEN 
  DO: 
    flag = 4.
    msg-str = translateExtended ("Room already blocked from",lvCAREA,"") + 
            " " + STRING(outorder.gespstart) + " " + 
            translateExtended ("to",lvCAREA,"") + " " + STRING(outorder.gespend).
    RETURN NO-APPLY. 
  END. 
END. 
