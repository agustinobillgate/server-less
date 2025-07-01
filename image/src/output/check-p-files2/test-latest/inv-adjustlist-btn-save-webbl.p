DEFINE TEMP-TABLE c-list 
  FIELD artnr       LIKE l-artikel.artnr 
  FIELD bezeich     AS CHAR FORMAT "x(36)" COLUMN-LABEL "Description" 
  FIELD munit       AS CHAR FORMAT "x(3)" COLUMN-LABEL "Unit" 
  FIELD inhalt      AS DECIMAL FORMAT ">>>9.99" COLUMN-LABEL "Content" 
  FIELD zwkum       AS INTEGER 
  FIELD endkum      AS INTEGER 
  FIELD qty         AS DECIMAL  FORMAT "->>>,>>9.999" LABEL "   Curr-Qty" 
  FIELD qty1        AS DECIMAL FORMAT "->>>,>>9.999" LABEL " Actual-Qty" 
  FIELD amount      AS DECIMAL  FORMAT "->>,>>>,>>>,>>9.99" LABEL " Amount"
  FIELD avrg-amount AS DECIMAL  FORMAT "->>,>>>,>>>,>>9.99" LABEL "Average Amount"
  FIELD fibukonto   AS CHAR INITIAL "0000000000" 
/* DO NOT change the INITIAL value 0000000000, used BY hcost-anal.p */ 
  FIELD cost-center AS CHAR FORMAT "x(50)" LABEL "Cost Allocation"
  FIELD variance    AS DECIMAL  FORMAT "->>>,>>9.999" LABEL "Variance Qty"
  FIELD lscheinnr   AS CHAR 
  FIELD id          AS CHAR
  FIELD change-id   AS CHAR
  FIELD chage-date  AS CHAR
.
                                                                                    
DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT-OUTPUT PARAMETER TABLE FOR c-list.
DEF OUTPUT PARAMETER err-code AS INT INITIAL 0.


DEFINE VARIABLE gl-notfound AS LOGICAL.

/*
FOR EACH c-list WHERE c-list.fibukonto NE "" 
    AND c-list.fibukonto NE ? :
        IF TRIM(c-list.fibukonto)    EQ "0" 
           OR TRIM(c-list.fibukonto) EQ "00" 
           OR TRIM(c-list.fibukonto) EQ "000"
           OR TRIM(c-list.fibukonto) EQ "0000" 
           OR TRIM(c-list.fibukonto) EQ "00000" 
           OR TRIM(c-list.fibukonto) EQ "000000" 
           OR TRIM(c-list.fibukonto) EQ "0000000" 
           OR TRIM(c-list.fibukonto) EQ "00000000" 
           OR TRIM(c-list.fibukonto) EQ "000000000" 
           OR TRIM(c-list.fibukonto) EQ "0000000000"
           OR TRIM(c-list.fibukonto) EQ "00000000000" 
           OR TRIM(c-list.fibukonto) EQ "000000000000"   
           OR TRIM(c-list.fibukonto) EQ "0000000000000"          
           THEN DO:
            gl-notfound = NO. 
           END.
        ELSE DO:
            FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ c-list.fibukonto NO-LOCK NO-ERROR.
            IF NOT AVAILABLE gl-acct THEN
            DO:
                gl-notfound = YES.
                LEAVE.
            END.
            ELSE DO:
                gl-notfound = NO.
            END.
        END.
END.
IF gl-notfound THEN 
DO:
    err-code = 1.
    RETURN.
END.
*/

FOR EACH c-list NO-LOCK:    
    FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr EQ c-list.lscheinnr 
     AND l-ophdr.docu-nr EQ c-list.lscheinnr
     AND l-ophdr.op-typ = "STT" 
     AND (TRIM(l-ophdr.fibukonto)    EQ "0" 
           OR TRIM(l-ophdr.fibukonto) EQ "00" 
           OR TRIM(l-ophdr.fibukonto) EQ "000"
           OR TRIM(l-ophdr.fibukonto) EQ "0000" 
           OR TRIM(l-ophdr.fibukonto) EQ "00000" 
           OR TRIM(l-ophdr.fibukonto) EQ "000000" 
           OR TRIM(l-ophdr.fibukonto) EQ "0000000" 
           OR TRIM(l-ophdr.fibukonto) EQ "00000000" 
           OR TRIM(l-ophdr.fibukonto) EQ "000000000" 
           OR TRIM(l-ophdr.fibukonto) EQ "0000000000"
           OR TRIM(l-ophdr.fibukonto) EQ "00000000000" 
           OR TRIM(l-ophdr.fibukonto) EQ "000000000000"   
           OR TRIM(l-ophdr.fibukonto) EQ "0000000000000")
        EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE l-ophdr THEN DO:
        ASSIGN  
            l-ophdr.fibukonto  = c-list.fibukonto.

        FIND CURRENT l-ophdr NO-LOCK.
        RELEASE l-ophdr.
    END.

    FIND FIRST l-op WHERE l-op.lscheinnr EQ c-list.lscheinnr
     AND l-op.artnr EQ c-list.artnr
     AND INT(l-op.stornogrund) = 0 EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE l-op THEN DO:
        FIND FIRST queasy WHERE queasy.KEY = 334
         AND queasy.char1   = l-op.lscheinnr 
         AND queasy.char2   = user-init
         AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN DO:
         CREATE queasy.
         ASSIGN
             queasy.KEY     = 334
             queasy.char1   = l-op.lscheinnr
             queasy.char2   = user-init
             queasy.char3   = "Adjusment Result"
             queasy.number1 = l-op.artnr
             queasy.date2   = TODAY
             .
        END.
        
        ASSIGN  
            l-op.stornogrund  = c-list.fibukonto.

        FIND CURRENT l-op NO-LOCK.
        RELEASE l-op.
    END.
END.
