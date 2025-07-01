/*FT 090514 fix-cost split reservasi*/

DEF TEMP-TABLE rline-list       LIKE res-line
  FIELD res-char                AS CHAR FORMAT "x(1)" INITIAL " "
  FIELD rsvname                 LIKE reservation.NAME
  FIELD kurzbez                 LIKE zimkateg.kurzbez
  FIELD status-str              AS CHAR FORMAT "x(10)".

DEFINE TEMP-TABLE reslin-list  LIKE res-line. 
DEFINE TEMP-TABLE curr-resline LIKE res-line.
DEFINE TEMP-TABLE t-history    LIKE history.

DEFINE TEMP-TABLE currency-list
    FIELD wabkurz   AS CHAR.

DEFINE TEMP-TABLE Res-Dynarate
  FIELD date1  AS DATE
  FIELD date2  AS DATE
  FIELD rate   AS DECIMAL
  FIELD rmCat  AS CHAR
  FIELD argt   AS CHAR
  FIELD prcode AS CHAR      /* current date static ratecode */
  FIELD rCode  AS CHAR      /* original dynamic ratecode    */
  FIELD markNo AS INTEGER
  FIELD setup  AS INTEGER
  FIELD adult  AS INTEGER
  FIELD child  AS INTEGER
  INDEX date1_ix date1
.

DEFINE TEMP-TABLE reschanged-list
  FIELD reslinnr     AS INTEGER.

DEF TEMP-TABLE f-resline
    FIELD guestname     AS CHAR
    FIELD curr-segm     AS CHAR
    FIELD curr-source   AS CHAR
    FIELD curr-arg      AS CHAR
    FIELD c-purpose     AS CHAR
    FIELD contcode      AS CHAR
    FIELD origcontcode  AS CHAR
    FIELD tip-code      AS CHAR
    FIELD voucher       AS CHAR
    FIELD instruct-str  AS CHAR
    FIELD arrday        AS CHAR
    FIELD depday        AS CHAR
    FIELD flight1       AS CHAR
    FIELD flight2       AS CHAR
    FIELD eta           AS CHAR
    FIELD etd           AS CHAR
    FIELD allot-str     AS CHAR
    FIELD allot-tooltip AS CHAR
    FIELD rate-zikat    AS CHAR
    FIELD zikatstr      AS CHAR
    FIELD currency      AS CHAR
    FIELD c-setup       AS CHAR
    FIELD memo-zinr     AS CHAR
    FIELD billname      AS CHAR
    FIELD billadress    AS CHAR
    FIELD billcity      AS CHAR
    FIELD billland      AS CHAR
    FIELD name-editor   AS CHAR
    FIELD hist-comment  AS CHAR
    FIELD main-resname  AS CHAR
    FIELD prog-str      AS CHAR
    FIELD rsv-tooltip   AS CHAR
    FIELD rate-tooltip  AS CHAR
    FIELD rline-bemerk  AS CHAR
    FIELD res-bemerk    AS CHAR
    FIELD child-age     AS CHAR
    FIELD combo-code    AS CHAR

    FIELD reslinnr      AS INTEGER
    FIELD bill-instruct AS INTEGER
    FIELD kontignr      AS INTEGER
    FIELD zimmeranz     AS INTEGER INIT 1
    FIELD comchild      AS INTEGER
    FIELD price-decimal AS INTEGER
    FIELD res-status    AS INTEGER
    FIELD karteityp     AS INTEGER
    FIELD guestnr       AS INTEGER
    FIELD tot-qty       AS INTEGER
    FIELD zahlungsart   AS INTEGER
    FIELD marknr        AS INTEGER
    FIELD i-purpose     AS INTEGER
    FIELD local-nr      AS INTEGER
    FIELD foreign-nr    AS INTEGER
    FIELD l-night       AS INTEGER
    FIELD six-pm        AS INTEGER

    FIELD accompany-gastnr  AS INTEGER
    FIELD accompany-gastnr2 AS INTEGER
    FIELD accompany-gastnr3 AS INTEGER

    FIELD ci-date       AS DATE
    FIELD billdate      AS DATE
    FIELD bookdate      AS DATE INIT ?
    FIELD l-ankunft     AS DATE INIT ?
    FIELD l-abreise     AS DATE INIT ?

    FIELD earlyci       AS LOGICAL
    FIELD master-exist  AS LOGICAL
    FIELD master-active AS LOGICAL
    FIELD pickup-flag   AS LOGICAL
    FIELD drop-flag     AS LOGICAL
    FIELD enable-frate  AS LOGICAL
    FIELD ebdisc-flag   AS LOGICAL
    FIELD kbdisc-flag   AS LOGICAL
    FIELD restricted    AS LOGICAL
    FIELD enable-ebdisc AS LOGICAL
    FIELD enable-kbdisc AS LOGICAL
    FIELD new-contrate  AS LOGICAL
    FIELD foreign-rate  AS LOGICAL
    FIELD gentable      AS LOGICAL
    FIELD offmarket     AS LOGICAL
    FIELD grpflag       AS LOGICAL
    FIELD sharer        AS LOGICAL
    FIELD fixed-rate    AS LOGICAL
    FIELD enable-disc   AS LOGICAL
    FIELD oral-flag     AS LOGICAL
    FIELD param472      AS LOGICAL INIT NO
    FIELD wci-flag      AS CHAR
    FIELD gdpr-flag     AS CHAR
    /*gerald Req Tauzia 14/12/20*/
    FIELD mark-flag     AS CHAR
    FIELD news-flag     AS CHAR
    .

DEFINE TEMP-TABLE nation-list
    FIELD nr        AS INTEGER
    FIELD kurzbez   AS CHAR
    FIELD bezeich   AS CHAR FORMAT "x(32)".


DEF INPUT PARAMETER pvILanguage     AS INTEGER NO-UNDO.
DEF INPUT-OUTPUT PARAMETER res-mode AS CHAR    NO-UNDO.
DEF INPUT PARAMETER session-date    AS CHAR    NO-UNDO.
DEF INPUT PARAMETER user-init       AS CHAR    NO-UNDO.
DEF INPUT PARAMETER inp-gastnr      AS INTEGER NO-UNDO.
DEF INPUT PARAMETER inp-resnr       AS INTEGER NO-UNDO.
DEF INPUT PARAMETER inp-reslinnr    AS INTEGER NO-UNDO. 
DEF INPUT PARAMETER rate-readonly   AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER qci-zinr        AS CHAR    NO-UNDO.

DEF INPUT PARAMETER TABLE FOR res-Dynarate.

DEF OUTPUT PARAMETER msg-str    AS CHAR INIT ""     NO-UNDO.
DEF OUTPUT PARAMETER error-flag AS LOGICAL INIT NO  NO-UNDO.

DEF OUTPUT PARAMETER record-use AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER init-time AS INT.
DEF OUTPUT PARAMETER init-date AS DATE.
DEF OUTPUT PARAMETER avail-gdpr AS LOGICAL.

/*gerald Req Tauzia 14/12/20*/
DEF OUTPUT PARAMETER avail-mark AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER avail-news AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER save-gdpr  AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER curr-date  AS DATE    NO-UNDO.
DEF OUTPUT PARAMETER serv-date  AS LOGICAL NO-UNDO INIT NO.

DEF OUTPUT PARAMETER TABLE FOR f-resline.
DEF OUTPUT PARAMETER TABLE FOR curr-resline.
DEF OUTPUT PARAMETER TABLE FOR reslin-list.
DEF OUTPUT PARAMETER TABLE FOR reschanged-list.
DEF OUTPUT PARAMETER TABLE FOR t-history.
DEF OUTPUT PARAMETER TABLE FOR rline-list.

DEFINE VARIABLE weekdays AS CHAR EXTENT 8  FORMAT "x(3)" 
  INITIAL ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].

DEFINE VARIABLE i          AS INTEGER NO-UNDO.
DEFINE VARIABLE str        AS CHAR    NO-UNDO.
DEFINE VARIABLE loopi      AS INTEGER NO-UNDO.
DEFINE VARIABLE loopj      AS INTEGER NO-UNDO.
DEFINE VARIABLE str1       AS CHAR    NO-UNDO.
DEFINE VARIABLE foreign-nr          AS INTEGER. 
DEF VAR tokcounter AS INTEGER NO-UNDO.
DEF VAR ifTask     AS CHAR    NO-UNDO.
DEF VAR mesToken   AS CHAR    NO-UNDO.
DEF VAR mesValue   AS CHAR    NO-UNDO.
DEF VAR rCode      AS CHAR    NO-UNDO INIT "".
DEF VAR prevCode   AS CHAR    NO-UNDO INIT "".
DEF VAR do-it      AS LOGICAL NO-UNDO.
DEF VAR do-it1     AS LOGICAL NO-UNDO.

DEFINE BUFFER resline    FOR res-line.
DEFINE BUFFER resbuff    FOR res-line.
DEFINE BUFFER zimkateg1  FOR zimkateg.
DEFINE BUFFER rbuff      FOR ratecode.
DEFINE BUFFER qci-zimmer FOR zimmer.
DEFINE BUFFER bresline   FOR res-line.
DEFINE BUFFER bguest     FOR guest.

DEFINE VARIABLE flag-ok      AS LOGICAL NO-UNDO.
DEFINE VARIABLE dayuse-flag  AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE split-modify AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE logic-p1109  AS LOGICAL NO-UNDO.
DEFINE VARIABLE priscilla-active AS LOGICAL NO-UNDO INIT YES.

DEFINE VARIABLE loopk     AS INTEGER NO-UNDO.
DEFINE VARIABLE resbemerk AS CHAR    NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mk-resline". 

/* SY 11 AUG 2015: used in mk-reslineUI, proc chg-reservation */
IF res-mode = "split+modify" THEN
ASSIGN
    res-mode     = "modify"
    split-modify = YES
.

IF NUM-ENTRIES(res-mode, CHR(2)) GT 1 THEN
DO:
  IF ENTRY(2, res-mode, CHR(2)) = "DU"  THEN dayuse-flag = YES.
  res-mode = ENTRY(1, res-mode, CHR(2)).
END.

FIND FIRST htparam WHERE paramnr = 346 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeichnung NE "not used" THEN DO:
    avail-gdpr = htparam.flogical.
    FIND FIRST htparam WHERE paramnr = 466 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN ASSIGN save-gdpr = htparam.finteger.
END.


IF avail-gdpr THEN DO:
    FOR EACH nation WHERE nation.natcode = 0 NO-LOCK,
        FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe
            AND queasy.char1 MATCHES "*europe*" NO-LOCK BY nation.kurzbez:
        CREATE nation-list.
        ASSIGN nation-list.nr      = nation.nationnr
               nation-list.kurzbez = nation.kurzbez
               nation-list.bezeich = ENTRY(1, nation.bezeich, ";").           
    END.
END.

/*gerald Req Tauzia 14/12/20*/
FIND FIRST htparam WHERE paramnr = 477 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeichnung NE "not used" THEN 
DO:
    avail-mark = htparam.flogical.
    avail-news = htparam.flogical.
END.
/*end gerald*/

RUN check-timebl.p(1, inp-resnr, inp-reslinnr, "res-line", ?, ?, OUTPUT flag-ok,
                   OUTPUT init-time, OUTPUT init-date).

IF NOT flag-ok THEN
DO:
    error-flag = YES.
    record-use = YES.
    RETURN NO-APPLY.
END.

/************************* FUNCTION ****************************************/
FUNCTION get-rackrate RETURNS DECIMAL 
    (INPUT erwachs  AS INTEGER, 
     INPUT kind1    AS INTEGER, 
     INPUT kind2    AS INTEGER). 
  DEF VAR rate      AS DECIMAL INITIAL 0. 
  IF erwachs GE 1 AND erwachs LE 4 THEN rate = rate + katpreis.perspreis[erwachs]. 
  rate = rate + kind1 * katpreis.kindpreis[1] + kind2 * katpreis.kindpreis[2]. 
  RETURN rate. 
END FUNCTION. 

  IF qci-zinr NE "" THEN
    FIND FIRST qci-zimmer WHERE qci-zimmer.zinr = qci-zinr NO-LOCK.

  CREATE f-resline.

  IF res-mode = "modify" OR res-mode = "inhouse" THEN 
  DO:  
    FIND FIRST resbuff WHERE resbuff.resnr = inp-resnr 
      AND resbuff.reslinnr = inp-reslinnr EXCLUSIVE-LOCK
      NO-WAIT NO-ERROR.
    IF NOT AVAILABLE resbuff THEN
    DO:
      msg-str = translateExtended ("Reservation is being modified by other user.",lvCAREA,""). 
      error-flag = YES.
      RETURN. 
    END.
    IF res-mode = "modify" AND resbuff.active-flag = 1 THEN 
    DO: 
      msg-str = translateExtended ("Guest already checked-in.",lvCAREA,""). 
      error-flag = YES.
      RETURN. 
    END.
  END.
    
  RUN htplogic.p (550, OUTPUT f-resline.new-contrate).
  RUN htpint.p   (491, OUTPUT f-resline.price-decimal). 
  RUN htpdate.p  (87,  OUTPUT curr-date).
  RUN htpdate.p  (110, OUTPUT f-resline.billdate).
  RUN htplogic.p (143, OUTPUT f-resline.foreign-rate).
  RUN htpint.p   (478, OUTPUT f-resline.res-status).
  RUN htplogic.p (938, OUTPUT f-resline.oral-flag).
  RUN htpint.p   (297, OUTPUT f-resline.six-pm).
  
  /*ITA 22/11/21 - Request HGU
  RUN htplogic.p(1355, OUTPUT serv-date).
  IF serv-date THEN 
      ASSIGN f-resline.ci-date  = TODAY
             f-resline.billdate = TODAY.
  ELSE ASSIGN f-resline.ci-date  = curr-date.*/

  FIND FIRST htparam WHERE htparam.paramnr = 1355 NO-LOCK.
  IF htparam.flogical = YES AND htparam.bezeichnung NE "not used" THEN 
      ASSIGN f-resline.ci-date  = TODAY
             f-resline.billdate = TODAY.
  ELSE ASSIGN f-resline.ci-date  = curr-date.

 
  FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.

  FIND FIRST master WHERE master.resnr = inp-resnr NO-LOCK NO-ERROR.
  f-resline.master-exist = AVAILABLE master. 
 
  FIND FIRST guest WHERE guest.gastnr = inp-gastnr NO-LOCK.
  ASSIGN
    f-resline.main-resname = guest.NAME. 
    f-resline.karteityp    = guest.karteityp
  .

  FIND FIRST reslin-queasy WHERE reslin-queasy.key = "rate-prog"
    AND reslin-queasy.char1       EQ ""
    AND reslin-queasy.reslinnr    EQ 1 
    AND reslin-queasy.number1     EQ inp-resnr
    AND reslin-queasy.number2     EQ 0 NO-LOCK NO-ERROR.
  IF AVAILABLE reslin-queasy THEN 
    f-resline.prog-str = reslin-queasy.char3.
  
  IF res-mode = "earlyci" THEN 
  ASSIGN
    f-resline.earlyci = YES 
    res-mode          = "modify"
  . 

  FIND FIRST htparam WHERE htparam.paramnr = 472 NO-LOCK. 
  IF htparam.paramgr = 99 AND htparam.feldtyp = 4 THEN
  ASSIGN f-resline.param472 = htparam.flogical.

  f-resline.allot-tooltip = 
    translateExtended ("Allotment",lvCAREA,""). 

  IF res-mode = "new" OR res-mode = "qci" THEN 
  DO: 
  DEF VAR new-reslinnr AS INTEGER NO-UNDO INIT 1.
      FOR EACH res-line WHERE res-line.resnr = inp-resnr NO-LOCK
          BY res-line.reslinnr DESCENDING:
          new-reslinnr = res-line.reslinnr + 1.
          LEAVE.
      END.
      f-resline.reslinnr = new-reslinnr. 
  END.
  ELSE IF res-mode = "modify" OR res-mode = "inhouse" THEN 
  DO:  
    FIND FIRST res-line WHERE res-line.resnr = inp-resnr 
      AND res-line.reslinnr = inp-reslinnr NO-LOCK. 
    
    FIND FIRST reservation WHERE reservation.resnr = inp-resnr NO-LOCK.
 
    IF res-line.kontignr GT 0 THEN
    DO:
      FIND FIRST kontline WHERE kontline.kontignr = res-line.kontignr 
        AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
      IF AVAILABLE kontline THEN f-resline.allot-tooltip = 
        translateExtended ("Allotment Code",lvCAREA,""). 
    END.
    ELSE IF res-line.kontignr LT 0 THEN
    DO:
      FIND FIRST kontline WHERE kontline.kontignr = - res-line.kontignr 
        AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
      IF AVAILABLE kontline THEN f-resline.allot-tooltip = 
        translateExtended ("Global Reservation Code",lvCAREA,""). 
    END.

    CREATE curr-resline.
    BUFFER-COPY res-line TO curr-resline.

    FIND FIRST gentable WHERE gentable.KEY = "reservation"
      AND gentable.number1 = inp-resnr 
      AND gentable.number2 = inp-reslinnr NO-LOCK NO-ERROR.
    f-resline.gentable = AVAILABLE gentable.

    FIND FIRST resline WHERE resline.resnr = res-line.resnr
      AND resline.active-flag LE 1 
      AND resline.kontakt-nr = res-line.reslinnr
      AND resline.l-zuordnung[3] = 1 NO-LOCK NO-ERROR.
    IF AVAILABLE resline THEN 
      ASSIGN f-resline.accompany-gastnr = resline.gastnrmember.
    
    IF AVAILABLE resline THEN
    FIND NEXT resline WHERE resline.resnr = res-line.resnr
      AND resline.active-flag LE 1 
      AND resline.kontakt-nr = res-line.reslinnr
      AND resline.l-zuordnung[3] = 1 NO-LOCK NO-ERROR.
    IF AVAILABLE resline THEN 
      ASSIGN f-resline.accompany-gastnr2 = resline.gastnrmember.

    IF AVAILABLE resline THEN
    FIND NEXT resline WHERE resline.resnr = res-line.resnr
      AND resline.active-flag LE 1 
      AND resline.kontakt-nr = res-line.reslinnr
      AND resline.l-zuordnung[3] = 1 NO-LOCK NO-ERROR.
    IF AVAILABLE resline THEN 
      ASSIGN f-resline.accompany-gastnr3 = resline.gastnrmember.

    IF session-date = "dmy" THEN
      ASSIGN 
        f-resline.rsv-tooltip = SUBSTR(res-line.reserve-char,7,2) + "/"
          + SUBSTR(res-line.reserve-char,4,2) + "/"
          + SUBSTR(res-line.reserve-char,1,2) + " "
          + SUBSTR(res-line.reserve-char,9,5) + " "
          + SUBSTR(res-line.reserve-char,14).
    ELSE IF SESSION:DATE-FORMAT = "mdy" THEN
      ASSIGN 
        f-resline.rsv-tooltip = SUBSTR(res-line.reserve-char,4,2) + "/"
          + SUBSTR(res-line.reserve-char,7,2) + "/"
          + SUBSTR(res-line.reserve-char,1,2) + " "
          + SUBSTR(res-line.reserve-char,9,5) + " "
          + SUBSTR(res-line.reserve-char,14).
    ELSE 
      ASSIGN 
        f-resline.rsv-tooltip = SUBSTR(res-line.reserve-char,1,8) + " "
          + SUBSTR(res-line.reserve-char,9,5) + " "
          + SUBSTR(res-line.reserve-char,14).
    
    IF res-mode = "modify" 
        AND (res-line.resstatus LE 2 OR res-line.resstatus = 5)
        AND res-line.zinr NE "" THEN 
    DO: 
      FIND FIRST outorder WHERE outorder.zinr = res-line.zinr 
        AND outorder.betriebsnr = res-line.resnr NO-LOCK NO-ERROR. 
      f-resline.offmarket = AVAILABLE outorder.
    END. 

    IF res-line.code NE "" AND res-line.CODE NE "0" THEN 
    DO: 
      f-resline.bill-instruct = INTEGER(res-line.code). 
      FIND FIRST queasy WHERE queasy.key EQ 9 AND queasy.number1 EQ f-resline.bill-instruct NO-LOCK NO-ERROR. /* Malik Serverless bill-instruct -> f-resline.bill-instruct */
      IF AVAILABLE queasy THEN f-resline.instruct-str = queasy.char1. 
    END. 
 
    ASSIGN
      f-resline.guestnr      = res-line.gastnrpay
      f-resline.reslinnr     = inp-reslinnr
      f-resline.grpflag      = res-line.grpflag
      f-resline.rline-bemerk = res-line.bemerk
      f-resline.res-bemerk   = reservation.bemerk
      f-resline.kontignr     = res-line.kontignr 
      f-resline.zimmeranz    = res-line.zimmeranz 
      f-resline.sharer       = (res-line.resstatus EQ 11) OR (res-line.resstatus EQ 13)
    . 

    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK. 
    IF AVAILABLE zimkateg THEN ASSIGN f-resline.zikatstr = zimkateg.kurzbez.
        
  END. 
  
  ELSE IF res-mode = "insert" OR res-mode = "split" THEN 
  DO: 
    ASSIGN
      f-resline.reslinnr = 1 
      f-resline.tot-qty  = 0
    . 
    FOR EACH res-line WHERE res-line.resnr = inp-resnr NO-LOCK: 
      IF f-resline.guestnr = 0 THEN 
        f-resline.guestnr = res-line.gastnrpay. 
      IF res-line.reslinnr GT f-resline.reslinnr THEN 
        f-resline.reslinnr = res-line.reslinnr. 
      f-resline.grpflag = res-line.grpflag. 
      f-resline.tot-qty = f-resline.tot-qty + res-line.zimmeranz. 
    END. 
    f-resline.reslinnr = f-resline.reslinnr + 1. 
  END. 
  
  
  RUN htplogic.p(1109, OUTPUT logic-p1109).
  IF f-resline.res-bemerk NE ? AND f-resline.res-bemerk NE "" THEN
    ASSIGN f-resline.res-bemerk = f-resline.res-bemerk 
         + CHR(2) + STRING(INTEGER(logic-p1109)).
  ELSE 
      ASSIGN f-resline.res-bemerk = STRING(INTEGER(logic-p1109)).
  
   /*ASSIGN  
   f-resline.res-bemerk = REPLACE(f-resline.res-bemerk,CHR(10),"").
    f-resline.res-bemerk = REPLACE(f-resline.res-bemerk,CHR(13),"").
    f-resline.res-bemerk = REPLACE(f-resline.res-bemerk,"~n","").
    f-resline.res-bemerk = REPLACE(f-resline.res-bemerk,"\n","").
    f-resline.res-bemerk = REPLACE(f-resline.res-bemerk,"~r","").
    f-resline.res-bemerk = REPLACE(f-resline.res-bemerk,"~r~n","").
    /*f-resline.res-bemerk = REPLACE(f-resline.res-bemerk,CHR(10) + CHR(13),"")*/.*/
    
    ASSIGN resbemerk = "".
    IF f-resline.res-bemerk NE ? AND f-resline.res-bemerk NE "" THEN  /*FT serverless*/
    DO:
        DO loopk = 1 TO LENGTH(f-resline.res-bemerk):
            if ASC(SUBSTR(f-resline.res-bemerk, loopk, 1)) = 0 OR ASC(SUBSTR(f-resline.res-bemerk, loopk, 1)) GT 255 THEN .
            ELSE resbemerk = resbemerk + SUBSTR(f-resline.res-bemerk, loopk, 1). 
        END.
        ASSIGN f-resline.res-bemerk = resbemerk.
    
        IF LENGTH(f-resline.res-bemerk) LT 3 THEN f-resline.res-bemerk = REPLACE(f-resline.res-bemerk,CHR(32),"").
        IF LENGTH(f-resline.res-bemerk) EQ ? THEN f-resline.res-bemerk = "". 
    END.
    

  /*ASSIGN  
    f-resline.rline-bemerk = REPLACE(f-resline.rline-bemerk,CHR(10),"").
    f-resline.rline-bemerk = REPLACE(f-resline.rline-bemerk,CHR(13),"").
    f-resline.rline-bemerk = REPLACE(f-resline.rline-bemerk,"~n","").
    f-resline.rline-bemerk = REPLACE(f-resline.rline-bemerk,"\n","").
    f-resline.rline-bemerk = REPLACE(f-resline.rline-bemerk,"~r","").
    f-resline.rline-bemerk = REPLACE(f-resline.rline-bemerk,"~r~n","").
    /*f-resline.rline-bemerk = REPLACE(f-resline.rline-bemerk,CHR(10) + CHR(13),"")*/.*/
    
    ASSIGN resbemerk = "".
    IF f-resline.rline-bemerk NE ? AND f-resline.rline-bemerk NE "" THEN  /*FT serverless*/
    DO:
        DO loopk = 1 TO LENGTH(f-resline.rline-bemerk):
            if ASC(SUBSTR(f-resline.rline-bemerk, loopk, 1)) = 0 OR ASC(SUBSTR(f-resline.rline-bemerk, loopk, 1)) GT 255 THEN.
            ELSE resbemerk = resbemerk + SUBSTR(f-resline.rline-bemerk, loopk, 1). 
        END.
        ASSIGN f-resline.rline-bemerk = resbemerk.
    
        IF LENGTH(f-resline.rline-bemerk) LT 3 THEN f-resline.rline-bemerk = REPLACE(f-resline.rline-bemerk,CHR(32),"").
        IF LENGTH(f-resline.rline-bemerk) EQ ? THEN f-resline.rline-bemerk = "".
    END.
    

  IF res-mode = "split" THEN RUN split-resline. 

  IF res-mode = "new" OR res-mode = "insert" OR res-mode = "qci" THEN 
  DO: 
    ASSIGN
      f-resline.bill-instruct = 0 
      f-resline.instruct-str = ""
    . 

/*
    CREATE reschanged-list. 
    ASSIGN reschanged-list.reslinnr = inp-reslinnr. 
*/
    FIND FIRST guest WHERE guest.gastnr = inp-gastnr NO-LOCK. 
    CREATE res-line. 
    ASSIGN
      f-resline.guestname   = guest.NAME
      f-resline.guestnr     = guest.gastnr
      res-line.resnr        = inp-resnr
      res-line.reslinnr     = f-resline.reslinnr 
      res-line.gastnr       = inp-gastnr
      res-line.gastnrpay    = inp-gastnr 
      res-line.gastnrmember = inp-gastnr 
      res-line.ankunft      = f-resline.ci-date 
      res-line.abreise      = res-line.ankunft + 1 
      res-line.anztage      = 1
      res-line.zimmeranz    = 1 
      res-line.name         = guest.NAME
      res-line.resname      = f-resline.main-resname 
      res-line.erwachs      = 1
      res-line.gratis       = 0 
      res-line.grpflag      = f-resline.grpflag
/* 08/16/00 the following two command lines are added TO avoid appearing 
   OF the NEW created res-line records IN the arl-list.  */ 
      res-line.active-flag = 2
      res-line.resstatus = 12
    . 
    
    FIND FIRST htparam WHERE htparam.paramnr = 262 NO-LOCK.
    IF htparam.finteger NE 0 THEN 
      ASSIGN res-line.erwachs = htparam.finteger.

    IF res-mode = "insert" THEN
    DO:
      FIND FIRST resline WHERE resline.resnr = inp-resnr
        AND resline.active-flag LE 1 AND resline.resstatus NE 12
        AND resline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
      IF AVAILABLE resline THEN
      DO:
        IF resline.active-flag = 0 THEN
        ASSIGN
          res-line.ankunft = resline.ankunft
          res-line.abreise = resline.abreise
          res-line.anztage = res-line.abreise - res-line.ankunft
        .
        ELSE IF resline.active-flag = 1 THEN
        ASSIGN
          res-line.abreise = resline.abreise
          res-line.anztage = res-line.abreise - res-line.ankunft
        .
      END.
    END.


   
    FIND FIRST htparam WHERE paramnr = 150 NO-LOCK. 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = htparam.finteger NO-LOCK NO-ERROR. 
    IF AVAILABLE zimkateg THEN 
    ASSIGN 
      f-resline.zikatstr = zimkateg.kurzbez
      res-line.zikatnr   = zimkateg.zikatnr
    . 
 
    FIND FIRST htparam WHERE paramnr = 151 NO-LOCK. 
    FIND FIRST arrangement WHERE arrangement.arrangement = htparam.fchar 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE arrangement THEN 
    ASSIGN 
      res-line.arrangement = arrangement.arrangement.
    ASSIGN f-resline.curr-arg = res-line.arrangement. 
  END.
 
  CREATE reslin-list.
  ASSIGN
    reslin-list.reserve-dec = 0
    reslin-list.resnr = inp-resnr
  . 

  IF res-mode NE "split" THEN 
  DO: 
    FIND FIRST guest WHERE guest.gastnr = f-resline.guestnr NO-LOCK. 
    ASSIGN
      f-resline.billname   = guest.name + ", " + guest.vorname1 
                           + guest.anredefirma 
                           + " " + guest.anrede1 
      f-resline.billadress = guest.adresse1
      f-resline.billcity   = guest.wohnort + " " + guest.plz
    . 


    FIND FIRST nation WHERE nation.kurzbez = guest.land NO-LOCK NO-ERROR. 
    IF AVAILABLE nation THEN 
      ASSIGN f-resline.billland = nation.bezeich. 
    
    ASSIGN
      f-resline.name-editor   = f-resline.billname + CHR(10) + CHR(10) 
        + f-resline.billadress + CHR(10) 
        + f-resline.billcity + CHR(10) + CHR(10) 
        + f-resline.billland
      f-resline.zahlungsart   = guest.zahlungsart
    .

    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
    f-resline.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1. 
    FIND FIRST guest WHERE guest.gastnr = inp-gastnr NO-LOCK. 
    
    IF AVAILABLE qci-zimmer THEN FIND FIRST zimkateg WHERE 
        zimkateg.zikatnr = qci-zimmer.zikatnr NO-LOCK.
    ELSE FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
    

    IF AVAILABLE zimkateg THEN 
      ASSIGN f-resline.zikatstr = zimkateg.kurzbez.
    
    ASSIGN f-resline.curr-arg = res-line.arrangement. 
    BUFFER-COPY res-line TO reslin-list.

    IF reslin-list.bemerk NE ? AND reslin-list.bemerk NE "" THEN  /*FT serverless*/
    DO:
        ASSIGN  
            reslin-list.bemerk = REPLACE(reslin-list.bemerk,CHR(10),"").
            reslin-list.bemerk = REPLACE(reslin-list.bemerk,CHR(13),"").
            reslin-list.bemerk = REPLACE(reslin-list.bemerk,"~n","").
            reslin-list.bemerk = REPLACE(reslin-list.bemerk,"\n","").
            reslin-list.bemerk = REPLACE(reslin-list.bemerk,"~r","").
            reslin-list.bemerk = REPLACE(reslin-list.bemerk,"~r~n","").
            reslin-list.bemerk = REPLACE(reslin-list.bemerk,CHR(10) + CHR(13),"").
        
     
        ASSIGN resbemerk = " ".
        DO loopk = 1 TO LENGTH(reslin-list.bemerk):
            if ASC(SUBSTR(reslin-list.bemerk, loopk, 1)) = 0 OR ASC(SUBSTR(reslin-list.bemerk, loopk, 1)) GT 255 THEN .
            ELSE resbemerk = resbemerk + SUBSTR(reslin-list.bemerk, loopk, 1). 
        END.
        ASSIGN reslin-list.bemerk = resbemerk.
    
        IF LENGTH(reslin-list.bemerk) LT 3 THEN reslin-list.bemerk = REPLACE(reslin-list.bemerk,CHR(32),"").
        IF LENGTH(reslin-list.bemerk) EQ ? THEN reslin-list.bemerk = "". 
    END.
    

    IF AVAILABLE qci-zimmer THEN
    ASSIGN
        reslin-list.setup = qci-zimmer.setup
        reslin-list.zinr  = qci-zimmer.zinr
    .

    ASSIGN
      f-resline.arrday      = weekdays[WEEKDAY(reslin-list.ankunft)]
      f-resline.depday      = weekdays[WEEKDAY(reslin-list.abreise)]
      f-resline.comchild    = reslin-list.l-zuordnung[4]
      f-resline.pickup-flag = reslin-list.zimmer-wunsch MATCHES ("*pickup*")
      f-resline.drop-flag   = reslin-list.zimmer-wunsch MATCHES ("*drop-passanger*")
      f-resline.marknr      = reslin-list.reserve-int.   
    . 
 
    IF reslin-list.l-zuordnung[1] NE 0 THEN 
    DO: 
      FIND FIRST zimkateg1 WHERE zimkateg1.zikatnr = reslin-list.l-zuordnung[1] 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE zimkateg1 THEN 
        f-resline.rate-zikat = zimkateg1.kurzbez.
    END. 

    IF res-mode = "new" OR res-mode = "insert" OR res-mode = "qci" THEN 
    DO: 
      IF f-resline.res-status = 1 THEN reslin-list.resstatus = 3. 
      ELSE IF f-resline.res-status = 2 THEN reslin-list.resstatus = 2. 
      ELSE IF f-resline.res-status = 3 AND f-resline.oral-flag THEN reslin-list.resstatus = 5.
      ELSE reslin-list.resstatus = 1. 
      reslin-list.active-flag  = 0. 
    END. 
    ELSE 
    DO: 
      reslin-list.resstatus = res-line.resstatus. 
      reslin-list.active-flag  = res-line.active-flag. 
    END. 
 
    FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR. 
    FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement 
      NO-LOCK NO-ERROR. 
 
    RUN fill-flightnr. 
/*    RUN check-bedsetup.    */
 
  END. 
 
  IF res-line.memozinr NE ? AND res-line.memozinr NE "" THEN
  DO:
    IF res-line.memozinr MATCHES("*;*") THEN 
      ASSIGN f-resline.memo-zinr = ENTRY(2,res-line.memozinr,";").
  END.

  IF f-resline.new-contrate THEN
  ASSIGN
    f-resline.ebdisc-flag = reslin-list.zimmer-wunsch MATCHES("*ebdisc*")
    f-resline.kbdisc-flag = reslin-list.zimmer-wunsch MATCHES("*kbdisc*") 
    f-resline.restricted  = reslin-list.zimmer-wunsch MATCHES ("*restricted*")
  .
  
  DEFINE VARIABLE curr-time AS INTEGER.
  curr-time = TIME.
  /*
/* check IF contract rate exists, fix rate defined */ 
  FOR EACH queasy WHERE queasy.KEY = 2 AND queasy.logi2 NO-LOCK:
    FIND FIRST guest-pr WHERE guest-pr.CODE = queasy.char1
      AND guest-pr.gastnr = inp-gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE guest-pr THEN LEAVE.
  END.
  
  IF NOT AVAILABLE guest-pr THEN*/

  IF f-resline.new-contrate THEN
  DO:
    FOR EACH guest-pr WHERE guest-pr.gastnr = inp-gastnr NO-LOCK USE-INDEX guest-pr_ix,
      FIRST queasy WHERE queasy.KEY = 2 AND queasy.logi2
        AND queasy.char1 = guest-pr.CODE NO-LOCK :

      do-it = YES.
      IF (res-mode = "new" OR res-mode = "insert" 
        OR res-mode = "qci") THEN
      DO:
        IF queasy.date1 NE ? THEN /*FT serverless*/
        DO:
          IF f-resline.ci-date LT queasy.date1 THEN do-it = NO. 
          ELSE IF f-resline.ci-date GT queasy.date2 THEN do-it = NO. 
        END.
      END.
      IF do-it THEN
      DO:
        FIND FIRST ratecode WHERE ratecode.code = guest-pr.code 
          AND f-resline.ci-date LE ratecode.endperiode NO-LOCK NO-ERROR. 
        IF AVAILABLE ratecode THEN 
        DO:    
          f-resline.enable-frate = YES.
          IF (res-mode = "new" OR res-mode = "insert" OR res-mode = "qci") 
            AND reslin-list.reserve-int = 0 AND ratecode.marknr GT 0 THEN
            ASSIGN
              reslin-list.reserve-int = ratecode.marknr
              f-resline.contcode      = ratecode.CODE
              f-resline.origcontcode  = ratecode.CODE
            .
        END.
        FIND FIRST ratecode WHERE ratecode.code = guest-pr.code 
          AND ratecode.char1[1] NE "" NO-LOCK NO-ERROR. 
        IF AVAILABLE ratecode THEN f-resline.enable-ebdisc = YES.
        FIND FIRST ratecode WHERE ratecode.code = guest-pr.code 
          AND ratecode.char1[2] NE "" NO-LOCK NO-ERROR. 
        IF AVAILABLE ratecode THEN f-resline.enable-kbdisc = YES.
      END.
    END.  
  END.
  ELSE
  DO:
    FIND FIRST guest-pr WHERE guest-pr.gastnr = inp-gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE guest-pr THEN
    DO:
      FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.logi2
        AND queasy.char1 = guest-pr.CODE NO-LOCK NO-ERROR.
      IF AVAILABLE queasy THEN 
      DO:
        FIND FIRST pricecod WHERE pricecod.code = guest-pr.code 
          AND f-resline.ci-date LE pricecod.endperiode NO-LOCK NO-ERROR. 
        IF AVAILABLE pricecod THEN f-resline.enable-frate = YES.
      END.
    END.
  END.

  /*
  FIND FIRST guest-pr WHERE guest-pr.gastnr = inp-gastnr NO-LOCK NO-ERROR. 
  IF AVAILABLE guest-pr THEN 
  DO:
    FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.logi2
          AND queasy.char1 = guest-pr.CODE NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN DO:
        IF f-resline.new-contrate THEN
        DO:
            DO WHILE AVAILABLE guest-pr:
              FIND FIRST queasy WHERE queasy.KEY = 2 
                AND queasy.char1 = guest-pr.CODE NO-LOCK NO-ERROR.
              IF AVAILABLE queasy THEN
              DO:
                do-it = YES.
                IF (res-mode = "new" OR res-mode = "insert" 
                   OR res-mode = "qci") THEN
                DO:
                  IF queasy.date1 NE ? THEN /*FT serverless*/
                  DO:
                    IF f-resline.ci-date LT queasy.date1 THEN do-it = NO. 
                    ELSE IF f-resline.ci-date GT queasy.date2 THEN do-it = NO. 
                  END.
                END.
                IF do-it THEN
                DO:
                  FIND FIRST ratecode WHERE ratecode.code = guest-pr.code 
                    AND f-resline.ci-date LE ratecode.endperiode NO-LOCK NO-ERROR. 
                  IF AVAILABLE ratecode THEN 
                  DO:    
                    f-resline.enable-frate = YES.
                    IF (res-mode = "new" OR res-mode = "insert" OR res-mode = "qci") 
                      AND reslin-list.reserve-int = 0 AND ratecode.marknr GT 0 THEN
                    ASSIGN
                      reslin-list.reserve-int = ratecode.marknr
                      f-resline.contcode      = ratecode.CODE
                      f-resline.origcontcode  = ratecode.CODE
                    .
                  END.
                  FIND FIRST ratecode WHERE ratecode.code = guest-pr.code 
                    AND ratecode.char1[1] NE "" NO-LOCK NO-ERROR. 
                  IF AVAILABLE ratecode THEN f-resline.enable-ebdisc = YES.
                  FIND FIRST ratecode WHERE ratecode.code = guest-pr.code 
                    AND ratecode.char1[2] NE "" NO-LOCK NO-ERROR. 
                  IF AVAILABLE ratecode THEN f-resline.enable-kbdisc = YES.
                END.
              END.
              FIND NEXT guest-pr WHERE guest-pr.gastnr = inp-gastnr NO-LOCK NO-ERROR. 
            END.
        END.
        ELSE
        DO:
          FIND FIRST pricecod WHERE pricecod.code = guest-pr.code 
            AND f-resline.ci-date LE pricecod.endperiode NO-LOCK NO-ERROR. 
          IF AVAILABLE pricecod THEN f-resline.enable-frate = YES.
        END.

    END.    
  END.*/
  
  DO i = 1 TO NUM-ENTRIES(reslin-list.zimmer-wunsch,";") - 1:
    str = ENTRY(i, reslin-list.zimmer-wunsch, ";").
    IF SUBSTR(str,1,7) = "voucher" THEN 
      f-resline.voucher = SUBSTR(str,8).
    ELSE IF SUBSTR(str,1,5) = "ChAge"  THEN 
      f-resline.child-age = SUBSTR(str,6).
    ELSE IF SUBSTR(str,1,6) = "$CODE$" THEN 
      f-resline.contcode  = SUBSTR(str,7).
    ELSE IF SUBSTR(str,1,5) = "DATE,"  THEN 
      f-resline.bookdate = DATE(INTEGER(SUBSTR(str,10,2)), 
      INTEGER(SUBSTR(str,12,2)), INTEGER(SUBSTR(str,6,4))) NO-ERROR.
    ELSE IF SUBSTR(str,1,8) = "SEGM_PUR" THEN 
      f-resline.i-purpose = INTEGER(SUBSTR(str,9)).
    ELSE IF str MATCHES "*WCI-req*" THEN DO:  /*ITA 120715*/
        ASSIGN str1 = ENTRY(2, str, "=").
        DO loopi = 1 TO NUM-ENTRIES(str1, ","):
           FIND FIRST queasy WHERE queasy.KEY = 160
              AND queasy.number1 = INT(ENTRY(loopi, str1, ",")) NO-LOCK NO-ERROR.
           IF AVAILABLE queasy THEN DO:
                DO loopj = 1 TO NUM-ENTRIES(queasy.char1, ";") :
                    IF ENTRY(loopj, queasy.char1, ";") MATCHES "*en*" THEN
                    DO:
                        ASSIGN f-resline.wci-flag = ENTRY(2, ENTRY(loopj, queasy.char1, ";"), "=") + ", " + f-resline.wci-flag.
                        LEAVE.
                    END.
                END.
           END.
        END.
    END.
    ELSE IF SUBSTR(str,1,4) = "GDPR" THEN DO:
        f-resline.gdpr-flag = SUBSTR(str,5). /*ITA 121218*/        
        /*IF avail-gdpr THEN DO:
            FIND FIRST bguest WHERE bguest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
            IF AVAILABLE bguest THEN DO:
                ASSIGN do-it1 = YES.
                FIND FIRST mc-guest WHERE mc-guest.gastnr = bguest.gastnr NO-LOCK NO-ERROR.
                IF AVAILABLE mc-guest THEN ASSIGN do-it1 = NO.
                ELSE ASSIGN do-it1 = YES.

                IF do-it1 = YES THEN DO:
                    IF bguest.land NE " " THEN DO:
                        FIND FIRST nation-list WHERE nation-list.kurzbez = bguest.land NO-LOCK NO-ERROR.
                        IF AVAILABLE nation-list THEN do-it1 = YES.
                        ELSE do-it1 = NO.
                    END.
    
                    IF do-it1 = NO THEN DO:
                          IF bguest.nation1 NE " " THEN DO:
                              FIND FIRST nation-list WHERE nation-list.kurzbez = bguest.nation1 NO-LOCK NO-ERROR.
                              IF AVAILABLE nation-list THEN do-it1 = YES.
                              ELSE do-it1 = NO.
                          END.                      
                    END.
                    ASSIGN f-resline.gdpr-flag = STRING(do-it1).                
                END.                
            END.
        END.  */
    END.
    ELSE IF SUBSTR(str,1,9) = "MARKETING" THEN DO:
        f-resline.mark-flag = SUBSTR(str,10).   /*gerald Req Tauzia 14/12/20*/
    END.
    ELSE IF SUBSTR(str,1,10) = "NEWSLETTER" THEN DO:
        f-resline.news-flag = SUBSTR(str,11).   /*gerald Req Tauzia 14/12/20*/
    END.
  END.
  
  /* SY 01 JUL 2017 */
  FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
      AND reslin-queasy.resnr = reslin-list.resnr
      AND reslin-queasy.reslinnr = reslin-list.reslinnr
      NO-LOCK NO-ERROR.
  IF AVAILABLE reslin-queasy THEN
  DO:
      FIND FIRST queasy WHERE queasy.KEY = 189 NO-LOCK NO-ERROR.
      IF AVAILABLE queasy THEN
      ASSIGN f-resline.voucher = f-resline.voucher + CHR(2)
                               + reslin-queasy.char3.
  END.

  IF f-resline.contcode NE "" THEN 
  DO:  
    FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = 
      f-resline.contcode NO-LOCK NO-ERROR.
    f-resline.combo-code = f-resline.contcode.
    IF AVAILABLE queasy THEN
    DO:
      f-resline.tip-code = queasy.char1 + " - " + queasy.char2.
      FIND FIRST rbuff WHERE rbuff.CODE = f-resline.contcode NO-LOCK NO-ERROR.
      IF AVAILABLE rbuff THEN
      DO:
        FIND FIRST prmarket WHERE prmarket.nr = rbuff.marknr NO-LOCK NO-ERROR.
        IF AVAILABLE prmarket THEN
        ASSIGN 
            f-resline.marknr   = rbuff.marknr
            f-resline.tip-code = f-resline.tip-code + " ["
                               + prmarket.bezeich + "]"
        . 
      END.
    END.
  END.

  IF (res-mode = "modify" OR res-mode = "inhouse") 
    AND SUBSTR(bediener.permission, 43, 2) LT "2" THEN
    f-resline.enable-disc = NO.
 
  IF res-mode = "modify" OR res-mode = "inhouse"
      OR res-mode = "split" THEN
  DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
      str = ENTRY(i, res-line.zimmer-wunsch, ";").
      IF SUBSTR(str,1,10) = "$OrigCode$" THEN
      DO:
        ASSIGN
          prevCode                  = SUBSTR(str,11)
          f-resline.origcontcode    = prevCode
        .
        LEAVE.
      END.
  END.
  
  IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN DO:
          FIND FIRST guest-pr WHERE guest-pr.gastnr = inp-gastnr NO-LOCK NO-ERROR. 
          IF AVAILABLE guest-pr THEN
          DO:
          DEF BUFFER qsy FOR queasy.
            FOR EACH guest-pr WHERE guest-pr.gastnr = inp-gastnr 
              AND guest-pr.CODE NE f-resline.contcode NO-LOCK,
              FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = guest-pr.CODE
               BY queasy.logi2 DESCENDING BY queasy.char1:
              do-it = YES.
              IF queasy.char1 NE prevCode THEN 
              DO:
                /* Malik Serverless */
                IF queasy.date1 NE ? THEN
                DO:
                    IF f-resline.ci-date LT queasy.date1 THEN do-it = NO.
                    ELSE IF f-resline.ci-date GT queasy.date2 THEN do-it = NO.
                END.
                ELSE 
                DO:
                  do-it = NO.
                END.
                /* END Malik */
                /*
                IF f-resline.ci-date LT queasy.date1 THEN do-it = NO.
                ELSE IF f-resline.ci-date GT queasy.date2 THEN do-it = NO.
                */
              END.
              IF do-it THEN
              DO:
                f-resline.combo-code = f-resline.combo-code + ";" + guest-pr.CODE.
                IF f-resline.contcode = "" THEN 
                DO:    
                  ASSIGN f-resline.contcode = guest-pr.CODE.
                  f-resline.tip-code = queasy.char1 + " - " + queasy.char2.
                
                  IF queasy.logi2 THEN
                  DO:
                    FIND FIRST rbuff WHERE rbuff.CODE = f-resline.contcode NO-LOCK NO-ERROR.
                    IF AVAILABLE rbuff THEN ifTask = rbuff.char1[5].
                    DO tokcounter = 1 TO NUM-ENTRIES(ifTask, ";") - 1:
                      mesToken = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 1, 2).
                      mesValue = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 3).
                      CASE mesToken:
                        WHEN "RC" THEN rCode = mesValue.
                      END CASE.
                    END.
                    IF rCode NE "" THEN
                    DO:
                      FIND FIRST rbuff WHERE rbuff.CODE = rCode NO-LOCK NO-ERROR.
                      IF AVAILABLE rbuff THEN 
                          FIND FIRST qsy WHERE qsy.key = 18 AND qsy.number1 = rbuff.marknr NO-LOCK NO-ERROR.
                    END.
                  END.
                  ELSE
                  DO:
                    FIND FIRST rbuff WHERE rbuff.CODE = guest-pr.CODE NO-LOCK NO-ERROR.
                    IF AVAILABLE rbuff THEN
                      FIND FIRST prmarket WHERE prmarket.nr = rbuff.marknr NO-LOCK NO-ERROR.
                    IF AVAILABLE prmarket THEN
                    DO:
                      ASSIGN f-resline.tip-code = f-resline.tip-code + " ["
                        + prmarket.bezeich + "]".           
                      FIND FIRST qsy WHERE qsy.KEY = 18 
                        AND qsy.number1 = prmarket.nr NO-LOCK NO-ERROR.
                    END.
                  END.
        
                  IF AVAILABLE qsy THEN 
                  DO:
                    FIND FIRST currency-list WHERE 
                      currency-list.wabkurz = qsy.char3 NO-ERROR.
                    IF NOT AVAILABLE currency-list THEN
                    DO:
                      CREATE currency-list.
                      ASSIGN currency-list.wabkurz = qsy.char3.
                    END.
                  END.
                END.
              END.
            END.
          END.
  END.

  /*Add By Gerald 210220 Ratecode RmSharer = Ratecode MainGuuest */
  IF (res-line.resstatus = 11 OR res-line.resstatus = 13)
     AND f-resline.contcode = " " THEN DO:

      FIND FIRST bresline WHERE bresline.resnr = res-line.resnr 
          AND bresline.reslinnr NE res-line.reslinnr
          AND bresline.kontakt-nr EQ res-line.kontakt-nr NO-LOCK NO-ERROR.
      IF AVAILABLE bresline THEN DO:
          DO i = 1 TO NUM-ENTRIES(bresline.zimmer-wunsch,";") - 1:
            str = ENTRY(i, bresline.zimmer-wunsch, ";").
            IF SUBSTR(str,1,6) = "$CODE$" THEN 
             ASSIGN 
                f-resline.contcode  = SUBSTR(str,7)
                f-resline.combo-code = f-resline.contcode.
          END.
      END.
  END.

  RUN disp-allotment. 
  RUN get-currency. 
 
  ASSIGN
    f-resline.l-ankunft = reslin-list.ankunft
    f-resline.l-abreise = reslin-list.abreise 
    f-resline.l-night   = reslin-list.anztage
  . 
 
  IF reslin-list.active-flag = 0 AND reslin-list.zinr NE "" THEN
  DO:
    FIND FIRST outorder WHERE outorder.zinr = reslin-list.zinr 
      AND outorder.betriebsnr = reslin-list.resnr NO-LOCK NO-ERROR. 
    f-resline.offmarket = AVAILABLE outorder.
  END.

    
  RUN disp-history. 
  RUN check-dynaRate.
  RUN check-bedsetup.
 
  FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
    AND reslin-queasy.resnr = reslin-list.resnr 
    AND reslin-queasy.reslinnr = reslin-list.reslinnr NO-LOCK NO-ERROR. 
  f-resline.fixed-rate = AVAILABLE reslin-queasy.
  IF f-resline.fixed-rate AND reslin-list.l-zuordnung[1] = 0 THEN
  DO:
      FIND FIRST zimkateg WHERE zimkateg.zikatnr = reslin-list.zikatnr
          NO-LOCK NO-ERROR.
      IF AVAILABLE zimkateg THEN
      ASSIGN
          f-resline.rate-zikat       = zimkateg.kurzbez
          reslin-list.l-zuordnung[1] = zimkateg.zikatnr
      .
  END.

  IF NOT f-resline.fixed-rate AND (bediener.char1 NE "") THEN 
    f-resline.enable-disc = YES.

  IF res-mode = "new" OR res-mode = "insert" OR res-mode = "qci" THEN 
    RUN set-roomrate(YES). /* SY: this must be after check-dynarate */

  /*ITA 271216*/
  IF res-mode = "inhouse" AND reslin-list.resstatus = 8 THEN
        RUN set-roomrate(YES).

  IF NOT split-modify THEN
  RUN mk-resline-query-q1bl.p (pvILanguage, YES, YES, inp-resnr,
                 INPUT-OUTPUT TABLE rline-list,
                 INPUT-OUTPUT TABLE reschanged-list).



/* SY 11 AUG 2015: replaced by above statement
  DEF BUFFER buf-rline-list FOR rline-list.
  IF res-mode = "inhouse" THEN 
  DO:
    FOR EACH res-line WHERE res-line.gastnr = inp-gastnr 
        AND res-line.resnr = inp-resnr 
        AND (res-line.resstatus EQ 6 OR res-line.resstatus EQ 13)
        AND (res-line.l-zuordnung[3] = 0) NO-LOCK, 
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
        NO-LOCK BY res-line.zinr:
        CREATE rline-list.
        BUFFER-COPY res-line TO rline-list.
        ASSIGN
        rline-list.res-char                = ""
        rline-list.rsvname                 = reservation.NAME
        rline-list.kurzbez                 = zimkateg.kurzbez
        rline-list.status-str              = "".

    END.
  END.
  ELSE IF res-mode NE "new" OR res-mode = "qci" THEN 
  DO: 
    FOR EACH res-line WHERE res-line.gastnr = inp-gastnr 
        AND res-line.resnr = inp-resnr 
        AND (res-line.resstatus LE 5 OR res-line.resstatus EQ 11)
        AND (res-line.l-zuordnung[3] = 0) NO-LOCK, 
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
        NO-LOCK BY res-line.zinr BY res-line.resstatus:
        CREATE rline-list.
        BUFFER-COPY res-line TO rline-list.
        ASSIGN
        rline-list.res-char                = ""
        rline-list.rsvname                 = reservation.NAME
        rline-list.kurzbez                 = zimkateg.kurzbez
        rline-list.status-str              = "".
    END.
  END.
*/

  IF f-resline.restricted THEN
    msg-str = msg-str + CHR(2) + "&W"
      + translateExtended ("This is Reservation with Restricted Discounted Rate",lvCAREA,"")   + CHR(10)
      + translateExtended ("Any reservation data changes such as C/I- or C/O-date",lvCAREA,"") + CHR(10)
      + translateExtended ("might have impact to the given room rate.",lvCAREA,"") + CHR(10).


/* SY 11 AUG 2015 */
  IF res-mode = "split" THEN
  RUN check-timebl.p(2, inp-resnr, inp-reslinnr, "res-line", 
     init-time, init-date, OUTPUT flag-ok, OUTPUT init-time, 
     OUTPUT init-date).


/*************** Procedures *****************/

PROCEDURE fill-flightnr: 
  ASSIGN
    f-resline.flight1 = SUBSTR(res-line.flight-nr, 1, 6)
    f-resline.eta     = SUBSTR(res-line.flight-nr, 7, 5) 
    f-resline.flight2 = SUBSTR(res-line.flight-nr, 12, 6) 
    f-resline.etd     = SUBSTR(res-line.flight-nr, 18, 5)
  . 
  IF TRIM(f-resline.eta) = "" THEN f-resline.eta = "0000". 
  IF TRIM(f-resline.etd) = "" THEN f-resline.etd = "0000". 
END. 

PROCEDURE split-resline: 
  DEFINE VARIABLE   i       AS INTEGER. 
  DEFINE VARIABLE anz       AS INTEGER. 
  DEFINE VARIABLE reihe     AS INTEGER INITIAL 0.
  DEFINE VARIABLE main-reihe AS INTEGER INITIAL 0.

/* SY 01 JUL 2017 */
  DEFINE VARIABLE zeit      AS INTEGER NO-UNDO.

  DEFINE BUFFER m-queasy    FOR reslin-queasy. 
  DEFINE BUFFER m-leist     FOR fixleist. 
  DEFINE BUFFER resmember   FOR res-line. 
  DEFINE BUFFER rline       FOR res-line.
  DEFINE BUFFER genbuff     FOR gentable.
  DEFINE BUFFER bline       FOR res-line.
  DEFINE BUFFER prline      FOR res-line.


  DEFINE VARIABLE max-comp        AS INTEGER  NO-UNDO. 
  DEFINE VARIABLE com-rm          AS INTEGER  NO-UNDO.
  DEFINE VARIABLE its-wrong       AS LOGICAL  NO-UNDO.
  DEFINE VARIABLE msg-str         AS CHAR    INIT ""  NO-UNDO.
  DEFINE VARIABLE pswd-str        AS CHAR    INIT ""  NO-UNDO.

  
/* SY 01 JUL 2017 */
  zeit = TIME - 2.

  /*ITA 050218 ......*/
  FIND FIRST bline WHERE bline.resnr = inp-resnr
      AND bline.reslinnr = inp-reslinnr NO-LOCK NO-ERROR.
  IF AVAILABLE bline THEN DO: 
      RUN check-complimentbl.p(pvILanguage, bline.resnr, 
                                 bline.reslinnr, 
                                 bline.gastnr, bline.ankunft, 
                                 f-resline.marknr, bline.zikatnr, bline.arrangement, 
                                 bline.zimmeranz, bline.zipreis, 
                                 OUTPUT its-wrong, OUTPUT com-rm, OUTPUT max-comp,
                                 OUTPUT pswd-str, OUTPUT msg-str).  
  END.

  FOR EACH rline WHERE rline.resnr = inp-resnr 
    AND rline.active-flag LE 1 NO-LOCK BY rline.reslinnr: 
    FIND FIRST res-line WHERE RECID(res-line) = RECID(rline) EXCLUSIVE-LOCK.
    IF reihe = 0 THEN reihe = res-line.reslinnr.

    IF res-line.reslinnr = 1 THEN DO:
          CREATE m-queasy.
          ASSIGN
              m-queasy.key      = "ResChanges"
              m-queasy.resnr    = res-line.resnr
              m-queasy.reslinnr = res-line.reslinnr  /*FT 090514*/
              m-queasy.date2    = TODAY 
              m-queasy.number2  = zeit /* SY 01 JUL 2017 */
            .
          
          m-queasy.char3 = STRING(res-line.ankunft) + ";" 
                            + STRING(res-line.ankunft) + ";" 
                            + STRING(res-line.abreise) + ";" 
                            + STRING(res-line.abreise) + ";" 
                            + STRING(res-line.zimmeranz) + ";" 
                            + STRING(res-line.zimmeranz) + ";" 
                            + STRING(res-line.erwachs) + ";" 
                            + STRING(res-line.erwachs) + ";" 
                            + STRING(res-line.kind1) + ";" 
                            + STRING(res-line.kind1) + ";" 
                            + STRING(res-line.gratis) + ";" 
                            + STRING(res-line.gratis) + ";" 
                            + STRING(res-line.zikatnr) + ";" 
                            + STRING(res-line.zikatnr) + ";" 
                            + STRING(res-line.zinr) + ";" 
                            + STRING(res-line.zinr) + ";" 
                            + STRING(res-line.arrangement) + ";" 
                            + STRING(res-line.arrangement) + ";"
                            + STRING(res-line.zipreis) + ";" 
                            + STRING(res-line.zipreis) + ";"
                            + STRING(user-init) + ";" 
                            + STRING(user-init) + ";" 
                            + STRING(TODAY) + ";" 
                            + STRING(TODAY) + ";" 
                            + STRING(res-line.NAME) + ";" 
                            + STRING("Splitted Reservation") + ";". 
          RELEASE m-queasy.
    END.
    
    IF priscilla-active THEN
    DO:
        IF res-line.zimmeranz GT 1 THEN
            RUN intevent-1.p(9, res-line.zinr, "Priscilla", res-line.resnr, res-line.reslinnr). 
    END.

    FIND FIRST gentable WHERE gentable.KEY = "reservation"
      AND gentable.number1 = res-line.resnr
      AND gentable.number2 = res-line.reslinnr NO-LOCK NO-ERROR.  

    /*IF res-line.reslinnr = 1 AND res-line.reslinnr NE 11 THEN 
        ASSIGN main-reihe = f-resline.reslinnr.*/

    IF res-line.resstatus = 11 THEN DO:
        FOR EACH prline WHERE prline.resnr = res-line.resnr 
              AND prline.resstatus = 11 AND prline.kontakt-nr = 1 BY prline.reslinnr DESC:
            ASSIGN main-reihe = prline.reslinnr + 1.
            LEAVE.
        END.
    END.
    
    /* SY 01 JUL 2017 */
    ASSIGN
        zeit = zeit + 2
        i    = 2.
    DO WHILE i LE res-line.zimmeranz: 
      CREATE resmember.
      ASSIGN
        resmember.zimmeranz = 1
        resmember.reslinnr  = f-resline.reslinnr
        resmember.resname   = f-resline.main-resname.
      
      BUFFER-COPY res-line EXCEPT zimmeranz reslinnr resname TO resmember.
        
      /*IT 030122 --> Sharer mengikuti main guest saat di split*/
      IF res-line.resstatus = 11 THEN DO:
          ASSIGN 
              resmember.kontakt-nr = main-reihe
              main-reihe           = main-reihe + 1.
      END.

      IF priscilla-active THEN
      DO:
        RUN intevent-1.p(13, "", "Priscilla", resmember.resnr, resmember.reslinnr). 
      END.
      IF com-rm NE 0 THEN 
          ASSIGN resmember.zipreis = 0
                 com-rm = com-rm - 1.

      CREATE m-queasy.
      ASSIGN
          m-queasy.key = "ResChanges"
          m-queasy.resnr = res-line.resnr
          m-queasy.reslinnr = f-resline.reslinnr  /*FT 090514*/
          m-queasy.date2 = TODAY 
          m-queasy.number2 = zeit /* SY 01 JUL 2017 */
        .
      
      m-queasy.char3 = STRING(res-line.ankunft) + ";" 
                        + STRING(res-line.ankunft) + ";" 
                        + STRING(res-line.abreise) + ";" 
                        + STRING(res-line.abreise) + ";" 
                        + STRING(res-line.zimmeranz) + ";" 
                        + STRING(res-line.zimmeranz) + ";" 
                        + STRING(res-line.erwachs) + ";" 
                        + STRING(res-line.erwachs) + ";" 
                        + STRING(res-line.kind1) + ";" 
                        + STRING(res-line.kind1) + ";" 
                        + STRING(res-line.gratis) + ";" 
                        + STRING(res-line.gratis) + ";" 
                        + STRING(res-line.zikatnr) + ";" 
                        + STRING(res-line.zikatnr) + ";" 
                        + STRING(res-line.zinr) + ";" 
                        + STRING(res-line.zinr) + ";" 
                        + STRING(res-line.arrangement) + ";" 
                        + STRING(res-line.arrangement) + ";"
                        + STRING(res-line.zipreis) + ";" 
                        + STRING(res-line.zipreis) + ";"
                        + STRING(user-init) + ";" 
                        + STRING(user-init) + ";" 
                        + STRING(TODAY) + ";" 
                        + STRING(TODAY) + ";" 
                        + STRING(res-line.NAME) + ";" 
                        + STRING("Splitted Reservation") + ";". 
      RELEASE m-queasy.

      FOR EACH reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
        AND reslin-queasy.resnr = res-line.resnr 
        AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK: 
        CREATE m-queasy. 
        ASSIGN m-queasy.reslinnr = f-resline.reslinnr.  /*FT 090514*/
        BUFFER-COPY reslin-queasy EXCEPT reslinnr TO m-queasy.
        RELEASE m-queasy. 
      END. 

      IF resmember.zipreis NE 0 THEN DO:
          FOR EACH reslin-queasy WHERE reslin-queasy.key = "arrangement" 
            AND reslin-queasy.resnr = res-line.resnr 
            AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK: 
            CREATE m-queasy.
            ASSIGN m-queasy.reslinnr = f-resline.reslinnr.  /*FT 090514*/
            BUFFER-COPY reslin-queasy EXCEPT reslinnr TO m-queasy.
            RELEASE m-queasy. 
          END. 

          FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr 
            AND fixleist.reslinnr = res-line.reslinnr NO-LOCK: 
            CREATE m-leist. 
            ASSIGN m-leist.reslinnr = f-resline.reslinnr.  /*FT 090514*/
            BUFFER-COPY fixleist EXCEPT reslinnr TO m-leist.
            RELEASE m-leist. 
          END. 
      END.
                      
      IF AVAILABLE gentable THEN
      DO:
        CREATE genbuff.
        ASSIGN genbuff.number2 = f-resline.reslinnr.  /*FT 090514*/
        BUFFER-COPY gentable EXCEPT number2 TO genbuff.
        RELEASE genbuff.
      END.

      FIND CURRENT resmember NO-LOCK. 
/*      
      CREATE reschanged-list. 
      reschanged-list.reslinnr = inp-reslinnr. 
*/      
      f-resline.reslinnr = f-resline.reslinnr + 1. 
      i = i + 1. 
    END. 
    res-line.zimmeranz = 1. 
    FIND CURRENT res-line NO-LOCK.
    RELEASE res-line. 
  END.   
  f-resline.reslinnr = reihe. 
  FIND FIRST res-line WHERE res-line.resnr = inp-resnr AND res-line.reslinnr = reihe NO-LOCK.
END. 

PROCEDURE check-bedsetup:
  IF reslin-list.setup NE 0 THEN 
  DO: 
    IF AVAILABLE zimkateg THEN
    DO:
      FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr 
        AND zimmer.setup = reslin-list.setup NO-LOCK NO-ERROR. 
    END.
      
    IF NOT AVAILABLE zimmer THEN 
    DO:  
      ASSIGN 
        reslin-list.setup  = 0
        f-resline.c-setup  = ""
      .
      RETURN.
    END.
    ELSE
    DO:
      FIND FIRST paramtext WHERE paramtext.txtnr = (9200 + reslin-list.setup) 
        NO-LOCK. 
      ASSIGN f-resline.c-setup = SUBSTR(paramtext.notes,1,1).
    END.
  END. 
  ELSE
  DO:
    ASSIGN 
      reslin-list.setup  = 0
      f-resline.c-setup  = ""
    .
    RUN check-bedsetup1.
  END.
END. 

PROCEDURE disp-allotment: 
  IF reslin-list.kontignr = 0 THEN RETURN.
  IF reslin-list.kontignr GT 0 THEN 
    FIND FIRST kontline WHERE kontline.kontignr = reslin-list.kontignr 
      AND kontline.kontstat = 1 NO-LOCK NO-ERROR. 
  ELSE 
    FIND FIRST kontline WHERE kontline.kontignr = - reslin-list.kontignr 
      AND kontline.betriebsnr = 1 AND kontline.kontstat = 1 NO-LOCK NO-ERROR. 
  IF AVAILABLE kontline THEN 
  ASSIGN 
    f-resline.kontignr  = reslin-list.kontignr
    f-resline.allot-str = kontline.kontcode
  .
END. 

PROCEDURE get-currency: 
DEFINE VARIABLE curr-wabnr      AS INTEGER           NO-UNDO. 
DEFINE VARIABLE guest-currency  AS INTEGER INITIAL 0 NO-UNDO.
DEFINE BUFFER waehrung1         FOR waehrung. 
DEFINE BUFFER rline             FOR res-line. 
DEFINE BUFFER gbuff             FOR guest.

  FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
  FIND FIRST waehrung1 WHERE waehrung1.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE waehrung1 THEN 
  DO:
    msg-str = translateExtended ("Local Currency Code incorrect! (Param 152 / Grp 7)", lvCAREA, "") 
            + CHR(10).
    RETURN. 
  END.
  ASSIGN f-resline.local-nr = waehrung1.waehrungsnr. 
 
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung1 WHERE waehrung1.wabkurz = htparam.fchar 
    NO-LOCK NO-ERROR. 
  IF (NOT AVAILABLE waehrung1) AND f-resline.foreign-rate THEN 
  DO:    
    msg-str = translateExtended ("Foreign Currency Code incorrect! (Param 144 / Grp 7)",lvCAREA,"")
            + CHR(10).
    RETURN.
  END.
  IF AVAILABLE waehrung1 THEN foreign-nr = waehrung1.waehrungsnr. 

  FIND FIRST gbuff WHERE gbuff.gastnr = inp-gastnr NO-LOCK.
  IF gbuff.notizen[3] NE "" THEN
  DO:
    FIND FIRST waehrung1 WHERE waehrung1.wabkurz = gbuff.notizen[3] 
      NO-LOCK NO-ERROR.
    IF AVAILABLE waehrung1 THEN 
    ASSIGN guest-currency = waehrung1.waehrungsnr.
  END.

  FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement" 
    AND reslin-queasy.resnr = reslin-list.resnr 
    AND reslin-queasy.reslinnr = reslin-list.reslinnr NO-LOCK NO-ERROR. 

  IF AVAILABLE reslin-queasy THEN 
  DO: 
    FOR EACH waehrung1 WHERE waehrung1.waehrungsnr NE reslin-list.betriebsnr 
      AND waehrung1.betriebsnr = 0 NO-LOCK BY waehrung1.bezeich: 
        /* Malik Serverless */
        IF f-resline.currency NE ? THEN
        DO:
          f-resline.currency = f-resline.currency + waehrung1.wabkurz + ";".
        END.
        ELSE
        DO:
          f-resline.currency = "".
          f-resline.currency = f-resline.currency + waehrung1.wabkurz + ";".
        END.
        /* END Malik */

        /* f-resline.currency = f-resline.currency + waehrung1.wabkurz + ";". */
    END. 
    FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr 
        = reslin-list.betriebsnr NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung1 THEN 
      f-resline.currency = waehrung1.wabkurz + ";" + f-resline.currency.
    RETURN. 
  END. 

  FIND FIRST currency-list NO-ERROR.
  IF AVAILABLE currency-list THEN
  DO:
    FOR EACH currency-list:
      f-resline.currency = f-resline.currency + currency-list.wabkurz + ";".
    END.
    RETURN.
  END.

  IF reslin-list.betriebsnr = 0 OR f-resline.marknr NE 0 THEN 
  DO: 
  DEFINE VARIABLE found AS LOGICAL INITIAL NO. 
    IF (res-mode = "new" OR res-mode = "insert" 
       OR res-mode = "qci" OR f-resline.marknr NE 0) THEN 
    DO: 
      RELEASE guest-pr.
      IF f-resline.contcode NE "" THEN FIND FIRST guest-pr WHERE guest-pr.CODE = f-resline.contcode
        NO-LOCK NO-ERROR.
      IF NOT AVAILABLE guest-pr THEN
      FIND FIRST guest-pr WHERE guest-pr.gastnr = inp-gastnr NO-LOCK NO-ERROR. 
      IF AVAILABLE guest-pr THEN 
      DO: 
        IF f-resline.marknr = 0 THEN
        DO:
          FIND FIRST ratecode WHERE ratecode.CODE = guest-pr.CODE
              NO-LOCK NO-ERROR.
          IF AVAILABLE ratecode THEN f-resline.marknr = ratecode.marknr.
        END.
        IF f-resline.marknr NE 0 THEN 
        DO: 
          FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 = f-resline.marknr 
            NO-LOCK NO-ERROR. 
          IF NOT AVAILABLE queasy OR (AVAILABLE queasy AND queasy.char3 = "") 
            THEN FIND FIRST queasy WHERE queasy.key = 2 AND queasy.char1 
            = guest-pr.code NO-LOCK NO-ERROR. 
        END. 
        ELSE FIND FIRST queasy WHERE queasy.key = 2 AND queasy.char1 
          = guest-pr.code NO-LOCK NO-ERROR. 
        IF AVAILABLE queasy THEN 
        DO: 
          IF queasy.key = 18 THEN FIND FIRST waehrung1 WHERE waehrung1.wabkurz 
            = queasy.char3 NO-LOCK NO-ERROR. 
          ELSE FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = queasy.number1 
            NO-LOCK NO-ERROR. 
          IF AVAILABLE waehrung1 THEN 
          DO: 
            found = YES. 
            curr-wabnr = waehrung1.waehrungsnr. 
            FIND FIRST rline WHERE rline.resnr = inp-resnr 
              AND rline.reslinnr = inp-reslinnr EXCLUSIVE-LOCK NO-ERROR. 
            IF AVAILABLE rline THEN 
            DO: 
              rline.betriebsnr = waehrung1.waehrungsnr. 
              FIND CURRENT rline NO-LOCK. 
            END. 
            reslin-list.betriebsnr = waehrung1.waehrungsnr.
          END. 
        END. 
      END. 
    END. 

    IF NOT found THEN 
    DO: 
      IF reslin-list.adrflag = YES OR NOT f-resline.foreign-rate THEN 
      DO: 
        curr-wabnr = f-resline.local-nr. 
        reslin-list.betriebsnr = f-resline.local-nr. 
        FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = f-resline.local-nr NO-LOCK. 
      END. 
      ELSE 
      DO: 
        IF guest-currency NE 0 THEN curr-wabnr = guest-currency.
        ELSE curr-wabnr = foreign-nr. 
        reslin-list.betriebsnr = curr-wabnr.
      END. 
      FOR EACH waehrung1 WHERE waehrung1.waehrungsnr NE curr-wabnr 
        AND waehrung1.betriebsnr = 0 NO-LOCK BY waehrung1.bezeich: 
        f-resline.currency = f-resline.currency + waehrung1.wabkurz + ";".
      END. 
      FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = curr-wabnr NO-LOCK. 
    END. 
  END. 
  ELSE 
  DO: 
    FOR EACH waehrung1 WHERE waehrung1.waehrungsnr NE reslin-list.betriebsnr 
      AND waehrung1.betriebsnr = 0 NO-LOCK BY waehrung1.bezeich: 
      f-resline.currency = f-resline.currency + waehrung1.wabkurz + ";". 
    END. 
    FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr 
      = reslin-list.betriebsnr NO-LOCK. 
  END.  
  IF AVAILABLE waehrung1 THEN
  DO:
    IF f-resline.currency NE ? THEN
      f-resline.currency = waehrung1.wabkurz + ";" + f-resline.currency. 
    ELSE f-resline.currency = waehrung1.wabkurz.
  END.
END. 
 
PROCEDURE disp-history: 
DEF VARIABLE i-anzahl AS INTEGER NO-UNDO INIT 0.
  FOR EACH history WHERE history.gastnr = reslin-list.gastnrmember 
      NO-LOCK BY history.ankunft DESCENDING:
      i-anzahl = i-anzahl + 1.
      CREATE t-history.
      BUFFER-COPY history TO t-history.
      IF i-anzahl = 4 THEN RETURN.
  END.
END. 

PROCEDURE set-roomrate: 
DEFINE INPUT PARAMETER direct-change AS LOGICAL. 
DEFINE VARIABLE datum           AS DATE. 
DEFINE VARIABLE add-it          AS LOGICAL INITIAL NO. 
DEFINE VARIABLE answer          AS LOGICAL INITIAL NO. 
DEFINE VARIABLE curr-rate       AS DECIMAL. 
DEFINE VARIABLE exchg-rate      AS DECIMAL INITIAL 1. 
DEFINE VARIABLE qty             AS INTEGER. 
DEFINE VARIABLE i               AS INTEGER. 
DEFINE VARIABLE argt-defined    AS LOGICAL INITIAL NO. 
DEFINE VARIABLE current-rate    AS DECIMAL              NO-UNDO.
DEFINE VARIABLE exrate1         AS DECIMAL INITIAL 1. 
DEFINE VARIABLE ex2             AS DECIMAL INITIAL 1. 
DEFINE VARIABLE child1          AS INTEGER INITIAL 0    NO-UNDO. 
DEFINE VARIABLE curr-zikatnr    AS INTEGER              NO-UNDO. 
DEFINE VARIABLE rate-found      AS LOGICAL INITIAL NO   NO-UNDO. 
DEFINE VARIABLE prgrate-found   AS LOGICAL              NO-UNDO.
DEFINE VARIABLE early-flag      AS LOGICAL              NO-UNDO.
DEFINE VARIABLE kback-flag      AS LOGICAL              NO-UNDO.
 
DEFINE VARIABLE wd-array        AS INTEGER EXTENT 8 
  INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 

DEFINE VARIABLE tmpInt AS INTEGER.

DEFINE BUFFER w1 FOR waehrung. 
 
  IF NOT AVAILABLE arrangement THEN RETURN. /* this is the case if param151 = "" */

  IF res-mode NE "new" AND res-mode NE "insert" AND res-mode NE "qci" THEN
  DO:
    IF NOT direct-change AND reslin-list.zipreis NE 0 THEN RETURN. 
    IF SUBSTR(bediener.permission, 43, 1) LT "2" THEN RETURN.
  END.
 
  ASSIGN current-rate = reslin-list.zipreis.

/*  DO NOT change !!! */ 
  datum = reslin-list.ankunft. 
  IF res-mode = "inhouse" THEN datum = f-resline.ci-date. 
    
  /*ITA 091216*/
  IF res-mode = "inhouse" AND reslin-list.resstatus = 8 THEN DO:
      IF reslin-list.ankunft = reslin-list.abreise THEN ASSIGN datum = reslin-list.abreise.
      ELSE ASSIGN datum = reslin-list.abreise - 1.
  END.

  IF reslin-list.l-zuordnung[1] NE 0 THEN 
    curr-zikatnr = reslin-list.l-zuordnung[1]. 
  ELSE curr-zikatnr = reslin-list.zikatnr. 

  FIND FIRST guest-pr WHERE guest-pr.gastnr = inp-gastnr NO-LOCK NO-ERROR. 
/*  
  IF AVAILABLE guest-pr AND prog-str = "" THEN 
  DO: 
    FIND FIRST queasy WHERE queasy.key = 2 AND queasy.char1 = guest-pr.code 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE queasy AND queasy.char3 NE "" THEN 
    DO: 
      OUTPUT STREAM s1 TO ".\_rate.p". 
      PUT STREAM s1 unformatted queasy.char3. 
      OUTPUT STREAM s1 CLOSE. 
      compile value(".\_rate.p"). 
      dos silent "del .\_rate.p". 
      IF NOT compiler:ERROR THEN 
      DO: 
        IF res-mode EQ "inhouse" THEN 
          RUN value(".\_rate.p") (RECID(reslin-list), resnr, reslinnr, 
          billdate, reslin-list.zipreis, NO, OUTPUT reslin-list.zipreis). 
        ELSE RUN value(".\_rate.p") (RECID(reslin-list), resnr, reslinnr, 
          reslin-list.ankunft, reslin-list.zipreis, NO, 
          OUTPUT reslin-list.zipreis). 
        DISP reslin-list.zipreis WITH FRAME frame1. 
        PAUSE 0. 
        RETURN. 
      END. 
    END. 
  END. 
*/ 
  IF reslin-list.erwachs = 0 AND reslin-list.kind1 = 0
    AND reslin-list.kind2 = 0 THEN reslin-list.zipreis = 0. 
  ELSE 
  DO: 
    IF f-resline.fixed-rate THEN 
    DO: 
      FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
        AND reslin-queasy.resnr = reslin-list.resnr 
        AND reslin-queasy.reslinnr = reslin-list.reslinnr 
        AND reslin-queasy.date1 LE datum
        AND reslin-queasy.date2 GE datum
        /*AND datum GE reslin-queasy.date1 
        AND datum LE reslin-queasy.date2 FT serverless*/ NO-LOCK NO-ERROR. 
      IF AVAILABLE reslin-queasy THEN 
      ASSIGN
        reslin-list.zipreis    = reslin-queasy.deci1
        f-resline.rate-tooltip = "" 
        rate-found             = YES
      . 
    END. 
 
    /*IF NOT rate-found THEN
    DO:*/
      FIND FIRST guest-pr WHERE guest-pr.gastnr = guest.gastnr NO-LOCK NO-ERROR.     
      IF AVAILABLE guest-pr AND NOT rate-found THEN 
      DO: 
        FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 
          = reslin-list.reserve-int NO-LOCK NO-ERROR. 
        IF AVAILABLE queasy AND queasy.logi3 THEN datum = reslin-list.ankunft. 
   
        FIND FIRST queasy WHERE queasy.key = 2 AND 
          queasy.char1 = guest-pr.code NO-LOCK NO-ERROR. 
        IF f-resline.contcode = ? THEN
          f-resline.contcode = "".
        IF f-resline.new-contrate THEN
        DO:
          IF f-resline.bookdate NE ? THEN
            RUN ratecode-rate.p(f-resline.ebdisc-flag, f-resline.kbdisc-flag, reslin-list.resnr, 
                reslin-list.reslinnr, ("!" + f-resline.contcode), f-resline.bookdate, datum, reslin-list.ankunft,
                reslin-list.abreise, reslin-list.reserve-int, arrangement.argtnr,
                curr-zikatnr, reslin-list.erwachs, reslin-list.kind1, reslin-list.kind2,
                reslin-list.reserve-dec, reslin-list.betriebsnr, OUTPUT rate-found,
                OUTPUT reslin-list.zipreis, OUTPUT f-resline.restricted, OUTPUT kback-flag).
          ELSE
            RUN ratecode-rate.p(f-resline.ebdisc-flag, f-resline.kbdisc-flag, reslin-list.resnr, 
                reslin-list.reslinnr, ("!" + f-resline.contcode), f-resline.ci-date, datum, reslin-list.ankunft,
                reslin-list.abreise, reslin-list.reserve-int, arrangement.argtnr,
                curr-zikatnr, reslin-list.erwachs, reslin-list.kind1, reslin-list.kind2,
                reslin-list.reserve-dec, reslin-list.betriebsnr, OUTPUT rate-found,
                OUTPUT reslin-list.zipreis, OUTPUT f-resline.restricted, OUTPUT kback-flag).
        END.
        ELSE
        DO:
          RUN pricecod-rate.p(reslin-list.resnr, reslin-list.reslinnr,
            ("!" + f-resline.contcode), datum, reslin-list.ankunft, reslin-list.abreise, 
            reslin-list.reserve-int, arrangement.argtnr, curr-zikatnr, 
            reslin-list.erwachs, reslin-list.kind1, reslin-list.kind2,
            reslin-list.reserve-dec, reslin-list.betriebsnr, 
            OUTPUT reslin-list.zipreis, OUTPUT rate-found).
        
          IF rate-found THEN
          DO:
            RUN check-bonus(datum).
          END.

/* pending
        RUN usr-prog2(datum, reslin-list.resnr, reslin-list.reslinnr, 
          INPUT-OUTPUT reslin-list.zipreis, OUTPUT prgrate-found). 
        IF prgrate-found THEN rate-found = YES.
        IF NOT rate-found AND bonus-array[curr-i] = YES 
          THEN reslin-list.zipreis = 0.  
*/
        END. /* old contract rate */
        IF AVAILABLE queasy AND queasy.logi1 THEN 
        ASSIGN
          reslin-list.adrflag = YES
          f-resline.rate-tooltip = translateExtended ("Contract Rate in LOCAL CURRENCY.", lvCAREA, "":U)
        . 
      END. /* IF AVAILABLE pricecod */ 
    /*END.*/

    IF NOT rate-found THEN 
    DO: 
      tmpInt = wd-array[WEEKDAY(datum)]. /*FT serverless*/
      IF res-mode = "inhouse" THEN 
      DO: 
        FIND FIRST katpreis WHERE katpreis.zikatnr = curr-zikatnr 
          AND katpreis.argtnr = arrangement.argtnr 
          AND katpreis.startperiode LE datum 
          AND katpreis.endperiode GE datum 
          AND katpreis.betriebsnr = tmpInt NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE katpreis THEN 
        FIND FIRST katpreis WHERE katpreis.zikatnr = curr-zikatnr 
          AND katpreis.argtnr = arrangement.argtnr 
          AND katpreis.startperiode LE datum 
          AND katpreis.endperiode GE datum 
          AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
      END. 
      ELSE 
      DO: 
        FIND FIRST katpreis WHERE katpreis.zikatnr = curr-zikatnr 
          AND katpreis.argtnr = arrangement.argtnr 
          AND katpreis.startperiode LE datum 
          AND katpreis.endperiode GE datum 
          /*AND datum GE katpreis.startperiode 
          AND datum LE katpreis.endperiode FT serverless*/
          AND katpreis.betriebsnr = tmpInt NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE katpreis THEN 
        FIND FIRST katpreis WHERE katpreis.zikatnr = curr-zikatnr 
          AND katpreis.argtnr = arrangement.argtnr 
          AND katpreis.startperiode LE datum
          AND katpreis.endperiode GE datum
          /*AND datum GE katpreis.startperiode 
          AND datum LE katpreis.endperiode FT serverless*/
          AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
      END. 
      IF AVAILABLE katpreis THEN 
      DO: 
        reslin-list.zipreis = get-rackrate(reslin-list.erwachs, 
          reslin-list.kind1, reslin-list.kind2). 
      END. 
      ELSE reslin-list.zipreis = 0. 
    END. 
  END. 
/* 
  IF prog-str NE "" THEN 
  DO: 
    OUTPUT STREAM s1 TO ".\_rate.p". 
    DO i = 1 TO length(prog-str): 
      PUT STREAM s1 SUBSTR(prog-str, i, 1) FORMAT "x(1)". 
    END. 
    OUTPUT STREAM s1 CLOSE. 
    compile value(".\_rate.p"). 
    dos silent "del .\_rate.p". 
    IF NOT compiler:ERROR THEN 
    DO: 
      IF res-mode EQ "inhouse" THEN 
        RUN value(".\_rate.p") (RECID(reslin-list), resnr, reslinnr, 
        ci-date, reslin-list.zipreis, NO, OUTPUT reslin-list.zipreis). 
      ELSE RUN value(".\_rate.p") (RECID(reslin-list), resnr, reslinnr, 
        reslin-list.ankunft, reslin-list.zipreis, NO, 
        OUTPUT reslin-list.zipreis). 
    END. 
  END. 
*/ 
  IF NOT direct-change AND NOT rate-readonly 
    AND current-rate NE 0 AND reslin-list.zipreis = 0 THEN
    ASSIGN reslin-list.zipreis = current-rate.

/* SY 05 Aug 2015: F12 when handling compliment guest */
  IF rate-found AND reslin-list.zipreis = 0
      AND (res-mode EQ "new" OR res-mode EQ "insert" OR res-mode EQ "qci")
      AND (reslin-list.erwachs GT 0 OR reslin-list.kind1 GT 0) THEN
  ASSIGN
      reslin-list.gratis  = reslin-list.erwachs + reslin-list.kind1
      reslin-list.erwachs = 0
      reslin-list.kind1   = 0
  .

END. 

PROCEDURE check-dynaRate:

/*
  IF res-mode NE "new" THEN RETURN.
*/

  FIND FIRST res-dynaRate USE-INDEX date1_ix NO-ERROR.
  IF NOT AVAILABLE res-dynaRate OR res-dynaRate.rmcat EQ "" OR res-dynaRate.rmcat EQ " " 
      OR res-dynaRate.rmcat EQ ? THEN RETURN. /*NC - ##052669 vhpcloud still sent input res-dynaRate not empty */
  
  FIND FIRST arrangement WHERE arrangement.arrangement = res-dynarate.argt NO-LOCK NO-ERROR.
  FIND FIRST paramtext WHERE paramtext.txtnr = (9200 + res-dynaRate.setup) 
    NO-LOCK. 

  FIND FIRST queasy WHERE queasy.KEY = 18 AND queasy.number1 = res-dynaRate.markNo NO-LOCK NO-ERROR.
  IF AVAILABLE queasy THEN /*NC - ##052669*/
  DO:
	  ASSIGN f-resline.currency  = queasy.char3.
	  
	  FIND FIRST waehrung WHERE waehrung.wabkurz = queasy.char3 NO-LOCK NO-ERROR.
	  IF AVAILABLE waehrung THEN
	  ASSIGN reslin-list.betriebsnr = waehrung.waehrungsnr. 
  
	END.
  ELSE DO: /*NC - ##052669*/
	FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK NO-ERROR.
	IF AVAILABLE htparam THEN
	DO:
		ASSIGN f-resline.currency  = htparam.fchar.
		FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR.
		IF NOT AVAILABLE waehrung THEN
			FIND FIRST waehrung NO-LOCK NO-ERROR.
		ASSIGN reslin-list.betriebsnr = waehrung.waehrungsnr.

	END.
  END.
  IF res-dynaRate.date1 NE ? THEN
      reslin-list.ankunft = res-dynaRate.date1. /*FT serverless*/
        
  ASSIGN
    
    reslin-list.arrangement     = res-dynaRate.argt    
    reslin-list.reserve-int     = res-dynaRate.markNo
    f-resline.zikatstr          = res-dynaRate.rmcat
    f-resline.rate-zikat        = res-dynaRate.rmcat
    f-resline.marknr            = res-dynaRate.markNo
    f-resline.contcode          = res-dynaRate.prCode
    f-resline.origcontcode      = res-dynaRate.rCode
    f-resline.combo-code        = res-dynaRate.rCode
    
  .

  FIND FIRST zimkateg WHERE zimkateg.kurzbez = res-dynaRate.rmcat NO-LOCK NO-ERROR.
  IF AVAILABLE zimkateg THEN
      ASSIGN reslin-list.zikatnr         = zimkateg.zikatnr
             reslin-list.l-zuordnung[1]  = zimkateg.zikatnr.

  /* SY 05 Aug 2015: Assignment for paying guest */
  IF reslin-list.gratis = 0 THEN
  ASSIGN
      reslin-list.erwachs     = res-dynaRate.adult
      reslin-list.kind1       = res-dynaRate.child
  .
  
  IF reslin-list.setup = 0 THEN
  ASSIGN
      reslin-list.setup       = res-dynaRate.setup
      f-resline.c-setup       = SUBSTR(paramtext.notes,1,1)
  .

  IF res-dynaRate.rate LT 0 THEN 
      reslin-list.zipreis  = - res-dynaRate.rate.
  ELSE reslin-list.zipreis = res-dynaRate.rate.
 
 
/*  IF res-dynaRate.rate GE 0 THEN   */
  FIND LAST res-dynaRate USE-INDEX date1_ix.

  IF res-dynaRate.date2 NE ? THEN /*FT serverless*/
    ASSIGN reslin-list.abreise = res-dynaRate.date2 + 1.
  IF dayuse-flag THEN reslin-list.abreise = reslin-list.ankunft.
  ASSIGN 
    reslin-list.anztage = reslin-list.abreise - reslin-list.ankunft
    f-resline.arrday    = weekdays[WEEKDAY(reslin-list.ankunft)] 
    f-resline.depday    = weekdays[WEEKDAY(reslin-list.abreise)] 
  .

  FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = f-resline.origcontcode
      NO-LOCK NO-ERROR.

/*
  IF res-dynaRate.rate LT 0 THEN 
  DO: 
      DELETE res-dynaRate.
      RETURN.
  END.
*/
  FOR EACH res-dynaRate USE-INDEX date1_ix:
    CREATE reslin-queasy.
    ASSIGN
      reslin-queasy.key         = "arrangement"
      reslin-queasy.resnr       = inp-resnr
      reslin-queasy.reslinnr    = f-resline.reslinnr /* new booking */
      reslin-queasy.date1       = res-dynaRate.date1
      reslin-queasy.date2       = res-dynaRate.date2
      reslin-queasy.deci1       = res-dynaRate.rate
      reslin-queasy.char2       = res-dynaRate.prCode
      reslin-queasy.char3       = user-init
    .
    IF reslin-queasy.deci1 LT 0 THEN
    DO:
      reslin-queasy.deci1 = - reslin-queasy.deci1.
      DELETE res-dynaRate.
    END.
    f-resline.fixed-rate = YES.
  END.

  f-resline.restricted = AVAILABLE queasy AND queasy.logi2.
  IF (res-mode = "new" OR res-mode = "qci") 
      AND f-resline.restricted THEN
  ASSIGN reslin-list.zimmer-wunsch = reslin-list.zimmer-wunsch 
                                   + "restricted;".

END.

PROCEDURE check-bedsetup1:
DEF VARIABLE anz-setup  AS INTEGER NO-UNDO INIT 0.
DEF VARIABLE curr-setup AS INTEGER NO-UNDO INIT 0.
  IF reslin-list.setup = 0 AND AVAILABLE zimkateg THEN
  DO:
      FOR EACH zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr 
          AND zimmer.setup NE 0 NO-LOCK BY zimmer.setup:
          IF curr-setup = 0 THEN
          ASSIGN
              curr-setup = zimmer.setup
              anz-setup  = 1
          .
          IF zimmer.setup NE curr-setup THEN 
          DO:    
            anz-setup = 2.
            LEAVE.
          END.
      END.
      IF anz-setup = 1 THEN 
      DO:    
          ASSIGN reslin-list.setup = curr-setup.
          FIND FIRST paramtext WHERE paramtext.txtnr = (9200 + curr-setup) 
            NO-LOCK. 
          ASSIGN f-resline.c-setup = SUBSTR(paramtext.notes,1,1).
      END.
  END.
END.

FIND FIRST fixleist WHERE fixleist.resnr = inp-resnr
    AND fixleist.reslinnr = inp-reslinnr NO-LOCK NO-ERROR.
IF AVAILABLE fixleist THEN
    msg-str = msg-str + "FixleistIncluded". /* Jason 1 December 2016, Siteminder v2 */
