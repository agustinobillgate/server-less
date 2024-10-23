DEFINE TEMP-TABLE user-list
    FIELD rec-id    AS INTEGER
    FIELD dept      AS INTEGER
    FIELD depart    AS CHARACTER
    FIELD usrnr     AS INTEGER
    FIELD usrname   AS CHARACTER.

DEFINE OUTPUT PARAMETER p-110 AS DATE.
DEFINE OUTPUT PARAMETER dstore-dept AS INTEGER.
DEFINE OUTPUT PARAMETER ekumnr AS INTEGER.
DEFINE OUTPUT PARAMETER zknr1 AS INTEGER. 
DEFINE OUTPUT PARAMETER zknr2 AS INTEGER. 
DEFINE OUTPUT PARAMETER zknr3 AS INTEGER. 
DEFINE OUTPUT PARAMETER zknr4 AS INTEGER. 
DEFINE OUTPUT PARAMETER zknr5 AS INTEGER. 
DEFINE OUTPUT PARAMETER zknr6 AS INTEGER.
DEFINE OUTPUT PARAMETER bezeich1 AS CHAR FORMAT "x(12)". 
DEFINE OUTPUT PARAMETER bezeich2 AS CHAR FORMAT "x(12)". 
DEFINE OUTPUT PARAMETER bezeich3 AS CHAR FORMAT "x(12)". 
DEFINE OUTPUT PARAMETER bezeich4 AS CHAR FORMAT "x(12)". 
DEFINE OUTPUT PARAMETER bezeich5 AS CHAR FORMAT "x(12)". 
DEFINE OUTPUT PARAMETER bezeich6 AS CHAR FORMAT "x(12)".
DEFINE OUTPUT PARAMETER TABLE FOR user-list.


FIND FIRST htparam WHERE paramnr = 110 no-lock.  /*Invoicing DATE */ 
p-110 = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 1082 no-lock.  /* Drugstore Dept*/ 
dstore-dept = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  

FIND FIRST htparam WHERE paramnr = 555 NO-LOCK. 
ekumnr = htparam.finteger. 

FOR EACH kellner WHERE kellner.departement = dstore-dept NO-LOCK, 
    FIRST hoteldpt WHERE hoteldpt.num = kellner.departement 
    NO-LOCK BY kellner.kellner-nr. 
    CREATE user-list.
    ASSIGN
        user-list.rec-id    = RECID(kellner)
        user-list.dept      = kellner.departement
        user-list.depart    = hoteldpt.depart
        user-list.usrnr     = kellner.kellner-nr
        user-list.usrname   = kellner.kellnername.
END.

FOR EACH h-artikel WHERE h-artikel.departement = dstore-dept 
    AND h-artikel.artart = 0 NO-LOCK BY h-artikel.zwkum: 
    IF zknr1 = 0 THEN 
    DO: 
        zknr1 = h-artikel.zwkum. 
        FIND FIRST wgrpdep WHERE wgrpdep.departement = dstore-dept 
            AND wgrpdep.zknr = h-artikel.zwkum NO-LOCK. 
        bezeich1 = wgrpdep.bezeich. 
    END. 
    ELSE IF h-artikel.zwkum NE zknr1 AND zknr2 = 0 THEN 
    DO: 
        zknr2 = h-artikel.zwkum. 
        FIND FIRST wgrpdep WHERE wgrpdep.departement = dstore-dept 
            AND wgrpdep.zknr = h-artikel.zwkum NO-LOCK. 
        bezeich2 = wgrpdep.bezeich. 
    END. 
    ELSE IF h-artikel.zwkum NE zknr1 
        AND h-artikel.zwkum NE zknr2 AND zknr3 = 0 THEN 
    DO: 
        zknr3 = h-artikel.zwkum. 
        FIND FIRST wgrpdep WHERE wgrpdep.departement = dstore-dept 
            AND wgrpdep.zknr = h-artikel.zwkum NO-LOCK. 
        bezeich3 = wgrpdep.bezeich. 
    END. 
    ELSE IF h-artikel.zwkum NE zknr1 
        AND h-artikel.zwkum NE zknr2 
        AND h-artikel.zwkum NE zknr3 
        AND zknr4 = 0 THEN 
    DO: 
        zknr4 = h-artikel.zwkum. 
        FIND FIRST wgrpdep WHERE wgrpdep.departement = dstore-dept 
            AND wgrpdep.zknr = h-artikel.zwkum NO-LOCK. 
        bezeich4 = wgrpdep.bezeich. 
    END. 
    ELSE IF h-artikel.zwkum NE zknr1 
        AND h-artikel.zwkum NE zknr2 
        AND h-artikel.zwkum NE zknr3 
        AND h-artikel.zwkum NE zknr4 
        AND zknr5 = 0 THEN 
    DO: 
        zknr5 = h-artikel.zwkum. 
        FIND FIRST wgrpdep WHERE wgrpdep.departement = dstore-dept 
            AND wgrpdep.zknr = h-artikel.zwkum NO-LOCK. 
        bezeich5 = wgrpdep.bezeich. 
    END. 
    ELSE IF h-artikel.zwkum NE zknr1 
        AND h-artikel.zwkum NE zknr2 
        AND h-artikel.zwkum NE zknr3 
        AND h-artikel.zwkum NE zknr4 
        AND h-artikel.zwkum NE zknr5 
        AND zknr6 = 0 THEN 
    DO: 
        zknr6 = h-artikel.zwkum. 
        FIND FIRST wgrpdep WHERE wgrpdep.departement = dstore-dept 
            AND wgrpdep.zknr = h-artikel.zwkum NO-LOCK. 
        bezeich6 = wgrpdep.bezeich. 
    END. 
END. 
