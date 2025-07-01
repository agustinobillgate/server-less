
DEF INPUT PARAMETER case-type   AS INT.
DEF INPUT PARAMETER int1        AS INT.
DEF INPUT PARAMETER char1       AS CHAR.
DEF INPUT PARAMETER date1       AS DATE.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

DEF VARIABLE user-init AS CHAR NO-UNDO. 

CASE case-type:
    WHEN 1 THEN
    DO:
        ASSIGN user-init = char1.
        FIND FIRST reslin-queasy WHERE RECID(reslin-queasy) = int1 
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE reslin-queasy THEN
        DO:
            FIND FIRST res-line WHERE res-line.resnr = reslin-queasy.resnr
                AND res-line.reslinnr = reslin-queasy.reslinnr
                NO-LOCK NO-ERROR.
            RUN res-changes.
            DELETE reslin-queasy.
            RELEASE reslin-queasy.
            success-flag = YES.
        END.
    END.
END CASE.

PROCEDURE res-changes:
DEF VAR cid   AS CHAR NO-UNDO INIT "".
DEF VAR cdate AS CHAR NO-UNDO FORMAT "x(8)" INIT "        ". 
DEF BUFFER rqy FOR reslin-queasy.

    IF NOT AVAILABLE res-line THEN RETURN.
    IF res-line.active-flag = 2 THEN RETURN. /* res-mode = "NEW" */

    IF res-line.changed NE ? THEN
    ASSIGN
        cid   = res-line.changed-id 
        cdate = STRING(res-line.changed)
    .

    CREATE rqy.
    ASSIGN
      rqy.key         = "ResChanges"
      rqy.resnr       = res-line.resnr
      rqy.reslinnr    = res-line.reslinnr
      rqy.date2       = TODAY
      rqy.number2     = TIME 
    .  
    rqy.char3 = STRING(res-line.ankunft) + ";" 
            + STRING(res-line.ankunft) + ";" 
            + STRING(res-line.abreise) + ";" 
            + STRING(res-line.abreise) + ";" 
            + STRING(res-line.zimmeranz) + ";" 
            + STRING(res-line.zimmeranz) + ";" 
            + STRING(res-line.erwachs) + ";" 
            + STRING(res-line.erwachs) + ";" 
            + STRING(res-line.kind1) + ";" 
            + STRING(res-line.kind1) + ";" 
            + STRING(res-line.gratis) + ";" 
            + STRING(res-line.gratis) + ";" 
            + STRING(res-line.zikatnr) + ";" 
            + STRING(res-line.zikatnr) + ";" 
            + STRING(res-line.zinr) + ";" 
            + STRING(res-line.zinr) + ";"
            + STRING(res-line.arrangement) + ";" 
            + STRING(res-line.arrangement) + ";"
            + STRING(res-line.zipreis) + ";" 
            + STRING(res-line.zipreis) + ";"
            + STRING(cid) + ";" 
            + STRING(user-init) + ";" 
            + STRING(cdate, "x(8)") + ";" 
            + STRING(TODAY) + ";" 
            + STRING("Fixrate DELETED:") + ";" 
            + STRING(reslin-queasy.date1) 
            + "-" + STRING(reslin-queasy.deci1) + ";"
            + STRING("YES", "x(3)") + ";" 
            + STRING("YES", "x(3)") + ";" 
    .
    FIND CURRENT rqy NO-LOCK.
    RELEASE rqy. 

END.
