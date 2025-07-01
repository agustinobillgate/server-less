DEFINE TEMP-TABLE bline-list 
    FIELD flag        AS INTEGER INITIAL 0 
    FIELD userinit    LIKE bediener.userinit 
    FIELD selected    AS LOGICAL INITIAL NO 
    FIELD name        LIKE bediener.username 
    FIELD bl-recid    AS INTEGER INITIAL 0
    . 

DEFINE TEMP-TABLE output-list 
    FIELD flag        AS CHAR 
    FIELD amt-foreign AS DECIMAL 
    FIELD str-foreign AS CHAR FORMAT "x(16)" LABEL "        F-Amount" 
    FIELD STR         AS CHAR
    FIELD gname       AS CHAR FORMAT "x(21)" COLUMN-LABEL "Guest Name"
    .

DEFINE TEMP-TABLE fo-cashjour-list
    FIELD datum     AS DATE     
    FIELD zinr      AS CHARACTER FORMAT "x(6)"
    FIELD rechnr    AS INTEGER   FORMAT ">>>>>>>>>"
    FIELD artnr     AS INTEGER   FORMAT ">>>>"
    FIELD bezeich   AS CHARACTER FORMAT "x(36)"
    FIELD dept      AS CHARACTER FORMAT "x(16)"
    FIELD l-amount  AS DECIMAL   FORMAT "->,>>>,>>>,>>9.99"
    FIELD f-amount  AS DECIMAL   FORMAT "->,>>>,>>>,>>9.99"
    FIELD gname     AS CHARACTER FORMAT "x(21)"
    FIELD zeit      AS CHARACTER FORMAT "x(8)"
    FIELD ID        AS CHARACTER FORMAT "x(3)"
    .

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER case-type    AS INTEGER.
DEFINE INPUT PARAMETER curr-shift   AS INTEGER.
DEFINE INPUT PARAMETER summary-flag AS LOGICAL.

DEFINE INPUT-OUTPUT PARAMETER from-date  AS DATE.
DEFINE OUTPUT PARAMETER double-currency  AS LOGICAL.
DEFINE OUTPUT PARAMETER foreign-curr     AS CHAR INIT "".

DEFINE INPUT-OUTPUT PARAMETER TABLE FOR bline-list.
DEFINE OUTPUT PARAMETER TABLE FOR fo-cashjour-list.

/*
define VARIABLE pvILanguage     as INTEGER INIT 0. 
define variable case-type       as INTEGER INIT 2.
define variable curr-shift      as INTEGER INIT 0.
define variable summary-flag    as LOGICAL INIT NO.
define variable from-date       as DATE    INIT 01/14/19.
define VARIABLE double-currency AS LOGICAL.
define variable foreign-curr    AS CHAR .
*/

RUN fo-cashgjournbl.p (pvILanguage, case-type, curr-shift, summary-flag, INPUT-OUTPUT from-date, 
    OUTPUT double-currency, OUTPUT foreign-curr, INPUT-OUTPUT TABLE bline-list, OUTPUT TABLE output-list).

FOR EACH fo-cashjour-list:
    DELETE fo-cashjour-list.
END.

FOR EACH output-list:
    CREATE fo-cashjour-list.
    ASSIGN
        fo-cashjour-list.datum    = DATE(SUBSTRING(output-list.STR,1,8))
        fo-cashjour-list.zinr     = SUBSTRING(output-list.STR,9,6)
        fo-cashjour-list.rechnr   = INTEGER(SUBSTRING(output-list.STR,15,9))
        fo-cashjour-list.artnr    = INTEGER(SUBSTRING(output-list.STR,24,4))
        fo-cashjour-list.bezeich  = SUBSTRING(output-list.STR,28, 40)
        fo-cashjour-list.dept     = SUBSTRING(output-list.STR,68, 17)  
        fo-cashjour-list.l-amount = DECIMAL(SUBSTRING(output-list.STR,85,17))   
        fo-cashjour-list.f-amount = DECIMAL(output-list.str-foreign)
        fo-cashjour-list.gname    = output-list.gname      
        fo-cashjour-list.zeit     = SUBSTRING(output-list.STR,102, 8)  
        fo-cashjour-list.ID       = SUBSTRING(output-list.STR,110, 3)  
        .
END.   

