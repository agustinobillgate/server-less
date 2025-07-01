
DEFINE TEMP-TABLE tourism-report
    FIELD gastnr      AS INTEGER
    FIELD gname       AS CHAR
    FIELD nat         AS CHAR
    FIELD passport-no AS CHAR
    FIELD ci-date     AS DATE
    FIELD co-date     AS DATE
    FIELD tourism-tax AS DECIMAL
    FIELD rmno        AS CHAR
    FIELD rechnr      AS INTEGER.

DEFINE INPUT PARAMETER fdate AS DATE NO-UNDO.
DEFINE INPUT PARAMETER tdate AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR tourism-report.

DEFINE VARIABLE tot-tax AS DECIMAL NO-UNDO.

FIND FIRST bill-line WHERE bill-line.bill-datum GE fdate
    AND bill-line.bill-datum LE tdate 
    AND bill-line.artnr = 108 USE-INDEX bildat_index NO-LOCK NO-ERROR.
DO WHILE AVAILABLE bill-line:
    FIND FIRST res-line WHERE res-line.resnr = bill-line.massnr
        AND res-line.reslinnr = bill-line.billin-nr NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN DO:
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember
            NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN DO:
            FIND FIRST tourism-report WHERE tourism-report.gastnr = guest.gastnr
                NO-LOCK NO-ERROR.
            IF NOT AVAILABLE tourism-report THEN DO:
                FIND FIRST nation WHERE nation.kurzbez = guest.nation1
                    AND nation.natcode = 0 NO-LOCK NO-ERROR.
                CREATE tourism-report.
                ASSIGN 
                    tourism-report.gastnr       = res-line.gastnrmember
                    tourism-report.gname        = res-line.NAME
                    tourism-report.passport-no  = guest.ausweis-nr1
                    tourism-report.ci-date      = res-line.ankunft
                    tourism-report.co-date      = res-line.abreise
                    tourism-report.tourism-tax  = bill-line.betrag
                    tourism-report.rmno         = res-line.zinr
                    tourism-report.rechnr       = bill-line.rechnr.

                IF AVAILABLE nation THEN ASSIGN tourism-report.nat = nation.bezeich.
            END.
            ELSE ASSIGN tourism-report.tourism-tax  = tourism-report.tourism-tax + bill-line.betrag. 
            ASSIGN tot-tax = tot-tax + bill-line.betrag.
        END.
   END.     
   ELSE DO:
       FIND FIRST bill WHERE bill.rechnr = bill-line.rechnr NO-LOCK NO-ERROR.
       IF AVAILABLE bill THEN DO:
           FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK NO-ERROR.
           IF AVAILABLE guest THEN DO:
                FIND FIRST tourism-report WHERE tourism-report.gastnr = guest.gastnr
                    NO-LOCK NO-ERROR.
                IF NOT AVAILABLE tourism-report THEN DO:
                    FIND FIRST nation WHERE nation.kurzbez = guest.nation1
                        AND nation.natcode = 0 NO-LOCK NO-ERROR.
                    CREATE tourism-report.
                    ASSIGN 
                        tourism-report.gastnr       = bill.gastnr
                        tourism-report.gname        = bill.NAME
                        tourism-report.passport-no  = guest.ausweis-nr1
                        tourism-report.tourism-tax  = bill-line.betrag
                        tourism-report.rechnr       = bill-line.rechnr.

                    IF AVAILABLE nation THEN ASSIGN tourism-report.nat = nation.bezeich.
                END.
                ELSE ASSIGN tourism-report.tourism-tax  = tourism-report.tourism-tax + bill-line.betrag. 
                ASSIGN tot-tax = tot-tax + bill-line.betrag.
           END.
       END.
   END.
    FIND NEXT bill-line WHERE bill-line.bill-datum GE fdate
        AND bill-line.bill-datum LE tdate 
        AND bill-line.artnr = 108 USE-INDEX bildat_index NO-LOCK NO-ERROR.
END.

CREATE tourism-report.
ASSIGN 
    tourism-report.gname        = "T O T A L"
    tourism-report.tourism-tax  = tot-tax.
