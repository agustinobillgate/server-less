DEFINE TEMP-TABLE str-list 
  FIELD fibu        AS CHAR 
  FIELD other-fibu  AS LOGICAL 
  FIELD op-recid    AS INTEGER 
  FIELD lscheinnr   AS CHAR 
  FIELD s           AS CHAR FORMAT "x(164)". 

DEFINE TEMP-TABLE cancel-stockout
    FIELD datum     AS DATE
    FIELD lager     AS CHARACTER
    FIELD lscheinnr AS CHARACTER
    FIELD artnr     AS INTEGER
    FIELD bezeich   AS CHARACTER
    FIELD out-qty   AS DECIMAL FORMAT "->>>,>>9.99"
    FIELD avrg-price AS DECIMAL FORMAT "->>>,>>9.99"
    FIELD amount    AS DECIMAL  FORMAT ">,>>>,>>>,>>9.99"
    FIELD id        AS CHARACTER
    FIELD reason    AS CHARACTER
    .  

DEF INPUT  PARAMETER from-grp AS INT.
DEF INPUT  PARAMETER mi-alloc-chk AS LOGICAL.
DEF INPUT  PARAMETER mi-article-chk AS LOGICAL.
DEF INPUT  PARAMETER mi-docu-chk AS LOGICAL.
DEF INPUT  PARAMETER mi-date-chk AS LOGICAL.
DEF INPUT  PARAMETER from-lager AS INT.
DEF INPUT  PARAMETER to-lager   AS INT.
DEF INPUT  PARAMETER from-date  AS DATE.
DEF INPUT  PARAMETER to-date    AS DATE.
DEF INPUT  PARAMETER from-art   AS INT.
DEF INPUT  PARAMETER to-art     AS INT.
DEF INPUT  PARAMETER show-price AS LOGICAL.
DEF INPUT  PARAMETER cost-acct  AS CHAR.
DEF INPUT  PARAMETER mattype    AS INT.
DEF OUTPUT PARAMETER it-exist AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR cancel-stockout.

/*    DEF VAR pvILanguage AS INT INIT 1.
    DEF VAR s-artnr AS INT INIT 3312036.
    DEF VAR show-price AS LOGICAL INIT YES.
    DEF VAR from-lager AS INT INIT 1.
    DEF VAR to-lager AS INT INIT 99.*/

RUN cancel-stockout-btn-gobl.p
    (from-grp, mi-alloc-chk, mi-article-chk, mi-docu-chk, mi-date-chk, from-lager, to-lager, 
     from-date, to-date, from-art, to-art, show-price, cost-acct, mattype, OUTPUT it-exist, OUTPUT TABLE str-list).

FOR EACH cancel-stockout:
    DELETE cancel-stockout.
END.

FOR EACH str-list:
    CREATE cancel-stockout.
    ASSIGN             
       cancel-stockout.datum        = DATE(SUBSTRING(str-list.s,1,8))
       cancel-stockout.lager        = SUBSTRING(str-list.s,9,30)
       cancel-stockout.lscheinnr    = SUBSTRING(str-list.s,120,12)
       cancel-stockout.artnr        = INTEGER(SUBSTRING(str-list.s,39,7))
       cancel-stockout.bezeich      = SUBSTRING(str-list.s,46,32) 
       cancel-stockout.out-qty      = DECIMAL(SUBSTRING(str-list.s,78,14))         
       cancel-stockout.avrg-price   = DECIMAL(SUBSTRING(str-list.s,92,14)) 
       cancel-stockout.amount       = DECIMAL(SUBSTRING(str-list.s,106,14))        
       cancel-stockout.id           = SUBSTRING(str-list.s,132,2)
       cancel-stockout.reason       = SUBSTRING(str-list.s,142,24)
     .
END.

/*FOR EACH cancel-stockout:
    DISP cancel-stockout.
END.*/

