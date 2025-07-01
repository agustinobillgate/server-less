DEFINE TEMP-TABLE bkrart LIKE bk-rart
    FIELD recid-bk-rart AS INT
    FIELD amount AS DECIMAL.

DEF INPUT  PARAMETER veran-nr           AS INT.
DEF INPUT  PARAMETER veran-seite        AS INT.
DEF INPUT  PARAMETER sub-group          AS INT.
DEF OUTPUT PARAMETER TABLE FOR bkrart.

FOR EACH bkrart:
    DELETE bkrart.
END.

FOR EACH bk-rart WHERE bk-rart.veran-nr = veran-nr 
    AND bk-rart.veran-seite = veran-seite 
    AND bk-rart.zwkum = sub-group NO-LOCK:        
    CREATE bkrart.
    ASSIGN
        bkrart.veran-nr         = bk-rart.veran-nr
        bkrart.veran-resnr      = bk-rart.veran-resnr
        bkrart.veran-seite      = bk-rart.veran-seite
        bkrart.zwkum            = bk-rart.zwkum
        bkrart.veran-artnr      = bk-rart.veran-artnr
        bkrart.bezeich          = bk-rart.bezeich
        bkrart.anzahl           = bk-rart.anzahl
        bkrart.preis            = bk-rart.preis
        bkrart.amount           = (bk-rart.anzahl * bk-rart.preis)
        bkrart.departement      = bk-rart.departement
        bkrart.fakturiert       = bk-rart.fakturiert
        bkrart.setup-id         = bk-rart.setup-id
        bkrart.recid-bk-rart    = RECID(bk-rart)
        bkrart.von-zeit         = bk-rart.von-zeit /*ITA 010714*/
        bkrart.raum             = bk-rart.raum
        bkrart.resstatus        = bk-rart.resstatus.
END.
