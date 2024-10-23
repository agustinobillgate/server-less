DEFINE TEMP-TABLE str-list 
  FIELD artnr       AS INTEGER 
  FIELD qty         AS DECIMAL 
  FIELD warenwert   AS DECIMAL 
  FIELD munit       AS CHAR FORMAT "x(4)"
  FIELD s           AS CHAR FORMAT "x(135)" 
  FIELD fibu        AS CHAR FORMAT "x(12)"
  FIELD fibu-ze     AS CHAR FORMAT "x(40)"
  FIELD addvat-value  AS DECIMAL
  . 

DEFINE TEMP-TABLE print-list 
  FIELD artnr       AS CHARACTER
  FIELD bezeich     AS CHARACTER
  FIELD qty         AS CHARACTER 
  FIELD warenwert   AS CHARACTER 
  FIELD price       AS CHARACTER
  FIELD munit       AS CHAR FORMAT "x(4)"
  FIELD fibu        AS CHAR FORMAT "x(12)"
  FIELD lscheinnr   AS CHAR
  FIELD fibu-ze     AS CHAR FORMAT "x(40)"
  FIELD addvat-value  AS DECIMAL
  .


DEF INPUT  PARAMETER pvILanguage    AS INT  NO-UNDO.
DEF INPUT  PARAMETER docu-nr        AS CHAR.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER po-nr          AS CHAR.
DEF INPUT  PARAMETER lief-nr        AS INT.
DEF INPUT  PARAMETER store          AS INT.
DEF INPUT  PARAMETER to-date        AS DATE. 
DEF OUTPUT PARAMETER show-price     AS LOGICAL.
DEF OUTPUT PARAMETER crterm         AS INTEGER INITIAL 0.
DEF OUTPUT PARAMETER d-purchase     AS LOGICAL.
DEF OUTPUT PARAMETER unit-price     AS DECIMAL INITIAL 0.
DEF OUTPUT PARAMETER l-lieferant-firma AS CHAR.
DEF OUTPUT PARAMETER avail-l-lager  AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER t-lager-nr     AS INT INITIAL 0.
DEF OUTPUT PARAMETER t-bezeich      AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR print-list.


RUN prepare-print-receiving-cldbl.p
    (pvILanguage, docu-nr, user-init, po-nr, lief-nr, store, to-date,
               OUTPUT show-price, OUTPUT crterm, OUTPUT d-purchase,
               OUTPUT unit-price, OUTPUT l-lieferant-firma, 
               OUTPUT avail-l-lager, OUTPUT t-lager-nr, OUTPUT t-bezeich,
               OUTPUT TABLE str-list).

FOR EACH str-list:
    CREATE print-list.
    ASSIGN 
        print-list.artnr = SUBSTRING(str-list.s,1,7)
        print-list.bezeich = SUBSTRING(str-list.s,8,24)
        print-list.price = SUBSTRING(str-list.s,32,15)
        print-list.qty = SUBSTRING(str-list.s,47,10)
        print-list.warenwert = SUBSTRING(str-list.s,57,15)
        print-list.lscheinnr = SUBSTRING(str-list.s,72,20)
        print-list.fibu = str-list.fibu
        print-list.munit = str-list.munit
        print-list.fibu-ze = str-list.fibu-ze
         print-list.addvat-value = str-list.addvat-value.
END.
