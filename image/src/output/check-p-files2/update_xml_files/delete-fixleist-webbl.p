
DEFINE INPUT  PARAMETER case-type  AS INTEGER.
DEFINE INPUT  PARAMETER int1       AS INTEGER.
DEFINE INPUT  PARAMETER user-init  AS CHAR. /* Dzikri 44C4DB - log fixcost */
DEFINE OUTPUT PARAMETER succesFlag AS LOGICAL INIT NO.

DEFINE VARIABLE is-fixrate AS CHAR INITIAL "NO". /* Dzikri 44C4DB - log fixcost */

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST fixleist WHERE RECID(fixleist) = int1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE fixleist THEN
        DO:
            /* Dzikri 44C4DB - log fixcost, check if reservation fixrate or not */
            FIND FIRST reslin-queasy WHERE reslin-queasy.key EQ "arrangement"
            AND reslin-queasy.resnr    EQ fixleist.resnr
            AND reslin-queasy.reslinnr EQ fixleist.reslinnr NO-LOCK NO-ERROR.
            IF AVAILABLE reslin-queasy THEN is-fixrate = "YES".
            /* Dzikri 44C4DB - END */
            /* Dzikri 44C4DB - log fixcost */
            FIND FIRST res-line WHERE res-line.resnr = fixleist.resnr
                AND res-line.reslinnr = fixleist.reslinnr
                NO-LOCK NO-ERROR.
            RUN res-changes.
            /* Dzikri 44C4DB - END */
            DELETE fixleist.
            RELEASE fixleist.
            succesFlag = YES.
        END.
    END.
END CASE.

/* Dzikri 44C4DB - log fixcost */
PROCEDURE res-changes:
DEF VAR cid   AS CHAR NO-UNDO INIT "".
DEF VAR cdate AS CHAR NO-UNDO FORMAT "x(8)" INIT "        ". 
DEF BUFFER rqy FOR reslin-queasy.

    IF NOT AVAILABLE res-line THEN RETURN.
    IF res-line.active-flag = 2 THEN RETURN.

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
            + STRING("Fixcost DELETED:") + ";" 
            + STRING(fixleist.artnr) 
            + "-" + STRING(fixleist.bezeich) + ";"
            + STRING(is-fixrate, "x(3)") + ";" 
            + STRING(is-fixrate, "x(3)") + ";" 
    .
    FIND CURRENT rqy NO-LOCK.
    RELEASE rqy. 
END.
/* Dzikri 44C4DB - END */
