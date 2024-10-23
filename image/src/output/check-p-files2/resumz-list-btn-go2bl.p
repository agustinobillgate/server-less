
DEFINE TEMP-TABLE output-list 
  FIELD mqty        AS INTEGER FORMAT "->>,>>>" LABEL "MTD Qty" 
  FIELD STR         AS CHAR. 

DEFINE TEMP-TABLE turn-reportlist /*william 10/01/24 add format for every field except bezeich*/
    FIELD artno         AS INTEGER   FORMAT ">>>>>>>>>"   
    FIELD descr         AS CHARACTER FORMAT "x(24)"
    FIELD day-net       AS DECIMAL   FORMAT "->>,>>>,>>9.99"
    FIELD day-gros      AS DECIMAL   FORMAT "->>,>>>,>>9.99"
    FIELD day-proz      AS DECIMAL   FORMAT "->>9.99" 
    FIELD todate-net    AS DECIMAL   FORMAT "->>,>>>,>>9.99"
    FIELD todate-gros   AS DECIMAL   FORMAT "->>,>>>,>>9.99"
    FIELD todate-proz   AS DECIMAL   FORMAT "->>9.99" 
    FIELD mqty          AS INTEGER   FORMAT "->>,>>>" 
    .

DEF INPUT PARAMETER ldry-flag   AS LOGICAL.
DEF INPUT PARAMETER ldry        AS INT.
DEF INPUT PARAMETER dstore      AS INT.
DEF INPUT PARAMETER from-dept   AS INT.
DEF INPUT PARAMETER to-dept     AS INT.
DEF INPUT PARAMETER from-date   AS DATE.
DEF INPUT PARAMETER to-date     AS DATE.
DEF INPUT PARAMETER detailed    AS LOGICAL.
DEF INPUT PARAMETER long-digit  AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR turn-reportlist.

RUN resumz-list-btn-gobl.p (ldry-flag, ldry, dstore, from-dept, 
                            to-dept, from-date, to-date, detailed, 
                            long-digit, OUTPUT TABLE output-list).

FOR EACH turn-reportlist:
    DELETE turn-reportlist.
END.

FOR EACH output-list:
    CREATE turn-reportlist.
    ASSIGN 
       turn-reportlist.artno        = INT(SUBSTR(STR, 1, 9)) /*william 10/01/24 add increase artno substring*/  
       turn-reportlist.descr        = SUBSTR(STR, 10, 24) 
       turn-reportlist.day-net      = DECIMAL(SUBSTR(STR, 34, 14))
       turn-reportlist.day-gros     = DECIMAL(SUBSTR(STR, 48, 14))
       turn-reportlist.day-proz     = DECIMAL(SUBSTR(STR, 62, 7)) 
       turn-reportlist.todate-net   = DECIMAL(SUBSTR(STR, 69, 15))
       turn-reportlist.todate-gros  = DECIMAL(SUBSTR(STR, 84, 15))
       turn-reportlist.todate-proz  = DECIMAL(SUBSTR(STR, 99, 7)) 
       turn-reportlist.mqty         = output-list.mqty
       .
END.







