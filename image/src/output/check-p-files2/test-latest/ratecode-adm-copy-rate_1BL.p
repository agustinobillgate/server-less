
DEFINE TEMP-TABLE pr-list 
    FIELD cstr    AS CHAR FORMAT "x(1)" EXTENT 2 INITIAL ["", "*"] 
    FIELD prcode  AS CHAR 
    FIELD rmcat   AS CHAR FORMAT "x(6)" LABEL "RmCat " 
    FIELD argt    AS CHAR FORMAT "x(27)" LABEL "Arrangement" 
    FIELD zikatnr AS INTEGER 
    FIELD argtnr  AS INTEGER 
    FIELD i-typ   AS INTEGER INIT 0
    FIELD flag    AS INTEGER INITIAL 0.  /* 0 = NOT selected */
/*Naufal - Add for bugs copy rate child rate always 0*/
DEFINE TEMP-TABLE child-list
    FIELD child-code AS CHAR
    FIELD true-child AS LOGICAL INIT YES
    FIELD in-percent AS LOGICAL
    FIELD adjust-value AS DECIMAL.
/*end*/

DEF INPUT PARAMETER pvILanguage AS INTEGER      NO-UNDO.
DEF INPUT PARAMETER argtnr1     AS INTEGER      NO-UNDO.
DEF INPUT PARAMETER zikatnr1    AS INTEGER      NO-UNDO.
DEF INPUT PARAMETER market-nr   AS INTEGER      NO-UNDO.
DEF INPUT PARAMETER prcode      AS CHAR         NO-UNDO.
DEF INPUT PARAMETER market      AS CHAR         NO-UNDO.
DEF INPUT PARAMETER user-init   AS CHAR         NO-UNDO.
DEF INPUT PARAMETER adj-value   AS DECIMAL      NO-UNDO.
DEF INPUT PARAMETER adj-type    AS CHAR         NO-UNDO.
DEF INPUT PARAMETER TABLE FOR pr-list.

DEF OUTPUT PARAMETER msg-str    AS CHAR INIT "" NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "ratecode-admin". 

RUN copy-rates.

PROCEDURE copy-rates: 
DEFINE VARIABLE it-is    AS LOGICAL. 
DEFINE BUFFER ratecode1  FOR ratecode. 
DEFINE BUFFER reslin-qsy FOR reslin-queasy.
DEFINE BUFFER child-code FOR ratecode.

    FIND FIRST pr-list.
    /*naufal - create child list*/
    RUN create-child-list.
    /*end*/
    FOR EACH ratecode1 WHERE ratecode1.marknr = market-nr 
        AND ratecode1.code = prcode 
        AND ratecode1.argtnr = argtnr1 AND ratecode1.zikatnr = zikatnr1 
        NO-LOCK BY ratecode1.startperiode: 
        
        RUN check-overlapping ("copy-rate", ratecode1.startperiode, ratecode1.endperiode,
            ratecode1.wday, ratecode1.erwachs, ratecode1.kind1, ratecode1.kind2,
            prcode, market, pr-list.zikatnr, pr-list.argtnr, OUTPUT it-is). 
        
        IF it-is THEN 
        DO: 
            msg-str = translateExtended ("Overlapping found: ",lvCAREA,"") + STRING(ratecode1.startperiode) 
                + " - " + STRING(ratecode1.endperiode). 
            RETURN. 
        END. 
        
        DO TRANSACTION: 
            CREATE ratecode. 
            BUFFER-COPY ratecode1 EXCEPT ratecode1.argtnr ratecode1.zikatnr TO ratecode.
            ASSIGN
                ratecode.argtnr   = pr-list.argtnr 
                ratecode.zikatnr  = pr-list.zikatnr
                ratecode.char1[5] = user-init.
            IF adj-value NE 0 THEN
            DO:
                IF adj-type = "In Amount" THEN
                  ratecode.zipreis  = ratecode.zipreis + adj-value.
                ELSE ratecode.zipreis  = ratecode.zipreis * (1 + adj-value * 0.01).
            END.
            FIND CURRENT ratecode NO-LOCK.
            RELEASE ratecode.
        END.

        FOR EACH child-list NO-LOCK:
            FIND FIRST child-code WHERE child-code.CODE EQ child-list.child-code
                AND child-code.startperiode EQ ratecode1.startperiode  
                AND child-code.endperiode EQ ratecode1.endperiode      
                AND child-code.erwachs EQ ratecode1.erwachs            
                AND child-code.zikatnr EQ pr-list.zikatnr NO-LOCK NO-ERROR.
            IF AVAILABLE child-code THEN
            DO:
                msg-str = translateExtended ("Child overlapping found: ",lvCAREA,"") + STRING(ratecode1.startperiode) 
                + " - " + STRING(ratecode1.endperiode).
            END.
            ELSE
            DO:
                CREATE child-code.
                BUFFER-COPY ratecode1 EXCEPT ratecode1.CODE ratecode1.argtnr ratecode1.zikatnr TO child-code.
                ASSIGN
                    child-code.CODE     = child-list.child-code
                    child-code.argtnr   = pr-list.argtnr 
                    child-code.zikatnr  = pr-list.zikatnr
                    child-code.char1[5] = user-init.
                IF adj-value NE 0 THEN
                DO:
                    IF adj-type = "In Amount" THEN
                    DO:
                        IF child-list.in-percent THEN
                        DO:
                            child-code.zipreis = (child-code.zipreis + adj-value) * (1 + child-list.adjust-value * 0.01).
                        END.
                        ELSE
                        DO:
                            child-code.zipreis  = (child-code.zipreis + adj-value) + child-list.adjust-value.
                        END.    
                    END.
                    ELSE
                    DO:
                        IF child-list.in-percent THEN
                        DO:
                            child-code.zipreis = (child-code.zipreis * (1 + adj-value * 0.01)) * (1 + child-list.adjust-value * 0.01).
                        END.
                        ELSE
                        DO:
                            child-code.zipreis  = (child-code.zipreis * (1 + adj-value * 0.01)) + child-list.adjust-value.
                        END.
                    END.    
                END.
                FIND CURRENT child-code NO-LOCK.
                RELEASE child-code.
            END.
        END.
    END. 
    
    IF argtnr1 NE pr-list.argtnr THEN msg-str = "&W" 
        + translateExtended ("Nocopy of argt-lines for different arrangement",lvCAREA,""). 
    ELSE  
    FOR EACH reslin-qsy WHERE reslin-qsy.key = "argt-line" 
        AND reslin-qsy.number1 = market-nr 
        AND reslin-qsy.number2 = argtnr1 AND reslin-qsy.char1 = prcode 
        AND reslin-qsy.reslinnr = zikatnr1 NO-LOCK 
        BY reslin-qsy.resnr BY reslin-qsy.number3 BY reslin-qsy.date1: 
        CREATE reslin-queasy. 
        ASSIGN
            reslin-queasy.key      = "argt-line"
            reslin-queasy.char1    = prcode
            reslin-queasy.number1  = market-nr 
            reslin-queasy.number2  = pr-list.argtnr 
            reslin-queasy.number3  = reslin-qsy.number3 
            reslin-queasy.resnr    = reslin-qsy.resnr
            reslin-queasy.reslinnr = pr-list.zikatnr 
            reslin-queasy.deci1    = reslin-qsy.deci1 
            reslin-queasy.date1    = reslin-qsy.date1 
            reslin-queasy.date2    = reslin-qsy.date2. 
        FIND CURRENT reslin-queasy NO-LOCK. 
    END. 
END. 

PROCEDURE check-overlapping:
DEFINE INPUT PARAMETER curr-mode    AS CHAR.
DEFINE INPUT PARAMETER f-date       AS DATE. 
DEFINE INPUT PARAMETER t-date       AS DATE. 
DEFINE INPUT PARAMETER w-day        AS INTEGER.
DEFINE INPUT PARAMETER adult        AS INTEGER.
DEFINE INPUT PARAMETER child1       AS INTEGER.
DEFINE INPUT PARAMETER child2       AS INTEGER.
DEFINE INPUT PARAMETER prcode       AS CHAR. 
DEFINE INPUT PARAMETER market       AS CHAR. 
DEFINE INPUT PARAMETER zikatnr      AS INTEGER. 
DEFINE INPUT PARAMETER argtnr       AS INTEGER. 
DEFINE OUTPUT PARAMETER it-is       AS LOGICAL INITIAL NO. 
DEFINE VARIABLE found               AS LOGICAL INITIAL NO. 
DEFINE BUFFER ratecode1             FOR ratecode. 

    IF curr-mode = "add-rate" OR curr-mode = "copy-rate" THEN
        FIND FIRST ratecode1 WHERE ratecode1.marknr = market-nr 
            AND ratecode1.code = prcode 
            AND ratecode1.argtnr = argtnr 
            AND ratecode1.zikatnr = zikatnr 
            AND ratecode1.erwachs = adult
            AND ratecode1.kind1 = child1 
            AND ratecode1.kind2 = child2 
            AND ratecode1.wday  = w-day
            AND NOT ratecode1.startperiod GE t-date
            AND NOT ratecode1.endperiod LE f-date NO-LOCK NO-ERROR. 
    ELSE IF curr-mode = "chg-rate" THEN
        FIND FIRST ratecode1 WHERE ratecode1.marknr = prmarket.nr 
            AND ratecode1.code = prcode 
            AND ratecode1.argtnr = argtnr 
            AND ratecode1.zikatnr = zikatnr 
            AND RECID(ratecode1) NE RECID(ratecode)
            AND ratecode1.erwachs = adult 
            AND ratecode1.kind1 = child1 
            AND ratecode1.kind2 = child2 
            AND ratecode1.wday  = w-day
            AND NOT ratecode1.startperiod GE t-date
            AND NOT ratecode1.endperiod LE f-date NO-LOCK NO-ERROR. 
    it-is = AVAILABLE ratecode1. 
END. 

PROCEDURE create-child-list:
    FOR EACH queasy WHERE queasy.KEY = 2
        AND NOT queasy.logi2
        AND NUM-ENTRIES(queasy.char3, ";") GT 2
        AND ENTRY(2, queasy.char3, ";") = prcode NO-LOCK:
        CREATE child-list.
        ASSIGN 
            child-list.child-code   = queasy.char1
            child-list.in-percent   = SUBSTR(ENTRY(3, queasy.char3, ";"),1,1) = "%"
            child-list.adjust-value = DECIMAL(SUBSTR(ENTRY(3, queasy.char3, ";"),2)) / 100
        .
    END.
END.
