DEFINE TEMP-TABLE allot-list
    FIELD bezeich   AS CHAR
    FIELD allotment AS INT EXTENT 31 
    FIELD nr        AS INT
.

DEFINE INPUT PARAMETER currcode AS CHAR.
DEFINE INPUT PARAMETER rmtype   AS CHAR.
DEFINE INPUT PARAMETER curr-month AS INT.
DEFINE INPUT PARAMETER curr-year  AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR allot-list.
/*
DEFINE var currcode AS CHAR INIT "dyna".
DEFINE var rmtype   AS CHAR INIT "hrs".
DEFINE var curr-month AS INT INIT 01.
DEFINE var curr-year  AS INT INIT 2017.
*/
DEFINE VARIABLE cat-flag AS LOGICAL INIT NO.
DEFINE VARIABLE do-it    AS LOGICAL INIT NO.

DEFINE VARIABLE occAll AS INT EXTENT 31.
DEFINE VARIABLE occ    AS INT EXTENT 31.
DEFINE VARIABLE ooo    AS INT EXTENT 31.
DEFINE VARIABLE anzahl AS INT.
DEFINE VARIABLE i      AS INT.
DEFINE VARIABLE i-typ  AS INT.

DEFINE VARIABLE fdate        AS DATE.
DEFINE VARIABLE tdate        AS DATE.
DEFINE VARIABLE start-date   AS DATE.
DEFINE VARIABLE end-date     AS DATE.
DEFINE VARIABLE datum        AS DATE.

DEFINE VARIABLE rline-origcode  AS CHAR INIT "".
DEFINE VARIABLE iftask          AS CHAR INIT "".
DEFINE VARIABLE mesToken        AS CHAR INIT "".
DEFINE VARIABLE mesValue        AS CHAR INIT "".

DEFINE BUFFER allot1 FOR allot-list.
DEFINE BUFFER allot2 FOR allot-list.
DEFINE BUFFER allot3 FOR allot-list.

FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN cat-flag = YES.

FIND FIRST queasy WHERE queasy.KEY = 152 AND queasy.char1 = rmtype NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN i-typ = queasy.number1.
ELSE IF NOT AVAILABLE queasy THEN
DO:
    FIND FIRST zimkateg WHERE zimkateg.kurzbez = rmtype NO-LOCK NO-ERROR.
    IF AVAILABLE zimkateg THEN i-typ = zimkateg.zikatnr.
END.


CREATE allot-list.
ASSIGN
    allot-list.nr = 1
    allot-list.bezeich = "AvailAllRate".

CREATE allot-list.
ASSIGN
    allot-list.nr = 2
    allot-list.bezeich = "AllotByRate".

CREATE allot-list.
ASSIGN
    allot-list.nr = 3
    allot-list.bezeich = "OccByRate".

FIND FIRST allot1 WHERE allot1.nr = 1 NO-LOCK NO-ERROR.
FIND FIRST allot2 WHERE allot2.nr = 2 NO-LOCK NO-ERROR.
FIND FIRST allot3 WHERE allot3.nr = 3 NO-LOCK NO-ERROR.

IF curr-month = 12 THEN tdate = DATE(1,1,curr-year + 1).
ELSE tdate = DATE(curr-month + 1,1,curr-year).

ASSIGN
    fdate = DATE(curr-month,1,curr-year)
    tdate = tdate - 1.

IF cat-flag THEN
DO:
    FOR EACH res-line WHERE res-line.active-flag LE 1 
        AND res-line.resstatus LE 6 AND res-line.resstatus NE 3
        AND res-line.resstatus NE 4 AND res-line.resstatus NE 12
        AND res-line.resstatus NE 11 AND res-line.resstatus NE 13
        AND res-line.kontignr GE 0 AND res-line.l-zuordnung[3] = 0
        AND res-line.ankunft LE tdate AND res-line.abreise GE fdate
        AND res-line.zimmer-wunsch MATCHES ("*$OrigCode$*") NO-LOCK,
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.typ = i-typ NO-LOCK:
    
        do-it = YES. 
        IF res-line.zinr NE "" THEN 
        DO: 
            FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
            do-it = zimmer.sleeping. 
        END. 
        
        IF do-it THEN
        DO:
            IF res-line.ankunft = res-line.abreise THEN end-date = res-line.abreise.
            ELSE end-date = res-line.abreise - 1.
    
            IF res-line.ankunft GE fdate THEN start-date = res-line.ankunft.
            ELSE start-date = fdate.

            IF end-date GE tdate THEN end-date = tdate.
            
            DO datum = start-date TO end-date:
                occAll[DAY(datum)] = occAll[DAY(datum)] + res-line.zimmeranz.
            END.
    
            IF res-line.zimmer-wunsch MATCHES ("*$OrigCode$*") THEN
            DO:
                rline-origcode = "".
                DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                    iftask = ENTRY(i, res-line.zimmer-wunsch, ";").
                    IF SUBSTR(iftask,1,10) = "$OrigCode$" THEN 
                    DO:
                        rline-origcode  = SUBSTR(iftask,11).
                        LEAVE.
                    END.
                END.
    
                IF rline-origcode = currcode THEN
                DO datum = start-date TO end-date:
                    occ[DAY(datum)] = occ[DAY(datum)] + res-line.zimmeranz.
                END.
            END.
        END.
    END.

    FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK,
        FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr 
            AND zimkateg.typ = i-typ AND zimkateg.verfuegbarkeit NO-LOCK BY zimmer.zikatnr: 
        anzahl = anzahl + 1.
    END.

    FOR EACH outorder WHERE outorder.betriebsnr LE 1 AND outorder.gespstart LE tdate
        AND outorder.gespende GE fdate NO-LOCK, 
        FIRST zimmer WHERE zimmer.zinr = outorder.zinr AND zimmer.sleeping = YES NO-LOCK,
        FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr AND zimkateg.typ = i-typ NO-LOCK:
    
        IF outorder.gespstart LE fdate THEN start-date = fdate.
        ELSE start-date = outorder.gespstart.
        IF outorder.gespende GE tdate THEN end-date = tdate.
        ELSE end-date = tdate.
        
        DO datum = start-date TO end-date:
            ooo[DAY(datum)] = ooo[DAY(datum)] + 1.
        END.
    END.
END.
ELSE IF NOT cat-flag THEN
DO:
    FOR EACH res-line WHERE res-line.active-flag LE 1 
        AND res-line.resstatus LE 6 AND res-line.resstatus NE 3
        AND res-line.resstatus NE 4 AND res-line.resstatus NE 12
        AND res-line.resstatus NE 11 AND res-line.resstatus NE 13
        AND res-line.kontignr GE 0 AND res-line.l-zuordnung[3] = 0
        AND res-line.ankunft LE tdate AND res-line.abreise GE fdate
        AND res-line.zikatnr = i-typ NO-LOCK,
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK:
    
        do-it = YES. 
        IF res-line.zinr NE "" THEN 
        DO: 
            FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
            do-it = zimmer.sleeping. 
        END. 
        
        IF do-it THEN
        DO:
            IF res-line.ankunft = res-line.abreise THEN end-date = res-line.abreise.
            ELSE end-date = res-line.abreise - 1.
    
            IF res-line.ankunft GE fdate THEN start-date = res-line.ankunft.
            ELSE start-date = fdate.

            IF end-date GE tdate THEN end-date = tdate.
            
            DO datum = start-date TO end-date:
                occAll[DAY(datum)] = occAll[DAY(datum)] + res-line.zimmeranz.
            END.
    
            IF res-line.zimmer-wunsch MATCHES ("*$OrigCode$*") THEN
            DO:
                rline-origcode = "".
                DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                    iftask = ENTRY(i, res-line.zimmer-wunsch, ";").
                    IF SUBSTR(iftask,1,10) = "$OrigCode$" THEN 
                    DO:
                        rline-origcode  = SUBSTR(iftask,11).
                        LEAVE.
                    END.
                END.
    
                IF rline-origcode = currcode THEN
                DO datum = start-date TO end-date:
                    occ[DAY(datum)] = occ[DAY(datum)] + res-line.zimmeranz.
                END.
                
            END.
        END.
    END.

    FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK,
        FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr AND zimkateg.zikatnr = i-typ 
            AND zimkateg.verfuegbarkeit NO-LOCK: 
        anzahl = anzahl + 1.
    END.

    FOR EACH outorder WHERE outorder.betriebsnr LE 1 AND outorder.gespstart LE tdate
        AND outorder.gespende GE fdate NO-LOCK, 
        FIRST zimmer WHERE zimmer.zinr = outorder.zinr AND zimmer.sleeping = YES NO-LOCK,
        FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr AND zimkateg.zikatnr = i-typ NO-LOCK:
    
        IF outorder.gespstart LE fdate THEN start-date = fdate.
        ELSE start-date = outorder.gespstart.
        IF outorder.gespende GE tdate THEN end-date = tdate.
        ELSE end-date = tdate.
        
        DO datum = start-date TO end-date:
            ooo[DAY(datum)] = ooo[DAY(datum)] + 1.
        END.
    END.
END.


DO datum = fdate TO tdate:
    FIND FIRST queasy  WHERE queasy.KEY = 171 AND queasy.char1 = currcode AND queasy.number1 = i-typ
        AND queasy.date1 = datum NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN allot2.allotment[DAY(datum)] = queasy.number3.
        IF queasy.number2 NE occ[DAY(datum)] THEN
        DO:
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            ASSIGN
                queasy.number2 = occ[DAY(datum)]
                queasy.logi3 = YES.
            FIND CURRENT queasy NO-LOCK.
            RELEASE queasy.
        END.               
    END.
    
    FIND FIRST queasy  WHERE queasy.KEY = 171 AND queasy.char1 = "" AND queasy.number1 = i-typ
        AND queasy.date1 = datum NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        ASSIGN
            queasy.number2 = occAll[DAY(datum)]
            queasy.number3 = ooo[DAY(datum)].
        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
    END.
END.

DO i = 1 TO 31:
    ASSIGN allot1.allotment[i] = anzahl - occAll[i] - ooo[i].
    ASSIGN allot3.allotment[i] = occ[i].
    IF allot2.allotment[i] GT allot1.allotment[i] THEN
        allot2.allotment[i] = allot1.allotment[i].
    
    IF allot1.allotment[i] LT 0 THEN allot1.allotment[i] = 0.
    IF allot2.allotment[i] LT 0 THEN allot2.allotment[i] = 0.
END.







