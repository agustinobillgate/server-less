DEFINE TEMP-TABLE t-prmarket    LIKE prmarket.

DEFINE INPUT PARAMETER case-type        AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-prmarket.


CASE case-type :
    WHEN 1 THEN
    DO:
        FOR EACH prmarket NO-LOCK :
            CREATE t-prmarket.
            BUFFER-COPY prmarket TO t-prmarket.
        END.
    END.
END CASE.

