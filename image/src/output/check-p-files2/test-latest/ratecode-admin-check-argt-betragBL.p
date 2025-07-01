DEFINE INPUT PARAMETER roomrate AS DECIMAL.
DEFINE INPUT PARAMETER argt-num AS INTEGER.
DEFINE INPUT PARAMETER tb1char3 AS CHARACTER.
DEFINE INPUT PARAMETER adult AS INTEGER.
DEFINE INPUT PARAMETER adult-str AS CHARACTER.
DEFINE OUTPUT PARAMETER error-msg AS CHARACTER INITIAL "".

DEFINE VARIABLE argt-betrag AS DECIMAL NO-UNDO. 
DEFINE VARIABLE bfast-art   AS INTEGER NO-UNDO. 
DEFINE VARIABLE lunch-art   AS INTEGER NO-UNDO. 
DEFINE VARIABLE dinner-art  AS INTEGER NO-UNDO. 
DEFINE VARIABLE lundin-art  AS INTEGER NO-UNDO.
DEFINE VARIABLE next-step   AS LOGICAL NO-UNDO.
DEFINE VARIABLE segmbez     AS CHARACTER NO-UNDO.
DEFINE VARIABLE loopi       AS INTEGER NO-UNDO.
DEFINE VARIABLE loopqty     AS INTEGER NO-UNDO.

FIND FIRST htparam WHERE paramnr EQ 125 NO-LOCK. 
bfast-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr EQ 227 NO-LOCK. 
lunch-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr EQ 228 NO-LOCK. 
dinner-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr EQ 229 NO-LOCK. 
lundin-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  

IF tb1char3 MATCHES("*;*") THEN segmbez = ENTRY(1, tb1char3, ";").
ELSE segmbez = tb1char3.
/*Escape Segment Compliment and House Use from validation*/
FIND FIRST segment WHERE segment.bezeich EQ segmbez
    AND (segment.betriebsnr EQ 1 OR segment.betriebsnr EQ 2) 
    AND NOT segment.bezeich MATCHES("*$$0*") NO-LOCK NO-ERROR.
IF AVAILABLE segment THEN RETURN.

FIND FIRST arrangement WHERE arrangement.argtnr EQ argt-num NO-LOCK NO-ERROR.
IF NOT AVAILABLE arrangement THEN
DO:
    error-msg = "Arrangement not found.".
    RETURN.
END.

IF adult-str MATCHES "*,*" THEN
DO:
    DO loopi = 1 TO NUM-ENTRIES(adult-str,","):
        loopqty = INT(ENTRY(loopi,adult-str,",")).

        FOR EACH argt-line WHERE argt-line.argtnr EQ arrangement.argtnr 
            AND NOT argt-line.kind2 AND argt-line.kind1,
            FIRST artikel WHERE artikel.artnr EQ argt-line.argt-artnr 
            AND artikel.departement EQ argt-line.departement NO-LOCK:
            
            IF argt-line.betrag GT 0 THEN argt-betrag = argt-line.betrag * loopqty.
            ELSE argt-betrag = roomrate * (- argt-line.betrag / 100) * loopqty.
        
            /*res-deci : [2] = bfast; [3] = lunch; [4] = dinner; [5] = misc*/
            IF artikel.zwkum EQ bfast-art AND (artikel.umsatzart EQ 3 OR artikel.umsatzart GE 5) THEN 
            DO:
                roomrate = roomrate - argt-betrag.  
            END.            
            ELSE IF artikel.zwkum EQ lunch-art AND (artikel.umsatzart EQ 3 OR artikel.umsatzart GE 5) THEN 
            DO:
                roomrate = roomrate - argt-betrag. 
            END.            
            ELSE IF artikel.zwkum EQ dinner-art AND (artikel.umsatzart EQ 3 OR artikel.umsatzart GE 5) THEN 
            DO:
                roomrate = roomrate - argt-betrag. 
            END.            
            ELSE IF artikel.zwkum EQ lundin-art AND (artikel.umsatzart EQ 3 OR artikel.umsatzart GE 5) THEN 
            DO:
                roomrate = roomrate - argt-betrag. 
            END.            
            ELSE 
            DO:
                roomrate = roomrate - argt-betrag. 
            END.                               
        END.

        IF roomrate LT 0 THEN
        DO:
            error-msg = "Breakdown arrangement line and this roomrate is unbalance." 
                + CHR(10) + "Please check again."
                .
            RETURN.
        END.
    END.
END.
ELSE
DO:
    IF adult EQ 0 THEN adult = INT(adult-str).

    FOR EACH argt-line WHERE argt-line.argtnr EQ arrangement.argtnr 
        AND NOT argt-line.kind2 AND argt-line.kind1,
        FIRST artikel WHERE artikel.artnr EQ argt-line.argt-artnr 
        AND artikel.departement EQ argt-line.departement NO-LOCK:
        
        IF argt-line.betrag GT 0 THEN argt-betrag = argt-line.betrag * adult.
        ELSE argt-betrag = roomrate * (- argt-line.betrag / 100) * adult.
    
        /*res-deci : [2] = bfast; [3] = lunch; [4] = dinner; [5] = misc*/
        IF artikel.zwkum EQ bfast-art AND (artikel.umsatzart EQ 3 OR artikel.umsatzart GE 5) THEN 
        DO:
            roomrate = roomrate - argt-betrag.  
        END.            
        ELSE IF artikel.zwkum EQ lunch-art AND (artikel.umsatzart EQ 3 OR artikel.umsatzart GE 5) THEN 
        DO:
            roomrate = roomrate - argt-betrag. 
        END.            
        ELSE IF artikel.zwkum EQ dinner-art AND (artikel.umsatzart EQ 3 OR artikel.umsatzart GE 5) THEN 
        DO:
            roomrate = roomrate - argt-betrag. 
        END.            
        ELSE IF artikel.zwkum EQ lundin-art AND (artikel.umsatzart EQ 3 OR artikel.umsatzart GE 5) THEN 
        DO:
            roomrate = roomrate - argt-betrag. 
        END.            
        ELSE 
        DO:
            roomrate = roomrate - argt-betrag. 
        END.                               
    END.

    IF roomrate LT 0 THEN
    DO:
        error-msg = "Breakdown arrangement line and this roomrate is unbalance." 
            + CHR(10) + "Please check again."
            .
        RETURN.
    END.
END.
