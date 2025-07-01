/*FT 230714 filter yang sama*/
DEFINE TEMP-TABLE szwkum-list
    FIELD zwkum     LIKE l-untergrup.zwkum 
    FIELD bezeich   LIKE l-untergrup.bezeich.
    
DEFINE INPUT PARAMETER main-nr      AS INT  NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR szwkum-list.

IF main-nr = 0 THEN
DO:
  FOR EACH l-untergrup NO-LOCK:
      CREATE szwkum-list.
      BUFFER-COPY l-untergrup TO szwkum-list.
  END.
END.
ELSE
DO:
  FOR EACH queasy WHERE queasy.KEY = 29 AND queasy.number1 = main-nr NO-LOCK
      BY queasy.number2:
    FIND FIRST l-untergrup WHERE l-untergrup.zwkum = queasy.number2
        NO-LOCK NO-ERROR.
    IF AVAILABLE l-untergrup THEN
    DO:
      /*FT 230714*/
      FIND FIRST szwkum-list WHERE szwkum-list.zwkum = l-untergrup.zwkum NO-LOCK NO-ERROR.
      IF NOT AVAILABLE szwkum-list THEN
      DO:
        CREATE szwkum-list.
        BUFFER-COPY l-untergrup TO szwkum-list.

      END.
    END.
  END.
  FOR EACH l-untergrup NO-LOCK BY l-untergrup.zwkum:
    FIND FIRST queasy WHERE queasy.KEY = 29 
      AND queasy.number2 = l-untergrup.zwkum NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
      CREATE szwkum-list.
      BUFFER-COPY l-untergrup TO szwkum-list.
    END.
  END.
END.
