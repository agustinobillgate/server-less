DEFINE TEMP-TABLE bkrart LIKE bk-rart
    FIELD recid-bk-rart AS INT
    FIELD amount AS DECIMAL.

DEF INPUT  PARAMETER veran-nr           AS INT.
DEF INPUT  PARAMETER veran-seite        AS INT.
DEF INPUT  PARAMETER sub-group          AS INT.
DEF INPUT  PARAMETER TABLE FOR bkrart.

FOR EACH bk-rart WHERE bk-rart.veran-nr = veran-nr 
    AND bk-rart.veran-seite = veran-seite 
    AND bk-rart.zwkum = sub-group:
    DELETE bk-rart.
END.

FOR EACH bkrart WHERE bkrart.veran-nr = veran-nr AND bkrart.veran-seite = veran-seite 
    AND bkrart.zwkum = sub-group NO-LOCK:
    CREATE bk-rart.
    ASSIGN
        bk-rart.veran-nr         = bkrart.veran-nr
        bk-rart.veran-resnr      = bkrart.veran-resnr
        bk-rart.veran-seite      = bkrart.veran-seite
        bk-rart.zwkum            = bkrart.zwkum
        bk-rart.veran-artnr      = bkrart.veran-artnr
        bk-rart.bezeich          = bkrart.bezeich
        bk-rart.anzahl           = bkrart.anzahl
        bk-rart.preis            = bkrart.preis
        bk-rart.departement      = bkrart.departement
        bk-rart.fakturiert       = bkrart.fakturiert
        bk-rart.setup-id         = bkrart.setup-id
        bkrart.recid-bk-rart     = RECID(bk-rart)
        bk-rart.von-zeit         = bkrart.von-zeit /*ITA 010714*/
        bk-rart.raum             = bkrart.raum
        bk-rart.resstatus        = bkrart.resstatus .
END.
