
DEFINE INPUT PARAMETER case-type AS INTEGER.
DEFINE INPUT PARAMETER int1      AS INTEGER.
DEFINE INPUT PARAMETER int2      AS INTEGER.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL.


CASE case-type:
    WHEN 1 THEN
    DO:
        FOR EACH nitestor WHERE nitestor.night-type = int1 
            AND nitestor.reihenfolge = int2 :
            DELETE nitestor.
            RELEASE nitestor.
            success-flag = YES.
        END.
    END.
END CASE.

