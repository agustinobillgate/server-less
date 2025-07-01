
DEF INPUT  PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER rec-id       AS INTEGER.
DEF INPUT  PARAMETER cReason      AS CHAR.
DEF INPUT  PARAMETER bediener-nr  AS INT.
DEF OUTPUT PARAMETER msg-str      AS CHAR.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "arl-list".

DEFINE VARIABLE user-nr AS CHAR NO-UNDO.

FIND FIRST res-line WHERE RECID(res-line) = rec-id NO-LOCK NO-ERROR.
IF AVAILABLE res-line THEN
DO:
    FIND FIRST outorder WHERE outorder.zinr = res-line.zinr 
         AND outorder.gespstart GE res-line.ankunft
         AND outorder.gespende LE res-line.ankunft NO-LOCK NO-ERROR.
    IF AVAILABLE outorder THEN
    DO:
        msg-str = msg-str + CHR(2)
                + translateExtended ("Room already blocked from",lvCAREA,"") 
                + " " + STRING(outorder.gespstart) 
                + " " + translateExtended ("to",lvCAREA,"") + " " 
                + STRING(outorder.gespend).
        RETURN NO-APPLY.
    END.
    
    DO TRANSACTION:
        FIND FIRST bediener WHERE bediener.nr = bediener-nr NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN ASSIGN user-nr = bediener.userinit.
        ELSE ASSIGN user-nr = STRING(bediener-nr).
    
        CREATE outorder.
        ASSIGN outorder.zinr   = res-line.zinr
            outorder.gespstart = res-line.ankunft
            outorder.gespende  = res-line.ankunft
            outorder.betriebsnr = res-line.resnr
            outorder.gespgrund = cReason + "$" + STRING(user-nr)
            outorder.betriebsnr = res-line.resnr.
        FIND CURRENT outorder NO-LOCK.
        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr
            EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
        IF AVAILABLE zimmer THEN
        DO:
          zimmer.bediener-nr-stat = bediener-nr.
          FIND CURRENT zimmer NO-LOCK.
          RELEASE zimmer.
        END.
    END.
END.

