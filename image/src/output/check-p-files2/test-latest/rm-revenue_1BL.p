
DEFINE TEMP-TABLE output-list 
  FIELD rmNo AS CHAR
  FIELD flag AS CHAR 
  FIELD STR AS CHAR. 
 
DEFINE TEMP-TABLE cl-list 
  FIELD flag       AS CHAR 
  FIELD zinr       LIKE zimmer.zinr /*MT 24/07/12 */
  FIELD rmcat      AS CHAR FORMAT "x(6)" 
  FIELD anz        AS INTEGER FORMAT ">>9" 
  FIELD pax        AS INTEGER FORMAT ">>9"
  FIELD net        AS DECIMAL FORMAT "->>>,>>>,>>9.99"
  FIELD proz       AS DECIMAL FORMAT "->>9.99"
  FIELD manz       AS INTEGER FORMAT ">>,>>9" 
  FIELD mpax       AS INTEGER FORMAT ">>,>>9" 
  FIELD mnet       AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0 
  FIELD proz1      AS DECIMAL FORMAT "->>9.99" INITIAL 0 
  FIELD yanz       AS INTEGER FORMAT ">>>,>>9" 
  FIELD ypax       AS INTEGER FORMAT ">>>,>>9" 
  FIELD ynet       AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0 
  FIELD proz2      AS DECIMAL FORMAT "->>9.99" INITIAL 0. 

DEFINE INPUT  PARAMETER m-ftd        AS LOGICAL. 
DEFINE INPUT  PARAMETER m-ytd        AS LOGICAL. 
DEFINE INPUT  PARAMETER f-date       AS DATE.
DEFINE INPUT  PARAMETER t-date       AS DATE.
DEFINE INPUT  PARAMETER to-date      AS DATE.
DEFINE INPUT  PARAMETER rm-no        AS CHAR.
DEFINE INPUT  PARAMETER sorttype     AS INTEGER.
DEFINE INPUT  PARAMETER lod_rev      AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

/**variable**/
DEFINE VARIABLE i                   AS INTEGER. 
DEFINE VARIABLE anz                 AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE manz                AS INTEGER FORMAT ">>,>>9". 
DEFINE VARIABLE yanz                AS INTEGER FORMAT ">>>,>>9". 
DEFINE VARIABLE pax                 AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE mpax                AS INTEGER FORMAT ">>,>>9". 
DEFINE VARIABLE ypax                AS INTEGER FORMAT ">>>,>>9". 
DEFINE VARIABLE mnet                AS DECIMAL FORMAT "->>>,>>>,>>9.99". 
DEFINE VARIABLE ynet                AS DECIMAL FORMAT "->>>,>>>,>>9.99". 
DEFINE VARIABLE net                 AS DECIMAL FORMAT "->>>,>>>,>>9.99". 
DEFINE VARIABLE t-anz               AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE t-manz              AS INTEGER FORMAT ">>,>>9". 
DEFINE VARIABLE t-yanz              AS INTEGER FORMAT ">>>,>>9".
DEFINE VARIABLE t-pax               AS INTEGER FORMAT ">>,>>9". 
DEFINE VARIABLE t-mpax              AS INTEGER FORMAT ">>,>>9". 
DEFINE VARIABLE t-ypax              AS INTEGER FORMAT ">>>,>>9". 
DEFINE VARIABLE t-net               AS DECIMAL FORMAT "->>,>>>,>>9.99". 
DEFINE VARIABLE t-mnet              AS DECIMAL FORMAT "->>>,>>>,>>9.99". 
DEFINE VARIABLE t-ynet              AS DECIMAL FORMAT "->>>,>>>,>>9.99". 
DEFINE VARIABLE from-bez            AS CHAR FORMAT "x(22)". 
DEFINE VARIABLE to-bez              AS CHAR FORMAT "x(22)". 
DEFINE VARIABLE price-decimal       AS INTEGER. 
DEFINE VARIABLE from-date           AS DATE LABEL "F&rom Date". 
/*DEFINE VARIABLE to-date             AS DATE LABEL "To &Date".*/

IF lod_rev = YES THEN RUN create-genstat. 
ELSE RUN create-zinrstat.

PROCEDURE create-zinrstat:
DEFINE VARIABLE mm                  AS INTEGER. 
DEFINE VARIABLE yy                  AS INTEGER. 
DEFINE VARIABLE datum               AS DATE. 
DEF VAR last-zikatnr                AS INTEGER INITIAL 0. 
  anz = 0.
  pax = 0.
  net = 0.
  manz = 0. 
  mpax = 0. 
  mnet = 0. 
  yanz = 0. 
  ypax = 0. 
  ynet = 0. 
 
  t-anz  = 0.
  t-pax  = 0.
  t-manz = 0. 
  t-mpax = 0. 
  t-mnet = 0. 
  t-yanz = 0. 
  t-ypax = 0. 
  t-ynet = 0. 
 
  /*mm = month(to-date). */
  IF m-ftd = YES AND m-ytd = NO THEN 
  DO: 
    from-date = f-date. 
    to-date = t-date. 
    mm = month(to-date). 
    yy = year(to-date). 
  END. 
  ELSE IF m-ftd = NO AND m-ytd = YES THEN
  DO:
    /*to-date = t-date.*/ 
    mm = month(to-date). 
    yy = year(to-date). 
    from-date = DATE(1,1,yy). 
  END. 
  
  FOR EACH output-list: 
    delete output-list. 
  END. 
  FOR EACH cl-list: 
    delete cl-list. 
  END. 


  IF rm-no NE "" THEN 
  DO:
        FIND FIRST zimmer WHERE zimmer.zinr = rm-no NO-LOCK NO-ERROR.
        IF AVAILABLE zimmer THEN
        DO:
            create cl-list. 
            cl-list.zinr = rm-no. 
            cl-list.rmcat = zimmer.kbezeich. 
            DO datum = from-date TO to-date: 
              FIND FIRST zinrstat WHERE zinrstat.zinr = rm-no 
                AND zinrstat.datum = datum AND zinrstat.zimmeranz GT 0
                USE-INDEX zinrdat_ix NO-LOCK NO-ERROR. 
              IF AVAILABLE zinrstat THEN 
              DO: 
                IF datum = to-date THEN
                DO:
                    cl-list.anz = cl-list.anz + zinrstat.zimmeranz.
                    cl-list.net = cl-list.net + zinrstat.argtumsatz. 
                    cl-list.pax = cl-list.pax + zinrstat.person. 
                    anz = anz + zinrstat.zimmeranz. 
                    pax = pax + zinrstat.person. 
                    net = net + zinrstat.argtumsatz. 
                END.
                IF month(zinrstat.datum) = mm AND YEAR(zinrstat.datum) = yy THEN 
                DO: 
                  cl-list.manz = cl-list.manz + zinrstat.zimmeranz. 
                  cl-list.mnet = cl-list.mnet + zinrstat.argtumsatz. 
                  cl-list.mpax = cl-list.mpax + zinrstat.person. 
                  manz = manz + zinrstat.zimmeranz. 
                  mpax = mpax + zinrstat.person. 
                  mnet = mnet + zinrstat.argtumsatz. 
                END. 
                cl-list.yanz = cl-list.yanz + zinrstat.zimmeranz. 
                cl-list.ypax = cl-list.ypax + zinrstat.person. 
                cl-list.ynet = cl-list.ynet + zinrstat.argtumsatz. 
                yanz = yanz + zinrstat.zimmeranz. 
                ypax = ypax + zinrstat.person. 
                ynet = ynet + zinrstat.argtumsatz. 
              END. 
            END. 
        END.
  END.
  ELSE 
  DO: 
      rm-no = "".
      IF sorttype = 1 THEN 
      FOR EACH zimmer /*WHERE zimmer.sleeping = YES*/ NO-LOCK, /* add by damen 13/03/2023 8A7CC6 */
        FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr 
          NO-LOCK BY zimmer.zinr: 
        create cl-list. 
        cl-list.zinr = zimmer.zinr. 
        cl-list.rmcat = zimkateg.kurzbez. 
        DO datum = from-date TO to-date: 
          FIND FIRST zinrstat WHERE zinrstat.zinr = zimmer.zinr 
            AND zinrstat.datum = datum AND zinrstat.zimmeranz GT 0
            USE-INDEX zinrdat_ix NO-LOCK NO-ERROR. 
          IF AVAILABLE zinrstat THEN 
          DO: 
            IF datum = to-date THEN
            DO:
                cl-list.anz = cl-list.anz + zinrstat.zimmeranz.
                cl-list.net = cl-list.net + zinrstat.argtumsatz. 
                cl-list.pax = cl-list.pax + zinrstat.person. 
                anz = anz + zinrstat.zimmeranz. 
                pax = pax + zinrstat.person. 
                net = net + zinrstat.argtumsatz. 
            END.
            IF month(zinrstat.datum) = mm AND YEAR(zinrstat.datum) = yy THEN 
            DO: 
              cl-list.manz = cl-list.manz + zinrstat.zimmeranz. 
              cl-list.mnet = cl-list.mnet + zinrstat.argtumsatz. 
              cl-list.mpax = cl-list.mpax + zinrstat.person. 
              manz = manz + zinrstat.zimmeranz. 
              mpax = mpax + zinrstat.person. 
              mnet = mnet + zinrstat.argtumsatz. 
            END. 
            cl-list.yanz = cl-list.yanz + zinrstat.zimmeranz. 
            cl-list.ypax = cl-list.ypax + zinrstat.person. 
            cl-list.ynet = cl-list.ynet + zinrstat.argtumsatz. 
            yanz = yanz + zinrstat.zimmeranz. 
            ypax = ypax + zinrstat.person. 
            ynet = ynet + zinrstat.argtumsatz. 
          END. 
        END. 
      END. 
      ELSE IF sorttype = 2 THEN 
      FOR EACH zimmer /*WHERE zimmer.sleeping = YES*/ NO-LOCK, /* add by damen 13/03/2023 8A7CC6 */
        FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr 
          NO-LOCK BY zimkateg.zikatnr BY zimmer.zinr: 

        IF last-zikatnr = 0 THEN last-zikatnr = zimmer.zikatnr. 
        IF last-zikatnr NE zimmer.zikatnr THEN 
        DO: 
          CREATE cl-list. 
          ASSIGN 
              cl-list.rmcat = "Total" 
              cl-list.anz  = t-anz
              cl-list.pax  = t-pax
              cl-list.net  = t-net
              cl-list.manz = t-manz 
              cl-list.mnet = t-mnet 
              cl-list.mpax = t-mpax 
              cl-list.yanz = t-yanz 
              cl-list.ypax = t-ypax 
              cl-list.ynet = t-ynet 
              t-anz  = 0
              t-pax  = 0
              t-net  = 0
              t-manz = 0 
          t-mnet = 0 
          t-mpax = 0 
          t-yanz = 0 
          t-ynet = 0 
          t-ypax = 0. 
          last-zikatnr = zimmer.zikatnr. 
        END. 

        CREATE cl-list. 
        cl-list.zinr = zimmer.zinr. 
        cl-list.rmcat = zimkateg.kurzbez. 
        DO datum = from-date TO to-date: 
          FIND FIRST zinrstat WHERE zinrstat.zinr = zimmer.zinr 
            AND zinrstat.datum = datum AND zinrstat.zimmeranz GT 0
            USE-INDEX zinrdat_ix NO-LOCK NO-ERROR. 
          IF AVAILABLE zinrstat THEN 
          DO: 
            IF datum = to-date THEN 
            DO: 
              cl-list.anz = cl-list.anz + zinrstat.zimmeranz. 
              cl-list.net = cl-list.net + zinrstat.argtumsatz. 
              cl-list.pax = cl-list.pax + zinrstat.person. 
              anz = anz + zinrstat.zimmeranz. 
              pax = pax + zinrstat.person. 
              net = net + zinrstat.argtumsatz. 
              t-anz = t-anz + zinrstat.zimmeranz. 
              t-pax = t-pax + zinrstat.person. 
              t-net = t-net + zinrstat.argtumsatz. 
            END. 
            IF month(zinrstat.datum) = mm THEN 
            DO: 
              cl-list.manz = cl-list.manz + zinrstat.zimmeranz. 
              cl-list.mnet = cl-list.mnet + zinrstat.argtumsatz. 
              cl-list.mpax = cl-list.mpax + zinrstat.person. 
              manz = manz + zinrstat.zimmeranz. 
              mpax = mpax + zinrstat.person. 
              mnet = mnet + zinrstat.argtumsatz. 
              t-manz = t-manz + zinrstat.zimmeranz. 
              t-mpax = t-mpax + zinrstat.person. 
              t-mnet = t-mnet + zinrstat.argtumsatz. 
            END. 
            cl-list.yanz = cl-list.yanz + zinrstat.zimmeranz. 
            cl-list.ypax = cl-list.ypax + zinrstat.person. 
            cl-list.ynet = cl-list.ynet + zinrstat.argtumsatz. 
            yanz = yanz + zinrstat.zimmeranz. 
            ypax = ypax + zinrstat.person. 
            ynet = ynet + zinrstat.argtumsatz. 
            t-yanz = t-yanz + zinrstat.zimmeranz. 
            t-ypax = t-ypax + zinrstat.person. 
            t-ynet = t-ynet + zinrstat.argtumsatz. 
          END. 
        END. 
      END. 

      IF sorttype = 2 THEN 
      DO: 
        CREATE cl-list. 
        ASSIGN 
          cl-list.rmcat = "Total" 
          cl-list.anz  = t-anz
          cl-list.pax  = t-pax
          cl-list.net  = t-net
          cl-list.manz = t-manz 
          cl-list.mnet = t-mnet 
          cl-list.mpax = t-mpax 
          cl-list.yanz = t-yanz 
          cl-list.ypax = t-ypax 
          cl-list.ynet = t-ynet. 
        ASSIGN
              t-anz  = 0
              t-pax  = 0
              t-net  = 0
              t-manz = 0 
              t-mnet = 0 
              t-mpax = 0 
              t-yanz = 0 
              t-ynet = 0 
              t-ypax = 0. 
      END. 

  END. 
     
      FOR EACH cl-list: 
        IF net  NE 0 THEN cl-list.proz = cl-list.net / net * 100.
        IF mnet NE 0 THEN cl-list.proz1 = cl-list.mnet / mnet * 100. 
        IF ynet NE 0 THEN cl-list.proz2 = cl-list.ynet / ynet * 100. 
      END. 
     
      create cl-list. 
      cl-list.flag = "*". 
     
      create cl-list. 
      cl-list.zinr = "". 
      cl-list.rmcat = "GTOTAL". 
      cl-list.anz  = anz.
      cl-list.pax  = pax.
      cl-list.net  = net.
      IF net NE 0 THEN cl-list.proz1 = 100.
      cl-list.manz = manz. 
      cl-list.mpax = mpax. 
      cl-list.mnet = mnet. 
      IF mnet NE 0 THEN cl-list.proz1 = 100. 
      cl-list.yanz = yanz. 
      cl-list.ypax = ypax. 
      cl-list.ynet = ynet. 
      IF ynet NE 0 THEN cl-list.proz2 = 100. 
     
      FOR EACH cl-list NO-LOCK: 
        create output-list. 
        output-list.flag = cl-list.flag. 
        output-list.rmNo = cl-list.zinr.
        IF cl-list.flag = "*" THEN 
            output-list.str = FILL("-", 115).
        ELSE 
        DO: 
          IF price-decimal = 0 THEN output-list.str = STRING(cl-list.zinr, "x(6)") 
            + STRING(cl-list.rmcat, "x(6)") 
            + STRING(cl-list.manz, ">>,>>9") 
            + STRING(cl-list.mpax, ">>,>>9") 
            + STRING(cl-list.mnet, "->,>>>,>>>,>>>,>>9") 
            + STRING(cl-list.proz1, "->>9.99") 
            + STRING(cl-list.yanz, ">>>,>>9") 
            + STRING(cl-list.ypax, ">>>,>>9") 
            + STRING(cl-list.ynet, "->,>>>,>>>,>>>,>>9") 
            + STRING(cl-list.proz2, "->>9.99")
            + STRING(cl-list.anz, ">>9")
            + STRING(cl-list.pax, ">>9")
            + STRING(cl-list.net, "->>,>>>,>>>,>>9")
            + STRING(cl-list.proz, "->>9.99"). 
     
          ELSE output-list.str = STRING(cl-list.zinr, "x(6)") 
            + STRING(cl-list.rmcat, "x(6)") 
            + STRING(cl-list.manz, ">>,>>9") 
            + STRING(cl-list.mpax, ">>,>>9") 
            + STRING(cl-list.mnet, "->>,>>>,>>>,>>9.99") 
            + STRING(cl-list.proz1, "->>9.99") 
            + STRING(cl-list.yanz, ">>>,>>9") 
            + STRING(cl-list.ypax, ">>>,>>9") 
            + STRING(cl-list.ynet, "->>,>>>,>>>,>>9.99") 
            + STRING(cl-list.proz2, "->>9.99")
            + STRING(cl-list.anz, ">>9")
            + STRING(cl-list.pax, ">>9")
            + STRING(cl-list.net, "->>>,>>>,>>9.99")
            + STRING(cl-list.proz, "->>9.99"). 
        END. 
  END. 
END.

PROCEDURE create-genstat: 
DEFINE VARIABLE mm AS INTEGER. 
DEFINE VARIABLE yy AS INTEGER. 
DEFINE VARIABLE datum AS DATE. 
DEF VAR last-zikatnr AS INTEGER INITIAL 0. 

  anz = 0.
  pax = 0.
  net = 0.
  manz = 0. 
  mpax = 0. 
  mnet = 0. 
  yanz = 0. 
  ypax = 0. 
  ynet = 0. 
 
  t-anz  = 0.
  t-pax  = 0.
  t-manz = 0. 
  t-mpax = 0. 
  t-mnet = 0. 
  t-yanz = 0. 
  t-ypax = 0. 
  t-ynet = 0. 
 
  /*mm = month(to-date). */
  IF m-ftd = YES THEN 
  DO: 
    from-date = f-date. 
    to-date = t-date. 
    mm = month(to-date). 
    yy = year(to-date). 
  END. 
  ELSE 
  DO: 
    /*to-date = t-date.*/
    mm = month(to-date). 
    yy = year(to-date). 
    from-date = DATE(1,1,yy). 
  END. 
 
  FOR EACH output-list: 
    delete output-list. 
  END. 
  FOR EACH cl-list: 
    delete cl-list. 
  END. 

  IF rm-no NE "" THEN 
  DO:
        FIND FIRST zimmer WHERE zimmer.zinr = rm-no NO-LOCK NO-ERROR.
        IF AVAILABLE zimmer THEN
        DO:
            create cl-list. 
            cl-list.zinr = rm-no. 
            cl-list.rmcat = zimmer.kbezeich. 
            DO datum = from-date TO to-date: 
              FOR EACH genstat WHERE genstat.zinr = rm-no 
                AND genstat.datum = datum 
                AND (genstat.resstatus = 6 OR genstat.resstatus = 8)
                /*AND genstat.logis NE 0*/ NO-LOCK : /*FT add for each genstat,resstatus = 6 & logis ne 0*/
                IF datum = to-date THEN
                DO:
                    cl-list.anz = cl-list.anz + 1.
                    cl-list.net = cl-list.net + genstat.logis.
                    cl-list.pax = cl-list.pax + genstat.erwachs + genstat.gratis +
                                  genstat.kind1 + genstat.kind2 + genstat.kind3. 
                    anz = anz + 1. 
                    pax = pax + genstat.erwachs + genstat.gratis +
                          genstat.kind1 + genstat.kind2 + genstat.kind3. 
                    net = net + genstat.logis. 
                END.
                IF month(genstat.datum) = mm AND YEAR(genstat.datum) = yy THEN 
                DO: 
                  cl-list.manz = cl-list.manz + 1. 
                  cl-list.mnet = cl-list.mnet + genstat.logis.
                  cl-list.mpax = cl-list.mpax + genstat.erwachs + genstat.gratis 
                                 + genstat.kind1 + genstat.kind2 + genstat.kind3. 
                  manz = manz + 1. 
                  mpax = mpax + genstat.erwachs + genstat.gratis 
                         + genstat.kind1 + genstat.kind2 + genstat.kind3. 
                  mnet = mnet + genstat.logis.
                END. 
                cl-list.yanz = cl-list.yanz + 1. 
                cl-list.ypax = cl-list.ypax + genstat.erwachs + genstat.gratis 
                               + genstat.kind1 + genstat.kind2 + genstat.kind3. 
                cl-list.ynet = cl-list.ynet + genstat.logis.
                yanz = yanz + 1.
                ypax = ypax + genstat.erwachs + genstat.gratis
                       + genstat.kind1 + genstat.kind2 + genstat.kind3. 
                ynet = ynet + genstat.logis. 
              END.
            END. 
        END.
  END.
  ELSE 
  DO: 
      rm-no = "".
      IF sorttype = 1 THEN 
      FOR EACH zimmer /*WHERE zimmer.sleeping = YES*/ NO-LOCK, /* add by damen 13/03/2023 8A7CC6 */
        FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr 
          NO-LOCK BY zimmer.zinr: 
        create cl-list. 
        cl-list.zinr = zimmer.zinr. 
        cl-list.rmcat = zimkateg.kurzbez. 
        DO datum = from-date TO to-date: 
          FOR EACH genstat WHERE genstat.zinr = zimmer.zinr 
            AND genstat.datum = datum
            AND (genstat.resstatus = 6 OR genstat.resstatus = 8)
            /*AND genstat.logis NE 0*/ NO-LOCK: /*FT 2,add resstatus = 6 & logis ne 0*/
            IF datum = to-date THEN
            DO:
              ASSIGN
                cl-list.anz = cl-list.anz + 1
                cl-list.net = cl-list.net + genstat.logis
                cl-list.pax = cl-list.pax + genstat.erwachs + genstat.gratis 
                              + genstat.kind1 + genstat.kind2 + genstat.kind3
                anz = anz + 1
                pax = pax + genstat.erwachs + genstat.gratis 
                      + genstat.kind1 + genstat.kind2 + genstat.kind3
                net = net + genstat.logis. 
            END.
            IF month(genstat.datum) = mm AND YEAR(genstat.datum) = yy THEN 
            DO: 
              ASSIGN
                cl-list.manz = cl-list.manz + 1
                cl-list.mnet = cl-list.mnet + genstat.logis
                cl-list.mpax = cl-list.mpax + genstat.erwachs + genstat.gratis 
                               + genstat.kind1 + genstat.kind2 + genstat.kind3
                manz = manz + 1
                mpax = mpax + genstat.erwachs + genstat.gratis 
                       + genstat.kind1 + genstat.kind2 + genstat.kind3
                mnet = mnet + genstat.logis. 
            END. 
            ASSIGN
              cl-list.yanz = cl-list.yanz + 1
              cl-list.ypax = cl-list.ypax + genstat.erwachs + genstat.gratis
                             + genstat.kind1 + genstat.kind2 + genstat.kind3 
              cl-list.ynet = cl-list.ynet + genstat.logis
              yanz = yanz + 1
              ypax = ypax + genstat.erwachs + genstat.gratis 
                     + genstat.kind1 + genstat.kind2 + genstat.kind3
              ynet = ynet + genstat.logis. 
          END. 
        END. 
      END. 
      ELSE IF sorttype = 2 THEN 
      FOR EACH zimmer /*WHERE zimmer.sleeping = YES*/ NO-LOCK, /* add by damen 13/03/2023 8A7CC6 */
        FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr 
          NO-LOCK BY zimkateg.zikatnr BY zimmer.zinr: 

        IF last-zikatnr = 0 THEN last-zikatnr = zimmer.zikatnr. 
        IF last-zikatnr NE zimmer.zikatnr THEN 
        DO: 
          CREATE cl-list. 
          ASSIGN 
              cl-list.rmcat = "Total" 
              cl-list.anz  = t-anz
              cl-list.pax  = t-pax
              cl-list.net  = t-net
              cl-list.manz = t-manz 
              cl-list.mnet = t-mnet 
              cl-list.mpax = t-mpax 
              cl-list.yanz = t-yanz 
              cl-list.ypax = t-ypax 
              cl-list.ynet = t-ynet 
              t-anz  = 0
              t-pax  = 0
              t-net  = 0
              t-manz = 0 
              t-mnet = 0 
              t-mpax = 0 
              t-yanz = 0 
              t-ynet = 0 
              t-ypax = 0. 
              last-zikatnr = zimmer.zikatnr. 
        END. 
 
        CREATE cl-list. 
        cl-list.zinr = zimmer.zinr. 
        cl-list.rmcat = zimkateg.kurzbez. 
        DO datum = from-date TO to-date: 
          FOR EACH genstat WHERE genstat.zinr = zimmer.zinr 
            AND genstat.datum = datum
            AND (genstat.resstatus = 6 OR genstat.resstatus = 8)
            /*AND genstat.logis NE 0*/ NO-LOCK : /*FT add for each genstat, resstatus = 6 & logis ne 0*/
            IF datum = to-date THEN 
            DO:
              ASSIGN
                cl-list.anz = cl-list.anz + 1
                cl-list.net = cl-list.net + genstat.logis
                cl-list.pax = cl-list.pax + genstat.erwachs + genstat.gratis 
                              + genstat.kind1 + genstat.kind2 + genstat.kind3
                anz = anz + 1
                pax = pax + genstat.erwachs + genstat.gratis
                      + genstat.kind1 + genstat.kind2 + genstat.kind3
                net = net + genstat.logis
                t-anz = t-anz + 1
                t-pax = t-pax + genstat.erwachs + genstat.gratis
                        + genstat.kind1 + genstat.kind2 + genstat.kind3
                t-net = t-net + genstat.logis. 
            END. 
            IF month(genstat.datum) = mm THEN 
            DO: 
              ASSIGN
                cl-list.manz = cl-list.manz + 1 
                cl-list.mnet = cl-list.mnet + genstat.logis
                cl-list.mpax = cl-list.mpax + genstat.erwachs + genstat.gratis 
                               + genstat.kind1 + genstat.kind2 + genstat.kind3
                manz = manz + 1
                mpax = mpax + genstat.erwachs + genstat.gratis 
                       + genstat.kind1 + genstat.kind2 + genstat.kind3
                mnet = mnet + genstat.logis
                t-manz = t-manz + 1
                t-mpax = t-mpax + genstat.erwachs + genstat.gratis 
                         + genstat.kind1 + genstat.kind2 + genstat.kind3
                t-mnet = t-mnet + genstat.logis.
            END. 
            ASSIGN
              cl-list.yanz = cl-list.yanz + 1 
              cl-list.ypax = cl-list.ypax + genstat.erwachs + genstat.gratis 
                             + genstat.kind1 + genstat.kind2 + genstat.kind3
              cl-list.ynet = cl-list.ynet + genstat.logis
              yanz = yanz + 1
              ypax = ypax + genstat.erwachs + genstat.gratis 
                     + genstat.kind1 + genstat.kind2 + genstat.kind3
              ynet = ynet + genstat.logis
              t-yanz = t-yanz + 1
              t-ypax = t-ypax + genstat.erwachs + genstat.gratis 
                       + genstat.kind1 + genstat.kind2 + genstat.kind3
              t-ynet = t-ynet + genstat.logis. 
          END. 
        END. 
      END. 

      IF sorttype = 2 THEN 
      DO: 
        CREATE cl-list. 
        ASSIGN 
          cl-list.rmcat = "Total" 
          cl-list.anz  = t-anz
          cl-list.pax  = t-pax
          cl-list.net  = t-net
          cl-list.manz = t-manz 
          cl-list.mnet = t-mnet 
          cl-list.mpax = t-mpax 
          cl-list.yanz = t-yanz 
          cl-list.ypax = t-ypax 
          cl-list.ynet = t-ynet. 
        ASSIGN
              t-anz  = 0
              t-pax  = 0
              t-net  = 0
              t-manz = 0 
              t-mnet = 0 
              t-mpax = 0 
              t-yanz = 0 
              t-ynet = 0 
              t-ypax = 0. 
      END. 

  END. 
     
      FOR EACH cl-list: 
        IF net  NE 0 THEN cl-list.proz = cl-list.net / net * 100.
        IF mnet NE 0 THEN cl-list.proz1 = cl-list.mnet / mnet * 100. 
        IF ynet NE 0 THEN cl-list.proz2 = cl-list.ynet / ynet * 100. 
      END. 
     
      create cl-list. 
      cl-list.flag = "*". 
     
      create cl-list. 
      cl-list.zinr = "". 
      cl-list.rmcat = "GTOTAL". 
      cl-list.anz  = anz.
      cl-list.pax  = pax.
      cl-list.net  = net.
      IF net NE 0 THEN cl-list.proz1 = 100.
      cl-list.manz = manz. 
      cl-list.mpax = mpax. 
      cl-list.mnet = mnet. 
      IF mnet NE 0 THEN cl-list.proz1 = 100. 
      cl-list.yanz = yanz. 
      cl-list.ypax = ypax. 
      cl-list.ynet = ynet. 
      IF ynet NE 0 THEN cl-list.proz2 = 100. 
     
      FOR EACH cl-list NO-LOCK: 
        create output-list. 
        output-list.flag = cl-list.flag. 
        output-list.rmNo = cl-list.zinr.
        IF cl-list.flag = "*" THEN 
            output-list.str = FILL("-", 115).
        ELSE 
        DO: 
          IF price-decimal = 0 THEN output-list.str = STRING(cl-list.zinr, "x(6)") 
            + STRING(cl-list.rmcat, "x(6)") 
            + STRING(cl-list.manz, ">>,>>9") 
            + STRING(cl-list.mpax, ">>,>>9") 
            + STRING(cl-list.mnet, "->,>>>,>>>,>>>,>>9") 
            + STRING(cl-list.proz1, "->>9.99") 
            + STRING(cl-list.yanz, ">>>,>>9") 
            + STRING(cl-list.ypax, ">>>,>>9") 
            + STRING(cl-list.ynet, "->,>>>,>>>,>>>,>>9") 
            + STRING(cl-list.proz2, "->>9.99")
            + STRING(cl-list.anz, ">>9")
            + STRING(cl-list.pax, ">>9")
            + STRING(cl-list.net, "->>,>>>,>>>,>>9")
            + STRING(cl-list.proz, "->>9.99"). 
     
          ELSE output-list.str = STRING(cl-list.zinr, "x(6)") 
            + STRING(cl-list.rmcat, "x(6)") 
            + STRING(cl-list.manz, ">>,>>9") 
            + STRING(cl-list.mpax, ">>,>>9") 
            + STRING(cl-list.mnet, "->>,>>>,>>>,>>9.99") 
            + STRING(cl-list.proz1, "->>9.99") 
            + STRING(cl-list.yanz, ">>>,>>9") 
            + STRING(cl-list.ypax, ">>>,>>9") 
            + STRING(cl-list.ynet, "->>,>>>,>>>,>>9.99") 
            + STRING(cl-list.proz2, "->>9.99")
            + STRING(cl-list.anz, ">>9")
            + STRING(cl-list.pax, ">>9")
            + STRING(cl-list.net, "->>>,>>>,>>9.99")
            + STRING(cl-list.proz, "->>9.99"). 
        END. 
  END. 

END.
