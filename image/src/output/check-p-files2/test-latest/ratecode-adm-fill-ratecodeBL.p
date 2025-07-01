
DEFINE TEMP-TABLE p-list LIKE ratecode
    FIELD s-recid        AS INTEGER INIT 0. /*M real ratecode */

DEFINE TEMP-TABLE early-discount
    FIELD disc-rate AS DECIMAL FORMAT ">9.99" LABEL "Disc%"
    FIELD min-days  AS INTEGER FORMAT ">>>"   LABEL "Min to C/I(days)"
    FIELD min-stay  AS INTEGER FORMAT ">>>"   LABEL "Min Stays"
    FIELD max-occ   AS INTEGER FORMAT " >>"   LABEL "Upto Occ"
    FIELD from-date AS DATE                   LABEL "Fr BookDate"
    FIELD to-date   AS DATE                   LABEL "To BookDate".

DEFINE TEMP-TABLE kickback-discount
    FIELD disc-rate AS DECIMAL FORMAT ">9.99" LABEL "Disc%"
    FIELD max-days  AS INTEGER FORMAT ">>>"   LABEL "Max to C/I(days)"
    FIELD min-stay  AS INTEGER FORMAT ">>>"   LABEL "Min Stays"
    FIELD max-occ   AS INTEGER FORMAT " >>"   LABEL "Upto Occ".

DEFINE TEMP-TABLE stay-pay
    FIELD f-date    AS DATE                      LABEL "FromDate"
    FIELD t-date    AS DATE                      LABEL "ToDate"
    FIELD stay      AS INTEGER FORMAT "     >>>" LABEL "Stay(Nights)"
    FIELD pay       AS INTEGER FORMAT "     >>>" LABEL "Pay(Nights)".

DEFINE TEMP-TABLE child-list
    FIELD child-code AS CHAR
    FIELD true-child AS LOGICAL INIT YES
    FIELD argt-no    AS INTEGER
    FIELD zikat-no   AS INTEGER
.
DEFINE TEMP-TABLE child-ratecode LIKE ratecode.

DEFINE TEMP-TABLE q-list
    FIELD rcode         AS CHAR
    FIELD dcode         AS CHAR.

DEFINE TEMP-TABLE r-list LIKE q-list.

DEFINE INPUT PARAMETER user-init    AS CHAR      NO-UNDO. 
DEFINE INPUT PARAMETER prcode       AS CHAR      NO-UNDO. 
DEFINE INPUT PARAMETER market-nr    AS INTEGER   NO-UNDO. 
DEFINE INPUT PARAMETER zikatnr      AS INTEGER   NO-UNDO. 
DEFINE INPUT PARAMETER argtnr       AS INTEGER   NO-UNDO. 
DEFINE INPUT PARAMETER book-room    AS INTEGER   NO-UNDO. 
DEFINE INPUT PARAMETER comp-room    AS INTEGER   NO-UNDO. 
DEFINE INPUT PARAMETER max-room     AS INTEGER   NO-UNDO. 
DEFINE INPUT PARAMETER TABLE FOR early-discount.
DEFINE INPUT PARAMETER TABLE FOR kickback-discount.
DEFINE INPUT PARAMETER TABLE FOR stay-pay.
/*DEFINE OUTPUT PARAMETER error-flag AS LOGICAL NO-UNDO INIT NO.*/ /*naufal*/
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR p-list.

DEF VARIABLE ci-date        AS DATE     NO-UNDO.
DEF VARIABLE round-betrag   AS INTEGER  NO-UNDO.
DEF VARIABLE round-method   AS INTEGER  NO-UNDO INIT 0.
DEF VARIABLE length-round   AS INTEGER  NO-UNDO.
DEF VARIABLE parent-code    AS CHAR     NO-UNDO.
DEF VARIABLE adjust-value   AS DECIMAL  NO-UNDO.
DEF VARIABLE in-percent     AS LOGICAL  NO-UNDO.
DEF VARIABLE chg-allot      AS LOGICAL  NO-UNDO INIT NO.

DEFINE VARIABLE ifTask      AS CHAR INIT "".
DEFINE VARIABLE mesToken    AS CHAR INIT "".
DEFINE VARIABLE mesValue    AS CHAR INIT "".
DEFINE VARIABLE tokcounter  AS INT  INIT 0.
DEFINE VARIABLE cat-flag    AS LOGICAL INIT NO.

/*DODY 310518 add log file*/
DEFINE VARIABLE bef-start   AS DATE.
DEFINE VARIABLE bef-end     AS DATE.
DEFINE VARIABLE bef-pax     AS INT.
DEFINE VARIABLE bef-rate    AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tax-included AS LOGICAL INITIAL NO NO-UNDO.

DEFINE BUFFER qsy     FOR queasy.
DEFINE BUFFER rbuff   FOR ratecode.
DEFINE BUFFER q-curr  FOR queasy.
DEFINE BUFFER tb3-buff FOR ratecode. /* Malik Serverless 313 change buffer name : tb3Buff  -> tb3-buff */

FIND FIRST p-list.

FIND FIRST qsy WHERE qsy.KEY = 152 NO-LOCK NO-ERROR.
IF AVAILABLE qsy THEN cat-flag = YES.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
ASSIGN ci-date = htparam.fdate.

FIND FIRST htparam WHERE htparam.paramnr = 1013 NO-LOCK.
IF htparam.feldtyp = 1 THEN
ASSIGN 
    round-betrag = htparam.finteger
    length-round = LENGTH(STRING(round-betrag))
.
ELSE IF htparam.feldtyp = 5 AND NUM-ENTRIES(htparam.fchar,";") GT 1 THEN
ASSIGN 
    round-betrag = INTEGER(ENTRY(1, htparam.fchar,";"))
    length-round = LENGTH(STRING(round-betrag))
    round-method = INTEGER(ENTRY(2, htparam.fchar,";")) NO-ERROR
.


FIND FIRST htparam WHERE htparam.paramnr = 127 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
tax-included = htparam.flogical.

/*naufal*//*
RUN check-overlapping.
IF error-flag THEN RETURN.
*/ 
RUN create-child-list.
RUN fill-ratecode.
RUN update-child-ratecode.
RUN update-bookengine-config.
/*naufal*/
/*
PROCEDURE check-overlapping:
    FIND FIRST ratecode WHERE ratecode.marknr EQ market-nr
        AND ratecode.CODE    EQ prcode
        AND ratecode.argtnr  EQ argtnr
        AND ratecode.zikatnr EQ zikatnr
        AND ratecode.erwachs EQ p-list.erwachs 
        AND ratecode.kind1   EQ p-list.kind1
        AND ratecode.kind2   EQ p-list.kind2
        AND ratecode.wday    EQ p-list.wday
        AND NOT ratecode.startperiod GE p-list.endperiode
        AND NOT ratecode.endperiod   LE p-list.startperiode NO-LOCK NO-ERROR.
    IF AVAILABLE ratecode THEN
    DO:
        error-flag = YES.
        RETURN.
    END.
END.*/

PROCEDURE create-child-list:
    FOR EACH queasy WHERE queasy.KEY = 2
        AND NOT queasy.logi2
        AND NUM-ENTRIES(queasy.char3, ";") GT 2
        AND ENTRY(2, queasy.char3, ";") = prcode NO-LOCK:
        CREATE child-list.
        ASSIGN child-list.child-code = queasy.char1.
        /* Comment FDL Ticket EA982C - If Parent(have > 1 child) and one of child have not same data ratecode
                                        the data child is not update
        FOR EACH ratecode WHERE ratecode.CODE = queasy.char1 
            AND ratecode.endperiode GE ci-date:
            
            FIND FIRST rbuff WHERE rbuff.marknr = ratecode.marknr 
                AND rbuff.code    = prcode 
                AND rbuff.argtnr  = ratecode.argtnr
                AND rbuff.zikatnr = ratecode.zikatnr
                AND rbuff.erwachs = ratecode.erwachs
                AND rbuff.kind1   = ratecode.kind1
                AND rbuff.kind2   = ratecode.kind2
                AND rbuff.wday    = ratecode.wday
                AND rbuff.startperiode = ratecode.startperiode
                AND rbuff.endperiode   = ratecode.endperiode
                NO-LOCK NO-ERROR.
            IF NOT AVAILABLE rbuff THEN 
            DO:   
                ASSIGN child-list.true-child = NO.
                LEAVE.
            END.
        END.
        */
    END.
END.

PROCEDURE fill-ratecode: 
    DEFINE VARIABLE to-date AS DATE. 
    DEFINE BUFFER pcode1    FOR ratecode. 
    DEFINE VARIABLE ori-allot AS INT.
    DEFINE VARIABLE log-flag AS CHAR.
    DEFINE VARIABLE tmp-kurzbez AS CHAR. /* Malik Serverless 313 */

  to-date = DATE(1,1,1990). /* Malik Serverless 313 : DATE(01,01,1990) -> DATE(1,1,1990) */

  IF p-list.s-recid NE 0 THEN
  DO:
      FIND FIRST ratecode WHERE RECID(ratecode) = p-list.s-recid NO-ERROR.
      IF AVAILABLE ratecode THEN
      DO:
          ASSIGN
            bef-start             = ratecode.startperiode 
            bef-end               = ratecode.endperiode  
            bef-pax               = ratecode.erwach
            bef-rate              = ratecode.zipreis.
      END.
  END.
  ELSE CREATE ratecode.

  IF p-list.s-recid NE 0 THEN
  DO:
    FIND FIRST queasy WHERE queasy.KEY = 2
        AND queasy.char1 = prcode NO-LOCK.
    IF NUM-ENTRIES(queasy.char3, ";") GT 2 THEN
    DO:
        ASSIGN 
            ratecode.startperiode = p-list.startperiode
            ratecode.endperiode   = p-list.endperiode
        .
        RETURN.
    END.
  END.

  FIND FIRST zimkateg WHERE zimkateg.zikatnr EQ p-list.zikatnr NO-LOCK NO-ERROR.  
  /* Malik Serverless 313 */
  IF AVAILABLE zimkateg THEN
  DO:
    tmp-kurzbez = zimkateg.kurzbez.
  END.
  ELSE
  DO:
    tmp-kurzbez = "".
  END. 
  /* END Malik */
  FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
  IF AVAILABLE bediener THEN 
  DO:
      CREATE res-history.
      ASSIGN 
          res-history.nr          = bediener.nr
          res-history.datum       = TODAY
          res-history.zeit        = TIME
          res-history.aenderung   = "Modify Contract Rate, Code: " + prcode + " RmType : " + tmp-kurzbez + /* Malik Serverless 313 : zimkateg.kurzbez -> tmp-kurzbez */
                                    ", FROM : start:" + STRING(bef-start) + "|end:" + STRING(bef-end) + "|adult:" + STRING(bef-pax) + "|rate:" + STRING(bef-rate) + 
                                    ", TO : start:" + STRING(p-list.startperiode) + "|end:" + STRING(p-list.endperiode) + "|adult:" + STRING(p-list.erwachs) + "|rate:" + STRING(p-list.zipreis) 
                                    .
          res-history.action      = "RateCode".
      FIND CURRENT res-history NO-LOCK.
      RELEASE res-history.
  END.

  BUFFER-COPY p-list EXCEPT p-list.argtnr p-list.zikatnr TO ratecode. 
  ASSIGN 
    ratecode.marknr      = market-nr 
    ratecode.code        = prcode 
    ratecode.argtnr      = argtnr 
    ratecode.zikatnr     = zikatnr 
    ratecode.char1[1]    = ""
    ratecode.char1[2]    = ""
    ratecode.char1[3]    = ""
    ratecode.char1[4]    = ""
    ratecode.char1[5]    = user-init
  . 

  IF book-room > 0 THEN 
    ratecode.char1[4] = STRING(book-room) + ";" + STRING(comp-room) + ";" 
      + STRING(max-room) + ";". 
  ELSE ratecode.char1[4] = "". 
  
  FOR EACH early-discount WHERE early-discount.disc-rate NE 0:
    ratecode.char1[1] = ratecode.char1[1] 
      + STRING(early-discount.disc-rate * 100) + ","
      + STRING(early-discount.min-days) + "," + STRING(early-discount.min-stay) + ","
      + STRING(early-discount.max-occ) + ",".
    IF early-discount.from-date NE ? THEN ratecode.char1[1] = ratecode.char1[1]      
      + STRING(YEAR(early-discount.from-date),"9999") 
      + STRING(MONTH(early-discount.from-date),"99")
      + STRING(DAY(early-discount.from-date),"99") + ",".
    ELSE ratecode.char1[1] = ratecode.char1[1] + " ,".
    IF early-discount.to-date NE ? THEN ratecode.char1[1] = ratecode.char1[1]      
      + STRING(YEAR(early-discount.to-date),"9999") 
      + STRING(MONTH(early-discount.to-date),"99")
      + STRING(DAY(early-discount.to-date),"99") + ";".
    ELSE ratecode.char1[1] = ratecode.char1[1] + " ;".
  END.
  
  FOR EACH kickback-discount WHERE kickback-discount.disc-rate NE 0:
    ratecode.char1[2] = ratecode.char1[2]
      + STRING(kickback-discount.disc-rate * 100) + ","
      + STRING(kickback-discount.max-days) + "," + STRING(kickback-discount.min-stay) + ","
      + STRING(kickback-discount.max-occ) + ";".
  END.
  
  FOR EACH stay-pay WHERE stay-pay.stay NE 0:
    ratecode.char1[3] = ratecode.char1[3]
      + STRING(YEAR(stay-pay.f-date),"9999") 
      + STRING(MONTH(stay-pay.f-date),"99") + STRING(DAY(stay-pay.f-date),"99") + ","
      + STRING(YEAR(stay-pay.t-date),"9999") 
      + STRING(MONTH(stay-pay.t-date),"99") + STRING(DAY(stay-pay.t-date),"99") + ","
      + STRING(stay) + "," + STRING(pay) + ";".
  END.

  FOR EACH pcode1 WHERE pcode1.CODE = prcode NO-LOCK: 
      /* Malik Serverless 313 */
      IF pcode1.endperiode NE ? AND to-date NE ? THEN
      DO:  
        IF pcode1.endperiode GT to-date THEN to-date = pcode1.endperiode. 
      END.
      /* END malik */  
  END. 
  IF to-date NE DATE(1,1,1990) THEN /* Malik Serverless 313 : DATE(01,01,1990) -> DATE(1,1,1990) */
  DO: 
    FOR EACH guest-pr WHERE guest-pr.CODE = prcode NO-LOCK: 
      FIND FIRST guest WHERE guest.gastnr = guest-pr.gastnr EXCLUSIVE-LOCK. 
      guest.endperiode = to-date. 
      FIND CURRENT guest NO-LOCK. 
    END. 
  END. 

  FIND FIRST tb3-buff WHERE RECID(tb3-buff) = RECID(ratecode) NO-LOCK.
  
  BUFFER-COPY ratecode TO p-list.
  IF p-list.s-recid = 0 THEN 
      ASSIGN p-list.s-recid = INTEGER(RECID(ratecode)).

END. 
 
PROCEDURE update-child-ratecode:
    DEF VARIABLE beg-datum    AS DATE    NO-UNDO.
    DEF VARIABLE end-datum    AS DATE    NO-UNDO.

    DEF BUFFER rbuff   FOR ratecode.

  FOR EACH child-list WHERE child-list.true-child = NO:      
    FIND FIRST queasy WHERE queasy.KEY = 2
        AND queasy.char1 = child-list.child-code NO-LOCK.
    ASSIGN 
        parent-code  = ENTRY(2, queasy.char3, ";")
        in-percent   = SUBSTR(ENTRY(3, queasy.char3, ";"),1,1) = "%"
        adjust-value = DECIMAL(SUBSTR(ENTRY(3, queasy.char3, ";"),2)) / 100
    .
    FOR EACH ratecode WHERE ratecode.marknr = tb3-buff.marknr 
        AND ratecode.code    = child-list.child-code 
        AND ratecode.argtnr  = tb3-buff.argtnr 
        AND ratecode.zikatnr = tb3-buff.zikatnr
        AND ratecode.erwachs = tb3-buff.erwachs
        AND ratecode.kind1   = tb3-buff.kind1 
        AND ratecode.kind2   = tb3-buff.kind2 
        AND ratecode.wday    = tb3-buff.wday
        AND NOT ratecode.endperiode LT tb3-buff.startperiode
        AND NOT ratecode.startperiode GT tb3-buff.endperiode: 
        IF ratecode.startperiode LT tb3-buff.startperiode THEN
        DO:
            IF ratecode.endperiode LE tb3-buff.endperiode THEN
            DO:
              ASSIGN 
                  end-datum           = ratecode.endperiode
                  ratecode.endperiode = tb3-buff.startperiode - 1.
              CREATE child-ratecode.
              BUFFER-COPY tb3-buff EXCEPT CODE endperiode TO child-ratecode.
              ASSIGN 
                  child-ratecode.CODE       = child-list.child-code
                  child-ratecode.endperiode = end-datum
              .
              RUN set-child-rate.
            END.
            ELSE 
            DO:
              CREATE child-ratecode.
              BUFFER-COPY ratecode EXCEPT startperiode TO child-ratecode.
              ASSIGN 
                  ratecode.endperiode         = tb3-buff.startperiode - 1
                  child-ratecode.startperiode = tb3-buff.endperiode + 1
              .
            END.
        END.
        ELSE IF (ratecode.startperiode GE tb3-buff.startperiode)
          AND (ratecode.endperiode LE tb3-buff.endperiode) THEN
          RUN set-child-rate-1.
        ELSE IF (ratecode.startperiode GE tb3-buff.startperiode)
          AND (ratecode.endperiode GT tb3-buff.endperiode) THEN
        DO:
            ASSIGN
                beg-datum             = ratecode.startperiode
                ratecode.startperiode = tb3-buff.endperiode + 1
            .
            CREATE child-ratecode.
            BUFFER-COPY tb3-buff EXCEPT CODE startperiode TO child-ratecode.
            ASSIGN 
                child-ratecode.CODE         = child-list.child-code
                child-ratecode.startperiode = beg-datum
            .
            RUN set-child-rate.
        END.
    END.
  END.

  FOR EACH child-ratecode:
      CREATE ratecode.
      BUFFER-COPY child-ratecode TO ratecode.
      DELETE child-ratecode.
  END.

  FOR EACH child-list WHERE child-list.true-child = YES:
      FIND FIRST queasy WHERE queasy.KEY = 2
          AND queasy.char1 = child-list.child-code NO-LOCK.
      ASSIGN 
          parent-code  = ENTRY(2, queasy.char3, ";")
          in-percent   = SUBSTR(ENTRY(3, queasy.char3, ";"),1,1) = "%"
          adjust-value = DECIMAL(SUBSTR(ENTRY(3, queasy.char3, ";"),2)) / 100
      .
      RUN link-ratecodebl.p (child-list.child-code, parent-code, queasy.char3,
          in-percent, adjust-value).
  END.
END.

PROCEDURE set-child-rate:
    DEF VAR rounded-rate AS DECIMAL NO-UNDO.
    IF in-percent THEN 
    DO:    
        child-ratecode.zipreis = tb3-buff.zipreis * (1 + adjust-value * 0.01).
        IF round-betrag NE 0 AND child-ratecode.zipreis GE (round-betrag * 10) THEN
        DO:
            RUN round-it (child-ratecode.zipreis, OUTPUT rounded-rate).
            child-ratecode.zipreis = rounded-rate.
        END.
    END.
    ELSE child-ratecode.zipreis = tb3-buff.zipreis + adjust-value.

END.

PROCEDURE set-child-rate-1:
DEF VAR rounded-rate AS DECIMAL NO-UNDO.
    IF in-percent THEN 
    DO:    
        ratecode.zipreis = tb3-buff.zipreis * (1 + adjust-value * 0.01).
        IF round-betrag NE 0 AND ratecode.zipreis GE (round-betrag * 10) THEN
        DO:
            RUN round-it (ratecode.zipreis, OUTPUT rounded-rate).
            ratecode.zipreis = rounded-rate.
        END.
    END.
    ELSE ratecode.zipreis = tb3-buff.zipreis + adjust-value.
END.

{round-it.i }

PROCEDURE update-bookengine-config:
    DEFINE BUFFER bqueasy FOR queasy.
    DEFINE BUFFER zbuff FOR zimkateg.
    DEFINE VARIABLE datum       AS DATE.
    DEFINE VARIABLE cm-gastno   AS INT NO-UNDO INIT 0.
    DEFINE VARIABLE roomnr      AS INT  INIT 0.
    DEFINE VARIABLE dyna        AS CHAR INIT "".
    DEFINE VARIABLE loopi       AS INTEGER.
    DEFINE VARIABLE currency    AS CHAR.
    DEFINE VARIABLE serv         AS DECIMAL.
    DEFINE VARIABLE vat          AS DECIMAL.
    DEFINE VARIABLE str          AS CHAR.

    DEFINE BUFFER tqueasy FOR queasy.
    
    FIND FIRST zbuff WHERE zbuff.zikatnr = p-list.zikatnr NO-LOCK NO-ERROR.
    IF cat-flag THEN
	DO:
		roomnr = zbuff.typ.
		FIND FIRST queasy WHERE queasy.KEY = 152 AND queasy.number1 = roomnr NO-LOCK NO-ERROR.
		IF AVAILABLE queasy THEN str = queasy.char1.
	END.
    ELSE 
		ASSIGN
			roomnr = zbuff.zikatnr
			str = zbuff.kurzbez.

    FOR EACH qsy WHERE qsy.KEY = 2 AND qsy.logi2 NO-LOCK:
        FOR EACH ratecode WHERE ratecode.CODE = qsy.char1 NO-LOCK:
            ifTask = ratecode.char1[5].
            DO tokcounter = 1 TO NUM-ENTRIES(ifTask, ";") - 1:
                mesToken = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 1, 2).
                mesValue = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 3).
                CASE mesToken:
                    WHEN "RC" THEN 
                    DO:
                        IF mesValue = prcode THEN
                        DO:
                            dyna = dyna + qsy.char1 + ";".
                        END.
                    END.
                END CASE.
            END.
        END.
    END.

    IF dyna NE "" THEN
    DO:
        DO tokcounter = 1 TO NUM-ENTRIES(dyna,";"):
            mesValue = TRIM(ENTRY(tokcounter,dyna, ";")).
            IF mesValue NE "" THEN
            DO:
                /* Malik Serverless 313  */
                IF p-list.startperiode NE ? AND p-list.endperiode NE ? THEN
                DO:
                    DO datum = p-list.startperiode TO p-list.endperiode:
                        /*naufal - add create queasy*/
                        FIND FIRST queasy WHERE queasy.KEY = 170 AND queasy.date1 = datum
                            AND queasy.number1 = roomnr AND queasy.char1 = mesValue
                            AND queasy.number2 = p-list.erwachs AND queasy.number3 = p-list.kind1 NO-LOCK NO-ERROR.
                        IF AVAILABLE queasy THEN
                        DO:
                            FIND FIRST qsy WHERE qsy.KEY = 170 AND qsy.date1 = datum
                                AND qsy.number1 = roomnr AND qsy.char1 = mesValue 
                                AND qsy.number2 = p-list.erwachs AND qsy.number3 = p-list.kind1 NO-LOCK NO-ERROR.
                            IF AVAILABLE qsy AND qsy.deci1 NE p-list.zipreis AND qsy.logi1 = NO AND qsy.logi2 = NO THEN
                            DO:
                                FIND FIRST bqueasy WHERE RECID(bqueasy) = RECID(qsy) EXCLUSIVE-LOCK NO-ERROR.
                                IF AVAILABLE bqueasy THEN
                                DO:
                                    ASSIGN bqueasy.logi2 = YES.
                                    FIND CURRENT bqueasy NO-LOCK.
                                    RELEASE bqueasy.
                                END.     
                            END.
                        END.
                        ELSE IF NOT AVAILABLE queasy THEN
                        DO:
                            FIND FIRST queasy WHERE queasy.KEY = 161 AND ENTRY(1, queasy.char1, ";") = mesValue AND ENTRY(3, queasy.char1, ";") = str NO-LOCK NO-ERROR.
                            DO WHILE AVAILABLE queasy:
                                CREATE queasy.
                                ASSIGN
                                    queasy.KEY      = 170
                                    queasy.date1    = datum
                                    queasy.char1    = mesValue
                                    queasy.number1  = roomnr
                                    queasy.number2  = p-list.erwachs
                                    queasy.number3  = p-list.kind1
                                    queasy.logi2    = YES
                                    queasy.char2    = p-list.CODE.

                                FIND FIRST arrangement WHERE arrangement.argtnr = p-list.argtnr NO-LOCK NO-ERROR.
                                IF AVAILABLE arrangement THEN
                                DO:                            
                                    FIND FIRST artikel WHERE artikel.artnr = arrangement.argt-artikelnr NO-LOCK NO-ERROR.
                                    IF AVAILABLE artikel THEN
                                        RUN calc-servvat.p (artikel.departement, artikel.artnr, datum,
                                                            artikel.service-code, artikel.mwst-code, 
                                                            OUTPUT serv, OUTPUT vat).
                                END.

                                IF tax-included THEN queasy.deci1 = p-list.zipreis.
                                ELSE queasy.deci1 = ROUND(DECIMAL(p-list.zipreis * (1 + serv + vat)),0).
                                
                                /*FIND FIRST bqueasy WHERE bqueasy.KEY = 160 AND bqueasy.number1 = queasy.number1
                                    NO-LOCK NO-ERROR.
                                IF AVAILABLE bqueasy THEN DO:
                                    DO loopi = 1 TO NUM-ENTRIES(bqueasy.char1,";"):
                                        str = ENTRY(loopi, bqueasy.char1, ";").
                                        IF SUBSTR(str,1,9)  = "$defcurr$"   THEN 
                                            ASSIGN currency = SUBSTR(str,10).
                                        IF currency NE " " THEN LEAVE.
                                    END.
                                    queasy.char3   = currency.
                                END.*/
                                FIND FIRST bqueasy WHERE bqueasy.KEY = 18 AND bqueasy.number1 = market-nr NO-LOCK NO-ERROR.
                                IF AVAILABLE bqueasy THEN
                                    FIND FIRST waehrung WHERE waehrung.wabkurz = bqueasy.char3 NO-LOCK NO-ERROR.
                                    IF AVAILABLE waehrung THEN
                                    DO:
                                        FIND FIRST q-curr WHERE q-curr.char1 = waehrung.wabkurz AND q-curr.KEY = 164
                                            /* AND q-curr.number1 = beCode */ AND q-curr.char2 NE "" NO-LOCK NO-ERROR.
                                        IF AVAILABLE q-curr THEN currency = q-curr.char2.
                                        ELSE currency = "IDR".
                                    END.
                                ELSE currency = "IDR".
                                queasy.char3 = currency.

                                FIND NEXT queasy WHERE queasy.KEY = 161 AND ENTRY(1, queasy.char1, ";") = mesValue AND ENTRY(3, queasy.char1, ";") = str NO-LOCK NO-ERROR.
                            END.                        
                        END.
                        /*end*/
                    END.
                END.
                /* END Malik */
            END.
        END.
    END.
    ELSE
    DO:
        /* Malik Serverless 313 */
        IF p-list.startperiode NE ? AND p-list.endperiode NE ? THEN
        DO:
            DO datum = p-list.startperiode TO p-list.endperiode:
                /*naufal - add create queasy*/
                FIND FIRST queasy WHERE queasy.KEY = 170 AND queasy.date1 = datum
                    AND queasy.number1 = roomnr AND queasy.char1 = prcode
                    AND queasy.number2 = p-list.erwachs AND queasy.number3 = p-list.kind1 NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                DO:
                    FIND FIRST qsy WHERE qsy.KEY = 170 AND qsy.date1 = datum
                        AND qsy.number1 = roomnr AND qsy.char1 = prcode 
                        AND qsy.number2 = p-list.erwachs AND qsy.number3 = p-list.kind1 NO-LOCK NO-ERROR.
                    IF AVAILABLE qsy AND qsy.deci1 NE p-list.zipreis AND qsy.logi1 = NO AND qsy.logi2 = NO THEN
                    DO:
                        FIND FIRST bqueasy WHERE RECID(bqueasy) = RECID(qsy) EXCLUSIVE-LOCK NO-ERROR.
                        IF AVAILABLE bqueasy THEN
                        DO:
                            ASSIGN bqueasy.logi2 = YES.
                            FIND CURRENT bqueasy NO-LOCK.
                            RELEASE bqueasy.
                        END.     
                    END.
                END.
                ELSE IF NOT AVAILABLE queasy THEN
                DO:

                    FIND FIRST queasy WHERE queasy.KEY = 161 AND ENTRY(1, queasy.char1, ";") = prcode 
                    AND ENTRY(3, queasy.char1, ";") = str  NO-LOCK NO-ERROR.
                    DO WHILE AVAILABLE queasy:
                        CREATE queasy.
                        ASSIGN
                            queasy.KEY      = 170
                            queasy.date1    = datum
                            queasy.char1    = prcode
                            queasy.number1  = roomnr
                            queasy.number2  = p-list.erwachs
                            queasy.number3  = p-list.kind1
                            queasy.logi2    = YES.

                        FIND FIRST arrangement WHERE arrangement.argtnr = p-list.argtnr NO-LOCK NO-ERROR.
                        IF AVAILABLE arrangement THEN
                        DO:                            
                            FIND FIRST artikel WHERE artikel.artnr = arrangement.argt-artikelnr NO-LOCK NO-ERROR.
                            IF AVAILABLE artikel THEN
                                RUN calc-servvat.p (artikel.departement, artikel.artnr, datum,
                                                    artikel.service-code, artikel.mwst-code, 
                                                    OUTPUT serv, OUTPUT vat).
                        END.

                        IF tax-included THEN queasy.deci1 = p-list.zipreis.
                        ELSE queasy.deci1 = ROUND(DECIMAL(p-list.zipreis * (1 + serv + vat)),0).
                        
                        /*FIND FIRST bqueasy WHERE bqueasy.KEY = 160 AND bqueasy.number1 = queasy.number1
                            NO-LOCK NO-ERROR.
                        IF AVAILABLE bqueasy THEN DO:
                            DO loopi = 1 TO NUM-ENTRIES(bqueasy.char1,";"):
                                str = ENTRY(loopi, bqueasy.char1, ";").
                                IF SUBSTR(str,1,9)  = "$defcurr$"   THEN 
                                    ASSIGN currency = SUBSTR(str,10).
                                IF currency NE " " THEN LEAVE.
                            END.
                            queasy.char3   = currency.
                        END.*/
                        FIND FIRST bqueasy WHERE bqueasy.KEY = 18 AND bqueasy.number1 = market-nr NO-LOCK NO-ERROR.
                        IF AVAILABLE bqueasy THEN
                            FIND FIRST waehrung WHERE waehrung.wabkurz = bqueasy.char3 NO-LOCK NO-ERROR.
                            IF AVAILABLE waehrung THEN
                            DO:
                                FIND FIRST q-curr WHERE q-curr.char1 = waehrung.wabkurz AND q-curr.KEY = 164
                                    /* AND q-curr.number1 = beCode */ AND q-curr.char2 NE "" NO-LOCK NO-ERROR.
                                IF AVAILABLE q-curr THEN currency = q-curr.char2.
                                ELSE currency = "IDR".
                            END.
                        ELSE currency = "IDR".
                        queasy.char3 = currency.

                        FIND NEXT queasy WHERE queasy.KEY = 161 AND ENTRY(1, queasy.char1, ";") = mesValue 
                        AND ENTRY(3, queasy.char1, ";") = str   NO-LOCK NO-ERROR.
                    END.                                        
                END.
                /*end*/
            END. 
        END.
        /* END Malik */
    END.
END.

