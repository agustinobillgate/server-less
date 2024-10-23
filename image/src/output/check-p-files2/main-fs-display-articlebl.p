
DEFINE TEMP-TABLE ol 
    FIELD STR AS CHAR FORMAT "x(120)". 

DEFINE TEMP-TABLE bkrart LIKE bk-rart
    FIELD tischform   AS CHAR
    FIELD amount  AS DECIMAL.
DEFINE TEMP-TABLE t-bkrart LIKE bkrart.

DEF INPUT  PARAMETER b1-resnr       AS INT.
DEF INPUT  PARAMETER resnr          AS INT.
DEF INPUT  PARAMETER resline        AS INT.
DEF OUTPUT PARAMETER TABLE FOR ol.
DEF OUTPUT PARAMETER TABLE FOR t-bkrart.

DEFINE BUFFER func-buff FOR bk-func.
DEFINE VARIABLE status-chr AS CHAR FORMAT "x(10)". 

FOR EACH ol: 
    DELETE ol. 
END. 
FIND FIRST bk-rart WHERE bk-rart.veran-nr = b1-resnr AND 
bk-rart.veran-resnr = resline USE-INDEX nr-pg-ug-ix NO-LOCK NO-ERROR. 
IF AVAILABLE bk-rart THEN 
DO: 
    IF bk-rart.resstatus = 1 THEN 
    DO: 
      status-chr = "Fix". 
    END. 
    ELSE IF bk-rart.resstatus = 2 THEN 
    DO: 
      status-chr = "Tentative". 
    END. 
    ELSE IF bk-rart.resstatus = 3 THEN 
    DO: 
      status-chr = "Waiting List". 
    END. 
    FIND FIRST bk-reser WHERE bk-reser.veran-nr = resnr 
      AND bk-reser.veran-resnr = resline NO-LOCK NO-ERROR. 
    FOR EACH bk-rart WHERE bk-rart.veran-nr = resnr 
      AND bk-rart.veran-resnr = resline 
      USE-INDEX nr-pg-ug-ix NO-LOCK: 
      CREATE ol. 
      ol.str = STRING(bk-reser.von-zeit,"99:99") + STRING(bk-reser.bis-zeit,"99:99") + STRING(bk-rart.raum,"x(15)") + 
        STRING(bk-rart.veran-nr,">>>,>>9") + STRING(bk-rart.bezeich,"x(30)") + STRING(bk-rart.anzahl,">>>,>>9") + 
        STRING(bk-rart.preis,">>>,>>>,>>9.99") + STRING(status-chr,"x(10)") + STRING(bk-rart.bemerkung,"x(2)"). 
    END. 
END.
RUN create-bkrart.
FOR EACH bkrart NO-LOCK,
    FIRST bk-func WHERE bk-func.veran-nr = bkrart.veran-nr AND
          bk-func.veran-seite = bkrart.veran-seite:
    CREATE t-bkrart.
    BUFFER-COPY bkrart TO t-bkrart.
    ASSIGN t-bkrart.tischform = bk-func.tischform[1].
END.
/*
FOR EACH bkrart WHERE bkrart.veran-nr = b1-resnr AND 
    bkrart.veran-seite = resline NO-LOCK,
    FIRST bk-func WHERE bk-func.veran-nr = bkrart.veran-nr AND
    bk-func.veran-seite = bkrart.veran-seite NO-LOCK:
    CREATE t-bkrart.
    BUFFER-COPY bkrart TO t-bkrart.
    ASSIGN t-bkrart.tischform = bk-func.tischform[1].
END.*/

PROCEDURE create-bkrart:
    FOR EACH bkrart:
        DELETE bkrart.
    END.
    FOR EACH bk-rart WHERE bk-rart.veran-nr = b1-resnr AND 
        bk-rart.veran-seite = resline NO-LOCK :
        CREATE bkrart.
        ASSIGN
            bkrart.veran-nr             = bk-rart.veran-nr
            bkrart.veran-seite          = bk-rart.veran-seite
            bkrart.von-zeit             = bk-rart.von-zeit
            bkrart.raum                 = bk-rart.raum
            bkrart.departement          = bk-rart.departement
            bkrart.veran-artnr          = bk-rart.veran-artnr
            bkrart.bezeich              = bk-rart.bezeich
            bkrart.anzahl               = bk-rart.anzahl
            bkrart.preis                = bk-rart.preis
            bkrart.amount               = ( bk-rart.anzahl * bk-rart.preis )
            bkrart.resstatus            = bk-rart.resstatus
            bkrart.setup-id             = bk-rart.setup-id
            bkrart.zwkum                = bk-rart.zwkum
            bkrart.fakturiert           = bk-rart.fakturiert.
    END.
END.

