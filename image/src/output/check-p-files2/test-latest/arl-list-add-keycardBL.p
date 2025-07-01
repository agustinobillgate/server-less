DEFINE BUFFER resline FOR res-line. 
DEFINE BUFFER rline FOR res-line. 

DEF TEMP-TABLE t-keycard
    FIELD msg-str AS CHAR
    FIELD rline-betrieb-gast LIKE rline.betrieb-gast
    FIELD rline-resstatus LIKE rline.resstatus
    FIELD resline-resnr LIKE resline.resnr
    FIELD resline-reslinnr LIKE resline.reslinnr
    FIELD rline-recid AS INT.

DEFINE INPUT  PARAMETER pvILanguage             AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER recid-resline           AS INTEGER.
DEFINE INPUT  PARAMETER keyint                  AS INTEGER.
DEFINE OUTPUT PARAMETER msg-str                 AS CHAR.
DEFINE OUTPUT PARAMETER anz0                    AS INTEGER. 
DEFINE OUTPUT PARAMETER do-it                   AS LOGICAL NO-UNDO. 
DEFINE OUTPUT PARAMETER card-type               AS CHAR INITIAL "" NO-UNDO. 
DEFINE OUTPUT PARAMETER case1                   AS INT INIT 0.
DEFINE OUTPUT PARAMETER resline-reslinnr        AS INT.
DEFINE OUTPUT PARAMETER resline-resnr           AS INT.
DEFINE OUTPUT PARAMETER err-flag                AS INT INIT 0.
DEFINE OUTPUT PARAMETER resline-betrieb-gast    AS INT.
DEFINE OUTPUT PARAMETER resline-resstatus       AS INT.
DEFINE OUTPUT PARAMETER resline-recid           AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR t-keycard.

DEF VAR lvCAREA AS CHAR INITIAL "arl-list".

DEFINE VARIABLE resno AS INTEGER. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE maxkey AS INTEGER INITIAL 2 NO-UNDO. 
DEFINE VARIABLE replaced AS LOGICAL INITIAL NO NO-UNDO. 

FIND FIRST res-line WHERE RECID(res-line) = recid-resline NO-LOCK NO-ERROR. /* Malik Serverless : tanpa ada NO-LOCK NO-ERROR -> NO-LOCK NO-ERROR */
IF NOT AVAILABLE res-line THEN RETURN. /* Malik Serverless */

FIND FIRST htparam WHERE paramnr = 926 NO-LOCK. 
anz0 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 927 NO-LOCK. 
IF htparam.finteger NE 0 THEN maxkey = htparam.finteger. 
IF res-line.resstatus = 11 OR res-line.resstatus = 13 THEN maxkey = 1. 
 
ELSE IF keyint = 1 THEN /* generate a keycard */ 
DO: 
    FIND FIRST resline WHERE resline.active-flag LE 1 
        AND ((resline.ankunft = res-line.ankunft) OR (resline.abreise = res-line.ankunft)) 
        AND resline.zinr = res-line.zinr AND resline.betrieb-gast > 0 
        AND resline.resnr NE res-line.resnr NO-LOCK NO-ERROR. 
    IF AVAILABLE resline THEN 
    DO: 
        err-flag = 1.
        msg-str = msg-str + CHR(2) + "Keycard is being used for other guest: " + resline.NAME.
        RETURN. 
    END. 
 
    FIND FIRST resline WHERE RECID(resline) = RECID(res-line) NO-LOCK. 
    IF resline.betrieb-gast GE maxkey THEN 
    DO: 
        err-flag = 2.
        msg-str = msg-str + CHR(2)
              + "Number of given KeyCard = " + STRING(resline.betrieb-gast)
              + CHR(10)
              + "No more KeyCard can be generated for room " + resline.zinr.
        RETURN. 
    END. 
 
    /*  cardtype=1 or "" -> maincard, cardtype=2 sharer, cardtype=3 Lost keycard */
    card-type = "cardtype=1". 
    FIND FIRST rline WHERE rline.resnr = res-line.resnr 
        AND rline.reslinnr NE res-line.resnr 
        AND rline.zinr = res-line.zinr 
        AND rline.active-flag LE 1
        AND rline.betrieb-gast > 0 NO-LOCK NO-ERROR.     
    IF AVAILABLE rline THEN card-type = "cardtype=2". 
 
    IF resline.betrieb-gast = 0 AND resline.resstatus NE 11 AND resline.resstatus NE 13 THEN case1 = 1.
    ELSE case1 = 2.
    ASSIGN
    resline-reslinnr = resline.reslinnr
    resline-resnr    = resline.resnr
    resline-recid    = RECID(resline).
END. 
 
ELSE IF keyint = 2 THEN /* replace keycards */ 
DO: 
    FIND FIRST resline WHERE RECID(resline) = RECID(res-line) NO-LOCK. 
    IF resline.betrieb-gast = 0 THEN 
    DO: 
        err-flag = 1.
        RETURN. 
    END. 
 
    IF (resline.resstatus = 11 OR resline.resstatus = 13) THEN err-flag = 2.
 
    /*  cardtype=1 or "" means maincard, cardtype=2 sharer, cardtype=3 One Shot */
    ASSIGN
        card-type            = "cardtype=1"
        resline-betrieb-gast = resline.betrieb-gast
        resline-reslinnr     = resline.reslinnr
        resline-resnr        = resline.resnr
        resline-resstatus    = resline.resstatus.
 
    IF (resline.resstatus = 1 OR resline.resstatus = 6) AND replaced THEN 
    DO: 
        FIND FIRST rline WHERE rline.resnr = resline.resnr 
            AND (rline.resstatus = 11 OR rline.resstatus = 13) 
            AND rline.zinr = resline.zinr AND rline.betrieb-gast GT 0 NO-LOCK NO-ERROR. 
        IF AVAILABLE rline THEN 
        DO: 
          msg-str = msg-str + CHR(2) + "&W" + "Room Shrer found. Replace the KeyCard too.".
        END. 
    END. 
END. 

ELSE IF keyint = 3 THEN  /* arrival group */ 
DO: 
    FIND FIRST resline WHERE RECID(resline) = RECID(res-line) NO-LOCK. 
    resno = resline.resnr. 
    IF anz0 = 0 THEN anz0 = resline.erwachs. 
    FOR EACH resline WHERE resline.resnr = resno 
        AND resline.active-flag = 0 AND resline.zinr NE "" 
        /*AND resline.betrieb-gast = 0*/ NO-LOCK BY resline.zinr BY resline.resstatus: 

        FIND FIRST rline WHERE rline.active-flag LE 1 
            AND ((rline.ankunft = resline.ankunft) OR (rline.abreise = resline.ankunft)) 
            AND rline.zinr = resline.zinr 
            AND rline.betrieb-gast > 0 
            AND rline.resnr NE resline.resnr NO-LOCK NO-ERROR. 

        CREATE t-keycard.
        
        do-it = NOT AVAILABLE rline. 
        IF NOT do-it THEN 
        DO: 
            t-keycard.msg-str = msg-str + CHR(2) + "RmNo " + rline.zinr + " Keycard is being used for other guest: " + rline.NAME.
        END. 
        ELSE FIND FIRST rline WHERE RECID(rline) = RECID(resline) NO-LOCK. 

        ASSIGN
            t-keycard.rline-betrieb-gast = rline.betrieb-gast
            t-keycard.rline-resstatus = rline.resstatus
            t-keycard.resline-resnr = resline.resnr
            t-keycard.resline-reslinnr = resline.reslinnr
            t-keycard.rline-recid = RECID(rline).

        IF resline.betrieb-gast GE maxkey THEN 
        DO: 
            t-keycard.msg-str = "Number of given KeyCard = " + STRING(resline.betrieb-gast) + CHR(10) + "No more KeyCard can be generated for room " + resline.zinr.
        END. 
    END. 
END. 
