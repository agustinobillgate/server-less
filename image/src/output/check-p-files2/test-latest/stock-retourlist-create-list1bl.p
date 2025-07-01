DEFINE TEMP-TABLE str-list 
  FIELD s AS CHAR FORMAT "x(147)". 

DEFINE TEMP-TABLE stock-retour-list
    FIELD datum     AS DATE FORMAT "99/99/9999"
    FIELD lief      AS CHARACTER
    FIELD art       AS CHARACTER
    FIELD bezeich   AS CHARACTER
    FIELD qty       AS DECIMAL FORMAT "->>>,>>9.99"     
    FIELD epreis    AS DECIMAL FORMAT ">,>>>,>>>,>>9.99"
    FIELD amount    AS DECIMAL FORMAT ">,>>>,>>>,>>9.99"
    FIELD reason    AS CHARACTER
    FIELD id        AS CHARACTER
    FIELD dlvnote   AS CHARACTER
    FIELD lager     AS CHARACTER
    .  

DEF INPUT PARAMETER from-date   AS DATE.
DEF INPUT PARAMETER to-date     AS DATE.
DEF INPUT PARAMETER from-supp    AS CHAR.
DEF INPUT PARAMETER to-supp      AS CHAR.
DEF INPUT PARAMETER show-price  AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR stock-retour-list.

/*DEF VAR from-date   AS DATE INIT 1/1/19.
DEF VAR to-date     AS DATE INIT 12/31/19.
DEF VAR from-supp   AS CHAR INIT "Anna".
DEF VAR to-supp     AS CHAR INIT "Anna".
DEF VAR show-price  AS LOGICAL INIT YES.*/

RUN stock-retourlist-create-listbl.p (from-date, to-date, from-supp, to-supp, show-price, OUTPUT TABLE str-list).

FOR EACH stock-retour-list:
    DELETE stock-retour-list.
END.

FOR EACH str-list:
    CREATE stock-retour-list.

    ASSIGN
        stock-retour-list.datum    =   DATE(SUBSTR(str-list.s, 1,  8))
        stock-retour-list.lief     =   SUBSTR(str-list.s, 9, 24) 
        stock-retour-list.art      =   SUBSTR(str-list.s, 33,  7) 
        stock-retour-list.bezeich  =   SUBSTR(str-list.s, 40, 36) 
        stock-retour-list.qty      =   DECIMAL(SUBSTR(str-list.s, 76, 10))
        stock-retour-list.epreis   =   DECIMAL(SUBSTR(str-list.s,86, 13))
        stock-retour-list.amount   =   DECIMAL(SUBSTR(str-list.s, 99, 13))
        stock-retour-list.reason   =   SUBSTR(str-list.s, 112, 16)
        stock-retour-list.id       =   SUBSTR(str-list.s, 128, 2)
        stock-retour-list.dlvnote  =   SUBSTR(str-list.s, 130, 20)
        stock-retour-list.lager    =   SUBSTR(str-list.s, 150,  2)  
        .
END.

/*FOR EACH stock-retour-list:
    DISP stock-retour-list.
END.*/

