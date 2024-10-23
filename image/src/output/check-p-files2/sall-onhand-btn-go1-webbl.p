DEFINE TEMP-TABLE str-list
  FIELD flag AS INTEGER 
  FIELD s AS CHAR FORMAT "x(135)". 

DEFINE TEMP-TABLE soh-list
	FIELD artnr		    AS INTEGER FORMAT "9999999"
    FIELD bezeich	    AS CHARACTER
    FIELD unit     	    AS CHARACTER
    FIELD act-qty  	    AS DECIMAL FORMAT "->>,>>9.99"
    FIELD act-val  	    AS DECIMAL  FORMAT "->>,>>>,>>9.99"
    FIELD cont1         AS CHARACTER
    FIELD d-unit        AS CHARACTER
    FIELD cont2         AS CHARACTER
    FIELD last-price    AS DECIMAL FORMAT "->>>,>>>,>>9.99"
    FIELD act-price     AS DECIMAL  FORMAT "->>>,>>>,>>9.99"
    FIELD avrg-price    AS DECIMAL  FORMAT "->>>,>>>,>>9.99"
    FIELD min-oh        AS DECIMAL
    FIELD must-order    AS DECIMAL
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
DEF INPUT  PARAMETER minoh-flag AS LOGICAL. /*FDL Dec 20, 2022 => 272C59*/
DEF OUTPUT PARAMETER TABLE FOR soh-list.

/* Local Testing 
DEF VAR all-flag   AS LOGICAL INIT NO.
DEF VAR show-price AS LOGICAL INIT YES.
DEF VAR zero-flag  AS LOGICAL INIT NO.
DEF VAR from-grp   AS INT INIT 0.
DEF VAR sub-grp    AS INT INIT 0.
DEF VAR from-lager AS INT INIT 1.      
DEF VAR to-lager   AS INT INIT 1.
DEF VAR sorttype   AS INT INIT 2.
DEF VAR mattype    AS INT INIT 0.
DEF VAR minoh-flag  AS LOGICAL INIT NO.
*/      
/* FD Comment
RUN sall-onhand-btn-gobl.p
    (all-flag, show-price, zero-flag, from-grp, sub-grp, from-lager, to-lager, sorttype, mattype, OUTPUT TABLE str-list).
*/

RUN sall-onhand-btn-go_1bl.p
    (all-flag, show-price, zero-flag, from-grp, sub-grp, 
     from-lager, to-lager, sorttype, mattype, minoh-flag,
     OUTPUT TABLE str-list).

FOR EACH soh-list:
    DELETE soh-list.
END.

FOR EACH str-list:
    CREATE soh-list.
    ASSIGN             
        soh-list.artnr      = INTEGER(SUBSTR(str-list.s, 1, 7))
        soh-list.bezeich    = SUBSTR(str-list.s, 8, 50)
        soh-list.unit       = SUBSTR(str-list.s, 58, 3)
        soh-list.act-qty    = DECIMAL(SUBSTR(str-list.s, 129, 13)) 
        soh-list.act-val    = DECIMAL(SUBSTR(str-list.s, 142, 18)) 
        soh-list.cont1      = SUBSTR(str-list.s, 61, 9)        
        soh-list.d-unit     = SUBSTR(str-list.s, 70, 8)         
        soh-list.cont2      = SUBSTR(str-list.s, 78, 9)        
        soh-list.last-price = DECIMAL(SUBSTR(str-list.s, 87, 14))
        soh-list.act-price  = DECIMAL(SUBSTR(str-list.s, 101, 14))
        soh-list.avrg-price = DECIMAL(SUBSTR(str-list.s, 115, 14))
        soh-list.min-oh     = DECIMAL(SUBSTR(str-list.s, 160, 13))
        soh-list.must-order = DECIMAL(SUBSTR(str-list.s, 173, 13))
        .
END.

/*FOR EACH soh-list:
    DISP soh-list.
END.*/

