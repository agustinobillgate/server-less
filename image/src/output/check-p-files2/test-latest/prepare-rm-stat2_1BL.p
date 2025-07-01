DEF TEMP-TABLE t-list
    FIELD gastnr    AS INTEGER
    FIELD mgastnr   AS INTEGER
    FIELD gname     AS CHAR FORMAT "x(32)"
    FIELD resNr     AS INTEGER FORMAT ">>>>>>>9"
    FIELD reslinnr  AS INTEGER
    FIELD fdate     AS DATE INITIAL TODAY
    FIELD tdate     AS DATE INITIAL 01/01/1900
    FIELD ankunft   AS DATE INITIAL ?
    FIELD abreise   AS DATE INITIAL ?
    FIELD zimmeranz AS INTEGER FORMAT ">>9"
    FIELD dlodge    AS DECIMAL FORMAT "->>>,>>>,>>9.99"
    FIELD dnite     AS INTEGER FORMAT ">>9"
    FIELD drate     AS DECIMAL FORMAT "->>,>>>,>>9.99"
    FIELD mlodge    AS DECIMAL FORMAT "->>,>>>,>>9.99"
    FIELD mnite     AS INTEGER FORMAT ">>9"
    FIELD mrate     AS DECIMAL FORMAT "->,>>>,>>9.99"
    FIELD ylodge    AS DECIMAL FORMAT "->>>,>>>,>>9.99"
    FIELD ynite     AS INTEGER FORMAT ">>9"
    FIELD yrate     AS DECIMAL FORMAT "->,>>>,>>9.99"
    .


DEFINE INPUT PARAMETER gastNo       AS INTEGER.
DEFINE INPUT PARAMETER segmcode     AS INTEGER.
DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER mi-ftd       AS LOGICAL.

DEF OUTPUT PARAMETER avail-guest AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER f-tittle    AS CHAR    INIT "".
DEF OUTPUT PARAMETER TABLE FOR t-list.

DEFINE VARIABLE ci-date AS DATE.

FIND FIRST guest WHERE guest.gastnr = gastNo NO-LOCK NO-ERROR.
IF NOT AVAILABLE guest THEN RETURN.
ELSE avail-guest = YES.
FIND FIRST segment WHERE segment.segmentcode = segmcode NO-LOCK NO-ERROR.
IF AVAIL segment THEN
f-tittle = ": " + ENTRY(1, segment.bezeich, "$$0") + " - " + guest.NAME.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
ci-date = htparam.fdate.

IF (from-date LT ci-date) AND (to-date LT ci-date)  THEN
DO:
  RUN create-list(from-date, to-date).  
END.
IF (from-date LT ci-date) AND (to-date GE ci-date) THEN
DO:
  RUN create-list(from-date, ci-date - 1).
  RUN create-list2(ci-date, to-date).     
END.
IF (from-date GE ci-date) AND (to-date GE ci-date) THEN
DO:
  RUN create-list2(from-date, to-date).
END.

   
PROCEDURE create-list:   /*history*/  
    DEFINE INPUT PARAMETER f-date AS DATE.
    DEFINE INPUT PARAMETER t-date AS DATE.
    
    FOR EACH genstat NO-LOCK WHERE 
        genstat.gastnr = gastNo        AND
        genstat.datum GE f-date        AND
        genstat.datum LE t-date        AND
        genstat.segmentcode = segmcode AND
        genstat.res-logic[2]           AND
        (genstat.erwachs + genstat.kind1) GT 0:
        
        FIND FIRST t-list WHERE t-list.resnr = genstat.resnr NO-ERROR.
        IF NOT AVAIL t-list THEN
        DO:
            CREATE t-list.
            ASSIGN t-list.resnr    = genstat.resnr
                   t-list.reslinnr = genstat.res-int[1]
                   t-list.mgastnr  = genstat.gastnrmember
                   t-list.gastnr   = genstat.gastnr
            .
            IF AVAILABLE guest THEN
            t-list.gname    = guest.NAME + ", " + guest.vorname1 + ", " 
                            + guest.anrede1 + guest.anredefirma.
        END.

        IF t-list.ankunft = ? OR t-list.ankunft GT genstat.res-date[1] THEN
           t-list.ankunft = genstat.res-date[1].
        IF t-list.abreise = ? OR t-list.abreise LT genstat.res-date[2] THEN
           t-list.abreise = genstat.res-date[2].

        IF t-list.fdate GT genstat.datum THEN ASSIGN t-list.fdate = genstat.datum.
        IF t-list.tdate LT genstat.datum THEN ASSIGN t-list.tdate = genstat.datum.

        IF mi-ftd AND f-date LT ci-date THEN
        DO:
          IF genstat.datum = f-date THEN
          DO:
             ASSIGN t-list.dlodge = t-list.dlodge + genstat.logis.
             /*ITA 071216
             IF genstat.res-int[1] NE 13 THEN t-list.dnite  = t-list.dnite  + 1.*/
             IF genstat.resstatus NE 13 THEN t-list.dnite  = t-list.dnite  + 1.
          END.                                                                

          IF MONTH(genstat.datum) = MONTH(t-date) AND YEAR(genstat.datum) = YEAR(t-date) THEN
          DO:
             ASSIGN t-list.mlodge = t-list.mlodge + genstat.logis.
             /*ITA 071216
             IF genstat.res-int[1] NE 13 THEN ASSIGN t-list.mnite  = t-list.mnite  + 1.*/
             IF genstat.resstatus NE 13 THEN ASSIGN t-list.mnite  = t-list.mnite  + 1.
          END.

          IF genstat.datum GE f-date AND genstat.datum LE t-date THEN
          DO:
             ASSIGN t-list.ylodge = t-list.ylodge + genstat.logis.
             /*ITA 071216
             IF genstat.res-int[1] NE 13 THEN ASSIGN t-list.ynite  = t-list.ynite  + 1.*/
             IF genstat.resstatus NE 13 THEN ASSIGN t-list.ynite  = t-list.ynite  + 1.
          END.
        END.

        ELSE IF NOT mi-ftd AND f-date LT ci-date THEN
        DO:
           IF genstat.datum = to-date THEN
           DO:
             ASSIGN t-list.dlodge = t-list.dlodge + genstat.logis.
             /*ITA 071216
             IF genstat.res-int[1] NE 13 THEN t-list.dnite  = t-list.dnite  + 1.*/
             IF genstat.resstatus NE 13 THEN t-list.dnite  = t-list.dnite  + 1.
           END.
           
           IF YEAR(genstat.datum) = YEAR(t-date) THEN
           DO:
             IF MONTH(genstat.datum) = MONTH(t-date) THEN
             DO:
               ASSIGN t-list.mlodge = t-list.mlodge + genstat.logis.
               /*ITA 071216
               IF genstat.res-int[1] NE 13 THEN ASSIGN t-list.mnite  = t-list.mnite  + 1.*/
               IF genstat.resstatus NE 13 THEN ASSIGN t-list.mnite  = t-list.mnite  + 1.
             END.
           
             ASSIGN t-list.ylodge = t-list.ylodge + genstat.logis.
             /*ITA 071216
             IF genstat.res-int[1] NE 13 THEN ASSIGN t-list.ynite  = t-list.ynite  + 1.*/
             IF genstat.resstatus NE 13 THEN ASSIGN t-list.ynite  = t-list.ynite  + 1.
           END.
        END.
    END.

    FOR EACH t-list :
      IF t-list.dnite NE 0 THEN ASSIGN t-list.drate = t-list.dlodge / t-list.dnite.
      IF t-list.mnite NE 0 THEN ASSIGN t-list.mrate = t-list.mlodge / t-list.mnite.
      IF t-list.ynite NE 0 THEN ASSIGN t-list.yrate = t-list.ylodge / t-list.ynite.
    END.
END.


PROCEDURE create-list2:   /*forecast*/      
    DEFINE INPUT PARAMETER f-date AS DATE.
    DEFINE INPUT PARAMETER t-date AS DATE.

    DEFINE VARIABLE datum  AS DATE.
    DEFINE VARIABLE datum1 AS DATE.
    DEFINE VARIABLE datum2 AS DATE.

    DEFINE VARIABLE local-net-lodg  AS DECIMAL.
    DEFINE VARIABLE net-lodg        AS DECIMAL.
    DEFINE VARIABLE tot-breakfast   AS DECIMAL.
    DEFINE VARIABLE tot-Lunch       AS DECIMAL.
    DEFINE VARIABLE tot-dinner      AS DECIMAL.
    DEFINE VARIABLE tot-Other       AS DECIMAL.
    DEFINE VAR tot-rmrev            AS DECIMAL INITIAL 0.
    DEFINE VAR tot-vat              AS DECIMAL INITIAL 0.
    DEFINE VAR tot-service          AS DECIMAL INITIAL 0.

    FOR EACH res-line WHERE 
        (res-line.active-flag LE 1 AND res-line.resstatus LE 13 
         AND res-line.resstatus NE 4 
         AND res-line.resstatus NE 8
         AND res-line.resstatus NE 9 
         AND res-line.resstatus NE 10
         AND res-line.resstatus NE 12
         AND res-line.active-flag LE 1
         AND NOT (res-line.ankunft GT t-date ) AND 
         NOT (res-line.abreise LT f-date)) OR
        (res-line.active-flag = 2 AND res-line.resstatus = 8 
         AND res-line.ankunft = ci-date AND res-line.abreise = ci-date) 
         AND res-line.gastnr EQ gastnr AND res-line.l-zuordnung[3] = 0
         USE-INDEX gnrank_ix NO-LOCK,
         FIRST reservation WHERE reservation.resnr = res-line.resnr 
         AND reservation.segmentcode = segmcode NO-LOCK :
    
        FIND FIRST t-list WHERE t-list.resnr = res-line.resnr NO-ERROR.
        IF NOT AVAIL t-list THEN
        DO: 
        CREATE t-list.
        ASSIGN t-list.resnr    = res-line.resnr
               t-list.reslinnr = res-line.reslinnr
               t-list.mgastnr  = res-line.gastnrmember
               t-list.gastnr   = res-line.gastnr
        .
        IF AVAILABLE guest THEN
        t-list.gname    = guest.NAME + ", " + guest.vorname1 + ", " 
                        + guest.anrede1 + guest.anredefirma.
        END.
        
        IF t-list.ankunft = ? OR t-list.ankunft GT res-line.ankunft THEN
           t-list.ankunft = res-line.ankunft.
        IF t-list.abreise = ? OR t-list.abreise LT res-line.abreise THEN
           t-list.abreise = res-line.abreise.

        IF res-line.ankunft GE f-date THEN datum1 = res-line.ankunft.
        ELSE datum1 = f-date.
        IF res-line.abreise LE t-date THEN datum2 = res-line.abreise - 1.
        ELSE datum2 = t-date.

        DO datum = datum1 TO datum2:
            local-net-lodg = 0.
            net-lodg  = 0.

            IF t-list.fdate GT datum THEN ASSIGN t-list.fdate = datum.
            IF t-list.tdate LT datum THEN ASSIGN t-list.tdate = datum.

            RUN get-room-breakdown.p(RECID(res-line), datum, 0, f-date,
                                         OUTPUT net-lodg, OUTPUT local-net-lodg,
                                         OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                         OUTPUT tot-dinner, OUTPUT tot-other,
                                         OUTPUT tot-rmrev, OUTPUT tot-vat,
                                         OUTPUT tot-service).
            IF tot-rmrev = 0 THEN  
                ASSIGN 
                    local-net-lodg      = 0
                    net-lodg            = 0. 

            IF mi-ftd THEN
            DO:
                IF datum = f-date AND from-date GE f-date THEN
                DO:
                   ASSIGN t-list.dlodge = t-list.dlodge + local-net-lodg.
                   IF res-line.resstatus NE 13 THEN t-list.dnite  = t-list.dnite  + res-line.zimmeranz.
                END.

                IF MONTH(datum) = MONTH(t-date) THEN
                DO:
                   ASSIGN t-list.mlodge = t-list.mlodge + local-net-lodg.
                   IF res-line.resstatus NE 13 THEN t-list.mnite = t-list.mnite + res-line.zimmeranz.
                END.

                IF datum GE f-date AND datum LE t-date THEN
                DO:
                   ASSIGN t-list.ylodge = t-list.ylodge + local-net-lodg.
                   IF res-line.resstatus NE 13 THEN t-list.ynite = t-list.ynite + res-line.zimmeranz.
                END.
            END.

            ELSE IF NOT mi-ftd THEN
            DO: 
               IF datum = t-date AND from-date GE f-date THEN
               DO:
                 ASSIGN t-list.dlodge = t-list.dlodge + local-net-lodg.
                 IF res-line.resstatus NE 13 THEN t-list.dnite  = t-list.dnite  + res-line.zimmeranz.
               END.
               
               IF YEAR(datum) = YEAR(t-date) THEN
               DO:
                 IF MONTH(datum) = MONTH(t-date) THEN
                 DO:
                    ASSIGN t-list.mlodge = t-list.mlodge + local-net-lodg.
                    IF res-line.resstatus NE 13 THEN t-list.mnite = t-list.mnite + res-line.zimmeranz.
                 END.
               
                 ASSIGN t-list.ylodge = t-list.ylodge + local-net-lodg.
                 IF res-line.resstatus NE 13 THEN t-list.ynite = t-list.ynite + res-line.zimmeranz.
               END.
            END.
        END.    
    END.

    FOR EACH t-list :
      IF t-list.dnite NE 0 THEN ASSIGN t-list.drate = t-list.dlodge / t-list.dnite.
      IF t-list.mnite NE 0 THEN ASSIGN t-list.mrate = t-list.mlodge / t-list.mnite.
      IF t-list.ynite NE 0 THEN ASSIGN t-list.yrate = t-list.ylodge / t-list.ynite.
    END.
END.
