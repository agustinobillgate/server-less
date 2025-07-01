
DEFINE TEMP-TABLE t-nation          LIKE nation.
DEFINE INPUT  PARAMETER case-type   AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE       FOR t-nation.

CASE case-type :
    WHEN 1 THEN
    DO:
       FOR EACH nation NO-LOCK by nation.bezeich :
           CREATE t-nation.
           BUFFER-COPY nation TO t-nation.
       END.
    END.
END CASE.


