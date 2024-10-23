/*FD Oct 23, 2020 => BL for view ratecode web based*/

DEFINE TEMP-TABLE t-viewrates 
  FIELD prcode          AS CHARACTER    /*Column Rate Code*/
  FIELD desc-prcode     AS CHARACTER    /*Column Rate Code Description*/
  FIELD currency        AS CHARACTER    /*Column Currency*/
  FIELD market          AS CHARACTER    /*Column Market Segment*/
  FIELD argt            AS CHARACTER    /*Column Arrangement*/
  FIELD rmtype          AS CHARACTER    /*Column Room Type*/  
. 

DEFINE TEMP-TABLE t-viewrates-line 
  FIELD prcode          AS CHARACTER    /*Column Rate Code*/
  FIELD desc-prcode     AS CHARACTER    /*Column Rate Code Description*/
  FIELD currency        AS CHARACTER    /*Column Currency*/
  FIELD market          AS CHARACTER    /*Column Market Segment*/
  FIELD argt            AS CHARACTER    /*Column Arrangement*/
  FIELD rmtype          AS CHARACTER    /*Column Room Type*/
  FIELD datum           AS CHARACTER    /*Column Detail Date*/
  FIELD str-aci         AS CHARACTER    /*Column Detail lable adult/child/infant*/
  FIELD aci             AS CHARACTER    /*Column Detail adult/child/infant*/
  FIELD str-rate-aci    AS CHARACTER    /*Column Detail lable adultRate/childRate/infantRate*/
  FIELD adult-rate      AS CHARACTER    /*Column Detail adult rate*/
  FIELD child-rate      AS CHARACTER    /*Column Detail child rate*/
  FIELD infant-rate     AS CHARACTER    /*Column Detail infant rate*/
  FIELD deci4           AS CHARACTER   
. 
 
DEFINE TEMP-TABLE select-list 
  FIELD argtnr      AS INTEGER 
  FIELD zikatnr     AS INTEGER
. 
/**/
DEFINE INPUT PARAMETER pvILanguage     AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER gastnr          AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER pr-code         AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER market-combo    AS CHAR    NO-UNDO INITIAL "All Market".
DEFINE OUTPUT PARAMETER comments       AS CHAR    NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER TABLE FOR t-viewrates.
DEFINE OUTPUT PARAMETER TABLE FOR t-viewrates-line.

/* Testing with DB Harris Cium
DEFINE variable  pvILanguage     AS INTEGER NO-UNDO INIT 1.
DEFINE variable  gastnr          AS INTEGER NO-UNDO INIT 686.
DEFINE variable  pr-code         AS CHAR    NO-UNDO INIT "".
DEFINE variable  market-combo    AS CHAR    NO-UNDO INIT "All Market".
DEFINE VARIABLE comments         AS CHAR.
*/
DEF VARIABLE ci-date            AS DATE     NO-UNDO.
DEF VARIABLE current-counter    AS INTEGER  NO-UNDO.  

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "view-ratecode-web". 


IF gastnr > 0 THEN RUN create-list. 
ELSE RUN create-list0.

/*************************************** PROCEDURE **************************************/
PROCEDURE create-list0: 
DEFINE VARIABLE marknr1             AS INTEGER INITIAL 0. 
DEFINE VARIABLE argt1               AS INTEGER INITIAL 0. 
DEFINE VARIABLE zikat1              AS INTEGER INITIAL 0. 
DEFINE VARIABLE i                   AS INTEGER.
DEFINE VARIABLE n                   AS INTEGER.

DEFINE VARIABLE ct                  AS CHAR.
DEFINE VARIABLE st                  AS CHAR.
DEFINE VARIABLE curr-str            AS CHAR.
DEFINE VARIABLE currency            AS CHAR.

DEFINE VARIABLE f-date              AS DATE.
DEFINE VARIABLE t-date              AS DATE.

DEFINE VARIABLE disc-rate           AS DECIMAL.
DEFINE VARIABLE rate                AS DECIMAL. 

DEFINE VARIABLE queasy-exist        AS LOGICAL INITIAL NO. 
DEFINE VARIABLE fixed-rate          AS LOGICAL INITIAL NO NO-UNDO. 
DEFINE VARIABLE do-it               AS LOGICAL INITIAL NO NO-UNDO.

DEFINE BUFFER qsy FOR queasy.

  FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
  ci-date = htparam.fdate.    

  FOR EACH prtable WHERE prtable.prcode = pr-code NO-LOCK,
    FIRST prmarket WHERE prmarket.nr = prtable.marknr 
      AND prmarket.bezeich = market-combo NO-LOCK
    BY prmarket.bezeich:
    
    RUN create-selectlist.
    
    FIND FIRST qsy WHERE qsy.key = 18 AND qsy.number1 = prmarket.nr 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE qsy THEN 
    DO: 
      currency = qsy.char3. 
      fixed-rate = qsy.logi3. 
    END.
    
    FOR EACH select-list BY select-list.argtnr BY select-list.zikatnr: 
      FIND FIRST arrangement WHERE arrangement.argtnr = select-list.argtnr 
        NO-LOCK. 
      FIND FIRST zimkateg WHERE zimkateg.zikatnr = select-list.zikatnr NO-LOCK. 
      ASSIGN
        argt1        = 0 
        zikat1       = 0 
        queasy-exist = NO
      . 
    
      FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = prtable.prcode NO-ERROR.
      FIND FIRST waehrung WHERE waehrung.waehrungsnr = queasy.number1 NO-LOCK NO-ERROR.
    
      FIND FIRST t-viewrates WHERE t-viewrates.prcode = pr-code
          AND t-viewrates.argt = arrangement.arrangement
          AND t-viewrates.rmtype = zimkateg.kurzbez NO-LOCK NO-ERROR.
      IF NOT AVAILABLE t-viewrates THEN
      DO:
        CREATE t-viewrates.
        IF AVAILABLE queasy THEN
        DO:
          ASSIGN
            t-viewrates.prcode      = queasy.char1
            t-viewrates.desc-prcode = queasy.char2
          .
        END.
        IF AVAILABLE waehrung THEN t-viewrates.currency = waehrung.bezeich.
        
        IF currency NE "" THEN 
          t-viewrates.market = prmarket.bezeich + " - " + "Currency" + " = " + qsy.char3.
        IF fixed-rate THEN
          t-viewrates.market = prmarket.bezeich + "; " + "Fixed Rate for whole stay".
        
        ASSIGN
          t-viewrates.argt         = arrangement.arrangement
          t-viewrates.rmtype       = zimkateg.kurzbez        
        .
      END.
    
      FOR EACH ratecode WHERE ratecode.code = pr-code 
        AND ratecode.marknr = prtable.marknr 
        AND ratecode.zikatnr = select-list.zikatnr 
        AND ratecode.argtnr = select-list.argtnr NO-LOCK 
        BY ratecode.startperiode BY ratecode.wday:            
    
        do-it = (ci-date LE ratecode.endperiode). 
        IF do-it THEN
        DO:
          CREATE t-viewrates-line.
    
          IF AVAILABLE queasy THEN
          DO:
            ASSIGN
              t-viewrates-line.prcode      = queasy.char1
              t-viewrates-line.desc-prcode = queasy.char2
            .
          END.
          IF AVAILABLE waehrung THEN t-viewrates-line.currency = waehrung.bezeich.
          
          IF currency NE "" THEN 
            t-viewrates-line.market = prmarket.bezeich + " - " + "Currency" + " = " + qsy.char3.
          IF fixed-rate THEN
            t-viewrates-line.market = prmarket.bezeich + "; " + "Fixed Rate for whole stay".
          
          ASSIGN
            t-viewrates-line.argt         = arrangement.arrangement
            t-viewrates-line.rmtype       = zimkateg.kurzbez
            t-viewrates-line.datum        = STRING(ratecode.startperiode, "99/99/99")
                                             + " - " + STRING(ratecode.endperiode, "99/99/99")
            t-viewrates-line.str-aci      = "Adult/Child/Infant :"
            t-viewrates-line.aci          = STRING(ratecode.erwachs) + "/" + STRING(ratecode.kind1) + "/"
                                             + STRING(ratecode.kind2)
            t-viewrates-line.str-rate-aci = "Adult Rate/Child Rate/Infant Rate :"
            t-viewrates-line.adult-rate   = TRIM(STRING(ratecode.zipreis, ">>>,>>>,>>9.99"))
            t-viewrates-line.child-rate   = TRIM(STRING(ratecode.ch1preis, ">>>,>>>,>>9.99"))
            t-viewrates-line.infant-rate  = TRIM(STRING(ratecode.ch2preis, ">>>,>>>,>>9.99"))
          .  
    
          IF ratecode.char1[1] NE "" OR ratecode.char1[2] NE ""
            OR ratecode.char1[3] NE "" OR ratecode.char1[4] NE "" THEN
          DO:          
            IF NUM-ENTRIES(ratecode.char1[4], ";") GE 3 THEN 
            DO: 
              CREATE t-viewrates-line.
              IF AVAILABLE queasy THEN t-viewrates-line.prcode = queasy.char1.
              ASSIGN
                t-viewrates-line.argt         = arrangement.arrangement
                t-viewrates-line.rmtype       = zimkateg.kurzbez
                t-viewrates-line.datum        = "COMPLIMENT ROOM :"
                t-viewrates-line.str-aci      = "Room Booked / Get Compliment / Tpotal Compliment :"
                t-viewrates-line.adult-rate   = TRIM(STRING(INTEGER(ENTRY(1, ratecode.char1[4], ";")),">>9"))           
                t-viewrates-line.child-rate   = TRIM(STRING(INTEGER(ENTRY(2, ratecode.char1[4], ";")),">>9")) 
                t-viewrates-line.infant-rate  = TRIM(STRING(INTEGER(ENTRY(3, ratecode.char1[4], ";")),">>9"))
              .
            END.
            
            IF NUM-ENTRIES(ratecode.char1[1], ";") GE 2 THEN    /*Early Booking Discount*/
            DO:
              CREATE t-viewrates-line.
              DO n = 1 TO NUM-ENTRIES(ratecode.char1[1], ";") - 1:
                ct = ENTRY(n, ratecode.char1[1], ";").
                disc-rate = DECIMAL(ENTRY(1, ct, ",")) / 100.
            
                IF AVAILABLE queasy THEN t-viewrates-line.prcode = queasy.char1.
                ASSIGN
                  t-viewrates-line.argt         = arrangement.arrangement
                  t-viewrates-line.rmtype       = zimkateg.kurzbez
                  t-viewrates-line.datum        = "EARLY BOOKING :"
                  t-viewrates-line.str-aci      = "Discount% / Advance Minimum Booking (Day) / Minimum Stay / Up To Occupancy"
                  t-viewrates-line.adult-rate   = TRIM(STRING(disc-rate,">9.99 "))
                  t-viewrates-line.child-rate   = TRIM(STRING(INTEGER(ENTRY(2, ct, ",")),">>>>>>>>9"))
                  t-viewrates-line.infant-rate  = TRIM(STRING(INTEGER(ENTRY(3, ct, ",")),">>>>>9"))   
                  t-viewrates-line.deci4        = TRIM(STRING(INTEGER(ENTRY(4, ct, ",")),">>>>>>9")) 
                .
              END.
            END. 
            
            IF NUM-ENTRIES(ratecode.char1[2], ";") GE 2 THEN
            DO:
              CREATE t-viewrates-line.
              DO n = 1 TO NUM-ENTRIES(ratecode.char1[2], ";") - 1:
                ct = ENTRY(n, ratecode.char1[2], ";").
                disc-rate = DECIMAL(ENTRY(1, ct, ",")) / 100.
                
                IF AVAILABLE queasy THEN t-viewrates-line.prcode = queasy.char1.
                ASSIGN
                  t-viewrates-line.argt         = arrangement.arrangement
                  t-viewrates-line.rmtype       = zimkateg.kurzbez
                  t-viewrates-line.datum        = "KICKBACK DISCOUNT :"
                  t-viewrates-line.str-aci      = "Discount% / Advance Maximum Booking (Day) / Minimum Stay / Up To Occupancy"
                  t-viewrates-line.adult-rate   = TRIM(STRING(disc-rate,">9.99"))
                  t-viewrates-line.child-rate   = TRIM(STRING(INTEGER(ENTRY(2, ct, ",")),">>>>>>>>9"))
                  t-viewrates-line.infant-rate  = TRIM(STRING(INTEGER(ENTRY(3, ct, ",")),">>>>>9"))   
                  t-viewrates-line.deci4        = TRIM(STRING(INTEGER(ENTRY(4, ct, ",")),">>>>>>9")) 
                .
              END.
            END.
            
            IF NUM-ENTRIES(ratecode.char1[3], ";") GE 2 THEN
            DO:
              CREATE t-viewrates-line.
              DO n = 1 TO NUM-ENTRIES(ratecode.char1[3], ";") - 1:
                ct = ENTRY(n, ratecode.char1[3], ";").
                f-date = DATE(INTEGER(SUBSTR(ENTRY(1, ct, ","),5,2)),
                              INTEGER(SUBSTR(ENTRY(1, ct, ","),7,2)), 
                              INTEGER(SUBSTR(ENTRY(1, ct, ","),1,4))).
                t-date = DATE(INTEGER(SUBSTR(ENTRY(2, ct, ","),5,2)),
                              INTEGER(SUBSTR(ENTRY(2, ct, ","),7,2)), 
                              INTEGER(SUBSTR(ENTRY(2, ct, ","),1,4))).
                
                IF AVAILABLE queasy THEN t-viewrates-line.prcode = queasy.char1.
                ASSIGN
                  t-viewrates-line.argt         = arrangement.arrangement
                  t-viewrates-line.rmtype       = zimkateg.kurzbez
                  t-viewrates-line.datum        = "STAY/PAY :"
                  t-viewrates-line.adult-rate   = STRING(f-date) + " - " + STRING(t-date)                    
                  t-viewrates-line.child-rate   = TRIM(STRING(INTEGER(ENTRY(3, ct, ",")),">>>9"))          
                  t-viewrates-line.infant-rate  = TRIM(STRING(INTEGER(ENTRY(4, ct, ",")),">>>9"))                 
                .
              END.
            END.                              
          END.            
          argt1 = ratecode.argtnr. 
          zikat1 = ratecode.zikatnr.
        END.
      END.
    
      FOR EACH reslin-queasy WHERE reslin-queasy.key = "argt-line" 
        AND reslin-queasy.char1 = pr-code AND reslin-queasy.number1 = prtable.marknr 
        AND reslin-queasy.number2 =  select-list.argtnr 
        AND reslin-queasy.reslinnr = select-list.zikatnr NO-LOCK 
        USE-INDEX argt_ix 
        BY reslin-queasy.resnr BY reslin-queasy.number3 BY reslin-queasy.date1: 
        queasy-exist = YES. 
        FIND FIRST artikel WHERE artikel.artnr = reslin-queasy.number3 
          AND artikel.departement = reslin-queasy.resnr NO-LOCK. 
        FIND FIRST argt-line WHERE argt-line.argtnr = select-list.argtnr 
          AND argt-line.argt-artnr = artikel.artnr 
          AND argt-line.departement = artikel.departement NO-LOCK NO-ERROR. 
    
        IF ci-date LE reslin-queasy.date2 AND do-it THEN
        DO:
          CREATE t-viewrates-line.
          ASSIGN
            t-viewrates-line.prcode   = queasy.char1
            t-viewrates-line.argt     = arrangement.arrangement
            t-viewrates-line.rmtype   = zimkateg.kurzbez
            t-viewrates-line.datum    = STRING(reslin-queasy.date1, "99/99/99") 
                                      + " - " + STRING(reslin-queasy.date2, "99/99/99")
            t-viewrates-line.str-aci  = artikel.bezeich
            t-viewrates-line.aci      = "Rate : " + TRIM(STRING(reslin-queasy.deci1, ">>>,>>>,>>9.99"))          
          .
    
          IF AVAILABLE argt-line THEN
          DO:          
            t-viewrates-line.str-rate-aci = "Posted : " + STRING(argt-line.fakt-modus, "9").
            IF argt-line.fakt-modus = 6 THEN
              t-viewrates-line.str-rate-aci = t-viewrates-line.str-rate-aci + "/" +
                STRING(argt-line.intervall, "9").
            ELSE
              t-viewrates-line.adult-rate = "Rate Include : " + STRING(argt-line.kind1,"Yes/No").
              t-viewrates-line.child-rate = "Optional : " + STRING(argt-line.kind2,"Yes/No").
            
            IF argt-line.betriebsnr = 0 THEN
              t-viewrates-line.infant-rate = "Qty Always 1 : No". 
            ELSE
              t-viewrates-line.infant-rate = "Qty Always 1 : Yes".
          END.
        END.
      END.
    
      IF NOT queasy-exist THEN
      DO:
        FOR EACH argt-line WHERE argt-line.argtnr = argt1 NO-LOCK:        
          FIND FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
            AND artikel.departement = argt-line.departement NO-LOCK.
    
          CREATE t-viewrates-line.
          ASSIGN
            t-viewrates-line.prcode = queasy.char1
            t-viewrates-line.argt   = arrangement.arrangement
            t-viewrates-line.rmtype = zimkateg.kurzbez
          .

          IF argt-line.vt-percnt = 0 THEN
          DO:
            ASSIGN
              t-viewrates-line.datum          = "" + " - " + ""
              t-viewrates-line.str-aci        = artikel.bezeich
              t-viewrates-line.aci            = "Adult Rate : " + TRIM(STRING(argt-line.betrag, ">>>,>>>,>>9.99"))
              t-viewrates-line.str-rate-aci   = "Posted : " + STRING(argt-line.fakt-modus, "9")            
            .
          END.
          ELSE IF argt-line.vt-percnt = 1 THEN
          DO:
            ASSIGN
              t-viewrates-line.datum          = "" + " - " + ""
              t-viewrates-line.str-aci        = artikel.bezeich
              t-viewrates-line.aci            = "Child Rate : " + TRIM(STRING(argt-line.betrag, ">>>,>>>,>>9.99"))
              t-viewrates-line.str-rate-aci   = "Posted : " + STRING(argt-line.fakt-modus, "9")            
            .
          END.
          ELSE IF argt-line.vt-percnt = 2 THEN
          DO:
            ASSIGN
              t-viewrates-line.datum          = "" + " - " + ""
              t-viewrates-line.str-aci        = artikel.bezeich
              t-viewrates-line.aci            = "Infant Rate : " + TRIM(STRING(argt-line.betrag, ">>>,>>>,>>9.99"))
              t-viewrates-line.str-rate-aci   = "Posted : " + STRING(argt-line.fakt-modus, "9")            
            .
          END.
    
          IF argt-line.fakt-modus = 6 THEN
            t-viewrates-line.str-rate-aci = t-viewrates-line.str-rate-aci + "/" +
              STRING(argt-line.intervall, "9").
          ELSE
            t-viewrates-line.adult-rate = "Rate Include : " + STRING(argt-line.kind1,"Yes/No").
            t-viewrates-line.child-rate = "Optional : " + STRING(argt-line.kind2,"Yes/No").
    
          IF argt-line.betriebsnr = 0 THEN
            t-viewrates-line.infant-rate = "Qty Always 1 : No". 
          ELSE
            t-viewrates-line.infant-rate = "Qty Always 1 : Yes".
        END.
      END.
    END.
  END.
END PROCEDURE.


PROCEDURE create-list: 
DEFINE VARIABLE marknr1             AS INTEGER INITIAL 0. 
DEFINE VARIABLE argt1               AS INTEGER INITIAL 0. 
DEFINE VARIABLE zikat1              AS INTEGER INITIAL 0. 
DEFINE VARIABLE i                   AS INTEGER.
DEFINE VARIABLE n                   AS INTEGER.

DEFINE VARIABLE ct                  AS CHAR.
DEFINE VARIABLE st                  AS CHAR.
DEFINE VARIABLE curr-str            AS CHAR.
DEFINE VARIABLE currency            AS CHAR.

DEFINE VARIABLE f-date              AS DATE.
DEFINE VARIABLE t-date              AS DATE.

DEFINE VARIABLE disc-rate           AS DECIMAL.
DEFINE VARIABLE rate                AS DECIMAL. 

DEFINE VARIABLE queasy-exist        AS LOGICAL INITIAL NO. 
DEFINE VARIABLE fixed-rate          AS LOGICAL INITIAL NO NO-UNDO. 
DEFINE VARIABLE do-it               AS LOGICAL INITIAL NO NO-UNDO.

DEFINE BUFFER qsy FOR queasy.

  FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
  ci-date = htparam.fdate.    

  FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK.
  comments = guest.bemerk.

  FOR EACH guest-pr WHERE guest-pr.gastnr = gastnr NO-LOCK BY guest-pr.CODE:
    pr-code = guest-pr.CODE.

    FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = pr-code NO-LOCK.
    FIND FIRST waehrung WHERE waehrung.waehrungsnr = queasy.number1 NO-LOCK NO-ERROR.

    CREATE t-viewrates.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN
            t-viewrates.prcode      = queasy.char1
            t-viewrates.desc-prcode = queasy.char2.
    END.
    IF AVAILABLE waehrung THEN
    DO:
        t-viewrates.currency = waehrung.bezeich.
    END.

    FOR EACH prtable WHERE prtable.prcode = pr-code NO-LOCK, 
      FIRST prmarket WHERE prmarket.nr = prtable.marknr 
      AND prmarket.bezeich = market-combo NO-LOCK 
      BY prmarket.bezeich:

      RUN create-selectlist.
  
      FIND FIRST qsy WHERE qsy.key = 18 AND qsy.number1 = prmarket.nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE qsy THEN 
      DO: 
        currency = qsy.char3. 
        fixed-rate = qsy.logi3. 
      END.
      
      FOR EACH select-list BY select-list.argtnr BY select-list.zikatnr: 
        FIND FIRST arrangement WHERE arrangement.argtnr = select-list.argtnr 
          NO-LOCK. 
        FIND FIRST zimkateg WHERE zimkateg.zikatnr = select-list.zikatnr NO-LOCK. 
        ASSIGN
          argt1        = 0 
          zikat1       = 0 
          queasy-exist = NO
        . 
        
        FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = prtable.prcode NO-ERROR.
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = queasy.number1 NO-LOCK NO-ERROR.
      
        FIND FIRST t-viewrates WHERE t-viewrates.prcode = pr-code
          AND t-viewrates.argt = arrangement.arrangement
          AND t-viewrates.rmtype = zimkateg.kurzbez NO-LOCK NO-ERROR.
        IF NOT AVAILABLE t-viewrates THEN
        DO:
          CREATE t-viewrates.
          IF AVAILABLE queasy THEN
          DO:
            ASSIGN
              t-viewrates.prcode      = queasy.char1
              t-viewrates.desc-prcode = queasy.char2
            .
          END.
          IF AVAILABLE waehrung THEN t-viewrates.currency = waehrung.bezeich.
          
          IF currency NE "" THEN 
            t-viewrates.market = prmarket.bezeich + " - " + "Currency" + " = " + qsy.char3.
          IF fixed-rate THEN
            t-viewrates.market = prmarket.bezeich + "; " + "Fixed Rate for whole stay".
          
          ASSIGN
            t-viewrates.argt         = arrangement.arrangement
            t-viewrates.rmtype       = zimkateg.kurzbez        
          .
        END.

        FOR EACH ratecode WHERE ratecode.code = pr-code 
          AND ratecode.marknr = prtable.marknr 
          AND ratecode.zikatnr = select-list.zikatnr 
          AND ratecode.argtnr = select-list.argtnr NO-LOCK 
          BY ratecode.startperiode BY ratecode.wday: 
          
          do-it = (ci-date LE ratecode.endperiode). 
          IF do-it THEN
          DO:
            CREATE t-viewrates-line. 

            IF AVAILABLE queasy THEN
            DO:
              ASSIGN
                t-viewrates-line.prcode      = queasy.char1
                t-viewrates-line.desc-prcode = queasy.char2
              .
            END.
            IF AVAILABLE waehrung THEN t-viewrates-line.currency = waehrung.bezeich.
            
            IF currency NE "" THEN 
              t-viewrates-line.market = prmarket.bezeich + " - " + "Currency" + " = " + qsy.char3.
            IF fixed-rate THEN
              t-viewrates-line.market = prmarket.bezeich + "; " + "Fixed Rate for whole stay".
            
            ASSIGN
              t-viewrates-line.argt         = arrangement.arrangement
              t-viewrates-line.rmtype       = zimkateg.kurzbez
              t-viewrates-line.datum        = STRING(ratecode.startperiode, "99/99/99")
                                               + " - " + STRING(ratecode.endperiode, "99/99/99")
              t-viewrates-line.str-aci      = "Adult/Child/Infant :"
              t-viewrates-line.aci          = STRING(ratecode.erwachs) + "/" + STRING(ratecode.kind1) + "/"
                                               + STRING(ratecode.kind2)
              t-viewrates-line.str-rate-aci = "Adult Rate/Child Rate/Infant Rate :"
              t-viewrates-line.adult-rate   = TRIM(STRING(ratecode.zipreis, ">>>,>>>,>>9.99"))
              t-viewrates-line.child-rate   = TRIM(STRING(ratecode.ch1preis, ">>>,>>>,>>9.99"))
              t-viewrates-line.infant-rate  = TRIM(STRING(ratecode.ch2preis, ">>>,>>>,>>9.99"))
            .  
            
            IF ratecode.char1[1] NE "" OR ratecode.char1[2] NE ""
              OR ratecode.char1[3] NE "" OR ratecode.char1[4] NE "" THEN
            DO:          
              IF NUM-ENTRIES(ratecode.char1[4], ";") GE 3 THEN 
              DO: 
                CREATE t-viewrates-line.
                IF AVAILABLE queasy THEN t-viewrates-line.prcode = queasy.char1.
                ASSIGN
                  t-viewrates-line.argt         = arrangement.arrangement
                  t-viewrates-line.rmtype       = zimkateg.kurzbez
                  t-viewrates-line.datum        = "COMPLIMENT ROOM :"
                  t-viewrates-line.str-aci      = "Room Booked / Get Compliment / Tpotal Compliment :"
                  t-viewrates-line.adult-rate   = TRIM(STRING(INTEGER(ENTRY(1, ratecode.char1[4], ";")),">>9"))           
                  t-viewrates-line.child-rate   = TRIM(STRING(INTEGER(ENTRY(2, ratecode.char1[4], ";")),">>9")) 
                  t-viewrates-line.infant-rate  = TRIM(STRING(INTEGER(ENTRY(3, ratecode.char1[4], ";")),">>9"))
                .
              END.
              
              IF NUM-ENTRIES(ratecode.char1[1], ";") GE 2 THEN    /*Early Booking Discount*/
              DO:
                CREATE t-viewrates-line.
                DO n = 1 TO NUM-ENTRIES(ratecode.char1[1], ";") - 1:
                  ct = ENTRY(n, ratecode.char1[1], ";").
                  disc-rate = DECIMAL(ENTRY(1, ct, ",")) / 100.
              
                  IF AVAILABLE queasy THEN t-viewrates-line.prcode = queasy.char1.
                  ASSIGN
                    t-viewrates-line.argt         = arrangement.arrangement
                    t-viewrates-line.rmtype       = zimkateg.kurzbez
                    t-viewrates-line.datum        = "EARLY BOOKING :"
                    t-viewrates-line.str-aci      = "Discount% / Advance Minimum Booking (Day) / Minimum Stay / Up To Occupancy"
                    t-viewrates-line.adult-rate   = TRIM(STRING(disc-rate,">9.99 "))
                    t-viewrates-line.child-rate   = TRIM(STRING(INTEGER(ENTRY(2, ct, ",")),">>>>>>>>9"))
                    t-viewrates-line.infant-rate  = TRIM(STRING(INTEGER(ENTRY(3, ct, ",")),">>>>>9"))   
                    t-viewrates-line.deci4        = TRIM(STRING(INTEGER(ENTRY(4, ct, ",")),">>>>>>9")) 
                  .
                END.
              END. 
              
              IF NUM-ENTRIES(ratecode.char1[2], ";") GE 2 THEN
              DO:
                CREATE t-viewrates-line.
                DO n = 1 TO NUM-ENTRIES(ratecode.char1[2], ";") - 1:
                  ct = ENTRY(n, ratecode.char1[2], ";").
                  disc-rate = DECIMAL(ENTRY(1, ct, ",")) / 100.
                  
                  IF AVAILABLE queasy THEN t-viewrates-line.prcode = queasy.char1.
                  ASSIGN
                    t-viewrates-line.argt         = arrangement.arrangement
                    t-viewrates-line.rmtype       = zimkateg.kurzbez
                    t-viewrates-line.datum        = "KICKBACK DISCOUNT :"
                    t-viewrates-line.str-aci      = "Discount% / Advance Maximum Booking (Day) / Minimum Stay / Up To Occupancy"
                    t-viewrates-line.adult-rate   = TRIM(STRING(disc-rate,">9.99"))
                    t-viewrates-line.child-rate   = TRIM(STRING(INTEGER(ENTRY(2, ct, ",")),">>>>>>>>9"))
                    t-viewrates-line.infant-rate  = TRIM(STRING(INTEGER(ENTRY(3, ct, ",")),">>>>>9"))   
                    t-viewrates-line.deci4        = TRIM(STRING(INTEGER(ENTRY(4, ct, ",")),">>>>>>9")) 
                  .
                END.
              END.
              
              IF NUM-ENTRIES(ratecode.char1[3], ";") GE 2 THEN
              DO:
                CREATE t-viewrates-line.
                DO n = 1 TO NUM-ENTRIES(ratecode.char1[3], ";") - 1:
                  ct = ENTRY(n, ratecode.char1[3], ";").
                  f-date = DATE(INTEGER(SUBSTR(ENTRY(1, ct, ","),5,2)),
                                INTEGER(SUBSTR(ENTRY(1, ct, ","),7,2)), 
                                INTEGER(SUBSTR(ENTRY(1, ct, ","),1,4))).
                  t-date = DATE(INTEGER(SUBSTR(ENTRY(2, ct, ","),5,2)),
                                INTEGER(SUBSTR(ENTRY(2, ct, ","),7,2)), 
                                INTEGER(SUBSTR(ENTRY(2, ct, ","),1,4))).
                  
                  IF AVAILABLE queasy THEN t-viewrates-line.prcode = queasy.char1.
                  ASSIGN
                    t-viewrates-line.argt         = arrangement.arrangement
                    t-viewrates-line.rmtype       = zimkateg.kurzbez
                    t-viewrates-line.datum        = "STAY/PAY :"
                    t-viewrates-line.adult-rate   = STRING(f-date) + " - " + STRING(t-date)                    
                    t-viewrates-line.child-rate   = TRIM(STRING(INTEGER(ENTRY(3, ct, ",")),">>>9"))          
                    t-viewrates-line.infant-rate  = TRIM(STRING(INTEGER(ENTRY(4, ct, ",")),">>>9"))                 
                  .
                END.  
              END.                                      
            END.      
             
            argt1 = ratecode.argtnr. 
            zikat1 = ratecode.zikatnr.
          END.          
        END.

        FOR EACH reslin-queasy WHERE reslin-queasy.key = "argt-line" 
          AND reslin-queasy.char1 = pr-code AND reslin-queasy.number1 = prtable.marknr 
          AND reslin-queasy.number2 =  select-list.argtnr 
          AND reslin-queasy.reslinnr = select-list.zikatnr NO-LOCK 
          USE-INDEX argt_ix 
          BY reslin-queasy.resnr BY reslin-queasy.number3 BY reslin-queasy.date1: 
          queasy-exist = YES. 
          FIND FIRST artikel WHERE artikel.artnr = reslin-queasy.number3 
            AND artikel.departement = reslin-queasy.resnr NO-LOCK. 
          FIND FIRST argt-line WHERE argt-line.argtnr = select-list.argtnr 
            AND argt-line.argt-artnr = artikel.artnr 
            AND argt-line.departement = artikel.departement NO-LOCK NO-ERROR. 
    
          IF ci-date LE reslin-queasy.date2 AND do-it THEN
          DO:
            CREATE t-viewrates-line.
            ASSIGN
              t-viewrates-line.prcode = queasy.char1
              t-viewrates-line.argt   = arrangement.arrangement
              t-viewrates-line.rmtype = zimkateg.kurzbez            
              t-viewrates-line.datum    = STRING(reslin-queasy.date1, "99/99/99") 
                                        + " - " + STRING(reslin-queasy.date2, "99/99/99")
              t-viewrates-line.str-aci  = artikel.bezeich
              t-viewrates-line.aci      = "Rate : " + TRIM(STRING(reslin-queasy.deci1, ">>>,>>>,>>9.99"))          
            .
    
            IF AVAILABLE argt-line THEN
            DO:          
              t-viewrates-line.str-rate-aci = "Posted : " + STRING(argt-line.fakt-modus, "9").
              IF argt-line.fakt-modus = 6 THEN
                t-viewrates-line.str-rate-aci = t-viewrates-line.str-rate-aci + "/" +
                  STRING(argt-line.intervall, "9").
              ELSE
                t-viewrates-line.adult-rate = "Rate Include : " + STRING(argt-line.kind1,"Yes/No").
                t-viewrates-line.child-rate = "Optional : " + STRING(argt-line.kind2,"Yes/No").
              
              IF argt-line.betriebsnr = 0 THEN
                t-viewrates-line.infant-rate = "Qty Always 1 : No". 
              ELSE
                t-viewrates-line.infant-rate = "Qty Always 1 : Yes".
            END.
          END.
        END.
    
        IF NOT queasy-exist THEN
        DO:            
          FOR EACH argt-line WHERE argt-line.argtnr = argt1 NO-LOCK:            
            FIND FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
              AND artikel.departement = argt-line.departement NO-LOCK.
    
            CREATE t-viewrates-line.
            ASSIGN
              t-viewrates-line.prcode = queasy.char1
              t-viewrates-line.argt   = arrangement.arrangement
              t-viewrates-line.rmtype = zimkateg.kurzbez
            .

            IF argt-line.vt-percnt = 0 THEN
            DO:
              ASSIGN
                t-viewrates-line.datum          = "" + " - " + ""
                t-viewrates-line.str-aci        = artikel.bezeich
                t-viewrates-line.aci            = "Adult Rate : " + TRIM(STRING(argt-line.betrag, ">>>,>>>,>>9.99"))
                t-viewrates-line.str-rate-aci   = "Posted : " + STRING(argt-line.fakt-modus, "9")            
              .
            END.    
            ELSE IF argt-line.vt-percnt = 1 THEN
            DO:
              ASSIGN
                t-viewrates-line.datum          = "" + " - " + ""
                t-viewrates-line.str-aci        = artikel.bezeich
                t-viewrates-line.aci            = "Child Rate : " + TRIM(STRING(argt-line.betrag, ">>>,>>>,>>9.99"))
                t-viewrates-line.str-rate-aci   = "Posted : " + STRING(argt-line.fakt-modus, "9")            
              .
            END.   
            ELSE IF argt-line.vt-percnt = 2 THEN
            DO:
              ASSIGN
                t-viewrates-line.datum          = "" + " - " + ""
                t-viewrates-line.str-aci        = artikel.bezeich
                t-viewrates-line.aci            = "Infant Rate : " + TRIM(STRING(argt-line.betrag, ">>>,>>>,>>9.99"))
                t-viewrates-line.str-rate-aci   = "Posted : " + STRING(argt-line.fakt-modus, "9")            
              .
            END.
    
            IF argt-line.fakt-modus = 6 THEN
              t-viewrates-line.str-rate-aci = t-viewrates-line.str-rate-aci + "/" +
                STRING(argt-line.intervall, "9").
            ELSE
              t-viewrates-line.adult-rate = "Rate Include : " + STRING(argt-line.kind1,"Yes/No").
              t-viewrates-line.child-rate = "Optional : " + STRING(argt-line.kind2,"Yes/No").
    
            IF argt-line.betriebsnr = 0 THEN
              t-viewrates-line.infant-rate = "Qty Always 1 : No". 
            ELSE
              t-viewrates-line.infant-rate = "Qty Always 1 : Yes".
          END.
        END.
      END.
    END.
  END.
END PROCEDURE.

PROCEDURE create-selectlist: 
DEFINE VARIABLE i           AS INTEGER  NO-UNDO.
DEFINE VARIABLE length-str  AS INTEGER  NO-UNDO.
DEFINE VARIABLE help-str    AS CHAR     NO-UNDO.
DEFINE VARIABLE product-str AS CHAR     NO-UNDO.

  FOR EACH select-list: 
    DELETE select-list. 
  END. 

  DO i = 1 TO 99: 
    IF prtable.product[i] NE 0 THEN 
    DO: 
      CREATE select-list. 
      ASSIGN product-str = STRING(prtable.product[i]).
      IF LENGTH(product-str) = 3 THEN
      ASSIGN
        select-list.zikatnr = INTEGER(SUBSTR(product-str,1,1))
        select-list.argtnr  = INTEGER(SUBSTR(product-str,2))
      .
      ELSE IF LENGTH(product-str) = 4 THEN 
      DO:
        RUN get-zikat-argt (prtable.product[i],
            OUTPUT select-list.zikatnr,
            OUTPUT select-list.argtnr).
        IF select-list.zikatnr = 0 OR select-list.argtnr = 0 THEN
            DELETE select-list.
      END.
      ELSE IF LENGTH(product-str) = 5 THEN
      ASSIGN
        select-list.zikatnr = INTEGER(SUBSTR(product-str,1,2))
        select-list.argtnr  = INTEGER(SUBSTR(product-str,3))
      .
      ELSE IF LENGTH(product-str) = 6 THEN
      ASSIGN
        select-list.zikatnr = INTEGER(SUBSTR(product-str,2,2))
        select-list.argtnr  = INTEGER(SUBSTR(product-str,4))
      .

      IF select-list.zikatnr GE 91 THEN 
          select-list.zikatnr = select-list.zikatnr - 90.

    END. 
  END. 
END. 

PROCEDURE get-zikat-argt:
DEF INPUT  PARAMETER curr-product AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER i-zikatnr    AS INTEGER NO-UNDO INIT 0.
DEF OUTPUT PARAMETER i-argtnr     AS INTEGER NO-UNDO INIT 0.
.
DEF VAR i           AS INTEGER NO-UNDO.
DEF VAR j           AS INTEGER NO-UNDO.
DEF VAR k           AS INTEGER NO-UNDO.
DEF VAR n           AS INTEGER NO-UNDO.
DEF VAR num-found1  AS INTEGER NO-UNDO.
DEF VAR num-found2  AS INTEGER NO-UNDO.

DEF VAR i-zikatnr1  AS INTEGER NO-UNDO.
DEF VAR i-argtnr1   AS INTEGER NO-UNDO.
DEF VAR i-zikatnr2  AS INTEGER NO-UNDO.
DEF VAR i-argtnr2   AS INTEGER NO-UNDO.
DEF VAR found1      AS LOGICAL NO-UNDO.
DEF VAR found2      AS LOGICAL NO-UNDO.
DEF VAR str         AS CHAR    NO-UNDO.

  IF curr-product GE 90000 THEN
  ASSIGN
    num-found1 = 0
    num-found2 = 0
    str        = STRING(curr-product)
    i-zikatnr1 = INTEGER(SUBSTR(str,1,2)) - 90
    i-argtnr1  = INTEGER(SUBSTR(str,3))
  .
  ELSE IF curr-product GE 10000 THEN
  ASSIGN
    num-found1 = 0
    num-found2 = 0
    str        = STRING(curr-product)
    i-zikatnr1 = INTEGER(SUBSTR(str,1,2))
    i-argtnr1  = INTEGER(SUBSTR(str,3))
  .
  ELSE
  ASSIGN
    num-found1 = 0
    num-found2 = 0
    str        = STRING(curr-product)
    i-zikatnr1 = INTEGER(SUBSTR(str,1,1))
    i-argtnr1  = INTEGER(SUBSTR(str,2))
  .
  
  IF i-argtnr1 GE 100 THEN
  DO:
    DO j = 1 TO 99:
      IF i-zikatnr1 = prtable.zikatnr[j] THEN
      DO:
        num-found1 = num-found1 + 1.
        j = 999.
      END.
    END.
    DO j = 1 TO 99:
      IF i-argtnr1 = prtable.argtnr[j] THEN
      DO:
        num-found1 = num-found1 + 2.
        j = 999.
      END.
    END.
  END.
  ASSIGN
    i-zikatnr2 = INTEGER(SUBSTR(str,1,2))
    i-argtnr2  = INTEGER(SUBSTR(str,3))
  .
  DO j = 1 TO 99:
    IF i-zikatnr2 = prtable.zikatnr[j] THEN
    DO:
      num-found2 = num-found2 + 1.
      j = 999.
    END.
  END.
  DO j = 1 TO 99:
    IF i-argtnr2 = prtable.argtnr[j] THEN
    DO:
      num-found2 = num-found2 + 2.
      j = 999.
    END.
  END.
  IF num-found1 = 3 AND num-found2 NE 3 THEN
  DO:
    i-zikatnr = i-zikatnr1.
    i-argtnr  = i-zikatnr1.
    RETURN.
  END.
  ELSE IF num-found1 NE 3 AND num-found2 = 3 THEN
  DO:
    i-zikatnr = i-zikatnr2.
    i-argtnr  = i-zikatnr2.
    RETURN.
  END.
  ELSE 
  DO:
    FIND FIRST ratecode WHERE ratecode.CODE = prtable.prcode
        AND ratecode.zikatnr = i-zikatnr1
        AND ratecode.argtnr = i-argtnr1 NO-LOCK NO-ERROR.
    IF AVAILABLE ratecode THEN
    DO:
      i-zikatnr = i-zikatnr1.
      i-argtnr  = i-zikatnr1.
      RETURN.
    END.
    FIND FIRST ratecode WHERE ratecode.CODE = prtable.prcode
        AND ratecode.zikatnr = i-zikatnr2
        AND ratecode.argtnr = i-argtnr2 NO-LOCK NO-ERROR.
    IF AVAILABLE ratecode THEN
    DO:
      i-zikatnr = i-zikatnr2.
      i-argtnr  = i-zikatnr2.
    END.
  END.
END.
