/*FD Oct 21, 2020 => BL for check temp-table p-list (Web Based)*/

DEFINE TEMP-TABLE p-list LIKE ratecode
    FIELD s-recid           AS INTEGER INIT 0
    FIELD rmcat-str         AS CHAR FORMAT "x(18)"
    FIELD wday-str          AS CHAR FORMAT "x(10)"
    FIELD adult-str         AS CHAR FORMAT "x(10)"
    FIELD child-str         AS CHAR FORMAT "x(10)"
.

DEFINE INPUT PARAMETER pvILanguage      AS INTEGER.
DEFINE INPUT PARAMETER curr-select      AS CHARACTER.
DEFINE INPUT PARAMETER prcode           AS CHARACTER.
DEFINE INPUT PARAMETER market           AS CHARACTER.
DEFINE INPUT PARAMETER prlist-zikatnr   AS INTEGER.
DEFINE INPUT PARAMETER prlist-argtnr    AS INTEGER.
DEFINE INPUT PARAMETER market-nr        AS INTEGER.
DEFINE INPUT PARAMETER tb3-srecid       AS INTEGER.
DEFINE INPUT PARAMETER TABLE FOR p-list.
DEFINE OUTPUT PARAMETER msg-str         AS CHARACTER.
DEFINE OUTPUT PARAMETER child-error     AS LOGICAL.
DEFINE OUTPUT PARAMETER error-msg       AS CHARACTER.

{SupertransBL.i}
DEFINE VARIABLE lvCAREA AS CHAR INITIAL "ratecode-adm-check-plistbl".
DEFINE VARIABLE curr-i AS INTEGER.
DEFINE VARIABLE mesVal AS CHARACTER.
DEFINE VARIABLE error-flag AS LOGICAL.
DEFINE VARIABLE err-result AS CHARACTER.

FIND FIRST p-list NO-ERROR.

IF p-list.startperiode = ? OR p-list.endperiode = ?   
    OR p-list.startperiode GT p-list.endperiode THEN   
DO:    
    msg-str = translateExtended ("Start- and/or End-periode incorrect",lvCAREA,"").      
    RETURN.   
END. 

IF p-list.zipreis = 0 THEN
DO:
    msg-str = translateExtended ("Room Rate not defined",lvCAREA,"").
    RETURN.
END.

IF curr-select = "insert" OR curr-select = "update" THEN RUN proc-checkA.
ELSE IF curr-select = "chg-rate" THEN RUN proc-checkB.

/****************** PROCEDURE *****************/
PROCEDURE proc-checkA:
    DO curr-i = 1 TO NUM-ENTRIES(p-list.wday-str, ","):
        mesVal = TRIM(ENTRY(curr-i, p-list.wday-str, ",")). 
        IF mesVal NE "" THEN
        DO: 
            IF ASC(mesVal) LT 48 OR ASC(mesVal) GT 55 THEN
            DO:
              msg-str = translateExtended ("Wrong weekday format.",lvCAREA,""). 
              RETURN.
            END.
        END.
    END.
    
    DO curr-i = 1 TO NUM-ENTRIES(p-list.adult-str, ","):
        mesVal = TRIM(ENTRY(curr-i, p-list.adult-str, ",")). 
        IF mesVal NE "" THEN
        DO: 
            /*IF ASC(mesVal) LT 48 OR ASC(mesVal) GT 57 OR mesVal MATCHES "*-*" THEN*/
            IF mesval MATCHES "*-*" THEN
            DO:
              msg-str = translateExtended ("Wrong adult format.",lvCAREA,""). 
              RETURN.
            END.
        END.
    END.
    
    DO curr-i = 1 TO NUM-ENTRIES(p-list.child-str, ","):
        mesVal = TRIM(ENTRY(curr-i, p-list.child-str, ",")). 
        IF mesVal NE "" THEN
        DO: 
            IF ASC(mesVal) LT 48 OR ASC(mesVal) GT 57 THEN
            DO:
              msg-str = translateExtended ("Wrong child format.",lvCAREA,""). 
              RETURN.
            END.
        END.
    END.
END PROCEDURE.

PROCEDURE proc-checkB:
    IF p-list.erwachs = 0 AND p-list.kind1 = 0 AND p-list.kind2 = 0 THEN   
    DO:     
      msg-str = translateExtended ("Adult and/or Child must be defined",lvCAREA,"").      
      RETURN.   
    END.
    IF p-list.kind1 NE 0 AND p-list.ch1preis NE 0 THEN  
    DO:   
        msg-str = translateExtended ("Choose ChildNo or Child Price only",lvCAREA,"").  
        RETURN.   
    END.  
    IF p-list.kind2 NE 0 AND p-list.ch2preis NE 0 THEN  
    DO:    
        msg-str = translateExtended ("Choose ChildNo or Child Price only",lvCAREA,"").     
        RETURN.   
    END. 
    RUN check-overlapping (curr-select, p-list.startperiode, p-list.endperiode,  
          p-list.wday, p-list.erwachs, p-list.kind1, p-list.kind2, 
          prcode, market, prlist-zikatnr, prlist-argtnr,p-list.zipreis,
          OUTPUT error-flag, OUTPUT child-error, OUTPUT error-msg).
    IF error-flag THEN
    DO:
        IF child-error THEN 
        DO:
            err-result  = translateExtended (error-msg,lvCAREA,"").
            error-msg   = translateExtended ("Overlapping period found with PARENT Code:",lvCAREA,"")
                        + CHR(10)
                        + translateExtended (err-result,lvCAREA,"").
        END.
        msg-str = translateExtended ("Wrong Start/End- Periode.",lvCAREA,"").
        RETURN.
    END.

END PROCEDURE.

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
DEFINE INPUT PARAMETER zipreis      AS DECIMAL.
DEFINE OUTPUT PARAMETER error-flag  AS LOGICAL NO-UNDO INITIAL NO.   
DEFINE OUTPUT PARAMETER child-error AS LOGICAL NO-UNDO INITIAL NO.   
DEFINE OUTPUT PARAMETER error-msg   AS CHAR    NO-UNDO INIT "".

DEFINE VARIABLE str AS CHARACTER NO-UNDO INIT "".

str = prcode + ";" + STRING(zipreis).
    
    IF curr-mode = "insert" OR curr-mode = "copy-rate" THEN  
    DO:  
        RUN load-ratecode2bl.p(4, market-nr, prcode, argtnr,  
                               zikatnr, adult, child1, child2,   
                               w-day, f-date, t-date, ?,   
                               OUTPUT error-flag, 
                               OUTPUT child-error, OUTPUT error-msg).  
    END.                                          
    ELSE IF curr-mode = "chg-rate" THEN  
    DO:  
        RUN load-ratecode2bl.p(4, market-nr, str, argtnr,  
                               zikatnr, adult, child1, child2, w-day,  
                               f-date, t-date, tb3-srecid,  
                               OUTPUT error-flag, 
                               OUTPUT child-error, OUTPUT error-msg).  
    END.                                          
END. 
