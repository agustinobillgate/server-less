DEFINE TEMP-TABLE bk-list
    FIELD datum         LIKE bk-reser.datum
    FIELD raum          LIKE bk-rart.raum
    FIELD veran-artnr   LIKE bk-rart.veran-artnr
    FIELD bezeich       LIKE bk-rart.bezeich
    FIELD anzahl        LIKE bk-rart.anzahl
    FIELD preis         LIKE bk-rart.preis
    FIELD amount        AS DECIMAL 
    FIELD von-zeit      LIKE bk-reser.von-zeit
    FIELD bis-zeit      LIKE bk-reser.bis-zeit
    .

DEFINE INPUT PARAMETER veran-nr LIKE bk-reser.veran-nr.
DEFINE INPUT PARAMETER bill-date AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR bk-list.

FOR EACH bk-rart WHERE bk-rart.veran-nr = veran-nr
    AND bk-rart.fakturiert = 0 AND bk-rart.preis GT 0 NO-LOCK,
    FIRST bk-reser WHERE bk-reser.veran-nr = veran-nr
    AND bk-reser.veran-resnr = bk-rart.veran-resnr
    AND bk-reser.resstatus = 1 AND bk-reser.datum LE bill-date
    NO-LOCK BY bk-reser.datum:

    CREATE bk-list.
    BUFFER-COPY bk-rart TO bk-list.

END.
