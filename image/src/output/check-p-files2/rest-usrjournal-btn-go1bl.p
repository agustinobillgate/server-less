DEFINE TEMP-TABLE output-list 
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

RUN rest-usrjournal-btn-gobl.p(sumFlag, from-date, to-date, usr-init, 
                               curr-dept, price-decimal, OUTPUT TABLE output-list).

FOR EACH rest-jour-list.
    DELETE rest-jour-list.
END.

FOR EACH output-list:
    CREATE rest-jour-list.
    ASSIGN
        rest-jour-list.datum   = date(SUBSTRING(STR,1,8))           
        rest-jour-list.tabelno = SUBSTRING(STR,9,6)           
        rest-jour-list.billno  = INTEGER(SUBSTRING(STR,15,9)) 
        rest-jour-list.artno   = integer(SUBSTRING(STR,24,9))
        rest-jour-list.descr   = SUBSTRING(STR,33, 28)        
        rest-jour-list.qty     = INTEGER(SUBSTRING(STR,73,5)) 
        rest-jour-list.amount  = decimal(SUBSTRING(STR,78,17))         
        rest-jour-list.depart  = SUBSTRING(STR,61, 12)        
        rest-jour-list.zeit    = SUBSTRING(STR,95, 5)         
        rest-jour-list.id      = SUBSTRING(STR,100, 3)         
        rest-jour-list.tb      = SUBSTRING(STR,103, 3)
        .
END.











