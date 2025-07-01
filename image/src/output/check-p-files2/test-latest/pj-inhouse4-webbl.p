DEFINE TEMP-TABLE inhouse-guest-list 
    FIELD flag          AS INTEGER 
    FIELD karteityp     AS INTEGER 
    FIELD nr            AS INTEGER   FORMAT ">>>9" 
    FIELD vip           AS CHAR      FORMAT "x(5)" 
    FIELD resnr         AS INTEGER   FORMAT ">>>>>9" 
    FIELD firstname     AS CHAR      FORMAT "x(32)" 
    FIELD lastname      AS CHAR      FORMAT "x(32)" 
    FIELD birthdate     AS CHAR      FORMAT "x(10)"
    FIELD groupname     AS CHAR      FORMAT "x(24)" 
    FIELD rmno          AS CHAR	  
    FIELD qty           AS INTEGER   FORMAT ">>9" 
    FIELD arrive        AS DATE 
    FIELD depart        AS DATE 
    FIELD rmcat         AS CHAR      FORMAT "x(6)" 
    FIELD ratecode      AS CHAR      FORMAT "x(15)"
    FIELD zipreis       AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"
    FIELD kurzbez       AS CHAR 
    FIELD bezeich       AS CHAR 
    FIELD a             AS INTEGER   FORMAT "9" 
    FIELD c             AS INTEGER   FORMAT "9" 
    FIELD co            AS INTEGER   FORMAT ">9" 
    FIELD pax           AS CHAR      FORMAT "x(6)" 
    FIELD nat           AS CHAR      FORMAT "x(3)" 
    FIELD nation        AS CHAR 
    FIELD argt          AS CHAR      FORMAT "x(6)" 
    FIELD company       AS CHAR      FORMAT "x(18)" 
    FIELD flight        AS CHAR      FORMAT "x(6)" 
    FIELD etd           AS CHAR      FORMAT "99:99" 
    FIELD paym          AS INTEGER   FORMAT ">>9" 
    FIELD segm          AS CHAR      FORMAT "x(12)"
    FIELD telefon       AS CHAR      FORMAT "x(24)" 
    FIELD mobil-tel     AS CHAR      FORMAT "x(16)" 
    FIELD created       AS DATE      FORMAT "99/99/99"
    FIELD createID      AS CHAR      FORMAT "x(4)"
    FIELD bemerk        AS CHAR      FORMAT "x(100)"
    FIELD bemerk1       AS CHAR      FORMAT "x(32)" 
    FIELD ci-time       AS CHAR
    FIELD curr          AS CHAR      FORMAT "x(4)"
    FIELD inhousedate   AS DATE
    FIELD sob           AS CHAR      FORMAT "x(25)" 
    FIELD gastnr        AS INTEGER
    FIELD lodging       AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
    FIELD breakfast     AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
    FIELD lunch         AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
    FIELD dinner        AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"    
    FIELD otherev       AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"       
    FIELD rechnr        AS INT            
    FIELD memberno      AS CHAR      FORMAT "x(15)"     
    FIELD membertype    AS CHAR      FORMAT "x(20)"     
    FIELD email         AS CHAR      FORMAT "x(30)"  
    FIELD localreg      AS CHAR      FORMAT "x(20)"  
    FIELD c-zipreis     AS CHAR      FORMAT "x(18)"
    FIELD c-lodging     AS CHAR     FORMAT "x(18)"
    FIELD c-breakfast   AS CHAR     FORMAT "x(18)"     
    FIELD c-lunch       AS CHAR     FORMAT "x(18)"    
    FIELD c-dinner      AS CHAR     FORMAT "x(18)"    
    FIELD c-otherev     AS CHAR     FORMAT "x(18)"
    FIELD c-a           AS CHAR  
    FIELD c-c           AS CHAR  
    FIELD c-co          AS CHAR  
    FIELD c-rechnr      AS CHAR  
    FIELD c-resnr       AS CHAR  
    FIELD night         AS CHAR     FORMAT "x(5)"
    FIELD city          AS CHAR     FORMAT "x(32)" 
    FIELD keycard       AS CHAR     FORMAT "x(6)"  
    FIELD co-time       AS CHAR                                     
    FIELD pay-art       AS CHAR     FORMAT "x(20)"
    FIELD etage         AS INTEGER
    FIELD zinr-bez      AS CHAR     /*Gerald 7E2311*/
    FIELD flag-guest    AS INTEGER  /*Gerald 7E2311*/
    .      

DEFINE TEMP-TABLE output-list 
    FIELD flag          AS INTEGER 
    FIELD karteityp     AS INTEGER 
    FIELD nr            AS INTEGER   FORMAT ">>>9" 
    FIELD vip           AS CHAR      FORMAT "x(5)" 
    FIELD resnr         AS INTEGER   FORMAT ">>>>>9" 
    FIELD firstname     AS CHAR      FORMAT "x(32)" 
    FIELD lastname      AS CHAR      FORMAT "x(32)" 
    FIELD birthdate     AS CHAR      FORMAT "x(10)"
    FIELD groupname     AS CHAR      FORMAT "x(24)" 
    FIELD rmno          AS CHAR	  
    FIELD qty           AS INTEGER   FORMAT ">>9" 
    FIELD arrive        AS DATE 
    FIELD depart        AS DATE 
    FIELD rmcat         AS CHAR      FORMAT "x(6)" 
    FIELD ratecode      AS CHAR      FORMAT "x(15)"
    FIELD zipreis       AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"
    FIELD kurzbez       AS CHAR 
    FIELD bezeich       AS CHAR 
    FIELD a             AS INTEGER   FORMAT "9" 
    FIELD c             AS INTEGER   FORMAT "9" 
    FIELD co            AS INTEGER   FORMAT ">9" 
    FIELD pax           AS CHAR      FORMAT "x(6)" 
    FIELD nat           AS CHAR      FORMAT "x(3)" 
    FIELD nation        AS CHAR 
    FIELD argt          AS CHAR      FORMAT "x(6)" 
    FIELD company       AS CHAR      FORMAT "x(18)" 
    FIELD flight        AS CHAR      FORMAT "x(6)" 
    FIELD etd           AS CHAR      FORMAT "99:99" 
    FIELD paym          AS INTEGER   FORMAT ">>9" 
    FIELD segm          AS CHAR      FORMAT "x(12)"
    FIELD telefon       AS CHAR      FORMAT "x(24)" 
    FIELD mobil-tel     AS CHAR      FORMAT "x(16)" 
    FIELD created       AS DATE      FORMAT "99/99/99"
    FIELD createID      AS CHAR      FORMAT "x(4)"
    FIELD bemerk        AS CHAR      FORMAT "x(100)"
    FIELD bemerk1       AS CHAR      FORMAT "x(32)" 
    FIELD ci-time       AS CHAR
    FIELD curr          AS CHAR      FORMAT "x(4)"
    FIELD inhousedate   AS DATE
    FIELD sob           AS CHAR      FORMAT "x(25)" 
    FIELD gastnr        AS INTEGER
    FIELD lodging       AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
    FIELD breakfast     AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
    FIELD lunch         AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
    FIELD dinner        AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"    
    FIELD otherev       AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"       
    FIELD rechnr        AS INT            
    FIELD memberno      AS CHAR      FORMAT "x(15)"     
    FIELD membertype    AS CHAR      FORMAT "x(20)"     
    FIELD email         AS CHAR      FORMAT "x(30)"  
    FIELD localreg      AS CHAR      FORMAT "x(20)"  
    FIELD c-zipreis     AS CHAR      FORMAT "x(18)"
    FIELD c-lodging     AS CHAR     FORMAT "x(18)"
    FIELD c-breakfast   AS CHAR     FORMAT "x(18)"     
    FIELD c-lunch       AS CHAR     FORMAT "x(18)"    
    FIELD c-dinner      AS CHAR     FORMAT "x(18)"    
    FIELD c-otherev     AS CHAR     FORMAT "x(18)"
    FIELD c-a           AS CHAR  
    FIELD c-c           AS CHAR  
    FIELD c-co          AS CHAR  
    FIELD c-rechnr      AS CHAR  
    FIELD c-resnr       AS CHAR  
    FIELD night         AS CHAR     FORMAT "x(5)"
    FIELD city          AS CHAR     FORMAT "x(32)" 
    FIELD keycard       AS CHAR     FORMAT "x(6)"  
    FIELD co-time       AS CHAR                                     
    FIELD pay-art       AS CHAR     FORMAT "x(20)" 
    FIELD etage         AS INTEGER
    FIELD zinr-bez      AS CHAR     /*Gerald 7E2311*/
    FIELD flag-guest    AS INTEGER  /*Gerald 7E2311*/
    . 

DEFINE TEMP-TABLE s-list 
    FIELD rmcat       AS CHAR FORMAT "x(6)" 
    FIELD bezeich     AS CHAR FORMAT "x(24)" 
    FIELD nat         AS CHAR FORMAT "x(24)" 
    FIELD anz         AS INTEGER FORMAT ">>9" 
    FIELD adult       AS INTEGER FORMAT ">>9" 
    FIELD proz        AS DECIMAL FORMAT ">>9.99" 
    FIELD child       AS INTEGER FORMAT ">>9"
    FIELD proz-qty    AS DECIMAL FORMAT ">>9.99"
    FIELD rev         AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
    FIELD proz-rev    AS DECIMAL FORMAT ">>9.99"
    FIELD arr         AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
 .  


DEFINE TEMP-TABLE zikat-list 
    FIELD selected AS LOGICAL INITIAL NO 
    FIELD zikatnr  AS INTEGER 
    FIELD kurzbez  AS CHAR 
    FIELD bezeich  AS CHAR FORMAT "x(32)"
.

DEFINE TEMP-TABLE t-buff-queasy LIKE queasy.

DEFINE INPUT PARAMETER sorttype        AS INT.
DEFINE INPUT PARAMETER from-date       AS DATE.
DEFINE INPUT PARAMETER to-date         AS DATE.
DEFINE INPUT PARAMETER froom           AS CHAR.
DEFINE INPUT PARAMETER troom           AS CHAR.
DEFINE INPUT PARAMETER exc-depart      AS LOGICAL.
DEFINE INPUT PARAMETER incl-gcomment   AS LOGICAL.
DEFINE INPUT PARAMETER incl-rsvcomment AS LOGICAL.
DEFINE INPUT PARAMETER disp-accompany  AS LOGICAL.
DEFINE INPUT PARAMETER idFlag          AS CHAR.


DEFINE VARIABLE curr-date       AS DATE.
DEFINE VARIABLE curr-gastnr     AS INT.

DEFINE VARIABLE str    AS CHAR NO-UNDO.
DEFINE VARIABLE htl-no AS CHAR NO-UNDO.
DEFINE STREAM s1.

DEFINE VARIABLE tdate   AS CHAR NO-UNDO.
DEFINE VARIABLE crdate  AS CHAR NO-UNDO.
DEFINE VARIABLE cgdate  AS CHAR NO-UNDO.
DEFINE VARIABLE counter AS INTEGER NO-UNDO.
DEFINE VARIABLE company AS CHAR NO-UNDO.

DEFINE VARIABLE tot-payrm   AS INTEGER INITIAL 0.  
DEFINE VARIABLE tot-rm      AS INTEGER INITIAL 0.  
DEFINE VARIABLE tot-a       AS INTEGER INITIAL 0.  
DEFINE VARIABLE tot-c       AS INTEGER INITIAL 0.  
DEFINE VARIABLE tot-co      AS INTEGER INITIAL 0.  
DEFINE VARIABLE tot-avail   AS INTEGER INITIAL 0.  
DEFINE VARIABLE inactive    AS INTEGER INITIAL 0.  
DEFINE VARIABLE tot-keycard AS INTEGER INITIAL 0.
DEFINE VARIABLE bemerk      AS CHAR.
DEFINE VARIABLE bemerk1     AS CHAR.
DEFINE VARIABLE bezeich     AS CHAR.


DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER tqueasy FOR queasy.


/*************************************** PROCCESS ***************************************/
CREATE queasy.
ASSIGN queasy.KEY      = 285
       queasy.char1    = "Inhouse List"
       queasy.number1  = 1
       queasy.number2  = INT(idFlag).
RELEASE queasy.


DEFINE VARIABLE curr-time AS INTEGER.
ASSIGN curr-time = TIME.

RUN htpdate.p(87, OUTPUT curr-date).

FOR EACH zimkateg NO-LOCK BY zimkateg.kurzbez: 
    CREATE zikat-list. 
    ASSIGN 
      zikat-list.zikatnr = zimkateg.zikatnr 
      zikat-list.kurzbez = zimkateg.kurzbez 
      zikat-list.bezeich = zimkateg.bezeich. 
END. 
FOR EACH zikat-list:
    zikat-list.selected = YES.
END.


FIND FIRST paramtext WHERE paramtext.txtnr = 243 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN
  RUN decode-string(paramtext.ptexte, OUTPUT htl-no). 


RUN pj-inhouse4-btn-go_4-cldbl.p
    (1, from-date, to-date, curr-date, curr-gastnr, froom, troom, exc-depart,
    incl-gcomment, incl-rsvcomment, "PJ-inhouse2", disp-accompany, INPUT TABLE zikat-list,
    OUTPUT tot-payrm, OUTPUT tot-rm, OUTPUT tot-a, OUTPUT tot-c,
    OUTPUT tot-co, OUTPUT tot-avail, OUTPUT inactive, OUTPUT tot-keycard,
    OUTPUT TABLE output-list, OUTPUT TABLE s-list, OUTPUT TABLE t-buff-queasy).

IF sorttype EQ 1 OR sorttype EQ 3 THEN /* By RoomNo */
DO:
    IF sorttype EQ 1 THEN
    DO:
        FOR EACH output-list NO-LOCK BY output-list.nr:
            counter = counter + 1.
            ASSIGN output-list.nr = counter.
    
            CREATE inhouse-guest-list.
            BUFFER-COPY output-list TO inhouse-guest-list.
        END.
    END.
    ELSE
    DO:
        FOR EACH output-list NO-LOCK BY output-list.etage BY output-list.rmno:
            counter = counter + 1.
            ASSIGN output-list.nr = counter.
    
            CREATE inhouse-guest-list.
            BUFFER-COPY output-list TO inhouse-guest-list.
        END.
    END.
END.
ELSE /* By Compnay */
DO:
    DEFINE BUFFER bufflist FOR output-list.

    FOR EACH output-list BY output-list.company:
        IF company NE output-list.company THEN
        DO:
            company = output-list.company.
            CREATE inhouse-guest-list.
            inhouse-guest-list.rmcat = output-list.company.

            FOR EACH bufflist WHERE bufflist.company EQ company:
                counter = counter + 1.
                CREATE inhouse-guest-list.
                BUFFER-COPY bufflist TO inhouse-guest-list.
                inhouse-guest-list.nr = counter.
            END.   
            CREATE inhouse-guest-list.
        END.
    END.
END.



FIND FIRST inhouse-guest-list NO-ERROR.
DO WHILE AVAILABLE inhouse-guest-list:

    IF inhouse-guest-list.bezeich = ? THEN bezeich = "".
    ELSE bezeich = inhouse-guest-list.bezeich.
    IF inhouse-guest-list.bemerk = ? THEN bemerk = "".
    ELSE bemerk = inhouse-guest-list.bemerk.
    IF inhouse-guest-list.bemerk1 = ? THEN bemerk1 = "".
    ELSE bemerk1 = inhouse-guest-list.bemerk1.

    ASSIGN bezeich = REPLACE(bezeich, CHR(10),"")
           bezeich = REPLACE(bezeich, CHR(13),"")
           bemerk  = REPLACE(bemerk, CHR(10),"")
           bemerk  = REPLACE(bemerk, CHR(13),"")
           bemerk  = REPLACE(bemerk, "|","")
           counter          = counter + 1
           .

    RUN add-html(bezeich,OUTPUT bezeich).
    RUN clean-html(bezeich,OUTPUT bezeich).

    RUN add-html(bemerk,OUTPUT bemerk).
    RUN clean-html(bemerk,OUTPUT bemerk).
    
    RUN add-html(bemerk1,OUTPUT bemerk1).
    RUN clean-html(bemerk1,OUTPUT bemerk1).

    CREATE queasy.
    ASSIGN queasy.KEY   = 280
           queasy.char1 = "Inhouse List"
           queasy.number2 = INT(idFlag)
           queasy.char3 = STRING(bezeich)                                + "|" +
                          STRING(bemerk)                                 + "|" +
                          STRING(bemerk1)                                  
           queasy.char2 = STRING(inhouse-guest-list.flag)        + "|" +  /*1*/
                          STRING(inhouse-guest-list.karteityp)   + "|" +  /*2*/
                          STRING(inhouse-guest-list.nr)          + "|" +  /*3*/
                          inhouse-guest-list.vip                 + "|" +  /*4*/
                          STRING(inhouse-guest-list.resnr)       + "|" +  /*5*/
                          inhouse-guest-list.firstname           + "|" +  /*6*/
                          inhouse-guest-list.lastname            + "|" +  /*7*/
                          inhouse-guest-list.birthdate           + "|" +  /*8*/
                          inhouse-guest-list.groupname           + "|" +  /*9*/
                          inhouse-guest-list.rmno                + "|" +  /*10*/
                          STRING(inhouse-guest-list.qty)         + "|" +  /*11*/
                          STRING(inhouse-guest-list.arrive)      + "|" +  /*12*/
                          STRING(inhouse-guest-list.depart)      + "|" +  /*13*/
                          inhouse-guest-list.rmcat               + "|" +  /*14*/
                          inhouse-guest-list.ratecode            + "|" +  /*15*/
                          STRING(inhouse-guest-list.zipreis)     + "|" +  /*16*/
                          inhouse-guest-list.kurzbez             + "|" +  /*17*/
                          STRING(inhouse-guest-list.a)           + "|" +  /*18*/
                          STRING(inhouse-guest-list.c)           + "|" +  /*19*/
                          STRING(inhouse-guest-list.co)          + "|" +  /*20*/
                          inhouse-guest-list.pax                 + "|" +  /*21*/
                          inhouse-guest-list.nat                 + "|" +  /*22*/
                          inhouse-guest-list.nation              + "|" +  /*23*/
                          inhouse-guest-list.argt                + "|" +  /*24*/
                          inhouse-guest-list.company             + "|" +  /*25*/
                          inhouse-guest-list.flight              + "|" +  /*26*/
                          inhouse-guest-list.etd                 + "|" +  /*27*/
                          STRING(inhouse-guest-list.paym)        + "|" +  /*28*/
                          inhouse-guest-list.segm                + "|" +  /*29*/
                          inhouse-guest-list.telefon             + "|" +  /*30*/
                          inhouse-guest-list.mobil-tel           + "|" +  /*31*/
                          STRING(inhouse-guest-list.created)     + "|" +  /*32*/
                          inhouse-guest-list.createID            + "|" +  /*33*/
                          inhouse-guest-list.ci-time             + "|" +  /*34*/
                          inhouse-guest-list.curr                + "|" +  /*35*/
                          STRING(inhouse-guest-list.inhousedate) + "|" +  /*36*/
                          inhouse-guest-list.sob                 + "|" +  /*37*/
                          STRING(inhouse-guest-list.gastnr)      + "|" +  /*38*/
                          STRING(inhouse-guest-list.lodging)     + "|" +  /*39*/
                          STRING(inhouse-guest-list.breakfast)   + "|" +  /*40*/
                          STRING(inhouse-guest-list.lunch)       + "|" +  /*41*/
                          STRING(inhouse-guest-list.dinner)      + "|" +  /*42*/
                          STRING(inhouse-guest-list.otherev)     + "|" +  /*43*/
                          STRING(inhouse-guest-list.rechnr)      + "|" +  /*44*/
                          inhouse-guest-list.memberno            + "|" +  /*45*/
                          inhouse-guest-list.membertype          + "|" +  /*46*/
                          inhouse-guest-list.email               + "|" +  /*47*/
                          inhouse-guest-list.localreg            + "|" +  /*48*/
                          inhouse-guest-list.c-zipreis           + "|" +  /*49*/
                          inhouse-guest-list.c-lodging           + "|" +  /*50*/
                          inhouse-guest-list.c-breakfast         + "|" +  /*51*/
                          inhouse-guest-list.c-lunch             + "|" +  /*52*/
                          inhouse-guest-list.c-dinner            + "|" +  /*53*/
                          inhouse-guest-list.c-otherev           + "|" +  /*54*/
                          inhouse-guest-list.c-a                 + "|" +  /*55*/
                          inhouse-guest-list.c-c                 + "|" +  /*56*/
                          inhouse-guest-list.c-co                + "|" +  /*57*/
                          inhouse-guest-list.c-rechnr            + "|" +  /*58*/
                          inhouse-guest-list.c-resnr             + "|" +  /*59*/
                          inhouse-guest-list.night               + "|" +  /*60*/
                          inhouse-guest-list.city                + "|" +  /*61*/
                          inhouse-guest-list.keycard             + "|" +  /*62*/
                          inhouse-guest-list.co-time             + "|" +  /*63*/
                          inhouse-guest-list.pay-art             + "|" +  /*64*/
                          STRING(inhouse-guest-list.etage)       + "|" +  /*65*/
                          inhouse-guest-list.zinr-bez            + "|" +  /*66*/
                          STRING(inhouse-guest-list.flag-guest)           /*67*/
            queasy.number1 = counter.
    FIND NEXT inhouse-guest-list NO-ERROR.
END.

FIND FIRST bqueasy WHERE bqueasy.KEY = 285
    AND bqueasy.char1 = "Inhouse List"
    AND bqueasy.number2 = INT(idFlag) NO-LOCK NO-ERROR.
IF AVAILABLE bqueasy THEN DO:
    FIND CURRENT bqueasy EXCLUSIVE-LOCK.
    ASSIGN bqueasy.number1 = 0.
    FIND CURRENT bqueasy NO-LOCK.
    RELEASE bqueasy.
END.


PROCEDURE decode-string: 
DEFINE INPUT PARAMETER in-str   AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE VARIABLE s   AS CHAR. 
DEFINE VARIABLE j   AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
  s = in-str. 
  j = ASC(SUBSTR(s, 1, 1)) - 70. 
  len = LENGTH(in-str) - 1. 
  s = SUBSTR(in-str, 2, len). 
  DO len = 1 TO LENGTH(s): 
    out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
  END. 
END. 

PROCEDURE add-html:
    DEFINE INPUT  PARAMETER pcString  AS CHARACTER   NO-UNDO.
    DEFINE OUTPUT PARAMETER pcCleaned AS CHARACTER   NO-UNDO.

    DEFINE VARIABLE iHtmlTagBegins AS INTEGER     NO-UNDO.
    DEFINE VARIABLE iHtmlTagEnds   AS INTEGER     NO-UNDO.
    DEFINE VARIABLE lHtmlTagActive AS LOGICAL     NO-UNDO.

    DEFINE VARIABLE i AS INTEGER     NO-UNDO.

    DO i = 1 TO LENGTH(pcString):
        IF lHtmlTagActive = FALSE AND SUBSTRING(pcString, i, 1) = ">" THEN DO:
            iHtmlTagBegins = i.
            lHtmlTagActive = TRUE.
        END.

        IF lHtmlTagActive AND SUBSTRING(pcString, i, 1) = "<" THEN DO:
            iHtmlTagEnds = i.
            lHtmlTagActive = FALSE.

            SUBSTRING(pcString, i,1) = " " + SUBSTRING(pcString, i,1).
       END.
    END.
    pcCleaned = pcString.
END PROCEDURE.

PROCEDURE clean-html:
    DEFINE INPUT  PARAMETER pcString  AS CHARACTER   NO-UNDO.
    DEFINE OUTPUT PARAMETER pcCleaned AS CHARACTER   NO-UNDO.

    DEFINE VARIABLE iHtmlTagBegins AS INTEGER     NO-UNDO.
    DEFINE VARIABLE iHtmlTagEnds   AS INTEGER     NO-UNDO.
    DEFINE VARIABLE lHtmlTagActive AS LOGICAL     NO-UNDO.

    DEFINE VARIABLE i AS INTEGER     NO-UNDO.

    DO i = 1 TO LENGTH(pcString):
        IF lHtmlTagActive = FALSE AND SUBSTRING(pcString, i, 1) = "<" THEN DO:
            iHtmlTagBegins = i.
            lHtmlTagActive = TRUE.
        END.

        IF lHtmlTagActive AND SUBSTRING(pcString, i, 1) = ">" THEN DO:
            iHtmlTagEnds = i.
            lHtmlTagActive = FALSE.

            SUBSTRING(pcString, iHtmlTagBegins, iHtmlTagEnds - iHtmlTagBegins + 1) = FILL("|", iHtmlTagEnds - iHtmlTagBegins).
        END.
    END.

    pcCleaned = REPLACE(pcString, "|", "").

END PROCEDURE.
