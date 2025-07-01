DEFINE TEMP-TABLE rmcomp-segm-list
    FIELD flag          AS INTEGER
    FIELD segment       AS CHARACTER FORMAT "x(40)"
    FIELD room          AS CHARACTER FORMAT "x(8)"
    FIELD pax           AS CHARACTER FORMAT "x(8)"
    FIELD logis         AS CHARACTER FORMAT "x(19)"
    FIELD proz          AS CHARACTER FORMAT "x(6)"
    FIELD avrgrate      AS CHARACTER FORMAT "x(19)"
    FIELD m-room        AS CHARACTER FORMAT "x(8)"
    FIELD m-pax         AS CHARACTER FORMAT "x(8)"
    FIELD m-logis       AS CHARACTER FORMAT "x(19)"
    FIELD m-proz        AS CHARACTER FORMAT "x(6)"
    FIELD m-avrgrate    AS CHARACTER FORMAT "x(19)"
    FIELD y-room        AS CHARACTER FORMAT "x(8)"
    FIELD y-pax         AS CHARACTER FORMAT "x(8)"
    FIELD y-logis       AS CHARACTER FORMAT "x(19)"
    FIELD y-proz        AS CHARACTER FORMAT "x(6)"
    FIELD y-avrgrate    AS CHARACTER FORMAT "x(19)"
    FIELD rmnite1       AS CHARACTER FORMAT "x(8)"
    FIELD rmrev1        AS CHARACTER FORMAT "x(19)"
    FIELD rmnite        AS CHARACTER FORMAT "x(8)"
    FIELD rmrev         AS CHARACTER FORMAT "x(19)"
    FIELD segm-code     AS INTEGER
    FIELD gastnr        AS INTEGER
    FIELD revenue       AS CHARACTER FORMAT "x(19)"
.

DEFINE TEMP-TABLE s-list
    FIELD segm-code AS INTEGER
    FIELD segm-grup AS INTEGER
    FIELD segment   AS CHAR FORMAT "x(24)" 
    FIELD segment1  AS CHAR FORMAT "x(24)"
    FIELD gastnr    AS INTEGER
    FIELD compname  AS CHAR FORMAT "x(24)"
    FIELD room      AS INTEGER FORMAT "->>9.99"
    FIELD c-room    AS INTEGER INITIAL 0
    FIELD pax       AS INTEGER FORMAT "->>,>>9"
    FIELD logis     AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0 
    FIELD proz      AS DECIMAL FORMAT "->>9.99" INITIAL 0 
    FIELD avrgrate  AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0 

    FIELD m-room     AS INTEGER FORMAT "->>,>>9" INITIAL 0 
    FIELD mc-room    AS INTEGER                  INITIAL 0
    FIELD m-pax      AS INTEGER FORMAT "->>,>>9" INITIAL 0 
    FIELD m-logis    AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0 
    FIELD m-proz     AS DECIMAL FORMAT "->>9.99" INITIAL 0 
    FIELD m-avrgrate AS DECIMAL FORMAT /*">,>>>,>>9"*/ "->,>>>,>>>,>>9" INITIAL 0 
    
    FIELD y-room     AS INTEGER FORMAT "->>>,>>9" INITIAL 0 
    FIELD yc-room    AS INTEGER                   INITIAL 0
    FIELD y-pax      AS INTEGER FORMAT "->>>,>>9" INITIAL 0 
    FIELD y-logis    AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0 
    FIELD y-proz     AS DECIMAL FORMAT "->>9.99" INITIAL 0 
    FIELD y-avrgrate AS DECIMAL FORMAT /*">,>>>,>>9"*/ "->,>>>,>>>,>>9" INITIAL 0
    FIELD revenue    AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0
    .  

DEFINE TEMP-TABLE tmp-room
    FIELD gastnr AS INTEGER
    FIELD zinr   AS CHAR
    FIELD flag   AS INTEGER
    INDEX gstnr gastnr DESC zinr.      /*1 DATE    2 MONTH   3 YEAR*/

DEFINE TEMP-TABLE t-list
    FIELD gastnr AS INT
    FIELD logis-guaranteed  AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD pax-guaranteed    AS INT
    FIELD room-guaranteed   AS INT
    FIELD logis-tentative   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD pax-tentative     AS INT
    FIELD room-tentative    AS INT

    FIELD mlogis-guaranteed  AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD mpax-guaranteed    AS INT
    FIELD mroom-guaranteed   AS INT
    FIELD mlogis-tentative   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD mpax-tentative     AS INT
    FIELD mroom-tentative    AS INT
    
    FIELD ylogis-guaranteed  AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD ypax-guaranteed    AS INT
    FIELD yroom-guaranteed   AS INT
    FIELD ylogis-tentative   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD ypax-tentative     AS INT
    FIELD yroom-tentative    AS INT

    FIELD resstatus         AS INT
    FIELD zipreis           AS DECIMAL
    .

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER sorttype     AS INTEGER.
DEFINE INPUT PARAMETER cardtype     AS INTEGER.
DEFINE INPUT PARAMETER incl-comp    AS LOGICAL.
DEFINE INPUT PARAMETER mi-ftd       AS LOGICAL.
DEFINE INPUT PARAMETER f-date       AS DATE.
DEFINE INPUT PARAMETER t-date       AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER sales-ID     AS CHAR.
DEFINE INPUT PARAMETER vhp-limited  AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR rmcomp-segm-list.
DEFINE OUTPUT PARAMETER TABLE FOR s-list.

/*
DEFINE VARIABLE pvILanguage  AS INTEGER NO-UNDO INIT 0.
DEFINE VARIABLE sorttype     AS INTEGER INIT 0.
DEFINE VARIABLE cardtype     AS INTEGER INIT 1.
DEFINE VARIABLE incl-comp    AS LOGICAL INIT NO.
DEFINE VARIABLE mi-ftd       AS LOGICAL INIT YES.
DEFINE VARIABLE f-date       AS DATE INIT 07/20/23.
DEFINE VARIABLE t-date       AS DATE INIT 07/30/23.
DEFINE VARIABLE to-date      AS DATE INIT 07/30/23.
DEFINE VARIABLE sales-ID     AS CHAR INIT "".
DEFINE VARIABLE vhp-limited  AS LOGICAL INIT NO.*/



DEFINE VARIABLE price-decimal AS INTEGER. 

DEFINE VARIABLE room         AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE c-room       AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE pax          AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE logis        AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE avrgrate     AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
dEFINE VARIABLE proz         AS DECIMAL FORMAT "->>9.99" INITIAL 0 .

DEFINE VARIABLE m-room       AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE mc-room      AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE m-pax        AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE m-logis      AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE m-avrgrate   AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
DEFINE VARIABLE m-proz       AS DECIMAL FORMAT "->>9.99" INITIAL 0 .

DEFINE VARIABLE y-room       AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE yc-room      AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE y-pax        AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE y-logis      AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE y-avrgrate   AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
DEFINE VARIABLE y-proz       AS DECIMAL FORMAT "->>9.99" INITIAL 0 .
DEFINE VARIABLE revenue       AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0.     /*william E3CA2B*/

DEFINE VARIABLE gt-room      AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE gtc-room     AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE gt-pax       AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE gt-logis     AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE gt-avrgrate  AS DECIMAL FORMAT "->,>>>,>>>,>>9". 

DEFINE VARIABLE gtm-room     AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE gtmc-room    AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE gtm-pax      AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE gtm-logis    AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE gtm-avrgrate AS DECIMAL FORMAT "->,>>>,>>>,>>9".
DEFINE VARIABLE gtm-proz     AS DECIMAL FORMAT "->>9.99" INITIAL 0 .
 
DEFINE VARIABLE gty-room     AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE gtyc-room    AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE gty-pax      AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE gty-logis    AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE gty-avrgrate AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
DEFINE VARIABLE gty-proz     AS DECIMAL FORMAT "->>9.99" INITIAL 0. 
DEFINE VARIABLE gty-revenue AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0.   /*william E3CA2B*/

DEFINE VARIABLE st-room      AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE stc-room     AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE st-pax       AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE st-logis     AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE st-avrgrate  AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
DEFINE VARIABLE st-proz      AS DECIMAL FORMAT "->>9.99" INITIAL 0. 
 
DEFINE VARIABLE stm-room     AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE stmc-room    AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE stm-pax      AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE stm-logis    AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE stm-avrgrate AS DECIMAL FORMAT "->,>>>,>>>,>>9".
DEFINE VARIABLE stm-proz     AS DECIMAL FORMAT "->>9.99" INITIAL 0 .
 
DEFINE VARIABLE sty-room     AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE styc-room    AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE sty-pax      AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE sty-logis    AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE sty-avrgrate AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
DEFINE VARIABLE sty-proz     AS DECIMAL FORMAT "->>9.99" INITIAL 0.
DEFINE VARIABLE sty-revenue  AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0.   /*william E3CA2B*/

DEFINE VARIABLE rmrevsubt    AS DECIMAL FORMAT "->>>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE rm-serv      AS LOGICAL. 
DEFINE VARIABLE rm-vat       AS LOGICAL.
DEFINE VARIABLE othRev       AS DECIMAL.

DEFINE VARIABLE datum           AS DATE.

DEFINE VARIABLE ci-date AS date. 
DEFINE VARIABLE mm         AS INTEGER NO-UNDO. 
DEFINE VARIABLE yy         AS INTEGER NO-UNDO. 
DEFINE VARIABLE from-date  AS DATE NO-UNDO. 
DEFINE VARIABLE fdate      AS DATE.
DEFINE VARIABLE beg-date   AS DATE NO-UNDO.
DEFINE VARIABLE d1         AS DATE.
DEFINE VARIABLE d2         AS DATE.
DEFINE VARIABLE tdate      AS DATE.
/* Rd, #746, 26Mar2025 , variable tmpdate */
DEFINE VARIABLE tmpdate    AS DATE.
{ supertransbl.i }
DEF VAR lvCAREA AS CHAR INITIAL "rmcomp-segment". 

/*************** MAIN LOGIC ***************/
FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
ci-date = htparam.fdate.

IF mi-ftd THEN
DO:
   ASSIGN
       from-date = f-date
       to-date   = t-date
       mm        = MONTH(to-date)
       yy        = YEAR(to-date).
END.
ELSE
DO:
   ASSIGN
       mm = MONTH(to-date)
       yy = YEAR(to-date)
       from-date = DATE(1,1,yy)
       f-date    = DATE(MONTH(t-date), 1, YEAR(t-date)).
END.

/*gerald forecast-history*/
IF (from-date LT ci-date) AND (to-date LT ci-date) THEN
DO:
   IF sorttype = 0 OR sorttype = 1 THEN 
   DO:
      
      RUN create-umsatz(from-date, to-date).
      IF sorttype = 0 THEN RUN create-output. 
      ELSE RUN create-output1.
   END.
   ELSE 
   DO:
       
      RUN create-umsatz2(from-date, to-date).

      RUN create-output2.
   END.
END.
ELSE IF (from-date LT ci-date) AND (to-date GE ci-date) THEN
DO:
    IF sorttype = 0 OR sorttype = 1 THEN
    DO:
      /* Rd, #746, 26Mar2025 , variable tmpdate */
      tmpdate = ci-date - 1.
      RUN create-umsatz(from-date, tmpdate).
      RUN create-fcast(ci-date, to-date).
      
      IF sorttype = 0 THEN RUN create-output.
      ELSE RUN create-output1.
    END.
    ELSE 
    DO:
      /* Rd, #746, 26Mar2025 , variable tmpdate */
      tmpdate = ci-date - 1.
      RUN create-umsatz2(from-date, tmpdate).
      RUN create-fcast2(ci-date, to-date).

       RUN create-output2.
    END.
END.
ELSE IF (from-date GE ci-date) AND (to-date GE ci-date) THEN
DO:
    IF sorttype = 0 OR sorttype = 1 THEN
    DO:
       RUN create-fcast(from-date, to-date).

       IF sorttype = 0 THEN RUN create-output.
       ELSE RUN create-output1.
    END.
    ELSE
    DO:
       RUN create-fcast2(from-date, to-date).

       RUN create-output2.
    END.
END.
/*end gerald*/
/********************* Procedure *********************************/
PROCEDURE create-umsatz:   /*history*/
    DEFINE INPUT PARAMETER date1 AS DATE.
    DEFINE INPUT PARAMETER date2 AS DATE.

    DEFINE VARIABLE rmrev      AS DECIMAL NO-UNDO.
    DEFINE VARIABLE otherrev      AS DECIMAL NO-UNDO.
    DEFINE VARIABLE service    AS DECIMAL NO-UNDO.
    DEFINE VARIABLE vat        AS DECIMAL NO-UNDO.
    DEFINE VARIABLE mm         AS INTEGER NO-UNDO. 
    DEFINE VARIABLE yy         AS INTEGER NO-UNDO. 
    DEFINE VARIABLE tdatum     AS DATE NO-UNDO.     /*william E3CA2B*/
    DEFINE VARIABLE do-dat     AS LOGICAL.          /*william E3CA2B*/
    DEFINE VARIABLE do-it      AS LOGICAL NO-UNDO. 
    DEFINE VARIABLE i          AS INTEGER INITIAL 0 NO-UNDO.
    DEFINE VARIABLE s          AS CHAR NO-UNDO.
    DEFINE VARIABLE curr-code  AS CHAR NO-UNDO.
    DEFINE VARIABLE status-vat AS LOGICAL NO-UNDO.
    DEFINE VARIABLE bydate     AS INTEGER NO-UNDO.

    DEFINE VARIABLE fdate       AS DATE.
    DEFINE VARIABLE beg-date    AS DATE NO-UNDO.
    
    ASSIGN
      room    = 0
      c-room  = 0
      pax     = 0
      logis   = 0

      m-room  = 0
      mc-room = 0
      m-pax   = 0
      m-logis = 0
      
      y-room  = 0 
      yc-room = 0 
      y-pax   = 0 
      y-logis = 0
      revenue = 0       /*william E3CA2B*/

      gt-room = 0
      gt-pax = 0
      gt-logis = 0
      gt-avrgrate = 0
      gtm-room = 0
      gtm-pax = 0
      gtm-logis = 0
      gtm-avrgrate = 0
      gtm-room = 0
      gtm-pax = 0
      gtm-logis = 0
      gtm-avrgrate = 0
      gty-room = 0
      gty-pax = 0
      gty-logis = 0
      gty-avrgrate = 0
      gty-revenue = 0   /*william E3CA2B*/
      . 
    
    /*FOR EACH s-list:
        DELETE s-list.
    END.
    
    FOR EACH output-list:
        DELETE output-list.
    END.*/

    IF mi-ftd THEN
    DO:    
      IF date2 LT (ci-date - 1) THEN d2 = date2. 
      ELSE d2  = (ci-date - 1). 

    END. 
    ELSE 
    DO: 
      d2     = date2.
    END.  

    ASSIGN 
        mm     = MONTH(d2)
        yy     = YEAR(d2)
        /*date1  = DATE(1,1,yy)*/
        f-date = DATE(MONTH(d2),1,YEAR(d2))
        beg-date = DATE(MONTH(date1),1,yy).

    IF date1 NE ci-date AND date1 GE ci-date THEN d1 = date1.
    ELSE d1 = date1.

    ASSIGN 
      mm     = MONTH(d2).
      yy     = YEAR(d2). 
      f-date = DATE(MONTH(d2),1,YEAR(d2)).
    
    /* Rd, #746, 26Mar2025 , variable tmpdate */
    tmpdate = d1 + 1.
    bydate = d2 - tmpdate.
    /* bydate = d2 - d1 + 1. */       /*william E3CA2B*/

    tdate = d2.

    DO WHILE bydate NE 0:   /*william, makes the data read sort bydate to makes it easier to calculate the othRev E3CA2B*/
        
    FOR EACH genstat WHERE genstat.datum EQ tdate
        /*genstat.datum GE d1 
        AND genstat.datum LE d2*/ 
        AND genstat.zinr NE "" 
        AND genstat.gastnr NE 0 
        AND genstat.resstatus NE 13
        /*AND genstat.res-int[1] NE 13*/
        AND genstat.segmentcode NE 0 
        AND genstat.res-logic[2] EQ YES 
        USE-INDEX date_ix NO-LOCK,
        FIRST guest WHERE guest.gastnr = genstat.gastnr 
        NO-LOCK BY guest.NAME BY guest.gastnr :

        IF genstat.datum NE tdatum THEN     /*william do other logic*/
        DO:
            tdatum = genstat.datum.
            do-dat = YES.
        END.
        ELSE
        DO: 
            do-dat = NO.
        END.

        FIND FIRST zimmer WHERE zimmer.zinr = genstat.zinr 
            NO-LOCK NO-ERROR. 
        FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode
            NO-LOCK NO-ERROR.
        IF cardtype LT 3 THEN do-it = guest.karteityp = cardtype.
        ELSE do-it = YES.
        
        IF NOT incl-comp AND genstat.zipreis = 0 THEN
        DO:
          IF (genstat.gratis GT 0) THEN do-it = NO.
          IF (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis = 0)
           AND genstat.resstatus NE 13 THEN do-it = NO.
        END.

        IF do-it AND sales-ID NE ? AND sales-ID NE "" THEN
        do-it = guest.phonetik3 = TRIM(ENTRY(1, sales-ID, "-")).

        IF do-it THEN
        DO:
            IF genstat.zipreis = 0 THEN
            DO:
              IF (genstat.gratis GT 0) 
                OR ((genstat.erwachs + genstat.kind1 + genstat.kind2 
                + genstat.gratis = 0) AND genstat.resstatus NE 13) THEN 
              DO:
                IF genstat.datum = d2 THEN c-room = c-room + 1.
                IF MONTH(genstat.datum) = mm AND YEAR(genstat.datum) = yy THEN 
                 mc-room = mc-room + 1.
                 yc-room = yc-room + 1.
              END.
            END.
            FIND FIRST s-list WHERE s-list.gastnr = genstat.gastnr
                AND s-list.segm-code = genstat.segmentcode
                NO-ERROR.
            IF NOT AVAILABLE s-list THEN
            DO:
                CREATE s-list.
                ASSIGN s-list.gastnr = genstat.gastnr
                    s-list.compname  = guest.NAME + " " + guest.vorname1 
                    + " " + guest.anrede1 + guest.anredefirma
                    s-list.segm-code = genstat.segmentcode.
                IF AVAILABLE segment THEN
                    s-list.segment  = segment.bezeich.
                ELSE s-list.segment = translateExtended("UNKNOWN", lvCAREA, "").

                     /*s-list.datum*/
            END.

            service = 0.
            vat = 0 .
             FIND FIRST htparam WHERE htparam.paramnr = 127 NO-LOCK NO-ERROR.
                 IF AVAILABLE htparam THEN status-vat = htparam.flogical.
            FIND FIRST arrangement WHERE arrangement.arrangement = genstat.argt NO-LOCK.
            FIND FIRST artikel WHERE artikel.artnr = arrangement.argt-artikelnr AND 
                artikel.departement = 0 NO-LOCK. 
                        IF AVAILABLE artikel AND status-vat = YES THEN 
                 RUN calc-servvat.p(artikel.departement, artikel.artnr, genstat.datum, artikel.service-code, 
                        artikel.mwst-code, OUTPUT service, OUTPUT vat).

            rmrev = genstat.rateLocal.
            IF rm-serv THEN
            DO:
                rmrev = rmrev / ( 1 + service + vat).
            END.
                

            IF mi-ftd AND d2 LT ci-date THEN
            DO:
              IF genstat.datum = d2 THEN /*d1->d2*/
              DO: 
                IF incl-comp THEN
                DO:
                  ASSIGN
                     s-list.room   = s-list.room     + 1
                     room          = room            + 1
                     s-list.pax    = s-list.pax      + genstat.erwachs 
                                     + genstat.kind1 + genstat.kind2 
                                     + genstat.gratis
                     pax           = pax             + genstat.erwachs
                                     + genstat.kind1 + genstat.kind2 
                                     + genstat.gratis
                     s-list.logis  = s-list.logis    + genstat.logis
                     logis         = logis           + genstat.logis
                     avrgrate      = avrgrate        + rmrev. 
                END.
                ELSE
                DO:
                  IF genstat.gratis EQ 0 THEN
                  DO:
                    ASSIGN
                      s-list.room   = s-list.room     + 1
                      room          = room            + 1
                      s-list.pax    = s-list.pax      + genstat.erwachs 
                                      + genstat.kind1 + genstat.kind2 
                      pax           = pax             + genstat.erwachs
                                      + genstat.kind1 + genstat.kind2 
                      s-list.logis  = s-list.logis    + genstat.logis
                      logis         = logis           + genstat.logis
                      avrgrate      = avrgrate        + rmrev.              
                  END.
                END.
              END.

              IF MONTH(genstat.datum) = mm THEN
              DO:
                IF incl-comp THEN
                DO:
                  ASSIGN
                     s-list.m-room      = s-list.m-room  + 1
                     m-room             = m-room  + 1
                     s-list.m-pax       = s-list.m-pax     + genstat.erwachs
                                          + genstat.kind1  + genstat.kind2
                                          + genstat.gratis
                     s-list.m-logis     = s-list.m-logis   + genstat.logis
                     m-pax              = m-pax            + genstat.erwachs
                                          + genstat.kind1  + genstat.kind2
                                          + genstat.gratis
                     m-logis            = m-logis          + genstat.logis
                     m-avrgrate         = m-avrgrate       + rmrev.
                END.
                ELSE
                DO:
                  IF genstat.gratis EQ 0 THEN
                  DO:
                     ASSIGN
                       s-list.m-room      = s-list.m-room  + 1
                       m-room             = m-room  + 1
                       s-list.m-pax       = s-list.m-pax     + genstat.erwachs
                                            + genstat.kind1  + genstat.kind2
                       s-list.m-logis     = s-list.m-logis   + genstat.logis
                       m-pax              = m-pax            + genstat.erwachs
                                            + genstat.kind1  + genstat.kind2
                       m-logis            = m-logis          + genstat.logis
                       m-avrgrate         = m-avrgrate       + rmrev.
                  END.
                END.
              END.

              IF genstat.datum GE d1 AND genstat.datum LE d2 THEN
              DO:
                 IF incl-comp THEN
                 DO:
                   ASSIGN 
                      s-list.y-room      = s-list.y-room  + 1
                      y-room             = y-room  + 1
                      s-list.y-pax       = s-list.y-pax     + genstat.erwachs
                                           + genstat.kind1  + genstat.kind2
                                           + genstat.gratis
                      s-list.y-logis     = s-list.y-logis   + genstat.logis
                      y-pax              = y-pax            + genstat.erwachs
                                           + genstat.kind1  + genstat.kind2
                                           + genstat.gratis
                      y-logis            = y-logis          + genstat.logis
                      y-avrgrate         = y-avrgrate       + rmrev.
                   s-list.revenue = s-list.revenue + genstat.logis.
                   /*IF do-dat THEN
                   DO:
                       RUN calc-othRev (genstat.datum, OUTPUT othRev).     /*william E3CA2B*/
                       ASSIGN
                           s-list.revenue = s-list.revenue + othRev.
                   END.*/    
                 END.
                 ELSE
                 DO:
                   IF genstat.gratis EQ 0 THEN
                   DO:
                     ASSIGN 
                       s-list.y-room      = s-list.y-room  + 1
                       y-room             = y-room  + 1
                       s-list.y-pax       = s-list.y-pax     + genstat.erwachs
                                            + genstat.kind1  + genstat.kind2
                                            + genstat.gratis
                       s-list.y-logis     = s-list.y-logis   + genstat.logis
                       y-pax              = y-pax            + genstat.erwachs
                                            + genstat.kind1  + genstat.kind2
                                            + genstat.gratis
                       y-logis            = y-logis          + genstat.logis
                       y-avrgrate         = y-avrgrate       + rmrev.
                     s-list.revenue = s-list.revenue + genstat.logis.
                     /*IF do-dat THEN
                     DO:
                         RUN calc-othRev (genstat.datum, OUTPUT othRev).     /*william E3CA2B*/
                         ASSIGN
                             s-list.revenue = s-list.revenue + othRev.
                     END.*/
                   END.
                 END.
              END.
            END.

            ELSE IF NOT mi-ftd AND d2 LT ci-date THEN
            DO:
              IF genstat.datum = to-date THEN
              DO:
                 IF incl-comp THEN
                 DO:
                   ASSIGN
                      s-list.room   = s-list.room     + 1
                      room          = room            + 1
                      s-list.pax    = s-list.pax      + genstat.erwachs 
                                      + genstat.kind1 + genstat.kind2 
                                      + genstat.gratis
                      pax           = pax             + genstat.erwachs
                                      + genstat.kind1 + genstat.kind2 
                                      + genstat.gratis
                      s-list.logis  = s-list.logis    + genstat.logis
                      logis         = logis           + genstat.logis
                      avrgrate      = avrgrate        + rmrev.
                 END.
                 ELSE
                 DO:
                   IF genstat.gratis EQ 0 THEN
                   DO:
                     ASSIGN
                       s-list.room   = s-list.room     + 1
                       room          = room            + 1
                       s-list.pax    = s-list.pax      + genstat.erwachs 
                                       + genstat.kind1 + genstat.kind2 
                       pax           = pax             + genstat.erwachs
                                       + genstat.kind1 + genstat.kind2 
                       s-list.logis  = s-list.logis    + genstat.logis
                       logis         = logis           + genstat.logis
                       avrgrate      = avrgrate        + rmrev.
                   END.
                 END.
              END.

              IF /*MONTH(genstat.datum) = mm AND*/ YEAR(genstat.datum) = yy THEN 
              DO:
                  IF incl-comp THEN
                  DO:
                      IF MONTH(genstat.datum) = mm AND YEAR(genstat.datum) = yy THEN
                      DO:
                        ASSIGN
                            s-list.m-room      = s-list.m-room  + 1
                            m-room             = m-room  + 1
                            s-list.m-pax       = s-list.m-pax     + genstat.erwachs
                                                 + genstat.kind1  + genstat.kind2
                                                 + genstat.gratis
                            s-list.m-logis     = s-list.m-logis   + genstat.logis
                            m-pax              = m-pax            + genstat.erwachs
                                                 + genstat.kind1  + genstat.kind2
                                                 + genstat.gratis
                            m-logis            = m-logis          + genstat.logis
                            m-avrgrate         = m-avrgrate       + rmrev.
                      END.
              
                      ASSIGN 
                          s-list.y-room      = s-list.y-room  + 1
                          y-room             = y-room  + 1
                          s-list.y-pax       = s-list.y-pax     + genstat.erwachs
                                               + genstat.kind1  + genstat.kind2
                                               + genstat.gratis
                          s-list.y-logis     = s-list.y-logis   + genstat.logis
                          y-pax              = y-pax            + genstat.erwachs
                                               + genstat.kind1  + genstat.kind2
                                               + genstat.gratis
                          y-logis            = y-logis          + genstat.logis
                          y-avrgrate         = y-avrgrate       + rmrev.
                      s-list.revenue = s-list.revenue + genstat.logis.
                      /*IF do-dat THEN
                      DO:
                          RUN calc-othRev (genstat.datum, OUTPUT othRev).     /*william E3CA2B*/
                          ASSIGN
                              s-list.revenue = s-list.revenue + othRev.
                      END.*/ 
                          /*s-list.y-fixcost   = s-list.y-fixcost + genstat.zipreis  /*william*/
                          y-fixcost   = y-fixcost + genstat.zipreis. */   
                  END.
                  ELSE
                  DO:
                      IF genstat.gratis EQ 0 THEN
                      DO:
                        IF MONTH(genstat.datum) = mm AND YEAR(genstat.datum) = yy THEN
                        DO:
                          ASSIGN
                            s-list.m-room      = s-list.m-room  + 1
                            m-room             = m-room  + 1
                            s-list.m-pax       = s-list.m-pax     + genstat.erwachs
                                                 + genstat.kind1  + genstat.kind2
                            s-list.m-logis     = s-list.m-logis   + genstat.logis
                            m-pax              = m-pax            + genstat.erwachs
                                                 + genstat.kind1  + genstat.kind2
                            m-logis            = m-logis          + genstat.logis
                            m-avrgrate         = m-avrgrate       + rmrev.
                        END.
              
                        ASSIGN 
                          s-list.y-room      = s-list.y-room  + 1
                          y-room             = y-room  + 1
                          s-list.y-pax       = s-list.y-pax     + genstat.erwachs
                                               + genstat.kind1  + genstat.kind2
                                               + genstat.gratis
                          s-list.y-logis     = s-list.y-logis   + genstat.logis
                          y-pax              = y-pax            + genstat.erwachs
                                               + genstat.kind1  + genstat.kind2
                                               + genstat.gratis
                          y-logis            = y-logis          + genstat.logis
                          y-avrgrate         = y-avrgrate       + rmrev.
                        s-list.revenue = s-list.revenue + genstat.logis.
                        /*IF do-dat THEN
                        DO:
                            RUN calc-othRev (genstat.datum, OUTPUT othRev).     /*william E3CA2B*/
                            ASSIGN
                                s-list.revenue = s-list.revenue + othRev.
                        END.*/ 
                          /*s-list.y-fixcost   = s-list.y-fixcost + genstat.zipreis  /*william*/
                          y-fixcost   = y-fixcost + genstat.zipreis. */
                      END.
                  END.
              END.
            END.

          FOR EACH s-list:
            

            IF (s-list.room - s-list.c-room) NE 0 THEN
              s-list.avrgrate = s-list.logis / (s-list.room - s-list.c-room).
            IF (s-list.m-room - s-list.mc-room) NE 0 THEN 
              s-list.m-avrgrate = s-list.m-logis / (s-list.m-room - s-list.mc-room). 
            IF (s-list.y-room - s-list.yc-room) NE 0 THEN 
              s-list.y-avrgrate = s-list.y-logis / (s-list.y-room - s-list.yc-room). 
            IF logis NE 0 THEN 
              s-list.proz = s-list.logis / logis * 100. 
            IF m-logis NE 0 THEN 
              s-list.m-proz = s-list.m-logis / m-logis * 100. 
            IF y-logis NE 0 THEN 
              s-list.y-proz = s-list.y-logis / y-logis * 100.
          END.      /* each s-list*/

          ASSIGN 
              gt-room   = 0
              gtc-room  = 0
              gt-pax    = 0
              gt-logis  = 0
              gt-avrgrate = 0
              gtm-room  = 0
              gtmc-room = 0
              gtm-pax   = 0
              gtm-logis = 0
              gtm-avrgrate = 0
              gty-room  = 0
              gty-pax   = 0
              gtyc-room = 0
              gty-pax   = 0
              gty-logis = 0
              gty-avrgrate = 0
              gty-revenue = 0.      /*william E3CA2B*/

          FOR EACH s-list NO-LOCK:
              ASSIGN
                  gt-room       = gt-room   + s-list.room
                  gtc-room      = gtc-room  + s-list.c-room
                  gt-pax        = gt-pax    + s-list.pax
                  gt-logis      = gt-logis  + s-list.logis
                  gt-avrgrate   = gt-avrgrate   + s-list.avrgrate
                  gtm-room      = gtm-room      + s-list.m-room
                  gtmc-room     = gtmc-room     + s-list.mc-room
                  gtm-pax       = gtm-pax       + s-list.m-pax
                  gtm-logis     = gtm-logis     + s-list.m-logis
                  gtm-avrgrate  = gtm-avrgrate  + s-list.m-avrgrate
                  gty-room      = gty-room      + s-list.y-room
                  gtyc-room     = gtyc-room     + s-list.yc-room
                  gty-pax       = gty-pax       + s-list.y-pax
                  gty-logis     = gty-logis     + s-list.y-logis
                  gty-avrgrate  = gty-avrgrate  + s-list.y-avrgrate 
                  gty-revenue   = gty-revenue   + s-list.revenue.     /*william E3CA2B*/
          END.
        END.
    END. /* each genstat*/
        tdate  = tdate - 1.     /*william E3CA2B*/
        bydate = bydate - 1.
    END.
    /*IF sorttype = 0 THEN RUN create-output.
    ELSE RUN create-output1.*/
END.

PROCEDURE create-umsatz2:  /*history*/
    DEFINE INPUT PARAMETER date1 AS DATE.
    DEFINE INPUT PARAMETER date2 AS DATE.

    DEFINE VARIABLE rmrev      AS DECIMAL NO-UNDO.
    DEFINE VARIABLE service    AS DECIMAL NO-UNDO.
    DEFINE VARIABLE vat        AS DECIMAL NO-UNDO.
    DEFINE VARIABLE do-it      AS LOGICAL.
    DEFINE VARIABLE i          AS INTEGER INITIAL 0.
    DEFINE VARIABLE s          AS CHAR.
    DEFINE VARIABLE curr-code  AS CHAR.
    DEFINE VARIABLE status-vat AS LOGICAL NO-UNDO.
    DEFINE VARIABLE beg-date    AS DATE NO-UNDO.
    DEFINE VARIABLE tdatum     AS DATE NO-UNDO.     /*william E3CA2B*/
    DEFINE VARIABLE do-dat     AS LOGICAL.          /*william E3CA2B*/
    DEFINE VARIABLE bydate     AS INTEGER NO-UNDO.

    ASSIGN
      room    = 0
      c-room  = 0
      pax     = 0
      logis   = 0

      m-room  = 0
      mc-room = 0
      m-pax   = 0
      m-logis = 0

      y-room  = 0
      yc-room = 0
      y-pax   = 0
      y-logis = 0
      revenue = 0

      gt-room       = 0
      gt-pax        = 0
      gt-logis      = 0
      gt-avrgrate   = 0
      gtm-room      = 0
      gtm-pax       = 0
      gtm-logis     = 0
      gtm-avrgrate  = 0
      gtm-room      = 0
      gtm-pax       = 0
      gtm-logis     = 0
      gtm-avrgrate  = 0
      gty-room      = 0
      gty-pax       = 0
      gty-logis     = 0
      gty-avrgrate  = 0
      gty-revenue   = 0
      . 
    
    /*FOR EACH output-list:
        DELETE output-list.
    END.

    FOR EACH s-list:
        DELETE s-list.
    END.*/

    IF mi-ftd THEN
    DO:    
      IF date2 LT (ci-date - 1) THEN d2 = date2. 
      ELSE d2  = (ci-date - 1). 
    END. 
    ELSE 
    DO: 
      d2     = date2.
    END.  

    ASSIGN 
        mm     = MONTH(d2)
        yy     = YEAR(d2)
        /*date1  = DATE(1,1,yy)*/
        f-date = DATE(MONTH(d2),1,YEAR(d2))
        beg-date = DATE(MONTH(date1),1,yy).

    IF date1 NE ci-date AND date1 GE ci-date THEN d1 = date1.
    ELSE d1 = date1.

    ASSIGN 
      mm     = MONTH(d2).
      yy     = YEAR(d2). 
      f-date = DATE(MONTH(d2),1,YEAR(d2)).

    /* Rd, #746, 26Mar2025 , variable tmpdate */
    tmpdate = d1 + 1.
    bydate = d2 - tmpdate.
    
    /* bydate = d2 - d1 + 1. */       /*william E3CA2B*/

    tdate = d2.

    DO WHILE bydate NE 0:   /*william, makes the data read sort bydate to makes it easier to calculate the othRev E3CA2B*/
    
    FOR EACH genstat WHERE genstat.datum EQ tdate
        /*genstat.datum GE d1 
        AND genstat.datum LE d2*/ 
        AND genstat.zinr NE "" 
        AND genstat.gastnr NE 0 
        AND genstat.resstatus NE 13
        /*AND genstat.res-int[1] NE 13*/
        AND genstat.segmentcode NE 0 
        AND genstat.res-logic[2] EQ YES 
        USE-INDEX DATE_ix NO-LOCK,
        FIRST guest WHERE guest.gastnr = genstat.gastnr 
        NO-LOCK BY guest.NAME BY guest.gastnr:

        IF genstat.datum NE tdatum THEN     /*william do other logic*/
        DO:
            tdatum = genstat.datum.
            do-dat = YES.
        END.
        ELSE do-dat = NO.
        
        FIND FIRST zimmer WHERE zimmer.zinr = genstat.zinr 
            NO-LOCK NO-ERROR. 
        FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode
            NO-LOCK NO-ERROR.
        IF cardtype LT 3 THEN do-it = guest.karteityp = cardtype.
        ELSE do-it = YES.

        IF NOT incl-comp AND genstat.zipreis = 0 THEN
        DO:
            IF genstat.gratis GT 0 THEN do-it = NO.
            IF (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis = 0)
                AND genstat.resstatus NE 13 THEN do-it = NO.
        END.

        IF do-it AND sales-ID NE ? AND sales-ID NE "" THEN
        do-it = guest.phonetik3 = TRIM(ENTRY(1, sales-ID, "-")).

        IF do-it THEN
        DO:
            IF genstat.zipreis = 0 THEN
            DO:
                IF (genstat.gratis GT 0) OR 
                    ((genstat.erwachs + genstat.kind1 + genstat.kind2
                      + genstat.gratis = 0) AND genstat.resstatus NE 13) THEN
                DO:
                    IF genstat.datum = date2 THEN c-room = c-room + 1.
                    IF MONTH(genstat.datum) = mm AND YEAR(genstat.datum) = yy THEN 
                       mc-room = mc-room + 1.
                    yc-room = yc-room + 1.
                END.
            END.
            
            FIND FIRST segment WHERE genstat.segmentcode = segment.segmentcode NO-LOCK NO-ERROR.
                
            IF AVAILABLE segment THEN
            FIND FIRST queasy WHERE queasy.KEY = 26 
                AND queasy.number1 = segment.segmentgrup NO-LOCK NO-ERROR.

            FIND FIRST s-list WHERE s-list.gastnr = genstat.gastnr
                AND s-list.segm-code = genstat.segmentcode
                AND s-list.segm-grup = queasy.number1
                NO-LOCK NO-ERROR.
              
            IF NOT AVAILABLE s-list THEN
            DO:
                CREATE s-list.
                ASSIGN s-list.gastnr = genstat.gastnr
                    s-list.compname  = guest.NAME + " " + guest.vorname1 
                    + " " + guest.anrede1 + guest.anredefirma
                    s-list.segm-code = genstat.segmentcode.
                IF AVAILABLE segment THEN
                    ASSIGN
                    s-list.segment  = segment.bezeich 
                    s-list.segm-grup = segment.segmentgrup.
                ELSE s-list.segment = translateExtended("UNKNOWN", lvCAREA, "").
                IF AVAILABLE queasy THEN
                    s-list.segment1 = queasy.char3.   
                ELSE s-list.segment1 = translateExtended("UNKNOWN", lvCAREA, "").
            END.

            service = 0.
            vat = 0 .
            FIND FIRST htparam WHERE htparam.paramnr = 127 NO-LOCK NO-ERROR.
            IF AVAILABLE htparam THEN status-vat = htparam.flogical.
            FIND FIRST arrangement WHERE arrangement.arrangement = genstat.argt NO-LOCK.
            FIND FIRST artikel WHERE artikel.artnr = arrangement.argt-artikelnr AND 
                artikel.departement = 0 NO-LOCK. 
             IF AVAILABLE artikel AND status-vat = YES THEN 
                 RUN calc-servvat.p(artikel.departement, artikel.artnr, genstat.datum, artikel.service-code, 
                        artikel.mwst-code, OUTPUT service, OUTPUT vat).

            rmrev = genstat.rateLocal.
            IF rm-serv THEN
            DO:
                rmrev = rmrev / ( 1 + service + vat).
            END.
                

            IF mi-ftd AND d2 LT ci-date THEN
            DO:
              IF genstat.datum = d1 THEN
              DO: 
                IF incl-comp THEN
                DO:
                  ASSIGN
                     s-list.room   = s-list.room     + 1
                     room          = room            + 1
                     s-list.pax    = s-list.pax      + genstat.erwachs 
                                     + genstat.kind1 + genstat.kind2 
                                     + genstat.gratis
                     pax           = pax             + genstat.erwachs
                                     + genstat.kind1 + genstat.kind2 
                                     + genstat.gratis
                     s-list.logis  = s-list.logis    + genstat.logis
                     logis         = logis           + genstat.logis
                     avrgrate      = avrgrate        + rmrev.                
                  END.
                ELSE
                DO:
                  IF genstat.gratis EQ 0 THEN
                  DO:
                    ASSIGN
                      s-list.room   = s-list.room     + 1
                      room          = room            + 1
                      s-list.pax    = s-list.pax      + genstat.erwachs 
                                      + genstat.kind1 + genstat.kind2 
                      pax           = pax             + genstat.erwachs
                                      + genstat.kind1 + genstat.kind2 
                      s-list.logis  = s-list.logis    + genstat.logis
                      logis         = logis           + genstat.logis
                      avrgrate      = avrgrate        + rmrev.
                  END.
                END.
              END.

              IF MONTH(genstat.datum) = mm THEN
              DO:
                IF incl-comp THEN
                DO:
                  ASSIGN
                     s-list.m-room      = s-list.m-room  + 1
                     m-room             = m-room  + 1
                     s-list.m-pax       = s-list.m-pax     + genstat.erwachs
                                          + genstat.kind1  + genstat.kind2
                                          + genstat.gratis
                     s-list.m-logis     = s-list.m-logis   + genstat.logis
                     m-pax              = m-pax            + genstat.erwachs
                                          + genstat.kind1  + genstat.kind2
                                          + genstat.gratis
                     m-logis            = m-logis          + genstat.logis
                     m-avrgrate         = m-avrgrate       + rmrev.
                END.
                ELSE
                DO:
                  IF genstat.gratis EQ 0 THEN
                  DO:
                     ASSIGN
                       s-list.m-room      = s-list.m-room  + 1
                       m-room             = m-room  + 1
                       s-list.m-pax       = s-list.m-pax     + genstat.erwachs
                                            + genstat.kind1  + genstat.kind2
                       s-list.m-logis     = s-list.m-logis   + genstat.logis
                       m-pax              = m-pax            + genstat.erwachs
                                            + genstat.kind1  + genstat.kind2
                       m-logis            = m-logis          + genstat.logis
                       m-avrgrate         = m-avrgrate       + rmrev.
                  END.
                END.
              END.

              IF genstat.datum GE d1 AND genstat.datum LE d2 THEN
              DO:
                 IF incl-comp THEN
                 DO:
                   ASSIGN 
                      s-list.y-room      = s-list.y-room  + 1
                      y-room             = y-room  + 1
                      s-list.y-pax       = s-list.y-pax     + genstat.erwachs
                                           + genstat.kind1  + genstat.kind2
                                           + genstat.gratis
                      s-list.y-logis     = s-list.y-logis   + genstat.logis
                      y-pax              = y-pax            + genstat.erwachs
                                           + genstat.kind1  + genstat.kind2
                                           + genstat.gratis
                      y-logis            = y-logis          + genstat.logis
                      y-avrgrate         = y-avrgrate       + rmrev.
                   s-list.revenue = s-list.revenue + genstat.logis.
                   /*IF do-dat THEN
                   DO:
                       RUN calc-othRev (genstat.datum, OUTPUT othRev).     /*william E3CA2B*/
                       ASSIGN
                           s-list.revenue = s-list.revenue + othRev.
                   END.*/ 
                      /*s-list.y-fixcost   = s-list.y-fixcost + genstat.res-deci[6] 
                      y-fixcost          = y-fixcost + genstat.res-deci[6] .  */   /*william E3CA2B*/
                 END.
                 ELSE
                 DO:
                   IF genstat.gratis EQ 0 THEN
                   DO:
                     ASSIGN 
                       s-list.y-room      = s-list.y-room  + 1
                       y-room             = y-room  + 1
                       s-list.y-pax       = s-list.y-pax     + genstat.erwachs
                                            + genstat.kind1  + genstat.kind2
                                            + genstat.gratis
                       s-list.y-logis     = s-list.y-logis   + genstat.logis
                       y-pax              = y-pax            + genstat.erwachs
                                            + genstat.kind1  + genstat.kind2
                                            + genstat.gratis
                       y-logis            = y-logis          + genstat.logis
                       y-avrgrate         = y-avrgrate       + rmrev.
                     s-list.revenue = s-list.revenue + genstat.logis.
                     /*IF do-dat THEN
                     DO:
                         RUN calc-othRev (genstat.datum, OUTPUT othRev).     /*william E3CA2B*/
                         ASSIGN
                             s-list.revenue = s-list.revenue + othRev.
                     END.*/ 
                       /*s-list.y-fixcost   = s-list.y-fixcost + genstat.res-deci[6] 
                       y-fixcost          = y-fixcost + genstat.res-deci[6]. */    /*william E3CA2B*/
                   END.
                 END.
              END.
            END.

            ELSE IF NOT mi-ftd AND d2 LT ci-date THEN
            DO:
              IF genstat.datum = to-date THEN
              DO:
                 IF incl-comp THEN
                 DO:
                   ASSIGN
                      s-list.room   = s-list.room     + 1
                      room          = room            + 1
                      s-list.pax    = s-list.pax      + genstat.erwachs 
                                      + genstat.kind1 + genstat.kind2 
                                      + genstat.gratis
                      pax           = pax             + genstat.erwachs
                                      + genstat.kind1 + genstat.kind2 
                                      + genstat.gratis
                      s-list.logis  = s-list.logis    + genstat.logis
                      logis         = logis           + genstat.logis
                      avrgrate      = avrgrate        + rmrev.
                 END.
                 ELSE
                 DO:
                   IF genstat.gratis EQ 0 THEN
                   DO:
                     ASSIGN
                       s-list.room   = s-list.room     + 1
                       room          = room            + 1
                       s-list.pax    = s-list.pax      + genstat.erwachs 
                                       + genstat.kind1 + genstat.kind2 
                       pax           = pax             + genstat.erwachs
                                       + genstat.kind1 + genstat.kind2 
                       s-list.logis  = s-list.logis    + genstat.logis
                       logis         = logis           + genstat.logis
                       avrgrate      = avrgrate        + rmrev.
                   END.
                 END.
              END.

              IF /*MONTH(genstat.datum) = mm AND*/ YEAR(genstat.datum) = yy THEN 
              DO:
                  IF incl-comp THEN
                  DO:
                      IF MONTH(genstat.datum) = mm AND YEAR(genstat.datum) = yy THEN
                      DO:
                        ASSIGN
                            s-list.m-room      = s-list.m-room  + 1
                            m-room             = m-room  + 1
                            s-list.m-pax       = s-list.m-pax     + genstat.erwachs
                                                 + genstat.kind1  + genstat.kind2
                                                 + genstat.gratis
                            s-list.m-logis     = s-list.m-logis   + genstat.logis
                            m-pax              = m-pax            + genstat.erwachs
                                                 + genstat.kind1  + genstat.kind2
                                                 + genstat.gratis
                            m-logis            = m-logis          + genstat.logis
                            m-avrgrate         = m-avrgrate       + rmrev.
                      END.
              
                      ASSIGN 
                          s-list.y-room      = s-list.y-room  + 1
                          y-room             = y-room  + 1
                          s-list.y-pax       = s-list.y-pax     + genstat.erwachs
                                               + genstat.kind1  + genstat.kind2
                                               + genstat.gratis
                          s-list.y-logis     = s-list.y-logis   + genstat.logis
                          y-pax              = y-pax            + genstat.erwachs
                                               + genstat.kind1  + genstat.kind2
                                               + genstat.gratis
                          y-logis            = y-logis          + genstat.logis
                          y-avrgrate         = y-avrgrate       + rmrev.
                      s-list.revenue = s-list.revenue + genstat.logis.
                      /*IF do-dat THEN
                      DO:
                          RUN calc-othRev (genstat.datum, OUTPUT othRev).     /*william E3CA2B*/
                          ASSIGN
                              s-list.revenue = s-list.revenue + othRev.
                      END. */
                          /*s-list.y-fixcost   = s-list.y-fixcost + genstat.res-deci[6] 
                          y-fixcost          = y-fixcost + genstat.res-deci[6]. */    /*william E3CA2B*/
                  END.
                  ELSE
                  DO:
                      IF genstat.gratis EQ 0 THEN
                      DO:
                        IF MONTH(genstat.datum) = mm AND YEAR(genstat.datum) = yy THEN
                        DO:
                          ASSIGN
                            s-list.m-room      = s-list.m-room  + 1
                            m-room             = m-room  + 1
                            s-list.m-pax       = s-list.m-pax     + genstat.erwachs
                                                 + genstat.kind1  + genstat.kind2
                            s-list.m-logis     = s-list.m-logis   + genstat.logis
                            m-pax              = m-pax            + genstat.erwachs
                                                 + genstat.kind1  + genstat.kind2
                            m-logis            = m-logis          + genstat.logis
                            m-avrgrate         = m-avrgrate       + rmrev.
                        END.
              
                        ASSIGN 
                          s-list.y-room      = s-list.y-room  + 1
                          y-room             = y-room  + 1
                          s-list.y-pax       = s-list.y-pax     + genstat.erwachs
                                               + genstat.kind1  + genstat.kind2
                                               + genstat.gratis
                          s-list.y-logis     = s-list.y-logis   + genstat.logis
                          y-pax              = y-pax            + genstat.erwachs
                                               + genstat.kind1  + genstat.kind2
                                               + genstat.gratis
                          y-logis            = y-logis          + genstat.logis
                          y-avrgrate         = y-avrgrate       + rmrev.
                        s-list.revenue = s-list.revenue + genstat.logis.
                        /*IF do-dat THEN
                        DO:
                            RUN calc-othRev (genstat.datum, OUTPUT othRev).     /*william E3CA2B*/
                            ASSIGN
                                s-list.revenue = s-list.revenue + othRev.
                        END.*/ 
                          /*s-list.y-fixcost   = s-list.y-fixcost + genstat.res-deci[6]
                          y-fixcost          = y-fixcost + genstat.res-deci[6]. */    /*william E3CA2B*/
                      END.
                  END.
              END.
            END.
            
           /*RUN calc-othRev (genstat.datum, OUTPUT othRev).     /*william E3CA2B*/
           ASSIGN
               s-list.y-fixcost = s-list.y-fixcost + othRev.*/
            
          FOR EACH s-list:
           

            IF (s-list.room - s-list.c-room) NE 0 THEN 
              s-list.avrgrate = s-list.logis / (s-list.room - s-list.c-room). 
            IF (s-list.m-room - s-list.mc-room) NE 0 THEN 
              s-list.m-avrgrate = s-list.m-logis / (s-list.m-room - s-list.mc-room). 
            IF (s-list.y-room - s-list.yc-room) NE 0 THEN 
              s-list.y-avrgrate = s-list.y-logis / (s-list.y-room - s-list.yc-room). 
            IF logis NE 0 THEN 
              s-list.proz = s-list.logis / logis * 100. 
            IF m-logis NE 0 THEN 
              s-list.m-proz = s-list.m-logis / m-logis * 100. 
            IF y-logis NE 0 THEN 
              s-list.y-proz = s-list.y-logis / y-logis * 100.
          END.      /* each s-list*/

          ASSIGN 
              gt-room       = 0
              gtc-room      = 0
              gt-pax        = 0
              gt-logis      = 0
              gt-avrgrate   = 0
              gtm-room      = 0
              gtmc-room     = 0
              gtm-pax       = 0
              gtm-logis     = 0
              gtm-avrgrate  = 0
              gty-room      = 0
              gty-pax       = 0
              gtyc-room     = 0
              gty-pax       = 0
              gty-logis     = 0
              gty-avrgrate  = 0
              gty-revenue   = 0.

          FOR EACH s-list NO-LOCK:
              ASSIGN
                  gt-room       = gt-room + s-list.room
                  gtc-room      = gtc-room + s-list.c-room
                  gt-pax        = gt-pax   + s-list.pax
                  gt-logis      = gt-logis + s-list.logis
                  gt-avrgrate   = gt-avrgrate + s-list.avrgrate
                  gtm-room      = gtm-room + s-list.m-room
                  gtmc-room     = gtmc-room + s-list.mc-room
                  gtm-pax       = gtm-pax + s-list.m-pax
                  gtm-logis     = gtm-logis + s-list.m-logis
                  gtm-avrgrate  = gtm-avrgrate + s-list.m-avrgrate
                  gty-room      = gty-room + s-list.y-room
                  gtyc-room     = gtyc-room + s-list.yc-room
                  gty-pax       = gty-pax + s-list.y-pax
                  gty-logis     = gty-logis + s-list.y-logis
                  gty-avrgrate  = gty-avrgrate + s-list.y-avrgrate
                  gty-revenue   = gty-revenue + s-list.revenue.
          END.

        END.
     
    END. /* each genstat*/
        tdate  = tdate - 1.     /*william E3CA2B*/
        bydate = bydate - 1.
    END.
    /*RUN create-output2.*/
END.

PROCEDURE create-fcast:   /*forecast*/
    DEFINE INPUT PARAMETER date1 AS DATE.
    DEFINE INPUT PARAMETER date2 AS DATE.

    DEFINE VARIABLE rmrev      AS DECIMAL NO-UNDO.
    DEFINE VARIABLE service    AS DECIMAL NO-UNDO.
    DEFINE VARIABLE vat        AS DECIMAL NO-UNDO.
    DEFINE VARIABLE mm         AS INTEGER NO-UNDO. 
    DEFINE VARIABLE yy         AS INTEGER NO-UNDO. 
    DEFINE VARIABLE do-it      AS LOGICAL NO-UNDO. 
    DEFINE VARIABLE i          AS INTEGER INITIAL 0 NO-UNDO.
    DEFINE VARIABLE s          AS CHAR NO-UNDO.
    DEFINE VARIABLE curr-code  AS CHAR NO-UNDO.
    DEFINE VARIABLE status-vat AS LOGICAL NO-UNDO.
    DEFINE VARIABLE fdate      AS DATE.
    DEFINE VARIABLE beg-date   AS DATE NO-UNDO.

    DEFINE VARIABLE datum           AS DATE.
    DEFINE VARIABLE datum1          AS DATE.
    DEFINE VARIABLE datum2          AS DATE.
    DEFINE VARIABLE d2              AS DATE.
    DEFINE VARIABLE local-net-lodg  AS DECIMAL.
    DEFINE VARIABLE net-lodg        AS DECIMAL.
    DEFINE VARIABLE t-pax             AS INTEGER NO-UNDO. 
    DEFINE VARIABLE a               AS INTEGER.
    DEFINE VARIABLE dayuse-flag     AS LOGICAL. 
    DEFINE VARIABLE consider-it     AS LOGICAL.
    DEFINE VARIABLE tot-breakfast   AS DECIMAL.
    DEFINE VARIABLE tot-Lunch       AS DECIMAL.
    DEFINE VARIABLE tot-dinner      AS DECIMAL.
    DEFINE VARIABLE tot-Other       AS DECIMAL.
    DEFINE VAR tot-rmrev            AS DECIMAL INITIAL 0.
    DEFINE VAR tot-vat              AS DECIMAL INITIAL 0.
    DEFINE VAR tot-service          AS DECIMAL INITIAL 0.
    
    DEFINE BUFFER rline1  FOR res-line.
    DEFINE BUFFER gmember FOR guest.
      

    ASSIGN
      room    = 0
      c-room  = 0
      pax     = 0
      logis   = 0

      m-room  = 0
      mc-room = 0
      m-pax   = 0
      m-logis = 0
      
      y-room  = 0 
      yc-room = 0 
      y-pax   = 0 
      y-logis = 0

      gt-room = 0
      gt-pax = 0
      gt-logis = 0
      gt-avrgrate = 0
      gtm-room = 0
      gtm-pax = 0
      gtm-logis = 0
      gtm-avrgrate = 0
      gtm-room = 0
      gtm-pax = 0
      gtm-logis = 0
      gtm-avrgrate = 0
      gty-room = 0
      gty-pax = 0
      gty-logis = 0
      gty-avrgrate = 0
      gty-revenue = 0
      .

    /*FOR EACH s-list:
        DELETE s-list.
    END.

    FOR EACH output-list:
        DELETE output-list.
    END.*/
    
    ASSIGN 
        mm     = MONTH(date2)
        yy     = YEAR(date2)
        f-date = DATE(MONTH(date2),1,YEAR(date2)).

    IF date1 LT ci-date THEN d1 = ci-date.
    ELSE d1 = date1.
    datum1 = d1.
    IF date2 LE (ci-date - 1) THEN d2 = ci-date.
    ELSE d2 = date2.

    FOR EACH res-line WHERE 
        (res-line.active-flag LE 1 AND res-line.resstatus LE 13 
         AND res-line.resstatus NE 4 
         AND res-line.resstatus NE 8
         AND res-line.resstatus NE 9 
         AND res-line.resstatus NE 10
         AND res-line.resstatus NE 12
         AND res-line.active-flag LE 1
         AND NOT (res-line.ankunft GT d2 ) AND 
         NOT (res-line.abreise LT d1)) OR
        (res-line.active-flag = 2 AND res-line.resstatus = 8 
         AND res-line.ankunft = ci-date AND res-line.abreise = ci-date) 
         AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] = 0
         USE-INDEX gnrank_ix NO-LOCK,
         FIRST guest WHERE guest.gastnr = res-line.gastnr 
         NO-LOCK BY guest.NAME BY guest.gastnr:

        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
            NO-LOCK NO-ERROR.
        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr 
            NO-LOCK NO-ERROR. 
        
        ASSIGN
            tot-breakfast = 0
            tot-lunch     = 0
            tot-dinner    = 0
            tot-other     = 0
            dayuse-flag   = NO.

        IF NOT vhp-limited THEN do-it = YES.
        ELSE
        DO:
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
              NO-LOCK NO-ERROR.
            do-it = AVAILABLE segment AND segment.vip-level = 0.
        END.

       IF do-it AND res-line.resstatus = 8 THEN
        DO:
            dayuse-flag = YES.     
            FIND FIRST arrangement WHERE arrangement.arrangement 
              =  res-line.arrangement NO-LOCK. 
            FIND FIRST bill-line WHERE bill-line.departement = 0
              AND bill-line.artnr = arrangement.argt-artikelnr
              AND bill-line.bill-datum = ci-date
              AND bill-line.massnr = res-line.resnr
              AND bill-line.billin-nr = res-line.reslinnr
              USE-INDEX dep-art-dat_ix NO-LOCK NO-ERROR.
            do-it = AVAILABLE bill-line.
        END.

        IF cardtype LT 3 THEN do-it = guest.karteityp = cardtype.
        ELSE do-it = YES.

        IF NOT incl-comp AND res-line.zipreis = 0 THEN
        DO:
          IF (res-line.gratis GT 0) THEN do-it = NO.
          IF (res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis = 0)
           AND res-line.resstatus NE 13 THEN do-it = NO.
        END.

        IF do-it AND sales-ID NE ? AND sales-ID NE "" THEN
        do-it = guest.phonetik3 = TRIM(ENTRY(1, sales-ID, "-")).

        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
        IF do-it AND AVAILABLE zimmer THEN 
        DO: 
            /* Malik Serverless 746 */
            IF datum NE ? THEN
            DO:
              FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
                AND queasy.date1 LE datum AND queasy.date2 GE datum NO-LOCK NO-ERROR. 
              IF zimmer.sleeping THEN 
              DO: 
                  IF AVAILABLE queasy AND queasy.number3 EQ res-line.gastnr THEN 
                    do-it = NO. 
              END. 
              ELSE 
              DO: 
                  IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN . 
                  ELSE do-it = NO. 
              END. 
            END.
            /* END Malik */
        END. 
        
        IF do-it THEN
        DO: 
            CREATE t-list.
            ASSIGN
                t-list.gastnr    = res-line.gastnr
                t-list.resstatus = res-line.resstatus.

            FIND FIRST s-list WHERE s-list.gastnr = res-line.gastnr NO-ERROR.
            IF NOT AVAILABLE s-list THEN
            DO:
                CREATE s-list.
                ASSIGN s-list.gastnr = res-line.gastnr
                    s-list.compname  = guest.NAME + " " + guest.vorname1 
                    + " " + guest.anrede1 + guest.anredefirma
                    s-list.segm-code = reservation.segmentcode.
            END.

            FIND FIRST segment WHERE segment.segmentcode = s-list.segm-code NO-LOCK NO-ERROR.
            IF AVAILABLE segment THEN s-list.segment  = segment.bezeich.
            ELSE s-list.segment = translateExtended("UNKNOWN", lvCAREA, "").

            IF res-line.ankunft GE d1 THEN datum1 = res-line.ankunft.
            ELSE datum1 = d1.
            IF res-line.abreise LE d2 THEN datum2 = res-line.abreise - 1.
            ELSE datum2 = d2.

            DO datum = datum1 TO datum2:
                a = a + 1.
                t-pax = res-line.erwachs.
                local-net-lodg = 0.
                net-lodg  = 0.
                FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                    AND reslin-queasy.resnr = res-line.resnr 
                    AND reslin-queasy.reslinnr = res-line.reslinnr 
                    AND reslin-queasy.date1 LE datum 
                    AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 
                IF AVAILABLE reslin-queasy AND reslin-queasy.number3 NE 0 THEN 
                    pax = reslin-queasy.number3. 

                consider-it = YES.
                IF res-line.zimmerfix THEN
                DO:
                    FIND FIRST rline1 WHERE rline1.resnr = res-line.resnr 
                      AND rline1.reslinnr NE res-line.reslinnr 
                      AND rline1.resstatus EQ 8 /*and rline1.erwachs GT 0*/ 
                      AND rline1.abreise GT datum NO-LOCK NO-ERROR. 
                    IF AVAILABLE rline1 THEN consider-it = NO. 
                END.

                /* START Breakfast lunch Dinner other From Room Rev*/
                ASSIGN 
                    local-net-lodg  = 0
                    net-lodg        = 0
                    tot-rmrev       = 0. 

                RUN get-room-breakdown.p(RECID(res-line), datum, 0, /*date1*/ from-date,
                                         OUTPUT net-lodg, OUTPUT local-net-lodg,
                                         OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                         OUTPUT tot-dinner, OUTPUT tot-other,
                                         OUTPUT tot-rmrev, OUTPUT tot-vat,
                                         OUTPUT tot-service).
                IF tot-rmrev = 0 THEN  
                ASSIGN 
                    local-net-lodg      = 0
                    net-lodg            = 0. 

                t-list.zipreis          = t-list.zipreis + (tot-rmrev * res-line.zimmeranz).   
                s-list.revenue          = s-list.revenue + local-net-lodg.

                IF res-line.zipreis = 0 THEN
                DO:
                  IF (res-line.gratis GT 0) 
                      OR ((res-line.erwachs + res-line.kind1 + res-line.kind2 
                      + res-line.gratis = 0) AND res-line.resstatus NE 13) THEN
                  DO:
                    IF datum = date2 THEN c-room = c-room + 1.
                    IF MONTH(datum) = mm AND YEAR(datum) = yy THEN
                    DO:
                      mc-room = mc-room + 1.
                      yc-room = yc-room + 1.
                    END.
                  END.
                END.

                IF mi-ftd AND datum = d1 AND from-date GE d1 AND consider-it THEN  /*Today*/
                DO:
                  ASSIGN
                     s-list.logis  = s-list.logis + local-net-lodg
                     logis         = logis + local-net-lodg
                     s-list.room   = s-list.room + res-line.zimmeranz
                     room          = room + res-line.zimmeranz
                     s-list.pax    = s-list.pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                      + res-line.gratis) * res-line.zimmeranz
                     pax           = pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                      + res-line.gratis) * res-line.zimmeranz
                     avrgrate      = avrgrate + t-list.zipreis.                   
                  
                  IF NOT incl-comp THEN
                  DO:
                    IF res-line.zipreis EQ 0 THEN
                    DO:
                       ASSIGN
                         s-list.logis  = s-list.logis + local-net-lodg
                         logis         = logis + local-net-lodg
                         s-list.room   = s-list.room + res-line.zimmeranz
                         room          = room + res-line.zimmeranz
                         s-list.pax    = s-list.pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                           + res-line.gratis) * res-line.zimmeranz
                         pax           = pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                           + res-line.gratis) * res-line.zimmeranz
                         avrgrate      = avrgrate + t-list.zipreis.                       
                    END.
                  END.
                END. 
                
                IF NOT mi-ftd AND datum = d2 AND consider-it THEN  /*Today*/
                DO:
                  ASSIGN
                     s-list.logis  = s-list.logis + local-net-lodg
                     logis         = logis + local-net-lodg
                     s-list.room   = s-list.room + res-line.zimmeranz
                     room          = room + res-line.zimmeranz
                     s-list.pax    = s-list.pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                      + res-line.gratis) * res-line.zimmeranz
                     pax           = pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                      + res-line.gratis) * res-line.zimmeranz
                     avrgrate      = avrgrate + t-list.zipreis.                   
                  
                  IF NOT incl-comp THEN
                  DO:
                    IF res-line.zipreis EQ 0 THEN
                    DO:
                       ASSIGN
                         s-list.logis  = s-list.logis + local-net-lodg
                         logis         = logis + local-net-lodg
                         s-list.room   = s-list.room + res-line.zimmeranz
                         room          = room + res-line.zimmeranz
                         s-list.pax    = s-list.pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                           + res-line.gratis) * res-line.zimmeranz
                         pax           = pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                           + res-line.gratis) * res-line.zimmeranz
                         avrgrate      = avrgrate + t-list.zipreis.                       
                    END.
                  END.
                END. 
                  
                IF mi-ftd AND MONTH(datum) = MONTH(d2) AND YEAR(datum) = YEAR(d2) THEN
                DO:
                  ASSIGN
                     s-list.m-logis  = s-list.m-logis + local-net-lodg
                     m-logis         = m-logis + local-net-lodg
                     s-list.m-room   = s-list.m-room + res-line.zimmeranz
                     m-room          = m-room + res-line.zimmeranz
                     s-list.m-pax    = s-list.m-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                       + res-line.gratis) * res-line.zimmeranz
                     m-pax           = m-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                       + res-line.gratis) * res-line.zimmeranz
                     m-avrgrate      = m-avrgrate + t-list.zipreis.                    
                  
                  IF NOT incl-comp THEN 
                  DO:
                    IF res-line.zipreis EQ 0 THEN
                    DO:
                      ASSIGN
                        s-list.m-logis  = s-list.m-logis + local-net-lodg
                        m-logis         = m-logis + local-net-lodg
                        s-list.m-room   = s-list.m-room + res-line.zimmeranz
                        m-room          = m-room + res-line.zimmeranz
                        s-list.m-pax    = s-list.m-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                          + res-line.gratis) * res-line.zimmeranz
                        m-pax           = m-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                          + res-line.gratis) * res-line.zimmeranz
                        m-avrgrate      = m-avrgrate + t-list.zipreis.                        
                    END.
                  END.
                END.
                
                IF mi-ftd AND datum GE d1 AND datum LE d2 THEN
                DO:
                  ASSIGN
                     s-list.y-logis  = s-list.y-logis + local-net-lodg
                     y-logis         = y-logis + local-net-lodg
                     s-list.y-room   = s-list.y-room + res-line.zimmeranz
                     y-room          = y-room + res-line.zimmeranz
                     s-list.y-pax    = s-list.y-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                       + res-line.gratis) * res-line.zimmeranz
                     y-pax           = y-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                       + res-line.gratis) * res-line.zimmeranz
                     y-avrgrate      = y-avrgrate + t-list.zipreis.                   
                  
                  IF NOT incl-comp THEN
                  DO:
                    IF res-line.zipreis EQ 0 THEN
                    DO:
                      ASSIGN
                         s-list.y-logis  = s-list.y-logis + local-net-lodg
                         y-logis         = y-logis + local-net-lodg
                         s-list.y-room   = s-list.y-room + res-line.zimmeranz
                         y-room          = y-room + res-line.zimmeranz
                         s-list.y-pax    = s-list.y-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                           + res-line.gratis) * res-line.zimmeranz
                         y-pax           = y-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                           + res-line.gratis) * res-line.zimmeranz
                         y-avrgrate      = y-avrgrate + t-list.zipreis.                       
                    END.
                  END.
                END.
                
                IF NOT mi-ftd AND MONTH(datum) = MONTH(d2) AND YEAR(datum) = YEAR(d2) THEN
                DO:
                    ASSIGN
                       s-list.m-logis  = s-list.m-logis + local-net-lodg
                       m-logis         = m-logis + local-net-lodg
                       s-list.m-room   = s-list.m-room + res-line.zimmeranz
                       m-room          = m-room + res-line.zimmeranz
                       s-list.m-pax    = s-list.m-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                         + res-line.gratis) * res-line.zimmeranz
                       m-pax           = m-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                         + res-line.gratis) * res-line.zimmeranz
                       m-avrgrate      = m-avrgrate + t-list.zipreis.                      
                
                  IF NOT incl-comp THEN
                  DO:
                    IF res-line.zipreis EQ 0 THEN
                    DO:
                      ASSIGN
                         s-list.m-logis  = s-list.m-logis + local-net-lodg
                         m-logis         = m-logis + local-net-lodg
                         s-list.m-room   = s-list.m-room + res-line.zimmeranz
                         m-room          = m-room + res-line.zimmeranz
                         s-list.m-pax    = s-list.m-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                           + res-line.gratis) * res-line.zimmeranz
                         m-pax           = m-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                           + res-line.gratis) * res-line.zimmeranz
                         m-avrgrate      = m-avrgrate + t-list.zipreis.                         
                    END.
                  END.
                END.
                
                
                IF NOT mi-ftd AND datum GE d1 AND datum LE d2 THEN
                DO:
                  ASSIGN
                     s-list.y-logis  = s-list.y-logis + local-net-lodg
                     y-logis         = y-logis + local-net-lodg
                     s-list.y-room   = s-list.y-room + res-line.zimmeranz
                     y-room          = y-room + res-line.zimmeranz
                     s-list.y-pax    = s-list.y-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                       + res-line.gratis) * res-line.zimmeranz
                     y-pax           = y-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                       + res-line.gratis) * res-line.zimmeranz
                     y-avrgrate      = y-avrgrate + t-list.zipreis.                  
                
                  IF NOT incl-comp THEN
                  DO:
                    IF res-line.zipreis EQ 0 THEN
                    DO:
                      ASSIGN
                         s-list.y-logis  = s-list.y-logis + local-net-lodg
                         y-logis         = y-logis + local-net-lodg
                         s-list.y-room   = s-list.y-room + res-line.zimmeranz
                         y-room          = y-room + res-line.zimmeranz
                         s-list.y-pax    = s-list.y-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                           + res-line.gratis) * res-line.zimmeranz
                         y-pax           = y-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                           + res-line.gratis) * res-line.zimmeranz
                         y-avrgrate      = y-avrgrate + t-list.zipreis.                      
                    END.
                  END.
                END.
            END.

          FOR EACH s-list:
            IF (s-list.room - s-list.c-room) NE 0 THEN
              s-list.avrgrate = s-list.logis / (s-list.room - s-list.c-room).
            IF (s-list.m-room - s-list.mc-room) NE 0 THEN 
              s-list.m-avrgrate = s-list.m-logis / (s-list.m-room - s-list.mc-room). 
            IF (s-list.y-room - s-list.yc-room) NE 0 THEN 
              s-list.y-avrgrate = s-list.y-logis / (s-list.y-room - s-list.yc-room). 
            IF logis NE 0 THEN 
              s-list.proz = s-list.logis / logis * 100. 
            IF m-logis NE 0 THEN 
              s-list.m-proz = s-list.m-logis / m-logis * 100. 
            IF y-logis NE 0 THEN 
              s-list.y-proz = s-list.y-logis / y-logis * 100. 
          END.      /* each s-list*/

          ASSIGN 
              gt-room   = 0
              gtc-room  = 0
              gt-pax    = 0
              gt-logis  = 0
              gt-avrgrate = 0
              gtm-room  = 0
              gtmc-room = 0
              gtm-pax   = 0
              gtm-logis = 0
              gtm-avrgrate = 0
              gty-room  = 0
              gty-pax   = 0
              gtyc-room = 0
              gty-pax   = 0
              gty-logis = 0
              gty-avrgrate = 0
              gty-revenue = 0.

          FOR EACH s-list NO-LOCK:
              ASSIGN
                  gt-room       = gt-room   + s-list.room
                  gtc-room      = gtc-room  + s-list.c-room
                  gt-pax        = gt-pax    + s-list.pax
                  gt-logis      = gt-logis  + s-list.logis
                  gt-avrgrate   = gt-avrgrate   + s-list.avrgrate
                  gtm-room      = gtm-room      + s-list.m-room
                  gtmc-room     = gtmc-room     + s-list.mc-room
                  gtm-pax       = gtm-pax       + s-list.m-pax
                  gtm-logis     = gtm-logis     + s-list.m-logis
                  gtm-avrgrate  = gtm-avrgrate  + s-list.m-avrgrate
                  gty-room      = gty-room      + s-list.y-room
                  gtyc-room     = gtyc-room     + s-list.yc-room
                  gty-pax       = gty-pax       + s-list.y-pax
                  gty-logis     = gty-logis     + s-list.y-logis
                  gty-avrgrate  = gty-avrgrate  + s-list.y-avrgrate
                  gty-revenue   = gty-revenue   + s-list.revenue.
          END.
        END.
    END. /* each genstat*/
    /*IF sorttype = 0 THEN RUN create-output.
    ELSE RUN create-output1.*/
END.

PROCEDURE create-fcast2:   /*forecast*/
    DEFINE INPUT PARAMETER date1 AS DATE.
    DEFINE INPUT PARAMETER date2 AS DATE.

    DEFINE VARIABLE rmrev      AS DECIMAL NO-UNDO.
    DEFINE VARIABLE service    AS DECIMAL NO-UNDO.
    DEFINE VARIABLE vat        AS DECIMAL NO-UNDO.
    DEFINE VARIABLE mm         AS INTEGER NO-UNDO. 
    DEFINE VARIABLE yy         AS INTEGER NO-UNDO. 
    DEFINE VARIABLE do-it      AS LOGICAL NO-UNDO. 
    DEFINE VARIABLE i          AS INTEGER INITIAL 0 NO-UNDO.
    DEFINE VARIABLE s          AS CHAR NO-UNDO.
    DEFINE VARIABLE curr-code  AS CHAR NO-UNDO.
    DEFINE VARIABLE status-vat AS LOGICAL NO-UNDO.
    DEFINE VARIABLE fdate      AS DATE.
    DEFINE VARIABLE beg-date   AS DATE NO-UNDO.

    DEFINE VARIABLE datum           AS DATE.
    DEFINE VARIABLE datum1          AS DATE.
    DEFINE VARIABLE datum2          AS DATE.
    DEFINE VARIABLE d2              AS DATE.
    DEFINE VARIABLE local-net-lodg  AS DECIMAL.
    DEFINE VARIABLE net-lodg        AS DECIMAL.
    DEFINE VARIABLE t-pax           AS INTEGER NO-UNDO. 
    DEFINE VARIABLE a               AS INTEGER.
    DEFINE VARIABLE dayuse-flag     AS LOGICAL. 
    DEFINE VARIABLE consider-it     AS LOGICAL.
    DEFINE VARIABLE tot-breakfast   AS DECIMAL.
    DEFINE VARIABLE tot-Lunch       AS DECIMAL.
    DEFINE VARIABLE tot-dinner      AS DECIMAL.
    DEFINE VARIABLE tot-Other       AS DECIMAL.
    DEFINE VAR tot-rmrev            AS DECIMAL INITIAL 0.
    DEFINE VAR tot-vat              AS DECIMAL INITIAL 0.
    DEFINE VAR tot-service          AS DECIMAL INITIAL 0.
    
    DEFINE BUFFER rline1  FOR res-line.
    DEFINE BUFFER gmember FOR guest.

    ASSIGN
      room    = 0
      c-room  = 0
      pax     = 0
      logis   = 0

      m-room  = 0
      mc-room = 0
      m-pax   = 0
      m-logis = 0
      
      y-room  = 0 
      yc-room = 0 
      y-pax   = 0 
      y-logis = 0

      gt-room = 0
      gt-pax = 0
      gt-logis = 0
      gt-avrgrate = 0
      gtm-room = 0
      gtm-pax = 0
      gtm-logis = 0
      gtm-avrgrate = 0
      gtm-room = 0
      gtm-pax = 0
      gtm-logis = 0
      gtm-avrgrate = 0
      gty-room = 0
      gty-pax = 0
      gty-logis = 0
      gty-avrgrate = 0
      gty-revenue = 0
      .

    /*FOR EACH s-list:
        DELETE s-list.
    END.

    FOR EACH output-list:
        DELETE output-list.
    END.*/

    ASSIGN 
        mm     = MONTH(date2)
        yy     = YEAR(date2)
        f-date = DATE(MONTH(date2),1,YEAR(date2)).

    IF date1 LT ci-date THEN d1 = ci-date.
    ELSE d1 = date1.
    datum1 = d1.
    IF date2 LE (ci-date - 1) THEN d2 = ci-date.
    ELSE d2 = date2.

    FOR EACH res-line WHERE 
        (res-line.active-flag LE 1 AND res-line.resstatus LE 13 
         AND res-line.resstatus NE 4 
         AND res-line.resstatus NE 8
         AND res-line.resstatus NE 9 
         AND res-line.resstatus NE 10
         AND res-line.resstatus NE 12
         AND res-line.active-flag LE 1
         AND NOT (res-line.ankunft GT d2) AND 
         NOT (res-line.abreise LT d1)) OR
        (res-line.active-flag = 2 AND res-line.resstatus = 8 
         AND res-line.ankunft = ci-date AND res-line.abreise = ci-date) 
         AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] = 0
         USE-INDEX gnrank_ix NO-LOCK,
         FIRST guest WHERE guest.gastnr = res-line.gastnr 
         NO-LOCK BY guest.NAME BY guest.gastnr:

        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
            NO-LOCK NO-ERROR.
        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr 
            NO-LOCK NO-ERROR. 
        
        ASSIGN
            tot-breakfast = 0
            tot-lunch     = 0
            tot-dinner    = 0
            tot-other     = 0
            dayuse-flag   = NO.

        IF NOT vhp-limited THEN do-it = YES.
        ELSE
        DO:
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
              NO-LOCK NO-ERROR.
            do-it = AVAILABLE segment AND segment.vip-level = 0.
        END.

       IF do-it AND res-line.resstatus = 8 THEN
        DO:
            dayuse-flag = YES.     
            FIND FIRST arrangement WHERE arrangement.arrangement 
              =  res-line.arrangement NO-LOCK. 
            FIND FIRST bill-line WHERE bill-line.departement = 0
              AND bill-line.artnr = arrangement.argt-artikelnr
              AND bill-line.bill-datum = ci-date
              AND bill-line.massnr = res-line.resnr
              AND bill-line.billin-nr = res-line.reslinnr
              USE-INDEX dep-art-dat_ix NO-LOCK NO-ERROR.
            do-it = AVAILABLE bill-line.
        END.

        IF cardtype LT 3 THEN do-it = guest.karteityp = cardtype.
        ELSE do-it = YES.

        IF NOT incl-comp AND res-line.zipreis = 0 THEN
        DO:
          IF (res-line.gratis GT 0) THEN do-it = NO.
          IF (res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis = 0)
           AND res-line.resstatus NE 13 THEN do-it = NO.
        END.

        IF do-it AND sales-ID NE ? AND sales-ID NE "" THEN
        do-it = guest.phonetik3 = TRIM(ENTRY(1, sales-ID, "-")).

        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
        IF do-it AND AVAILABLE zimmer THEN 
        DO: 
            FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
              AND queasy.date1 LE datum AND queasy.date2 GE datum NO-LOCK NO-ERROR. 
            IF zimmer.sleeping THEN 
            DO: 
                IF AVAILABLE queasy AND queasy.number3 EQ res-line.gastnr THEN 
                  do-it = NO. 
            END. 
            ELSE 
            DO: 
                IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN . 
                ELSE do-it = NO. 
            END. 
        END. 
        
        IF do-it THEN
        DO: 
            CREATE t-list.
            ASSIGN
                t-list.gastnr    = res-line.gastnr
                t-list.resstatus = res-line.resstatus.

            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
            IF AVAILABLE segment THEN
                FIND FIRST queasy WHERE queasy.KEY = 26 
                AND queasy.number1 = segment.segmentgrup NO-LOCK NO-ERROR.

            FIND FIRST s-list WHERE s-list.gastnr = res-line.gastnr 
                AND s-list.segm-code = segment.segmentcode
                AND s-list.segm-grup = queasy.number1 NO-ERROR.
            IF NOT AVAILABLE s-list THEN
            DO:
                CREATE s-list.
                ASSIGN s-list.gastnr = res-line.gastnr
                    s-list.compname  = guest.NAME + " " + guest.vorname1 
                    + " " + guest.anrede1 + guest.anredefirma.
                IF AVAILABLE segment THEN
                ASSIGN
                    s-list.segment  = segment.bezeich 
                    s-list.segm-code = reservation.segmentcode
                    s-list.segm-grup = segment.segmentgrup.
                ELSE s-list.segment = translateExtended("UNKNOWN", lvCAREA, "").
                IF AVAILABLE queasy THEN
                    s-list.segment1 = queasy.char3.   
                ELSE s-list.segment1 = translateExtended("UNKNOWN", lvCAREA, "").
            END.

            IF res-line.ankunft GE d1 THEN datum1 = res-line.ankunft.
            ELSE datum1 = d1.
            IF res-line.abreise LE d2 THEN datum2 = res-line.abreise - 1.
            ELSE datum2 = d2.

            DO datum = datum1 TO datum2:
                a = a + 1.
                t-pax = res-line.erwachs.
                local-net-lodg = 0.
                net-lodg  = 0.
                FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                    AND reslin-queasy.resnr = res-line.resnr 
                    AND reslin-queasy.reslinnr = res-line.reslinnr 
                    AND reslin-queasy.date1 LE datum 
                    AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 
                IF AVAILABLE reslin-queasy AND reslin-queasy.number3 NE 0 THEN 
                    pax = reslin-queasy.number3. 

                consider-it = YES.
                IF res-line.zimmerfix THEN
                DO:
                    FIND FIRST rline1 WHERE rline1.resnr = res-line.resnr 
                      AND rline1.reslinnr NE res-line.reslinnr 
                      AND rline1.resstatus EQ 8 /*and rline1.erwachs GT 0*/ 
                      AND rline1.abreise GT datum NO-LOCK NO-ERROR. 
                    IF AVAILABLE rline1 THEN consider-it = NO. 
                END.

                /* START Breakfast lunch Dinner other From Room Rev*/
                ASSIGN 
                    local-net-lodg  = 0
                    net-lodg        = 0
                    tot-rmrev       = 0. 

                RUN get-room-breakdown.p(RECID(res-line), datum, 0, /*date1*/ from-date,
                                         OUTPUT net-lodg, OUTPUT local-net-lodg,
                                         OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                         OUTPUT tot-dinner, OUTPUT tot-other,
                                         OUTPUT tot-rmrev, OUTPUT tot-vat,
                                         OUTPUT tot-service).
                IF tot-rmrev = 0 THEN  
                ASSIGN 
                    local-net-lodg      = 0
                    net-lodg            = 0. 

                t-list.zipreis          = t-list.zipreis + (tot-rmrev * res-line.zimmeranz).
                s-list.revenue          = s-list.revenue + local-net-lodg.

                IF res-line.zipreis = 0 THEN
                DO:
                  IF (res-line.gratis GT 0) 
                      OR ((res-line.erwachs + res-line.kind1 + res-line.kind2 
                      + res-line.gratis = 0) AND res-line.resstatus NE 13) THEN
                  DO:
                    IF datum = d2 THEN c-room = c-room + 1.
                    IF MONTH(datum) = mm AND YEAR(datum) = yy THEN
                    DO:
                      mc-room = mc-room + 1.
                      yc-room = yc-room + 1.
                    END.
                  END.
                END.

                IF mi-ftd AND datum = d2 AND from-date GE d1 AND consider-it THEN  /*Today*/
                DO:
                  ASSIGN
                     s-list.logis  = s-list.logis + local-net-lodg
                     logis         = logis + local-net-lodg
                     s-list.room   = s-list.room + res-line.zimmeranz
                     room          = room + res-line.zimmeranz
                     s-list.pax    = s-list.pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                      + res-line.gratis) * res-line.zimmeranz
                     pax           = pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                      + res-line.gratis) * res-line.zimmeranz
                     avrgrate      = avrgrate + t-list.zipreis.
                  
                  IF NOT incl-comp THEN
                  DO:
                    IF res-line.zipreis EQ 0 THEN
                    DO:
                       ASSIGN
                         s-list.logis  = s-list.logis + local-net-lodg
                         logis         = logis + local-net-lodg
                         s-list.room   = s-list.room + res-line.zimmeranz
                         room          = room + res-line.zimmeranz
                         s-list.pax    = s-list.pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                           + res-line.gratis) * res-line.zimmeranz
                         pax           = pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                           + res-line.gratis) * res-line.zimmeranz
                         avrgrate      = avrgrate + t-list.zipreis.
                    END.
                  END.
                END. 

                IF NOT mi-ftd AND datum = d2 AND consider-it THEN  /*Today*/
                DO:
                  ASSIGN
                     s-list.logis  = s-list.logis + local-net-lodg
                     logis         = logis + local-net-lodg
                     s-list.room   = s-list.room + res-line.zimmeranz
                     room          = room + res-line.zimmeranz
                     s-list.pax    = s-list.pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                      + res-line.gratis) * res-line.zimmeranz
                     pax           = pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                      + res-line.gratis) * res-line.zimmeranz
                     avrgrate      = avrgrate + t-list.zipreis.
                  
                  IF NOT incl-comp THEN
                  DO:
                    IF res-line.zipreis EQ 0 THEN
                    DO:
                       ASSIGN
                         s-list.logis  = s-list.logis + local-net-lodg
                         logis         = logis + local-net-lodg
                         s-list.room   = s-list.room + res-line.zimmeranz
                         room          = room + res-line.zimmeranz
                         s-list.pax    = s-list.pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                           + res-line.gratis) * res-line.zimmeranz
                         pax           = pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                           + res-line.gratis) * res-line.zimmeranz
                         avrgrate      = avrgrate + t-list.zipreis.
                    END.
                  END.
                END. 

                IF NOT mi-ftd AND /*MONTH(genstat.datum) = mm AND*/ YEAR(datum) = YEAR(d2) THEN
                DO:
                  IF MONTH(datum) = MONTH(d2) AND YEAR(datum) = YEAR(d2) THEN   /*MTD*/
                  DO:
                    ASSIGN
                       s-list.m-logis  = s-list.m-logis + local-net-lodg
                       m-logis         = m-logis + local-net-lodg
                       s-list.m-room   = s-list.m-room + res-line.zimmeranz
                       m-room          = m-room + res-line.zimmeranz
                       s-list.m-pax    = s-list.m-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                         + res-line.gratis) * res-line.zimmeranz
                       m-pax           = m-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                         + res-line.gratis) * res-line.zimmeranz
                       m-avrgrate      = m-avrgrate + t-list.zipreis.   

                    ASSIGN
                       s-list.y-logis  = s-list.y-logis + local-net-lodg
                       y-logis         = y-logis + local-net-lodg
                       s-list.y-room   = s-list.y-room + res-line.zimmeranz
                       y-room          = y-room + res-line.zimmeranz
                       s-list.y-pax    = s-list.y-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                         + res-line.gratis) * res-line.zimmeranz
                       y-pax           = y-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                         + res-line.gratis) * res-line.zimmeranz
                       y-avrgrate      = y-avrgrate + t-list.zipreis.
                  END.

                  IF NOT incl-comp THEN
                  DO:
                    IF res-line.zipreis EQ 0 THEN
                    DO:
                      IF MONTH(datum) = MONTH(d2) AND YEAR(datum) = YEAR(d2) THEN   /*MTD*/
                      DO:
                        ASSIGN
                           s-list.m-logis  = s-list.m-logis + local-net-lodg
                           m-logis         = m-logis + local-net-lodg
                           s-list.m-room   = s-list.m-room + res-line.zimmeranz
                           m-room          = m-room + res-line.zimmeranz
                           s-list.m-pax    = s-list.m-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                             + res-line.gratis) * res-line.zimmeranz
                           m-pax           = m-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                             + res-line.gratis) * res-line.zimmeranz
                           m-avrgrate      = m-avrgrate + t-list.zipreis.   
                        
                        ASSIGN
                           s-list.y-logis  = s-list.y-logis + local-net-lodg
                           y-logis         = y-logis + local-net-lodg
                           s-list.y-room   = s-list.y-room + res-line.zimmeranz
                           y-room          = y-room + res-line.zimmeranz
                           s-list.y-pax    = s-list.y-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                             + res-line.gratis) * res-line.zimmeranz
                           y-pax           = y-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                             + res-line.gratis) * res-line.zimmeranz
                           y-avrgrate      = y-avrgrate + t-list.zipreis.
                      END.
                    END.
                  END.
                END.

                IF mi-ftd AND MONTH(datum) = MONTH(d2) AND YEAR(datum) = YEAR(d2) THEN
                DO:
                  ASSIGN
                     s-list.m-logis  = s-list.m-logis + local-net-lodg
                     m-logis         = m-logis + local-net-lodg
                     s-list.m-room   = s-list.m-room + res-line.zimmeranz
                     m-room          = m-room + res-line.zimmeranz
                     s-list.m-pax    = s-list.m-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                       + res-line.gratis) * res-line.zimmeranz
                     m-pax           = m-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                       + res-line.gratis) * res-line.zimmeranz
                     m-avrgrate      = m-avrgrate + t-list.zipreis.   
                  
                  IF NOT incl-comp THEN 
                  DO:
                    IF res-line.zipreis EQ 0 THEN
                    DO:
                      ASSIGN
                        s-list.m-logis  = s-list.m-logis + local-net-lodg
                        m-logis         = m-logis + local-net-lodg
                        s-list.m-room   = s-list.m-room + res-line.zimmeranz
                        m-room          = m-room + res-line.zimmeranz
                        s-list.m-pax    = s-list.m-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                          + res-line.gratis) * res-line.zimmeranz
                        m-pax           = m-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                          + res-line.gratis) * res-line.zimmeranz
                        m-avrgrate      = m-avrgrate + t-list.zipreis.   
                    END.
                  END.
                END.

                IF mi-ftd AND datum GE d1 AND datum LE d2 THEN
                DO:
                  ASSIGN
                     s-list.y-logis  = s-list.y-logis + local-net-lodg
                     y-logis         = y-logis + local-net-lodg
                     s-list.y-room   = s-list.y-room + res-line.zimmeranz
                     y-room          = y-room + res-line.zimmeranz
                     s-list.y-pax    = s-list.y-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                       + res-line.gratis) * res-line.zimmeranz
                     y-pax           = y-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                       + res-line.gratis) * res-line.zimmeranz
                     y-avrgrate      = y-avrgrate + t-list.zipreis.
                  
                  IF NOT incl-comp THEN
                  DO:
                    IF res-line.zipreis EQ 0 THEN
                    DO:
                      ASSIGN
                         s-list.y-logis  = s-list.y-logis + local-net-lodg
                         y-logis         = y-logis + local-net-lodg
                         s-list.y-room   = s-list.y-room + res-line.zimmeranz
                         y-room          = y-room + res-line.zimmeranz
                         s-list.y-pax    = s-list.y-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                           + res-line.gratis) * res-line.zimmeranz
                         y-pax           = y-pax + (t-pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                           + res-line.gratis) * res-line.zimmeranz
                         y-avrgrate      = y-avrgrate + t-list.zipreis.
                    END.
                  END.
                END.
            END.

          FOR EACH s-list:
            IF (s-list.room - s-list.c-room) NE 0 THEN
              s-list.avrgrate = s-list.logis / (s-list.room - s-list.c-room).
            IF (s-list.m-room - s-list.mc-room) NE 0 THEN 
              s-list.m-avrgrate = s-list.m-logis / (s-list.m-room - s-list.mc-room). 
            IF (s-list.y-room - s-list.yc-room) NE 0 THEN 
              s-list.y-avrgrate = s-list.y-logis / (s-list.y-room - s-list.yc-room). 
            IF logis NE 0 THEN 
              s-list.proz = s-list.logis / logis * 100. 
            IF m-logis NE 0 THEN 
              s-list.m-proz = s-list.m-logis / m-logis * 100. 
            IF y-logis NE 0 THEN 
              s-list.y-proz = s-list.y-logis / y-logis * 100. 
          END.      /* each s-list*/

          ASSIGN 
              gt-room   = 0
              gtc-room  = 0
              gt-pax    = 0
              gt-logis  = 0
              gt-avrgrate = 0
              gtm-room  = 0
              gtmc-room = 0
              gtm-pax   = 0
              gtm-logis = 0
              gtm-avrgrate = 0
              gty-room  = 0
              gty-pax   = 0
              gtyc-room = 0
              gty-pax   = 0
              gty-logis = 0
              gty-avrgrate = 0
              gty-revenue = 0.

          FOR EACH s-list NO-LOCK:
              ASSIGN
                  gt-room       = gt-room   + s-list.room
                  gtc-room      = gtc-room  + s-list.c-room
                  gt-pax        = gt-pax    + s-list.pax
                  gt-logis      = gt-logis  + s-list.logis
                  gt-avrgrate   = gt-avrgrate   + s-list.avrgrate
                  gtm-room      = gtm-room      + s-list.m-room
                  gtmc-room     = gtmc-room     + s-list.mc-room
                  gtm-pax       = gtm-pax       + s-list.m-pax
                  gtm-logis     = gtm-logis     + s-list.m-logis
                  gtm-avrgrate  = gtm-avrgrate  + s-list.m-avrgrate
                  gty-room      = gty-room      + s-list.y-room
                  gtyc-room     = gtyc-room     + s-list.yc-room
                  gty-pax       = gty-pax       + s-list.y-pax
                  gty-logis     = gty-logis     + s-list.y-logis
                  gty-avrgrate  = gty-avrgrate  + s-list.y-avrgrate
                  gty-revenue   = gty-revenue   + s-list.revenue.
          END.
        END.
    END. /* each genstat*/
    
    /*RUN create-output2.*/
END.

PROCEDURE create-output:
    DEFINE VARIABLE tot-room AS INTEGER FORMAT "->>>,>>9".
    DEFINE BUFFER sbuff FOR s-list.
    DEFINE VARIABLE i AS INTEGER INITIAL 0.
    DEFINE VARIABLE curr-rmtype AS CHAR INITIAL "".
    DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL -1 NO-UNDO.

    FOR EACH s-list NO-LOCK BY s-list.compname BY s-list.segment:
        i = i + 1.
        IF curr-gastnr NE s-list.gastnr AND curr-gastnr NE -1 THEN
        DO:
            RUN create-sub.
        END.
        IF curr-gastnr NE s-list.gastnr THEN
        DO:
            CREATE rmcomp-segm-list.
            ASSIGN
                rmcomp-segm-list.flag    = 1
                rmcomp-segm-list.segment = s-list.compname.
        END.
        IF price-decimal = 0 THEN
        DO:
            CREATE rmcomp-segm-list.
            RUN count-sub1.
        END.
        ELSE
        DO:
            CREATE rmcomp-segm-list.
            RUN count-sub2.
        END.
        curr-gastnr = s-list.gastnr.
    END.

    RUN create-sub.

    gt-avrgrate = 0.
    IF (gt-room - gtc-room) NE 0 THEN gt-avrgrate = gt-logis / (gt-room - gtc-room). 
    gtm-avrgrate = 0. 
    IF (gtm-room - gtmc-room) NE 0 THEN gtm-avrgrate = gtm-logis / (gtm-room - gtmc-room). 
    gty-avrgrate = 0. 
    IF (gty-room - gtyc-room) NE 0 THEN gty-avrgrate = gty-logis / (gty-room - gtyc-room). 
    

    CREATE rmcomp-segm-list.
    ASSIGN
        rmcomp-segm-list.segment    = translateExtended("T o t a l", lvCAREA, "")
        rmcomp-segm-list.room       = STRING(gt-room, "->>>,>>9")                
        rmcomp-segm-list.pax        = STRING(gt-pax, "->>>,>>9")                 
        rmcomp-segm-list.logis      = STRING(gt-logis, "->>,>>>,>>>,>>>,>>9")    
        rmcomp-segm-list.proz       = "100.00"                                   
        rmcomp-segm-list.avrgrate   = STRING(gt-avrgrate, "->>,>>>,>>>,>>>,>>9") 
        rmcomp-segm-list.m-room     = STRING(gtm-room, "->>>,>>9")               
        rmcomp-segm-list.m-pax      = STRING(gtm-pax, "->>>,>>9")                
        rmcomp-segm-list.m-logis    = STRING(gtm-logis, "->>,>>>,>>>,>>>,>>9")   
        rmcomp-segm-list.m-proz     = "100.00"                                   
        rmcomp-segm-list.m-avrgrate = STRING(gtm-avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcomp-segm-list.y-room     = STRING(gty-room, "->>>,>>9")               
        rmcomp-segm-list.y-pax      = STRING(gty-pax, "->>>,>>9")                
        rmcomp-segm-list.y-logis    = STRING(gty-logis, "->>,>>>,>>>,>>>,>>9")   
        rmcomp-segm-list.y-proz     = "100.00"                                   
        rmcomp-segm-list.y-avrgrate = STRING(gty-avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcomp-segm-list.revenue    = STRING(gty-revenue, "->>,>>>,>>>,>>>,>>9")
    .    
END PROCEDURE.

PROCEDURE create-output1:
    DEFINE VARIABLE tot-room AS INTEGER FORMAT "->>>,>>9".
    DEFINE BUFFER sbuff FOR s-list.
    DEFINE VARIABLE i AS INTEGER INITIAL 0.
    DEFINE VARIABLE curr-segment AS INTEGER NO-UNDO.

    FOR EACH s-list NO-LOCK BY s-list.segment BY s-list.compname:
        i = i + 1.
        IF curr-segment NE s-list.segm-code AND curr-segment NE 0 THEN
        DO:
            RUN create-sub.
        END.
        IF curr-segment NE s-list.segm-code THEN
        DO:
            CREATE rmcomp-segm-list.
            ASSIGN
                rmcomp-segm-list.flag    = 1
                rmcomp-segm-list.segment = s-list.segment.
        END.
        IF price-decimal = 0 THEN
        DO:
            CREATE rmcomp-segm-list.
            RUN count-sub1.
        END.
        ELSE
        DO:
            CREATE rmcomp-segm-list.
            RUN count-sub2.
        END.
        curr-segment = s-list.segm-code.
    END.

    RUN create-sub.

    gt-avrgrate = 0.
    IF (gt-room - gtc-room) NE 0 THEN gt-avrgrate = gt-logis / (gt-room - gtc-room). 
    gtm-avrgrate = 0. 
    IF (gtm-room - gtmc-room) NE 0 THEN gtm-avrgrate = gtm-logis / (gtm-room - gtmc-room). 
    gty-avrgrate = 0. 
    IF (gty-room - gtyc-room) NE 0 THEN gty-avrgrate = gty-logis / (gty-room - gtyc-room). 

    CREATE rmcomp-segm-list.
    ASSIGN
        rmcomp-segm-list.segment    = translateExtended("T o t a l", lvCAREA, "")
        rmcomp-segm-list.room       = STRING(gt-room, "->>>,>>9")                
        rmcomp-segm-list.pax        = STRING(gt-pax, "->>>,>>9")                 
        rmcomp-segm-list.logis      = STRING(gt-logis, "->>,>>>,>>>,>>>,>>9")    
        rmcomp-segm-list.proz       = "100.00"                                   
        rmcomp-segm-list.avrgrate   = STRING(gt-avrgrate, "->>,>>>,>>>,>>>,>>9") 
        rmcomp-segm-list.m-room     = STRING(gtm-room, "->>>,>>9")               
        rmcomp-segm-list.m-pax      = STRING(gtm-pax, "->>>,>>9")                
        rmcomp-segm-list.m-logis    = STRING(gtm-logis, "->>,>>>,>>>,>>>,>>9")   
        rmcomp-segm-list.m-proz     = "100.00"                                   
        rmcomp-segm-list.m-avrgrate = STRING(gtm-avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcomp-segm-list.y-room     = STRING(gty-room, "->>>,>>9")               
        rmcomp-segm-list.y-pax      = STRING(gty-pax, "->>>,>>9")                
        rmcomp-segm-list.y-logis    = STRING(gty-logis, "->>,>>>,>>>,>>>,>>9")   
        rmcomp-segm-list.y-proz     = "100.00"                                   
        rmcomp-segm-list.y-avrgrate = STRING(gty-avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcomp-segm-list.revenue    = STRING(gty-revenue, "->>,>>>,>>>,>>>,>>9")
    .  
END PROCEDURE.

PROCEDURE create-output2:
    DEFINE VARIABLE tot-room AS INTEGER FORMAT "->>>,>>9".
    DEFINE BUFFER sbuff FOR s-list.
    DEFINE VARIABLE i AS INTEGER INITIAL 0.
    DEFINE VARIABLE curr-segment AS INTEGER NO-UNDO.

    FOR EACH s-list NO-LOCK BY s-list.segment BY s-list.compname:
        i = i + 1.
        IF curr-segment NE s-list.segm-grup AND curr-segment NE 0 THEN
        DO:
            RUN create-sub.
        END.
        IF curr-segment NE s-list.segm-grup THEN
        DO:
            CREATE rmcomp-segm-list.
            ASSIGN
                rmcomp-segm-list.flag    = 1
                rmcomp-segm-list.segment = s-list.segment1.
        END.
        IF price-decimal = 0 THEN
        DO:
            CREATE rmcomp-segm-list.
            RUN count-sub1.
        END.
        ELSE
        DO:
            CREATE rmcomp-segm-list.
            RUN count-sub2.
        END.
        curr-segment = s-list.segm-grup.
    END.

    RUN create-sub.
    
    gt-avrgrate = 0.
    IF (gt-room - gtc-room) NE 0 THEN gt-avrgrate = gt-logis / (gt-room - gtc-room). 
    gtm-avrgrate = 0. 
    IF (gtm-room - gtmc-room) NE 0 THEN gtm-avrgrate = gtm-logis / (gtm-room - gtmc-room). 
    gty-avrgrate = 0. 
    IF (gty-room - gtyc-room) NE 0 THEN gty-avrgrate = gty-logis / (gty-room - gtyc-room). 

    CREATE rmcomp-segm-list.
    ASSIGN
        rmcomp-segm-list.segment    = translateExtended("T o t a l", lvCAREA, "")
        rmcomp-segm-list.room       = STRING(gt-room, "->>>,>>9")                
        rmcomp-segm-list.pax        = STRING(gt-pax, "->>>,>>9")                 
        rmcomp-segm-list.logis      = STRING(gt-logis, "->>,>>>,>>>,>>>,>>9")    
        rmcomp-segm-list.proz       = "100.00"                                   
        rmcomp-segm-list.avrgrate   = STRING(gt-avrgrate, "->>,>>>,>>>,>>>,>>9") 
        rmcomp-segm-list.m-room     = STRING(gtm-room, "->>>,>>9")               
        rmcomp-segm-list.m-pax      = STRING(gtm-pax, "->>>,>>9")                
        rmcomp-segm-list.m-logis    = STRING(gtm-logis, "->>,>>>,>>>,>>>,>>9")   
        rmcomp-segm-list.m-proz     = "100.00"                                   
        rmcomp-segm-list.m-avrgrate = STRING(gtm-avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcomp-segm-list.y-room     = STRING(gty-room, "->>>,>>9")               
        rmcomp-segm-list.y-pax      = STRING(gty-pax, "->>>,>>9")                
        rmcomp-segm-list.y-logis    = STRING(gty-logis, "->>,>>>,>>>,>>>,>>9")   
        rmcomp-segm-list.y-proz     = "100.00"                                   
        rmcomp-segm-list.y-avrgrate = STRING(gty-avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcomp-segm-list.revenue    = STRING(gty-revenue, "->>,>>>,>>>,>>>,>>9")
    .          
END PROCEDURE.

PROCEDURE count-sub1:
    IF sorttype = 0 THEN rmcomp-segm-list.segment = s-list.segment.
    ELSE rmcomp-segm-list.segment = s-list.compname.
    
    ASSIGN                          
        rmcomp-segm-list.room       = STRING(s-list.room, "->>>,>>9")                 
        rmcomp-segm-list.pax        = STRING(s-list.pax, "->>>,>>9")                  
        rmcomp-segm-list.logis      = STRING(s-list.logis, "->>,>>>,>>>,>>>,>>9")     
        rmcomp-segm-list.proz       = STRING(s-list.proz, ">>9.99")                   
        rmcomp-segm-list.avrgrate   = STRING(s-list.avrgrate, "->>,>>>,>>>,>>>,>>9")  
        rmcomp-segm-list.m-room     = STRING(s-list.m-room, "->>>,>>9")               
        rmcomp-segm-list.m-pax      = STRING(s-list.m-pax, "->>>,>>9")                
        rmcomp-segm-list.m-logis    = STRING(s-list.m-logis, "->>,>>>,>>>,>>>,>>9")   
        rmcomp-segm-list.m-proz     = STRING(s-list.m-proz, ">>9.99")                 
        rmcomp-segm-list.m-avrgrate = STRING(s-list.m-avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcomp-segm-list.y-room     = STRING(s-list.y-room, "->>>,>>9")               
        rmcomp-segm-list.y-pax      = STRING(s-list.y-pax, "->>>,>>9")                
        rmcomp-segm-list.y-logis    = STRING(s-list.y-logis, "->>,>>>,>>>,>>>,>>9")   
        rmcomp-segm-list.y-proz     = STRING(s-list.y-proz, ">>9.99")                 
        rmcomp-segm-list.y-avrgrate = STRING(s-list.y-avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcomp-segm-list.revenue    = STRING(s-list.revenue, "->>,>>>,>>>,>>>,>>9")

        rmcomp-segm-list.rmnite     = STRING(s-list.y-room, "->>>,>>9")            
        rmcomp-segm-list.rmrev      = STRING(s-list.y-logis, "->>,>>>,>>>,>>>,>>9")
        rmcomp-segm-list.rmnite1    = STRING(s-list.m-room, "->>>,>>9")            
        rmcomp-segm-list.rmrev1     = STRING(s-list.m-logis, "->>,>>>,>>>,>>>,>>9")
        rmcomp-segm-list.gastnr     = s-list.gastnr  
        rmcomp-segm-list.segm-code  = s-list.segm-code
    .
    proz = proz + s-list.proz.
    m-proz = m-proz + s-list.m-proz.
    y-proz = y-proz + s-list.y-proz.
    st-room = st-room + s-list.room.
    st-pax = st-pax  + s-list.pax.
    st-proz = st-proz + s-list.proz.
    st-logis = st-logis + s-list.logis.
    st-avrgrate = st-avrgrate + s-list.avrgrate.
    stm-room = stm-room + s-list.m-room.        
    stm-pax = stm-pax  + s-list.m-pax.
    stm-proz = stm-proz + s-list.m-proz.
    stm-logis = stm-logis + s-list.m-logis.
    stm-avrgrate = stm-avrgrate + s-list.m-avrgrate.
    sty-room = sty-room + s-list.y-room.        
    sty-pax = sty-pax  + s-list.y-pax.
    sty-proz = sty-proz + s-list.y-proz.
    sty-logis = sty-logis + s-list.y-logis.
    sty-avrgrate = sty-avrgrate + s-list.y-avrgrate. 
    sty-revenue = sty-revenue + s-list.revenue.
    rmrevsubt = rmrevsubt + sty-revenue. /*will*/
END PROCEDURE.

PROCEDURE count-sub2:
    IF sorttype = 0 THEN rmcomp-segm-list.segment = s-list.segment.
    ELSE rmcomp-segm-list.segment = s-list.compname.
    
    ASSIGN                          
        rmcomp-segm-list.room       = STRING(s-list.room, "->>>,>>9")                 
        rmcomp-segm-list.pax        = STRING(s-list.pax, "->>>,>>9")                  
        rmcomp-segm-list.logis      = STRING(s-list.logis, "->>>,>>>,>>>,>>9.99")     
        rmcomp-segm-list.proz       = STRING(s-list.proz, ">>9.99")                   
        rmcomp-segm-list.avrgrate   = STRING(s-list.avrgrate, "->>>,>>>,>>>,>>9.99")  
        rmcomp-segm-list.m-room     = STRING(s-list.m-room, "->>>,>>9")               
        rmcomp-segm-list.m-pax      = STRING(s-list.m-pax, "->>>,>>9")                
        rmcomp-segm-list.m-logis    = STRING(s-list.m-logis, "->>>,>>>,>>>,>>9.99")   
        rmcomp-segm-list.m-proz     = STRING(s-list.m-proz, ">>9.99")                 
        rmcomp-segm-list.m-avrgrate = STRING(s-list.m-avrgrate, "->>>,>>>,>>>,>>9.99")
        rmcomp-segm-list.y-room     = STRING(s-list.y-room, "->>>,>>9")               
        rmcomp-segm-list.y-pax      = STRING(s-list.y-pax, "->>>,>>9")                
        rmcomp-segm-list.y-logis    = STRING(s-list.y-logis, "->>>,>>>,>>>,>>9.99")   
        rmcomp-segm-list.y-proz     = STRING(s-list.y-proz, ">>9.99")                 
        rmcomp-segm-list.y-avrgrate = STRING(s-list.y-avrgrate, "->>>,>>>,>>>,>>9.99")
        rmcomp-segm-list.revenue    = STRING(s-list.revenue, "->>>,>>>,>>>,>>9.99")

        rmcomp-segm-list.rmnite     = STRING(s-list.y-room, "->>>,>>9")            
        rmcomp-segm-list.rmrev      = STRING(s-list.y-logis, "->>>,>>>,>>>,>>9.99")
        rmcomp-segm-list.rmnite1    = STRING(s-list.m-room, "->>>,>>9")            
        rmcomp-segm-list.rmrev1     = STRING(s-list.m-logis, "->>>,>>>,>>>,>>9.99") 
        rmcomp-segm-list.gastnr     = s-list.gastnr
        rmcomp-segm-list.segm-code  = s-list.segm-code
    .
    proz = proz + s-list.proz.
    m-proz = m-proz + s-list.m-proz.
    y-proz = y-proz + s-list.y-proz.
    st-room = st-room + s-list.room.
    st-pax = st-pax  + s-list.pax.
    st-proz = st-proz + s-list.proz.
    st-logis = st-logis + s-list.logis.
    st-avrgrate = st-avrgrate + s-list.avrgrate.
    stm-room = stm-room + s-list.m-room.        
    stm-pax = stm-pax  + s-list.m-pax.
    stm-proz = stm-proz + s-list.m-proz.
    stm-logis = stm-logis + s-list.m-logis.
    stm-avrgrate = stm-avrgrate + s-list.m-avrgrate.
    sty-room = sty-room + s-list.y-room.        
    sty-pax = sty-pax  + s-list.y-pax.
    sty-proz = sty-proz + s-list.y-proz.
    sty-logis = sty-logis + s-list.y-logis.
    sty-avrgrate = sty-avrgrate + s-list.y-avrgrate. 
    sty-revenue = sty-revenue + s-list.revenue.
    rmrevsubt = rmrevsubt + sty-revenue. /*will*/
END PROCEDURE.

PROCEDURE create-sub:
    DEF VAR ind AS INTEGER NO-UNDO.

    CREATE rmcomp-segm-list. 
    rmcomp-segm-list.flag = 1. 
    
    CREATE rmcomp-segm-list. 
    rmcomp-segm-list.flag = 2. 

    st-avrgrate = 0. 
    IF (st-room - stc-room) NE 0 THEN st-avrgrate = st-logis / (st-room - stc-room). 
    stm-avrgrate = 0. 
    IF (stm-room - stmc-room) NE 0 THEN stm-avrgrate = stm-logis / (stm-room - stmc-room). 
    sty-avrgrate = 0. 
    IF (sty-room - styc-room) NE 0 THEN sty-avrgrate = sty-logis / (sty-room - styc-room). 
    
    IF price-decimal = 0 THEN 
    DO:
        ASSIGN
            rmcomp-segm-list.segment    = translateExtended("S u b T o t a l", lvCAREA, "")
            rmcomp-segm-list.room       = STRING(st-room, "->>>,>>9")                      
            rmcomp-segm-list.pax        = STRING(st-pax, "->>>,>>9")                       
            rmcomp-segm-list.logis      = STRING(st-logis, "->>,>>>,>>>,>>>,>>9")          
            rmcomp-segm-list.proz       = STRING(st-proz, ">>9.99")                        
            rmcomp-segm-list.avrgrate   = STRING(st-avrgrate, "->>,>>>,>>>,>>>,>>9")       
            rmcomp-segm-list.m-room     = STRING(stm-room, "->>>,>>9")                     
            rmcomp-segm-list.m-pax      = STRING(stm-pax, "->>>,>>9")                      
            rmcomp-segm-list.m-logis    = STRING(stm-logis, "->>,>>>,>>>,>>>,>>9")         
            rmcomp-segm-list.m-proz     = STRING(stm-proz, ">>9.99")                       
            rmcomp-segm-list.m-avrgrate = STRING(stm-avrgrate, "->>,>>>,>>>,>>>,>>9")      
            rmcomp-segm-list.y-room     = STRING(sty-room, "->>>,>>9")                     
            rmcomp-segm-list.y-pax      = STRING(sty-pax, "->>>,>>9")                      
            rmcomp-segm-list.y-logis    = STRING(sty-logis, "->>,>>>,>>>,>>>,>>9")         
            rmcomp-segm-list.y-proz     = STRING(sty-proz, ">>9.99")                       
            rmcomp-segm-list.y-avrgrate = STRING(sty-avrgrate, "->>,>>>,>>>,>>>,>>9")
            rmcomp-segm-list.revenue    = STRING(sty-revenue, "->>,>>>,>>>,>>>,>>9")
        .
    END.
    ELSE
    DO:
        ASSIGN 
            rmcomp-segm-list.segment    = translateExtended("S u b T o t a l", lvCAREA, "")
            rmcomp-segm-list.room       = STRING(st-room, "->>>,>>9")                      
            rmcomp-segm-list.pax        = STRING(st-pax, "->>>,>>9")                       
            rmcomp-segm-list.logis      = STRING(st-logis, "->>>,>>>,>>>,>>9.99")          
            rmcomp-segm-list.proz       = STRING(st-proz, ">>9.99")                        
            rmcomp-segm-list.avrgrate   = STRING(st-avrgrate, "->>>,>>>,>>>,>>9.99")       
            rmcomp-segm-list.m-room     = STRING(stm-room, "->>>,>>9")                     
            rmcomp-segm-list.m-pax      = STRING(stm-pax, "->>>,>>9")                      
            rmcomp-segm-list.m-logis    = STRING(stm-logis, "->>>,>>>,>>>,>>9.99")         
            rmcomp-segm-list.m-proz     = STRING(stm-proz, ">>9.99")                       
            rmcomp-segm-list.m-avrgrate = STRING(stm-avrgrate, "->>>,>>>,>>>,>>9.99")      
            rmcomp-segm-list.y-room     = STRING(sty-room, "->>>,>>9")                     
            rmcomp-segm-list.y-pax      = STRING(sty-pax, "->>>,>>9")                      
            rmcomp-segm-list.y-logis    = STRING(sty-logis, "->>>,>>>,>>>,>>9.99")         
            rmcomp-segm-list.y-proz     = STRING(sty-proz, ">>9.99")                       
            rmcomp-segm-list.y-avrgrate = STRING(sty-avrgrate, "->>>,>>>,>>>,>>9.99")
            rmcomp-segm-list.revenue    = STRING(sty-revenue, "->>>,>>>,>>>,>>9.99")
        .
    END.    

    CREATE rmcomp-segm-list. 
    RUN init-val.
END PROCEDURE.

PROCEDURE calc-othRev:
DEFINE INPUT PARAMETER datum AS DATE.
DEFINE OUTPUT PARAMETER othRev AS DECIMAL.

DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE max-i       AS INTEGER INITIAL 0.
DEFINE VARIABLE art-list    AS INTEGER EXTENT 200. 
DEFINE VARIABLE serv-vat    AS LOGICAL. 
DEFINE VARIABLE fact        AS DECIMAL. 
DEFINE VARIABLE serv        AS DECIMAL. 
DEFINE VARIABLE vat         AS DECIMAL.


FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
serv-vat = htparam.flogical. 

FOR EACH artikel WHERE artikel.departement = 0
    AND artikel.artart = 0 AND artikel.umsatzart = 1 NO-LOCK 
    BY artikel.artnr:
    max-i = max-i + 1.
    art-list[max-i] = artikel.artnr.
END.
    
    DO i = 1 TO max-i: 
        FIND FIRST artikel WHERE artikel.artnr = art-list[i] 
            AND artikel.departement = 0 NO-LOCK NO-ERROR. 
        IF AVAILABLE artikel THEN 
        DO: 
            serv = 0. 
            vat = 0. 
            FOR EACH umsatz WHERE umsatz.artnr = artikel.artnr 
                AND umsatz.departement = artikel.departement 
                AND umsatz.datum EQ datum NO-LOCK: 
                RUN calc-servvat.p(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service-code, 
                                   artikel.mwst-code, OUTPUT serv, OUTPUT vat).
                
                fact = 1.00 + serv + vat. 
                othRev = othRev + umsatz.betrag / fact.
            END. 
        END.
    END.
END.


PROCEDURE init-val:
    st-room       = 0.
    st-pax        = 0.
    st-proz       = 0.
    st-logis      = 0.
    st-avrgrate   = 0.
    stm-room      = 0.        
    stm-pax       = 0.
    stm-proz      = 0.
    stm-logis     = 0.
    stm-avrgrate  = 0.
    sty-room      = 0.   
    sty-pax       = 0.
    sty-proz      = 0.
    sty-logis     = 0.
    sty-avrgrate  = 0.
    sty-revenue   = 0.
END PROCEDURE.

