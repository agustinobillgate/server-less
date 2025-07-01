DEFINE TEMP-TABLE output-list
    FIELD zikatnr       AS INTEGER
    FIELD kurzbez       AS CHARACTER FORMAT "x(30)"
    FIELD bezeichnung   AS CHARACTER FORMAT "x(30)"
    FIELD m-anztage     AS INTEGER
    FIELD y-anztage     AS INTEGER
    FIELD m-logis       AS DECIMAL FORMAT "->>,>>>,>>>,>>>,>>>,>>>,>>9.99"
    FIELD y-logis       AS DECIMAL FORMAT "->>,>>>,>>>,>>>,>>>,>>>,>>9.99"
    FIELD m-los         AS DECIMAL /*length of stay*/
    FIELD y-los         AS DECIMAL /*length of stay*/
    FIELD m-erwachs     AS INTEGER 
    FIELD y-erwachs     AS INTEGER
    FIELD m-kind        AS INTEGER
    FIELD y-kind        AS INTEGER
    FIELD m-avrg-logis  AS DECIMAL FORMAT "->>,>>>,>>>,>>>,>>>,>>>,>>9.99"
    FIELD y-avrg-logis  AS DECIMAL FORMAT "->>,>>>,>>>,>>>,>>>,>>>,>>9.99"
    FIELD m-resv        AS INTEGER
    FIELD y-resv        AS INTEGER
    .

DEFINE INPUT PARAMETER to-date AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

/* DEFINE VARIABLE to-date AS DATE NO-UNDO INIT "12/31/23". */
DEFINE VARIABLE fdate   AS DATE NO-UNDO.
DEFINE VARIABLE yy      AS INTEGER  NO-UNDO.

DEFINE VARIABLE curr-zikatnr        AS INTEGER NO-UNDO.

DEFINE VARIABLE tot-m-anztage       AS INTEGER NO-UNDO. 
DEFINE VARIABLE tot-y-anztage       AS INTEGER NO-UNDO. 
DEFINE VARIABLE tot-m-logis         AS DECIMAL NO-UNDO FORMAT "->>,>>>,>>>,>>>,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-y-logis         AS DECIMAL NO-UNDO FORMAT "->>,>>>,>>>,>>>,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-m-erwachs       AS INTEGER NO-UNDO. 
DEFINE VARIABLE tot-y-erwachs       AS INTEGER NO-UNDO. 
DEFINE VARIABLE tot-m-kind          AS INTEGER NO-UNDO. 
DEFINE VARIABLE tot-y-kind          AS INTEGER NO-UNDO. 
DEFINE VARIABLE tot-m-avrg-logis    AS DECIMAL NO-UNDO FORMAT "->>,>>>,>>>,>>>,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-y-avrg-logis    AS DECIMAL NO-UNDO FORMAT "->>,>>>,>>>,>>>,>>>,>>>,>>9.99".

DEFINE VARIABLE tot-m-room-resv     AS INTEGER NO-UNDO.
DEFINE VARIABLE tot-y-room-resv     AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-m-resnr        AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-y-resnr        AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-m-reslinnr     AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-y-reslinnr     AS INTEGER NO-UNDO.

DEFINE VARIABLE t-m-anztage        AS INTEGER NO-UNDO.
DEFINE VARIABLE t-y-anztage        AS INTEGER NO-UNDO.
DEFINE VARIABLE t-m-logis          AS DECIMAL NO-UNDO FORMAT "->>,>>>,>>>,>>>,>>>,>>>,>>9.99".
DEFINE VARIABLE t-y-logis          AS DECIMAL NO-UNDO FORMAT "->>,>>>,>>>,>>>,>>>,>>>,>>9.99".
DEFINE VARIABLE t-m-erwachs        AS INTEGER NO-UNDO.
DEFINE VARIABLE t-y-erwachs        AS INTEGER NO-UNDO.
DEFINE VARIABLE t-m-kind           AS INTEGER NO-UNDO.
DEFINE VARIABLE t-y-kind           AS INTEGER NO-UNDO.
DEFINE VARIABLE t-m-room-resv      AS INTEGER NO-UNDO.
DEFINE VARIABLE t-y-room-resv      AS INTEGER NO-UNDO.
DEFINE VARIABLE t-m-los            AS DECIMAL NO-UNDO.
DEFINE VARIABLE t-y-los            AS DECIMAL NO-UNDO.
DEFINE VARIABLE t-m-avrg-logis     AS DECIMAL NO-UNDO FORMAT "->>,>>>,>>>,>>>,>>>,>>>,>>9.99".
DEFINE VARIABLE t-y-avrg-logis     AS DECIMAL NO-UNDO FORMAT "->>,>>>,>>>,>>>,>>>,>>>,>>9.99".

yy = YEAR(to-date).
fdate = DATE(1,1,yy).

tot-m-anztage = 0.
tot-y-anztage = 0.
tot-m-logis = 0.0.
tot-y-logis = 0.0.
tot-m-erwachs = 0.
tot-y-erwachs = 0.
tot-m-kind = 0.
tot-y-kind = 0.
tot-m-room-resv = 0.
tot-y-room-resv = 0.

t-m-anztage   = 0. 
t-y-anztage   = 0. 
t-m-logis     = 0. 
t-y-logis     = 0. 
t-m-erwachs   = 0. 
t-y-erwachs   = 0. 
t-m-kind      = 0. 
t-y-kind      = 0. 
t-m-room-resv = 0. 
t-y-room-resv = 0. 
t-m-los       = 0. 
t-y-los       = 0. 
t-m-avrg-logis= 0. 
t-y-avrg-logis= 0. 

curr-m-resnr = -1.
curr-y-resnr = -1.
curr-zikatnr = -1.

FOR EACH genstat WHERE genstat.datum GE fdate
    AND genstat.datum LE to-date
    AND genstat.zikatnr NE 0 NO-LOCK,
    FIRST zimkateg WHERE zimkateg.zikatnr EQ genstat.zikatnr NO-LOCK,
/*     FIRST reservation WHERE reservation.resnr EQ genstat.resnr NO-LOCK,  */
    FIRST res-line WHERE res-line.resnr EQ genstat.resnr AND res-line.reslinnr EQ genstat.res-int[1] NO-LOCK 
    BY zimkateg.zikatnr BY genstat.resnr BY genstat.res-int[1]:

    IF curr-zikatnr NE zimkateg.zikatnr AND AVAILABLE output-list THEN
    DO:
        ASSIGN
            output-list.m-anztage    = tot-m-anztage
            output-list.y-anztage    = tot-y-anztage
            output-list.m-logis      = tot-m-logis
            output-list.y-logis      = tot-y-logis
            output-list.m-los        = tot-m-anztage / tot-m-room-resv
            output-list.y-los        = tot-y-anztage / tot-y-room-resv
            output-list.m-erwachs    = tot-m-erwachs
            output-list.y-erwachs    = tot-y-erwachs
            output-list.m-kind       = tot-m-kind
            output-list.y-kind       = tot-y-kind
            output-list.m-resv       = tot-m-room-resv
            output-list.y-resv       = tot-y-room-resv
        .

        /* count total */
         t-m-anztage   = t-m-anztage + tot-m-anztage.
         t-y-anztage   = t-y-anztage + tot-y-anztage.
         t-m-logis     = t-m-logis + tot-m-logis.
         t-y-logis     = t-y-logis + tot-y-logis.
         t-m-erwachs   = t-m-erwachs + tot-m-erwachs.
         t-y-erwachs   = t-y-erwachs + tot-y-erwachs.
         t-m-kind      = t-m-kind + tot-m-kind.
         t-y-kind      = t-y-kind + tot-y-kind.
         t-m-room-resv = t-m-room-resv + tot-m-room-resv.
         t-y-room-resv = t-y-room-resv + tot-y-room-resv.
         t-m-los       = t-m-los + (tot-m-anztage / tot-m-room-resv).
         t-y-los       = t-y-los + (tot-y-anztage / tot-y-room-resv).

        /* handle case undefined */
        IF tot-m-logis EQ 0.0 THEN
            ASSIGN 
                output-list.m-avrg-logis = 0.0
                t-m-avrg-logis = t-m-avrg-logis + 0.0.
        ELSE 
            ASSIGN output-list.m-avrg-logis = tot-m-logis / tot-m-anztage
                t-m-avrg-logis = t-m-avrg-logis + (tot-m-logis / tot-m-anztage).
        IF tot-y-logis EQ 0.0 THEN
            ASSIGN 
                output-list.y-avrg-logis = 0.0
                t-y-avrg-logis = t-y-avrg-logis + 0.0.
        ELSE 
            ASSIGN output-list.y-avrg-logis = tot-y-logis / tot-y-anztage
                t-y-avrg-logis = t-y-avrg-logis + (tot-y-logis / tot-y-anztage).

        tot-m-anztage = 0.
        tot-y-anztage = 0.
        tot-m-logis = 0.0.
        tot-y-logis = 0.0.
        tot-m-erwachs = 0.
        tot-y-erwachs = 0.
        tot-m-kind = 0.
        tot-y-kind = 0.
        tot-m-room-resv = 0.
        tot-y-room-resv = 0.
    END.

    FIND FIRST output-list WHERE output-list.zikatnr EQ zimkateg.zikatnr
        AND output-list.kurzbez EQ zimkateg.kurzbez NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE output-list THEN
    DO:
        CREATE output-list.
        ASSIGN
            output-list.zikatnr      = zimkateg.zikatnr
            output-list.kurzbez      = zimkateg.kurzbez
            output-list.bezeichnung  = zimkateg.bezeichnung
            .
        curr-zikatnr = zimkateg.zikatnr.
        curr-m-resnr = -1.
        curr-y-resnr = -1.
    END.

    IF MONTH(genstat.datum) EQ MONTH(to-date) THEN
    DO:
        ASSIGN
            tot-m-anztage   = tot-m-anztage + 1
            tot-m-logis     = tot-m-logis + genstat.logis
            tot-m-erwachs   = tot-m-erwachs + INTEGER(genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2)
            tot-m-kind      = tot-m-kind + INTEGER(genstat.kind1 + genstat.kind2)
            .
        IF curr-m-resnr NE genstat.resnr OR curr-m-reslinnr NE genstat.res-int[1] THEN
        DO:
            tot-m-room-resv = tot-m-room-resv + 1.
            curr-m-reslinnr = res-line.reslinnr.
            curr-m-resnr    = genstat.resnr.
        END.
            
    END.
    ASSIGN
        tot-y-anztage   = tot-y-anztage + 1
        tot-y-logis     = tot-y-logis + genstat.logis
        tot-y-erwachs   = tot-y-erwachs + INTEGER(genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2)
        tot-y-kind      = tot-y-kind + INTEGER(genstat.kind1 + genstat.kind2)
        .
    IF curr-y-resnr NE genstat.resnr OR curr-m-reslinnr NE genstat.res-int[1] THEN
    DO:
        tot-y-room-resv = tot-y-room-resv + 1.
        curr-y-reslinnr = res-line.reslinnr.
        curr-y-resnr    = genstat.resnr.
    END.
END.

FIND LAST output-list NO-LOCK NO-ERROR.
IF AVAILABLE output-list THEN DO:
    ASSIGN
      output-list.m-anztage    = tot-m-anztage
      output-list.y-anztage    = tot-y-anztage
      output-list.m-logis      = tot-m-logis
      output-list.y-logis      = tot-y-logis
      output-list.m-los        = tot-m-anztage / tot-m-room-resv 
      output-list.y-los        = tot-y-anztage / tot-y-room-resv 
      output-list.m-erwachs    = tot-m-erwachs
      output-list.y-erwachs    = tot-y-erwachs
      output-list.m-kind       = tot-m-kind
      output-list.y-kind       = tot-y-kind
      output-list.m-resv       = tot-m-room-resv 
      output-list.y-resv       = tot-y-room-resv 
        .

    /* count total */                                             
     t-m-anztage   = t-m-anztage + tot-m-anztage.                 
     t-y-anztage   = t-y-anztage + tot-y-anztage.                 
     t-m-logis     = t-m-logis + tot-m-logis.                     
     t-y-logis     = t-y-logis + tot-y-logis.                     
     t-m-erwachs   = t-m-erwachs + tot-m-erwachs.                 
     t-y-erwachs   = t-y-erwachs + tot-y-erwachs.                 
     t-m-kind      = t-m-kind + tot-m-kind.                       
     t-y-kind      = t-y-kind + tot-y-kind.                       
     t-m-room-resv = t-m-room-resv + tot-m-room-resv.             
     t-y-room-resv = t-y-room-resv + tot-y-room-resv.             
     t-m-los       = t-m-los + (tot-m-anztage / tot-m-room-resv). 
     t-y-los       = t-y-los + (tot-y-anztage / tot-y-room-resv). 

    /* handle case undefined */
    IF tot-m-logis EQ 0.0 THEN
        ASSIGN 
            output-list.m-avrg-logis = 0.0
            t-m-avrg-logis = t-m-avrg-logis + 0.0.
    ELSE 
        ASSIGN output-list.m-avrg-logis = tot-m-logis / tot-m-anztage
            t-m-avrg-logis = t-m-avrg-logis + (tot-m-logis / tot-m-anztage).
    IF tot-y-logis EQ 0.0 THEN
        ASSIGN 
            output-list.y-avrg-logis = 0.0
            t-y-avrg-logis = t-y-avrg-logis + 0.0.
    ELSE 
        ASSIGN output-list.y-avrg-logis = tot-y-logis / tot-y-anztage
            t-y-avrg-logis = t-y-avrg-logis + (tot-y-logis / tot-y-anztage).

    /* create total*/
    CREATE output-list.
    ASSIGN
        output-list.zikatnr      = 0
        output-list.kurzbez      = ""
        output-list.bezeichnung  = "T O T A L"
        output-list.m-anztage    = t-m-anztage
        output-list.y-anztage    = t-y-anztage
        output-list.m-logis      = t-m-logis
        output-list.y-logis      = t-y-logis
        output-list.m-los        = t-m-anztage / t-m-room-resv
        output-list.y-los        = t-y-anztage / t-y-room-resv
        output-list.m-erwachs    = t-m-erwachs
        output-list.y-erwachs    = t-y-erwachs
        output-list.m-kind       = t-m-kind
        output-list.y-kind       = t-y-kind
        output-list.m-avrg-logis = t-m-avrg-logis
        output-list.y-avrg-logis = t-y-avrg-logis
        output-list.m-resv       = t-m-room-resv
        output-list.y-resv       = t-y-room-resv
          .   
END.    
