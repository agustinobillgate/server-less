DEFINE TEMP-TABLE output-list
  FIELD departement  AS INTEGER
  FIELD datum        AS DATE        LABEL "Date"
  FIELD zeit         AS CHAR        LABEL "Time"
  FIELD artnr        AS INTEGER                                 
  FIELD artbezeich   AS CHARACTER   FORMAT "x(24)"              
  FIELD bfastqty     AS INTEGER     FORMAT "->>>>>9" INITIAL 0    /*william add >*/  
  FIELD bfastamount  AS DECIMAL     FORMAT "->>,>>>,>>>,>>9.99" 
  FIELD lunchqty     AS INTEGER     FORMAT "->>>>>9" INITIAL 0    /*william add >*/      
  FIELD lunchamount  AS DECIMAL     FORMAT "->>,>>>,>>>,>>9.99" 
  FIELD dinnerqty    AS INTEGER     FORMAT "->>>>>9" INITIAL 0    /*william add >*/    
  FIELD dinneramount AS DECIMAL     FORMAT "->>,>>>,>>>,>>9.99"  
  FIELD supperqty    AS INTEGER     FORMAT "->>>>>9" INITIAL 0    /*william add >*/    
  FIELD supperamount AS DECIMAL     FORMAT "->>,>>>,>>>,>>9.99"  
  FIELD totqty       AS INTEGER     FORMAT "->>>>>9" INITIAL 0    /*william add >*/   
  FIELD totamount    AS DECIMAL     FORMAT "->>,>>>,>>>,>>9.99" 
    .   

DEFINE TEMP-TABLE output-list2
  FIELD departement  AS CHARACTER FORMAT "x(3)"
  FIELD datum        AS CHARACTER FORMAT "x(8)"
  FIELD zeit         AS CHARACTER FORMAT "x(5)"
  FIELD artnr        AS CHARACTER FORMAT "x(9)"  /*william change 8 to 9 830b8e*/                    
  FIELD artbezeich   AS CHARACTER FORMAT "x(24)"              
  FIELD bfastqty     AS CHARACTER FORMAT "x(5)" 
  FIELD bfastamount  AS CHARACTER FORMAT "x(18)"
  FIELD lunchqty     AS CHARACTER FORMAT "x(5)"  
  FIELD lunchamount  AS CHARACTER FORMAT "x(18)"
  FIELD dinnerqty    AS CHARACTER FORMAT "x(5)" 
  FIELD dinneramount AS CHARACTER FORMAT "x(18)"
  FIELD supperqty    AS CHARACTER FORMAT "x(5)" 
  FIELD supperamount AS CHARACTER FORMAT "x(18)"
  FIELD totqty       AS CHARACTER FORMAT "x(5)" 
  FIELD totamount    AS CHARACTER FORMAT "x(18)"
.   

DEF INPUT PARAMETER from-dept AS INT.
DEF INPUT PARAMETER to-dept AS INT.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR output-list2.

DEFINE BUFFER h-art    FOR h-artikel. 
DEFINE BUFFER b-hbline FOR h-bill-line. 

DEFINE VARIABLE curr-dept          AS INTEGER   NO-UNDO.
DEFINE VARIABLE curr-date          AS DATE      NO-UNDO.
DEFINE VARIABLE bfastqty           AS INTEGER   NO-UNDO.
DEFINE VARIABLE billtime           AS CHARACTER NO-UNDO. 
                                   
DEFINE VARIABLE startshift1        AS INTEGER NO-UNDO. 
DEFINE VARIABLE endshift1          AS INTEGER NO-UNDO.
DEFINE VARIABLE startshift2        AS INTEGER NO-UNDO.
DEFINE VARIABLE endshift2          AS INTEGER NO-UNDO.
DEFINE VARIABLE startshift3        AS INTEGER NO-UNDO.
DEFINE VARIABLE endshift3          AS INTEGER NO-UNDO.
DEFINE VARIABLE startshift4        AS INTEGER NO-UNDO.
DEFINE VARIABLE endshift4          AS INTEGER NO-UNDO.
                                   
DEFINE VARIABLE depbfastqty        AS INTEGER INIT 0 NO-UNDO.  
DEFINE VARIABLE depbfastamount     AS DECIMAL INIT 0 NO-UNDO.  
DEFINE VARIABLE deplunchqty        AS INTEGER INIT 0 NO-UNDO.  
DEFINE VARIABLE deplunchamount     AS DECIMAL INIT 0 NO-UNDO.  
DEFINE VARIABLE depdinnerqty       AS INTEGER INIT 0 NO-UNDO.  
DEFINE VARIABLE depdinneramount    AS DECIMAL INIT 0 NO-UNDO.  
DEFINE VARIABLE depsupperqty       AS INTEGER INIT 0 NO-UNDO.  
DEFINE VARIABLE depsupperamount    AS DECIMAL INIT 0 NO-UNDO.  
DEFINE VARIABLE deptotqty          AS INTEGER INIT 0 NO-UNDO.   
DEFINE VARIABLE deptotamount       AS DECIMAL INIT 0 NO-UNDO.   

DEFINE VARIABLE totbfastqty        AS INTEGER INIT 0 NO-UNDO.  
DEFINE VARIABLE totbfastamount     AS DECIMAL INIT 0 NO-UNDO.  
DEFINE VARIABLE totlunchqty        AS INTEGER INIT 0 NO-UNDO.  
DEFINE VARIABLE totlunchamount     AS DECIMAL INIT 0 NO-UNDO.  
DEFINE VARIABLE totdinnerqty       AS INTEGER INIT 0 NO-UNDO.  
DEFINE VARIABLE totdinneramount    AS DECIMAL INIT 0 NO-UNDO.  
DEFINE VARIABLE totsupperqty       AS INTEGER INIT 0 NO-UNDO.  
DEFINE VARIABLE totsupperamount    AS DECIMAL INIT 0 NO-UNDO.  
DEFINE VARIABLE sumtotqty          AS INTEGER INIT 0 NO-UNDO.   
DEFINE VARIABLE sumtotamount       AS DECIMAL INIT 0 NO-UNDO.   

DEFINE VARIABLE sumtotbfastqty     AS INTEGER INIT 0 NO-UNDO.  
DEFINE VARIABLE sumtotbfastamount  AS DECIMAL INIT 0 NO-UNDO.  
DEFINE VARIABLE sumtotlunchqty     AS INTEGER INIT 0 NO-UNDO.  
DEFINE VARIABLE sumtotlunchamount  AS DECIMAL INIT 0 NO-UNDO.  
DEFINE VARIABLE sumtotdinnerqty    AS INTEGER INIT 0 NO-UNDO.  
DEFINE VARIABLE sumtotdinneramount AS DECIMAL INIT 0 NO-UNDO.  
DEFINE VARIABLE sumtotsupperqty    AS INTEGER INIT 0 NO-UNDO.  
DEFINE VARIABLE sumtotsupperamount AS DECIMAL INIT 0 NO-UNDO.  
DEFINE VARIABLE totsumtotqty       AS INTEGER INIT 0 NO-UNDO.   
DEFINE VARIABLE totsumtotamount    AS DECIMAL INIT 0 NO-UNDO.

FOR EACH output-list: 
    DELETE output-list. 
END. 

FOR EACH queasy WHERE key = 5 AND queasy.number3 NE 0 NO-LOCK BY queasy.number1:
    IF queasy.number3 = 1 THEN
    DO:
        ASSIGN 
            startshift1 = queasy.number1
            endshift1   = queasy.number2.
    END.
    IF queasy.number3 = 2 THEN
    DO:
        ASSIGN 
            startshift2 = queasy.number1
            endshift2   = queasy.number2.
    END.
    IF queasy.number3 = 3 THEN
    DO:
        ASSIGN 
            startshift3 = queasy.number1
            endshift3   = queasy.number2.
    END.
    IF queasy.number3 = 4 THEN
    DO:
        ASSIGN 
            startshift4 = queasy.number1
            endshift4   = queasy.number2.
    END.
END.

FOR EACH h-bill-line WHERE h-bill-line.bill-datum GE from-date 
    AND h-bill-line.bill-datum LE to-date
    AND h-bill-line.departement GE from-dept
    AND h-bill-line.departement LE to-dept BY h-bill-line.departement BY h-bill-line.bill-datum:
    IF curr-dept NE h-bill-line.departement THEN
    DO:
        IF curr-dept NE 0 THEN
        DO:
            CREATE output-list.
            ASSIGN
                output-list.artbezeich   = "TOTAL"
                output-list.bfastqty     = depbfastqty       
                output-list.bfastamount  = depbfastamount    
                output-list.lunchqty     = deplunchqty       
                output-list.lunchamount  = deplunchamount    
                output-list.dinnerqty    = depdinnerqty      
                output-list.dinneramount = depdinneramount   
                output-list.supperqty    = depsupperqty      
                output-list.supperamount = depsupperamount   
                output-list.totqty       = deptotqty         
                output-list.totamount    = deptotamount.
            CREATE output-list.     
        END.                    

        ASSIGN curr-dept = h-bill-line.departement.
        FIND FIRST hoteldpt WHERE hoteldpt.num EQ curr-dept NO-LOCK NO-ERROR.
        IF AVAILABLE hoteldpt THEN
        DO:    
            CREATE output-list.
            ASSIGN 
                output-list.artbezeich = STRING(hoteldpt.num,"99 ") + STRING(hoteldpt.depart,"x(21)").            
        END.
    END.

    IF curr-date NE h-bill-line.bill-datum THEN
    DO:
        ASSIGN curr-date = h-bill-line.bill-datum.
        FOR EACH b-hbline WHERE b-hbline.departement EQ curr-dept AND b-hbline.bill-datum EQ curr-date NO-LOCK:
            FIND FIRST h-artikel WHERE h-artikel.departement EQ curr-dept 
                AND h-artikel.artnr EQ b-hbline.artnr AND h-artikel.artart = 0 NO-LOCK NO-ERROR.
            IF AVAILABLE h-artikel THEN
            DO:
                CREATE output-list.
                ASSIGN 
                    output-list.departement = curr-dept
                    output-list.datum       = b-hbline.bill-datum
                    output-list.zeit        = string(b-hbline.zeit,"hh:mm")
                    output-list.artnr       = b-hbline.artnr
                    output-list.artbezeich  = h-artikel.bezeich.
         
                billtime = STRING(b-hbline.zeit,"HH:MM").
                billtime = ENTRY(1,billtime,":") + ENTRY(2,billtime,":").
        
                IF INT(billtime) GE startshift1 AND INT(billtime) LT endshift1 THEN
                DO:
                    ASSIGN 
                        output-list.bfastqty    = b-hbline.anzahl
                        output-list.bfastamount = b-hbline.betrag.
                END.
                IF INT(billtime) GE startshift2 AND INT(billtime) LT endshift2 THEN
                DO:
                    ASSIGN 
                        output-list.lunchqty    = b-hbline.anzahl
                        output-list.lunchamount = b-hbline.betrag.
                END.
                IF INT(billtime) GE startshift3 AND INT(billtime) LT endshift3 THEN
                DO:
                    ASSIGN 
                        output-list.dinnerqty    = b-hbline.anzahl
                        output-list.dinneramount = b-hbline.betrag.
                END.
                IF INT(billtime) GE startshift4 AND INT(billtime) LT endshift4 THEN
                DO:
                    ASSIGN 
                        output-list.supperqty    = b-hbline.anzahl
                        output-list.supperamount = b-hbline.betrag.
                END.
                ASSIGN output-list.totqty    = output-list.bfastqty + output-list.lunchqty + output-list.dinnerqty + output-list.supperqty
                       output-list.totamount = output-list.bfastamount + output-list.lunchamount + output-list.dinneramount + output-list.supperamount.
        
                ASSIGN
                    totbfastqty     = totbfastqty     + output-list.bfastqty     
                    totbfastamount  = totbfastamount  + output-list.bfastamount  
                    totlunchqty     = totlunchqty     + output-list.lunchqty     
                    totlunchamount  = totlunchamount  + output-list.lunchamount  
                    totdinnerqty    = totdinnerqty    + output-list.dinnerqty    
                    totdinneramount = totdinneramount + output-list.dinneramount 
                    totsupperqty    = totsupperqty    + output-list.supperqty    
                    totsupperamount = totsupperamount + output-list.supperamount 
                    sumtotqty       = sumtotqty       + output-list.totqty       
                    sumtotamount    = sumtotamount    + output-list.totamount.   
            END.
        END.
        CREATE output-list.
        ASSIGN
            output-list.artbezeich   = "SUB TOTAL"
            output-list.bfastqty     = totbfastqty         
            output-list.bfastamount  = totbfastamount      
            output-list.lunchqty     = totlunchqty         
            output-list.lunchamount  = totlunchamount      
            output-list.dinnerqty    = totdinnerqty        
            output-list.dinneramount = totdinneramount     
            output-list.supperqty    = totsupperqty        
            output-list.supperamount = totsupperamount     
            output-list.totqty       = sumtotqty           
            output-list.totamount    = sumtotamount .        
        CREATE output-list.
        ASSIGN
            totbfastqty     = 0    
            totbfastamount  = 0   
            totlunchqty     = 0   
            totlunchamount  = 0   
            totdinnerqty    = 0   
            totdinneramount = 0   
            totsupperqty    = 0  
            totsupperamount = 0  
            sumtotqty       = 0  
            sumtotamount    = 0. 
    END.
    
    ASSIGN              
        depbfastqty     = 0    
        depbfastamount  = 0   
        deplunchqty     = 0   
        deplunchamount  = 0   
        depdinnerqty    = 0   
        depdinneramount = 0   
        depsupperqty    = 0  
        depsupperamount = 0  
        deptotqty       = 0  
        deptotamount    = 0. 
    FOR EACH output-list WHERE output-list.departement EQ curr-dept:
        ASSIGN

            depbfastqty       = depbfastqty     + output-list.bfastqty     
            depbfastamount    = depbfastamount  + output-list.bfastamount  
            deplunchqty       = deplunchqty     + output-list.lunchqty     
            deplunchamount    = deplunchamount  + output-list.lunchamount  
            depdinnerqty      = depdinnerqty    + output-list.dinnerqty    
            depdinneramount   = depdinneramount + output-list.dinneramount 
            depsupperqty      = depsupperqty    + output-list.supperqty    
            depsupperamount   = depsupperamount + output-list.supperamount 
            deptotqty         = deptotqty       + output-list.totqty       
            deptotamount      = deptotamount    + output-list.totamount.   
    END.
END.

CREATE output-list.
ASSIGN
    output-list.artbezeich   = "TOTAL"
    output-list.bfastqty     = depbfastqty       
    output-list.bfastamount  = depbfastamount    
    output-list.lunchqty     = deplunchqty       
    output-list.lunchamount  = deplunchamount    
    output-list.dinnerqty    = depdinnerqty      
    output-list.dinneramount = depdinneramount   
    output-list.supperqty    = depsupperqty      
    output-list.supperamount = depsupperamount   
    output-list.totqty       = deptotqty         
    output-list.totamount    = deptotamount.
CREATE output-list.     

sumtotbfastqty     = 0.      
sumtotbfastamount  = 0.      
sumtotlunchqty     = 0.      
sumtotlunchamount  = 0.      
sumtotdinnerqty    = 0.      
sumtotdinneramount = 0.      
sumtotsupperqty    = 0.      
sumtotsupperamount = 0.      
totsumtotqty       = 0.      
totsumtotamount    = 0.

FOR EACH output-list WHERE output-list.artbezeich EQ "TOTAL" :
    ASSIGN 
        sumtotbfastqty     = sumtotbfastqty     + output-list.bfastqty         
        sumtotbfastamount  = sumtotbfastamount  + output-list.bfastamount      
        sumtotlunchqty     = sumtotlunchqty     + output-list.lunchqty         
        sumtotlunchamount  = sumtotlunchamount  + output-list.lunchamount      
        sumtotdinnerqty    = sumtotdinnerqty    + output-list.dinnerqty        
        sumtotdinneramount = sumtotdinneramount + output-list.dinneramount     
        sumtotsupperqty    = sumtotsupperqty    + output-list.supperqty        
        sumtotsupperamount = sumtotsupperamount + output-list.supperamount     
        totsumtotqty       = totsumtotqty       + output-list.totqty           
        totsumtotamount    = totsumtotamount    + output-list.totamount.       
END.

CREATE output-list.
ASSIGN
    output-list.artbezeich   = "G R A N D  T O T A L"
    output-list.bfastqty     = sumtotbfastqty    
    output-list.bfastamount  = sumtotbfastamount 
    output-list.lunchqty     = sumtotlunchqty    
    output-list.lunchamount  = sumtotlunchamount 
    output-list.dinnerqty    = sumtotdinnerqty   
    output-list.dinneramount = sumtotdinneramount
    output-list.supperqty    = sumtotsupperqty   
    output-list.supperamount = sumtotsupperamount
    output-list.totqty       = totsumtotqty      
    output-list.totamount    = totsumtotamount .  

    
FOR EACH output-list:
    CREATE output-list2.
    IF TRIM(SUBSTRING(output-list.artbezeich,1,1)) = "0" THEN
    ASSIGN                                                              
        output-list2.departement  = ""
        output-list2.datum        = ""  
        output-list2.zeit         = ""  
        output-list2.artnr        = ""  
        output-list2.artbezeich   = STRING(output-list.artbezeich)                          
        output-list2.bfastqty     = ""
        output-list2.bfastamount  = ""
        output-list2.lunchqty     = ""
        output-list2.lunchamount  = ""
        output-list2.dinnerqty    = ""
        output-list2.dinneramount = ""
        output-list2.supperqty    = ""
        output-list2.supperamount = ""
        output-list2.totqty       = ""
        output-list2.totamount    = "".

    ELSE IF output-list.departement = 0 AND output-list.artbezeich NE "" THEN
        ASSIGN 
            output-list2.departement  = ""
            output-list2.datum        = ""      
            output-list2.zeit         = ""        
            output-list2.artnr        = ""       
            output-list2.artbezeich   = STRING(output-list.artbezeich)                          
            output-list2.bfastqty     = STRING(output-list.bfastqty, "->>>>>9")    /*william add >*/                 
            output-list2.bfastamount  = STRING(output-list.bfastamount, "->>,>>>,>>>,>>9.99" )  
            output-list2.lunchqty     = STRING(output-list.lunchqty, "->>>>>9")    /*william add >*/               
            output-list2.lunchamount  = STRING(output-list.lunchamount, "->>,>>>,>>>,>>9.99" )  
            output-list2.dinnerqty    = STRING(output-list.dinnerqty, "->>>>>9")   /*william add >*/              
            output-list2.dinneramount = STRING(output-list.dinneramount, "->>,>>>,>>>,>>9.99" ) 
            output-list2.supperqty    = STRING(output-list.supperqty, "->>>>>9")   /*william add >*/               
            output-list2.supperamount = STRING(output-list.supperamount, "->>,>>>,>>>,>>9.99" ) 
            output-list2.totqty       = STRING(output-list.totqty, "->>>>>9")      /*william add >*/                 
            output-list2.totamount    = STRING(output-list.totamount, "->>,>>>,>>>,>>9.99" ).    
    ELSE IF output-list.departement = 0 AND output-list.artbezeich EQ "" THEN
        ASSIGN 
            output-list2.departement  = ""
            output-list2.datum        = ""      
            output-list2.zeit         = ""        
            output-list2.artnr        = ""       
            output-list2.artbezeich   = ""  
            output-list2.bfastqty     = ""  
            output-list2.bfastamount  = ""  
            output-list2.lunchqty     = ""  
            output-list2.lunchamount  = ""  
            output-list2.dinnerqty    = ""  
            output-list2.dinneramount = ""  
            output-list2.supperqty    = ""  
            output-list2.supperamount = ""  
            output-list2.totqty       = ""  
            output-list2.totamount    = "".
    ELSE
    ASSIGN                               
        output-list2.departement  = STRING(output-list.departement)
        output-list2.datum        = STRING(output-list.datum)        
        output-list2.zeit         = STRING(output-list.zeit)         
        output-list2.artnr        = STRING(output-list.artnr, ">>>>>>>>>9")  /*william change 5 to 9 830b8e*/      
        output-list2.artbezeich   = STRING(output-list.artbezeich)                          
        output-list2.bfastqty     = STRING(output-list.bfastqty, "->>>>>9")  /*william add >*/                 
        output-list2.bfastamount  = STRING(output-list.bfastamount, "->>,>>>,>>>,>>9.99" )  
        output-list2.lunchqty     = STRING(output-list.lunchqty, "->>>>>9")  /*william add >*/                 
        output-list2.lunchamount  = STRING(output-list.lunchamount, "->>,>>>,>>>,>>9.99" )  
        output-list2.dinnerqty    = STRING(output-list.dinnerqty, "->>>>>9") /*william add >*/                 
        output-list2.dinneramount = STRING(output-list.dinneramount, "->>,>>>,>>>,>>9.99" ) 
        output-list2.supperqty    = STRING(output-list.supperqty, "->>>>>9") /*william add >*/                 
        output-list2.supperamount = STRING(output-list.supperamount, "->>,>>>,>>>,>>9.99" ) 
        output-list2.totqty       = STRING(output-list.totqty, "->>>>>9")    /*william add >*/                
        output-list2.totamount    = STRING(output-list.totamount, "->>,>>>,>>>,>>9.99" ).   
END.

