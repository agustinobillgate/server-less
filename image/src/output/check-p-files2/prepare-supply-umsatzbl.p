DEFINE TEMP-TABLE umsatz-list
    FIELD lief-nr       LIKE l-liefumsatz.lief-nr
    FIELD datum         LIKE l-liefumsatz.datum 
    FIELD gesamtumsatz  LIKE l-liefumsatz.gesamtumsatz.

DEFINE INPUT PARAMETER lief-nr      AS INTEGER  NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR umsatz-list.
    
FOR EACH l-liefumsatz WHERE l-liefumsatz.lief-nr = lief-nr 
    NO-LOCK BY l-liefumsatz.datum. 
    CREATE umsatz-list.
    BUFFER-COPY l-liefumsatz TO umsatz-list.
END.
