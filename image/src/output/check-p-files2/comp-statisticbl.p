DEFINE TEMP-TABLE cl-list
    FIELD hno           AS INTEGER  FORMAT ">>>9"                   COLUMN-LABEL "HNo"
    FIELD htlname       AS CHAR     FORMAT "x(24)"                  COLUMN-LABEL "Hotel Name"
    FIELD occ-rm        AS DECIMAL  FORMAT ">>>,>>9.99"             COLUMN-LABEL "OccRm"
    FIELD saleable      AS DECIMAL  FORMAT ">,>>9.99"               COLUMN-LABEL "Saleable"
    FIELD rmrev         AS DECIMAL  FORMAT "->>,>>>,>>>,>>9.99"     COLUMN-LABEL "RmRevenue"   /*FT*/
    FIELD avrgrate      AS DECIMAL  FORMAT "->>,>>>,>>>,>>9.99"     COLUMN-LABEL "Average Rate" /*->,>>>,>>9.99*/
    FIELD yield         AS DECIMAL  FORMAT "->>,>>>,>>>,>>9.99"          /*->,>>>,>>9.99*/
    FIELD nat-mark      AS DECIMAL  FORMAT ">>9.99"
    FIELD mark-share    AS DECIMAL  FORMAT ">>9.99"
    FIELD occ-rm1       AS DECIMAL  FORMAT ">>>,>>9.99"             COLUMN-LABEL "OccRm"
    FIELD saleable1     AS DECIMAL  FORMAT ">>,>>9.99"              COLUMN-LABEL "Saleable"
    FIELD rmrev1        AS DECIMAL  FORMAT "->>,>>>,>>>,>>9.99"     COLUMN-LABEL "RmRevenue"
    FIELD avrgrate1     AS DECIMAL  FORMAT "->>,>>>,>>>,>>9.99"     COLUMN-LABEL "AvrgRate"    /*->,>>>,>>9.99*/
    FIELD yield1        AS DECIMAL  FORMAT "->>,>>>,>>>,>>9.99"        /*->,>>>,>>9.99*/
    FIELD nat-mark1     AS DECIMAL  FORMAT ">>9.99"
    FIELD mark-share1   AS DECIMAL  FORMAT ">>9.99"
    FIELD occ-rm2       AS DECIMAL  FORMAT ">>>,>>9.99"             COLUMN-LABEL "OccRm"
    FIELD saleable2     AS DECIMAL  FORMAT ">,>>>,>>9.99"           COLUMN-LABEL "Saleable"
    FIELD rmrev2        AS DECIMAL  FORMAT "->>>,>>>,>>>,>>9.99"    COLUMN-LABEL "RmRevenue"
    FIELD avrgrate2     AS DECIMAL  FORMAT "->>>,>>>,>>>,>>9.99"    COLUMN-LABEL "AvrgRate"     /*->,>>>,>>9.99*/
    FIELD yield2        AS DECIMAL  FORMAT "->>>,>>>,>>>,>>9.99"         /*->,>>>,>>9.99*/
    FIELD nat-mark2     AS DECIMAL  FORMAT ">>9.99"
    FIELD mark-share2   AS DECIMAL  FORMAT ">>9.99"
    FIELD hotel1        AS DECIMAL  FORMAT ">>,>>9.99" /*">>,>>9.99"*/
    FIELD hotel2        AS DECIMAL  FORMAT ">>,>>9.99"
    FIELD hotel3        AS DECIMAL  FORMAT ">>,>>9.99"
/*gerald EB2449*/
    FIELD occ-proz      AS DECIMAL  FORMAT ">>9.99"
    FIELD occ-proz1     AS DECIMAL  FORMAT ">>9.99"
    FIELD occ-proz2     AS DECIMAL  FORMAT ">>9.99".

DEFINE TEMP-TABLE output-list
    FIELD hno           AS INTEGER
    FIELD htlname       AS CHAR     FORMAT "x(50)" COLUMN-LABEL "Hotel Name"    /*wen 24*/
    FIELD occ-rm        AS CHAR     FORMAT "x(7)"  COLUMN-LABEL " OccRm"
    FIELD saleable      AS CHAR     FORMAT "x(5)"  COLUMN-LABEL "SleRm"
    FIELD rmrev         AS CHAR     FORMAT "x(17)" COLUMN-LABEL "     Room Revenue"
    FIELD avrgrate      AS CHAR     FORMAT "x(17)" COLUMN-LABEL "Average Rate"
    FIELD nat-mark      AS CHAR     FORMAT "x(6)"  COLUMN-LABEL "NatMkt"
    FIELD mark-share    AS CHAR     FORMAT "x(6)"  COLUMN-LABEL "Share"
    FIELD yield         AS CHAR     FORMAT "x(17)" COLUMN-LABEL "       Yield"
    FIELD occ-rm1       AS CHAR     FORMAT "x(7)"  COLUMN-LABEL " OccRm"
    FIELD saleable1     AS CHAR     FORMAT "x(6)"  COLUMN-LABEL "  MTD"
    FIELD rmrev1        AS CHAR     FORMAT "x(17)" COLUMN-LABEL " MTD Room Revenue"
    FIELD avrgrate1     AS CHAR     FORMAT "x(17)" COLUMN-LABEL "MTD AvrgRate"
    FIELD nat-mark1     AS CHAR     FORMAT "x(6)"  COLUMN-LABEL "NatMkt"
    FIELD mark-share1   AS CHAR     FORMAT "x(6)"  COLUMN-LABEL "MShare"
    FIELD yield1        AS CHAR     FORMAT "x(17)" COLUMN-LABEL "   MTD Yield"
    FIELD occ-rm2       AS CHAR     FORMAT "x(7)"  COLUMN-LABEL " OccRm"
    FIELD saleable2     AS CHAR     FORMAT "x(9)"  COLUMN-LABEL "      YTD"
    FIELD rmrev2        AS CHAR     FORMAT "x(18)" COLUMN-LABEL "  YTD Room Revenue"
    FIELD avrgrate2     AS CHAR     FORMAT "x(17)" COLUMN-LABEL "YTD AvrgRate"
    FIELD nat-mark2     AS CHAR     FORMAT "x(6)"  COLUMN-LABEL "NatMkt"
    FIELD mark-share2   AS CHAR     FORMAT "x(6)"  COLUMN-LABEL "MShare"
    FIELD yield2        AS CHAR     FORMAT "x(17)" COLUMN-LABEL "   YTD Yield"
    FIELD hotel1        AS CHARACTER FORMAT "x(10)"
    FIELD hotel2        AS CHARACTER FORMAT "x(10)"
    FIELD hotel3        AS CHARACTER FORMAT "x(10)"
/*gerald EB2449*/   
    FIELD occ-proz      AS CHARACTER FORMAT "x(6)"  COLUMN-LABEL " % OCC"
    FIELD occ-proz1     AS CHARACTER FORMAT "x(6)"  COLUMN-LABEL " % OCC"  
    FIELD occ-proz2     AS CHARACTER FORMAT "x(6)"  COLUMN-LABEL " % OCC".

/*DEFINE VARIABLE tocc-rm AS INTEGER FORMAT  ">>>,>>9".
DEFINE VARIABLE tocc-rm1 AS INTEGER FORMAT ">>>,>>9".
DEFINE VARIABLE tocc-rm2 AS INTEGER FORMAT ">>>,>>9".*/

DEFINE VARIABLE tocc-rm  AS DECIMAL FORMAT ">>>,>>9".
DEFINE VARIABLE tocc-rm1 AS DECIMAL FORMAT ">>>,>>9".
DEFINE VARIABLE tocc-rm2 AS DECIMAL FORMAT ">>>,>>9".

/*DEFINE VARIABLE tsale AS INTEGER FORMAT ">,>>9".
DEFINE VARIABLE tsale1 AS INTEGER FORMAT ">,>>9".
DEFINE VARIABLE tsale2 AS INTEGER FORMAT ">,>>>,>>9".*/

DEFINE VARIABLE tsale  AS DECIMAL FORMAT ">>,>>9.99".
DEFINE VARIABLE tsale1 AS DECIMAL FORMAT ">>,>>9.99".
DEFINE VARIABLE tsale2 AS DECIMAL FORMAT ">>,>>9.99".

DEFINE VARIABLE tocc-proz  AS DECIMAL FORMAT ">>9.99".
DEFINE VARIABLE tocc-proz1 AS DECIMAL FORMAT ">>9.99".
DEFINE VARIABLE tocc-proz2 AS DECIMAL FORMAT ">>9.99".

DEFINE VARIABLE hotel1 AS DECIMAL FORMAT ">>>,>>9.99" /*">>,>>9.99"*/  /*">>>,>>9"*/.
DEFINE VARIABLE hotel2 AS DECIMAL FORMAT ">>>,>>9.99".
DEFINE VARIABLE hotel3 AS DECIMAL FORMAT ">>>,>>9.99".

DEFINE VARIABLE hotela AS DECIMAL FORMAT ">>>,>>9.99".
DEFINE VARIABLE hotelb AS DECIMAL FORMAT ">>>,>>9.99".
DEFINE VARIABLE hotelc AS DECIMAL FORMAT ">>>,>>9.99".


DEFINE INPUT PARAMETER  pvILanguage        AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER  from-date          AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER  to-date            AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER  all-occ            AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER  check-ftd          AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

/*
DEFINE VARIABLE trmrev AS INTEGER FORMAT ">>>,>>>,>>9.99".
DEFINE VARIABLE trmrev1 AS INTEGER FORMAT ">>,>>>,>>>,>>9.99".
DEFINE VARIABLE trmrev2 AS INTEGER FORMAT ">>,>>>,>>>,>>9.99".

-rs 16 februari 2010  menyebabkan muncul alert too long for integer. 
*/
DEFINE VARIABLE trmrev  AS decimal FORMAT ">>,>>>,>>>,>>9.99".
DEFINE VARIABLE trmrev1 AS decimal FORMAT ">>,>>>,>>>,>>9.99".
DEFINE VARIABLE trmrev2 AS decimal FORMAT ">>>,>>>,>>>,>>9.99".

DEFINE VARIABLE f-date          AS DATE    NO-UNDO.
DEFINE VARIABLE t-date          AS DATE    NO-UNDO.

{ supertransbl.i }
DEFINE VARIABLE lvCAREA AS CHAR INITIAL "comp-statistic". 
/*******************************MAIN LOGIC**********************************/
IF NOT check-ftd THEN
DO:
    from-date = DATE(1,1, YEAR(to-date)).
    RUN to-date.
END.
ELSE
DO:
    /*f-date    = from-date.*/
    /* change by damen 21/03/23 33DB34  from-date = DATE(1,1, YEAR(to-date)). */
    f-date  = DATE(1,1, YEAR(to-date)).
    t-date  = to-date.
    RUN to-date2.
END.

/******************************* PROCEDURE *********************************/
PROCEDURE to-date:
    FOR EACH cl-list:
        DELETE cl-list.
    END.
    FOR EACH output-list:
        DELETE output-list.
    END.
    ASSIGN
        tocc-rm    = 0
        tocc-rm1   = 0
        tocc-rm2   = 0
        tsale      = 0
        tsale1     = 0
        tsale2     = 0
        trmrev     = 0
        trmrev1    = 0
        trmrev2    = 0
        tocc-proz  = 0
        tocc-proz1 = 0
        tocc-proz2 = 0.

    /*from-date = DATE(1,1, YEAR(to-date)).*/
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
    
        IF zinrstat.datum = to-date THEN
        DO:
            ASSIGN
                cl-list.occ-rm      = cl-list.occ-rm + zinrstat.personen
                cl-list.saleable    = cl-list.saleable + zinrstat.zimmeranz
                cl-list.rmrev       = cl-list.rmrev + zinrstat.logisumsatz
                cl-list.hotel1      = (cl-list.occ-rm / cl-list.saleable) * 100. /*wen*/

            IF all-occ THEN /*M 010612 -> add option include compliment */
                    cl-list.occ-rm = cl-list.occ-rm + INT(zinrstat.argtumsatz).

            IF cl-list.saleable NE 0 THEN
                cl-list.occ-proz = cl-list.occ-rm / cl-list.saleable * 100.
        END.
        
        IF MONTH(zinrstat.datum) = MONTH(to-date) AND YEAR(zinrstat.datum) = YEAR(to-date) THEN
        DO:
            ASSIGN
                cl-list.occ-rm1      = cl-list.occ-rm1 + zinrstat.personen
                cl-list.saleable1    = cl-list.saleable1 + zinrstat.zimmeranz
                cl-list.rmrev1       = cl-list.rmrev1 + zinrstat.logisumsatz
                cl-list.hotel2       = (cl-list.occ-rm1 / cl-list.saleable1) * 100 . /*wen*/.
                   
            IF all-occ THEN /*M 010612 -> add option include compliment */
                    cl-list.occ-rm1 = cl-list.occ-rm1 + INT(zinrstat.argtumsatz).

            IF cl-list.saleable1 NE 0 THEN
                cl-list.occ-proz1 = cl-list.occ-rm1 / cl-list.saleable1 * 100.
        END.
        ASSIGN
            cl-list.occ-rm2      = cl-list.occ-rm2      + zinrstat.personen
            cl-list.saleable2    = cl-list.saleable2    + zinrstat.zimmeranz
            cl-list.rmrev2       = cl-list.rmrev2       + zinrstat.logisumsatz.
            cl-list.hotel3       = (cl-list.occ-rm2 / cl-list.saleable2) * 100. /*wen*/
        IF all-occ THEN /*M 010612 -> add option include compliment */
                cl-list.occ-rm2 = cl-list.occ-rm2 + INT(zinrstat.argtumsatz).

        IF cl-list.saleable2 NE 0 THEN
                cl-list.occ-proz2 = cl-list.occ-rm2 / cl-list.saleable2 * 100.
    
        /*
        ASSIGN
            tocc-rm                 = tocc-rm + cl-list.occ-rm
            tocc-rm1                = tocc-rm1 + cl-list.occ-rm1
            tocc-rm2                = tocc-rm2 + cl-list.occ-rm2
            tsale                   = tsale    + cl-list.saleable
            tsale1                  = tsale1   + cl-list.saleable1
            tsale2                  = tsale2   + cl-list.saleable2
            trmrev1                 = trmrev1  + cl-list.rmrev1
            trmrev2                 = trmrev2  + cl-list.rmrev2
            trmrev                  = trmrev  + cl-list.rmrev.
            
        -rs 16 februari 2010  menyebabkan salah perhitungan di baris total.
        */   
    END.
    
    /* change by damen 30/03/23 0972D8 */
    FOR EACH cl-list BY cl-list.hno:
        ASSIGN
            tocc-rm    = tocc-rm + cl-list.occ-rm
            tocc-rm1   = tocc-rm1 + cl-list.occ-rm1
            tocc-rm2   = tocc-rm2 + cl-list.occ-rm2
            tsale      = tsale    + cl-list.saleable
            tsale1     = tsale1   + cl-list.saleable1
            tsale2     = tsale2   + cl-list.saleable2
            trmrev1    = trmrev1  + cl-list.rmrev1
            trmrev2    = trmrev2  + cl-list.rmrev2
            trmrev     = trmrev  + cl-list.rmrev
            hotel1     = hotel1  + cl-list.hotel1
            hotel2     = hotel2  + cl-list.hotel2
            hotel3     = hotel3  + cl-list.hotel3       
            tocc-proz  = tocc-proz  + cl-list.occ-proz
            tocc-proz1 = tocc-proz1 + cl-list.occ-proz1
            tocc-proz2 = tocc-proz2 + cl-list.occ-proz2.
    END.
   
    /* change by damen 30/03/23 0972D8 */
    FOR EACH cl-list BY cl-list.hno desc:
        IF cl-list.occ-rm NE 0 THEN
            cl-list.avrgrate        = cl-list.rmrev / cl-list.occ-rm.
        IF cl-list.occ-rm1 NE 0 THEN
            cl-list.avrgrate1        = cl-list.rmrev1 / cl-list.occ-rm1.
        IF cl-list.occ-rm2 NE 0 THEN
            cl-list.avrgrate2        = cl-list.rmrev2 / cl-list.occ-rm2.
    
        IF cl-list.saleable NE 0 THEN
            cl-list.yield           = cl-list.rmrev / cl-list.saleable.
        IF cl-list.saleable1 NE 0 THEN
            cl-list.yield1           = cl-list.rmrev1 / cl-list.saleable1.
        IF cl-list.saleable2 NE 0 THEN
            cl-list.yield2           = cl-list.rmrev2 / cl-list.saleable2.
        IF cl-list.hotel3 NE 0 THEN  
            cl-list.hotel3           = (cl-list.occ-rm2 / cl-list.saleable2) * 100. /*wen*/
    
        IF tsale NE 0 THEN
            cl-list.nat-mark         = cl-list.saleable / tsale * 100.
        IF tsale1 NE 0 THEN
            cl-list.nat-mark1        = cl-list.saleable1 / tsale1 * 100.
        IF tsale2 NE 0 THEN
            cl-list.nat-mark2        = cl-list.saleable2 / tsale2 * 100.
    
        IF tocc-rm NE 0 THEN
            cl-list.mark-share      = cl-list.occ-rm / tocc-rm * 100.
        IF tocc-rm1 NE 0 THEN
            cl-list.mark-share1      = cl-list.occ-rm1 / tocc-rm1 * 100.
        IF tocc-rm2 NE 0 THEN
            cl-list.mark-share2      = cl-list.occ-rm2 / tocc-rm2 * 100.

    
        CREATE output-list.
        ASSIGN 
            output-list.hno         = cl-list.hno
            output-list.htlname     = cl-list.htlname
            output-list.occ-rm      = STRING(cl-list.occ-rm, ">>>,>>9")
            output-list.saleable    = STRING(cl-list.saleable, ">>>,>>9")
            output-list.rmrev       = STRING(cl-list.rmrev, "->>,>>>,>>>,>>9.99")
            output-list.occ-rm1     = STRING(cl-list.occ-rm1, ">>>,>>9")
            output-list.saleable1   = STRING(cl-list.saleable1, ">>>,>>9")
            output-list.rmrev1      = STRING(cl-list.rmrev1, "->>,>>>,>>>,>>9.99")
            output-list.occ-rm2     = STRING(cl-list.occ-rm2, ">>>,>>9")
            output-list.saleable2   = STRING(cl-list.saleable2, ">>>,>>9")
            output-list.rmrev2      = STRING(cl-list.rmrev2, "->>>,>>>,>>>,>>9.99")
            output-list.avrgrate    = STRING(cl-list.avrgrate, "->>,>>>,>>>,>>9.99")
            output-list.avrgrate1   = STRING(cl-list.avrgrate1, "->>,>>>,>>>,>>9.99")
            output-list.avrgrate2   = STRING(cl-list.avrgrate2, "->>,>>>,>>>,>>9.99")
            output-list.yield       = STRING(cl-list.yield, "->>,>>>,>>>,>>9.99")
            output-list.yield1      = STRING(cl-list.yield1, "->>,>>>,>>>,>>9.99")
            output-list.yield2      = STRING(cl-list.yield2, "->>,>>>,>>>,>>9.99")
            output-list.nat-mark    = STRING(cl-list.nat-mark, ">>9.99")
            output-list.nat-mark1   = STRING(cl-list.nat-mark1, ">>9.99")
            output-list.nat-mark2   = STRING(cl-list.nat-mark2, ">>9.99")
            output-list.mark-share  = STRING(cl-list.mark-share, ">>9.99")
            output-list.mark-share1 = STRING(cl-list.mark-share1, ">>9.99")
            output-list.mark-share2 = STRING(cl-list.mark-share2, ">>9.99")
            output-list.hotel1      = STRING(cl-list.hotel1, ">>>,>>9.99") /*">>,>>9.99"*/
            output-list.hotel2      = STRING(cl-list.hotel2, ">>>,>>9.99")
            output-list.hotel3      = STRING(cl-list.hotel3, ">>>,>>9.99")
            output-list.occ-proz    = STRING(cl-list.occ-proz, ">>9.99")
            output-list.occ-proz1   = STRING(cl-list.occ-proz1, ">>9.99")
            output-list.occ-proz2   = STRING(cl-list.occ-proz2, ">>9.99")
            .
       /*FT ASSIGN
            /*tocc-rm                 = tocc-rm + cl-list.occ-rm
            tocc-rm1                = tocc-rm1 + cl-list.occ-rm1
            tocc-rm2                = tocc-rm2 + cl-list.occ-rm2
            tsale                   = tsale    + cl-list.saleable
            tsale1                  = tsale1   + cl-list.saleable1
            tsale2                  = tsale2   + cl-list.saleable2*/
            trmrev1                 = trmrev1  + cl-list.rmrev1
            trmrev2                 = trmrev2  + cl-list.rmrev2
            trmrev                  = trmrev  + cl-list.rmrev.*/
    
    END.
    ASSIGN
        hotela = (tocc-rm  / tsale) * 100
        hotelb = (tocc-rm1 / tsale1) * 100
        hotelc = (tocc-rm2 / tsale2) * 100.

    CREATE output-list.
    ASSIGN 
        output-list.hno         = 999999
        output-list.htlname     = translateExtended("T o t a l", lvCAREA, "")

        output-list.occ-rm      = STRING(tocc-rm,  ">>>,>>9")
        output-list.occ-rm1     = STRING(tocc-rm1, ">>>,>>9")
        output-list.occ-rm2     = STRING(tocc-rm2, ">>>,>>9")
        output-list.saleable    = STRING(tsale, ">>>,>>9")
        output-list.saleable1   = STRING(tsale1, ">>>,>>9")
        output-list.saleable2   = STRING(tsale2, ">>>,>>9")

        output-list.rmrev       = STRING(trmrev,  "->>,>>>,>>>,>>9.99")
        output-list.rmrev1      = STRING(trmrev1, "->>,>>>,>>>,>>9.99")
        output-list.rmrev2      = STRING(trmrev2, "->>>,>>>,>>>,>>9.99")
        output-list.nat-mark    = "100.00"
        output-list.nat-mark1   = "100.00"
        output-list.nat-mark2   = "100.00"
        output-list.mark-share  = "100.00"
        output-list.mark-share1 = "100.00"
        output-list.mark-share2 = "100.00"
        output-list.hotel1      = STRING(hotela, ">>>,>>9.99")
        output-list.hotel2      = STRING(hotelb, ">>>,>>9.99")
        output-list.hotel3      = STRING(hotelc, ">>>,>>9.99").

    IF output-list.hotel1 EQ ? THEN output-list.hotel1 = "  0.00". 
    ELSE IF output-list.hotel2 EQ ? THEN output-list.hotel2 = " 0.00". 
    ELSE IF output-list.hotel3 EQ ? THEN output-list.hotel3 = " 0.00". 
            
    IF tocc-rm NE 0 THEN
        output-list.avrgrate   = STRING(trmrev / tocc-rm, "->>,>>>,>>>,>>9.99").
    ELSE output-list.avrgrate  = STRING(0, "->>,>>>,>>>,>>9.99").
    
    IF tocc-rm1 NE 0 THEN
        output-list.avrgrate1  = STRING(trmrev1 / tocc-rm1, "->>,>>>,>>>,>>9.99").
    ELSE output-list.avrgrate1 = STRING(0, "->>,>>>,>>>,>>9.99").
    IF tocc-rm2 NE 0 THEN
        output-list.avrgrate2  = STRING(trmrev2 / tocc-rm2, "->>,>>>,>>>,>>9.99").
    ELSE output-list.avrgrate2 = STRING(0, "->>,>>>,>>>,>>9.99").
    
    
    IF tsale NE 0 THEN
        output-list.yield      = STRING(trmrev / tsale, "->>,>>>,>>>,>>9.99").
    ELSE output-list.yield      = STRING(0, "->>,>>>,>>>,>>9.99").
    
    IF tsale1 NE 0 THEN
        output-list.yield1      = STRING(trmrev1 / tsale1, "->>,>>>,>>>,>>9.99").
    ELSE output-list.yield1      = STRING(0, "->>,>>>,>>>,>>9.99").
    
    IF tsale2 NE 0 THEN
        output-list.yield2      = STRING(trmrev2 / tsale2, "->>,>>>,>>>,>>9.99").
    ELSE output-list.yield2      = STRING(0, "->>,>>>,>>>,>>9.99").

    IF tocc-proz NE 0 THEN
        output-list.occ-proz = STRING(tocc-rm / tsale * 100, ">>9.99").
    ELSE output-list.occ-proz = STRING(0, ">>9.99").

    IF tocc-proz1 NE 0 THEN
        output-list.occ-proz1 = STRING(tocc-rm1 / tsale1 * 100, ">>9.99").
    ELSE output-list.occ-proz1 = STRING(0, ">>9.99").

    IF tocc-proz2 NE 0 THEN
        output-list.occ-proz2 = STRING(tocc-rm2 / tsale2 * 100, ">>9.99").
    ELSE output-list.occ-proz2 = STRING(0, ">>9.99").
END.

PROCEDURE to-date2:
    FOR EACH cl-list:
        DELETE cl-list.
    END.
    FOR EACH output-list:
        DELETE output-list.
    END.
    ASSIGN
        tocc-rm = 0
        tocc-rm1 = 0
        tocc-rm2 = 0
        tsale = 0
        tsale1 = 0
        tsale2 = 0
        trmrev = 0
        trmrev1 = 0
        trmrev2 = 0.

    FOR EACH zinrstat WHERE zinrstat.datum GE f-date AND 
        zinrstat.datum LE t-date AND zinrstat.zinr = "Competitor" NO-LOCK:
        FIND FIRST akt-code WHERE akt-code.aktiongrup = 4 AND akt-code.aktionscode = zinrstat.betriebsnr NO-LOCK NO-ERROR.
    
        FIND FIRST cl-list WHERE cl-list.hno = zinrstat.betriebsnr NO-ERROR.
        IF NOT AVAILABLE cl-list THEN
        DO:
            CREATE cl-list.
            ASSIGN
                cl-list.hno  = zinrstat.betriebsnr.
            IF AVAILABLE akt-code THEN
                cl-list.htlname = akt-code.bezeich.
        END.
    
        IF zinrstat.datum = t-date THEN
        DO:
            ASSIGN
                cl-list.occ-rm      = cl-list.occ-rm + zinrstat.personen
                cl-list.saleable    = cl-list.saleable + zinrstat.zimmeranz
                cl-list.rmrev       = cl-list.rmrev + zinrstat.logisumsatz
                cl-list.hotel1      = (cl-list.occ-rm / cl-list.saleable) * 100. /*wen*/

            IF all-occ THEN /*M 010612 -> add option include compliment */
                    cl-list.occ-rm = cl-list.occ-rm + INT(zinrstat.argtumsatz).

            IF cl-list.saleable NE 0 THEN
                cl-list.occ-proz = cl-list.occ-rm / cl-list.saleable * 100.
        END.
        
        /*IF MONTH(zinrstat.datum) = MONTH(to-date) AND YEAR(zinrstat.datum) = YEAR(to-date) THEN*/
        IF zinrstat.datum GE from-date AND zinrstat.datum LE to-date THEN
        DO:
            ASSIGN
                cl-list.occ-rm1      = cl-list.occ-rm1 + zinrstat.personen
                cl-list.saleable1    = cl-list.saleable1 + zinrstat.zimmeranz
                cl-list.rmrev1       = cl-list.rmrev1 + zinrstat.logisumsatz
                cl-list.hotel2       = (cl-list.occ-rm1 / cl-list.saleable1) * 100 . /*wen*/.
                   
            IF all-occ THEN /*M 010612 -> add option include compliment */
                    cl-list.occ-rm1 = cl-list.occ-rm1 + INT(zinrstat.argtumsatz).

            IF cl-list.saleable1 NE 0 THEN
                cl-list.occ-proz1 = cl-list.occ-rm1 / cl-list.saleable1 * 100.
        END.
        ASSIGN
            cl-list.occ-rm2      = cl-list.occ-rm2      + zinrstat.personen
            cl-list.saleable2    = cl-list.saleable2    + zinrstat.zimmeranz
            cl-list.rmrev2       = cl-list.rmrev2       + zinrstat.logisumsatz.
            cl-list.hotel3       = (cl-list.occ-rm2 / cl-list.saleable2) * 100. /*wen*/
        IF all-occ THEN /*M 010612 -> add option include compliment */
                cl-list.occ-rm2 = cl-list.occ-rm2 + INT(zinrstat.argtumsatz).

        IF cl-list.saleable2 NE 0 THEN
                cl-list.occ-proz2 = cl-list.occ-rm2 / cl-list.saleable2 * 100.
    END.

    /* change by damen 30/03/23 0972D8 */
    FOR EACH cl-list BY cl-list.hno DESC:
        ASSIGN
            tocc-rm    = tocc-rm + cl-list.occ-rm
            tocc-rm1   = tocc-rm1 + cl-list.occ-rm1
            tocc-rm2   = tocc-rm2 + cl-list.occ-rm2
            tsale      = tsale    + cl-list.saleable
            tsale1     = tsale1   + cl-list.saleable1
            tsale2     = tsale2   + cl-list.saleable2
            trmrev1    = trmrev1  + cl-list.rmrev1
            trmrev2    = trmrev2  + cl-list.rmrev2
            trmrev     = trmrev  + cl-list.rmrev
            hotel1     = hotel1  + cl-list.hotel1
            hotel2     = hotel2  + cl-list.hotel2
            hotel3     = hotel3  + cl-list.hotel3  
            tocc-proz  = tocc-proz  + cl-list.occ-proz
            tocc-proz1 = tocc-proz1 + cl-list.occ-proz1
            tocc-proz2 = tocc-proz2 + cl-list.occ-proz2.
    END.
   
    /* change by damen 30/03/23 0972D8 */
    FOR EACH cl-list BY cl-list.hno DESC:
        IF cl-list.occ-rm NE 0 THEN
            cl-list.avrgrate        = cl-list.rmrev / cl-list.occ-rm.
        IF cl-list.occ-rm1 NE 0 THEN
            cl-list.avrgrate1        = cl-list.rmrev1 / cl-list.occ-rm1.
        IF cl-list.occ-rm2 NE 0 THEN
            cl-list.avrgrate2        = cl-list.rmrev2 / cl-list.occ-rm2.
    
        IF cl-list.saleable NE 0 THEN
            cl-list.yield           = cl-list.rmrev / cl-list.saleable.
        IF cl-list.saleable1 NE 0 THEN
            cl-list.yield1           = cl-list.rmrev1 / cl-list.saleable1.
        IF cl-list.saleable2 NE 0 THEN
            cl-list.yield2           = cl-list.rmrev2 / cl-list.saleable2.
        IF cl-list.hotel3 NE 0 THEN  
            cl-list.hotel3           = (cl-list.occ-rm2 / cl-list.saleable2) * 100. /*wen*/
    
        IF tsale NE 0 THEN
            cl-list.nat-mark         = cl-list.saleable / tsale * 100.
        IF tsale1 NE 0 THEN
            cl-list.nat-mark1        = cl-list.saleable1 / tsale1 * 100.
        IF tsale2 NE 0 THEN
            cl-list.nat-mark2        = cl-list.saleable2 / tsale2 * 100.
    
        IF tocc-rm NE 0 THEN
            cl-list.mark-share      = cl-list.occ-rm / tocc-rm * 100.
        IF tocc-rm1 NE 0 THEN
            cl-list.mark-share1      = cl-list.occ-rm1 / tocc-rm1 * 100.
        IF tocc-rm2 NE 0 THEN
            cl-list.mark-share2      = cl-list.occ-rm2 / tocc-rm2 * 100.

    
        CREATE output-list.
        ASSIGN 
            output-list.hno         = cl-list.hno
            output-list.htlname     = cl-list.htlname
            output-list.occ-rm      = STRING(cl-list.occ-rm, ">>>,>>9")
            output-list.saleable    = STRING(cl-list.saleable, ">>>,>>9")
            output-list.rmrev       = STRING(cl-list.rmrev, "->>,>>>,>>>,>>9.99")
            output-list.occ-rm1     = STRING(cl-list.occ-rm1, ">>>,>>9")
            output-list.saleable1   = STRING(cl-list.saleable1, ">>>,>>9")
            output-list.rmrev1      = STRING(cl-list.rmrev1, "->>,>>>,>>>,>>9.99")
            output-list.occ-rm2     = STRING(cl-list.occ-rm2, ">>>,>>9")
            output-list.saleable2   = STRING(cl-list.saleable2, ">>>,>>9")
            output-list.rmrev2      = STRING(cl-list.rmrev2, "->>>,>>>,>>>,>>9.99")
            output-list.avrgrate    = STRING(cl-list.avrgrate, "->>,>>>,>>>,>>9.99")
            output-list.avrgrate1   = STRING(cl-list.avrgrate1, "->>,>>>,>>>,>>9.99")
            output-list.avrgrate2   = STRING(cl-list.avrgrate2, "->>,>>>,>>>,>>9.99")
            output-list.yield       = STRING(cl-list.yield, "->>,>>>,>>>,>>9.99")
            output-list.yield1      = STRING(cl-list.yield1, "->>,>>>,>>>,>>9.99")
            output-list.yield2      = STRING(cl-list.yield2, "->>,>>>,>>>,>>9.99")
            output-list.nat-mark    = STRING(cl-list.nat-mark, ">>9.99")
            output-list.nat-mark1   = STRING(cl-list.nat-mark1, ">>9.99")
            output-list.nat-mark2   = STRING(cl-list.nat-mark2, ">>9.99")
            output-list.mark-share  = STRING(cl-list.mark-share, ">>9.99")
            output-list.mark-share1 = STRING(cl-list.mark-share1, ">>9.99")
            output-list.mark-share2 = STRING(cl-list.mark-share2, ">>9.99")
            output-list.hotel1      = STRING(cl-list.hotel1, ">>>,>>9.99") /*">>,>>9.99"*/
            output-list.hotel2      = STRING(cl-list.hotel2, ">>>,>>9.99")
            output-list.hotel3      = STRING(cl-list.hotel3, ">>>,>>9.99")
            output-list.occ-proz    = STRING(cl-list.occ-proz, ">>9.99")
            output-list.occ-proz1   = STRING(cl-list.occ-proz1, ">>9.99")
            output-list.occ-proz2   = STRING(cl-list.occ-proz2, ">>9.99")
            .
    END.
    ASSIGN
        hotela = (tocc-rm  / tsale) * 100
        hotelb = (tocc-rm1 / tsale1) * 100
        hotelc = (tocc-rm2 / tsale2) * 100.

    CREATE output-list.
    ASSIGN 
        output-list.hno         = 999999
        output-list.htlname     = translateExtended("T o t a l", lvCAREA, "")

        output-list.occ-rm      = STRING(tocc-rm,  ">>>,>>9")
        output-list.occ-rm1     = STRING(tocc-rm1, ">>>,>>9")
        output-list.occ-rm2     = STRING(tocc-rm2, ">>>,>>9")
        output-list.saleable    = STRING(tsale, ">>>,>>9")
        output-list.saleable1   = STRING(tsale1, ">>>,>>9")
        output-list.saleable2   = STRING(tsale2, ">>>,>>9")

        output-list.rmrev       = STRING(trmrev,  "->>,>>>,>>>,>>9.99")
        output-list.rmrev1      = STRING(trmrev1, "->>,>>>,>>>,>>9.99")
        output-list.rmrev2      = STRING(trmrev2, "->>>,>>>,>>>,>>9.99")
        output-list.nat-mark    = "100.00"
        output-list.nat-mark1   = "100.00"
        output-list.nat-mark2   = "100.00"
        output-list.mark-share  = "100.00"
        output-list.mark-share1 = "100.00"
        output-list.mark-share2 = "100.00"
        output-list.hotel1      = STRING(hotela, ">>>,>>9.99")
        output-list.hotel2      = STRING(hotelb, ">>>,>>9.99")
        output-list.hotel3      = STRING(hotelc, ">>>,>>9.99").

    IF output-list.hotel1 EQ ? THEN output-list.hotel1 = "  0.00". 
    ELSE IF output-list.hotel2 EQ ? THEN output-list.hotel2 = " 0.00". 
    ELSE IF output-list.hotel3 EQ ? THEN output-list.hotel3 = " 0.00". 

    IF tocc-rm NE 0 THEN
        output-list.avrgrate   = STRING(trmrev / tocc-rm, "->>,>>>,>>>,>>9.99").
    ELSE output-list.avrgrate  = STRING(0, "->>,>>>,>>>,>>9.99").
    
    IF tocc-rm1 NE 0 THEN
        output-list.avrgrate1  = STRING(trmrev1 / tocc-rm1, "->>,>>>,>>>,>>9.99").
    ELSE output-list.avrgrate1 = STRING(0, "->>,>>>,>>>,>>9.99").
    IF tocc-rm2 NE 0 THEN
        output-list.avrgrate2  = STRING(trmrev2 / tocc-rm2, "->>,>>>,>>>,>>9.99").
    ELSE output-list.avrgrate2 = STRING(0, "->>,>>>,>>>,>>9.99").
    
    
    IF tsale NE 0 THEN
        output-list.yield      = STRING(trmrev / tsale, "->>,>>>,>>>,>>9.99").
    ELSE output-list.yield      = STRING(0, "->>,>>>,>>>,>>9.99").
    
    IF tsale1 NE 0 THEN
        output-list.yield1      = STRING(trmrev1 / tsale1, "->>,>>>,>>>,>>9.99").
    ELSE output-list.yield1      = STRING(0, "->>,>>>,>>>,>>9.99").
    
    IF tsale2 NE 0 THEN
        output-list.yield2      = STRING(trmrev2 / tsale2, "->>,>>>,>>>,>>9.99").
    ELSE output-list.yield2      = STRING(0, "->>,>>>,>>>,>>9.99").

    IF tocc-proz NE 0 THEN
        output-list.occ-proz = STRING((tocc-rm / tsale) * 100, ">>9.99").
    ELSE output-list.occ-proz = STRING(0, ">>9.99").

    IF tocc-proz1 NE 0 THEN
        output-list.occ-proz1 = STRING((tocc-rm1 / tsale1) * 100, ">>9.99").
    ELSE output-list.occ-proz1 = STRING(0, ">>9.99").

    IF tocc-proz2 NE 0 THEN
        output-list.occ-proz2 = STRING((tocc-rm2 / tsale2) * 100, ">>9.99").
    ELSE output-list.occ-proz2 = STRING(0, ">>9.99").
END.


