DEFINE TEMP-TABLE t-cl-member LIKE cl-member.

DEFINE INPUT PARAMETER case-type AS INTEGER.
DEFINE INPUT PARAMETER gastNo    AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-cl-member.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST cl-member WHERE cl-member.gastnr = gastNo 
            NO-LOCK NO-ERROR.
        IF AVAILABLE cl-member THEN
        DO:
            CREATE t-cl-member.
            BUFFER-COPY cl-member TO t-cl-member.
        END.
    END.
END CASE.
