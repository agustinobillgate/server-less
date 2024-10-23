DEFINE TEMP-TABLE str-list 
  FIELD docu-nr AS CHAR FORMAT "x(12)" 
  FIELD s AS CHAR FORMAT "x(135)" 
  FIELD dunit AS CHAR FORMAT "x(8)" 
  FIELD content AS INTEGER 
  FIELD lief-nr AS INTEGER 
  FIELD warenwert AS DECIMAL. 

DEFINE TEMP-TABLE po-list
    FIELD datum         AS DATE
    FIELD document-no   AS CHAR      FORMAT "x(12)"
    FIELD artno         AS INTEGER
    FIELD artdesc       AS CHARACTER FORMAT "x(30)"
    FIELD orderqty      AS INTEGER
    FIELD unit-price    AS DECIMAL   FORMAT "->,>>>,>>>,>>9.99"
    FIELD amount1       AS DECIMAL   FORMAT "->,>>>,>>>,>>9.99"
    FIELD delivered     AS INTEGER
    FIELD s-unit        AS INTEGER
    FIELD amount2       AS DECIMAL   FORMAT "->,>>>,>>>,>>9.99"
    FIELD delivdate     AS DATE
    FIELD supplier      AS CHARACTER FORMAT "x(30)"
    .

DEFiNE INPUT PARAMETER user-init AS CHAR.
DEFINE INPUT PARAMETER sorttype  AS INTEGER.
DEFINE INPUT PARAMETER s-artnr   AS INTEGER.
DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER to-date   AS DATE.
DEFINE INPUT PARAMETER from-sup  AS CHAR.
DEFINE INPUT PARAMETER to-sup    AS CHAR.
DEFINE INPUT PARAMETER closepo   AS LOGICAL NO-UNDO.

DEFINE OUTPUT PARAMETER TABLE FOR po-list.

DEF VAR delidate AS DATE FORMAT "99/99/99".

RUN sorder-list-btn-gobl.p(user-init, sorttype, s-artnr, 
                            from-date, to-date, from-sup, to-sup, closepo,
                            OUTPUT TABLE str-list).
FOR EACH po-list:
    DELETE po-list.
END.

FOR EACH str-list:
    IF str-list.s MATCHES "*T O T A L*" THEN 
    DO:
        CREATE po-list.
        ASSIGN 
            artdesc     = "T O T A L"
            amount1     = DECIMAL(TRIM(SUBSTR(str-list.s, 81, 15))).
    END.
    ELSE
    DO:
        delidate = DATE(TRIM(SUBSTR(str-list.s, 123, 8))).

        CREATE po-list.
        ASSIGN
            datum       = DATE(TRIM(SUBSTR(str-list.s, 1, 8)))
            document-no = TRIM(SUBSTR(str-list.s, 9, 12))   
            artno       = INT(TRIM(SUBSTR(str-list.s, 21, 7)))
            artdesc     = TRIM(SUBSTR(str-list.s, 28, 30))  
            orderqty    = INT(TRIM(SUBSTR(str-list.s, 58, 10)))
            unit-price  = DECIMAL(TRIM(SUBSTR(str-list.s, 68, 13)))
            amount1     = DECIMAL(TRIM(SUBSTR(str-list.s, 81, 15)))
            delivered   = INT(TRIM(SUBSTR(str-list.s, 96, 11)))
            s-unit      = INT(TRIM(SUBSTR(str-list.s, 106, 4)))
            amount2     = DECIMAL(TRIM(SUBSTR(str-list.s, 109, 15)))
            delivdate   = delidate
            supplier    = TRIM(SUBSTR(str-list.s, 131, 16))
            .
    END.
END.
