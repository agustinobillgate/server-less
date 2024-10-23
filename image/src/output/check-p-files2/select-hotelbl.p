
DEFINE TEMP-TABLE b1-list
    FIELD aktionscode   LIKE akt-code.aktionscode
    FIELD bezeich       LIKE akt-code.bezeich
    FIELD bemerkung     LIKE akt-code.bemerkung.


DEFINE OUTPUT PARAMETER TABLE  FOR b1-list.

FOR EACH akt-code WHERE akt-code.aktiongrup = 4 NO-LOCK BY 
    akt-code.aktionscode:
    CREATE b1-list.
    ASSIGN
      b1-list.aktionscode   = akt-code.aktionscode
      b1-list.bezeich       = akt-code.bezeich
      b1-list.bemerkung     = akt-code.bemerkung.
END.
