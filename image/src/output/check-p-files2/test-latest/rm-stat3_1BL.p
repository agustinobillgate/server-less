
DEF TEMP-TABLE t-list
    FIELD gastnr    AS INTEGER
    FIELD gname     AS CHAR FORMAT "x(32)"
    FIELD nat       AS CHAR FORMAT "x(4)"
    FIELD zinr      LIKE zimmer.zinr
    FIELD erwachs   AS INTEGER FORMAT ">9"
    FIELD kind1     AS INTEGER FORMAT ">9"
    FIELD gratis    AS INTEGER FORMAT ">9"
    FIELD zipreis   LIKE res-line.zipreis
    FIELD curr      AS CHAR FORMAT "x(6)"
    FIELD resnr     AS INTEGER
    FIELD reslinnr  AS INTEGER
    FIELD ankunft   AS DATE INITIAL ?
    FIELD abreise   AS DATE INITIAL ?
    FIELD dlodge    AS DECIMAL FORMAT "->>>,>>>,>>9.99"
    FIELD drate     AS DECIMAL FORMAT "->,>>>,>>9.99"
    .

DEFINE INPUT PARAMETER segmNo      AS INTEGER.
DEFINE INPUT PARAMETER gastNo      AS INTEGER.
DEFINE INPUT PARAMETER fr-date     AS DATE.
DEFINE INPUT PARAMETER to-date     AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR t-list.

DEFINE VARIABLE ci-date AS DATE.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
ci-date = htparam.fdate.

/*gerald forecast-history*/
IF (fr-date LT ci-date) AND (to-date LT ci-date) THEN
DO:
  RUN create-list(fr-date, to-date).
END.
IF (fr-date LT ci-date) AND (to-date GE ci-date) THEN
DO:
  RUN create-list(fr-date, ci-date - 1).
  RUN create-list2(ci-date, to-date).     
END.
IF (fr-date GE ci-date) AND (to-date GE ci-date) THEN
DO:
  RUN create-list2(fr-date, to-date).
END.
/*end geral*/

/************************* PROCEDURES ***************************/

PROCEDURE create-list:     /*history*/
    DEFINE INPUT PARAMETER f-date AS DATE.
    DEFINE INPUT PARAMETER t-date AS DATE.

    FOR EACH genstat NO-LOCK WHERE 
        genstat.gastnr = gastNo      AND
        genstat.datum GE f-date     AND
        genstat.datum LE t-date     AND
        genstat.segmentcode = segmNo AND
        (genstat.erwachs + genstat.kind1) GT 0 AND
        genstat.gastnr GT 0 AND
        genstat.res-logic[2] :
        FIND FIRST t-list WHERE t-list.resnr = genstat.resnr 
            AND t-list.reslinnr = genstat.res-int[1] NO-ERROR.
        IF NOT AVAIL t-list THEN
        DO:
            FIND FIRST guest WHERE guest.gastnr = genstat.gastnrmember
                NO-LOCK NO-ERROR.
            FIND FIRST waehrung WHERE waehrung.waehrungsnr = genstat.wahrungsnr
                NO-LOCK NO-ERROR.
            CREATE t-list.
            ASSIGN t-list.resnr    = genstat.resnr
                   t-list.reslinnr = genstat.res-int[1]
                   t-list.gastnr   = genstat.gastnrmember
                   t-list.nat      = guest.nation1
                   t-list.zinr     = genstat.zinr
                   t-list.zipreis  = genstat.zipreis
                   t-list.erwachs  = genstat.erwachs
                   t-list.kind1    = genstat.kind1
                   t-list.gratis   = genstat.gratis
            .
            IF AVAILABLE guest THEN
                   t-list.gname    = guest.NAME + ", " + guest.vorname1 + ", " 
                                   + guest.anrede1 + guest.anredefirma.
            IF AVAILABLE waehrung THEN t-list.curr = waehrung.wabkurz.
        END.
        IF t-list.ankunft = ? OR t-list.ankunft GT genstat.res-date[1] THEN
           t-list.ankunft = genstat.res-date[1].
        IF t-list.abreise = ? OR t-list.abreise LT genstat.res-date[2] THEN
           t-list.abreise = genstat.res-date[2].

        ASSIGN t-list.dlodge = t-list.dlodge + genstat.logis.
    END.
END.

/*gerald forecast*/
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
         AND reservation.segmentcode = segmno NO-LOCK :

        FIND FIRST t-list WHERE t-list.resnr = res-line.resnr 
            AND t-list.reslinnr = res-line.reslinnr NO-ERROR.
        IF NOT AVAIL t-list THEN
        DO:
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember
                NO-LOCK NO-ERROR.
            FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr
                NO-LOCK NO-ERROR.
            CREATE t-list.
            ASSIGN t-list.resnr    = res-line.resnr
                   t-list.reslinnr = res-line.reslinnr
                   t-list.gastnr   = res-line.gastnrmember
                   t-list.zinr     = res-line.zinr
                   t-list.zipreis  = res-line.zipreis
                   t-list.erwachs  = res-line.erwachs
                   t-list.kind1    = res-line.kind1
                   t-list.gratis   = res-line.gratis
            .
            IF AVAILABLE guest THEN
                ASSIGN
                   t-list.gname    = guest.NAME + ", " + guest.vorname1 + ", " 
                                   + guest.anrede1 + guest.anredefirma
                   t-list.nat      = guest.nation1.
            IF AVAILABLE waehrung THEN t-list.curr = waehrung.wabkurz.
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

            ASSIGN t-list.dlodge = t-list.dlodge + local-net-lodg.
                
        END.
    END.
END.
