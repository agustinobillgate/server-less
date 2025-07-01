DEFINE TEMP-TABLE str-list
  FIELD flag AS INTEGER 
  FIELD s AS CHAR FORMAT "x(135)". 

DEFINE TEMP-TABLE soh-list
	FIELD artnr		AS INTEGER FORMAT "9999999"
    FIELD bezeich	AS CHARACTER
    FIELD unit     	AS CHARACTER
    FIELD act-qty  	AS DECIMAL FORMAT "->>,>>9.99"
    FIELD act-val  	AS DECIMAL  FORMAT "->>,>>>,>>9.99"
    FIELD cont1     AS CHARACTER
    FIELD d-unit    AS CHARACTER
    FIELD cont2     AS CHARACTER
    FIELD last-price AS DECIMAL FORMAT "->>>,>>>,>>9.99"
    FIELD act-price AS DECIMAL  FORMAT "->>>,>>>,>>9.99"
    FIELD avrg-price AS DECIMAL  FORMAT "->>>,>>>,>>9.99"
    .  

DEF INPUT  PARAMETER all-flag   AS LOGICAL.
DEF INPUT  PARAMETER show-price AS LOGICAL.
DEF INPUT  PARAMETER zero-flag  AS LOGICAL.
DEF INPUT  PARAMETER from-grp   AS INT.
DEF INPUT  PARAMETER sub-grp    AS INT.
DEF INPUT  PARAMETER from-lager AS INT.
DEF INPUT  PARAMETER to-lager   AS INT.
DEF INPUT  PARAMETER sorttype   AS INT.
DEF INPUT  PARAMETER mattype    AS INT.
DEF OUTPUT PARAMETER TABLE FOR soh-list.

/*    DEF VAR all-flag   AS LOGICAL INIT NO.
    DEF VAR show-price AS LOGICAL INIT YES.
    DEF VAR zero-flag  AS LOGICAL INIT NO.
    DEF VAR from-grp   AS INT INIT 0.
    DEF VAR sub-grp    AS INT INIT 0.
    DEF VAR from-lager AS INT INIT 1.      
    DEF VAR to-lager   AS INT INIT 1.
    DEF VAR sorttype   AS INT INIT 2.
    DEF VAR mattype    AS INT INIT 0.*/      

RUN sall-onhand-btn-gobl.p
    (all-flag, show-price, zero-flag, from-grp, sub-grp, from-lager, to-lager, sorttype, mattype, OUTPUT TABLE str-list).

FOR EACH soh-list:
    DELETE soh-list.
END.

FOR EACH str-list:
    CREATE soh-list.
    ASSIGN             
       soh-list.artnr      = INTEGER(SUBSTR(str-list.s, 1, 7))
       soh-list.bezeich    = SUBSTR(str-list.s, 8, 30)
       soh-list.unit       = SUBSTR(str-list.s, 38, 3)
       soh-list.act-qty    = DECIMAL(SUBSTR(str-list.s, 109, 13)) 
       soh-list.act-val    = DECIMAL(SUBSTR(str-list.s, 122, 15)) 
       soh-list.cont1      = SUBSTR(str-list.s, 41, 9)        
       soh-list.d-unit     = SUBSTR(str-list.s, 50, 8)         
       soh-list.cont2      = SUBSTR(str-list.s, 58, 9)        
       soh-list.last-price = DECIMAL(SUBSTR(str-list.s, 67, 14))
       soh-list.act-price  = DECIMAL(SUBSTR(str-list.s, 81, 14))
       soh-list.avrg-price = DECIMAL(SUBSTR(str-list.s, 95, 14))
       .
END.

/*FOR EACH soh-list:
    DISP soh-list.
END.*/

