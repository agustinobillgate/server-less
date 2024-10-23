DEFINE TEMP-TABLE om-list2   
    FIELD zinr AS CHAR   
    FIELD userinit AS CHAR FORMAT "x(2)" LABEL "ID"   
    FIELD ind         AS INTEGER INITIAL 0
    FIELD reason      AS CHAR 
    FIELD gespstart   AS DATE 
    FIELD gespende    AS DATE
    .   

DEFINE TEMP-TABLE om-list   
    FIELD zinr        AS CHAR   
    FIELD userinit    AS CHAR FORMAT "x(2)" LABEL "ID"   
    FIELD ind         AS INTEGER INITIAL 0
    FIELD reason      AS CHAR 
    FIELD gespstart   AS DATE 
    FIELD gespende    AS DATE
    FIELD rec-id      AS INTEGER
    .   


DEFINE TEMP-TABLE ooo-list  
    FIELD zinr       LIKE outorder.zinr  
    FIELD gespgrund  LIKE outorder.gespgrund  
    FIELD gespstart  LIKE outorder.gespstart  
    FIELD gespende   LIKE outorder.gespende  
    FIELD userinit   AS CHAR FORMAT "x(2)" LABEL "ID"   
    FIELD etage      LIKE zimmer.etage  
    FIELD ind        AS INTEGER INITIAL 0
    FIELD bezeich    LIKE zimmer.bezeich  
    FIELD betriebsnr LIKE outorder.betriebsnr
    FIELD selected-om AS LOGICAL INITIAL NO
    FIELD rec-id      AS INTEGER
    .  

DEFINE TEMP-TABLE t-ooo-list  
    FIELD zinr       LIKE outorder.zinr  
    FIELD gespgrund  LIKE outorder.gespgrund  
    FIELD gespstart  LIKE outorder.gespstart  
    FIELD gespende   LIKE outorder.gespende  
    FIELD userinit   AS CHAR FORMAT "x(2)" LABEL "ID"  
    FIELD etage      LIKE zimmer.etage  
    FIELD ind        AS INTEGER INITIAL 0 
    FIELD bezeich    LIKE zimmer.bezeich  
    FIELD betriebsnr LIKE outorder.betriebsnr. 


DEFINE INPUT PARAMETER fdate AS DATE.
DEFINE INPUT PARAMETER tdate AS DATE.
DEFINE INPUT PARAMETER disptype AS INT.
DEFINE INPUT PARAMETER sorttype AS INT.
DEFINE OUTPUT PARAMETER ci-date AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR om-list.
DEFINE OUTPUT PARAMETER TABLE FOR ooo-list.

/*
DEFINE VAR fdate AS DATE.
DEFINE VAR tdate AS DATE.
DEFINE VAR disptype AS INT.
DEFINE VAR sorttype AS INT.
DEFINE VAR ci-date AS DATE.
*/

/*
DEFINE BUFFER bediener2 FOR bediener.
FIND FIRST bediener2 NO-LOCK NO-ERROR.
*/

DEFINE VARIABLE user-init AS CHAR.
/* FIND FIRST bediener WHERE bediener.userinit EQ bediener2.userinit NO-LOCK NO-ERROR. */ 
/* Malik Serverless: tanpa where -> WHERE bediener.userinit EQ bediener.userinit */ 
user-init = "".
/*
sorttype 
0: RmNo
1: Department
*/

/*
disptype
1: OOO
2: Off Market
0: All
*/
FOR EACH om-list2:
    DELETE om-list2.
END.
FOR EACH om-list:
    DELETE om-list.
END.

RUN create-om-list-cldbl.p (fdate, tdate, OUTPUT TABLE om-list2).
RUN hk-ooo_1-cldbl.p (INPUT TABLE om-list2, fdate, tdate,disptype, sorttype, user-init, OUTPUT ci-date, OUTPUT TABLE ooo-list).  

FOR EACH om-list2:
    CREATE om-list.
    ASSIGN 
        om-list.zinr       = om-list2.zinr      
        om-list.userinit   = om-list2.userinit  
        om-list.ind        = om-list2.ind       
        om-list.reason     = om-list2.reason    
        om-list.gespstart  = om-list2.gespstart 
        om-list.gespende   = om-list2.gespende. 
END.

FOR EACH om-list:
    FIND FIRST outorder WHERE outorder.zinr EQ om-list.zinr 
        AND outorder.gespstart EQ om-list.gespstart 
        AND outorder.gespende EQ om-list.gespende NO-LOCK NO-ERROR.
    IF AVAILABLE outorder THEN
    DO:
        om-list.rec-id = RECID(outorder).
    END.
END.
