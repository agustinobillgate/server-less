DEFINE TEMP-TABLE cl-list
    FIELD hno         AS INTEGER FORMAT ">>>9"                      COLUMN-LABEL "HNo"
    FIELD htlname     AS CHAR    FORMAT "x(24)"                     COLUMN-LABEL "Hotel Name"
    FIELD occ-rm      AS INTEGER FORMAT ">,>>9"                     COLUMN-LABEL "OccRm"
    FIELD occ-rm-c    AS INTEGER FORMAT ">,>>9"                     COLUMN-LABEL "OccRmIncComp"
    FIELD saleable    AS INTEGER FORMAT ">,>>9"                     COLUMN-LABEL "Saleable"                 /*Today*/
    FIELD rmrev       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99 "      COLUMN-LABEL "RmRevenue"
    FIELD avrgrate    AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"       COLUMN-LABEL "Average Rate"  /*geral 290420 bef ->,>>>,>>9.99*/
    FIELD yield       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"       /*geral 290420 bef ->,>>>,>>9.99*/
    FIELD nat-mark    AS DECIMAL FORMAT ">>9.99"
    FIELD mark-share  AS DECIMAL FORMAT ">>9.99"
    FIELD revpar      AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"       COLUMN-LABEL "RevPar"   /*geral 290420 bef ->,>>>,>>9.99*/
    FIELD rgi         AS DECIMAL FORMAT "->>>,>>>,>>9.99"            COLUMN-LABEL "RGI"
    FIELD mpi         AS DECIMAL FORMAT "->>9.99"                    COLUMN-LABEL "MPI"
    FIELD ari         AS DECIMAL FORMAT "->,>>>,>>9.99"              COLUMN-LABEL "ARI"
    FIELD occ-proz    AS DECIMAL FORMAT ">>9.99"                    COLUMN-LABEL "OCC"
    FIELD occ-proz-c  AS DECIMAL FORMAT ">>9.99"                    COLUMN-LABEL "OCCIncComp"
                                                                                                   
    FIELD occ-rm1     AS INTEGER FORMAT ">,>>9"                     COLUMN-LABEL "OccRm"
    FIELD occ-rm-c1   AS INTEGER FORMAT ">,>>9"                     COLUMN-LABEL "OccRmIncComp"
    FIELD saleable1   AS INTEGER FORMAT ">>,>>9"                    COLUMN-LABEL "Saleable"
    FIELD rmrev1      AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"       COLUMN-LABEL "RmRevenue" /*sis 080814 bef --> >>,>>>,>>>,>>9.99*/
    FIELD avrgrate1   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"       COLUMN-LABEL "AvrgRate" /*geral 290420 bef ->>,>>>,>>9.99*/
    FIELD yield1      AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"            /*geral 290420 bef ->>,>>>,>>9.99*/
    FIELD nat-mark1   AS DECIMAL FORMAT ">>9.99"
    FIELD mark-share1 AS DECIMAL FORMAT ">>9.99"                                                    /*MTD this Year*/
    FIELD revpar1     AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"       COLUMN-LABEL "RevPar" /*geral 290420 bef ->>,>>>,>>9.99*/
    FIELD rgi1        AS DECIMAL FORMAT "->>>,>>>,>>9.99"            COLUMN-LABEL "RGI"
    FIELD mpi1        AS DECIMAL FORMAT "->>9.99"                    COLUMN-LABEL "MPI"
    FIELD ari1        AS DECIMAL FORMAT "->,>>>,>>9.99"              COLUMN-LABEL "ARI"
    FIELD occ-proz1   AS DECIMAL FORMAT ">>9.99"                    COLUMN-LABEL "OCC"                 
    FIELD occ-proz-c1 AS DECIMAL FORMAT ">>9.99"                    COLUMN-LABEL "OCCIncComp"        

    FIELD occ-rm2     AS INTEGER FORMAT ">>>,>>9"                   COLUMN-LABEL "OccRm"
    FIELD occ-rm-c2   AS INTEGER FORMAT ">>>,>>9"                   COLUMN-LABEL "OccRmIncComp"
    FIELD saleable2   AS INTEGER FORMAT ">>>,>>9"                   COLUMN-LABEL "Saleable"
    FIELD rmrev2      AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99"     COLUMN-LABEL "RmRevenue"
    FIELD avrgrate2   AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99"     COLUMN-LABEL "AvrgRate"    /*geral 290420 bef ->>>,>>>,>>9.99*/
    FIELD yield2      AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99"           /*geral 290420 bef ->>>,>>>,>>9.99*/
    FIELD nat-mark2   AS DECIMAL FORMAT ">,>>9.99"                                                  /*YTD this Year*/
    FIELD mark-share2 AS DECIMAL FORMAT ">,>>9.99"
    FIELD revpar2     AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99"     COLUMN-LABEL "RevPar"   /*geral 290420 bef ->>>,>>>,>>9.99*/
    FIELD rgi2        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"          COLUMN-LABEL "RGI"
    FIELD mpi2        AS DECIMAL FORMAT "->,>>9.99"                  COLUMN-LABEL "MPI"
    FIELD ari2        AS DECIMAL FORMAT "->>>,>>>,>>9.99"            COLUMN-LABEL "ARI"
    FIELD occ-proz2   AS DECIMAL FORMAT ">,>>9.99"                  COLUMN-LABEL "OCC"
    FIELD occ-proz-c2 AS DECIMAL FORMAT ">,>>9.99"                  COLUMN-LABEL "OCCIncComp"
    
    FIELD occ-rm3     AS INTEGER FORMAT ">>>,>>9"                   COLUMN-LABEL "OccRm"
    FIELD occ-rm-c3   AS INTEGER FORMAT ">>>,>>9"                   COLUMN-LABEL "OccRmIncComp"
    FIELD saleable3   AS INTEGER FORMAT ">>>,>>9"                   COLUMN-LABEL "Saleable"
    FIELD rmrev3      AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99"     COLUMN-LABEL "RmRevenue"
    FIELD avrgrate3   AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99"     COLUMN-LABEL "AvrgRate" /*geral 290420 bef ->>,>>>,>>>,>>9.99*/
    FIELD yield3      AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99"           /*geral 290420 bef ->>>,>>>,>>9.99*/
    FIELD nat-mark3   AS DECIMAL FORMAT ">,>>9.99"                                              /*MTD last year*/
    FIELD mark-share3 AS DECIMAL FORMAT ">,>>9.99"
    FIELD revpar3     AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99"     COLUMN-LABEL "RevPar" /*geral 290420 bef ->>,>>>,>>>,>>9.99*/
    FIELD rgi3        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"          COLUMN-LABEL "RGI"
    FIELD mpi3        AS DECIMAL FORMAT "->,>>9.99"                  COLUMN-LABEL "MPI"
    FIELD ari3        AS DECIMAL FORMAT "->>>,>>>,>>9.99"            COLUMN-LABEL "ARI"
    FIELD occ-proz3   AS DECIMAL FORMAT ">,>>9.99"                  COLUMN-LABEL "OCC"
    FIELD occ-proz-c3 AS DECIMAL FORMAT ">,>>9.99"                  COLUMN-LABEL "OCCIncComp"

    FIELD occ-rm4     AS INTEGER FORMAT ">>>,>>9"                   COLUMN-LABEL "OccRm"
    FIELD occ-rm-c4   AS INTEGER FORMAT ">>>,>>9"                   COLUMN-LABEL "OccRmIncComp"
    FIELD saleable4   AS INTEGER FORMAT ">>>,>>9"                   COLUMN-LABEL "Saleable"
    FIELD rmrev4      AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99"     COLUMN-LABEL "RmRevenue"
    FIELD avrgrate4   AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99"     COLUMN-LABEL "AvrgRate" /*geral 290420 bef ->>>,>>>,>>9.99*/
    FIELD yield4      AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99"           /*geral 290420 bef ->>>,>>>,>>9.99*/
    FIELD nat-mark4   AS DECIMAL FORMAT ">,>>9.99"                                               /*YTD last year*/
    FIELD mark-share4 AS DECIMAL FORMAT ">,>>9.99"
    FIELD revpar4     AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99"     COLUMN-LABEL "RevPar"       /*geral 290420 bef ->>>,>>>,>>9.99*/
    FIELD rgi4        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"          COLUMN-LABEL "RGI"
    FIELD mpi4        AS DECIMAL FORMAT "->,>>9.99"                  COLUMN-LABEL "MPI"
    FIELD ari4        AS DECIMAL FORMAT "->>>,>>>,>>9.99"            COLUMN-LABEL "ARI"
    FIELD occ-proz4   AS DECIMAL FORMAT ">,>>9.99"                  COLUMN-LABEL "OCC"
    FIELD occ-proz-c4 AS DECIMAL FORMAT ">,>>9.99"                  COLUMN-LABEL "OCCIncComp"

    FIELD index-nr    AS INTEGER.

DEFINE INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER to-date        AS DATE.
DEFINE INPUT  PARAMETER show-ytd       AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR cl-list.

DEF VAR tsale          AS INTEGER FORMAT ">,>>9".
DEF VAR tsale1         AS INTEGER FORMAT ">,>>9".
DEF VAR tocc-rm        AS INTEGER FORMAT ">,>>9".
DEF VAR tocc-rm1       AS INTEGER FORMAT ">,>>9".
DEF VAR tocc-rm-c      AS INTEGER FORMAT ">,>>9".
DEF VAR tocc-rm-c1     AS INTEGER FORMAT ">,>>9".
  
/*
DEFINE VARIABLE pvILanguage    AS INTEGER NO-UNDO INIT 1.
DEFINE VARIABLE to-date        AS DATE INIT 06/10/13.
DEFINE VARIABLE show-ytd       AS LOGICAL NO-UNDO INIT YES.
DEFINE VARIABLE tsale          AS INTEGER FORMAT ">,>>9".
DEFINE VARIABLE tsale1         AS INTEGER FORMAT ">,>>9".
DEFINE VARIABLE tocc-rm        AS INTEGER FORMAT ">,>>9".
DEFINE VARIABLE tocc-rm1       AS INTEGER FORMAT ">,>>9".
*/

DEFINE VARIABLE tot-hotel   AS INTEGER.
DEFINE VARIABLE tocc-rm2    AS INTEGER FORMAT ">,>>9".
DEFINE VARIABLE tocc-rm3    AS INTEGER FORMAT ">,>>9".
DEFINE VARIABLE tocc-rm4    AS INTEGER FORMAT ">,>>9".
DEFINE VARIABLE tocc-rm-c2  AS INTEGER FORMAT ">,>>9".
DEFINE VARIABLE tocc-rm-c3  AS INTEGER FORMAT ">,>>9".
DEFINE VARIABLE tocc-rm-c4  AS INTEGER FORMAT ">,>>9".

DEFINE VARIABLE tsale2      AS INTEGER FORMAT ">,>>9".
DEFINE VARIABLE tsale3      AS INTEGER FORMAT ">,>>9".
DEFINE VARIABLE tsale4      AS INTEGER FORMAT ">,>>9".

DEFINE VARIABLE trmrev      AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEFINE VARIABLE trmrev1     AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99".
DEFINE VARIABLE trmrev2     AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99".
DEFINE VARIABLE trmrev3     AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99".
DEFINE VARIABLE trmrev4     AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99".

DEFINE VARIABLE tavr        AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEFINE VARIABLE tavr1       AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEFINE VARIABLE tavr2       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tavr3       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".
DEFINE VARIABLE tavr4       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".

/*DEFINE VARIABLE tocc-proz   AS INTEGER FORMAT ">,>>9".  */
/*DEFINE VARIABLE tocc-proz1  AS INTEGER FORMAT ">,>>9".  */
/*DEFINE VARIABLE tocc-proz2  AS INTEGER FORMAT ">>>,>>9".*/
/*DEFINE VARIABLE tocc-proz3  AS INTEGER FORMAT ">>>,>>9".*/
/*DEFINE VARIABLE tocc-proz4  AS INTEGER FORMAT ">>>,>>9".*/
/*Naufal 140420 - change from int to dec*/
DEFINE VARIABLE tocc-proz   AS DECIMAL FORMAT ">,>>9.99".  
DEFINE VARIABLE tocc-proz1  AS DECIMAL FORMAT ">,>>9.99".  
DEFINE VARIABLE tocc-proz2  AS DECIMAL FORMAT ">>>,>>9.99".
DEFINE VARIABLE tocc-proz3  AS DECIMAL FORMAT ">>>,>>9.99".
DEFINE VARIABLE tocc-proz4  AS DECIMAL FORMAT ">>>,>>9.99".
/*end*/
/*DEFINE VARIABLE tocc-proz-c   AS INTEGER FORMAT ">,>>9".  */
/*DEFINE VARIABLE tocc-proz-c1  AS INTEGER FORMAT ">,>>9".  */
/*DEFINE VARIABLE tocc-proz-c2  AS INTEGER FORMAT ">>>,>>9".*/
/*DEFINE VARIABLE tocc-proz-c3  AS INTEGER FORMAT ">>>,>>9".*/
/*DEFINE VARIABLE tocc-proz-c4  AS INTEGER FORMAT ">>>,>>9".*/

DEFINE VARIABLE tocc-proz-c   AS DECIMAL FORMAT ">,>>9.99".  
DEFINE VARIABLE tocc-proz-c1  AS DECIMAL FORMAT ">,>>9.99".  
DEFINE VARIABLE tocc-proz-c2  AS DECIMAL FORMAT ">>>,>>9.99".
DEFINE VARIABLE tocc-proz-c3  AS DECIMAL FORMAT ">>>,>>9.99".
DEFINE VARIABLE tocc-proz-c4  AS DECIMAL FORMAT ">>>,>>9.99".

DEFINE VARIABLE trevpar     AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".
DEFINE VARIABLE trevpar1    AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".
DEFINE VARIABLE trevpar2    AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99".
DEFINE VARIABLE trevpar3    AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99".
DEFINE VARIABLE trevpar4    AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99".

DEFINE VARIABLE trgi        AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEFINE VARIABLE trgi1       AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEFINE VARIABLE trgi2       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE trgi3       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".
DEFINE VARIABLE trgi4       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".

DEFINE VARIABLE tmpi        AS DECIMAL FORMAT "->>9.99".
DEFINE VARIABLE tmpi1       AS DECIMAL FORMAT "->>9.99".
DEFINE VARIABLE tmpi2       AS DECIMAL FORMAT "->,>>9.99".
DEFINE VARIABLE tmpi3       AS DECIMAL FORMAT "->,>>9.99".
DEFINE VARIABLE tmpi4       AS DECIMAL FORMAT "->,>>9.99".

DEFINE VARIABLE tari        AS DECIMAL FORMAT "->,>>>,>>9.99".
DEFINE VARIABLE tari1       AS DECIMAL FORMAT "->,>>>,>>9.99".
DEFINE VARIABLE tari2       AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEFINE VARIABLE tari3       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tari4       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".

DEFINE VARIABLE from-date   AS DATE LABEL "From Date".
DEFINE VARIABLE last-fdate  AS DATE.
DEFINE VARIABLE last-tdate  AS DATE.
DEFINE BUFFER t-zinrstat FOR zinrstat.


{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "comp-stataccor".

IF show-ytd THEN RUN create-umsatz1.


PROCEDURE get-totalhtl:
    tot-hotel = 0.
    FOR EACH akt-code WHERE akt-code.aktiongrup = 4 NO-LOCK:
        tot-hotel = tot-hotel + 1.

    END.
END.

PROCEDURE create-umsatz1:
   DEF VAR str1 AS CHAR.
   DEF VAR str2 AS CHAR.
   DEF VAR str3 AS CHAR.
   DEF VAR str4 AS CHAR.

   DEF VAR dd AS INTEGER.
   DEF VAR mm AS INTEGER.

   RUN get-totalhtl.

   FOR EACH cl-list:
       DELETE cl-list.
   END.

   ASSIGN
       tocc-rm      = 0
       tocc-rm1     = 0
       tocc-rm2     = 0
       tocc-rm3     = 0
       tocc-rm4     = 0
       tocc-rm-c    = 0
       tocc-rm-c1   = 0
       tocc-rm-c2   = 0
       tocc-rm-c3   = 0
       tocc-rm-c4   = 0
       tsale        = 0
       tsale1       = 0
       tsale2       = 0
       tsale3       = 0
       tsale4       = 0
       trmrev       = 0
       trmrev1      = 0
       trmrev2      = 0
       trmrev3      = 0
       trmrev4      = 0
       tocc-proz    = 0
       tocc-proz1   = 0
       tocc-proz2   = 0
       tocc-proz3   = 0
       tocc-proz4   = 0
       trevpar      = 0
       tocc-proz-c  = 0
       tocc-proz-c1 = 0
       tocc-proz-c2 = 0
       tocc-proz-c3 = 0
       tocc-proz-c4 = 0
       trevpar1     = 0
       trevpar2     = 0
       trevpar3     = 0
       trevpar4     = 0
       trgi         = 0
       trgi1        = 0
       trgi2        = 0
       trgi3        = 0
       trgi4        = 0
       tmpi         = 0
       tmpi1        = 0
       tmpi2        = 0
       tmpi3        = 0
       tmpi4        = 0
       tari         = 0
       tari1        = 0
       tari2        = 0
       tari3        = 0
       tari4        = 0
    .

    from-date = DATE(1,1, YEAR(to-date)).
    last-fdate = DATE(1,1, YEAR(to-date) - 1).
    /*last-tdate = DATE(MONTH(to-date),DAY(to-date), YEAR(to-date) - 1).*/
    dd = DAY(to-date).
    mm = MONTH(to-date).

    /*FDL March 26, 2024 => Ticket 4DD18F*/
    IF dd EQ 29 AND mm EQ 2 THEN
    DO:       
        last-tdate = DATE(MONTH(to-date),28, YEAR(to-date) - 1).
    END.    
    ELSE last-tdate = DATE(MONTH(to-date),DAY(to-date), YEAR(to-date) - 1).

    FOR EACH zinrstat WHERE zinrstat.datum GE from-date AND 
        zinrstat.datum LE to-date AND zinrstat.zinr = "Competitor" NO-LOCK:
        /*FIND FIRST queasy WHERE queasy.KEY = 136 AND queasy.number1 = zinrstat.betriebsnr
            NO-LOCK NO-ERROR.*/
        FIND FIRST akt-code WHERE akt-code.aktiongrup = 4 AND 
            akt-code.aktionscode = zinrstat.betriebsnr NO-LOCK NO-ERROR.

        FIND FIRST cl-list WHERE cl-list.hno = zinrstat.betriebsnr NO-ERROR.
        IF NOT AVAILABLE cl-list THEN
        DO:
            CREATE cl-list.
            ASSIGN
                cl-list.hno  = zinrstat.betriebsnr.
            /*IF AVAILABLE queasy THEN
                cl-list.htlname = queasy.char3.
             */
            IF AVAILABLE akt-code THEN
                cl-list.htlname = akt-code.bezeich.
        END.

        IF zinrstat.datum = to-date THEN    /*Today*/
        DO:
            ASSIGN
                cl-list.occ-rm      = cl-list.occ-rm   + zinrstat.personen
                cl-list.occ-rm-c    = cl-list.occ-rm-c + (zinrstat.personen + INTEGER(zinrstat.argtumsatz))
                cl-list.saleable    = cl-list.saleable + zinrstat.zimmeranz
                cl-list.rmrev       = cl-list.rmrev    + zinrstat.logisumsatz
                .
        END.
        IF MONTH(zinrstat.datum) = MONTH(to-date) AND YEAR(zinrstat.datum) = YEAR(to-date) THEN /*MTD this year*/
        DO:
            ASSIGN
                cl-list.occ-rm1      = cl-list.occ-rm1   + zinrstat.personen
                cl-list.occ-rm-c1    = cl-list.occ-rm-c1 + (zinrstat.personen + INTEGER(zinrstat.argtumsatz))
                cl-list.saleable1    = cl-list.saleable1 + zinrstat.zimmeranz
                cl-list.rmrev1       = cl-list.rmrev1    + zinrstat.logisumsatz
                .

        END.

        IF zinrstat.datum GE from-date AND zinrstat.datum LE to-date THEN DO:    /*YTD this year*/
            ASSIGN
                cl-list.occ-rm2      = cl-list.occ-rm2   + zinrstat.personen
                cl-list.occ-rm-c2    = cl-list.occ-rm-c2 + (zinrstat.personen + INTEGER(zinrstat.argtumsatz))
                cl-list.saleable2    = cl-list.saleable2 + zinrstat.zimmeranz
                cl-list.rmrev2       = cl-list.rmrev2    + zinrstat.logisumsatz
                .

        END.
        
        /*
        IF MONTH(zinrstat.datum) = MONTH(to-date) AND YEAR(zinrstat.datum) = YEAR(to-date) - 1 THEN /*MTD last year*/
        DO:
            ASSIGN
                cl-list.occ-rm3      = cl-list.occ-rm3   + zinrstat.personen
                cl-list.occ-rm-c3    = cl-list.occ-rm-c3 + (zinrstat.personen + INTEGER(zinrstat.argtumsatz))
                cl-list.saleable3    = cl-list.saleable3 + zinrstat.zimmeranz
                cl-list.rmrev3       = cl-list.rmrev3    + zinrstat.logisumsatz
                .

        END.

        IF zinrstat.datum GE last-fdate AND zinrstat.datum LE last-tdate THEN DO:    /*YTD last year*/
            ASSIGN
                cl-list.occ-rm4      = cl-list.occ-rm4   + zinrstat.personen
                cl-list.occ-rm-c4    = cl-list.occ-rm-c4 + (zinrstat.personen + INTEGER(zinrstat.argtumsatz))
                cl-list.saleable4    = cl-list.saleable4 + zinrstat.zimmeranz
                cl-list.rmrev4       = cl-list.rmrev4    + zinrstat.logisumsatz
                .
        END.*/
        
        
        IF cl-list.saleable NE 0 THEN
          ASSIGN
            cl-list.occ-proz        = cl-list.occ-rm / cl-list.saleable * 100
            cl-list.occ-proz-c      = cl-list.occ-rm-c / cl-list.saleable * 100.
        IF cl-list.saleable1 NE 0 THEN
          ASSIGN
            cl-list.occ-proz1        = cl-list.occ-rm1 / cl-list.saleable1 * 100
            cl-list.occ-proz-c1      = cl-list.occ-rm-c1 / cl-list.saleable1 * 100.
        IF cl-list.saleable2 NE 0 THEN
          ASSIGN
            cl-list.occ-proz2        = cl-list.occ-rm2 / cl-list.saleable2 * 100
            cl-list.occ-proz-c2        = cl-list.occ-rm-c2 / cl-list.saleable2 * 100.
        /*IF cl-list.saleable3 NE 0 THEN
          ASSIGN
            cl-list.occ-proz3        = cl-list.occ-rm3 / cl-list.saleable3 * 100
            cl-list.occ-proz-c3      = cl-list.occ-rm-c3 / cl-list.saleable3 * 100.
        IF cl-list.saleable4 NE 0 THEN
          ASSIGN
            cl-list.occ-proz4        = cl-list.occ-rm4 / cl-list.saleable4 * 100
            cl-list.occ-proz-c4      = cl-list.occ-rm-c4 / cl-list.saleable4 * 100.*/

        IF cl-list.occ-rm NE 0 THEN
            cl-list.avrgrate        = cl-list.rmrev / cl-list.occ-rm.
        IF cl-list.occ-rm1 NE 0 THEN
            cl-list.avrgrate1       = cl-list.rmrev1 / cl-list.occ-rm1.
        IF cl-list.occ-rm2 NE 0 THEN
            cl-list.avrgrate2       = cl-list.rmrev2 / cl-list.occ-rm2.
        /*IF cl-list.occ-rm3 NE 0 THEN
            cl-list.avrgrate3       = cl-list.rmrev3 / cl-list.occ-rm3.
        IF cl-list.occ-rm4 NE 0 THEN
            cl-list.avrgrate4       = cl-list.rmrev4 / cl-list.occ-rm4.*/

        IF cl-list.saleable NE 0 THEN
            cl-list.yield           = cl-list.rmrev / cl-list.saleable.
        IF cl-list.saleable1 NE 0 THEN
            cl-list.yield1           = cl-list.rmrev1 / cl-list.saleable1.
        IF cl-list.saleable2 NE 0 THEN
            cl-list.yield2           = cl-list.rmrev2 / cl-list.saleable2.
        /*IF cl-list.saleable3 NE 0 THEN
            cl-list.yield3           = cl-list.rmrev3 / cl-list.saleable3.
        IF cl-list.saleable4 NE 0 THEN
            cl-list.yield4           = cl-list.rmrev4 / cl-list.saleable4.*/
    END.

    /*for mtd last year and ytd last year*/

    FOR EACH t-zinrstat WHERE t-zinrstat.datum GE last-fdate AND 
        t-zinrstat.datum LE last-tdate AND t-zinrstat.zinr = "Competitor" NO-LOCK:

        FIND FIRST akt-code WHERE akt-code.aktiongrup = 4 AND 
            akt-code.aktionscode = t-zinrstat.betriebsnr NO-LOCK NO-ERROR.

        FIND FIRST cl-list WHERE cl-list.hno = t-zinrstat.betriebsnr NO-ERROR.
        IF NOT AVAILABLE cl-list THEN
        DO:
            CREATE cl-list.
            ASSIGN
                cl-list.hno  = t-zinrstat.betriebsnr.
            
            IF AVAILABLE akt-code THEN
                cl-list.htlname = akt-code.bezeich.
        END.

        IF MONTH(t-zinrstat.datum) = MONTH(last-tdate) AND YEAR(t-zinrstat.datum) = YEAR(last-fdate) THEN   /*MTD last year*/
        DO:
            ASSIGN
                cl-list.occ-rm3      = cl-list.occ-rm3   + t-zinrstat.personen
                cl-list.occ-rm-c3    = cl-list.occ-rm-c3 + (t-zinrstat.personen + INTEGER(t-zinrstat.argtumsatz))
                cl-list.saleable3    = cl-list.saleable3 + t-zinrstat.zimmeranz
                cl-list.rmrev3       = cl-list.rmrev3    + t-zinrstat.logisumsatz
                .

        END.

        IF t-zinrstat.datum GE last-fdate AND t-zinrstat.datum LE last-tdate THEN DO:    /*YTD last year*/
            ASSIGN
                cl-list.occ-rm4      = cl-list.occ-rm4   + t-zinrstat.personen
                cl-list.occ-rm-c4    = cl-list.occ-rm-c4 + (t-zinrstat.personen + INTEGER(t-zinrstat.argtumsatz))
                cl-list.saleable4    = cl-list.saleable4 + t-zinrstat.zimmeranz
                cl-list.rmrev4       = cl-list.rmrev4    + t-zinrstat.logisumsatz
                .
        END.
        
        IF cl-list.saleable3 NE 0 THEN
          ASSIGN
            cl-list.occ-proz3        = cl-list.occ-rm3 / cl-list.saleable3 * 100
            cl-list.occ-proz-c3      = cl-list.occ-rm-c3 / cl-list.saleable3 * 100.
        IF cl-list.saleable4 NE 0 THEN
          ASSIGN
            cl-list.occ-proz4        = cl-list.occ-rm4 / cl-list.saleable4 * 100
            cl-list.occ-proz-c4      = cl-list.occ-rm-c4 / cl-list.saleable4 * 100.

        IF cl-list.occ-rm3 NE 0 THEN
            cl-list.avrgrate3       = cl-list.rmrev3 / cl-list.occ-rm3.
        IF cl-list.occ-rm4 NE 0 THEN
            cl-list.avrgrate4       = cl-list.rmrev4 / cl-list.occ-rm4.

        IF cl-list.saleable3 NE 0 THEN
            cl-list.yield3           = cl-list.rmrev3 / cl-list.saleable3.
        IF cl-list.saleable4 NE 0 THEN
            cl-list.yield4           = cl-list.rmrev4 / cl-list.saleable4.
    END.
    /*end*/
    
    FOR EACH cl-list:
        ASSIGN
                tocc-rm     = tocc-rm + cl-list.occ-rm
                tocc-rm1    = tocc-rm1 + cl-list.occ-rm1
                tocc-rm2    = tocc-rm2 + cl-list.occ-rm2
                tocc-rm3    = tocc-rm3 + cl-list.occ-rm3
                tocc-rm4    = tocc-rm4 + cl-list.occ-rm4
                tocc-rm-c   = tocc-rm-c  + cl-list.occ-rm-c
                tocc-rm-c1  = tocc-rm-c1 + cl-list.occ-rm-c1
                tocc-rm-c2  = tocc-rm-c2 + cl-list.occ-rm-c2
                tocc-rm-c3  = tocc-rm-c3 + cl-list.occ-rm-c3
                tocc-rm-c4  = tocc-rm-c4 + cl-list.occ-rm-c4
                tsale       = tsale    + cl-list.saleable
                tsale1      = tsale1   + cl-list.saleable1
                tsale2      = tsale2   + cl-list.saleable2
                tsale3      = tsale3   + cl-list.saleable3
                tsale4      = tsale4   + cl-list.saleable4
                trmrev1     = trmrev1  + cl-list.rmrev1
                trmrev      = trmrev   + cl-list.rmrev
                trmrev2     = trmrev2  + cl-list.rmrev2
                trmrev3     = trmrev3  + cl-list.rmrev3
                trmrev4     = trmrev4  + cl-list.rmrev4.
    END.
        ASSIGN
                tavr        = trmrev / tocc-rm
                tavr1       = trmrev1 / tocc-rm1
                tavr2       = trmrev2 / tocc-rm2
                tavr3       = trmrev3 / tocc-rm3
                tavr4       = trmrev4 / tocc-rm4
                tocc-proz   = (tocc-rm / tsale) * 100
                tocc-proz1  = (tocc-rm1 / tsale1) * 100
                tocc-proz2  = (tocc-rm2 / tsale2) * 100
                tocc-proz3  = (tocc-rm3 / tsale3) * 100
                tocc-proz4  = (tocc-rm4 / tsale4) * 100
                tocc-proz-c   = (tocc-rm-c / tsale) * 100
                tocc-proz-c1  = (tocc-rm-c1 / tsale1) * 100
                tocc-proz-c2  = (tocc-rm-c2 / tsale2) * 100
                tocc-proz-c3  = (tocc-rm-c3 / tsale3) * 100
                tocc-proz-c4  = (tocc-rm-c4 / tsale4) * 100

                trevpar     = trmrev / tsale
                trevpar1    = trmrev1 / tsale1  
                trevpar2    = trmrev2 / tsale2
                trevpar3    = trmrev3 / tsale3  
                trevpar4    = trmrev4 / tsale4
          .
        
        IF tocc-rm = ? THEN tocc-rm = 0.00.
        IF tocc-rm1 = ? THEN tocc-rm1 = 0.00.
        IF tocc-rm2 = ? THEN tocc-rm2 = 0.00.
        IF tocc-rm3 = ? THEN tocc-rm3 = 0.00.
        IF tocc-rm4 = ? THEN tocc-rm4 = 0.00.
        IF tocc-rm-c  = ? THEN tocc-rm-c  = 0.00.
        IF tocc-rm-c1 = ? THEN tocc-rm-c1 = 0.00.
        IF tocc-rm-c2 = ? THEN tocc-rm-c2 = 0.00.
        IF tocc-rm-c3 = ? THEN tocc-rm-c3 = 0.00.
        IF tocc-rm-c4 = ? THEN tocc-rm-c4 = 0.00.
        IF tsale  = ? THEN tsale  = 0.00.
        IF tsale1 = ? THEN tsale1 = 0.00.
        IF tsale2 = ? THEN tsale2 = 0.00.
        IF tsale3 = ? THEN tsale3 = 0.00.
        IF tsale4 = ? THEN tsale4 = 0.00.
        IF trmrev = ? THEN trmrev = 0.00.
        IF trmrev1 = ? THEN trmrev1 = 0.00.
        IF trmrev2 = ? THEN trmrev2 = 0.00.
        IF trmrev3 = ? THEN trmrev3 = 0.00.
        IF trmrev4 = ? THEN trmrev4 = 0.00.

          IF tavr  = ? THEN tavr  = 0.00.
          IF tavr1 = ? THEN tavr1 = 0.00.
          IF tavr2 = ? THEN tavr2 = 0.00.
          IF tavr3 = ? THEN tavr3 = 0.00.
          IF tavr4 = ? THEN tavr4 = 0.00.
          IF tocc-proz = ?  THEN tocc-proz  = 0.00.
          IF tocc-proz1 = ? THEN tocc-proz1 = 0.00.
          IF tocc-proz2 = ? THEN tocc-proz2 = 0.00.
          IF tocc-proz3 = ? THEN tocc-proz3 = 0.00.
          IF tocc-proz4 = ? THEN tocc-proz4 = 0.00.
          IF tocc-proz-c  = ?  THEN tocc-proz-c = 0.00.
          IF tocc-proz-c1 = ? THEN tocc-proz-c1 = 0.00.
          IF tocc-proz-c2 = ? THEN tocc-proz-c2 = 0.00.
          IF tocc-proz-c3 = ? THEN tocc-proz-c3 = 0.00.
          IF tocc-proz-c4 = ? THEN tocc-proz-c4 = 0.00.
          IF trevpar  = ? THEN trevpar  = 0.00.
          IF trevpar1 = ? THEN trevpar1 = 0.00.
          IF trevpar2 = ? THEN trevpar2 = 0.00.
          IF trevpar3 = ? THEN trevpar3 = 0.00.
          IF trevpar4 = ? THEN trevpar4 = 0.00.

    FOR EACH cl-list:
        IF cl-list.saleable NE 0 THEN
            ASSIGN
                cl-list.mpi = cl-list.occ-proz / tocc-proz.
        IF cl-list.saleable NE 0 AND cl-list.rmrev NE 0 THEN
                cl-list.rgi = cl-list.yield / trevpar.
        cl-list.ari = cl-list.avrgrate / tavr.

        IF cl-list.saleable1 NE 0 THEN
            ASSIGN
            cl-list.mpi1 = cl-list.occ-proz1 / tocc-proz1.
        IF cl-list.saleable1 NE 0 AND cl-list.rmrev1 NE 0 THEN
            cl-list.rgi1 = cl-list.yield1 / trevpar1.
        cl-list.ari1 = cl-list.avrgrate1 / tavr1.

        IF cl-list.saleable2 NE 0 THEN
            ASSIGN
            cl-list.mpi2 = cl-list.occ-proz2 / tocc-proz2.
        IF cl-list.saleable2 NE 0 AND cl-list.rmrev2 NE 0 THEN
            cl-list.rgi2 = cl-list.yield2 / trevpar2.
        cl-list.ari2 = cl-list.avrgrate2 / tavr2.

        IF cl-list.saleable3 NE 0 THEN
            ASSIGN
            cl-list.mpi3 =  cl-list.occ-proz3 / tocc-proz3.
        IF cl-list.saleable3 NE 0 AND cl-list.rmrev3 NE 0 THEN
            cl-list.rgi3 = cl-list.yield3 / trevpar3.
        cl-list.ari3 = cl-list.avrgrate3 / tavr3.
        
        IF cl-list.saleable4 NE 0 THEN
            ASSIGN
            cl-list.mpi4 = cl-list.occ-proz4 / tocc-proz4.
        IF cl-list.saleable4 NE 0 AND cl-list.rmrev4 NE 0 THEN
            cl-list.rgi4 = cl-list.yield4 / trevpar4.
        cl-list.ari4 = cl-list.avrgrate4 / tavr4.

        IF cl-list.ari  = ? THEN cl-list.ari  = 0.00.
        IF cl-list.ari1 = ? THEN cl-list.ari1 = 0.00.
        IF cl-list.ari2 = ? THEN cl-list.ari2 = 0.00.
        IF cl-list.ari3 = ? THEN cl-list.ari3 = 0.00.
        IF cl-list.ari4 = ? THEN cl-list.ari4 = 0.00.
         

         ASSIGN
            trgi        = trevpar / trevpar
            trgi1       = trevpar1 / trevpar1
            trgi2       = trevpar2 / trevpar2
            trgi3       = trevpar3 / trevpar3
            trgi4       = trevpar4 / trevpar4
            tmpi        = tocc-proz / tocc-proz
            tmpi1       = tocc-proz1 / tocc-proz1
            tmpi2       = tocc-proz2 / tocc-proz2
            tmpi3       = tocc-proz3 / tocc-proz3
            tmpi4       = tocc-proz4 / tocc-proz4
            tari        = tavr / tavr
            tari1       = tavr1 / tavr1
            tari2        = tavr2 / tavr2
            tari3       = tavr3 / tavr3
            tari4       = tavr4 / tavr4    
        .
         IF trgi  = ? THEN trgi  = 0.00.
         IF trgi1 = ? THEN trgi1 = 0.00.
         IF trgi2 = ? THEN trgi2 = 0.00.
         IF trgi3 = ? THEN trgi3 = 0.00.
         IF trgi4 = ? THEN trgi4 = 0.00.
         IF tmpi  = ? THEN tmpi  = 0.00.
         IF tmpi1 = ? THEN tmpi1 = 0.00.
         IF tmpi2 = ? THEN tmpi2 = 0.00.
         IF tmpi3 = ? THEN tmpi3 = 0.00.
         IF tmpi4 = ? THEN tmpi4 = 0.00.
         IF tari  = ? THEN tari  = 0.00.
         IF tari1 = ? THEN tari1 = 0.00.
         IF tari2 = ? THEN tari2 = 0.00.
         IF tari3 = ? THEN tari3 = 0.00.
         IF tari4 = ? THEN tari4 = 0.00.        
    END.

    CREATE cl-list.
    ASSIGN
        cl-list.htlname     = STRING("T O T A L", "x(24) ")  
        cl-list.saleable    = tsale
        cl-list.occ-rm      = tocc-rm   
        cl-list.occ-rm-c    = tocc-rm-c  
        cl-list.occ-proz    = tocc-proz  
        cl-list.occ-proz-c  = tocc-proz-c
        cl-list.avrgrate    = tavr      
        cl-list.rmrev       = trmrev    
        cl-list.yield       = trevpar   
        cl-list.rgi         = trgi     
        cl-list.mpi         = tmpi      
        cl-list.ari         = tari       
        cl-list.saleable1   = tsale1
        cl-list.occ-rm1     = tocc-rm1
        cl-list.occ-rm-c1   = tocc-rm-c1
        cl-list.occ-proz1   = tocc-proz1
        cl-list.occ-proz-c1 = tocc-proz-c1
        cl-list.avrgrate1   = tavr1
        cl-list.rmrev1      = trmrev1
        cl-list.yield1      = trevpar1
        cl-list.rgi1        = trgi1
        cl-list.mpi1        = tmpi1
        cl-list.ari1        = tari1
        cl-list.saleable2   = tsale2
        cl-list.occ-rm2     = tocc-rm2
        cl-list.occ-rm-c2   = tocc-rm-c2
        cl-list.occ-proz2   = tocc-proz2
        cl-list.occ-proz-c2 = tocc-proz-c2
        cl-list.avrgrate2   = tavr2
        cl-list.rmrev2      = trmrev2
        cl-list.yield2      = trevpar2
        cl-list.rgi2        = trgi2
        cl-list.mpi2        = tmpi2
        cl-list.ari2        = tari2
        cl-list.saleable3   = tsale3
        cl-list.occ-rm3     = tocc-rm3
        cl-list.occ-rm-c3   = tocc-rm-c3
        cl-list.occ-proz3   = tocc-proz3
        cl-list.occ-proz-c3 = tocc-proz-c3
        cl-list.avrgrate3   = tavr3
        cl-list.rmrev3      = trmrev3
        cl-list.yield3      = trevpar3
        cl-list.rgi3        = trgi3
        cl-list.mpi3        = tmpi3
        cl-list.ari3        = tari3
        cl-list.saleable4   = tsale4
        cl-list.occ-rm4     = tocc-rm4
        cl-list.occ-rm-c4   = tocc-rm-c4
        cl-list.occ-proz4   = tocc-proz4
        cl-list.occ-proz-c4 = tocc-proz-c4
        cl-list.avrgrate4   = tavr4
        cl-list.rmrev4      = trmrev4
        cl-list.yield4      = trevpar4
        cl-list.rgi4        = trgi4
        cl-list.mpi4        = tmpi4
        cl-list.ari4        = tari4
        cl-list.index-nr    = 1
        cl-list.hno         = 99999.
END.
