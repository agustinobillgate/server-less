DEFINE TEMP-TABLE t-nebenst LIKE nebenst
    FIELD n-id AS INT.
DEFINE INPUT PARAMETER case-type        AS INTEGER. 
DEFINE INPUT PARAMETER finRoom          AS CHAR. 
DEFINE INPUT PARAMETER rechNo           AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-nebenst.

CASE case-type:
  WHEN 1 THEN
  DO:
      FIND FIRST nebenst WHERE nebenst.zinr = finRoom 
          AND nebenst.nebst-type  = 3 NO-LOCK NO-ERROR.
  END.
  WHEN 2 THEN
  DO:
      FIND FIRST nebenst WHERE nebenst.zinr = finRoom
          AND nebenst.rechnr = rechNo NO-LOCK NO-ERROR. 
  END.
  WHEN 3 THEN
  DO:
      FIND FIRST nebenst WHERE nebenst.nebenstelle = finRoom NO-LOCK NO-ERROR. 
  END.
  WHEN 4 THEN
  DO:
      FIND FIRST nebenst WHERE nebenst.nebenstelle = finRoom 
          AND RECID(nebenst) NE rechNo NO-LOCK NO-ERROR. 
  END.
  WHEN 5 THEN
  DO:
      FIND FIRST nebenst WHERE nebenst.nebenstelle = finRoom
          AND nebenst.nebst-type = rechNo NO-LOCK NO-ERROR. 
  END.
END CASE.

IF AVAILABLE nebenst THEN
DO:
    CREATE t-nebenst.
    BUFFER-COPY nebenst TO t-nebenst.
    t-nebenst.n-id = RECID(nebenst).
END.
