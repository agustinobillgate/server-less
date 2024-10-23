DEFINE TEMP-TABLE test
    FIELD xx AS CHAR
    FIELD yy AS CHAR.

DEFINE TEMP-TABLE cl-list 
  FIELD flag    AS INTEGER 
  FIELD loc     AS CHAR FORMAT "x(10)" LABEL "Location"
  FIELD etage   AS CHAR FORMAT "x(10)" LABEL "Floor" 
  FIELD inact   AS INTEGER FORMAT ">>>9" LABEL "Inactive" 
  FIELD occ     AS INTEGER FORMAT ">>>9" LABEL "Occupied" 
  FIELD hu      AS INTEGER FORMAT ">>>9" LABEL "HUse" 
  FIELD ooo     AS INTEGER FORMAT ">>>9" LABEL "OOO" 
  FIELD com     AS INTEGER FORMAT ">>>9" LABEL "Compl" 
  FIELD vac     AS INTEGER FORMAT ">>>9" LABEL "Vacant" 
  FIELD sum     AS INTEGER FORMAT ">>>9" LABEL "Total" 
  FIELD pax     AS INTEGER FORMAT ">>>9" LABEL "Payable Pax" 
  FIELD cpax    AS INTEGER FORMAT ">>>9" LABEL "Compl Pax" 
  FIELD rev     AS DECIMAL FORMAT "->,>>>>,>>>,>>9.99" LABEL "Gross Room Revenue" 
  FIELD nrev    AS DECIMAL FORMAT "->,>>>>,>>>,>>9.99" LABEL "Net Room Revenue". 

DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER ci-date        AS DATE.
DEF OUTPUT PARAMETER price-decimal  AS INT.
DEF OUTPUT PARAMETER long-digit     AS LOGICAL.
DEF OUTPUT PARAMETER foreign-rate   AS LOGICAL.
DEF OUTPUT PARAMETER curr-local     AS CHAR.
DEF OUTPUT PARAMETER curr-foreign   AS CHAR.
DEF OUTPUT PARAMETER exchg-rate     AS DECIMAL.
DEF OUTPUT PARAMETER flag-t         AS LOGICAL.

DEF OUTPUT PARAMETER t-occ          AS INTEGER FORMAT ">>>>>9" INITIAL 0. 
DEF OUTPUT PARAMETER t-hu           AS INTEGER FORMAT ">>>>>9"  INITIAL 0. 
DEF OUTPUT PARAMETER t-ooo          AS INTEGER FORMAT ">>>>>9"  INITIAL 0. 
DEF OUTPUT PARAMETER t-com          AS INTEGER FORMAT ">>>>>9"  INITIAL 0. 
DEF OUTPUT PARAMETER t-vac          AS INTEGER FORMAT ">>>>>9"  INITIAL 0. 
DEF OUTPUT PARAMETER t-sum          AS INTEGER FORMAT ">>>>>9"  INITIAL 0. 
DEF OUTPUT PARAMETER t-inact        AS INTEGER FORMAT ">>>>>9"  INITIAL 0. 
DEF OUTPUT PARAMETER t-rev          AS DECIMAL FORMAT "->,>>>>,>>>,>>9.99"  INITIAL 0. 
DEF OUTPUT PARAMETER t-nrev         AS DECIMAL FORMAT "->,>>>>,>>>,>>9.99"  INITIAL 0. 
DEF OUTPUT PARAMETER t-pax          AS INTEGER FORMAT ">>>>>9"  INITIAL 0. 
DEF OUTPUT PARAMETER t-cpax         AS INTEGER FORMAT ">>>>>9"  INITIAL 0. 

DEF OUTPUT PARAMETER TABLE FOR cl-list.

DEFINE VARIABLE fact AS DECIMAL.
DEFINE VARIABLE frate AS DECIMAL. 
DEFINE VARIABLE ex-rate AS DECIMAL. 

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "rm-ATdrecap".

FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
ci-date = htparam.fdate. 
 
FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger. 
 
FIND FIRST htparam WHERE htparam.paramnr = 246. 
long-digit = htparam.flogical. 
 
FIND FIRST htparam WHERE paramnr = 240 no-lock.  /* double currency */ 
foreign-rate = htparam.flogical. 


FIND FIRST htparam WHERE paramnr = 152 NO-LOCK. 
curr-local = fchar. 
FIND FIRST htparam WHERE paramnr = 144 NO-LOCK. 
curr-foreign = fchar. 
FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
ELSE exchg-rate = 1. 

RUN create-list.

PROCEDURE create-list: 
DEFINE VARIABLE temp-loc AS CHARACTER.
DEFINE VARIABLE temp-et AS CHAR.

DEFINE VARIABLE status-vat AS LOGICAL.
DEFINE VARIABLE serv AS DECIMAL. 
DEFINE VARIABLE vat  AS DECIMAL. 
DEFINE VARIABLE vat2 AS DECIMAL NO-UNDO.
DEFINE VARIABLE fact AS DECIMAL NO-UNDO.
DEFINE VARIABLE serv-vat AS LOGICAL.

DEFINE VARIABLE argt-betrag AS DECIMAL. 
DEFINE VARIABLE lodging AS DECIMAL FORMAT "->,>>>>,>>>,>>9.99". 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE n AS INTEGER. 
/*DEFINE VARIABLE post-it AS LOGICAL. */
DEFINE BUFFER bzimmer  FOR zimmer.

FIND FIRST bzimmer WHERE NOT(bzimmer.CODE MATCHES "") NO-LOCK NO-ERROR.
IF AVAILABLE bzimmer THEN flag-t = YES.

  FOR EACH zimmer NO-LOCK BY zimmer.CODE: 
    FIND FIRST cl-list WHERE cl-list.etage = STRING (zimmer.etage) AND cl-list.loc = zimmer.CODE NO-ERROR. 
    IF NOT AVAILABLE cl-list THEN 
    DO: 
      create cl-list. 
      cl-list.loc = zimmer.CODE.
      cl-list.etage = STRING (zimmer.etage). 
    END. 
    IF zimmer.zistatus LE 2 THEN cl-list.vac = cl-list.vac + 1. 
    ELSE IF zimmer.zistatus EQ 6 THEN cl-list.ooo = cl-list.ooo + 1. 
    IF NOT zimmer.sleeping THEN cl-list.inact = cl-list.inact + 1. 
  END. 

  FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
  serv-vat = htparam.flogical. 
  FIND FIRST htparam WHERE htparam.paramnr = 127 NO-LOCK NO-ERROR.
  status-vat = htparam.flogical. 
  FIND FIRST artikel WHERE artikel.artnr = 99 AND artikel.departement = 0 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE artikel AND status-vat = YES THEN 
  DO: 
/*
    serv = 0. 
    vat = 0. 
    RUN calc-servvat.p(artikel.departement, artikel.artnr, ci-date, artikel.service-code, 
             artikel.mwst-code, OUTPUT serv, OUTPUT vat).
    fact = 1.00 + serv + vat. 
*/
/* SY AUG 13 2017 */
    RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
        ci-date, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
    ASSIGN vat = vat + vat2.
  END. 
  FOR EACH res-line WHERE (res-line.active-flag = 1 AND resstatus NE 12 ) 
    AND ((res-line.abreise GT ci-date) OR 
    (res-line.ankunft = res-line.abreise)) 
    NO-LOCK, 
    FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK 
    BY res-line.zinr BY res-line.resnr: 
    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK. 
    FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement 
    NO-LOCK. 
   
    frate = 1.
    
    IF res-line.betriebsnr NE 1 THEN frate = exchg-rate.
    ELSE IF res-line.adrflag THEN frate = 1. 
    ELSE IF res-line.reserve-dec NE 0 THEN frate = reserve-dec. 
     
    FIND FIRST cl-list WHERE cl-list.etage = STRING (zimmer.etage) AND cl-list.loc = zimmer.CODE. 
    IF res-line.gratis GT 0 OR (res-line.zipreis = 0 AND res-line.erwachs GT 0) 
    THEN 
    DO: 
      IF zimmer.sleeping THEN cl-list.com = cl-list.com + 1. 
      ELSE cl-list.hu = cl-list.hu + 1. 
      cl-list.cpax = cl-list.cpax + res-line.gratis + res-line.erwachs. 
      IF res-line.zipreis = 0 AND res-line.erwachs GT 0 THEN 
      DO: 
        msg-str = msg-str + CHR(2) + "&W"
                + translateExtended ("RmNo ",lvCAREA,"") + res-line.zinr + ": Rate = 0 and Adult = " 
                + STRING(res-line.erwachs) + " found.".
      END. 
    END. 
 
    IF res-line.zipreis GT 0 THEN 
    DO: 
      lodging = res-line.zipreis. 
      FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr 
        AND NOT argt-line.kind2 NO-LOCK: 
        FIND FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
          AND artikel.departement = argt-line.departement NO-LOCK. 
        RUN argt-betrag.p(RECID(res-line), RECID(argt-line), 
          OUTPUT argt-betrag, OUTPUT ex-rate). 
        lodging = lodging - argt-betrag. 
      END. 
      
      lodging = round(lodging * frate, price-decimal). 
      
      IF foreign-rate AND price-decimal = 0 THEN 
      DO: 
        FIND FIRST htparam WHERE paramnr = 145 NO-LOCK. 
        IF htparam.finteger NE 0 THEN 
        DO: 
          n = 1. 
          DO i = 1 TO finteger: 
            n = n * 10. 
          END. 
          lodging = ROUND(lodging / n, 0) * n. 
        END. 
      END.
      cl-list.occ = cl-list.occ + 1. 
      cl-list.pax = cl-list.pax + res-line.erwachs + res-line.kind1. 
      cl-list.rev = cl-list.rev + lodging. 
    END. 
    
 END.
 /*
    FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr 
      AND fixleist.reslinnr = res-line.reslinnr NO-LOCK: 
      RUN check-fixleist-posted(fixleist.artnr, fixleist.departement, 
        fixleist.sequenz, fixleist.dekade, 
        fixleist.lfakt, OUTPUT post-it). 
      IF post-it THEN cl-list.rev = cl-list.rev 
        + (fixleist.betrag * fixleist.number) * frate. 
    END. 
 */

  RUN gr-tot.

FOR EACH cl-list WHERE NOT cl-list.loc MATCHES ("Gr. TOTAL") BY cl-list.loc DESC:
  FIND FIRST test WHERE xx = cl-list.loc NO-ERROR.
  IF NOT AVAILABLE test THEN
  DO:
          CREATE test.
          ASSIGN test.xx = cl-list.loc
                      test.yy = "".
  END.
END.

FOR EACH cl-list WHERE NOT cl-list.etage MATCHES ("G. TOTAL") BY cl-list.etage DESC:
  FIND FIRST test WHERE yy = cl-list.etage NO-ERROR.
  IF NOT AVAILABLE test THEN
  DO:
          CREATE test.
          ASSIGN test.yy = cl-list.etage
                         test.xx = "".
  END.
END.

 FOR EACH test WHERE test.xx MATCHES ("") AND NOT test.yy MATCHES ("G.TOTAL") :
      t-occ = 0.
      t-hu = 0.
      t-ooo = 0.
      t-com = 0.
      t-vac = 0.
      t-sum = 0.
      t-inact = 0.
      t-rev = 0.
      t-nrev = 0.
      t-pax = 0.
      t-cpax = 0.
     FOR EACH cl-list WHERE cl-list.etage = test.yy:
         temp-et = cl-list.etage.
         temp-loc = cl-list.loc.
         cl-list.sum = cl-list.occ + cl-list.hu + cl-list.ooo 
           + cl-list.com + cl-list.vac. 
         cl-list.nrev = round(cl-list.rev / fact, price-decimal). 
         t-occ = t-occ + cl-list.occ. 
         t-hu = t-hu + cl-list.hu. 
         t-ooo = t-ooo + cl-list.ooo. 
         t-com = t-com + cl-list.com. 
         t-vac = t-vac + cl-list.vac. 
         t-sum = t-sum + cl-list.sum. 
         t-inact = t-inact + cl-list.inact. 
         t-rev = t-rev + cl-list.rev. 
         t-nrev = t-nrev + cl-list.nrev. 
         t-pax = t-pax + cl-list.pax. 
         t-cpax = t-cpax + cl-list.cpax. 
         /*STRING (t-etage) = cl-list.etage.*/
  END.
  IF NOT temp-et MATCHES ("") THEN DO:
  CREATE cl-list.
  ASSIGN
      cl-list.flag = 1. 
      cl-list.etage = temp-et + "-TOTAL".
      cl-list.loc = "".
      cl-list.occ = t-occ. 
      cl-list.hu = t-hu. 
      cl-list.ooo = t-ooo. 
      cl-list.com = t-com. 
      cl-list.vac = t-vac. 
      cl-list.sum = t-sum. 
      cl-list.inact = t-inact. 
      cl-list.rev = t-rev. 
      cl-list.nrev = t-nrev. 
      cl-list.pax = t-pax. 
      cl-list.cpax = t-cpax.
  END.
      t-occ = 0.
      t-hu = 0.
      t-ooo = 0.
      t-com = 0.
      t-vac = 0.
      t-sum = 0.
      t-inact = 0.
      t-rev = 0.
      t-nrev = 0.
      t-pax = 0.
      t-cpax = 0.
 END.

     FOR EACH test WHERE NOT test.xx MATCHES (""):
          t-occ = 0.
          t-hu = 0.
          t-ooo = 0.
          t-com = 0.
          t-vac = 0.
          t-sum = 0.
          t-inact = 0.
          t-rev = 0.
          t-nrev = 0.
          t-pax = 0.
          t-cpax = 0.

         FOR EACH cl-list WHERE cl-list.loc MATCHES test.xx:
             temp-loc = cl-list.loc.
             cl-list.sum = cl-list.occ + cl-list.hu + cl-list.ooo 
               + cl-list.com + cl-list.vac. 
             cl-list.nrev = round(cl-list.rev / fact, price-decimal). 
             t-occ = t-occ + cl-list.occ. 
             t-hu = t-hu + cl-list.hu. 
             t-ooo = t-ooo + cl-list.ooo. 
             t-com = t-com + cl-list.com. 
             t-vac = t-vac + cl-list.vac. 
             t-sum = t-sum + cl-list.sum. 
             t-inact = t-inact + cl-list.inact. 
             t-rev = t-rev + cl-list.rev. 
             t-nrev = t-nrev + cl-list.nrev. 
             t-pax = t-pax + cl-list.pax. 
             t-cpax = t-cpax + cl-list.cpax. 
         END.
         CREATE cl-list.
         ASSIGN
             cl-list.flag = 1. 
             cl-list.loc = temp-loc + "-TOTAL".
             cl-list.etage = "".
             cl-list.occ = t-occ. 
             cl-list.hu = t-hu. 
             cl-list.ooo = t-ooo. 
             cl-list.com = t-com. 
             cl-list.vac = t-vac. 
             cl-list.sum = t-sum. 
             cl-list.inact = t-inact. 
             cl-list.rev = t-rev. 
             cl-list.nrev = t-nrev. 
             cl-list.pax = t-pax. 
             cl-list.cpax = t-cpax.

             t-occ = 0.
             t-hu = 0.
             t-ooo = 0.
             t-com = 0.
             t-vac = 0.
             t-sum = 0.
             t-inact = 0.
             t-rev = 0.
             t-nrev = 0.
             t-pax = 0.
             t-cpax = 0.
 END.
END. 


PROCEDURE gr-tot:
    t-occ = 0.
    t-hu = 0.
    t-ooo = 0.
    t-com = 0.
    t-vac = 0.
    t-sum = 0.
    t-inact = 0.
    t-rev = 0.
    t-nrev = 0.
    t-pax = 0.
    t-cpax = 0.

    DEFINE VAR t-etage AS INTEGER.

    FOR EACH cl-list BY cl-list.etage: 
      cl-list.sum = cl-list.occ + cl-list.hu + cl-list.ooo 
        + cl-list.com + cl-list.vac. 
      cl-list.nrev = round(cl-list.rev / fact, price-decimal). 
      t-occ = t-occ + cl-list.occ. 
      t-hu = t-hu + cl-list.hu. 
      t-ooo = t-ooo + cl-list.ooo. 
      t-com = t-com + cl-list.com. 
      t-vac = t-vac + cl-list.vac. 
      t-sum = t-sum + cl-list.sum. 
      t-inact = t-inact + cl-list.inact. 
      t-rev = t-rev + cl-list.rev. 
      t-nrev = t-nrev + cl-list.nrev. 
      t-pax = t-pax + cl-list.pax. 
      t-cpax = t-cpax + cl-list.cpax. 
      STRING (t-etage) = cl-list.etage.
    END. 

    create cl-list. 
    ASSIGN 
      cl-list.flag = 1 
      cl-list.loc = "Gr. TOTAL"
        cl-list.etage = ""
      cl-list.occ = t-occ 
      cl-list.hu = t-hu 
      cl-list.ooo = t-ooo 
      cl-list.com = t-com 
      cl-list.vac = t-vac 
      cl-list.sum = t-sum 
      cl-list.inact = t-inact 
      cl-list.rev = t-rev 
      cl-list.nrev = t-nrev 
      cl-list.pax = t-pax 
      cl-list.cpax = t-cpax. 

    IF t-etage = 0 THEN t-etage = 999.
    create cl-list. 
    ASSIGN 
      cl-list.flag = 1 
      cl-list.loc = ""
      cl-list.etage = "G.TOTAL"
      cl-list.occ = t-occ 
      cl-list.hu = t-hu 
      cl-list.ooo = t-ooo 
      cl-list.com = t-com 
      cl-list.vac = t-vac 
      cl-list.sum = t-sum 
      cl-list.inact = t-inact 
      cl-list.rev = t-rev 
      cl-list.nrev = t-nrev 
      cl-list.pax = t-pax 
      cl-list.cpax = t-cpax. 


    t-occ = 0.
    t-hu = 0.
    t-ooo = 0.
    t-com = 0.
    t-vac = 0.
    t-sum = 0.
    t-inact = 0.
    t-rev = 0.
    t-nrev = 0.
    t-pax = 0.
    t-cpax = 0.
END.

