DEFINE TEMP-TABLE output-list 
    FIELD STR     AS CHAR
    FIELD gname   AS CHAR FORMAT "x(32)" COLUMN-LABEL "Guest Name"
    . 

DEFINE TEMP-TABLE fo-usrjourn-list
    FIELD rec-id    AS INTEGER
    FIELD datum     AS DATE
    FIELD zinr      AS CHARACTER FORMAT "x(6)"
    FIELD rechnr    AS INTEGER   FORMAT ">>>>>>>>>"
    FIELD artnr     AS INTEGER   FORMAT ">>>>"
    FIELD bezeich   AS CHARACTER FORMAT "x(30)"
    FIELD dept      AS CHARACTER FORMAT "x(12)"
    FIELD qty       AS INTEGER   FORMAT "->>>9"
    FIELD amount    AS DECIMAL   FORMAT "->,>>>,>>>,>>9.99"
    FIELD gname     AS CHARACTER FORMAT "x(32)"
    FIELD zeit      AS CHARACTER FORMAT "x(8)"
    FIELD ID        AS CHARACTER FORMAT "x(4)"
    FIELD sysdate   AS DATE 
    .

DEFINE INPUT PARAMETER incl-trans   AS LOGICAL.
DEFINE INPUT PARAMETER excl-trans   AS LOGICAL.
DEFINE INPUT PARAMETER trans-only   AS LOGICAL.

DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER from-dept    AS INTEGER.
DEFINE INPUT PARAMETER to-dept      AS INTEGER.
DEFINE INPUT PARAMETER from-art     AS INTEGER.
DEFINE INPUT PARAMETER to-art       AS INTEGER.

DEFINE INPUT PARAMETER usr-init     AS CHAR.
DEFINE INPUT PARAMETER long-digit   AS LOGICAL.
DEFINE INPUT PARAMETER foreign-flag AS LOGICAL.

DEFINE OUTPUT PARAMETER TABLE FOR fo-usrjourn-list.

/*
DEFINE Variable  incl-trans AS LOGICAL INIT YES.
DEFINE Variable  excl-trans AS LOGICAL INIT NO.
DEFINE Variable  trans-only AS LOGICAL INIT NO.
        
DEFINE Variable  from-date AS DATE INIT 08/10/19.
DEFINE Variable  to-date   AS DATE INIT 08/10/19.
DEFINE Variable  from-dept AS INTEGER INIT 0.
DEFINE Variable  to-dept   AS INTEGER INIT 99.
DEFINE Variable  from-art  AS INTEGER INIT 0.
DEFINE Variable  to-art    AS INTEGER INIT 9999.
       
DEFINE Variable  usr-init     AS CHAR INIT "AG".
DEFINE Variable  long-digit   AS LOGICAL INIT NO.
DEFINE Variable  foreign-flag AS LOGICAL INIT NO.
*/

RUN fo-usrjournal-cldbl.p (incl-trans, excl-trans, trans-only, from-date, to-date, 
    from-dept, to-dept, from-art, to-art, usr-init, long-digit, foreign-flag, OUTPUT TABLE output-list).

FOR EACH fo-usrjourn-list:
    DELETE fo-usrjourn-list.
END.


FOR EACH output-list.
    CREATE fo-usrjourn-list.
    ASSIGN
        fo-usrjourn-list.datum   = DATE(SUBSTRING(output-list.STR, 1, 8))
        fo-usrjourn-list.zinr    = SUBSTRING(output-list.STR, 9, 6)
        fo-usrjourn-list.rechnr  = INTEGER(SUBSTRING(output-list.STR, 15, 9))
        fo-usrjourn-list.artnr   = INTEGER(SUBSTRING(output-list.STR, 24,  4)) 
        fo-usrjourn-list.bezeich = SUBSTRING(output-list.STR, 28, 30)        
        fo-usrjourn-list.dept    = SUBSTRING(output-list.STR, 58, 12)        
        fo-usrjourn-list.qty     = INTEGER(SUBSTRING(output-list.STR, 70, 5)) 
        fo-usrjourn-list.Amount  = DECIMAL(SUBSTRING(output-list.STR, 75, 17))
        fo-usrjourn-list.gname   = output-list.gname            
        fo-usrjourn-list.zeit    = SUBSTRING(output-list.STR, 92, 8)         
        fo-usrjourn-list.ID      = SUBSTRING(output-list.STR, 100, 4)        
        fo-usrjourn-list.sysdate = DATE(SUBSTRING(output-list.STR, 104, 8))  
        fo-usrjourn-list.rec-id  = INTEGER(SUBSTRING(output-list.STR, 112, 122))
        .
END.

