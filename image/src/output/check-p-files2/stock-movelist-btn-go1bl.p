DEFINE TEMP-TABLE str-list 
  FIELD s AS CHAR FORMAT "x(135)"
  FIELD ID  AS CHAR FORMAT "x(4)"
  FIELD m-unit AS CHAR FORMAT "x(7)"
  . 

DEFINE TEMP-TABLE stock-movelist
    FIELD datum     AS DATE
    FIELD lscheinnr AS CHARACTER
    FIELD init-qty  AS DECIMAL FORMAT "->>>,>>9.99"
    FIELD init-val  AS DECIMAL  FORMAT ">,>>>,>>>,>>9.99"
    FIELD in-qty    AS DECIMAL FORMAT "->>>,>>9.99"
    FIELD in-val    AS DECIMAL  FORMAT ">,>>>,>>>,>>9.99"
    FIELD out-qty   AS DECIMAL FORMAT "->>>,>>9.99"
    FIELD out-val   AS DECIMAL  FORMAT ">,>>>,>>>,>>9.99"
    FIELD note      AS CHARACTER
    FIELD id        AS CHARACTER
    .  

DEF INPUT PARAMETER pvILanguage AS INT.
DEF INPUT PARAMETER s-artnr AS INT.
DEF INPUT PARAMETER show-price AS LOGICAL.
DEF INPUT PARAMETER from-lager AS INT.
DEF INPUT PARAMETER to-lager AS INT.
DEF OUTPUT PARAMETER TABLE FOR stock-movelist.

/*    DEF VAR pvILanguage AS INT INIT 1.
    DEF VAR s-artnr AS INT INIT 3312036.
    DEF VAR show-price AS LOGICAL INIT YES.
    DEF VAR from-lager AS INT INIT 1.
    DEF VAR to-lager AS INT INIT 99.*/

RUN stock-movelist-btn-gobl.p
    (pvILanguage, s-artnr, show-price, from-lager, to-lager, OUTPUT TABLE str-list).

FOR EACH stock-movelist:
    DELETE stock-movelist.
END.

FOR EACH str-list:
    CREATE stock-movelist.
    ASSIGN             
       stock-movelist.datum        = DATE(SUBSTRING(s,1,8))
       stock-movelist.lscheinnr    = SUBSTRING(s,9,16)
       stock-movelist.init-qty     = DECIMAL(SUBSTRING(s,25,11))
       stock-movelist.init-val     = DECIMAL(SUBSTRING(s,36,15)) 
       stock-movelist.in-qty       = DECIMAL(SUBSTRING(s,51,13)) 
       stock-movelist.in-val       = DECIMAL(SUBSTRING(s,64,14))        
       stock-movelist.out-qty      = DECIMAL(SUBSTRING(s,78,13))         
       stock-movelist.out-val      = DECIMAL(SUBSTRING(s,91,14))        
       stock-movelist.note         = SUBSTRING(s,116,13)
       stock-movelist.id           = str-list.id
     .
END.

/*FOR EACH stock-movelist:
    DISP stock-movelist.
END.*/

