DEFINE TEMP-TABLE str-list 
  FIELD h-recid     AS INTEGER INITIAL 0 
  FIELD l-recid     AS INTEGER INITIAL 0 
  FIELD lief-nr     AS INTEGER 
  FIELD billdate    AS DATE 
  FIELD artnr       AS INTEGER 
  FIELD lager-nr    AS INTEGER 
  FIELD docu-nr     AS CHAR 
  FIELD lscheinnr   AS CHAR INITIAL "" 
  FIELD invoice-nr  AS CHAR FORMAT "x(16)" INITIAL "" LABEL "Invoice No" 
  FIELD qty         AS DECIMAL 
  FIELD epreis      AS DECIMAL 
  FIELD warenwert   AS DECIMAL 
  FIELD deci1-3     AS DECIMAL 
  FIELD s           AS CHAR FORMAT "x(135)". 

DEFINE TEMP-TABLE cancel-stockinhis-list
    FIELD datum     AS DATE FORMAT "99/99/9999"
    FIELD lager     AS CHARACTER
    FIELD lief-nr   AS INTEGER
    FIELD lief      AS CHARACTER
    FIELD art       AS CHARACTER
    FIELD bezeich   AS CHARACTER
    FIELD unit      AS CHARACTER
    FIELD epreis    AS DECIMAL FORMAT ">,>>>,>>>,>>9.99"
    FIELD in-qty    AS DECIMAL FORMAT "->>>,>>9.99"     
    FIELD amount    AS DECIMAL FORMAT ">,>>>,>>>,>>9.99"
    FIELD docunr    AS CHARACTER
    FIELD dlvnote   AS CHARACTER
    FIELD note      AS CHARACTER
    FIELD reason    AS CHARACTER
    FIELD invnr     AS CHARACTER
    .  

DEF INPUT  PARAMETER pvILanguage AS INT  NO-UNDO.
DEF INPUT  PARAMETER all-supp    AS LOGICAL  NO-UNDO.
DEF INPUT  PARAMETER sorttype    AS INT  NO-UNDO.
DEF INPUT  PARAMETER from-grp    AS INT  NO-UNDO.
DEF INPUT  PARAMETER store       AS INT  NO-UNDO.
DEF INPUT  PARAMETER from-date   AS DATE  NO-UNDO.
DEF INPUT  PARAMETER to-date     AS DATE  NO-UNDO.
DEF INPUT  PARAMETER show-price  AS LOGICAL  NO-UNDO.
DEF INPUT  PARAMETER from-supp   AS CHARACTER.
DEF OUTPUT PARAMETER TABLE FOR cancel-stockinhis-list.

RUN cancel-stockinhis-btn-go-cldbl.p (pvILanguage, all-supp, sorttype, from-grp, store, from-date, to-date, show-price, from-supp, OUTPUT TABLE str-list).

FOR EACH cancel-stockinhis-list:
    DELETE cancel-stockinhis-list.
END.

FOR EACH str-list:
    CREATE cancel-stockinhis-list.

    ASSIGN
        cancel-stockinhis-list.datum    =   DATE(SUBSTR(str-list.s, 1,  8))
        cancel-stockinhis-list.lager    =   SUBSTR(str-list.s, 9,  2)
        cancel-stockinhis-list.lief-nr  =   str-list.lief-nr
        cancel-stockinhis-list.lief     =   SUBSTR(str-list.s, 84, 18) 
        cancel-stockinhis-list.art      =   SUBSTR(str-list.s, 11,  7) 
        cancel-stockinhis-list.bezeich  =   SUBSTR(str-list.s, 18, 32) 
        cancel-stockinhis-list.unit     =   SUBSTR(str-list.s, 50, 6)  
        cancel-stockinhis-list.epreis   =   DECIMAL(SUBSTR(str-list.s,144, 14))
        cancel-stockinhis-list.in-qty   =   DECIMAL(SUBSTR(str-list.s, 56, 13))
        cancel-stockinhis-list.amount   =   DECIMAL(SUBSTR(str-list.s, 69, 15))
        cancel-stockinhis-list.docunr   =   SUBSTR(str-list.s, 108, 16)
        cancel-stockinhis-list.dlvnote  =   SUBSTR(str-list.s, 124, 20)
        cancel-stockinhis-list.note     =   SUBSTR(str-list.s, 158, 26)
        cancel-stockinhis-list.reason   =   SUBSTR(str-list.s, 184, 24)
        cancel-stockinhis-list.invnr    =   str-list.invoice-nr
        .
END.
