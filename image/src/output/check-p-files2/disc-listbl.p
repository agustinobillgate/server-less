
DEFINE TEMP-TABLE disc-list
    FIELD flag          AS CHARACTER
    FIELD dept-no       AS CHARACTER    FORMAT "x(2)"
    FIELD dept-name     AS CHARACTER    FORMAT "x(24)"
    FIELD artnr         AS CHARACTER    FORMAT "x(4)"
    FIELD day-disc      AS CHARACTER    FORMAT "x(14)" 
    FIELD day-percent   AS CHARACTER    FORMAT "x(7)" 
    FIELD mtd-disc      AS CHARACTER    FORMAT "x(15)" 
    FIELD mtd-percent   AS CHARACTER    FORMAT "x(7)" 
    FIELD ytd-disc      AS CHARACTER    FORMAT "x(15)"
    FIELD ytd-percent   AS CHARACTER    FORMAT "x(7)" 
    .

DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR disc-list.

DEFINE VARIABLE ekumnr      AS INTEGER  NO-UNDO. 
DEFINE VARIABLE mm          AS INTEGER  NO-UNDO.
DEFINE VARIABLE from-date   AS DATE     NO-UNDO INITIAL ?.
DEFINE VARIABLE i           AS INTEGER  NO-UNDO. 
DEFINE VARIABLE dnet        AS DECIMAL  NO-UNDO FORMAT "->>,>>>,>>9.99". 
DEFINE VARIABLE mnet        AS DECIMAL  NO-UNDO FORMAT "->>>,>>>,>>9.99". 
DEFINE VARIABLE ynet        AS DECIMAL  NO-UNDO FORMAT "->>>,>>>,>>9.99". 

DEFINE WORKFILE art-list 
    FIELD artnr      AS INTEGER 
    FIELD dept       AS INTEGER 
    FIELD name       AS CHARACTER FORMAT "x(16)". 

DEFINE TEMP-TABLE disc-list1
    FIELD flag          AS CHARACTER    
    FIELD dept-no       AS INTEGER      FORMAT ">9"
    FIELD dept-name     AS CHARACTER    FORMAT "x(24)"
    FIELD artnr         AS INTEGER      FORMAT ">>>>"
    FIELD day-disc      AS DECIMAL      FORMAT "->,>>>,>>>,>>9" INITIAL 0 
    FIELD day-percent   AS DECIMAL      FORMAT "->>9.99" INITIAL 0 
    FIELD mtd-disc      AS DECIMAL      FORMAT "->>,>>>,>>>,>>9" INITIAL 0 
    FIELD mtd-percent   AS DECIMAL      FORMAT "->>9.99" INITIAL 0
    FIELD ytd-disc      AS DECIMAL      FORMAT "->>,>>>,>>>,>>9" INITIAL 0 
    FIELD ytd-percent   AS DECIMAL      FORMAT "->>9.99" INITIAL 0
    .

FIND FIRST htparam WHERE paramnr = 555 NO-LOCK. 
ekumnr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FOR EACH hoteldpt NO-LOCK: 
    FOR EACH artikel WHERE artikel.departement = hoteldpt.num 
        AND artikel.artart = 0 AND artikel.endkum = ekumnr 
        USE-INDEX artart_ix NO-LOCK: 
        CREATE art-list. 
        ASSIGN  art-list.artnr = artikel.artnr
                art-list.dept = artikel.departement
                art-list.name = hoteldpt.depart
                .
    END. 
END. 


dnet = 0. 
mnet = 0. 
ynet = 0. 
mm = month(to-date). 
from-date = DATE(1, 1, YEAR(to-date)). 
 
FOR EACH disc-list: 
    DELETE disc-list. 
END. 

FOR EACH disc-list1: 
    DELETE disc-list1. 
END. 

FOR EACH art-list NO-LOCK: 
    CREATE disc-list1. 
    ASSIGN  disc-list1.artnr     = art-list.artnr
            disc-list1.dept-no   = art-list.dept
            disc-list1.dept-name = art-list.name
        . 
    
    FOR EACH umsatz WHERE umsatz.artnr = art-list.artnr 
        AND umsatz.departement = art-list.dept 
        AND umsatz.datum GE from-date AND umsatz.datum LE to-date 
        USE-INDEX umsatz_index NO-LOCK: 
        IF umsatz.datum = to-date THEN 
        DO: 
            disc-list1.day-disc =  - umsatz.betrag. 
            dnet = dnet - umsatz.betrag.                /*wenni 29/11/16*/
        END. 
        IF month(umsatz.datum) = mm THEN 
        DO: 
            disc-list1.mtd-disc = disc-list1.mtd-disc - umsatz.betrag. 
            mnet = mnet - umsatz.betrag. 
        END. 
        disc-list1.ytd-disc = disc-list1.ytd-disc - umsatz.betrag. 
        ynet = ynet - umsatz.betrag. 
    END. 
END. 

FOR EACH disc-list1: 
    IF dnet NE 0 THEN disc-list1.day-percent = disc-list1.day-disc / dnet * 100. 
    IF mnet NE 0 THEN disc-list1.mtd-percent = disc-list1.mtd-disc / mnet * 100. 
    IF ynet NE 0 THEN disc-list1.ytd-percent = disc-list1.ytd-disc / ynet * 100. 
END. 

CREATE disc-list1. 
disc-list1.flag = "*". 

CREATE disc-list1. 
disc-list1.flag = "**". 
disc-list1.dept-name = "T O T A L". 
disc-list1.day-disc = dnet. 
IF dnet NE 0 THEN disc-list1.day-percent = 100. 
disc-list1.mtd-disc = mnet. 
IF mnet NE 0 THEN disc-list1.mtd-percent = 100. 
disc-list1.ytd-disc = ynet. 
IF ynet NE 0 THEN disc-list1.ytd-percent = 100. 

FOR EACH disc-list1 NO-LOCK : 
    CREATE disc-list. 
    disc-list.flag = disc-list1.flag. 
    IF disc-list1.flag = "*" THEN 
        ASSIGN  disc-list.dept-no     = FILL("-", 2)
                disc-list.dept-name   = FILL("-", 24)
                disc-list.artnr       = FILL("-", 4)
                disc-list.day-disc    = FILL("-", 14)
                disc-list.day-percent = FILL("-", 7) 
                disc-list.mtd-disc    = FILL("-", 15)
                disc-list.mtd-percent = FILL("-", 7) 
                disc-list.ytd-disc    = FILL("-", 15) 
                disc-list.ytd-percent = FILL("-", 7) 
        .
    ELSE 
    DO: 
        IF disc-list1.flag = "**" THEN disc-list.dept-no = STRING(disc-list1.dept-no, ">>"). 
        ELSE disc-list.dept-no = STRING(disc-list1.dept-no, ">9"). 
             
        ASSIGN  disc-list.dept-name   = STRING(disc-list1.dept-name, "x(24)") 
                disc-list.artnr       = STRING(disc-list1.artnr, ">>>>") 
                disc-list.day-disc    = STRING(disc-list1.day-disc, "->>,>>>>>,>>9") 
                disc-list.day-percent = STRING(disc-list1.day-percent, "->>9.9") 
                disc-list.mtd-disc    = STRING(disc-list1.mtd-disc, "->>,>>>,>>>,>>9") 
                disc-list.mtd-percent = STRING(disc-list1.mtd-percent, "->>9.9") 
                disc-list.ytd-disc    = STRING(disc-list1.ytd-disc, "->>,>>>,>>>,>>9") 
                disc-list.ytd-percent = STRING(disc-list1.ytd-percent, "->>9.9") 
                . 
    END. 
END. 
