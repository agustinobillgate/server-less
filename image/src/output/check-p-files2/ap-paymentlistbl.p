DEF TEMP-TABLE t-list 
    FIELD artnr   AS INTEGER 
    FIELD bezeich AS CHAR FORMAT "x(36)" 
    FIELD betrag  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99". 

DEFINE TEMP-TABLE output-list 
  FIELD srecid AS INTEGER INITIAL 0
  FIELD remark AS CHAR FORMAT "x(32)" LABEL "Remark"
  FIELD STR    AS CHAR. 

DEFINE TEMP-TABLE ap-paymentlist
    FIELD srecid     AS INTEGER INIT 0
    FIELD remark     AS CHARACTER 
    FIELD billdate   AS DATE
    FIELD docu-nr    AS CHARACTER
    FIELD ap-amount  AS DECIMAL
    FIELD pay-amount AS DECIMAL
    FIELD pay-date   AS DATE
    FIELD id         AS CHARACTER
    FIELD pay-art    AS CHARACTER
    FIELD supplier   AS CHARACTER
    FIELD deliv-note AS CHARACTER
    .

DEF INPUT  PARAMETER all-supp       AS LOGICAL.
DEF INPUT  PARAMETER remark-flag    AS LOGICAL.
DEF INPUT  PARAMETER from-supp      AS CHAR.
DEF INPUT  PARAMETER from-date      AS DATE.
DEF INPUT  PARAMETER to-date        AS DATE.
DEF INPUT  PARAMETER from-remark    AS CHAR.
DEF INPUT  PARAMETER price-decimal  AS INT.
DEF OUTPUT PARAMETER lief-nr1       AS INT.
DEF OUTPUT PARAMETER ap-exist       AS LOGICAL.
DEF OUTPUT PARAMETER err-code       AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR ap-paymentlist.
DEF OUTPUT PARAMETER TABLE FOR t-list.

DEF VAR amount AS CHAR.

RUN ap-paylist-btn-go-bl.p (all-supp, remark-flag, from-supp, from-date, to-date,
                 from-remark, price-decimal, OUTPUT lief-nr1, OUTPUT ap-exist,
                 OUTPUT err-code, OUTPUT TABLE output-list, OUTPUT TABLE t-list).

FOR EACH output-list:
    amount = TRIM(SUBSTRING(output-list.str,39,17)).
    IF amount EQ "TOTAL" THEN amount = "".
    ELSE IF amount EQ "Grand TOTAL" THEN amount = "".

    CREATE ap-paymentlist.
    ASSIGN 
        ap-paymentlist.srecid      = output-list.srecid
        ap-paymentlist.remark      = output-list.remark
        ap-paymentlist.billdate    = DATE(TRIM(SUBSTRING(output-list.str,1,8)))
        ap-paymentlist.docu-nr     = TRIM(SUBSTRING(output-list.str,9,30))
        ap-paymentlist.ap-amount   = DECIMAL(amount)
        ap-paymentlist.pay-amount  = DECIMAL(SUBSTRING(output-list.str,56,17))
        ap-paymentlist.pay-date    = DATE(TRIM(SUBSTRING(output-list.str,73,8)))
        ap-paymentlist.id          = TRIM(SUBSTRING(output-list.str,81,3))
        ap-paymentlist.pay-art     = SUBSTRING(output-list.str,84,20)
        ap-paymentlist.supplier    = SUBSTRING(output-list.STR,136,24)  /*MG Kebutuhan Cloud 1C5944*/
        ap-paymentlist.deliv-note  = SUBSTRING(output-list.str,161,30)  /*MG Kebutuhan Cloud 1C5944*/
        .

    /*IF ap-paymentlist.docu-nr NE "" THEN
    DO:
        FIND FIRST l-kredit WHERE l-kredit.NAME EQ ap-paymentlist.docu-nr NO-LOCK NO-ERROR.
        IF AVAILABLE l-kredit THEN
        DO:
            ap-paymentlist.deliv-note  = l-kredit.lscheinnr.
        END.
    END.*/
END.    
