/*agung command make field
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
  
*/


DEFINE TEMP-TABLE str-list 
  FIELD artnr           AS CHAR 
  FIELD qty             AS DECIMAL FORMAT "->>>,>>>,>>9.99"
  FIELD warenwert       AS CHAR
  FIELD munit           AS CHAR FORMAT "x(4)"
  FIELD fibu            AS CHAR FORMAT "x(12)"
  FIELD fibu-ze         AS CHAR FORMAT "x(40)"
  FIELD addvat-value    AS DECIMAL
  FIELD bezeich         AS CHAR
  FIELD lscheinnr       AS CHAR
  FIELD unit-price      AS CHAR
  FIELD disc-amount     AS DECIMAL
  FIELD addvat-amount   AS DECIMAL
  FIELD disc-amount2    AS DECIMAL
  FIELD vat-amount      AS DECIMAL
  . 


DEFINE TEMP-TABLE print-list 
  FIELD artnr           AS CHAR
  FIELD bezeich         AS CHARACTER
  FIELD qty             AS DECIMAL 
  FIELD warenwert       AS CHAR
  FIELD price           AS CHAR
  FIELD munit           AS CHAR FORMAT "x(4)"
  FIELD fibu            AS CHAR FORMAT "x(12)"
  FIELD lscheinnr       AS CHAR
  FIELD fibu-ze         AS CHAR FORMAT "x(40)"
  FIELD addvat-value    AS DECIMAL
  FIELD disc-amount     AS DECIMAL
  FIELD addvat-amount   AS DECIMAL
  FIELD disc-amount2    AS DECIMAL
  FIELD vat-amount      AS DECIMAL
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

DEFINE VARIABLE curr-price AS DECIMAL.

/*ragung change to _1*/
/*FDL change to _2BL*/
RUN prepare-print-receiving-cld_2bl.p
    (pvILanguage, docu-nr, user-init, po-nr, lief-nr, store, to-date,
               OUTPUT show-price, OUTPUT crterm, OUTPUT d-purchase,
               OUTPUT unit-price, OUTPUT l-lieferant-firma, 
               OUTPUT avail-l-lager, OUTPUT t-lager-nr, OUTPUT t-bezeich,
               OUTPUT TABLE str-list).

FOR EACH str-list:
    CREATE print-list.
    ASSIGN 
        print-list.artnr = str-list.artnr
        print-list.bezeich = str-list.bezeich
        print-list.price = str-list.unit-price
        print-list.qty = str-list.qty
        print-list.warenwert = str-list.warenwert
        print-list.lscheinnr = str-list.lscheinnr
        print-list.fibu = str-list.fibu
        print-list.munit = str-list.munit
        print-list.fibu-ze = str-list.fibu-ze
        print-list.addvat-value = str-list.addvat-value.
    
    print-list.disc-amount = str-list.disc-amount.
    print-list.disc-amount2 = str-list.disc-amount2.
    print-list.addvat-amount = str-list.addvat-amount.
    print-list.vat-amount = str-list.vat-amount.

    IF str-list.disc-amount NE 0 THEN print-list.price = STRING(DEC(print-list.price) + str-list.disc-amount, "->>,>>>,>>>,>>9.99").
    /*IF str-list.disc-amount2 NE 0 THEN print-list.price = STRING(DEC(print-list.price) + str-list.disc-amount2, "->>,>>>,>>>,>>9.99").*/
    IF str-list.vat-amount NE 0 THEN print-list.price = STRING(DEC(print-list.price) - str-list.vat-amount, "->>,>>>,>>>,>>9.99" ).
END.


/* 
command agung 
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

*/
