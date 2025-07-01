DEF TEMP-TABLE q2-artikel
    FIELD artnr LIKE artikel.artnr
    FIELD bezeich LIKE artikel.bezeich
    FIELD epreis LIKE artikel.epreis
    FIELD anzahl LIKE artikel.anzahl.

DEF INPUT  PARAMETER departement AS INT.
DEF INPUT  PARAMETER sub-group   AS INT.
DEF OUTPUT PARAMETER TABLE FOR q2-artikel.

FOR EACH artikel WHERE artikel.departement = departement 
    AND artikel.zwkum = sub-group AND artikel.activeflag = YES
    USE-INDEX artart_ix NO-LOCK BY artikel.artnr:
    CREATE q2-artikel.
    ASSIGN
        q2-artikel.artnr = artikel.artnr
        q2-artikel.bezeich = artikel.bezeich
        q2-artikel.epreis = artikel.epreis
        q2-artikel.anzahl = artikel.anzahl.
END.
