DEFINE TEMP-TABLE str-list
    FIELD l-bezeich AS CHAR FORMAT "x(24)" LABEL "Store Name" 
    FIELD STR AS CHAR. 

DEFINE TEMP-TABLE soh-list
	FIELD store		    AS INTEGER FORMAT "99"
    FIELD bezeich       AS CHAR FORMAT "x(24)"
    FIELD from-date	    AS CHAR
    FIELD init-stock    AS DECIMAL FORMAT "->>,>>9.99"
    FIELD init-value  	AS DECIMAL FORMAT "->>,>>9.99"
    FIELD in-qty  	    AS DECIMAL  FORMAT "->>>,>>>,>>9.99"
    FIELD in-amount     AS DECIMAL FORMAT "->>,>>9.99"
    FIELD out-qty       AS DECIMAL FORMAT "->>,>>9.99"
    FIELD out-amount    AS DECIMAL FORMAT "->>,>>9.99"
    FIELD adjustment    AS DECIMAL FORMAT "->>,>>9.99"
    FIELD end-qty       AS DECIMAL  FORMAT "->>,>>9.99"
    FIELD end-value     AS DECIMAL  FORMAT "->>>,>>>,>>9.99"
    .  

DEF INPUT  PARAMETER s-artnr    AS INT.
DEF OUTPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER artnr AS INT.
DEF OUTPUT PARAMETER bezeich AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR soh-list.

/*DEF VAR s-artnr         AS INT INIT 1101001.      
DEF VAR price-decimal   AS DEC.      
DEF VAR artnr           AS INT.      
DEF VAR bezeich         AS CHAR.*/      

RUN prepare-stock-onhandbl.p
    (s-artnr, OUTPUT price-decimal, OUTPUT artnr, OUTPUT bezeich, OUTPUT TABLE str-list).

FOR EACH soh-list:
    DELETE soh-list.
END.

FOR EACH str-list:
    CREATE soh-list.
    ASSIGN             
       soh-list.store      = INTEGER(SUBSTR(str-list.s, 1, 2))
       soh-list.bezeich    = str-list.l-bezeich
       soh-list.from-date  = SUBSTR(str-list.s, 3, 8)
       soh-list.init-stock = DECIMAL(SUBSTR(str-list.s, 11, 13))
       soh-list.init-value = DECIMAL(SUBSTR(str-list.s, 24, 14)) 
       soh-list.in-qty     = DECIMAL(SUBSTR(str-list.s, 38, 13)) 
       soh-list.in-amount  = DECIMAL(SUBSTR(str-list.s, 51, 14))        
       soh-list.out-qty    = DECIMAL(SUBSTR(str-list.s, 65, 13))         
       soh-list.out-amount = DECIMAL(SUBSTR(str-list.s, 78, 14))        
       soh-list.adjustment = DECIMAL(SUBSTR(str-list.s, 92, 13))
       soh-list.end-qty    = DECIMAL(SUBSTR(str-list.s, 105, 13))
       soh-list.end-value  = DECIMAL(SUBSTR(str-list.s, 118, 14))
       .
END.

/*FOR EACH soh-list:
    DISP soh-list.
END.*/
