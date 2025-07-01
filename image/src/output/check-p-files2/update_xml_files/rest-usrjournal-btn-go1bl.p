DEFINE TEMP-TABLE output-list
  FIELD bezeich AS CHAR FORMAT "x(40)" /* Naufal Afthar - AFB4A4*/
  FIELD STR AS CHAR. 

DEFINE TEMP-TABLE rest-jour-list 
    FIELD datum     AS DATE 
    FIELD tabelno   AS CHAR
    FIELD billno    AS INTEGER   format ">>>>>>>>>"           
    FIELD artno     AS INTEGER   format ">>>>>>>>>"             
    FIELD descr     AS CHAR      format "x(28)"                  
    FIELD qty       AS INTEGER   FORMAT ">>>>>"                                
    FIELD amount    AS DECIMAL   format "->>>,>>>,>>>,>>>,>>9.99"
    FIELD depart    AS CHARACTER format "x(12)"                  
    FIELD zeit      AS CHARACTER
    FIELD id        AS CHARACTER
    FIELD tb        AS CHARACTER
    .      

DEF INPUT PARAMETER sumFlag AS LOGICAL.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF INPUT PARAMETER usr-init AS CHAR.
DEF INPUT PARAMETER curr-dept AS INT.
DEF INPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER TABLE FOR rest-jour-list.

DEF VAR monthPart AS CHAR.
DEF VAR dayPart   AS CHAR.
DEF VAR yearPart  AS CHAR.
DEF VAR fullYear  AS INTEGER.
DEF VAR date-flag AS LOGICAL.

/* Naufal Afthar - AFB4B4*/
/*RUN rest-usrjournal-btn-gobl.p(sumFlag, from-date, to-date, usr-init, 
                               curr-dept, price-decimal, OUTPUT TABLE output-list).
*/

RUN rest-usrjournal-btn-cldbl.p(sumFlag, from-date, to-date, usr-init, 
                               curr-dept, price-decimal, OUTPUT TABLE output-list).

FOR EACH rest-jour-list.
    DELETE rest-jour-list.
END.

FOR EACH output-list:
    monthPart = SUBSTRING(SUBSTRING(output-list.str,1,8), 4, 2). /*modified by Bernatd 683B73*/
    dayPart   = SUBSTRING(SUBSTRING(output-list.str,1,8), 1, 2). 
    yearPart  = SUBSTRING(SUBSTRING(output-list.str,1,8), 7, 2).

    IF  monthPart = "" AND dayPart = "" AND yearPart = "" THEN date-flag = YES.
    

    IF INTEGER(yearPart) < 50 THEN
    DO:
        fullYear =  2000 + INTEGER(yearPart).
    END.          
    ELSE
    DO:
        fullYear = 1900 + INTEGER(yearPart).
    END.  
    IF NOT date-flag THEN 
    DO:
        CREATE rest-jour-list.
        ASSIGN 
            rest-jour-list.datum   = DATE(INTEGER(monthPart), INTEGER(dayPart), fullYear) /* Malik Serverless 385 : STR ->  output-list.str -> date(SUBSTRING(output-list.str,1,8)) */         
            rest-jour-list.tabelno = SUBSTRING(output-list.str,9,6)           
            rest-jour-list.billno  = INTEGER(SUBSTRING(output-list.str,15,9)) 
            rest-jour-list.artno   = INTEGER(SUBSTRING(output-list.str,24,9))
            /*rest-jour-list.descr   = SUBSTRING(output-list.str,33, 28) */
            rest-jour-list.descr   = output-list.bezeich /* Naufal Afthar - AFB4A4*/
            rest-jour-list.qty     = INTEGER(SUBSTRING(output-list.str,73,5)) 
            rest-jour-list.amount  = DECIMAL(SUBSTRING(output-list.str,78,17))         
            rest-jour-list.depart  = SUBSTRING(output-list.str,61, 12)        
            rest-jour-list.zeit    = SUBSTRING(output-list.str,95, 5)         
            rest-jour-list.id      = SUBSTRING(output-list.str,100, 5)         
            rest-jour-list.tb      = SUBSTRING(output-list.str,105, 5)
            .
    END. 
    /*modified by Bernatd 683B73*/
    ELSE 
    DO:
        CREATE rest-jour-list.
        ASSIGN   
            rest-jour-list.descr   = "TOTAL"       
            rest-jour-list.qty     = INTEGER(SUBSTRING(output-list.str,73,5)) 
            rest-jour-list.amount  = DECIMAL(SUBSTRING(output-list.str,78,17))         
            .
    END.       
    
END.














