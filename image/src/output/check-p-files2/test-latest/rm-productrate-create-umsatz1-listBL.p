
DEFINE TEMP-TABLE to-list 
    FIELD gastnr     AS INTEGER 
    FIELD name       AS CHAR FORMAT "x(24)" 
    
    FIELD room       AS INTEGER FORMAT "->>,>>9" INITIAL 0 
    FIELD c-room     AS INTEGER                  INITIAL 0
    FIELD pax        AS INTEGER FORMAT "->>,>>9" INITIAL 0 
    FIELD logis      AS DECIMAL FORMAT /*">>>,>>>,>>9"*/ "->>,>>>,>>>,>>9" INITIAL 0 
    FIELD proz       AS DECIMAL FORMAT "->>9.99" INITIAL 0 
    FIELD avrgrate   AS DECIMAL FORMAT /*">,>>>,>>9"*/ "->,>>>,>>>,>>9" INITIAL 0 
    FIELD ratecode   AS CHAR    FORMAT "x(15)"
    /*FIELD ratename   AS CHAR    FORMAT "x(15)"*/
    
    FIELD m-room     AS INTEGER FORMAT "->>,>>9" INITIAL 0 
    FIELD mc-room    AS INTEGER                  INITIAL 0
    FIELD m-pax      AS INTEGER FORMAT "->>,>>9" INITIAL 0 
    FIELD m-logis    AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0 
    FIELD m-proz     AS DECIMAL FORMAT "->>9.99" INITIAL 0 
    FIELD m-avrgrate AS DECIMAL FORMAT /*">,>>>,>>9"*/ "->,>>>,>>>,>>9" INITIAL 0 
    
    FIELD y-room     AS INTEGER FORMAT "->>>,>>9" INITIAL 0 
    FIELD yc-room    AS INTEGER                   INITIAL 0
    FIELD y-pax      AS INTEGER FORMAT "->>>,>>9" INITIAL 0 
    FIELD y-logis    AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0 
    FIELD y-proz     AS DECIMAL FORMAT "->>9.99" INITIAL 0 
    FIELD y-avrgrate AS DECIMAL FORMAT /*">,>>>,>>9"*/ "->,>>>,>>>,>>9" INITIAL 0.

DEFINE TEMP-TABLE output-list2 
  FIELD flag AS INTEGER 
  FIELD name AS CHAR 
  FIELD rmnite1 AS INTEGER  /*MTD*/ 
  FIELD rmrev1 AS DECIMAL 
  FIELD rmnite AS INTEGER   /*YTD*/ 
  FIELD rmrev AS DECIMAL 
  FIELD str2 AS CHAR
  FIELD rate AS CHAR.
  /*FIELD ratenm AS CHAR.*/
/*
DEFINE TEMP-TABLE out-list
    FIELD name        AS CHAR 
    FIELD rate        AS CHAR
    FIELD room        AS INTEGER FORMAT "->>,>>9" INITIAL 0
    FIELD pax         AS INTEGER FORMAT "->>,>>9" INITIAL 0                          
    FIELD logis       AS DECIMAL FORMAT /*">>>,>>>,>>9"*/ "->>,>>>,>>>,>>9" INITIAL 0
    FIELD proz        AS DECIMAL FORMAT "->>9.99" INITIAL 0                                        
    FIELD avrgrate    AS DECIMAL FORMAT /*">,>>>,>>9"*/ "->,>>>,>>>,>>9" INITIAL 0   
    FIELD m-room      AS INTEGER FORMAT "->>,>>9" INITIAL 0 
    FIELD m-pax       AS INTEGER FORMAT "->>,>>9" INITIAL 0                       
    FIELD m-logis     AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0                           
    FIELD m-proz      AS DECIMAL FORMAT "->>9.99" INITIAL 0                                   
    FIELD m-avrgrate  AS DECIMAL FORMAT /*">,>>>,>>9"*/ "->,>>>,>>>,>>9" INITIAL 0
    FIELD y-room      AS INTEGER FORMAT "->>>,>>9" INITIAL 0
    FIELD y-pax       AS INTEGER FORMAT "->>>,>>9" INITIAL 0                      
    FIELD y-logis     AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0                         
    FIELD y-proz      AS DECIMAL FORMAT "->>9.99" INITIAL 0                                    
    FIELD y-avrgrate  AS DECIMAL FORMAT /*">,>>>,>>9"*/ "->,>>>,>>>,>>9" INITIAL 0
    .
*/

DEFINE TEMP-TABLE out-list
    FIELD name        AS CHAR FORMAT "x(24)"
    FIELD rate        AS CHAR FORMAT "x(15)"
    FIELD room        AS CHAR FORMAT "x(7)" 
    FIELD pax         AS CHAR FORMAT "x(7)" 
    FIELD logis       AS CHAR FORMAT "x(15)"
    FIELD proz        AS CHAR FORMAT "x(7)"             
    FIELD avrgrate    AS CHAR FORMAT "x(14)"
    FIELD m-room      AS CHAR FORMAT "x(7)" 
    FIELD m-pax       AS CHAR FORMAT "x(7)" 
    FIELD m-logis     AS CHAR FORMAT "x(15)"       
    FIELD m-proz      AS CHAR FORMAT "x(7)"        
    FIELD m-avrgrate  AS CHAR FORMAT "x(14)"
    FIELD y-room      AS CHAR FORMAT "x(8)" 
    FIELD y-pax       AS CHAR FORMAT "x(8)" 
    FIELD y-logis     AS CHAR FORMAT "x(18)"        
    FIELD y-proz      AS CHAR FORMAT "x(7)"         
    FIELD y-avrgrate  AS CHAR FORMAT "x(14)"
    .

DEF INPUT PARAMETER disptype    AS INT.
DEF INPUT PARAMETER mi-ftd      AS LOGICAL.
DEF INPUT PARAMETER f-date      AS DATE.
DEF INPUT PARAMETER t-date      AS DATE.
DEF INPUT PARAMETER to-date     AS DATE.
DEF INPUT PARAMETER cardtype    AS INT.
DEF INPUT PARAMETER incl-comp   AS LOGICAL.
DEF INPUT PARAMETER sales-ID    AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR out-list.

RUN rm-productrate-create-umsatz1bl.p 
    (disptype, mi-ftd, f-date,t-date, to-date, cardtype, incl-comp, sales-ID,
     OUTPUT TABLE output-list2, OUTPUT TABLE to-list).

FOR EACH out-list.
    DELETE out-list. 
END.

FOR EACH output-list2:    
    CREATE out-list.
    ASSIGN
        out-list.rate       = SUBSTR(output-list2.str2, 180,15)
        out-list.NAME       = SUBSTR(output-list2.str2, 1, 24) 
        out-list.room       = /*INTEGER*/ SUBSTR(output-list2.str2, 25, 7) 
        out-list.pax        = /*INTEGER*/ SUBSTR(output-list2.str2, 32, 7) 
        out-list.logis      = /*DECIMAL*/ SUBSTR(output-list2.str2, 39,15) 
        out-list.proz       = /*DECIMAL*/ SUBSTR(output-list2.str2, 54,7)  
        out-list.avrgrate   = /*DECIMAL*/ SUBSTR(output-list2.str2, 61,14) 
        out-list.m-room     = /*INTEGER*/ SUBSTR(output-list2.str2, 75,7)  
        out-list.m-pax      = /*INTEGER*/ SUBSTR(output-list2.str2, 82,7)  
        out-list.m-logis    = /*DECIMAL*/ SUBSTR(output-list2.str2, 89,15) 
        out-list.m-proz     = /*DECIMAL*/ SUBSTR(output-list2.str2, 104,7) 
        out-list.m-avrgrate = /*DECIMAL*/ SUBSTR(output-list2.str2, 111,14)
        out-list.y-room     = /*INTEGER*/ SUBSTR(output-list2.str2, 125,8) 
        out-list.y-pax      = /*INTEGER*/ SUBSTR(output-list2.str2, 133,8) 
        out-list.y-logis    = /*DECIMAL*/ SUBSTR(output-list2.str2, 141,18)
        out-list.y-proz     = /*DECIMAL*/ SUBSTR(output-list2.str2, 159,7) 
        out-list.y-avrgrate = /*DECIMAL*/ SUBSTR(output-list2.str2, 166,14)
        .
END.
