
DEFINE TEMP-TABLE res-dynarate
  FIELD date1  AS DATE
  FIELD date2  AS DATE
  FIELD rate   AS DECIMAL
  FIELD rmCat  AS CHAR
  FIELD argt   AS CHAR
  FIELD prcode AS CHAR
  FIELD rCode  AS CHAR
  FIELD markNo AS INTEGER
  FIELD setup  AS INTEGER
  FIELD adult  AS INTEGER
  FIELD child  AS INTEGER
  INDEX date1_ix date1
.

DEFINE TEMP-TABLE reslin-list  LIKE res-line. 

DEFINE TEMP-TABLE nation-list
    FIELD nr        AS INTEGER
    FIELD kurzbez   AS CHAR
    FIELD bezeich   AS CHAR FORMAT "x(32)".

DEF INPUT PARAMETER  pvILanguage        AS INTEGER NO-UNDO.
DEF INPUT PARAMETER  accompany-tmpnr1   AS INTEGER NO-UNDO.
DEF INPUT PARAMETER  accompany-tmpnr2   AS INTEGER NO-UNDO.
DEF INPUT PARAMETER  accompany-tmpnr3   AS INTEGER NO-UNDO.
DEF INPUT PARAMETER  accompany-gastnr   AS INTEGER NO-UNDO.
DEF INPUT PARAMETER  accompany-gastnr2  AS INTEGER NO-UNDO.
DEF INPUT PARAMETER  accompany-gastnr3  AS INTEGER NO-UNDO.
DEF INPUT PARAMETER  comchild           AS INTEGER NO-UNDO.
DEF INPUT PARAMETER  rm-bcol            AS INTEGER NO-UNDO.
DEF INPUT PARAMETER  marknr             AS INTEGER NO-UNDO.
DEF INPUT PARAMETER  bill-instruct      AS INTEGER NO-UNDO.
DEF INPUT PARAMETER  restype            AS INTEGER NO-UNDO.
DEF INPUT PARAMETER  restype0           AS INTEGER NO-UNDO.
DEF INPUT PARAMETER  restype1           AS INTEGER NO-UNDO.
DEF INPUT PARAMETER  contact-nr         AS INTEGER NO-UNDO.
DEF INPUT PARAMETER  cutoff-days        AS INTEGER NO-UNDO.
DEF INPUT PARAMETER  segm_purcode       AS INTEGER NO-UNDO.

DEF INPUT PARAMETER  deposit            AS DECIMAL NO-UNDO.

DEF INPUT PARAMETER  limitdate          AS DATE    NO-UNDO.

DEF INPUT PARAMETER  wechsel-str        AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  origcontcode       AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  groupname          AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  guestname          AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  main-voucher       AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  resline-comment    AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  mainres-comment    AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  purpose-svalue     AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  letter-svalue      AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  segm-svalue        AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  source-svalue      AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  res-mode           AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  prev-zinr          AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  memo-zinr          AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  voucherno          AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  contcode           AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  child-age          AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  flight1            AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  flight2            AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  eta                AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  etd                AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  user-init          AS CHAR    NO-UNDO.
  
DEF INPUT PARAMETER  currency-changed   AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER  fixed-rate         AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER  grpflag            AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER  memozinr-readonly  AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER  group-enable       AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER  init-fixrate       AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER  oral-flag          AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER  pickup-flag        AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER  drop-flag          AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER  ebdisc-flag        AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER  kbdisc-flag        AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER  restricted         AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER  sharer             AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER  coder-exist        AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER  gname-chged        AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER earlyci             AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER gdpr-flag           AS LOGICAL NO-UNDO.

/*gerald Req Tauzia 14/12/20*/
DEF INPUT PARAMETER mark-flag           AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER news-flag           AS LOGICAL NO-UNDO.

/*gerald add input param temp-segment ACDD51*/
DEF INPUT PARAMETER temp-segment        AS CHARACTER NO-UNDO.

DEF INPUT PARAMETER TABLE              FOR reslin-list.
DEF INPUT PARAMETER TABLE              FOR res-dynarate.

DEF OUTPUT PARAMETER update-kcard       AS LOGICAL INIT NO NO-UNDO.
DEF OUTPUT PARAMETER msg-str            AS CHAR    INIT "" NO-UNDO.
DEF OUTPUT PARAMETER waehrungnr         AS INTEGER INIT ?  NO-UNDO.
DEF OUTPUT PARAMETER reserve-dec        AS DECIMAL INIT ?  NO-UNDO.
DEF OUTPUT PARAMETER dyna-rmrate        AS DECIMAL INIT ?  NO-UNDO.
DEF INPUT-OUTPUT PARAMETER tot-qty      AS INTEGER         NO-UNDO.

DEF VARIABLE accompany-tmpnr    AS INTEGER EXTENT 3 NO-UNDO.
DEF VARIABLE ci-date            AS DATE             NO-UNDO.
DEF VARIABLE dynaRate-created   AS LOGICAL          NO-UNDO INIT NO.

DEFINE VARIABLE vipnr1              AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr2              AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr3              AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr4              AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr5              AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr6              AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr7              AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr8              AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr9              AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE max-resline         AS INTEGER INITIAL 0    NO-UNDO.

DEFINE VARIABLE ind-gastnr          AS INTEGER NO-UNDO.
DEFINE VARIABLE wig-gastnr          AS INTEGER NO-UNDO.
DEFINE VARIABLE source-changed      AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE priscilla-active    AS LOGICAL NO-UNDO INIT YES.
DEFINE VARIABLE avail-gdpr          AS LOGICAL NO-UNDO.
DEFINE VARIABLE curr-nat            AS CHAR    NO-UNDO.
DEFINE VARIABLE list-region         AS CHAR    NO-UNDO.
DEFINE VARIABLE list-nat            AS CHAR    NO-UNDO.
DEFINE VARIABLE loopi               AS INTEGER NO-UNDO.

DEFINE VARIABLE avail-mark          AS LOGICAL NO-UNDO.
DEFINE VARIABLE avail-news          AS LOGICAL NO-UNDO.

/* Rd, #752, 27Mar25, date variable */
DEFINE VARIABLE tmpdate            AS DATE NO-UNDO.

DEF BUFFER resline   FOR res-line.

/* SY 04 June 2016 */
DEF BUFFER bbuff FOR bill.
DEF BUFFER buff-bill FOR bill. /*FDL*/
DEF BUFFER bbline FOR bill-line. /*FDL*/


{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mk-resline". 

RUN htpint.p(109, OUTPUT wig-gastnr).
RUN htpint.p(123, OUTPUT ind-gastnr).

ASSIGN
    accompany-tmpnr[1] = accompany-tmpnr1
    accompany-tmpnr[2] = accompany-tmpnr2
    accompany-tmpnr[3] = accompany-tmpnr3
.

RUN htpdate.p(87, OUTPUT ci-date).
FIND FIRST htparam WHERE paramnr = 700 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr1 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 701 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr2 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 702 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr3 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 703 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr4 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 704 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr5 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 705 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr6 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 706 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr7 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 707 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr8 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 708 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr9 = htparam.finteger. 

FIND FIRST htparam WHERE paramnr = 346 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN avail-gdpr = htparam.flogical.

/*gerald Req Tauzia 14/12/20*/
FIND FIRST htparam WHERE paramnr = 477 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich NE "not used" THEN 
DO: 
    avail-news = htparam.flogical. 
    avail-mark = htparam.flogical.
END.
/*end gerald*/

IF avail-gdpr THEN DO:
    FIND FIRST htparam WHERE htparam.paramnr = 448 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN ASSIGN list-region = htparam.fchar.

    FIND FIRST htparam WHERE htparam.paramnr = 449 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN ASSIGN list-nat = htparam.fchar. 

    FOR EACH nation WHERE nation.natcode = 0 NO-LOCK,
        FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe
            AND queasy.char1 MATCHES "*europe*" NO-LOCK BY nation.kurzbez:
        FIND FIRST nation-list WHERE nation-list.nr = nation.nationnr NO-ERROR.
        IF NOT AVAILABLE nation-list THEN DO:                    
            CREATE nation-list.
            ASSIGN nation-list.nr      = nation.nationnr
                   nation-list.kurzbez = nation.kurzbez
                   nation-list.bezeich = ENTRY(1, nation.bezeich, ";").           
        END.          
    END.
    
    IF list-region NE "" THEN DO:
        DO loopi = 1 TO NUM-ENTRIES(list-region, ";"):
            FOR EACH nation WHERE nation.natcode = 0 
                AND nation.untergruppe = INTEGER(ENTRY(loopi, list-region, ";")) NO-LOCK BY nation.kurzbez:
                FIND FIRST nation-list WHERE nation-list.nr = nation.nationnr NO-ERROR.
                IF NOT AVAILABLE nation-list THEN DO:                    
                    CREATE nation-list.
                    ASSIGN nation-list.nr      = nation.nationnr
                           nation-list.kurzbez = nation.kurzbez
                           nation-list.bezeich = ENTRY(1, nation.bezeich, ";").           
                END.
            END.
        END.        
    END.

    IF list-nat NE "" THEN DO:
        DO loopi = 1 TO NUM-ENTRIES(list-nat, ";"):
            FOR EACH nation WHERE nation.natcode = 0 
                AND nation.nationnr = INTEGER(ENTRY(loopi, list-nat, ";")) NO-LOCK BY nation.kurzbez:
                FIND FIRST nation-list WHERE nation-list.nr = nation.nationnr NO-ERROR.
                IF NOT AVAILABLE nation-list THEN DO:                    
                    CREATE nation-list.
                    ASSIGN nation-list.nr      = nation.nationnr
                           nation-list.kurzbez = nation.kurzbez
                           nation-list.bezeich = ENTRY(1, nation.bezeich, ";").           
                END.           
            END.
        END.       
    END.
END.

FIND FIRST reslin-list NO-ERROR.

FIND FIRST arrangement WHERE arrangement.arrangement = reslin-list.arrangement NO-LOCK.

FIND FIRST reservation WHERE reservation.resnr = reslin-list.resnr
  NO-LOCK NO-ERROR.
   
FIND FIRST res-line WHERE res-line.resnr = reslin-list.resnr
  AND res-line.reslinnr = reslin-list.reslinnr NO-LOCK NO-ERROR.
IF NOT AVAILABLE res-line THEN RETURN. /*FT serverless*/
    
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.

/*
IF INTEGER(SUBSTR(source-svalue, 1, INDEX(source-svalue," "))) NE reservation.resart THEN
DO:
    source-changed = YES.
END.
*/

IF res-mode = "modify" OR res-mode = "split" 
  OR res-mode = "inhouse" THEN RUN min-resplan. 

IF res-line.betrieb-gast GT 0 AND res-line.zinr NE "" THEN 
update-kcard = (res-line.ankunft NE reslin-list.ankunft) 
  OR (res-line.abreise NE reslin-list.abreise) 
  OR (reslin-list.zinr NE res-line.zinr). 
 
IF rm-bcol NE 15 AND reslin-list.ankunft NE res-line.ankunft 
  AND reslin-list.resstatus = 1 THEN 
DO: 
  FIND FIRST outorder WHERE outorder.zinr = reslin-list.zinr 
    AND outorder.betriebsnr = reslin-list.resnr NO-LOCK NO-ERROR. 
  IF AVAILABLE outorder THEN 
  DO:   
    FIND CURRENT outorder EXCLUSIVE-LOCK.
    ASSIGN 
        outorder.gespstart = reslin-list.ankunft - outorder.gespende 
                             + outorder.gespstart 
        outorder.gespende  = reslin-list.ankunft. 
    FIND CURRENT outorder NO-LOCK. 
    RELEASE outorder.
  END. 
END. 
 
IF res-mode = "inhouse" THEN 
DO: 
  IF res-line.abreise = ci-date AND reslin-list.abreise GT res-line.abreise 
    AND res-line.zinr = reslin-list.zinr THEN 
  DO:   
    FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
    IF AVAILABLE zimmer AND zimmer.zistatus = 3 THEN 
    DO:    
      FIND CURRENT zimmer EXCLUSIVE-LOCK. 
      zimmer.zistatus = 4. 
      FIND CURRENT zimmer NO-LOCK. 
    END. 
  END. 
  
  IF res-line.zinr NE reslin-list.zinr AND res-line.resstatus = 6 
    AND NOT sharer AND NOT (res-line.zinr = "") THEN 
  DO:   
    RUN rmchg-sharer(res-line.zinr, reslin-list.zinr). 
    FIND FIRST htparam WHERE htparam.paramnr = 307 NO-LOCK. 
    IF htparam.flogical THEN 
      RUN intevent-1.p(2, res-line.zinr, "Move out", res-line.resnr, res-line.reslinnr). 
  END. 
  
  IF (res-line.resstatus = 6) AND NOT sharer 
    AND (res-line.abreise NE reslin-list.abreise)
    AND (res-line.zinr = reslin-list.zinr) THEN
  DO:  
    FIND FIRST htparam WHERE paramnr = 341 NO-LOCK. 
    IF htparam.fchar NE "" THEN 
      RUN intevent-1.p( 9, res-line.zinr, "Chg DepTime!", res-line.resnr, res-line.reslinnr).      
  END.
  
  IF (res-line.resstatus = 6)
    AND ((res-line.abreise NE reslin-list.abreise)
    OR (res-line.zinr NE reslin-list.zinr)
    OR (res-line.zikatnr NE reslin-list.zikatnr)
    OR source-changed) THEN
  DO:
  
    /*ubah disini*/
    RUN intevent-1.p( 1, res-line.zinr, "DataExchange", res-line.resnr, res-line.reslinnr). 
  END.           

  RUN update-billzinr. 
END. 
 
ELSE IF res-mode = "modify" THEN /* move res-sharer TO NEW room */ 
DO: 
  IF res-line.zinr NE reslin-list.zinr AND 
      (res-line.resstatus LE 2 OR res-line.resstatus = 5) THEN 
    RUN rmchg-ressharer(res-line.zinr, reslin-list.zinr, res-line.reslinnr). 
END. 
 
FIND FIRST res-line WHERE res-line.resnr = reslin-list.resnr 
  AND res-line.reslinnr = reslin-list.reslinnr EXCLUSIVE-LOCK. 
  prev-zinr = res-line.zinr. 
  
RUN check-currency. 
/*RUN usr-program.*/ 
/*MT
RUN res-changes.   /* create log file IF any res-line changes */ 
*/

RUN res-changesbl.p(pvILanguage,res-mode,guestname,mainres-comment,
                    resline-comment,user-init,earlyci,fixed-rate,
                    TABLE reslin-list).

/*IF res-mode NE "split" THEN*/
DO:
    FIND FIRST queasy WHERE queasy.KEY = 171 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN RUN update-qsy171.
END.                                           

RUN update-resline. 
RUN res-dyna-rmrate.

RUN update-mainres.
RUN add-resplan. 


IF res-mode = "inhouse" AND (prev-zinr NE res-line.zinr) THEN 
DO: 
  DEF VAR move-str AS CHAR NO-UNDO.
  FIND FIRST htparam WHERE paramnr = 307 NO-LOCK. 
  IF htparam.flogical THEN
  DO:
    ASSIGN move-str = "Move in|" + prev-zinr.
    RUN intevent-1.p(1, res-line.zinr, move-str, 
        res-line.resnr, res-line.reslinnr). 
  END.
  RUN create-historybl.p(res-line.resnr, res-line.reslinnr, 
    prev-zinr, "roomchg", user-init, wechsel-str). 

  /****************** Check MEalCoupon ***************/ 
  FIND FIRST resline WHERE resline.resnr = res-line.resnr 
    AND resline.active-flag LE 1 AND resline.resstatus NE 12 
    AND resline.zinr = prev-zinr NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE resline THEN /* NO guest IN the previous stayed room */ 
  DO: 
    FIND FIRST mealcoup WHERE mealcoup.zinr = prev-zinr 
      AND mealcoup.activeflag = YES USE-INDEX zinrflag_ix EXCLUSIVE-LOCK 
      NO-ERROR. 
    IF AVAILABLE mealcoup THEN 
    DO: 
      mealcoup.zinr = res-line.zinr. 
      FIND CURRENT mealcoup NO-LOCK. 
    END. 
  END. 
    
  IF res-mode = "inhouse" AND res-line.resstatus = 6 AND gname-chged 
  THEN DO: 
    FIND FIRST htparam WHERE paramnr = 307 NO-LOCK. 
    IF htparam.flogical THEN 
      RUN intevent-1.p(1, res-line.zinr, "Change name", res-line.resnr, res-line.reslinnr). 
    FIND FIRST htparam WHERE paramnr = 359 NO-LOCK. 
    IF htparam.flogical THEN 
      RUN intevent-1.p(1, res-line.zinr, "Change name", res-line.resnr, res-line.reslinnr). 
  END. 
 
  IF update-kcard THEN 
  DO: 
    IF coder-exist THEN RUN add-keycard. 
    ELSE 
    msg-str = msg-str + CHR(2) + "&W"
      + translateExtended ("Replace the KeyCard / Qty =", lvCAREA, "":U) 
      + " " + STRING(res-line.betrieb-gast) + CHR(10). 
  END. 
END.

/*FDL Nov 29, 2024: Ticket */
IF res-mode EQ "inhouse" 
    AND res-line.resstatus EQ 6 AND res-line.zipreis GT 0
    AND (res-line.ankunft EQ res-line.abreise) THEN
DO:
    FIND FIRST bbline WHERE bbline.departement EQ 0
        AND bbline.artnr EQ arrangement.argt-artikelnr
        AND bbline.bill-datum EQ ci-date
        AND bbline.massnr EQ res-line.resnr
        AND bbline.billin-nr EQ res-line.reslinnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE bbline THEN
    DO:
        RUN post-dayuse.p(res-line.resnr, res-line.reslinnr).
    END.        
END.

PROCEDURE static-ratecode-rates:
DEF VARIABLE to-date      AS DATE NO-UNDO.
DEF VARIABLE bill-date    AS DATE NO-UNDO.
DEF VARIABLE curr-zikatnr AS INTEGER NO-UNDO.
DEF VARIABLE early-flag   AS LOGICAL NO-UNDO.
DEF VARIABLE kback-flag   AS LOGICAL NO-UNDO.
DEF VARIABLE rate-found   AS LOGICAL NO-UNDO.
DEF VARIABLE rm-rate      AS DECIMAL NO-UNDO.

    FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
        AND reslin-queasy.resnr = reslin-list.resnr 
        AND reslin-queasy.reslinnr = reslin-list.reslinnr 
        NO-LOCK NO-ERROR.
    
    IF AVAILABLE reslin-queasy THEN 
    DO:    
        RETURN.
    END.
    
    IF reslin-list.ankunft = reslin-list.abreise THEN 
        to-date = reslin-list.abreise.
    ELSE to-date = reslin-list.abreise - 1.
    
    curr-zikatnr = reslin-list.zikatnr.
    IF reslin-list.l-zuordnung[1] NE 0 THEN curr-zikatnr = reslin-list.l-zuordnung[1]. 
/*    
    FIND FIRST arrangement WHERE arrangement.arrangement = reslin-list.arrangement
        NO-LOCK.        
*/
    DO bill-date = reslin-list.ankunft TO to-date:
        RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, reslin-list.resnr, 
          reslin-list.reslinnr, origContcode, ?, bill-date, reslin-list.ankunft,
          reslin-list.abreise, reslin-list.reserve-int, arrangement.argtnr,
          curr-zikatnr, reslin-list.erwachs, reslin-list.kind1, reslin-list.kind2,
          reslin-list.reserve-dec, reslin-list.betriebsnr, OUTPUT rate-found,
          OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
        IF rate-found THEN
        DO:
            CREATE reslin-queasy.
            ASSIGN
              reslin-queasy.key      = "arrangement"
              reslin-queasy.resnr    = reslin-list.resnr
              reslin-queasy.reslinnr = reslin-list.reslinnr
              reslin-queasy.date1    = bill-date 
              reslin-queasy.date2    = bill-date
              reslin-queasy.deci1    = rm-rate
              reslin-queasy.char2    = origContcode
              reslin-queasy.char3    = user-init
            .
        END.
    END.
END.

PROCEDURE min-resplan:
  DEFINE VARIABLE curr-date     AS DATE     NO-UNDO.
  DEFINE VARIABLE beg-datum     AS DATE     NO-UNDO.
  DEFINE VARIABLE i             AS INTEGER  NO-UNDO.
  DEFINE BUFFER rline  FOR res-line.
  DEFINE BUFFER rpbuff FOR resplan.

  FIND FIRST rline WHERE rline.resnr = reslin-list.resnr 
      AND rline.reslinnr = reslin-list.reslinnr NO-LOCK.
  FIND FIRST zimmer WHERE zimmer.zinr = rline.zinr NO-LOCK NO-ERROR.
  if AVAILABLE zimmer AND (not zimmer.sleeping) THEN
  DO:
/* do not update */  
  END.
  ELSE 
  DO:
    i = rline.resstatus.
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = rline.zikatnr NO-LOCK NO-ERROR.
    if res-mode = "inhouse" THEN beg-datum = today.
    ELSE beg-datum = rline.ankunft.
    curr-date = beg-datum.
    DO WHILE curr-date GE beg-datum AND curr-date LT rline.abreise:
      FIND FIRST resplan WHERE resplan.zikatnr = zimkateg.zikatnr
        AND resplan.datum = curr-date NO-LOCK NO-ERROR.
      IF AVAILABLE resplan THEN 
      /* SY 25 March 2016: fixing for 
         'min-resplan mk-resline-gobl.p' Line:444) 
         Lock wait timeout of 1800 seconds expired (8812)  */
      DO TRANSACTION:
          FIND FIRST rpbuff WHERE RECID(rpbuff) = RECID(resplan)
              EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
          IF AVAILABLE rpbuff THEN
          DO:
            rpbuff.anzzim[i] = rpbuff.anzzim[i] - rline.zimmeranz.
              FIND CURRENT rpbuff NO-LOCK.
            RELEASE rpbuff.
          END.
      END.
      curr-date = curr-date + 1.
    END.
  END.
END.

PROCEDURE rmchg-ressharer: 
DEFINE INPUT PARAMETER act-zinr LIKE zimmer.zinr.
DEFINE INPUT PARAMETER new-zinr LIKE zimmer.zinr.
DEFINE INPUT PARAMETER main-nr  AS INTEGER.
DEFINE VARIABLE curr-datum      AS DATE. 
DEFINE BUFFER res-line2         FOR res-line. 
DEFINE BUFFER rline2            FOR res-line. 
DEFINE BUFFER rpbuff            FOR resplan. 

  FIND FIRST res-line2 WHERE res-line2.resnr = reslin-list.resnr
      AND res-line2.kontakt-nr = main-nr AND res-line2.resstatus = 11 
      AND ((res-line2.zinr NE "" AND res-line2.zinr = act-zinr)
      OR  res-line2.zinr EQ "") NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE res-line2:
    IF res-line2.zinr NE "" AND reslin-list.zikatnr NE res-line2.zikatnr THEN 
    DO TRANSACTION:
      /* Rd, #752, 27Mar25, date variable */
      tmpdate = res-line2.abreise - 1. 
      DO curr-datum = res-line2.ankunft TO tmpdate: 
        FIND FIRST resplan WHERE resplan.zikatnr = res-line2.zikatnr 
          AND resplan.datum = curr-datum NO-LOCK NO-ERROR. 
        IF AVAILABLE resplan THEN 
        DO: 
          FIND FIRST rpbuff WHERE RECID(rpbuff) = RECID(resplan) EXCLUSIVE-LOCK.
          IF AVAILABLE rpbuff THEN
          DO:
            rpbuff.anzzim[11] = rpbuff.anzzim[11] - 1. 
            FIND CURRENT rpbuff NO-LOCK.
            RELEASE rpbuff. 
          END.
        END. 

        FIND FIRST resplan WHERE resplan.zikatnr = reslin-list.zikatnr 
          AND resplan.datum = curr-datum NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE resplan THEN 
        DO: 
          CREATE rpbuff. 
          ASSIGN
            rpbuff.datum = curr-datum
            rpbuff.zikatnr = reslin-list.zikatnr
            rpbuff.anzzim[11] = rpbuff.anzzim[11] + 1
          . 
        END.
        ELSE DO:
            FIND FIRST rpbuff WHERE RECID(rpbuff) = RECID(resplan) EXCLUSIVE-LOCK.
            ASSIGN rpbuff.anzzim[11] = rpbuff.anzzim[11] + 1. 
            FIND CURRENT rpbuff NO-LOCK.
            RELEASE rpbuff. 
        END.
      END.
    END.
    
    FIND FIRST zimmer WHERE zimmer.zinr = new-zinr NO-LOCK NO-ERROR.
    DO TRANSACTION:
      FIND FIRST rline2 WHERE RECID(rline2) = RECID(res-line2)
          EXCLUSIVE-LOCK.
      ASSIGN
        rline2.zinr    = new-zinr
        rline2.zikatnr = reslin-list.zikatnr
        rline2.setup   = zimmer.setup NO-ERROR
      .
      FIND CURRENT rline2 NO-LOCK.
      RELEASE rline2.
    END.
    
    FIND NEXT res-line2 WHERE res-line2.resnr = reslin-list.resnr
      AND res-line2.kontakt-nr = main-nr AND res-line2.resstatus = 11 
      AND ((res-line2.zinr NE "" AND res-line2.zinr = act-zinr)
      OR  res-line2.zinr EQ "") NO-LOCK NO-ERROR.
  END.

  /*
  FIND FIRST res-line2 WHERE res-line2.resnr = reslin-list.resnr 
    AND res-line2.zinr NE "" 
    AND res-line2.zinr = act-zinr AND res-line2.resstatus = 11 
    NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE res-line2:
    IF reslin-list.zikatnr NE res-line2.zikatnr THEN 
    DO TRANSACTION:
      DO curr-datum = res-line2.ankunft TO (res-line2.abreise - 1): 
        FIND FIRST resplan WHERE resplan.zikatnr = res-line2.zikatnr 
          AND resplan.datum = curr-datum NO-LOCK NO-ERROR. 
        IF AVAILABLE resplan THEN 
        DO: 
          FIND FIRST rpbuff WHERE RECID(rpbuff) = RECID(resplan)
            EXCLUSIVE-LOCK.
          IF AVAILABLE rpbuff THEN
          DO:
            rpbuff.anzzim[11] = rpbuff.anzzim[11] - 1. 
            FIND CURRENT rpbuff NO-LOCK.
            RELEASE rpbuff. 
          END.
        END. 
        FIND FIRST resplan WHERE resplan.zikatnr = reslin-list.zikatnr 
          AND resplan.datum = curr-datum NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE resplan THEN 
        DO: 
          CREATE rpbuff. 
          ASSIGN
            rpbuff.datum = curr-datum
            rpbuff.zikatnr = reslin-list.zikatnr
          . 
        END.
        ELSE FIND FIRST rpbuff WHERE RECID(rpbuff) = RECID(resplan)
            EXCLUSIVE-LOCK.
        ASSIGN rpbuff.anzzim[11] = rpbuff.anzzim[11] + 1. 
        FIND CURRENT rpbuff NO-LOCK.
        RELEASE rpbuff. 
      END.
    END.
    
    FIND FIRST zimmer WHERE zimmer.zinr = new-zinr NO-LOCK NO-ERROR.
    DO TRANSACTION:
      FIND FIRST rline2 WHERE RECID(rline2) = RECID(res-line2)
          EXCLUSIVE-LOCK.
      ASSIGN
        rline2.zinr    = new-zinr
        rline2.zikatnr = reslin-list.zikatnr
        rline2.setup   = zimmer.setup NO-ERROR
      .
      FIND CURRENT rline2 NO-LOCK.
      RELEASE rline2.
    END.
    
    FIND NEXT res-line2 WHERE res-line2.resnr = reslin-list.resnr 
      AND res-line2.zinr NE "" 
      AND res-line2.zinr = act-zinr AND res-line2.resstatus = 11 
      NO-LOCK NO-ERROR.
  END. */
END. 
 
PROCEDURE rmchg-sharer:
DEFINE INPUT PARAMETER act-zinr LIKE zimmer.zinr.
DEFINE INPUT PARAMETER new-zinr LIKE zimmer.zinr.
DEFINE VARIABLE res-recid1      AS INTEGER.
DEFINE VARIABLE parent-nr       AS INTEGER.
DEFINE VARIABLE curr-datum      AS DATE.
DEFINE VARIABLE beg-datum       AS DATE.
DEFINE VARIABLE end-datum       AS DATE.
DEFINE VARIABLE answer          AS LOGICAL.

DEFINE BUFFER res-line1 FOR res-line.
DEFINE BUFFER res-line2 FOR res-line.
DEFINE BUFFER rline2    FOR res-line.
DEFINE BUFFER new-zkat  FOR zimkateg.
DEFINE BUFFER rpbuff    FOR resplan.
DEFINE BUFFER mbuff     FOR messages.

    FIND FIRST zimmer WHERE zimmer.zinr = new-zinr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE zimmer THEN RETURN.

    FIND FIRST new-zkat WHERE new-zkat.zikatnr = zimmer.zikatnr
      NO-LOCK.

    FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
    ASSIGN
      beg-datum  = htparam.fdate
      end-datum  = beg-datum
      res-recid1 = 0
    .    
    
    FIND FIRST messages WHERE messages.zinr = act-zinr 
        AND messages.resnr = reslin-list.resnr 
        AND messages.reslinnr GE 1 NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE messages:
        FIND FIRST mbuff WHERE RECID(mbuff) = RECID(messages)
            EXCLUSIVE-LOCK.
        mbuff.zinr = new-zinr.
        FIND CURRENT mbuff NO-LOCK.
        RELEASE mbuff.

        FIND NEXT messages WHERE messages.zinr = act-zinr 
            AND messages.resnr = reslin-list.resnr 
            AND messages.reslinnr GE 1 NO-LOCK NO-ERROR.
    END.
    
    FOR EACH res-line1 WHERE res-line1.resnr = resnr
      AND res-line1.zinr = act-zinr AND res-line1.resstatus = 13 
      NO-LOCK:
      if end-datum LE res-line1.abreise THEN 
      ASSIGN
        res-recid1 = RECID(res-line1)
        end-datum  = res-line1.abreise
      .
    END. 

    IF res-line.resstatus = 6  /* this is the res-line from the main guest */
       AND res-recid1 EQ 0 THEN /* there is no room sharers */
    DO:
      FIND FIRST zimmer WHERE zimmer.zinr = act-zinr NO-LOCK NO-ERROR.
      IF AVAILABLE zimmer THEN 
      DO:
          FIND CURRENT zimmer EXCLUSIVE-LOCK.
          zimmer.zistatus = 2.
          FIND CURRENT zimmer NO-LOCK.
          RELEASE zimmer.
      END.
    END.
    
    IF res-line.resstatus = 6  /* this is the res-line from the main guest */
       AND res-recid1 NE 0 THEN /* there is a room sharer */
    DO:
      FIND FIRST res-line1 WHERE RECID(res-line1) = res-recid1 NO-LOCK.
      DO:       
        FIND FIRST res-line2 WHERE res-line2.resnr = reslin-list.resnr
           AND res-line2.zinr = act-zinr AND res-line2.resstatus = 13 
           AND res-line2.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE res-line2:
            IF new-zkat.zikatnr NE res-line2.zikatnr THEN 
            /* Rd, #752, 27Mar25, date variable */
            DO:
              tmpdate = res-line2.abreise - 1.
              DO curr-datum = beg-datum TO tmpdate: 
                  FIND FIRST resplan WHERE resplan.zikatnr = res-line2.zikatnr
                  AND resplan.datum = curr-datum NO-LOCK NO-ERROR.
                  IF AVAILABLE resplan THEN 
                  DO:
                      FIND FIRST rpbuff WHERE RECID(rpbuff) = RECID(resplan)
                          EXCLUSIVE-LOCK.
                      rpbuff.anzzim[13] = rpbuff.anzzim[13] - 1.
                      FIND CURRENT rpbuff NO-LOCK.
                      RELEASE rpbuff.
                  END.
                  FIND FIRST resplan WHERE resplan.zikatnr = new-zkat.zikatnr
                      AND resplan.datum = curr-datum NO-LOCK NO-ERROR.
                  IF NOT AVAILABLE resplan THEN
                  DO:
                      CREATE rpbuff.
                      ASSIGN
                        rpbuff.datum   = curr-datum
                        rpbuff.zikatnr = new-zkat.zikatnr
                      .
                  END.
                  ELSE FIND FIRST rpbuff WHERE RECID(rpbuff) = RECID(resplan)
                      EXCLUSIVE-LOCK.
                  ASSIGN rpbuff.anzzim[13] = rpbuff.anzzim[13] + 1.
                  FIND CURRENT rpbuff NO-LOCK.
                  RELEASE rpbuff.
              END.  
            END.
            
           /*            
           FOR EACH bill WHERE bill.resnr = reslin-list.resnr 
              AND bill.parent-nr = res-line2.reslinnr AND bill.flag = 0
              AND bill.zinr = res-line2.zinr EXCLUSIVE-LOCK:
             bill.zinr = new-zinr.
             RELEASE bill.
           END.
*/
           /* SY 04 June 2016 */           
           FOR EACH bill WHERE bill.resnr = reslin-list.resnr 
             AND bill.parent-nr = res-line2.reslinnr NO-LOCK:
             FIND FIRST bbuff WHERE RECID(bbuff) = RECID(bill)
                 EXCLUSIVE-LOCK.
             bbuff.zinr = new-zinr.
             FIND CURRENT bbuff NO-LOCK.
             RELEASE bbuff.
           END.
          
           FIND FIRST rline2 WHERE RECID(rline2) = RECID(res-line2)
               EXCLUSIVE-LOCK.
           ASSIGN
             rline2.zinr    = new-zinr
             rline2.zikatnr = new-zkat.zikatnr
             rline2.setup   = zimmer.setup
           .
           FIND CURRENT rline2 NO-LOCK.
           RELEASE rline2.
        
           FIND NEXT res-line2 WHERE res-line2.resnr = reslin-list.resnr
              AND res-line2.zinr = act-zinr AND res-line2.resstatus = 13 
              AND res-line2.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
        END.    

        FIND FIRST res-line2 WHERE res-line2.resnr = reslin-list.resnr
            AND res-line2.zinr = act-zinr AND res-line2.resstatus = 12 
            NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE res-line2:
          DO:
            FIND FIRST rline2 WHERE RECID(rline2) = RECID(res-line2)
                EXCLUSIVE-LOCK.
            ASSIGN
              rline2.zinr    = new-zinr
              rline2.zikatnr = new-zkat.zikatnr
              rline2.setup   = zimmer.setup
            .
            FIND CURRENT rline2 NO-LOCK.
            RELEASE rline2.
          END.
          FIND NEXT res-line2 WHERE res-line2.resnr = reslin-list.resnr
              AND res-line2.zinr = act-zinr AND res-line2.resstatus = 12 
              NO-LOCK NO-ERROR.
        END.
            
        FIND FIRST zimmer WHERE zimmer.zinr = act-zinr NO-LOCK NO-ERROR.
        IF AVAILABLE zimmer THEN 
        DO:
            FIND CURRENT zimmer EXCLUSIVE-LOCK.
            zimmer.zistatus = 2.
            FIND CURRENT zimmer NO-LOCK.
            RELEASE zimmer.
        END.
      END.
    END.
END. 

PROCEDURE update-billzinr: 
DEFINE VARIABLE old-zinr  AS CHAR. 
DEFINE VARIABLE new-zinr  AS CHAR. 
DEFINE VARIABLE parent-nr AS INTEGER. 
DEFINE BUFFER resline     FOR res-line. 
  
  IF reslin-list.zipreis GT 0 AND res-line.l-zuordnung[3] = 1 THEN
  DO:
    FIND FIRST bill WHERE bill.resnr = res-line.resnr
      AND bill.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE bill THEN
    DO:
      CREATE bill. 
      ASSIGN 
          bill.flag        = 0 
          bill.billnr      = 1 
          bill.rgdruck     = 1 
          bill.zinr        = reslin-list.zinr 
          bill.gastnr      = reslin-list.gastnrpay 
          bill.resnr       = res-line.resnr 
          bill.reslinnr    = res-line.reslinnr 
          bill.parent-nr   = res-line.reslinnr 
          bill.name        = res-line.NAME 
          bill.kontakt-nr  = bediener.nr 
          bill.segmentcode = reservation.segmentcode
          bill.datum       = ci-date
      .
      FIND FIRST resline WHERE RECID(resline) = RECID(res-line) NO-LOCK NO-ERROR.
      IF AVAILABLE resline THEN DO:
          FIND CURRENT resline EXCLUSIVE-LOCK.
          ASSIGN resline.l-zuordnung[3] = 0.
          FIND CURRENT resline NO-LOCK.
          RELEASE resline.
      END.
    END.
  END.
  old-zinr = res-line.zinr. 
  new-zinr = reslin-list.zinr. 
  IF old-zinr NE new-zinr THEN 
  DO: 
    /*
    FOR EACH bill WHERE bill.resnr = res-line.resnr 
        AND bill.parent-nr = res-line.reslinnr AND bill.flag = 0 
        AND bill.zinr = old-zinr EXCLUSIVE-LOCK: 
*/
/* SY 04 June 2016 */
    FOR EACH bill WHERE bill.resnr = res-line.resnr 
        AND bill.parent-nr = res-line.reslinnr 
        AND bill.flag = 0 NO-LOCK: 
      FIND FIRST bbuff WHERE RECID(bbuff) = RECID(bill)
          EXCLUSIVE-LOCK.
      bbuff.zinr = new-zinr. 
      FIND CURRENT bbuff NO-LOCK.
      RELEASE bbuff.
      FIND FIRST resline WHERE resline.resnr = bill.resnr 
        AND resline.reslinnr = bill.reslinnr NO-LOCK. 
      IF resline.resstatus = 12 /* i.e. res-line FOR additional bill */ 
      THEN DO: 
        FIND CURRENT resline EXCLUSIVE-LOCK. 
        resline.zinr = new-zinr. 
        FIND CURRENT resline NO-LOCK. 
      END. 
    END. 

    IF res-line.active-flag = 1 THEN 
    /*
    FOR EACH bill WHERE bill.resnr = res-line.resnr 
        AND bill.parent-nr = res-line.reslinnr AND bill.flag = 1 
        AND bill.zinr = old-zinr EXCLUSIVE-LOCK: 
*/      
    /* SY 04 June 2016 */
    FOR EACH bill WHERE bill.resnr = res-line.resnr 
        AND bill.parent-nr = res-line.reslinnr AND bill.flag = 1 
        NO-LOCK: 
      FIND FIRST bbuff WHERE RECID(bbuff) = RECID(bill)
          EXCLUSIVE-LOCK.
      bbuff.zinr = new-zinr. 
      FIND CURRENT bbuff NO-LOCK.
      RELEASE bbuff.

      FIND FIRST resline WHERE resline.resnr = bill.resnr 
        AND resline.reslinnr = bill.reslinnr NO-LOCK. 
      IF resline.resstatus = 12 /* i.e. res-line FOR additional bill */ 
      THEN DO: 
        FIND CURRENT resline EXCLUSIVE-LOCK. 
        resline.zinr = new-zinr. 
        FIND CURRENT resline NO-LOCK. 
      END. 
    END. 
  END. 
END. 
 
PROCEDURE check-currency: 
DEFINE buffer waehrung1 FOR waehrung. 

  IF NOT currency-changed THEN RETURN. 
  DO: 
    FIND FIRST guest-pr WHERE guest-pr.gastnr = reslin-list.gastnr 
      NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE guest-pr THEN RETURN. 

    IF marknr NE 0 THEN 
    DO: 
      FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 = marknr 
        NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE queasy OR (AVAILABLE queasy AND queasy.char3 = "") THEN 
      FIND FIRST queasy WHERE queasy.key = 2 AND queasy.char1 = guest-pr.code 
        NO-LOCK NO-ERROR. 
    END. 
    ELSE FIND FIRST queasy WHERE queasy.key = 2 AND queasy.char1 
      = guest-pr.code NO-LOCK NO-ERROR. 
    IF AVAILABLE queasy THEN 
    DO: 

      IF queasy.key = 18 THEN FIND FIRST waehrung1 WHERE waehrung1.wabkurz 
        = queasy.char3 NO-LOCK NO-ERROR. 
      ELSE FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = queasy.number1 
        NO-LOCK NO-ERROR. 

      IF AVAILABLE waehrung1 AND waehrung1.waehrungsnr 
        NE res-line.betriebsnr THEN 
      DO:

        ASSIGN
          waehrungnr          = waehrung1.waehrungsnr
          res-line.betriebsnr = waehrungnr
          reslin-list.betriebsnr = waehrungnr
        . 

        IF reslin-list.reserve-dec NE 0 THEN 
        ASSIGN
          reserve-dec = waehrung1.ankauf / waehrung1.einheit
          res-line.reserve-dec = reserve-dec
          reslin-list.reserve-dec = reserve-dec

        . 
        msg-str = msg-str + CHR(2) + "&W"
          + translateExtended ("No AdHoc Rates found; Currency back to : ", lvCAREA, "":U) 
          + waehrung1.wabkurz + CHR(10).
      END. 
    END.
  END.

  /*FIND FIRST reslin-queasy WHERE key = "arrangement" 
    AND reslin-queasy.resnr = reslin-list.resnr 
    AND reslin-queasy.reslinnr = reslin-list.reslinnr NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE reslin-queasy THEN 
  DO: 
    FIND FIRST guest-pr WHERE guest-pr.gastnr = reslin-list.gastnr 
      NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE guest-pr THEN RETURN. 
    IF marknr NE 0 THEN 
    DO: 
      FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 = marknr 
        NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE queasy OR (AVAILABLE queasy AND queasy.char3 = "") THEN 
      FIND FIRST queasy WHERE queasy.key = 2 AND queasy.char1 = guest-pr.code 
        NO-LOCK NO-ERROR. 
    END. 
    ELSE FIND FIRST queasy WHERE queasy.key = 2 AND queasy.char1 
      = guest-pr.code NO-LOCK NO-ERROR. 
    IF AVAILABLE queasy THEN 
    DO: 
      IF queasy.key = 18 THEN FIND FIRST waehrung1 WHERE waehrung1.wabkurz 
        = queasy.char3 NO-LOCK NO-ERROR. 
      ELSE FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = queasy.number1 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE waehrung1 AND waehrung1.waehrungsnr 
        NE res-line.betriebsnr THEN 
      DO:
        ASSIGN
          waehrungnr          = waehrung1.waehrungsnr
          res-line.betriebsnr = waehrungnr
        . 
        IF reslin-list.reserve-dec NE 0 THEN 
        ASSIGN
          reserve-dec = waehrung1.ankauf / waehrung1.einheit
          res-line.reserve-dec = reserve-dec
        . 
        msg-str = msg-str + CHR(2) + "&W"
          + translateExtended ("No AdHoc Rates found; Currency back to : ", lvCAREA, "":U) 
          + waehrung1.wabkurz + CHR(10).
      END. 
    END. 
  END. */
END. 

PROCEDURE add-keycard: 
DEFINE VARIABLE maxkey AS INTEGER INITIAL 2 NO-UNDO. 
DEFINE VARIABLE errcode AS INTEGER. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE anz0 AS INTEGER. 
DEFINE VARIABLE answer AS LOGICAL INITIAL YES. 
 
  FIND FIRST htparam WHERE paramnr = 926 NO-LOCK. 
  anz0 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 927 NO-LOCK. 
  IF htparam.finteger NE 0 THEN maxkey = htparam.finteger. 
 
  msg-str = msg-str + CHR(2)
    + translateExtended ("The Keycard has been created (Qty =",lvCAREA,"") 
    + " " + STRING(res-line.betrieb-gast) + ") " 
    + translateExtended ("and need to be replaced.",lvCAREA,"") + CHR(10). 
/* 
  DO i = 1 TO res-line.betrieb-gast: 
    IF i = 1 AND res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN 
      RUN keycard.w(res-line.resnr, res-line.reslinnr, "", OUTPUT errcode). 
    ELSE  RUN keycard.w(res-line.resnr, res-line.reslinnr, "cardtype=2", 
      OUTPUT errcode). 
  END.
*/ 
END. 
 
PROCEDURE res-changes: 
DEFINE VARIABLE do-it AS LOGICAL INITIAL NO. 
DEFINE buffer guest1 FOR guest. 
DEFINE VARIABLE cid AS CHAR FORMAT "x(2)" INITIAL "  ". 
DEFINE VARIABLE cdate AS CHAR FORMAT "x(8)" INITIAL "        ". 
DEF VAR heute AS DATE NO-UNDO. 
DEF VAR zeit AS INTEGER NO-UNDO. 
 
  IF res-mode = "new" OR res-mode = "insert" OR res-mode = "qci" THEN 
  DO: 
    RUN res-changes0. 
    RETURN. 
  END. 
 
  IF res-line.ankunft        NE reslin-list.ankunft 
    OR res-line.abreise      NE reslin-list.abreise 
    OR res-line.zimmeranz    NE reslin-list.zimmeranz 
    OR res-line.erwachs      NE reslin-list.erwachs 
    OR res-line.kind1        NE reslin-list.kind1 
    OR res-line.gratis       NE reslin-list.gratis 
    OR res-line.zikatnr      NE reslin-list.zikatnr 
    OR res-line.zinr         NE reslin-list.zinr 
    OR res-line.arrangement  NE reslin-list.arrangement 
    OR res-line.zipreis      NE reslin-list.zipreis 
    OR reslin-list.was-status NE INTEGER(fixed-rate) 
    OR res-line.name         NE guestname 
    OR reservation.bemerk    NE mainres-comment
    OR res-line.bemerk       NE resline-comment
  THEN do-it = YES. 
 
  IF do-it THEN 
  DO: 
    heute = TODAY. 
    zeit = TIME. 
    IF TRIM(res-line.changed-id) NE "" THEN 
    DO: 
      cid = res-line.changed-id. 
      cdate = STRING(res-line.changed). 
    END. 
    ELSE IF LENGTH(res-line.reserve-char) GE 14 THEN    /* created BY */ 
      cid = SUBSTR(res-line.reserve-char,14). 
 
    CREATE reslin-queasy.
    ASSIGN
      reslin-queasy.key = "ResChanges"
      reslin-queasy.resnr = reslin-list.resnr
      reslin-queasy.reslinnr = reslin-list.reslinnr
      reslin-queasy.date2 = heute
      reslin-queasy.number2 = zeit. 
    . 
    IF earlyci THEN reslin-queasy.number1 = 1. 
 
    reslin-queasy.char3 = STRING(res-line.ankunft) + ";" 
                        + STRING(reslin-list.ankunft) + ";" 
                        + STRING(res-line.abreise) + ";" 
                        + STRING(reslin-list.abreise) + ";" 
                        + STRING(res-line.zimmeranz) + ";" 
                        + STRING(reslin-list.zimmeranz) + ";" 
                        + STRING(res-line.erwachs) + ";" 
                        + STRING(reslin-list.erwachs) + ";" 
                        + STRING(res-line.kind1) + ";" 
                        + STRING(reslin-list.kind1) + ";" 
                        + STRING(res-line.gratis) + ";" 
                        + STRING(reslin-list.gratis) + ";" 
                        + STRING(res-line.zikatnr) + ";" 
                        + STRING(reslin-list.zikatnr) + ";" 
                        + STRING(res-line.zinr) + ";" 
                        + STRING(reslin-list.zinr) + ";". 

    IF reslin-list.reserve-int = res-line.reserve-int THEN 
    reslin-queasy.char3 = reslin-queasy.char3 
                        + STRING(res-line.arrangement) + ";" 
                        + STRING(reslin-list.arrangement) + ";". 
    ELSE 
    reslin-queasy.char3 = reslin-queasy.char3 
                        + STRING(res-line.arrangement) + ";" 
                        + STRING(res-line.reserve-int) + ";".

    reslin-queasy.char3 = reslin-queasy.char3 
                        + STRING(res-line.zipreis) + ";" 
                        + STRING(reslin-list.zipreis) + ";"
                        + STRING(cid) + ";" 
                        + STRING(user-init) + ";" 
                        + STRING(cdate, "x(8)") + ";" 
                        + STRING(heute) + ";" 
                        + STRING(res-line.NAME) + ";" 
                        + STRING(guestname) + ";". 
    IF reslin-list.was-status = 0 THEN 
      reslin-queasy.char3 = reslin-queasy.char3 + STRING("NO", "x(3)") + ";". 
    ELSE reslin-queasy.char3 = reslin-queasy.char3 + STRING("YES", "x(3)") + ";". 
    IF NOT fixed-rate THEN 
      reslin-queasy.char3 = reslin-queasy.char3 + STRING("NO", "x(3)") + ";". 
    ELSE reslin-queasy.char3 = reslin-queasy.char3 + STRING("YES", "x(3)") + ";". 
  
    FIND CURRENT reslin-queasy NO-LOCK.
    RELEASE reslin-queasy. 
 
    IF (reservation.bemerk NE mainres-comment) OR 
       (res-line.bemerk NE resline-comment) THEN
    DO: 
        CREATE res-history. 
        ASSIGN 
            res-history.nr = bediener.nr 
            res-history.resnr = res-line.resnr 
            res-history.reslinnr = res-line.reslinnr 
            res-history.datum = heute 
            res-history.zeit = zeit 
            res-history.aenderung = res-line.bemerk 
            res-history.action = "Remark". 
 
        res-history.aenderung = STRING(res-line.resnr, ">>>>>>>9") + "-" + reservation.bemerk + CHR(10) 
            + res-line.bemerk + CHR(10) + CHR(10) 
            + "*** Changed to:" + CHR(10) + CHR(10) 
            + mainres-comment + CHR(10) + resline-comment. 
 
        IF AVAILABLE bediener THEN res-history.betriebsnr = bediener.nr. 
        RELEASE res-history. 
    END. 
 
  END. 
END. 
 
PROCEDURE res-changes0: 
DEFINE buffer guest1 FOR guest. 
DEFINE VARIABLE cid AS CHAR FORMAT "x(2)" INITIAL "  ". 
DEFINE VARIABLE cdate AS CHAR FORMAT "x(8)" INITIAL "        ". 
  CREATE reslin-queasy. 
  ASSIGN
    reslin-queasy.key = "ResChanges"
    reslin-queasy.resnr = reslin-list.resnr 
    reslin-queasy.reslinnr = reslin-list.reslinnr 
    reslin-queasy.date2 = TODAY 
    reslin-queasy.number2 = TIME
  . 
  reslin-queasy.char3 = STRING(reslin-list.ankunft) + ";" 
                        + STRING(reslin-list.ankunft) + ";" 
                        + STRING(reslin-list.abreise) + ";" 
                        + STRING(reslin-list.abreise) + ";" 
                        + STRING(reslin-list.zimmeranz) + ";" 
                        + STRING(reslin-list.zimmeranz) + ";" 
                        + STRING(reslin-list.erwachs) + ";" 
                        + STRING(reslin-list.erwachs) + ";" 
                        + STRING(reslin-list.kind1) + ";" 
                        + STRING(reslin-list.kind1) + ";" 
                        + STRING(reslin-list.gratis) + ";" 
                        + STRING(reslin-list.gratis) + ";" 
                        + STRING(reslin-list.zikatnr) + ";" 
                        + STRING(reslin-list.zikatnr) + ";" 
                        + STRING(reslin-list.zinr) + ";" 
                        + STRING(reslin-list.zinr) + ";" 
                        + STRING(reslin-list.arrangement) + ";" 
                        + STRING(reslin-list.arrangement) + ";"
                        + STRING(reslin-list.zipreis) + ";" 
                        + STRING(reslin-list.zipreis) + ";"
                        + STRING(user-init) + ";" 
                        + STRING(user-init) + ";" 
                        + STRING(TODAY) + ";" 
                        + STRING(TODAY) + ";" 
                        + STRING(reslin-list.NAME) + ";" 
                        + STRING("New Reservation") + ";". 
  IF reslin-list.was-status = 0 THEN 
    reslin-queasy.char3 = reslin-queasy.char3 + STRING("NO") + ";". 
  ELSE reslin-queasy.char3 = reslin-queasy.char3 + STRING("YES") + ";". 
 
  IF NOT fixed-rate THEN 
    reslin-queasy.char3 = reslin-queasy.char3 + STRING("NO") + ";". 
  ELSE reslin-queasy.char3 = reslin-queasy.char3 + STRING("YES") + ";". 
 
  FIND CURRENT reslin-queasy NO-LOCK.
  RELEASE reslin-queasy. 
 
END. 

PROCEDURE add-resplan:
  DEFINE VARIABLE curr-date AS DATE.
  DEFINE VARIABLE beg-datum AS DATE.
  DEFINE VARIABLE end-datum AS DATE.
  DEFINE VARIABLE i         AS INTEGER.
  DEFINE VARIABLE anz       AS INTEGER.
  
  DEFINE BUFFER rline       FOR res-line.
  DEFINE BUFFER rpbuff      FOR resplan.

  FIND FIRST rline WHERE rline.resnr = reslin-list.resnr 
    AND rline.reslinnr = reslin-list.reslinnr NO-LOCK.
  FIND FIRST zimmer WHERE zimmer.zinr = rline.zinr NO-LOCK NO-ERROR.
  if AVAILABLE zimmer AND (not zimmer.sleeping) THEN
  DO:
/* do not update */  
  END.
  ELSE DO:
    i = rline.resstatus.
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = rline.zikatnr NO-LOCK NO-ERROR.
    if res-mode = "inhouse" THEN beg-datum = today.
    ELSE beg-datum = rline.ankunft.
    ASSIGN
      end-datum = rline.abreise - 1
      curr-date = beg-datum
    .
    DO curr-date = beg-datum TO end-datum:
      FIND FIRST resplan WHERE resplan.zikatnr = zimkateg.zikatnr
        AND resplan.datum = curr-date NO-LOCK NO-ERROR.
      IF NOT AVAILABLE resplan THEN
      DO:
        CREATE rpbuff.
        ASSIGN  
          rpbuff.datum   = curr-date
          rpbuff.zikatnr = zimkateg.zikatnr
          rpbuff.anzzim[i] = rpbuff.anzzim[i] + rline.zimmeranz
        .
      END.
      ELSE DO: 
          FIND FIRST rpbuff WHERE RECID(rpbuff) = RECID(resplan) EXCLUSIVE-LOCK.
          ASSIGN rpbuff.anzzim[i] = rpbuff.anzzim[i] + rline.zimmeranz.
          FIND CURRENT rpbuff NO-LOCK.
          RELEASE rpbuff.
      END.      
    END.
  END.
END.

PROCEDURE update-mainres:
DEFINE VARIABLE ct      AS CHAR                 NO-UNDO. 
DEFINE VARIABLE answer  AS LOGICAL INITIAL YES  NO-UNDO.
DEFINE VARIABLE l-grpnr AS INTEGER              NO-UNDO.
DEFINE VARIABLE source-code AS CHARACTER        NO-UNDO.
DEFINE BUFFER rline     FOR res-line. 
DEFINE BUFFER rgast     FOR guest.
    
/* must be here */  
  FIND CURRENT reservation EXCLUSIVE-LOCK.
  ASSIGN reservation.bemerk = mainres-comment.

  IF NOT group-enable THEN RETURN.

  FIND FIRST htparam WHERE htparam.paramnr = 440 NO-LOCK. 
  l-grpnr = htparam.finteger. 

  FIND FIRST rgast WHERE rgast.gastnr = reslin-list.gastnr NO-LOCK.
  FIND FIRST master WHERE master.resnr = reslin-list.resnr 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE master AND master.active THEN reservation.verstat = 1. 
  ELSE reservation.verstat = 0. 
  IF res-mode = "new" OR res-mode = "qci" 
      THEN reservation.useridanlage = user-init. 
 
  ct = letter-svalue.
  FIND FIRST brief WHERE brief.briefkateg = l-grpnr 
    AND brief.briefnr = INTEGER(SUBSTR(ct, 1, INDEX(ct," "))) NO-LOCK NO-ERROR. 
  IF AVAILABLE brief THEN reservation.briefnr = brief.briefnr. 
  ELSE reservation.briefnr = 0.

  ct = segm-svalue.

  /*ITA 030119 --> log if the change of segment*/
  IF INTEGER(SUBSTR(ct, 1, INDEX(ct," "))) NE reservation.segmentcode THEN DO:
      FIND FIRST segment WHERE segment.segmentcode = INTEGER(SUBSTR(ct, 1, INDEX(ct," "))) NO-LOCK NO-ERROR.
      CREATE res-history. 
      ASSIGN 
            res-history.nr = bediener.nr 
            res-history.resnr = res-line.resnr 
            res-history.reslinnr = res-line.reslinnr 
            res-history.datum = TODAY
            res-history.zeit = TIME
            res-history.action  = "Segment" 
            /*res-history.aenderung = "Segment has been changed to " + segment.bezeich.*/
           res-history.aenderung = "Reservation " + STRING(reservation.resnr) + ", Segment has been changed from " + 
                                    temp-segment + " to " + segment.bezeich.
  END.
    
  FIND FIRST segment WHERE segment.segmentcode =
      INTEGER(SUBSTR(ct, 1, INDEX(ct," "))) NO-LOCK NO-ERROR.
  IF AVAILABLE segment THEN reservation.segmentcode = segment.segmentcode.
  
  ct = source-svalue.

  /*FD August 05, 2021 => log if the change of source*/      
  FIND FIRST sourccod WHERE sourccod.source-code EQ reservation.resart NO-LOCK NO-ERROR.
  IF AVAILABLE sourccod THEN source-code = sourccod.bezeich.

  IF INTEGER(SUBSTR(ct, 1, INDEX(ct," "))) NE reservation.resart THEN 
  DO:          
      FIND FIRST sourccod WHERE sourccod.source-code EQ INTEGER(SUBSTR(ct, 1, INDEX(ct," "))) 
          NO-LOCK NO-ERROR.
      CREATE res-history. 
      ASSIGN 
        res-history.nr        = bediener.nr 
        res-history.resnr     = res-line.resnr 
        res-history.reslinnr  = res-line.reslinnr 
        res-history.datum     = TODAY
        res-history.zeit      = TIME
        res-history.action    = "Source" 
        res-history.aenderung = "Source has been changed from: " + CAPS(source-code) + " to: "
                            + CAPS(sourccod.bezeich) + "  ResNo: " + STRING(res-line.resnr)
                            + " - " + STRING(res-line.reslinnr).
  END.  
  /*End FD*/

  FIND FIRST sourccod WHERE sourccod.source-code =
      INTEGER(SUBSTR(ct, 1, INDEX(ct," "))) NO-LOCK NO-ERROR.
  IF AVAILABLE sourccod THEN reservation.resart = sourccod.source-code. 

  /* Dzikri A89D6D - Reservation deposit log */
  IF reservation.depositgef NE deposit THEN
  DO:
    FIND FIRST res-history WHERE res-history.action EQ "Reservation Deposit"
      AND res-history.resnr     EQ res-line.resnr 
      AND res-history.reslinnr  EQ res-line.reslinnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE res-history AND reservation.depositgef EQ 0 THEN
    DO:
      CREATE res-history. 
      ASSIGN 
        res-history.nr        = bediener.nr 
        res-history.resnr     = res-line.resnr 
        res-history.reslinnr  = res-line.reslinnr 
        res-history.datum     = TODAY
        res-history.zeit      = TIME
        res-history.action    = "Reservation Deposit" 
        res-history.aenderung = "Reservation Deposit has been created: " + TRIM(STRING(deposit,"->>>,>>>,>>>,>>>,>>9.99")) 
                            + "  ResNo: " + STRING(res-line.resnr)
                            + "/" + STRING(res-line.reslinnr,"999")
                            + " - Name: " + STRING(res-line.NAME)
      .
    END.
    ELSE
    DO:
      CREATE res-history. 
      ASSIGN 
        res-history.nr        = bediener.nr 
        res-history.resnr     = res-line.resnr 
        res-history.reslinnr  = res-line.reslinnr 
        res-history.datum     = TODAY
        res-history.zeit      = TIME
        res-history.action    = "Reservation Deposit" 
        res-history.aenderung = "Reservation Deposit has been changed from: " + TRIM(STRING(reservation.depositgef,"->>>,>>>,>>>,>>>,>>9.99")) + " to: "
                            + TRIM(STRING(deposit,"->>>,>>>,>>>,>>>,>>9.99")) + "  ResNo: " + STRING(res-line.resnr)
                            + "/" + STRING(res-line.reslinnr,"999")
                            + " - Name: " + STRING(res-line.NAME)
      .
    END.
  END.
  /* Dzikri A89D6D - END */
  
  ASSIGN 
      reservation.groupname   = groupname 
      reservation.grpflag     = (groupname NE "") 
      reservation.limitdate   = limitdate 
      reservation.depositgef  = deposit 
      reservation.vesrdepot   = main-voucher 
      reservation.kontakt-nr  = contact-nr
      reservation.point-resnr = cutoff-days
  . 
  IF (reservation.insurance AND NOT init-fixrate) 
    OR (NOT reservation.insurance AND init-fixrate) THEN
  DO:
    ASSIGN reservation.insurance = init-fixrate.
    RUN resline-reserve-dec. 
  END.

  IF reservation.grpflag THEN 
  DO: 
    FIND FIRST rline WHERE rline.resnr = reservation.resnr 
      NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE rline: 
      FIND CURRENT rline EXCLUSIVE-LOCK. 
      rline.grpflag = YES. 
      FIND CURRENT rline NO-LOCK. 
      FIND NEXT rline WHERE rline.resnr = reservation.resnr 
        NO-LOCK NO-ERROR. 
    END. 
  END. 
  
  IF AVAILABLE master THEN 
  DO: 
    FIND CURRENT master EXCLUSIVE-LOCK. 
    IF NOT master.active THEN 
    DO: 
      FIND FIRST bill WHERE bill.resnr = reslin-list.resnr 
        AND bill.reslinnr = 0 NO-LOCK NO-ERROR. 
      IF AVAILABLE bill AND bill.saldo NE 0 THEN master.active = YES. 
    END.  
    FIND CURRENT master NO-LOCK. 
    IF master.active THEN reservation.verstat = 1. 
    ELSE reservation.verstat = 0. 
 
/* create master bill only IF resident guest exists !! ******/ 
    FIND FIRST rline WHERE rline.resnr = master.resnr 
      AND rline.active-flag = 1 NO-LOCK NO-ERROR. 
    IF AVAILABLE rline THEN 
    DO: 
      FIND FIRST bill WHERE bill.resnr = reslin-list.resnr 
        AND bill.reslinnr = 0 EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE bill THEN 
      DO: 
        CREATE bill. 
        ASSIGN
          bill.resnr    = reslin-list.resnr 
          bill.reslinnr = 0 
          bill.rgdruck  = 1 
          bill.billtyp  = 2
        . 
        IF master.rechnr NE 0 THEN bill.rechnr = master.rechnr. 
        ELSE 
        DO: 
          FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK. 
          counters.counter = counters.counter + 1. 
          bill.rechnr = counters.counter. 
          FIND CURRENT counter NO-LOCK. 
          FIND CURRENT master EXCLUSIVE-LOCK. 
          master.rechnr = bill.rechnr. 
          FIND CURRENT master NO-LOCK. 
        END. 
      END.
      ASSIGN
        bill.gastnr      = reslin-list.gastnr 
        bill.name        = rgast.NAME 
        bill.segmentcode = reservation.segmentcode
      . 
      FIND CURRENT bill NO-LOCK. 

      /*FDL Jan 10, 2024 => Ticket 1DBBEB => Validation Double Bill*/
      FIND FIRST buff-bill WHERE buff-bill.rechnr EQ bill.rechnr
          AND buff-bill.resnr EQ 0 AND buff-bill.reslinnr EQ 1
          AND buff-bill.billtyp NE 2 NO-LOCK NO-ERROR.
      IF AVAILABLE buff-bill THEN
      DO:
          /*FDL Debug
          MESSAGE 
              "MK-RESLINE-GO_2BL" SKIP
              "Origin Bill: " bill.rechnr SKIP
              "Double Bill Number: " STRING(buff-bill.rechnr)
              VIEW-AS ALERT-BOX INFO BUTTONS OK.
			*/
          FIND CURRENT buff-bill EXCLUSIVE-LOCK.
          DELETE buff-bill.
          RELEASE buff-bill.
      END.
    END.                      
  END.   

  IF NOT AVAILABLE master AND (rgast.karteityp = 1 OR rgast.karteityp = 2) 
      AND res-mode NE "qci" 
      AND rgast.gastnr NE ind-gastnr
      AND rgast.gastnr NE wig-gastnr THEN 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = 166 NO-LOCK. 
    IF htparam.flogical THEN 
    ASSIGN 
      msg-str = msg-str + CHR(2) + "&Q"
        + translateExtended ("Master Bill does not exist, CREATE IT?",lvCAREA,"") 
        + CHR(10).
  END. 
END. 

PROCEDURE update-resline: 
DEF VARIABLE hh                 AS INTEGER              NO-UNDO. 
DEF VARIABLE mm                 AS INTEGER              NO-UNDO. 
DEF VARIABLE n                  AS INTEGER              NO-UNDO.
DEF VARIABLE st                 AS CHAR                 NO-UNDO.
DEF VARIABLE ct                 AS CHAR INITIAL ""      NO-UNDO.
DEF VARIABLE memoRmNo           AS CHAR INITIAL ""      NO-UNDO.
DEF VARIABLE datum              AS DATE                 NO-UNDO.
DEF VARIABLE curr-zikatnr       AS INTEGER              NO-UNDO. 
DEF VARIABLE rate-found         AS LOGICAL INITIAL NO   NO-UNDO. 
DEF VARIABLE early-flag         AS LOGICAL              NO-UNDO.
DEF VARIABLE kback-flag         AS LOGICAL              NO-UNDO.
DEF VARIABLE rmrate             AS DECIMAL INITIAL ?    NO-UNDO.

DEF BUFFER qsy                  FOR queasy. 
DEF BUFFER resline              FOR res-line. 
DEF BUFFER rline                FOR res-line. 
DEF BUFFER accguest             FOR guest.

/* 19 aug 2009 for VHP online need, send guaranted email to guest */
  IF res-mode = "modify" AND res-line.resstatus = 3 AND 
      (reslin-list.resstatus LE 2 OR reslin-list.resstatus = 5) THEN
     RUN check-vhpOnline-conf-email.
  
  IF accompany-gastnr GT 0 OR accompany-tmpnr[1] GT 0 THEN
  DO:
    FIND FIRST resline WHERE resline.resnr = res-line.resnr
      AND resline.active-flag LE 1 
      AND resline.kontakt-nr = res-line.reslinnr
      AND resline.gastnrmember = accompany-gastnr
      AND resline.l-zuordnung[3] = 1 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE resline THEN
    DO:
      FOR EACH resline WHERE resline.resnr = res-line.resnr NO-LOCK: 
        IF resline.reslinnr GT max-resline THEN max-resline = resline.reslinnr. 
      END. 
      max-resline = max-resline + 1.
      IF accompany-gastnr GT 0 THEN
        FIND FIRST accguest WHERE accguest.gastnr = accompany-gastnr NO-LOCK.
      ELSE FIND FIRST accguest WHERE accguest.gastnr = accompany-tmpnr[1] NO-LOCK.
      CREATE resline.
      ASSIGN 
        resline.resnr          = reslin-list.resnr
        resline.reslinnr       = max-resline
        resline.gastnr         = reslin-list.gastnr
        resline.gastnrpay      = accompany-gastnr
        resline.gastnrmember   = accompany-gastnr
        resline.erwachs        = 0
        resline.zimmeranz      = 1
        resline.l-zuordnung[3] = 1
        resline.kontakt-nr     = reslin-list.reslinnr
        resline.NAME           = accguest.NAME + ", " + accguest.vorname1
                               + ", " + accguest.anrede1
        resline.reserve-char   = STRING(YEAR(TODAY) - 2000,"99") + "/" 
                               + STRING(MONTH(TODAY),"99")       + "/"
                               + STRING(DAY(TODAY),"99")
                               + STRING(TIME,"HH:MM") + user-init
      .
      
      IF accompany-gastnr = 0 THEN
      ASSIGN
        resline.gastnrpay      = accompany-tmpnr[1]
        resline.gastnrmember   = accompany-tmpnr[1]
      .
      
      IF res-mode = "inhouse" THEN 
      ASSIGN
          resline.cancelled-id = user-init
          resline.ankzeit = TIME
          resline.resstatus = 13.
      ELSE resline.resstatus = 11.
      FIND CURRENT resline NO-LOCK.
      RUN accompany-vip.
    END.
    ELSE IF (resline.gastnrmember NE accompany-tmpnr[1])
      AND (accompany-tmpnr[1] GT 0) THEN
    DO:
      FIND FIRST accguest WHERE accguest.gastnr = accompany-tmpnr[1] NO-LOCK.
      FIND CURRENT resline EXCLUSIVE-LOCK.
      ASSIGN
        resline.NAME           = accguest.NAME + ", " + accguest.vorname1
                               + ", " + accguest.anrede1
        resline.gastnrpay      = accompany-tmpnr[1]
        resline.gastnrmember   = accompany-tmpnr[1].
      RUN accompany-vip.
      FIND CURRENT resline NO-LOCK.
    END.
  END.

  IF accompany-gastnr2 GT 0 OR accompany-tmpnr[2] GT 0 THEN
  DO:
    FIND FIRST resline WHERE resline.resnr = res-line.resnr
      AND resline.active-flag LE 1 
      AND resline.kontakt-nr = res-line.reslinnr
      AND resline.gastnrmember = accompany-gastnr2
      AND resline.l-zuordnung[3] = 1 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE resline THEN
    DO:
      FOR EACH resline WHERE resline.resnr = res-line.resnr NO-LOCK: 
        IF resline.reslinnr GT max-resline THEN max-resline = resline.reslinnr. 
      END. 
      max-resline = max-resline + 1.
      IF accompany-gastnr2 GT 0 THEN
        FIND FIRST accguest WHERE accguest.gastnr = accompany-gastnr2 NO-LOCK.
      ELSE FIND FIRST accguest WHERE accguest.gastnr = accompany-tmpnr[2] NO-LOCK.
      CREATE resline.
      ASSIGN 
        resline.resnr          = reslin-list.resnr
        resline.reslinnr       = max-resline
        resline.gastnr         = reslin-list.gastnr
        resline.gastnrpay      = accompany-gastnr2
        resline.gastnrmember   = accompany-gastnr2
        resline.erwachs        = 0
        resline.zimmeranz      = 1
        resline.l-zuordnung[3] = 1
        resline.kontakt-nr     = reslin-list.reslinnr
        resline.NAME           = accguest.NAME + ", " + accguest.vorname1
                               + ", " + accguest.anrede1
        resline.reserve-char   = STRING(YEAR(TODAY) - 2000,"99") + "/" 
                               + STRING(MONTH(TODAY),"99")       + "/"
                               + STRING(DAY(TODAY),"99")
                               + STRING(TIME,"HH:MM") + user-init
      .
      
      IF accompany-gastnr2 = 0 THEN
      ASSIGN
        resline.gastnrpay      = accompany-tmpnr[2]
        resline.gastnrmember   = accompany-tmpnr[2]
      .

      IF res-mode = "inhouse" THEN 
      ASSIGN
          resline.cancelled-id = user-init
          resline.ankzeit = TIME
          resline.resstatus = 13.
      ELSE resline.resstatus = 11.
      RUN accompany-vip.
      FIND CURRENT resline NO-LOCK.
    END.
    ELSE IF (resline.gastnrmember NE accompany-tmpnr[2])
      AND (accompany-tmpnr[2] GT 0) THEN
    DO:                                              
      FIND FIRST accguest WHERE accguest.gastnr = accompany-tmpnr[2] NO-LOCK.
      FIND CURRENT resline EXCLUSIVE-LOCK.
      ASSIGN
        resline.NAME           = accguest.NAME + ", " + accguest.vorname1
                               + ", " + accguest.anrede1
        resline.gastnrpay      = accompany-tmpnr[2]
        resline.gastnrmember   = accompany-tmpnr[2].
      RUN accompany-vip.
      FIND CURRENT resline NO-LOCK.
    END.
  END.

  IF accompany-gastnr3 GT 0 OR accompany-tmpnr[3] GT 0 THEN
  DO:
    FIND FIRST resline WHERE resline.resnr = res-line.resnr
      AND resline.active-flag LE 1 
      AND resline.kontakt-nr = res-line.reslinnr
      AND resline.gastnrmember = accompany-gastnr3
      AND resline.l-zuordnung[3] = 1 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE resline THEN
    DO:
      FOR EACH resline WHERE resline.resnr = res-line.resnr NO-LOCK: 
        IF resline.reslinnr GT max-resline THEN max-resline = resline.reslinnr. 
      END. 
      max-resline = max-resline + 1.
      IF accompany-gastnr3 GT 0 THEN
        FIND FIRST accguest WHERE accguest.gastnr = accompany-gastnr3 NO-LOCK.
      ELSE FIND FIRST accguest WHERE accguest.gastnr = accompany-tmpnr[3] NO-LOCK.
      CREATE resline.
      ASSIGN 
        resline.resnr          = reslin-list.resnr
        resline.reslinnr       = max-resline
        resline.gastnr         = reslin-list.gastnr
        resline.gastnrpay      = accompany-gastnr3
        resline.gastnrmember   = accompany-gastnr3
        resline.erwachs        = 0
        resline.zimmeranz      = 1
        resline.l-zuordnung[3] = 1
        resline.kontakt-nr     = reslin-list.reslinnr
        resline.NAME           = accguest.NAME + ", " + accguest.vorname1
                               + ", " + accguest.anrede1
        resline.reserve-char   = STRING(YEAR(TODAY) - 2000,"99") + "/" 
                               + STRING(MONTH(TODAY),"99")       + "/"
                               + STRING(DAY(TODAY),"99")
                               + STRING(TIME,"HH:MM") + user-init
      .
      
      IF accompany-gastnr3 = 0 THEN
      ASSIGN
        resline.gastnrpay      = accompany-tmpnr[3]
        resline.gastnrmember   = accompany-tmpnr[3]
      .
      
      IF res-mode = "inhouse" THEN 
      ASSIGN
          resline.cancelled-id = user-init
          resline.ankzeit = TIME
          resline.resstatus = 13.
      ELSE resline.resstatus = 11.
      RUN accompany-vip.
      FIND CURRENT resline NO-LOCK.
    END.
    ELSE IF (resline.gastnrmember NE accompany-tmpnr[3])
      AND (accompany-tmpnr[3] GT 0) THEN
    DO:
      FIND FIRST accguest WHERE accguest.gastnr = accompany-tmpnr[3] NO-LOCK.
      FIND CURRENT resline EXCLUSIVE-LOCK.
      ASSIGN
        resline.NAME           = accguest.NAME + ", " + accguest.vorname1
                               + ", " + accguest.anrede1
        resline.gastnrpay      = accompany-tmpnr[3]
        resline.gastnrmember   = accompany-tmpnr[3].
      RUN accompany-vip.
      FIND CURRENT resline NO-LOCK.
    END.
  END.

  FIND FIRST rline WHERE rline.resnr = reslin-list.resnr
    AND rline.l-zuordnung[3] = 1
    AND rline.kontakt-nr     = reslin-list.reslinnr NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE rline:
    FIND FIRST resline WHERE RECID(resline) = RECID(rline) EXCLUSIVE-LOCK.
    ASSIGN
        resline.gastnrpay    = reslin-list.gastnrpay
        resline.ankunft      = reslin-list.ankunft
        resline.abreise      = reslin-list.abreise
        resline.anztage      = reslin-list.anztage 
        resline.zikatnr      = reslin-list.zikatnr
        resline.zinr         = reslin-list.zinr
        resline.arrangement  = reslin-list.arrangement 
        resline.grpflag      = grpflag
        resline.reserve-int  = reslin-list.reserve-int 
        resline.setup        = reslin-list.setup
        resline.active-flag  = reslin-list.active-flag 
        resline.adrflag      = reslin-list.adrflag  /* YES -> rate IN local currency */ 
        resline.betriebsnr   = reslin-list.betriebsnr 
        resline.code         = STRING(bill-instruct) 
        resline.changed      = ci-date
        resline.changed-id   = user-init
    .
    FIND CURRENT resline NO-LOCK.
    FIND NEXT rline WHERE rline.resnr = reslin-list.resnr
      AND rline.l-zuordnung[3] = 1
      AND rline.kontakt-nr     = reslin-list.reslinnr NO-LOCK NO-ERROR.
  END.

  IF purpose-svalue NE "" THEN
  DO:
    FIND FIRST queasy WHERE queasy.KEY = 143 AND queasy.char1 =
        ENTRY(1, purpose-svalue, " ") NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN ASSIGN segm_purcode = queasy.number1.
  END.

  ct = "".
  IF pickup-flag THEN ct = ct + "pickup;".
  IF drop-flag   THEN ct = ct + "drop-passanger;".
  IF ebdisc-flag THEN ct = ct + "ebdisc;".
  IF kbdisc-flag THEN ct = ct + "kbdisc;".
  
  /*ITA 121218*/
  DEFINE VARIABLE do-it AS LOGICAL NO-UNDO.
  IF gdpr-flag THEN ct = ct + "GDPRyes;".
  ELSE IF NOT gdpr-flag THEN DO:
      IF avail-gdpr THEN DO:
          FIND FIRST guest WHERE guest.gastnr = reslin-list.gastnrmember NO-LOCK NO-ERROR.
          IF AVAILABLE guest THEN DO: /*kalo guestnya dari negara EU*/
              
              FIND FIRST mc-guest WHERE mc-guest.gastnr = reslin-list.gastnrmember NO-LOCK NO-ERROR.
              IF AVAILABLE mc-guest THEN ASSIGN do-it = NO.
              ELSE ASSIGN do-it = YES.

              
              IF do-it = YES THEN DO:
                  IF guest.land NE " " THEN DO: 
                      ASSIGN curr-nat = guest.land.
                      FIND FIRST nation-list WHERE nation-list.kurzbez = curr-nat NO-LOCK NO-ERROR.
                      IF AVAILABLE nation-list THEN do-it = YES.
                      ELSE do-it = NO.
                  END.
                  
                  IF do-it = NO THEN DO:
                      IF guest.nation1 NE " " THEN ASSIGN curr-nat = guest.nation1.
                      FIND FIRST nation-list WHERE nation-list.kurzbez = curr-nat NO-LOCK NO-ERROR.
                      IF AVAILABLE nation-list THEN do-it = YES.
                      ELSE do-it = NO.
                  END.
              END.
              
              
              IF do-it THEN DO:
                  IF NOT reslin-list.zimmer-wunsch MATCHES "*GDPR*" THEN DO:
                      ct = ct + "GDPRyes;".
                  END.
                  ELSE IF reslin-list.zimmer-wunsch MATCHES "*GDPRyes*" THEN DO:
                      ct = ct + "GDPRno;".
                  END.
              END.
              ELSE IF do-it = NO THEN DO:
                ct = ct + "GDPRno;".
              END.
          END.
      END.
      ELSE DO:
          IF reslin-list.zimmer-wunsch MATCHES "*GDPRyes*" THEN DO:
              ct = ct + "GDPRno;".
          END.
      END.
  END.
  /*end*/

  IF NOT gdpr-flag AND res-line.zimmer-wunsch MATCHES("*GDPRyes*") THEN
  DO:
    CREATE res-history. 
    ASSIGN 
        res-history.nr          = bediener.nr 
        res-history.resnr       = res-line.resnr 
        res-history.reslinnr    = res-line.reslinnr 
        res-history.datum       = TODAY
        res-history.zeit        = TIME
        res-history.action      = "GDPR". 
        res-history.aenderung   = "GDPR has been removed in reservation No " 
                                  + STRING(res-line.resnr) + "-" + STRING(res-line.reslinnr)
    .
  END.

  IF gdpr-flag AND (res-line.zimmer-wunsch MATCHES("*GDPRno*")
                    OR NOT res-line.zimmer-wunsch MATCHES("*GDPR*")) THEN
  DO:
    CREATE res-history. 
    ASSIGN 
        res-history.nr          = bediener.nr 
        res-history.resnr       = res-line.resnr 
        res-history.reslinnr    = res-line.reslinnr 
        res-history.datum       = TODAY
        res-history.zeit        = TIME
        res-history.action      = "GDPR". 
        res-history.aenderung   = "GDPR has been created in reservation No " 
                                  + STRING(res-line.resnr) + "-" + STRING(res-line.reslinnr)
    .
  END.


  /*gerald Req Tauzia 14/12/20*/
  IF mark-flag = YES THEN ct = ct + "MARKETINGyes;".
  ELSE IF mark-flag = NO THEN ct = ct + "MARKETINGno;".

  IF NOT mark-flag AND res-line.zimmer-wunsch MATCHES("*MARKETINGyes*") THEN
  DO:
    CREATE res-history. 
    ASSIGN 
        res-history.nr          = bediener.nr 
        res-history.resnr       = res-line.resnr 
        res-history.reslinnr    = res-line.reslinnr 
        res-history.datum       = TODAY
        res-history.zeit        = TIME
        res-history.action      = "MARKETING NEWS". 
        res-history.aenderung   = "MARKETING has been removed in reservation No " 
                                  + STRING(res-line.resnr) + "-" + STRING(res-line.reslinnr)
    .
  END.

  IF mark-flag AND (res-line.zimmer-wunsch MATCHES("*MARKETINGno*")
                    OR NOT res-line.zimmer-wunsch MATCHES("*MARKETING*")) THEN
  DO:
    CREATE res-history. 
    ASSIGN 
        res-history.nr          = bediener.nr 
        res-history.resnr       = res-line.resnr 
        res-history.reslinnr    = res-line.reslinnr 
        res-history.datum       = TODAY
        res-history.zeit        = TIME
        res-history.action      = "MARKETING NEWS". 
        res-history.aenderung   = "MARKETING has been created in reservation No " 
                                  + STRING(res-line.resnr) + "-" + STRING(res-line.reslinnr)
    .
  END.

  IF news-flag = YES THEN ct = ct + "NEWSLETTERyes;".
  ELSE IF news-flag = NO THEN ct = ct + "NEWSLETTERno;".

  IF NOT news-flag AND res-line.zimmer-wunsch MATCHES("*NEWSLETTERyes*") THEN
  DO:
    CREATE res-history. 
    ASSIGN 
        res-history.nr          = bediener.nr 
        res-history.resnr       = res-line.resnr 
        res-history.reslinnr    = res-line.reslinnr 
        res-history.datum       = TODAY
        res-history.zeit        = TIME
        res-history.action      = "NEWSLETTER". 
        res-history.aenderung   = "NEWSLETTER has been removed in reservation No " 
                                  + STRING(res-line.resnr) + "-" + STRING(res-line.reslinnr)
    .
  END.

  IF news-flag AND (res-line.zimmer-wunsch MATCHES("*NEWSLETTERno*")
                    OR NOT res-line.zimmer-wunsch MATCHES("*NEWSLETTER*")) THEN
  DO:
    CREATE res-history. 
    ASSIGN 
        res-history.nr          = bediener.nr 
        res-history.resnr       = res-line.resnr 
        res-history.reslinnr    = res-line.reslinnr 
        res-history.datum       = TODAY
        res-history.zeit        = TIME
        res-history.action      = "NEWSLETTER". 
        res-history.aenderung   = "NEWSLETTER has been created in reservation No " 
                                  + STRING(res-line.resnr) + "-" + STRING(res-line.reslinnr)
    .
  END.
  /*end*/
 
  IF restricted OR dynaRate-created THEN ct = ct + "restricted;".
  DO n = 1 TO NUM-ENTRIES(reslin-list.zimmer-wunsch,";") - 1:
    st = ENTRY(n, reslin-list.zimmer-wunsch, ";").
    IF st = "ebdisc"                             THEN .
    ELSE IF st = "kbdisc"                        THEN .
    ELSE IF st = "restricted"                    THEN .
    ELSE IF SUBSTR(st,1,7)  = "voucher"          THEN .
    ELSE IF SUBSTR(st,1,5)  = "ChAge"            THEN .
    ELSE IF SUBSTR(st,1,10) = "$OrigCode$"       THEN .
    ELSE IF SUBSTR(st,1,6)  = "$CODE$"           THEN .
    ELSE IF SUBSTR(st,1,8)  = "segm_pur"         THEN .
    ELSE IF SUBSTR(st,1,6)  = "pickup"           THEN .
    ELSE IF SUBSTR(st,1,14) = "drop-passanger"   THEN .
    ELSE IF SUBSTR(st,1,4)  = "GDPR"             THEN .
    ELSE IF SUBSTR(st,1,9)  = "MARKETING"        THEN .
    ELSE IF SUBSTR(st,1,10)  = "NEWSLETTER"        THEN .
    ELSE IF TRIM(st) = ""                        THEN .
    ELSE ct = ct + st + ";".
  END.
  
  IF segm_purcode NE 0 THEN 
  DO:    
      ct = ct + "SEGM_PUR" + STRING(segm_purcode) + ";".
      FIND FIRST resline WHERE resline.resnr = res-line.resnr
        AND resline.reslinnr NE res-line.reslinnr
        AND resline.active-flag LE 1
        AND resline.resstatus NE 12
        AND resline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
      DO WHILE AVAILABLE resline:
        IF NOT resline.zimmer-wunsch MATCHES("*SEGM_PUR*") THEN
        DO:
            FIND FIRST rline WHERE RECID(rline) = RECID(resline)
              EXCLUSIVE-LOCK NO-ERROR NO-WAIT.
            IF AVAILABLE rline THEN
            DO:
              ASSIGN rline.zimmer-wunsch = rline.zimmer-wunsch +
                "SEGM_PUR" + STRING(segm_purcode) + ";".
            END.
            FIND CURRENT rline NO-LOCK.
        END.
        FIND NEXT resline WHERE resline.resnr = res-line.resnr
          AND resline.reslinnr NE res-line.reslinnr
          AND resline.active-flag LE 1
          AND resline.resstatus NE 12
          AND resline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
      END.
  END.
    
  IF NOT pickup-flag AND res-line.zimmer-wunsch MATCHES("*pickup*") THEN
  DO:
    CREATE res-history. 
    ASSIGN 
        res-history.nr = bediener.nr 
        res-history.resnr = res-line.resnr 
        res-history.reslinnr = res-line.reslinnr 
        res-history.datum = TODAY
        res-history.zeit = TIME
        res-history.action = "Pickup". 
        res-history.aenderung =  "Pickup has been removed."
    .
  END.

  IF NOT drop-flag AND res-line.zimmer-wunsch MATCHES("*drop-passanger*") THEN
  DO:
    CREATE res-history. 
    ASSIGN 
        res-history.nr = bediener.nr 
        res-history.resnr = res-line.resnr 
        res-history.reslinnr = res-line.reslinnr 
        res-history.datum = TODAY
        res-history.zeit = TIME
        res-history.action = "Drop". 
        res-history.aenderung =  "DROP Guest has been removed."
    .
  END.

  IF res-mode = "new" OR res-mode = "insert" OR res-mode = "qci" THEN
  ct = ct + "DATE," + STRING(YEAR(ci-date)) + STRING(MONTH(ci-date),"99")
     + STRING(DAY(ci-date),"99") + ";".
  IF voucherno NE "" THEN
  DO:
    ct = ct + "voucher".
    DO n = 1 TO LENGTH(voucherno):
      IF SUBSTR(voucherno,n,1) = ";" THEN ct = ct + ",".
      ELSE ct = ct + SUBSTR(voucherno,n,1).
    END.
    ct = ct + ";".
  END.
  IF child-age NE "" THEN
  DO:
    ct = ct + "ChAge".
    DO n = 1 TO LENGTH(child-age):
      IF SUBSTR(child-age,n,1) = ";" THEN ct = ct + ",".
      ELSE ct = ct + SUBSTR(child-age,n,1).
    END.
    ct = ct + ";".
  END.

  DEF VARIABLE ratecode-date AS DATE NO-UNDO.
  IF reslin-list.ankunft GE ci-date THEN ratecode-date = reslin-list.ankunft.
  ELSE ratecode-date = ci-date.
  FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement"
      AND reslin-queasy.resnr = reslin-list.resnr
      AND reslin-queasy.reslinnr = reslin-list.reslinnr
      AND reslin-queasy.date1 LE ratecode-date
      AND reslin-queasy.date2 GE ratecode-date NO-LOCK NO-ERROR.
  IF AVAILABLE reslin-queasy AND reslin-queasy.char2 NE "" THEN
      contcode = reslin-queasy.char2.

  IF contcode NE "" THEN ct = ct + "$CODE$" + contcode + ";".
  
  ct = ct + "$OrigCode$" + origcontcode + ";".
  
  ASSIGN res-line.zimmer-wunsch = ct.

  IF NOT memozinr-readonly
    AND res-line.memozinr NE (";" + memo-zinr + ";") THEN
  DO:  
    IF res-line.memozinr MATCHES ("*;*") THEN
      memoRmNo = ENTRY(2, res-line.memozinr,";") NO-ERROR.
    CREATE res-history. 
    ASSIGN 
      res-history.nr = bediener.nr 
      res-history.datum = TODAY 
      res-history.zeit = TIME
      res-history.action = "Memo RmNo"
      res-history.aenderung = "CHG Memo RmNo " + memoRmNo + " -> " + memo-zinr
    .
    FIND CURRENT res-history NO-LOCK. 
    RELEASE res-history. 
    ASSIGN
      res-line.memozinr = ";" + memo-zinr + ";"
      res-line.memodatum = TODAY.
  END.
  
  IF restricted THEN
  DO:
    IF reslin-list.l-zuordnung[1] NE 0 THEN 
      curr-zikatnr = reslin-list.l-zuordnung[1]. 
     ELSE curr-zikatnr = reslin-list.zikatnr. 
    FIND FIRST guest-pr WHERE guest-pr.gastnr = reslin-list.gastnr NO-LOCK NO-ERROR. 
    IF AVAILABLE guest-pr THEN
    /* Rd, #752, 27Mar25, date variable */
    DO:
      tmpdate = reslin-list.abreise - 1.
      DO datum = reslin-list.ankunft TO tmpdate:
        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement"
          AND reslin-queasy.resnr = reslin-list.resnr 
          AND reslin-queasy.reslinnr = reslin-list.reslinnr
          AND reslin-queasy.date1 LE datum AND reslin-queasy.date2 GE datum
          NO-LOCK NO-ERROR.
        IF NOT AVAILABLE reslin-queasy THEN
        DO:
          RUN ratecode-rate.p(YES, kbdisc-flag, reslin-list.resnr, reslin-list.reslinnr,
            ("!" + guest-pr.CODE), datum, datum, reslin-list.ankunft,
            reslin-list.abreise, reslin-list.reserve-int, arrangement.argtnr,
            curr-zikatnr, reslin-list.erwachs, reslin-list.kind1, reslin-list.kind2,
            reslin-list.reserve-dec, reslin-list.betriebsnr, OUTPUT rate-found,
            OUTPUT rmrate, OUTPUT early-flag, OUTPUT kback-flag).
          IF rate-found THEN
          DO:
            CREATE reslin-queasy.
            ASSIGN
              reslin-queasy.key      = "arrangement"
              reslin-queasy.resnr    = reslin-list.resnr 
              reslin-queasy.reslinnr = reslin-list.reslinnr
              reslin-queasy.date1    = datum 
              reslin-queasy.date2    = datum
              reslin-queasy.deci1    = rmrate
            .
            FIND CURRENT reslin-queasy NO-LOCK.
          END.
        END.
      END.
    END.
  END.

  IF res-line.active-flag = 1 AND res-line.zinr NE reslin-list.zinr 
      AND res-line.zinr NE "" THEN 
  DO: 
      FIND FIRST queasy WHERE queasy.KEY = 24 AND queasy.char1 
         = res-line.zinr NO-LOCK NO-ERROR. 
      DO WHILE AVAILABLE queasy:    /* HK Guest Preference */ 
          FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK. 
          qsy.char1 = reslin-list.zinr. 
          FIND CURRENT qsy NO-LOCK. 
          FIND NEXT queasy WHERE queasy.KEY = 24 AND queasy.char1 
             = res-line.zinr NO-LOCK NO-ERROR. 
      END. 
      FIND FIRST resline WHERE resline.active-flag = 1 AND resline.resstatus NE 12
          AND resline.zinr = res-line.zinr AND RECID(resline) NE RECID(res-line)
          NO-LOCK NO-ERROR.
      IF NOT AVAILABLE resline THEN
      DO:
        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr EXCLUSIVE-LOCK.
        ASSIGN zimmer.zistatus = 2.
        FIND CURRENT zimmer NO-LOCK.
      END.
  END. 
 
  res-line.flight-nr = STRING(flight1, "x(6)") 
                     + STRING(eta, "x(5)") 
                     + STRING(flight2, "x(6)") 
                     + STRING(etd, "x(5)"). 
 
  IF res-line.abreisezeit = 0 THEN 
  DO: 
    IF etd NE "0000" THEN 
    DO: 
      hh = INTEGER(SUBSTR(etd,1,2)). 
      IF hh > 24 THEN hh = hh - 24. 
      mm = INTEGER(SUBSTR(etd,3,2)). 
      IF mm > 60 THEN mm = mm - 60. 
      res-line.abreisezeit = hh * 3600 + mm * 60. 
    END. 
    ELSE 
    DO:    
        /* SY 30/04/15: Add MT 19/04/13 */
        FIND FIRST htparam NO-LOCK WHERE
            htparam.paramnr = 925 NO-ERROR.
        IF AVAILABLE htparam AND htparam.fchar NE "" AND NUM-ENTRIES(htparam.fchar, ":") EQ 2 THEN 
        ASSIGN
            hh = INT(ENTRY(1, htparam.fchar, ":"))
            mm = INT(ENTRY(2, htparam.fchar, ":"))
            reslin-list.abreisezeit = (hh * 3600) + (mm * 60)
            res-line.abreisezeit    = reslin-list.abreisezeit NO-ERROR
        .
        ELSE IF reslin-list.abreise > reslin-list.ankunft THEN 
            res-line.abreisezeit = 12 * 3600. 
    END.
  END.   
  
  /* Dzikri A6FE57 - Default C/I time */
  IF res-line.ankzeit = 0 THEN 
  DO: 
    IF eta NE "0000" THEN 
    DO: 
      hh = INTEGER(SUBSTR(eta,1,2)). 
      IF hh > 24 THEN hh = hh - 24. 
      mm = INTEGER(SUBSTR(eta,3,2)). 
      IF mm > 60 THEN mm = mm - 60. 
      res-line.ankzeit = hh * 3600 + mm * 60. 
    END. 
    ELSE 
    DO:    
        FIND FIRST htparam NO-LOCK WHERE htparam.paramnr = 1054 NO-ERROR.
        IF AVAILABLE htparam AND htparam.fchar NE "" AND NUM-ENTRIES(htparam.fchar, ":") EQ 2 THEN 
        ASSIGN
            hh = INT(ENTRY(1, htparam.fchar, ":"))
            mm = INT(ENTRY(2, htparam.fchar, ":"))
            reslin-list.ankzeit = (hh * 3600) + (mm * 60)
            res-line.ankzeit    = reslin-list.ankzeit NO-ERROR
        .
        /*
        ELSE IF reslin-list.abreise > reslin-list.ankunft THEN 
            res-line.ankzeit = 14 * 3600.  
        */
    END.
  END.   
  /* Dzikri A6FE57 - END */

  IF res-line.gastnrmember NE reslin-list.gastnrmember THEN 
    gname-chged = YES. 
  ELSE gname-chged = NO. 
 
  /*FDL Debug CatchLog
  IF gname-chged THEN
  DO:      
      MESSAGE 
          "CatchLog Update Guest Name from Modify RSV " reslin-list.resnr "/" reslin-list.reslinnr SKIP
          "Gastnrmember from " res-line.gastnrmember " => " reslin-list.gastnrmember SKIP
          "Guest Name from " res-line.NAME " => " guestname SKIP
          "END CatchLog"
          VIEW-AS ALERT-BOX INFO BUTTONS OK.
  END.
*/
  res-line.gastnrmember = reslin-list.gastnrmember. 
  
  IF res-line.gastnrpay NE reslin-list.gastnrpay AND res-line.active-flag = 1 THEN 
  DO: 
    FIND FIRST bill WHERE bill.resnr = res-line.resnr 
      AND bill.reslinnr = res-line.reslinnr 
      AND bill.zinr = res-line.zinr NO-LOCK NO-ERROR. 
    IF AVAILABLE bill THEN 
    DO: 
      FIND CURRENT bill EXCLUSIVE-LOCK NO-ERROR.
      DEFINE BUFFER b-receiver FOR guest. 
      bill.gastnr = reslin-list.gastnrpay. 
      FIND FIRST b-receiver WHERE b-receiver.gastnr = bill.gastnr NO-LOCK. 
      bill.name = b-receiver.name. 
      FIND CURRENT bill NO-LOCK.
      RELEASE bill. 
    END. 
  END. 
 
  ASSIGN
    res-line.gastnrpay    = reslin-list.gastnrpay
    res-line.ankunft      = reslin-list.ankunft
    res-line.abreise      = reslin-list.abreise
    res-line.anztage      = reslin-list.anztage 
    res-line.zimmeranz    = reslin-list.zimmeranz 
    res-line.erwachs      = reslin-list.erwachs 
    res-line.kind1        = reslin-list.kind1
    res-line.kind2        = reslin-list.kind2 
    res-line.gratis       = reslin-list.gratis 
    res-line.zikatnr      = reslin-list.zikatnr
    res-line.zinr         = reslin-list.zinr
    res-line.arrangement  = reslin-list.arrangement 
    res-line.kontignr     = reslin-list.kontignr
    res-line.reserve-int  = reslin-list.reserve-int 
    res-line.setup        = reslin-list.setup
    res-line.active-flag  = reslin-list.active-flag 
    res-line.adrflag      = reslin-list.adrflag  /* YES -> rate IN local currency */ 
    res-line.betriebsnr   = reslin-list.betriebsnr 
    res-line.l-zuordnung[1] = reslin-list.l-zuordnung[1]
    res-line.name         = guestname
    res-line.grpflag      = grpflag
    res-line.code         = STRING(bill-instruct) 
    res-line.bemerk       = resline-comment
    res-line.l-zuordnung[4] = comchild
    res-line.resstatus    = reslin-list.resstatus
    res-line.zimmerfix    = (res-line.resstatus = 13)
    tot-qty               = tot-qty + res-line.zimmeranz 
  .


  IF accompany-gastnr GT 0 OR accompany-tmpnr[1] GT 0 THEN
      ASSIGN res-line.kontakt-nr = res-line.reslinnr.
/* SY Nov 05 2013
  IF res-mode EQ "inhouse" THEN res-line.resstatus = restype1. 
  IF res-mode NE "inhouse" THEN 
  DO:    
      IF oral-flag THEN res-line.resstatus = restype. 
      ELSE res-line.resstatus = restype0. 
  END.
*/  

  IF fixed-rate THEN res-line.was-status = 1. 
  ELSE res-line.was-status = 0. 
 
  IF res-mode = "new" OR res-mode = "insert" OR res-mode = "qci" THEN
  ASSIGN
      res-line.reserve-char   = STRING(YEAR(TODAY) - 2000,"99") + "/" 
                              + STRING(MONTH(TODAY),"99")       + "/"
                              + STRING(DAY(TODAY),"99")
                              + STRING(TIME,"HH:MM") + user-init
  .
  res-line.zipreis      = reslin-list.zipreis. 
 
  IF res-mode = "modify" OR res-mode = "split" OR res-mode = "inhouse" THEN 
  ASSIGN 
    res-line.changed    = ci-date 
    res-line.changed-id = user-init
  . 
    
  IF res-line.zinr NE "" THEN 
  DO: 
    FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
    res-line.setup = zimmer.setup. 
  END. 
  
  /*  December 12, 2000: store vip segment IF exist */ 
  RUN store-vip. 

  FIND CURRENT res-line NO-LOCK. 
 
  IF res-line.CODE NE "" THEN 
  DO: 
    FIND FIRST resline WHERE resline.resnr = res-line.resnr 
      AND resline.reslinnr NE res-line.reslinnr 
      AND resline.resstatus = 12 
      AND resline.CODE = "" NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE resline:
      FIND FIRST rline WHERE RECID(rline) = RECID(resline)
        EXCLUSIVE-LOCK NO-ERROR NO-WAIT.
      IF AVAILABLE rline THEN
      DO:
        rline.CODE = res-line.CODE. 
        FIND CURRENT rline NO-LOCK.
        RELEASE rline.
      END.
      FIND NEXT resline WHERE resline.resnr = res-line.resnr 
        AND resline.reslinnr NE res-line.reslinnr 
        AND resline.resstatus = 12 
        AND resline.CODE = "" NO-LOCK NO-ERROR. 
    END. 
  END. 

END. 
 
PROCEDURE check-vhpOnline-conf-email:
  FIND FIRST htparam WHERE htparam.paramnr = 39 NO-LOCK.
  IF res-line.gastnr NE htparam.finteger THEN RETURN.
  FIND FIRST interface WHERE interface.KEY = 16 
      AND interface.resnr = res-line.resnr NO-LOCK NO-ERROR.
  IF AVAILABLE interface THEN RETURN.
  DO TRANSACTION:
      CREATE interface.
      ASSIGN
          interface.KEY = 16
          interface.resnr = res-line.resnr
          interface.intdate = TODAY
          interface.int-time = TIME
      .
      FIND CURRENT interface NO-LOCK.
      RELEASE interface.
  END.
END.

PROCEDURE store-vip: 
DEFINE BUFFER gmember FOR guest. 
  FIND FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK.
  IF gmember.karteityp NE 0 THEN RETURN. 
  FIND FIRST guestseg WHERE guestseg.gastnr = gmember.gastnr 
    AND (guestseg.segmentcode = vipnr1 OR 
     guestseg.segmentcode = vipnr2 OR 
     guestseg.segmentcode = vipnr3 OR 
     guestseg.segmentcode = vipnr4 OR 
     guestseg.segmentcode = vipnr5 OR 
     guestseg.segmentcode = vipnr6 OR 
     guestseg.segmentcode = vipnr7 OR 
     guestseg.segmentcode = vipnr8 OR 
     guestseg.segmentcode = vipnr9) NO-LOCK NO-ERROR. 
  IF AVAILABLE guestseg THEN res-line.betrieb-gastmem = guestseg.segmentcode. 
  ELSE res-line.betrieb-gastmem = 0. 
END. 

PROCEDURE accompany-vip:
DEFINE BUFFER gmember FOR guest.
  FIND FIRST resline WHERE resline.resnr = reslin-list.resnr
      AND resline.reslinnr = max-resline NO-LOCK NO-ERROR.
  IF NOT AVAILABLE resline THEN RETURN.

  FIND FIRST gmember WHERE gmember.gastnr = resline.gastnrmember 
      NO-LOCK NO-ERROR.
  IF NOT AVAILABLE gmember THEN RETURN.
  
  FIND CURRENT resline EXCLUSIVE-LOCK.
  IF gmember.karteityp NE 0 THEN 
  DO:
    ASSIGN resline.betrieb-gastmem = 0.
    RETURN. 
  END.
  FIND FIRST guestseg WHERE guestseg.gastnr = gmember.gastnr 
    AND (guestseg.segmentcode = vipnr1 OR 
     guestseg.segmentcode = vipnr2 OR 
     guestseg.segmentcode = vipnr3 OR 
     guestseg.segmentcode = vipnr4 OR 
     guestseg.segmentcode = vipnr5 OR 
     guestseg.segmentcode = vipnr6 OR 
     guestseg.segmentcode = vipnr7 OR 
     guestseg.segmentcode = vipnr8 OR 
     guestseg.segmentcode = vipnr9) NO-LOCK NO-ERROR. 
  IF AVAILABLE guestseg THEN resline.betrieb-gastmem = guestseg.segmentcode. 
  ELSE resline.betrieb-gastmem = 0. 
  FIND CURRENT resline NO-LOCK.
END.

PROCEDURE resline-reserve-dec: 
DEFINE VARIABLE exchg-rate AS DECIMAL INITIAL 0. 
DEFINE BUFFER rline FOR res-line.
  IF NOT reservation.insurance THEN 
  DO: 
    FOR EACH rline WHERE rline.resnr = reservation.resnr 
      AND (rline.resstatus = 6 OR rline.resstatus = 13) 
      AND rline.reserve-dec NE 0: 
      rline.reserve-dec = 0. 
    END. 
    RETURN. 
  END.  
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
  IF exchg-rate NE 0 THEN 
  FOR EACH rline WHERE rline.resnr = reservation.resnr 
    AND (rline.resstatus = 6 OR rline.resstatus = 13) 
    AND rline.reserve-dec = 0: 
    rline.reserve-dec = exchg-rate. 
  END. 
END. 

PROCEDURE res-dyna-rmrate:
DEF VARIABLE rmrate               AS DECIMAL INITIAL ?  NO-UNDO.
DEF VARIABLE arrival-date         AS DATE               NO-UNDO.
DEF VARIABLE zikatstr             AS CHAR               NO-UNDO.

/* SY 16 AUG 2015 */
  IF origContcode = "" THEN RETURN.
  FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = origContcode
      NO-LOCK NO-ERROR.
  
  IF NOT AVAILABLE queasy THEN RETURN.


  IF NOT queasy.logi2 THEN
  DO:
      RUN static-ratecode-rates. 
      RETURN.
  END.

/* SY: dynamic rate applied */
  IF res-mode = "modify" OR res-mode = "inhouse" THEN
  DO:
      FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement"
          AND reslin-queasy.resnr = reslin-list.resnr 
          AND reslin-queasy.reslinnr = reslin-list.reslinnr
          NO-LOCK NO-ERROR.
      IF AVAILABLE reslin-queasy THEN RETURN.
  END.

/*
  FIND FIRST arrangement WHERE arrangement.arrangement = reslin-list.arrangement NO-LOCK.
*/  
  FIND FIRST zimkateg WHERE zimkateg.zikatnr = reslin-list.zikatnr NO-LOCK NO-ERROR.
  zikatstr = zimkateg.kurzbez.

  FIND FIRST res-dynarate USE-INDEX date1_ix NO-ERROR.  
  IF NOT AVAILABLE res-dynarate THEN
  DO:
    IF NOT fixed-rate  THEN
    DO:
        RUN res-dyna-rmrate.p(reslin-list.resnr, reslin-list.reslinnr,
          reslin-list.reserve-int, reslin-list.erwachs, reslin-list.kind1, reslin-list.kind2,      
          reslin-list.betriebsnr, arrangement.argtnr, zikatstr, reslin-list.ankunft, 
          reslin-list.abreise, origContcode, user-init, 
          reslin-list.reserve-dec, ebdisc-flag, kbdisc-flag, 
          OUTPUT dynaRate-created, OUTPUT rmRate).

        IF rmRate NE ? AND rmRate NE reslin-list.zipreis THEN
        DO:
          ASSIGN dyna-rmrate = rmRate.
          msg-str = msg-str + CHR(2) + "&W"
            + translateExtended ("Room Rate has been updated.", lvCAREA,"")
            + CHR(2).
          ASSIGN reslin-list.zipreis = rmRate.
        END.
    END.
    RETURN.
  END.
    
  IF AVAILABLE res-dynarate THEN
    ASSIGN arrival-date = res-dynarate.date1.
  FIND LAST res-dynarate USE-INDEX date1_ix.

  IF reslin-list.ankunft       NE arrival-date
    OR reslin-list.abreise     NE res-dynarate.date2 + 1
    OR reslin-list.erwachs     NE res-dynarate.adult
    OR reslin-list.kind1       NE res-dynarate.child
    OR reslin-list.arrangement NE res-dynarate.argt
    OR zikatstr                NE res-dynarate.rmcat
    OR marknr                  NE res-dynarate.markNo THEN
  DO:
/* SY 25-07-2015 Day Use */
    IF reslin-list.ankunft = arrival-date
        AND reslin-list.abreise = reslin-list.ankunft THEN .
/* SY 15-08-2015 add compliment room from F12 */
    ELSE IF reslin-list.gratis GT 0 AND reslin-list.zipreis = 0 THEN .
    ELSE
    DO:
      msg-str = msg-str + CHR(2) + "&W"
            + translateExtended ("Reservation data was changed,", lvCAREA,"")
            + CHR(10)
            + translateExtended ("Please re-check the rates.", lvCAREA,"")
            + CHR(2).
/* SY 16 AUG 2015: deactivate this auto rate re-calculation      
      RUN res-dyna-rmrate.p(reslin-list.resnr, reslin-list.reslinnr,
          reslin-list.reserve-int, reslin-list.erwachs, reslin-list.kind1, reslin-list.kind2,      
          reslin-list.betriebsnr, arrangement.argtnr, zikatstr, reslin-list.ankunft, 
          reslin-list.abreise, origContcode, user-init, 
          reslin-list.reserve-dec, ebdisc-flag, kbdisc-flag, 
          OUTPUT dynaRate-created, OUTPUT rmRate).
      IF rmRate NE ? AND rmRate NE reslin-list.zipreis THEN
      ASSIGN dyna-rmrate = rmRate.
      RETURN.
*/      
    END.
  END.

  ASSIGN dynaRate-created = YES.
  FOR EACH res-dynarate USE-INDEX date1_ix:
    FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement"
        AND reslin-queasy.resnr = reslin-list.resnr 
        AND reslin-queasy.reslinnr = reslin-list.reslinnr
        AND reslin-queasy.date1 = res-dynarate.date1 
        AND reslin-queasy.date2 = res-dynarate.date2
        NO-LOCK NO-ERROR.
    IF NOT AVAILABLE reslin-queasy THEN
    DO:
      CREATE reslin-queasy.
      ASSIGN
        reslin-queasy.key         = "arrangement"
        reslin-queasy.resnr       = reslin-list.resnr
        reslin-queasy.reslinnr    = reslin-list.reslinnr
        reslin-queasy.date1       = res-dynarate.date1
        reslin-queasy.date2       = res-dynarate.date2
        reslin-queasy.deci1       = res-dynarate.rate
        reslin-queasy.char2       = res-dynarate.prCode
        reslin-queasy.char3       = user-init
      . 
    END.
  END.
END.

PROCEDURE update-qsy171:
    
    DEFINE BUFFER qsy FOR queasy.
    DEFINE BUFFER bqsy    FOR queasy.
    DEFINE BUFFER zbuff   FOR zimkateg.
    DEFINE BUFFER zbuff1  FOR zimkateg.
    DEFINE BUFFER qsy-buff FOR queasy.

    DEFINE VARIABLE upto-date AS DATE.
    DEFINE VARIABLE datum  AS DATE.
    DEFINE VARIABLE start-date  AS DATE.

    DEFINE VARIABLE i           AS INT INIT 0.
    DEFINE VARIABLE iftask      AS CHAR INIT "".
    DEFINE VARIABLE origcode    AS CHAR INIT "".
    DEFINE VARIABLE do-it       AS LOGICAL INIT NO.
    DEFINE VARIABLE cat-flag    AS LOGICAL INIT NO.

    DEFINE VARIABLE roomnr      AS INT INIT 0.
    DEFINE VARIABLE roomnr1     AS INT INIT 0.
    
    IF origcode = "" THEN origcode = origContcode.

    FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN cat-flag = YES. 

    FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.char1 = origcode NO-LOCK NO-ERROR.
    IF AVAILABLE queasy AND origcode NE "" THEN do-it = YES.   

    FIND FIRST zbuff WHERE zbuff.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
    IF AVAILABLE zbuff THEN
    DO:
        IF cat-flag THEN roomnr = zbuff.typ.
        ELSE roomnr = zbuff.zikatnr.
    END.

    FIND FIRST zbuff1 WHERE zbuff1.zikatnr = reslin-list.zikatnr NO-LOCK NO-ERROR.
    IF AVAILABLE zbuff1 THEN
    DO:
        IF cat-flag THEN roomnr1 = zbuff1.typ.
        ELSE roomnr1 = zbuff1.zikatnr.
    END.

    IF (res-line.zikatnr NE reslin-list.zikatnr) OR (res-line.zimmeranz NE reslin-list.zimmeranz)
        OR (res-line.abreise NE reslin-list.abreise) OR (res-line.ankunft NE reslin-list.ankunft) THEN
        RUN intevent-1.p(1, res-line.zinr, "DataExchange", res-line.resnr, res-line.reslinnr). 
    
    IF res-line.zikatnr NE reslin-list.zikatnr THEN
    DO:
        IF res-line.ankunft = res-line.abreise THEN upto-date = res-line.abreise .
        ELSE upto-date = res-line.abreise  - 1. 

        DO datum = res-line.ankunft TO upto-date:
            FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                AND queasy.number1 = roomnr AND queasy.char1 = "" NO-LOCK NO-ERROR.
            IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
            DO:
                FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
                IF AVAILABLE qsy THEN
                DO:
                    qsy.logi2 = YES.
                    FIND CURRENT qsy NO-LOCK.
                    RELEASE qsy.
                END.       
            END. 

            IF do-it THEN
            DO:
                FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                    AND queasy.number1 = roomnr AND queasy.char1 = origcode NO-LOCK NO-ERROR.
                IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                DO:
                    FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
                    IF AVAILABLE qsy THEN
                    DO:
                        qsy.logi2 = YES.
                        FIND CURRENT qsy NO-LOCK.
                        RELEASE qsy.
                    END.   
                END. 
            END.
        END.

        IF reslin-list.ankunft = reslin-list.abreise THEN upto-date = reslin-list.abreise .
        ELSE upto-date = reslin-list.abreise - 1. 
        
        DO datum = reslin-list.ankunft TO upto-date:
            FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                AND queasy.number1 = roomnr1 AND queasy.char1 = "" NO-LOCK NO-ERROR.
            IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
            DO:
                FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
                IF AVAILABLE qsy THEN
                DO:
                    qsy.logi2 = YES.
                    FIND CURRENT qsy NO-LOCK.
                    RELEASE qsy.
                END.   
            END. 

            IF do-it THEN
            DO:
                FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                    AND queasy.number1 = roomnr1 AND queasy.char1 = origcode NO-LOCK NO-ERROR.
                IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                DO:
                    FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
                    IF AVAILABLE qsy THEN
                    DO:
                        qsy.logi2 = YES.
                        FIND CURRENT qsy NO-LOCK.
                        RELEASE qsy.
                    END.   
                END. 
            END.
        END.

         IF res-mode NE "new" THEN DO:
            /*ITA 260525 log availability*/
            CREATE res-history. 
            ASSIGN 
                res-history.nr          = bediener.nr 
                res-history.resnr       = res-line.resnr 
                res-history.reslinnr    = res-line.reslinnr 
                res-history.datum       = TODAY 
                res-history.zeit        = TIME 
                res-history.aenderung = "Modify ResLine: ResNo " + STRING(res-line.resnr ) + " No " 
                    + STRING(res-line.reslinnr ) + " - From Room Category : " + STRING(res-line.zikatnr) + " To: " 
                    + STRING(reslin-list.zikatnr)
                res-history.action      = "Log Availability".  
            IF AVAILABLE bediener THEN res-history.betriebsnr = bediener.nr. 
            RELEASE res-history. 
        END.
    END.
    ELSE IF res-line.zikatnr = reslin-list.zikatnr THEN
    DO:	
        /*IF res-line.ankunft = reslin-list.ankunft AND res-line.abreise = reslin-list.abreise AND */ /* NC - 14/06/24 #B763E6*/
        IF res-line.resstatus NE reslin-list.resstatus THEN 
		DO: /*NC- 24 Dec 21 - tiket number C5CC8F - modified 14/06/24 */
			IF reslin-list.ankunft = reslin-list.abreise THEN upto-date = reslin-list.abreise .
            ELSE upto-date = reslin-list.abreise - 1. 
            
            DO datum = reslin-list.ankunft TO upto-date:
                FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                    AND queasy.number1 = roomnr1 AND queasy.char1 = "" NO-LOCK NO-ERROR.
                IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                DO:
                    FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
                    IF AVAILABLE qsy THEN
                    DO:
                        qsy.logi2 = YES.
                        FIND CURRENT qsy NO-LOCK.
                        RELEASE qsy.
                    END.   
                END.

                IF do-it THEN
                DO:
                    FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                        AND queasy.number1 = roomnr1 AND queasy.char1 = origcode NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                    DO:
                        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
                        IF AVAILABLE qsy THEN
                        DO:
                            qsy.logi2 = YES.
                            FIND CURRENT qsy NO-LOCK.
                            RELEASE qsy.
                        END.   
                    END. 
                END.
            END.

             IF res-mode NE "new" THEN DO:
                /*ITA 260525 log availability*/
                CREATE res-history. 
                ASSIGN 
                    res-history.nr          = bediener.nr 
                    res-history.resnr       = res-line.resnr 
                    res-history.reslinnr    = res-line.reslinnr 
                    res-history.datum       = TODAY
                    res-history.zeit        = TIME 
                    res-history.aenderung = "Modify ResLine: ResNo " + STRING(res-line.resnr ) + " No " 
                        + STRING(res-line.reslinnr ) + " - From Resstatus : " + STRING(res-line.resstatus) + " To: " 
                        + STRING(reslin-list.resstatus)
                    res-history.action      = "Log Availability".  
                IF AVAILABLE bediener THEN res-history.betriebsnr = bediener.nr. 
                RELEASE res-history. 
            END.
		END. /* NC */
        ELSE IF res-line.ankunft = reslin-list.ankunft AND res-line.abreise = reslin-list.abreise AND 
           res-line.zimmeranz = reslin-list.zimmeranz THEN.
       /* ELSE  IF res-line.ankunft = reslin-list.ankunft AND res-line.abreise = reslin-list.abreise AND */ /* NC - 14/06/24 #B763E6*/
        ELSE IF res-line.zimmeranz NE reslin-list.zimmeranz THEN
        DO:
            IF reslin-list.ankunft = reslin-list.abreise THEN upto-date = reslin-list.abreise .
            ELSE upto-date = reslin-list.abreise - 1. 
            
            DO datum = reslin-list.ankunft TO upto-date:
                FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                    AND queasy.number1 = roomnr1 AND queasy.char1 = "" NO-LOCK NO-ERROR.
                IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                DO:
                    FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
                    IF AVAILABLE qsy THEN
                    DO:
                        qsy.logi2 = YES.
                        FIND CURRENT qsy NO-LOCK.
                        RELEASE qsy.
                    END.   
                END.

                IF do-it THEN
                DO:
                    FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                        AND queasy.number1 = roomnr1 AND queasy.char1 = origcode NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                    DO:
                        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
                        IF AVAILABLE qsy THEN
                        DO:
                            qsy.logi2 = YES.
                            FIND CURRENT qsy NO-LOCK.
                            RELEASE qsy.
                        END.   
                    END. 
                END.
            END.

            IF res-mode NE "new" THEN DO:
                /*ITA 260525 log availability*/
                CREATE res-history. 
                ASSIGN 
                    res-history.nr          = bediener.nr 
                    res-history.resnr       = res-line.resnr 
                    res-history.reslinnr    = res-line.reslinnr 
                    res-history.datum       = TODAY
                    res-history.zeit        = TIME 
                    res-history.aenderung = "Modify ResLine: ResNo " + STRING(res-line.resnr ) + " No " 
                        + STRING(res-line.reslinnr ) + " - From Qty : " + STRING(res-line.zimmeranz) + " To: " 
                        + STRING(reslin-list.zimmeranz)
                    res-history.action      = "Log Availability".  
                IF AVAILABLE bediener THEN res-history.betriebsnr = bediener.nr. 
                RELEASE res-history. 
            END.
        END.
        ELSE IF res-line.ankunft = reslin-list.ankunft AND res-line.abreise NE reslin-list.abreise THEN
        DO:
            IF res-line.abreise GT reslin-list.abreise THEN
            DO datum = reslin-list.abreise TO res-line.abreise - 1 :
                FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                    AND queasy.number1 = roomnr AND queasy.char1 = "" NO-LOCK NO-ERROR.
                IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                DO:
                    FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
                    IF AVAILABLE qsy THEN
                    DO:
                        qsy.logi2 = YES.
                        FIND CURRENT qsy NO-LOCK.
                        RELEASE qsy.
                    END.   
                END.
                IF do-it THEN
                DO:
                    FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                        AND queasy.number1 = roomnr AND queasy.char1 = origcode NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                    DO:
                        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
                        IF AVAILABLE qsy THEN
                        DO:
                            qsy.logi2 = YES.
                            FIND CURRENT qsy NO-LOCK.
                            RELEASE qsy.
                        END.   
                    END.
                END.
            END.
            ELSE IF reslin-list.abreise GT res-line.abreise THEN
            DO datum = res-line.abreise TO reslin-list.abreise - 1:
                FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                    AND queasy.number1 = roomnr AND queasy.char1 = "" NO-LOCK NO-ERROR.
                IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                DO:
                    FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
                    IF AVAILABLE qsy THEN
                    DO:
                        qsy.logi2 = YES.
                        FIND CURRENT qsy NO-LOCK.
                        RELEASE qsy.
                    END.   
                END.
                IF do-it THEN
                DO:
                    FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                        AND queasy.number1 = roomnr AND queasy.char1 = origcode NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                    DO:
                        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
                        IF AVAILABLE qsy THEN
                        DO:
                            qsy.logi2 = YES.
                            FIND CURRENT qsy NO-LOCK.
                            RELEASE qsy.
                        END.   
                    END.
                END.
            END.

            IF res-mode NE "new" THEN DO:
                /*ITA 260525 log availability*/
                CREATE res-history. 
                ASSIGN 
                    res-history.nr          = bediener.nr 
                    res-history.resnr       = res-line.resnr 
                    res-history.reslinnr    = res-line.reslinnr 
                    res-history.datum       = TODAY
                    res-history.zeit        = TIME 
                    res-history.aenderung = "Modify ResLine: ResNo " + STRING(res-line.resnr ) + " No " 
                        + STRING(res-line.reslinnr ) + " - From depart : " + STRING(res-line.abreise) + " To: " 
                        + STRING(reslin-list.abreise)
                    res-history.action      = "Log Availability".  
                IF AVAILABLE bediener THEN res-history.betriebsnr = bediener.nr. 
                RELEASE res-history. 
            END.

        END.
        ELSE IF res-line.ankunft NE reslin-list.ankunft AND res-line.abreise = reslin-list.abreise THEN
        DO:
            IF res-line.ankunft GT reslin-list.ankunft THEN
            DO datum = reslin-list.ankunft TO res-line.ankunft - 1:
                FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                    AND queasy.number1 = roomnr AND queasy.char1 = "" NO-LOCK NO-ERROR.
                IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                DO:
                    FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
                    IF AVAILABLE qsy THEN
                    DO:
                        qsy.logi2 = YES.
                        FIND CURRENT qsy NO-LOCK.
                        RELEASE qsy.
                    END.   
                END.
                IF do-it THEN
                DO:
                    FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                        AND queasy.number1 = roomnr AND queasy.char1 = origcode NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                    DO:
                        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
                        IF AVAILABLE qsy THEN
                        DO:
                            qsy.logi2 = YES.
                            FIND CURRENT qsy NO-LOCK.
                            RELEASE qsy.
                        END.   
                    END. 
                END.
            END.
            ELSE IF reslin-list.ankunft GT res-line.ankunft THEN
            DO datum = res-line.ankunft TO reslin-list.ankunft - 1:
                FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                    AND queasy.number1 = roomnr AND queasy.char1 = "" NO-LOCK NO-ERROR.
                IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                DO:
                    FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
                    IF AVAILABLE qsy THEN
                    DO:
                        qsy.logi2 = YES.
                        FIND CURRENT qsy NO-LOCK.
                        RELEASE qsy.
                    END.   
                END.
                IF do-it THEN
                DO:
                    FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                        AND queasy.number1 = roomnr AND queasy.char1 = origcode NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                    DO:
                        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
                        IF AVAILABLE qsy THEN
                        DO:
                            qsy.logi2 = YES.
                            FIND CURRENT qsy NO-LOCK.
                            RELEASE qsy.
                        END.   
                    END. 
                END.
            END.

            IF res-mode NE "new" THEN DO:
                /*ITA 260525 log availability*/
                CREATE res-history. 
                ASSIGN 
                    res-history.nr          = bediener.nr 
                    res-history.resnr       = res-line.resnr 
                    res-history.reslinnr    = res-line.reslinnr 
                    res-history.datum       = TODAY
                    res-history.zeit        = TIME 
                    res-history.aenderung = "Modify ResLine: ResNo " + STRING(res-line.resnr ) + " No " 
                        + STRING(res-line.reslinnr ) + " - From arrive : " + STRING(res-line.ankunft) + " To: " 
                        + STRING(reslin-list.ankunft)
                    res-history.action      = "Log Availability".  
                IF AVAILABLE bediener THEN res-history.betriebsnr = bediener.nr. 
                RELEASE res-history. 
            END.
        END.
        ELSE IF res-line.ankunft NE reslin-list.ankunft AND res-line.abreise NE reslin-list.abreise THEN
        DO:
            IF res-line.ankunft = res-line.abreise THEN upto-date = res-line.abreise .
            ELSE upto-date = res-line.abreise  - 1. 
            
            DO datum = res-line.ankunft TO upto-date:
                FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                    AND queasy.number1 = roomnr AND queasy.char1 = "" NO-LOCK NO-ERROR.
                IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                DO:
                    FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
                    IF AVAILABLE qsy THEN
                    DO:
                        qsy.logi2 = YES.
                        FIND CURRENT qsy NO-LOCK.
                        RELEASE qsy.
                    END.   
                END.
                IF do-it THEN
                DO:
                    FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                        AND queasy.number1 = roomnr AND queasy.char1 = origcode NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                    DO:
                        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
                        IF AVAILABLE qsy THEN
                        DO:
                            qsy.logi2 = YES.
                            FIND CURRENT qsy NO-LOCK.
                            RELEASE qsy.
                        END.   
                    END. 
                END.
            END.

            IF reslin-list.ankunft = reslin-list.abreise THEN upto-date = reslin-list.abreise .
            ELSE upto-date = reslin-list.abreise - 1. 
            
            DO datum = reslin-list.ankunft TO upto-date:
                FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                    AND queasy.number1 = roomnr1 AND queasy.char1 = "" NO-LOCK NO-ERROR.
                IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                DO:
                    FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
                    IF AVAILABLE qsy THEN
                    DO:
                        qsy.logi2 = YES.
                        FIND CURRENT qsy NO-LOCK.
                        RELEASE qsy.
                    END.   
                END.
                IF do-it THEN
                DO:
                    FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                        AND queasy.number1 = roomnr1 AND queasy.char1 = origcode NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                    DO:
                        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
                        IF AVAILABLE qsy THEN
                        DO:
                            qsy.logi2 = YES.
                            FIND CURRENT qsy NO-LOCK.
                            RELEASE qsy.
                        END.   
                    END.
                END.
            END.

            IF res-mode NE "new" THEN DO:
                /*ITA 260525 log availability*/
                CREATE res-history. 
                ASSIGN 
                    res-history.nr          = bediener.nr 
                    res-history.resnr       = res-line.resnr 
                    res-history.reslinnr    = res-line.reslinnr 
                    res-history.datum       = TODAY
                    res-history.zeit        = TIME 
                    res-history.aenderung = "Modify ResLine: ResNo " + STRING(res-line.resnr ) + " No " 
                        + STRING(res-line.reslinnr ) + " - From arrive : " + STRING(res-line.ankunft) + " To: " 
                        + STRING(reslin-list.ankunft) + " and From Depart : " + STRING(res-line.abreise) + " To: " 
                        + STRING(reslin-list.abreise)
                    res-history.action      = "Log Availability".  
                IF AVAILABLE bediener THEN res-history.betriebsnr = bediener.nr. 
                RELEASE res-history. 
            END.

        END.
    END.

    IF res-mode = "new" THEN DO:
        CREATE res-history. 
        ASSIGN 
            res-history.nr          = bediener.nr 
            res-history.resnr       = res-line.resnr 
            res-history.reslinnr    = res-line.reslinnr 
            res-history.datum       = TODAY
            res-history.zeit        = TIME 
            res-history.aenderung = "Create ResLine: ResNo " + STRING(res-line.resnr ) + " No " 
                + STRING(res-line.reslinnr ) + " - " + res-line.NAME 
            res-history.action      = "Log Availability".  
        IF AVAILABLE bediener THEN res-history.betriebsnr = bediener.nr. 
        RELEASE res-history. 
    END.

END.

IF priscilla-active AND res-line.active-flag NE 2 
    AND (res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1)
    AND res-line.resstatus NE 12 THEN
DO:
    IF res-mode = "modify" THEN
        RUN intevent-1.p(9, res-line.zinr, "Priscilla", res-line.resnr, res-line.reslinnr).
    ELSE IF res-mode = "qci" THEN
        RUN intevent-1.p(10, res-line.zinr, "Priscilla", res-line.resnr, res-line.reslinnr). 
    ELSE IF res-mode = "insert" THEN
        RUN intevent-1.p(11, res-line.zinr, "Priscilla", res-line.resnr, res-line.reslinnr). 
    ELSE IF res-mode = "new" THEN
        RUN intevent-1.p(12, res-line.zinr, "Priscilla", res-line.resnr, res-line.reslinnr). 
    ELSE IF res-mode = "inhouse" THEN
    DO:
        RUN intevent-1.p(9, res-line.zinr, "Priscilla", res-line.resnr, res-line.reslinnr).
        FIND FIRST htparam WHERE paramnr = 359 NO-LOCK. 
        IF htparam.flogical THEN 
            RUN intevent-1.p(1, res-line.zinr, "Change name", res-line.resnr, res-line.reslinnr). 
    END.
END.

