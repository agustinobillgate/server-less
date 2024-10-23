/*Eko 11 Februari 2015 create BL for fa-movelist*/
/*mathis
fa-op*/

DEFINE TEMP-TABLE output-list
    FIELD asset-name AS CHAR FORMAT "x(30)"         LABEL "Asset Name"
    FIELD asset-no   AS CHAR FORMAT "99.999.9999"   LABEL "Asset No"
    FIELD Move-from  AS CHAR FORMAT "x(24)"         LABEL "Move From"
    FIELD Move-to    AS CHAR FORMAT "x(24)"         LABEL "Move To"
    FIELD datum      AS DATE FORMAT "99/99/99"      LABEL "Date"
    FIELD usrid      AS CHAR FORMAT "x(3)"          LABEL "By"
    FIELD zeit       AS CHAR FORMAT "x(8)"          LABEL "Time"
    FIELD qty        AS INTEGER FORMAT ">>9"        LABEL "Qty"
    FIELD price      AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Price"
    FIELD amount     AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99" LABEL "Amount".

DEFINE TEMP-TABLE tmp-mathis LIKE mathis.

DEFINE INPUT PARAMETER c-procedure  AS CHARACTER               NO-UNDO.
DEFINE INPUT PARAMETER bl-all       AS LOGICAL                 NO-UNDO.
DEFINE INPUT PARAMETER user-init    AS CHARACTER FORMAT "x(2)" NO-UNDO.
DEFINE INPUT PARAMETER typ-of       AS CHAR                    NO-UNDO.
DEFINE INPUT PARAMETER main-query   AS INTEGER                 NO-UNDO.
DEFINE INPUT PARAMETER sub-query    AS INTEGER                 NO-UNDO.
DEFINE INPUT PARAMETER int-query    AS INTEGER                 NO-UNDO.
DEFINE INPUT PARAMETER fdate        AS DATE                    NO-UNDO.
DEFINE INPUT PARAMETER tdate        AS DATE                    NO-UNDO.
DEFINE OUTPUT PARAMETER retMessage  AS INTEGER INITIAL 0       NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

DEFINE BUFFER fa-buff   FOR fa-artikel.
DEFINE BUFFER inventory FOR fa-artikel.

/************************* Main Logic *****************************/
IF c-procedure = "create-list"  THEN
DO:
    RUN create-list.
END.
ELSE IF c-procedure = "cancel-upgrade"  THEN
DO:
    RUN cancel-upgrade.
END.
/********************* Procedures ********************************/
PROCEDURE create-list:
IF bl-all THEN
DO:
    FOR EACH fa-op WHERE fa-op.opart = 2 AND fa-op.datum GE fdate 
        AND fa-op.datum LE tdate NO-LOCK, 
        FIRST mathis WHERE mathis.nr = fa-op.nr AND mathis.flag = 1 
        NO-LOCK BY fa-op.datum :

        CREATE output-list.
        ASSIGN 
            output-list.asset-name      = mathis.NAME
            output-list.asset-no        = mathis.asset
            output-list.datum           = fa-op.datum
            output-list.zeit            = STRING(fa-op.zeit, "HH:MM:SS")
            output-list.move-from       = ENTRY(3, fa-op.docu-nr, ";;")
            output-list.move-to         = ENTRY(5, fa-op.docu-nr, ";;")
            output-list.usrid           = fa-op.id 
            output-list.qty             = fa-op.anzahl
            output-list.price           = fa-op.einzelpreis   
            output-list.amount          = fa-op.warenwert .
    END.
END.
ELSE
DO:
    IF typ-of = "1" THEN
    DO:
        FOR EACH tmp-mathis :
            DELETE tmp-mathis.
        END.

        IF main-query NE 0 THEN
        DO:
            IF sub-query NE 0 THEN
            DO:
                FOR EACH fa-artikel WHERE fa-artikel.gnr = main-query AND fa-artikel.subgrp = sub-query , 
                    FIRST mathis WHERE mathis.nr = fa-artikel.nr NO-LOCK  BY fa-artikel.nr :
                    CREATE tmp-mathis.
                    BUFFER-COPY mathis TO tmp-mathis.
                END.
            END.
            ELSE
            DO:
                FOR EACH fa-artikel WHERE fa-artikel.gnr = main-query , 
                    FIRST mathis WHERE mathis.nr = fa-artikel.nr NO-LOCK  BY fa-artikel.nr :
                    CREATE tmp-mathis.
                    BUFFER-COPY mathis TO tmp-mathis.
                END.
            END.


            FOR EACH tmp-mathis :
                /*DISP tmp-mathis.
                PAUSE.*/
                FOR EACH fa-op WHERE fa-op.opart = 2 AND fa-op.datum GE fdate 
                    AND fa-op.datum LE tdate AND fa-op.nr = tmp-mathis.nr NO-LOCK BY fa-op.datum :

                    CREATE output-list.
                    ASSIGN output-list.asset-name   = tmp-mathis.NAME
                            output-list.asset-no    = tmp-mathis.asset
                            output-list.datum       = fa-op.datum
                            output-list.zeit        = STRING(fa-op.zeit, "HH:MM:SS")
                            output-list.move-from   = ENTRY(3, fa-op.docu-nr, ";;")
                            output-list.move-to     = ENTRY(5, fa-op.docu-nr, ";;")
                            output-list.usrid       = fa-op.id 
                            output-list.qty         = fa-op.anzahl
                            output-list.price       = fa-op.einzelpreis   
                            output-list.amount      = fa-op.warenwert .
                END.
            END.
        END.
    END.
    ELSE
    DO:
        FOR EACH mathis WHERE mathis.asset = STRING(int-query) :
            FOR EACH fa-op WHERE fa-op.opart = 2 AND fa-op.datum GE fdate 
                AND fa-op.datum LE tdate AND fa-op.nr =  mathis.nr NO-LOCK BY fa-op.datum :

                CREATE output-list.
                ASSIGN output-list.asset-name   = mathis.NAME
                        output-list.asset-no    = mathis.asset
                        output-list.datum       = fa-op.datum
                        output-list.zeit        = STRING(fa-op.zeit, "HH:MM:SS")
                        output-list.move-from   = ENTRY(3, fa-op.docu-nr, ";;")
                        output-list.move-to     = ENTRY(5, fa-op.docu-nr, ";;")
                        output-list.usrid       = fa-op.id 
                        output-list.qty         = fa-op.anzahl
                        output-list.price       = fa-op.einzelpreis   
                        output-list.amount      = fa-op.warenwert .
            END.
        END.
    END.
END.
END PROCEDURE.

PROCEDURE cancel-upgrade:
DEF VAR last-depn AS DATE NO-UNDO.
FIND FIRST htparam WHERE paramnr = 881 NO-LOCK.
last-depn = htparam.fdate.

FIND FIRST fa-op WHERE fa-op.opart = 4 AND fa-op.nr = fa-artikel.nr
    AND fa-op.datum = fa-artikel.deleted NO-LOCK .
IF YEAR(fa-op.datum) = YEAR(last-depn) AND MONTH(fa-op.datum) = MONTH(last-depn) THEN
DO:
    retMessage = 1. 
    RETURN NO-APPLY.
END.
DO TRANSACTION:
    FIND CURRENT fa-op EXCLUSIVE-LOCK.
    ASSIGN fa-op.loeschflag = 1.
    FIND CURRENT fa-op NO-LOCK.
    
    FIND CURRENT fa-artikel EXCLUSIVE-LOCK.
    ASSIGN
        fa-artikel.loeschflag = 0
        fa-artikel.deleted = ? 
        fa-artikel.DID = user-init
        fa-art.p-nr    = 0.
    FIND CURRENT fa-artikel NO-LOCK.

    FIND FIRST fa-buff WHERE fa-buff.nr = fa-artikel.p-nr EXCLUSIVE-LOCK .
    ASSIGN 
        fa-buff.warenwert = fa-buff.warenwert - fa-artikel.warenwert
        fa-buff.book-wert = fa-buff.book-wert - fa-artikel.warenwert
        .
    FIND CURRENT fa-buff NO-LOCK.
END.
END PROCEDURE.
