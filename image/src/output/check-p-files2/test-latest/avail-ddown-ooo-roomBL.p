.
DEFINE TEMP-TABLE rlist
    FIELD resnr                 AS CHAR LABEL "ResNo"
    FIELD zinr                  LIKE res-line.zinr
    FIELD ankunft               LIKE res-line.ankunft
    FIELD abreise               LIKE res-line.abreise
    FIELD zimmeranz             LIKE res-line.zimmeranz
    FIELD resstatus             LIKE res-line.resstatus
    FIELD zipreis               LIKE res-line.zipreis
    FIELD erwachs               LIKE res-line.erwachs
    FIELD kind1                 LIKE res-line.kind1
    FIELD gratis                LIKE res-line.gratis
    FIELD NAME                  LIKE res-line.NAME
    FIELD rsvName               AS CHAR FORMAT "x(24)" LABEL "Reserved Name"
    FIELD confirmed             AS LOGICAL INITIAL NO
    FIELD sleeping              AS LOGICAL INITIAL YES
    FIELD bezeich               AS CHAR FORMAT "x(15)"
    FIELD res-status            AS CHAR FORMAT "x(15)"
.

DEF INPUT PARAMETER curr-zikat   AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER datum        AS DATE     NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR rlist.

RUN ooo-room.

PROCEDURE ooo-room :
DEFINE VARIABLE tot  AS INTEGER INITIAL 0 NO-UNDO.
    IF curr-zikat EQ 0 THEN
    DO:
        FOR EACH outorder WHERE outorder.gespstart LE datum 
            AND outorder.gespende GE datum AND outorder.betriebsnr LE 1 
            NO-LOCK, 
            FIRST zimmer WHERE zimmer.zinr = outorder.zinr AND zimmer.sleeping 
            NO-LOCK: 
            CREATE rlist.
            ASSIGN
                rlist.zimmeranz                       = 1
                rlist.zinr                            = outorder.zinr 
                rlist.name                            = outorder.gespgrund 
                rlist.abreise                         = outorder.gespende 
                rlist.ankunft                         = outorder.gespstart 
                rlist.bezeich                         = zimmer.bezeich
                .
            ASSIGN tot = tot + rlist.zimmeranz.
        END.
    END.
    ELSE
    DO:
        FOR EACH outorder WHERE outorder.gespstart LE datum 
            AND outorder.gespende GE datum AND outorder.betriebsnr LE 1 
            NO-LOCK, 
            FIRST zimmer WHERE zimmer.zinr = outorder.zinr AND zimmer.sleeping 
            AND zimmer.zikatnr = curr-zikat NO-LOCK: 
            CREATE rlist.
            ASSIGN
                rlist.zimmeranz                       = 1
                rlist.zinr                            = outorder.zinr 
                rlist.name                            = outorder.gespgrund 
                rlist.abreise                         = outorder.gespende 
                rlist.ankunft                         = outorder.gespstart 
                rlist.bezeich                         = zimmer.bezeich
                .
             ASSIGN tot = tot + 1.
        END. 
    END.
    IF tot NE 0 THEN
    DO:
        CREATE rlist.
        ASSIGN 
            rlist.name                  = "TOTAL"
            rlist.zimmeranz             = tot
            rlist.abreise               = ? 
            rlist.ankunft               = ?
            .
    END.
END.

