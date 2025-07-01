/*FD Oct 27, 2020 => For display table Dynamic Contract Rate Code VHP WEB BASED*/

DEFINE TEMP-TABLE t-ratecode1   LIKE ratecode
    FIELD s-recid               AS INTEGER INIT 0.

DEFINE TEMP-TABLE dynaRate-list  
    FIELD s-recid AS INTEGER  
    FIELD counter AS INTEGER  
    FIELD w-day   AS INTEGER FORMAT "9"     LABEL "DW" INIT 0 /* week day 0=ALL, 1=Mon..7=Sun */  
    FIELD rmType  AS CHAR    FORMAT "x(10)" LABEL "Room Type"  
    FIELD fr-room AS INTEGER FORMAT ">,>>9" LABEL "FrRoom"   
    FIELD to-room AS INTEGER FORMAT ">,>>9" LABEL "ToRoom"   
    FIELD days1   AS INTEGER FORMAT ">>9"   LABEL ">Days2CI"  
    FIELD days2   AS INTEGER FORMAT ">>9"   LABEL "<Days2CI"  
    FIELD rCode   AS CHAR    FORMAT "x(18)" LABEL "RateCode".
/**/
DEFINE INPUT PARAMETER prcode1      AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR dynaRate-list.

DEFINE VARIABLE tokcounter          AS INTEGER NO-UNDO.  
DEFINE VARIABLE ifTask              AS CHAR    NO-UNDO.  
DEFINE VARIABLE mesToken            AS CHAR    NO-UNDO.  
DEFINE VARIABLE mesValue            AS CHAR    NO-UNDO.  
DEFINE VARIABLE curr-counter        AS INT.

RUN load-ratecode1bl.p(2, ?, prcode1, ?, ?, ?, ?, ?, ?, ?, ?, ?, OUTPUT TABLE t-ratecode1).
FOR EACH t-ratecode1 NO-LOCK:  
    CREATE dynaRate-list.  
    ASSIGN dynaRate-list.s-recid = t-ratecode1.s-recid.  
    ifTask = t-ratecode1.char1[5].  
    DO tokcounter = 1 TO NUM-ENTRIES(ifTask, ";") - 1:  
        mesToken = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 1, 2).  
        mesValue = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 3).  
        CASE mesToken:  
            WHEN "CN" THEN dynaRate-list.counter = INTEGER(mesValue).  
            WHEN "RT" THEN dynaRate-list.rmType  = mesValue.  
            WHEN "WD" THEN dynaRate-list.w-day   = INTEGER(mesValue).  
            WHEN "FR" THEN dynaRate-list.fr-room = INTEGER(mesValue).  
            WHEN "TR" THEN dynaRate-list.to-room = INTEGER(mesValue).  
            WHEN "D1" THEN dynaRate-list.days1   = INTEGER(mesValue).  
            WHEN "D2" THEN dynaRate-list.days2   = INTEGER(mesValue).  
            WHEN "RC" THEN dynaRate-list.rCode   = mesValue.  
        END CASE.  
    END.  
    IF dynaRate-list.counter = 0 THEN   
    DO:   
        RUN ratecode-admin-fill-dynarate-counterbl.p  
            (t-ratecode1.code, dynaRate-list.rmType, dynaRate-list.rCode,
             dynarate-list.w-day,OUTPUT curr-counter).  
        ASSIGN dynaRate-list.counter = curr-counter.  
    END.  
END.


