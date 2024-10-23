
DEFINE TEMP-TABLE age-list 
  FIELD nr              AS INTEGER 
  FIELD paint-it        AS LOGICAL INITIAL NO 
  FIELD rechnr          AS INTEGER FORMAT ">>>>>>>>9" 
  FIELD refno           AS INTEGER FORMAT ">>>>>>>>>" 
  FIELD rechnr2         AS INTEGER FORMAT ">>>>>>>>>"
  FIELD opart           AS INTEGER 
  FIELD zahlkonto       AS INTEGER
  FIELD counter         AS INTEGER
  FIELD gastnr          AS INTEGER 
  FIELD company         AS CHAR
  FIELD billname        AS CHAR FORMAT "x(36)" 
  FIELD gastnrmember    AS INTEGER 
  FIELD zinr            LIKE zimmer.zinr		/*MT 25/07/12 */
  FIELD datum           AS DATE
  FIELD rgdatum         AS DATE 
  FIELD paydatum        AS DATE 
  FIELD user-init       AS CHAR FORMAT "x(2)" 
  FIELD bezeich         AS CHARACTER FORMAT "x(16)" 
  FIELD wabkurz         AS CHAR FORMAT "x(4)" 
  FIELD debt            AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0 
  FIELD credit          AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0 
  FIELD fdebt           AS DECIMAL LABEL "Foreign-Amt" 
                           FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0 
  FIELD t-debt          AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0   /*MT 20/07/12 */
  FIELD tot-debt        AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0   /*MT 20/07/12 */
  FIELD rid             AS INTEGER INITIAL 0
  FIELD dept            AS INTEGER INITIAL 0
  FIELD gname           AS CHAR    FORMAT "x(36)"
  FIELD voucher         AS CHAR    FORMAT "x(12)"
  FIELD ankunft         AS DATE    FORMAT "99/99/99"
  FIELD abreise         AS DATE    FORMAT "99/99/99"
  FIELD stay            AS INTEGER FORMAT ">>9"
  FIELD remarks         AS CHAR    FORMAT "x(50)" /*MT 130812 */
  FIELD ttl             AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0   /*MT 20/07/12 */

  FIELD resname         AS CHAR
  FIELD comp-name       AS CHAR
  FIELD comp-add        AS CHAR
  FIELD comp-fax        AS CHAR
  FIELD comp-phone      AS CHAR
  INDEX idx1 rechnr dept gastnr
      . 

DEF INPUT  PARAMETER detail     AS LOGICAL.
DEF INPUT  PARAMETER incl       AS LOGICAL.
DEF INPUT  PARAMETER t-artnr    AS INT.
DEF INPUT  PARAMETER t-artart   AS INT.
DEF INPUT  PARAMETER t-dept     AS INT.
DEF INPUT  PARAMETER from-name  AS CHAR.
DEF INPUT  PARAMETER to-name    AS CHAR.
DEF INPUT  PARAMETER fr-date    AS DATE.
DEF INPUT  PARAMETER to-date    AS DATE.
DEF INPUT  PARAMETER Bdate      AS DATE.
DEF OUTPUT PARAMETER tot-debt   AS DECIMAL.
DEF OUTPUT PARAMETER tot-paid   AS DECIMAL.
DEF OUTPUT PARAMETER tot-bal    AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR age-list.

DEF VAR curr-art      AS INTEGER.
DEF VAR debt-selected AS LOGICAL.

IF SUBSTR(to-name,1,2) = "zz" THEN RUN create-age-list1A. 
ELSE RUN create-age-list1.

PROCEDURE create-age-list1:
    DEFINE VARIABLE pay-amt       AS DECIMAL.
    DEFINE VARIABLE pay-date      AS DATE.
    DEFINE BUFFER abuff           FOR age-list.

    curr-art = t-artnr.

    RUN ar-subledger-create-age-list1bl.p
        (incl, t-artnr, t-dept, from-name, to-name,
        fr-date, to-date, Bdate, OUTPUT tot-debt, OUTPUT tot-paid,
        OUTPUT TABLE age-list).

    tot-bal = tot-debt - tot-paid. 
    DISP tot-debt tot-paid tot-bal WITH FRAME frame1. 
    debt-selected = YES. 
 
    pay-amt = 0. 
    IF NOT detail THEN 
    FOR EACH age-list BY age-list.nr descending: 
        IF age-list.billname NE "" AND pay-amt NE 0 THEN 
        DO: 
            age-list.paydatum = pay-date. 
            age-list.credit = age-list.credit + pay-amt. 
            age-list.tot-debt = age-list.tot-debt - pay-amt. 
            pay-amt = 0. 
        END. 
        ELSE IF age-list.billname = "" THEN 
        DO: 
            pay-amt = pay-amt + age-list.credit. 
            pay-date = age-list.paydatum. 
            delete age-list. 
        END. 
    END. 

    IF NOT detail AND t-artart = 2 THEN
    FOR EACH age-list WHERE age-list.billname NE "": 
        FOR EACH abuff WHERE abuff.rechnr = age-list.rechnr
            AND abuff.dept = age-list.dept
            AND abuff.gastnr = age-list.gastnr
            AND RECID(abuff) NE RECID(age-list) USE-INDEX idx1:
            ASSIGN
                age-list.credit   = age-list.credit   + abuff.credit
                age-list.debt     = age-list.debt     + abuff.debt
                age-list.fdebt    = age-list.fdebt    + abuff.fdebt
                age-list.tot-debt = age-list.tot-debt + abuff.tot-debt
                .   
            DELETE abuff.
        END.
    END.
END. 
 
PROCEDURE create-age-list1A:
    DEFINE VARIABLE pay-amt       AS DECIMAL. 
    DEFINE VARIABLE pay-date      AS DATE.
    DEFINE BUFFER abuff           FOR age-list.
  
    curr-art = t-artnr. 
    RUN ar-subledger-create-age-list1abl.p
        (incl, t-artnr, t-dept, from-name, to-name,
        fr-date, to-date, Bdate, OUTPUT tot-debt, OUTPUT tot-paid,
        OUTPUT TABLE age-list).

    tot-bal = tot-debt - tot-paid. 
  
    debt-selected = YES. 
 
    pay-amt = 0. 
    IF NOT detail THEN 
    FOR EACH age-list BY age-list.nr descending: 
        IF age-list.billname NE "" AND pay-amt NE 0 THEN 
        DO: 
            age-list.paydatum = pay-date. 
            age-list.credit = age-list.credit + pay-amt. 
            age-list.tot-debt = age-list.tot-debt - pay-amt. 
            pay-amt = 0. 
        END. 
        ELSE IF age-list.billname = "" THEN 
        DO: 
            pay-amt = pay-amt + age-list.credit. 
            pay-date = age-list.paydatum. 
            delete age-list. 
        END. 
    END. 

    IF NOT detail AND t-artart = 2 THEN
    FOR EACH age-list WHERE age-list.billname NE "": 
        FOR EACH abuff WHERE abuff.rechnr = age-list.rechnr
            AND abuff.dept = age-list.dept
            AND abuff.gastnr = age-list.gastnr
            AND RECID(abuff) NE RECID(age-list) USE-INDEX idx1:
            ASSIGN
              age-list.credit   = age-list.credit   + abuff.credit
              age-list.debt     = age-list.debt     + abuff.debt
              age-list.fdebt    = age-list.fdebt    + abuff.fdebt
              age-list.tot-debt = age-list.tot-debt + abuff.tot-debt
            . 
            DELETE abuff.
        END.
    END. 
END. 
