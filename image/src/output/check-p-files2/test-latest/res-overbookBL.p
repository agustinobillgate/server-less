
DEFINE INPUT PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER res-mode     AS CHAR. 
DEFINE INPUT PARAMETER inp-resnr    AS INTEGER. 
DEFINE INPUT PARAMETER inp-reslinnr AS INTEGER. 
DEFINE INPUT PARAMETER inp-ankunft  AS DATE. 
DEFINE INPUT PARAMETER inp-abreise  AS DATE. 
DEFINE INPUT PARAMETER qty          AS INTEGER. 
DEFINE INPUT PARAMETER rmcat        AS CHAR. 
DEFINE INPUT PARAMETER bed-setup    AS CHAR. 
DEFINE INPUT PARAMETER ask-it       AS LOGICAL. 
DEFINE OUTPUT PARAMETER overbook    AS LOGICAL INITIAL NO. 
DEFINE OUTPUT PARAMETER overmax     AS LOGICAL INITIAL NO. 
DEFINE OUTPUT PARAMETER overanz     AS INTEGER INITIAL 0. 
DEFINE OUTPUT PARAMETER overdate    AS DATE. 
DEFINE OUTPUT PARAMETER incl-allot  AS LOGICAL INITIAL NO. 
DEFINE OUTPUT PARAMETER msg-str     AS CHAR INITIAL "".
DEFINE OUTPUT PARAMETER zimkateg-overbook AS INT.

/* 
DEFINE VARIABLE inp-ankunft AS DATE INITIAL 05/05/04. 
DEFINE VARIABLE inp-abreise AS DATE INITIAL 05/06/04. 
DEFINE VARIABLE qty AS INTEGER INITIAL 20. 
DEFINE VARIABLE rmcat AS CHAR FORMAT "x(6)" INITIAL "SUP". 
DEFINE VARIABLE overbook AS LOGICAL INITIAL NO. 
DEFINE VARIABLE overmax AS LOGICAL INITIAL NO. 
DEFINE VARIABLE overanz AS INTEGER INITIAL 0. 
DEFINE VARIABLE overdate AS DATE. 
abreise = today + 1. 
*/ 

DEF TEMP-TABLE occ-list
    FIELD datum      AS DATE
    FIELD anz-avail  AS INTEGER INIT 0
    FIELD anz-alot   AS INTEGER INIT 0
    FIELD anz-ooo    AS INTEGER INIT 0
    INDEX datum_ix datum
.

DEFINE VARIABLE origcontcode AS CHAR    NO-UNDO INIT "".
DEFINE VARIABLE statcode     AS CHAR    NO-UNDO INIT "".
DEFINE VARIABLE res-argt     AS CHAR    NO-UNDO INIT "".

DEFINE VARIABLE curr-date AS DATE. 
DEFINE VARIABLE i         AS INTEGER INITIAL 0. 
DEFINE VARIABLE anz       AS INTEGER INITIAL 0. 
DEFINE VARIABLE anz0      AS INTEGER INITIAL 0. 
DEFINE VARIABLE anzooo    AS INTEGER INITIAL 0. 
DEFINE VARIABLE anzalot   AS INTEGER INITIAL 0. 
DEFINE VARIABLE delta     AS INTEGER               NO-UNDO. 
DEFINE VARIABLE maxzimmer AS INTEGER INITIAL 0     NO-UNDO.
DEFINE VARIABLE ci-date   AS DATE                  NO-UNDO.
DEFINE VARIABLE overbook-flag AS LOGICAL INIT NO   NO-UNDO.
DEFINE VARIABLE do-it    AS LOGICAL. 

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "res-overbook". 

RUN htpdate.p(87, OUTPUT ci-date).
IF NUM-ENTRIES(rmcat, ";") GT 1 THEN
ASSIGN
    origcontcode = ENTRY(2, rmcat, ";")
    statcode     = ENTRY(3, rmcat, ";")
    res-argt     = ENTRY(4, rmcat, ";")
    rmcat        = ENTRY(1, rmcat, ";") NO-ERROR
.

FIND FIRST zimkateg WHERE zimkateg.kurzbez = rmcat NO-LOCK NO-ERROR. 
ASSIGN zimkateg-overbook = zimkateg.overbooking.

/* IF res-argt NE "" THEN FIND FIRST arrangement WHERE arrangement.arrangement = res-argt NO-LOCK NO-ERROR.  */

RUN check-allotment-by-ratecode.

FOR EACH zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr AND zimmer.sleeping:
    ASSIGN maxzimmer = maxzimmer + 1.
END.
 
curr-date = inp-ankunft. 
FIND FIRST res-line WHERE res-line.resnr = inp-resnr AND res-line.reslinnr = inp-reslinnr NO-LOCK NO-ERROR.
IF AVAILABLE res-line THEN
DO:
    IF res-line.active-flag = 1 THEN curr-date = ci-date.
END.

DO WHILE curr-date LT inp-abreise: 
    FIND FIRST occ-list WHERE occ-list.datum = curr-date NO-ERROR.
    IF NOT AVAILABLE occ-list THEN
    DO:
        CREATE occ-list.
        ASSIGN
        occ-list.datum    = curr-date
        occ-list.anz-avail = maxzimmer - qty
        .
    END.
    FOR EACH res-line WHERE res-line.active-flag LE 1 AND res-line.resstatus LE 6 
        AND res-line.resstatus NE 3 AND res-line.resstatus NE 4 
        AND res-line.ankunft LE curr-date AND res-line.abreise GT curr-date 
        AND res-line.zikatnr = zimkateg.zikatnr NO-LOCK: 
        IF (res-mode = "new" OR res-mode = "insert" OR res-mode = "qci") AND (res-line.resnr EQ inp-resnr AND res-line.reslinnr EQ inp-reslinnr) THEN . 
        ELSE do-it = NO.
        IF res-line.zinr NE "" THEN 
        DO: 
            FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
            do-it = zimmer.sleeping. 
        END. 
    
        IF do-it THEN 
        DO:
            /* SY 19 AUG 2015 not applicable for global reservation */
            IF res-line.kontignr GE 0 THEN
            DO:
                IF res-line.resnr EQ inp-resnr AND res-line.reslinnr EQ inp-reslinnr THEN  
                    ASSIGN occ-list.anz-avail = occ-list.anz-avail + res-line.zimmeranz.
                ELSE
                    ASSIGN occ-list.anz-avail = occ-list.anz-avail - res-line.zimmeranz.
            END.
            
            IF res-line.kontignr NE 0 THEN 
            DO: 
                /* allotment */
                IF res-line.kontignr GT 0 THEN 
                DO:
                    FIND FIRST kontline WHERE kontline.kontignr = res-line.kontignr NO-LOCK NO-ERROR.
                    IF AVAILABLE kontline AND curr-date GE (ci-date + kontline.ruecktage) THEN
                    DO:
                        /* global allotment */
                        FIND FIRST queasy WHERE queasy.KEY = 147 AND queasy.number1 = kontline.gastnr AND queasy.char1   = kontline.kontcode NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE queasy THEN occ-list.anz-alot = occ-list.anz-alot - res-line.zimmeranz. 
                    END.
                END.
            END.
        END. 
    END. 
    
    FOR EACH kontline WHERE kontline.gastnr > 0 AND kontline.ankunft LE curr-date 
        AND kontline.abreise GE curr-date AND kontline.zikatnr = zimkateg.zikatnr 
        AND kontline.kontstat = 1 NO-LOCK USE-INDEX gastnr_ix:    
        /* global reservation */
        IF kontline.betriebsnr = 1 THEN occ-list.anz-avail = occ-list.anz-avail - kontline.zimmeranz. 
        ELSE /* allotment */
        DO:
            /* global allotment for the OTA */    
            FIND FIRST queasy WHERE queasy.KEY = 147 AND queasy.number1 = kontline.gastnr AND queasy.char1 = kontline.kontcode NO-LOCK NO-ERROR.
            IF NOT AVAILABLE queasy AND curr-date GE (ci-date + kontline.ruecktage) THEN occ-list.anz-alot = occ-list.anz-alot + kontline.zimmeranz. 
        END.
    END.
        
    FOR EACH outorder WHERE outorder.gespstart LE curr-date                                     /* Rulita 191224 | Fixing serverless issue 251 from AND curr-date GE outorder.gespstart */
        AND outorder.gespende GE curr-date AND outorder.betriebsnr LE 1 NO-LOCK,                /* Rulita 061224 | Fixing serverless issue 251 from AND curr-date LE outorder.gespende */
        FIRST zimmer WHERE zimmer.zinr = outorder.zinr
        AND zimmer.sleeping = YES 
        AND zimmer.zikatnr = zimkateg.zikatnr NO-LOCK: 
        ASSIGN occ-list.anz-ooo = occ-list.anz-ooo + 1.
    END. 
    curr-date = curr-date + 1. 
END. 


FOR EACH occ-list BY occ-list.datum:
    IF (occ-list.anz-avail + zimkateg-overbook - occ-list.anz-ooo) LT 0 THEN
    DO:
        ASSIGN
        overanz  = - (occ-list.anz-avail + zimkateg-overbook - occ-list.anz-ooo)
        overdate = occ-list.datum
        .
        overbook = YES.
        IF NOT overbook THEN overmax = YES.
        LEAVE.
    END.
END.

IF overbook THEN RETURN.

IF NOT overmax THEN
FOR EACH occ-list BY occ-list.datum:
    IF (occ-list.anz-avail + zimkateg-overbook - occ-list.anz-ooo - occ-list.anz-alot) LT 0 THEN
    DO:
        ASSIGN
            overmax    = YES
            overanz    = - (occ-list.anz-avail + zimkateg-overbook - occ-list.anz-ooo - occ-list.anz-alot)
            overdate   = occ-list.datum
            incl-allot = YES
        .
        LEAVE.
    END.
END.

PROCEDURE check-allotment-by-ratecode:
    DEF VARIABLE occ-room           AS INTEGER  NO-UNDO INIT 0.
    DEF VARIABLE allotment          AS INTEGER  NO-UNDO INIT 0.
    DEF VARIABLE curr-i             AS INTEGER  NO-UNDO.
    DEF VARIABLE rline-origcode     AS CHAR     NO-UNDO.
    DEF VARIABLE str                AS CHAR     NO-UNDO.
    DEF VARIABLE ratecode-found     AS LOGICAL  NO-UNDO INIT NO.
    DEF VARIABLE doit-flag          AS LOGICAL  NO-UNDO.
    DEF VARIABLE curr-date          AS DATE     NO-UNDO.
    
    DEF BUFFER zbuff FOR zimkateg.
    DEF BUFFER rbuff FOR res-line.  
    
    IF origcontcode = "" OR statcode = "" THEN RETURN.
    
    FIND FIRST res-line WHERE res-line.resnr = inp-resnr AND res-line.reslinnr = inp-reslinnr NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
        IF zimkateg.typ = 0 THEN
        DO:
            FIND FIRST queasy WHERE queasy.char1 = origcontcode AND queasy.number1 = zimkateg.zikatnr AND queasy.KEY = 171 AND queasy.date1 = inp-ankunft AND queasy.number3 NE 0 NO-LOCK NO-ERROR.
            /*ASSIGN ratecode-found = AVAILABLE ratecode.
            IF ratecode-found THEN allotment = queasy.number3. */ /*masdod 211124 serverless*/
        END.
        ELSE
        DO:
            FIND FIRST queasy WHERE queasy.char1 = origcontcode AND queasy.number1 = zimkateg.typ AND queasy.KEY = 171 AND queasy.date1 = inp-ankunft AND queasy.number3 NE 0 NO-LOCK NO-ERROR.
            /*ASSIGN ratecode-found = AVAILABLE ratecode.
            IF ratecode-found THEN allotment = queasy.number3. */ /*masdod 211124 serverless*/
        END.
        IF NOT ratecode-found THEN RETURN.
        
        DO curr-date = inp-ankunft TO inp-abreise - 1:
            occ-room = 0.
            FOR EACH rbuff WHERE rbuff.gastnr = res-line.gastnr
                AND rbuff.active-flag LE 1
                AND rbuff.ankunft LE curr-date
                AND rbuff.abreise GT curr-date
                AND (rbuff.resstatus LE 6 AND rbuff.resstatus NE 3
                AND rbuff.resstatus NE 4) 
                AND rbuff.zimmer-wunsch MATCHES ("*$OrigCode$*") NO-LOCK:
                doit-flag = (rbuff.resnr NE inp-resnr) OR (rbuff.reslinnr NE inp-reslinnr).
                IF doit-flag AND zimkateg.typ = 0 THEN
                DO:
                    IF rbuff.zikatnr NE zimkateg.zikatnr
                    THEN doit-flag = NO.
                END.
                ELSE
                DO: 
                    FIND FIRST zbuff WHERE zbuff.zikatnr = rbuff.zikatnr NO-LOCK.
                    IF zbuff.typ NE zimkateg.typ THEN doit-flag = NO.
                END.
                IF doit-flag THEN
                DO:
                    IF res-argt NE rbuff.arrangement THEN doit-flag = NO.
                END.
                IF doit-flag THEN
                DO curr-i = 1 TO NUM-ENTRIES(rbuff.zimmer-wunsch,";") - 1:
                    str = ENTRY(curr-i, rbuff.zimmer-wunsch, ";").
                    IF SUBSTR(str,1,10) = "$OrigCode$" THEN 
                    DO:
                        rline-origcode  = SUBSTR(str,11).
                        IF rline-origcode = origcontcode THEN occ-room = occ-room + rbuff.zimmeranz.
                        LEAVE.
                    END.
                END.
            END.
            IF (occ-room + qty) GT allotment THEN 
            DO: 
                IF msg-str = "" THEN
                ASSIGN
                msg-str = "&Q" + translateExtended ("Allotment by Rate Code Overbooking found.",lvCAREA,"") + CHR(10) + STRING(curr-date) + " - " + translateExtended ("Actual Overbooking:",lvCAREA,"") + " " + STRING(occ-room + qty - allotment) + CHR(10).
                ELSE
                ASSIGN
                msg-str = msg-str + STRING(curr-date) + " - " + translateExtended ("Actual Overbooking:",lvCAREA,"") + " " + STRING(occ-room + qty - allotment) + CHR(10)
                .
            END.
        END.
        IF msg-str NE "" THEN msg-str = msg-str + translateExtended ("Do you wish to continue?",lvCAREA,"").
    END.
END.
