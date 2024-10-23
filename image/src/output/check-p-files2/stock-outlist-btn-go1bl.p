DEFINE TEMP-TABLE str-list 
  FIELD billdate    AS DATE
  FIELD fibu        AS CHAR FORMAT "x(12)"
  FIELD other-fibu  AS LOGICAL
  FIELD op-recid    AS INTEGER
  FIELD lscheinnr   AS CHAR
  FIELD s           AS CHAR FORMAT "x(135)"
  FIELD ID          AS CHAR FORMAT "x(4)". 

DEFINE TEMP-TABLE stock-outlist
    FIELD datum     AS DATE
    FIELD lager     AS CHARACTER
    FIELD lscheinnr AS CHARACTER
    FIELD docu-nr   AS CHARACTER
    FIELD art-nr    AS INTEGER
    FIELD art-bez   AS CHARACTER
    FIELD out-qty   AS DECIMAL FORMAT "->,>>>,>>9.999"
    FIELD avrg-price AS DECIMAL FORMAT ">>>,>>>,>>9.99"
    FIELD amount    AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD id        AS CHARACTER
    FIELD billdate    AS DATE
    FIELD fibu        AS CHAR FORMAT "x(12)"
    FIELD other-fibu  AS LOGICAL
    FIELD op-recid    AS INTEGER
    FIELD strPanjang  AS CHAR FORMAT "x(135)"
    .  

DEF INPUT PARAMETER trans-code  AS CHARACTER.
DEF INPUT PARAMETER from-grp    AS INTEGER.
DEF INPUT PARAMETER mi-alloc    AS LOGICAL.
DEF INPUT PARAMETER mi-article  AS LOGICAL.
DEF INPUT PARAMETER mi-docu     AS LOGICAL.
DEF INPUT PARAMETER mi-date     AS LOGICAL.
DEF INPUT PARAMETER mattype     AS INTEGER.
DEF INPUT PARAMETER from-lager  AS INTEGER.
DEF INPUT PARAMETER to-lager    AS INTEGER.
DEF INPUT PARAMETER from-date   AS DATE.
DEF INPUT PARAMETER to-date     AS DATE.
DEF INPUT PARAMETER from-art    AS INTEGER.
DEF INPUT PARAMETER to-art 	    AS INTEGER.
DEF INPUT PARAMETER show-price  AS LOGICAL.
DEF INPUT PARAMETER cost-acct   AS CHARACTER.
DEF INPUT PARAMETER deptNo	    AS INTEGER.
DEF OUTPUT PARAMETER it-exist   AS LOGICAL.  
DEF OUTPUT PARAMETER tot-anz    AS DECIMAL.
DEF OUTPUT PARAMETER tot-amount AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR stock-outlist.

/*    DEF VAR trans-code      AS CHAR         INIT "".
    DEF VAR from-grp        AS INT          INIT 0.
    DEF VAR mi-alloc        AS LOGICAL      INIT NO.
    DEF VAR mi-article      AS LOGICAL      INIT NO.
    DEF VAR mi-docu         AS LOGICAL      INIT YES.
    DEF VAR mi-date         AS LOGICAL      INIT NO.
    DEF VAR mattype         AS INT          INIT 0.
    DEF VAR from-lager      AS INT          INIT 1.
    DEF VAR to-lager        AS INT          INIT 99.
    DEF VAR from-date       AS DATE         INIT 5/1/19.
    DEF VAR to-date         AS DATE         INIT 5/1/19.
    DEF VAR from-art        AS INT          INIT 1.
    DEF VAR to-art          AS INT          INIT 9999999.
    DEF VAR show-price      AS LOGICAL      INIT YES.
    DEF VAR cost-acct       AS CHAR         INIT "".
    DEF VAR deptNo          AS INT          INIT 0.
    DEF VAR it-exist        AS LOGICAL.
    DEF VAR tot-anz         AS DECIMAL.
    DEF VAR tot-amount      AS DECIMAL.*/

RUN stock-outlist-btn-gobl.p
    (trans-code, from-grp, mi-alloc, mi-article, mi-docu, mi-date, mattype, from-lager, to-lager, from-date, to-date, from-art , to-art, show-price, cost-acct, 
     deptNo, OUTPUT it-exist, OUTPUT tot-anz, OUTPUT tot-amount, OUTPUT TABLE str-list).
	 
FOR EACH stock-outlist:
    DELETE stock-outlist.
END.

FOR EACH str-list:
    CREATE stock-outlist.
    ASSIGN             
       stock-outlist.datum        = DATE(SUBSTRING(str-list.s,1,8))
       stock-outlist.lager        = SUBSTRING(str-list.s,9,30)
       stock-outlist.docu-nr      = SUBSTRING(str-list.s,141,12)
       stock-outlist.art-nr       = INTEGER(SUBSTRING(str-list.s,39,7))
       stock-outlist.art-bez      = SUBSTRING(str-list.s,46,50)
       stock-outlist.out-qty      = DECIMAL(SUBSTRING(str-list.s,96,14))         
       stock-outlist.avrg-price   = DECIMAL(SUBSTRING(str-list.s,110,14))        
       stock-outlist.amount       = DECIMAL(SUBSTRING(str-list.s,124,17))        
       stock-outlist.id           = str-list.id
       stock-outlist.billdate     = str-list.billdate
       stock-outlist.fibu         = str-list.fibu
       stock-outlist.other-fibu   = str-list.other-fibu
       stock-outlist.op-recid     = str-list.op-recid
       stock-outlist.strPanjang   = str-list.s
     .
END.

/*FOR EACH stock-outlist:
    DISP stock-outlist.
END.*/

