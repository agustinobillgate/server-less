
DEF INPUT  PARAMETER ci-date    AS DATE.
DEF INPUT  PARAMETER zinr       AS CHAR.
DEF OUTPUT PARAMETER err-no     AS INT INIT 0.

DEF BUFFER resline FOR res-line.

FIND FIRST res-line WHERE res-line.resstatus = 8 
  AND res-line.abreise = ci-date 
  AND res-line.zinr = zinr NO-LOCK NO-ERROR. 
IF NOT AVAILABLE res-line THEN 
DO: 
    err-no = 1.
    /**
    hide MESSAGE NO-PAUSE. 
    MESSAGE translateExtended ("No checked-out guests found.",lvCAREA,"") 
      VIEW-AS ALERT-BOX INFORMATION. 
    APPLY "entry" TO zinr IN FRAME frame2.
    */
END. 
ELSE 
DO: 
    FIND FIRST resline WHERE resline.resnr NE res-line.resnr 
      AND resline.zinr = zinr 
      AND resline.active-flag = 1 NO-LOCK NO-ERROR. 
    IF AVAILABLE resline THEN 
    DO: 
        err-no = 2.
        /**
        hide MESSAGE NO-PAUSE. 
        MESSAGE translateExtended ("Other inhouse guest different reservation number found,",lvCAREA,"") 
        SKIP 
        translateExtended ("re-checkin no longer possible.",lvCAREA,"") 
            VIEW-AS ALERT-BOX INFORMATION. 
        APPLY "entry" TO zinr IN FRAME frame2. 
        */
    END. 
    ELSE 
    DO: 
        err-no = 3.
        /**
        room = zinr. 
        APPLY "choose" TO btn-cancel IN FRAME frame2.
        */
    END. 
END.
