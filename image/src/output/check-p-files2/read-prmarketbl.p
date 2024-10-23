
DEF TEMP-TABLE t-prmarket    LIKE prmarket.

DEFINE INPUT PARAMETER case-type        AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER prNo             AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER bezeich          AS CHAR     NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR t-prmarket.

CASE case-type :
    WHEN 1 THEN
        FIND FIRST prmarket WHERE prmarket.nr = prNo NO-LOCK NO-ERROR.
    WHEN 2 THEN
        FIND FIRST prmarket WHERE prmarket.bezeich = bezeich NO-LOCK NO-ERROR.
    WHEN 3 THEN
        FIND FIRST prmarket WHERE prmarket.bezeich = bezeich 
        AND RECID(prmarket) NE prNo NO-LOCK NO-ERROR.
END CASE.

IF AVAILABLE prmarket THEN
DO:
  CREATE t-prmarket.
  BUFFER-COPY prmarket TO t-prmarket.
END.

