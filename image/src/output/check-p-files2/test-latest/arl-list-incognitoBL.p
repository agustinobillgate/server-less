

DEF INPUT  PARAMETER t-resnr    AS INT.
DEF INPUT  PARAMETER t-reslinnr AS INT.
DEF INPUT  PARAMETER user-init  AS CHAR.

DEFINE VARIABLE cid AS CHAR FORMAT "x(2)" INITIAL "  ". 
DEFINE VARIABLE cdate AS CHAR FORMAT "x(8)" INITIAL "        ". 
DEFINE VARIABLE s AS CHAR. 

DEF BUFFER resline FOR res-line.
FIND FIRST res-line WHERE res-line.resnr = t-resnr 
    AND res-line.reslinnr = t-reslinnr NO-LOCK.
DO transaction: 
    FIND FIRST resline WHERE RECID(resline) = RECID(res-line) EXCLUSIVE-LOCK. 
    resline.pseudofix = NOT resline.pseudofix. 
 
    IF TRIM(resline.changed-id) NE "" THEN 
    DO: 
      cid = resline.changed-id. 
      cdate = STRING(resline.changed). 
    END. 
    resline.changed-id = user-init. 
    resline.changed = TODAY. 
    FIND CURRENT resline NO-LOCK. 
    IF resline.pseudofix THEN 
    DO:    
        s = "INCOGNITO ON". 
        IF resline.active-flag = 1 THEN 
          RUN intevent-1.p( 7, res-line.zinr, "Do Not Disturb ON!", 
            res-line.resnr, res-line.reslinnr). 
    END.
    ELSE
    DO:    
        s = "INCOGNITO OFF". 
        IF resline.active-flag = 1 THEN 
            RUN intevent-1.p( 8, res-line.zinr, "Do Not Disturb OFF!", 
                res-line.resnr, res-line.reslinnr). 
    END.
 
    CREATE reslin-queasy. 
    ASSIGN
      reslin-queasy.key = "ResChanges"
      reslin-queasy.resnr = res-line.resnr 
      reslin-queasy.reslinnr = res-line.reslinnr
      reslin-queasy.date2 = TODAY 
      reslin-queasy.number2 = TIME
    . 
    reslin-queasy.char3 = STRING(res-line.ankunft) + ";" 
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
                        + STRING(res-line.zinr, "x(6)") + ";"
                        + STRING(res-line.zinr, "x(6)") + ";"
                        + STRING(res-line.arrangement) + ";" 
                        + STRING(res-line.arrangement) + ";" 
                        + STRING(res-line.zipreis) + ";" 
                        + STRING(res-line.zipreis) + ";" 
                        + STRING(cid) + ";" 
                        + STRING(user-init) + ";" 
                        + STRING(" ") + ";" 
                        + STRING(TODAY) + ";" 
                        + STRING(res-line.NAME) + ";" 
                        + STRING(s, "x(16)") + ";" 
                        + STRING(" ") + ";" 
                        + STRING(" ") + ";". 
    
    FIND CURRENT reslin-queasy NO-LOCK.
    RELEASE reslin-queasy. 
END. 
