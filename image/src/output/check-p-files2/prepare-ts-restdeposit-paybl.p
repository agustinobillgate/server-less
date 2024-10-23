
DEF TEMP-TABLE artikel-list
    FIELD artnr       LIKE artikel.artnr
    FIELD departement LIKE artikel.departement
    FIELD bezeich     LIKE artikel.bezeich
    FIELD artart      LIKE artikel.artart
    FIELD payment     AS DECIMAL
    FIELD pay-exrate  AS INTEGER.

DEFINE INPUT PARAMETER pvILanguage      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER selected-gastnr  AS INTEGER.
DEFINE INPUT PARAMETER sorttype         AS INTEGER.
DEFINE OUTPUT PARAMETER f-tittle        AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR artikel-list.

{SupertransBL.i}
DEFINE VARIABLE lvCAREA AS CHAR INITIAL "ts-rest-deposit-pay". 

DEFINE VARIABLE unallocated-subgrp  AS INTEGER NO-UNDO INIT 0.

RUN htpint.p(116, OUTPUT unallocated-subgrp).

f-tittle = translateExtended ("Restaurant Deposit Payment",lvCAREA,"").

FIND FIRST guest WHERE guest.gastnr EQ selected-gastnr NO-LOCK NO-ERROR.
IF AVAILABLE guest THEN
DO:
    f-tittle = f-tittle + "  -  " + guest.NAME + "," + guest.vorname1.
END.

RUN display-artikel.

PROCEDURE display-artikel: 
    IF sorttype = 1 THEN
    DO:
        FOR EACH artikel WHERE artikel.departement EQ 0 AND
            ((artikel.artart EQ 6 OR artikel.artart EQ 7)
            OR (artikel.artart EQ 2 AND (artikel.zwkum EQ unallocated-subgrp)))
            AND artikel.activeflag EQ YES
            NO-LOCK BY artikel.artnr:

            RUN assign-it.
        END.
    END.    
    ELSE
    FOR EACH artikel WHERE artikel.departement EQ 0 AND
        ((artikel.artart EQ 6 OR artikel.artart EQ 7)
        OR (artikel.artart EQ 2 AND (artikel.zwkum EQ unallocated-subgrp)))
        AND artikel.activeflag EQ YES
        NO-LOCK BY artikel.bezeich:

        RUN assign-it.
    END.
END PROCEDURE.

PROCEDURE assign-it:
    CREATE artikel-list.
    ASSIGN
        artikel-list.artnr          = artikel.artnr
        artikel-list.departement    = artikel.departement
        artikel-list.bezeich        = artikel.bezeich
        artikel-list.artart         = artikel.artart        
        artikel-list.pay-exrate     = 1
    .
END PROCEDURE.


