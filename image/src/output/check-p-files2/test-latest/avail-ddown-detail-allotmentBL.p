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

RUN detail-allotments.

PROCEDURE detail-allotments :
    IF curr-zikat EQ 0 THEN
    DO:
        FOR EACH kontline WHERE kontline.betriebsnr = 1 
          AND kontline.ankunft LE datum AND kontline.abreise GE datum 
          AND kontline.kontstatus = 1 NO-LOCK:                                /* CR 05/04/24 | Fix for Serverless */
          FIND FIRST zimmer WHERE zimmer.zikatnr = kontline.zikatnr 
          AND zimmer.sleeping NO-LOCK NO-ERROR. 
          CREATE rlist.
          ASSIGN
              rlist.zimmeranz                       = kontline.zimmeranz + 1
              rlist.zinr                            = zimmer.zinr 
              rlist.name                            = outorder.gespgrund 
              rlist.abreise                         = kontline.abreise 
              rlist.ankunft                         = kontline.ankunft 
              rlist.bezeich                         = zimmer.bezeich
              .
        END. 
    END.
    ELSE
    DO:
        FOR EACH kontline WHERE kontline.betriebsnr = 1 
          AND kontline.ankunft LE datum AND kontline.abreise GE datum 
          AND kontline.zikatnr = curr-zikat 
          AND kontline.kontstatus = 1 NO-LOCK:                                  /* CR 05/04/24 | Fix for Serverless */
          FIND FIRST zimmer WHERE zimmer.zikatnr = kontline.zikatnr 
          AND zimmer.sleeping NO-LOCK NO-ERROR. 
          CREATE rlist.
          ASSIGN
              rlist.zimmeranz                       = kontline.zimmeranz + 1
              rlist.zinr                            = zimmer.zinr 
              rlist.name                            = outorder.gespgrund 
              rlist.abreise                         = kontline.abreise 
              rlist.ankunft                         = kontline.ankunft 
              rlist.bezeich                         = zimmer.bezeich
              .
        END. 
    END.

END.

