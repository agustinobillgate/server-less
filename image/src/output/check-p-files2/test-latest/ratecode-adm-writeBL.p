DEFINE TEMP-TABLE tb3       LIKE ratecode  
    FIELD s-recid           AS INTEGER INIT 0. /*M real ratecode */  

DEFINE TEMP-TABLE tb3Buff   LIKE tb3.   

DEFINE TEMP-TABLE p-list    LIKE tb3
    FIELD rmcat-str         AS CHAR FORMAT "x(18)"
    FIELD wday-str          AS CHAR FORMAT "x(10)"
    FIELD adult-str         AS CHAR FORMAT "x(10)"
    FIELD child-str         AS CHAR FORMAT "x(10)"
.   

DEFINE TEMP-TABLE t-ratecode   LIKE ratecode
    FIELD s-recid               AS INTEGER.

DEFINE TEMP-TABLE q-list
    FIELD rcode         AS CHAR
    FIELD dcode         AS CHAR.

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
    FIELD in-percent AS LOGICAL
    FIELD adjust-value AS DECIMAL
.
DEFINE TEMP-TABLE child-ratecode LIKE ratecode.

DEF TEMP-TABLE product-list
    FIELD market    AS INTEGER
    FIELD i-product AS INTEGER EXTENT 99
    FIELD prcode    AS CHAR
.

DEFINE INPUT PARAMETER mode-str     AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER markNo       AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER prcode       AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER argtNo       AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER user-init    AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER book-room    AS INTEGER  NO-UNDO. 
DEFINE INPUT PARAMETER comp-room    AS INTEGER  NO-UNDO. 
DEFINE INPUT PARAMETER max-room     AS INTEGER  NO-UNDO. 
DEFINE INPUT PARAMETER TABLE FOR p-list.
DEFINE INPUT PARAMETER TABLE FOR early-discount.
DEFINE INPUT PARAMETER TABLE FOR kickback-discount.
DEFINE INPUT PARAMETER TABLE FOR stay-pay.
DEFINE OUTPUT PARAMETER error-flag AS LOGICAL NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER TABLE FOR tb3Buff.

DEF VARIABLE zikatno    AS INTEGER NO-UNDO.
DEF VARIABLE wday       AS INTEGER NO-UNDO.
DEF VARIABLE adult      AS INTEGER NO-UNDO.
DEF VARIABLE child1     AS INTEGER NO-UNDO.
DEF VARIABLE curr-1     AS INTEGER NO-UNDO.
DEF VARIABLE curr-2     AS INTEGER NO-UNDO.
DEF VARIABLE curr-3     AS INTEGER NO-UNDO.
DEF VARIABLE curr-4     AS INTEGER NO-UNDO.
DEF VARIABLE mesVal     AS CHAR    NO-UNDO.

DEF VARIABLE ci-date        AS DATE     NO-UNDO.
DEF VARIABLE round-betrag   AS INTEGER  NO-UNDO.
DEF VARIABLE round-method   AS INTEGER  NO-UNDO INIT 0.
DEF VARIABLE length-round   AS INTEGER  NO-UNDO.
DEF VARIABLE adjust-value   AS DECIMAL  NO-UNDO.
DEF VARIABLE in-percent     AS LOGICAL  NO-UNDO.

DEFINE VARIABLE tax-included AS LOGICAL INITIAL NO NO-UNDO.

DEFINE BUFFER rbuff  FOR ratecode.
DEFINE BUFFER q-curr FOR queasy.

/*****************************************************************************/
FIND FIRST p-list.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
ASSIGN ci-date = htparam.fdate.

IF mode-str = "insert" THEN RUN check-overlapping.
IF error-flag THEN RETURN.
RUN create-records.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN 
DO:
    CREATE res-history.
    ASSIGN 
        res-history.nr          = bediener.nr
        res-history.datum       = TODAY
        res-history.zeit        = TIME
        res-history.action      = "RateCode".
    FIND FIRST zimkateg WHERE zimkateg.zikatnr EQ p-list.zikatnr NO-LOCK NO-ERROR.
    IF AVAILABLE zimkateg THEN
        ASSIGN res-history.aenderung   = "Create Contract Rate, Code: " + prcode + " RmType : " + zimkateg.kurzbez + 
                                          " start:" + STRING(p-list.startperiode) + "|end:" + STRING(p-list.endperiode) + 
                                          "|adult:" + STRING(adult) + "|rate:" + STRING(p-list.zipreis) 
                                          .
    ELSE ASSIGN res-history.aenderung   = "Create Contract Rate, Code: " + prcode + 
                                          " start:" + STRING(p-list.startperiode) + "|end:" + STRING(p-list.endperiode) + 
                                          "|adult:" + STRING(adult) + "|rate:" + STRING(p-list.zipreis) 
                                          .
    FIND CURRENT res-history NO-LOCK.
    RELEASE res-history.
END.

IF mode-str = "update" THEN 
DO:   
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
    /*Naufal*/
    RUN create-child-list.
    
    RUN update-child-rate-dates.
END.

DEFINE VARIABLE curr-time AS CHAR NO-UNDO.
/*/*Naufal - add check overlapping for chg rate #431314*/
IF mode-str = "chg-rate" THEN RUN check-overlapping.
IF error-flag THEN RETURN.
/*end*/*/
RUN update-ratecode-dates.
/*FT*/
RUN create-child-list.
ASSIGN curr-time = STRING(TIME, "HH:MM:SS").
RUN delete-old-childrate.
RUN create-childrate.


FOR EACH guest-pr WHERE guest-pr.CODE = prcode NO-LOCK: 
  FIND FIRST guest WHERE guest.gastnr = guest-pr.gastnr NO-LOCK. 
  IF guest.endperiode = ? OR guest.endperiode LT p-list.endperiode THEN
  DO:
    FIND CURRENT guest SHARE-LOCK.
    ASSIGN guest.endperiode = p-list.endperiode.
    FIND CURRENT guest NO-LOCK.
  END.
END. 
RUN update-bookengine-config.

PROCEDURE delete-old-childrate:
    DEFINE VARIABLE curr-i AS INT.

    FIND FIRST p-list NO-LOCK NO-ERROR.
    
    FIND FIRST child-list NO-LOCK NO-ERROR.
    /*naufal 110320 - add validation wday and erwachs*/
    DO WHILE AVAILABLE child-list:
        FIND FIRST ratecode WHERE ratecode.CODE = child-list.child-code
            AND ratecode.startperiode = p-list.startperiode
            AND ratecode.endperiode = p-list.endperiode
            AND ratecode.wday = p-list.wday
            AND ratecode.erwachs = p-list.erwachs 
            AND ratecode.argtnr = p-list.argtnr
            AND ratecode.zikatnr = p-list.zikatnr NO-LOCK NO-ERROR.
        IF AVAILABLE ratecode THEN DO:
            FIND CURRENT ratecode EXCLUSIVE-LOCK.
            DELETE ratecode.
            RELEASE ratecode.
        END.
        FIND NEXT child-list NO-LOCK NO-ERROR.
    END.

    FIND FIRST child-list NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE child-list:
        FIND FIRST prtable WHERE prtable.prcode = child-list.child-code NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE prtable :
            CREATE product-list.
            ASSIGN product-list.market = prtable.marknr
                   product-list.prcode = prtable.prcode.

            DO curr-i = 1 TO 99:
                IF prtable.product[curr-i] = 0 THEN LEAVE.
                /* SY 28/07/2014 */    
                IF prtable.product[curr-i] GE 90001 THEN
                    FIND FIRST rbuff WHERE rbuff.CODE = prtable.prcode
                        AND rbuff.marknr = prtable.marknr
                        AND ((90 + rbuff.zikatnr) * 1000 + rbuff.argtnr) = prtable.product[curr-i]
                        NO-LOCK NO-ERROR.    
                ELSE IF prtable.product[curr-i] GE 10001 THEN
                    FIND FIRST rbuff WHERE rbuff.CODE = prtable.prcode
                        AND rbuff.marknr = prtable.marknr
                        AND (rbuff.zikatnr * 1000 + rbuff.argtnr) = prtable.product[curr-i]
                        NO-LOCK NO-ERROR.    
                ELSE
                    FIND FIRST rbuff WHERE rbuff.CODE = prtable.prcode
                        AND rbuff.marknr = prtable.marknr
                        AND (rbuff.zikatnr * 100 + rbuff.argtnr) = prtable.product[curr-i]
                        NO-LOCK NO-ERROR.
                IF AVAILABLE rbuff THEN
                DO:
                    ASSIGN product-list.i-product[curr-i] = prtable.product[curr-i].
                END.
            END.
            FIND CURRENT prtable EXCLUSIVE-LOCK.
            DELETE prtable.
            RELEASE prtable.
            FIND NEXT prtable WHERE prtable.prcode = child-list.child-code NO-LOCK NO-ERROR.
        END.
        FIND NEXT child-list NO-LOCK NO-ERROR.
    END.
END.

PROCEDURE create-childrate:
    DEF BUFFER prbuff FOR prtable.

    DEFINE VAR curr-i AS INTEGER.
    DEFINE VAR rounded-rate AS DECIMAL NO-UNDO.

    FIND FIRST p-list NO-LOCK NO-ERROR.

    FOR EACH child-list NO-LOCK :
        FOR EACH ratecode WHERE ratecode.CODE EQ prcode
            AND ratecode.startperiode EQ p-list.startperiode
            AND ratecode.endperiode EQ p-list.endperiode NO-LOCK:

            /*Naufal - add validation for fix rbuff already exists*/
            /*Naufal 100320 - add validation to argtnr and zikatnr for fix rate not inserted*/
            FIND FIRST rbuff WHERE rbuff.CODE EQ child-list.child-code 
                AND rbuff.startperiode EQ ratecode.startperiode
                AND rbuff.endperiode EQ ratecode.endperiode
                AND rbuff.wday EQ ratecode.wday
                AND rbuff.erwachs EQ ratecode.erwachs
                AND rbuff.argtnr EQ ratecode.argtnr
                AND rbuff.zikatnr EQ ratecode.zikatnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE rbuff THEN
            DO:
                CREATE rbuff.
                /*naufal - add except ratecode.argtnr ratecode.zikatnr*/
                /*mnaufal - remove except ratecode.zikatnr*/
                BUFFER-COPY ratecode EXCEPT ratecode.CODE ratecode.argtnr TO rbuff.
                ASSIGN
                    rbuff.CODE    = child-list.child-code
                    rbuff.argtnr  = argtno.       
                
                IF child-list.in-percent THEN 
                DO: 
                    /*DISP child-list.child-code rbuff.zipreis child-list.adjust-value round-betrag.*/
                    rbuff.zipreis = rbuff.zipreis * (1 + child-list.adjust-value * 0.01).
                    IF round-betrag NE 0 AND rbuff.zipreis GE (round-betrag * 10) THEN
                    DO:
                        RUN round-it (rbuff.zipreis, OUTPUT rounded-rate).
                        rbuff.zipreis = rounded-rate.
                    END.
                END.
                ELSE rbuff.zipreis = rbuff.zipreis + child-list.adjust-value.
            END.
            /*end*/
        END.
    END.

    FIND FIRST child-list NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE child-list:
        FIND FIRST prtable WHERE prtable.prcode = prcode NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE prtable:
            CREATE prbuff.
            BUFFER-COPY prtable EXCEPT prcode TO prbuff.
            ASSIGN prbuff.prcode = child-list.child-code.

            FIND FIRST product-list WHERE product-list.market = prbuff.marknr
                AND product-list.prcode = prbuff.prcode NO-LOCK NO-ERROR.
            IF AVAILABLE product-list THEN DO:
                DO curr-i = 1 TO 99:
                    IF prbuff.product[curr-i] = 0 THEN
                    DO:
                        ASSIGN prbuff.product[curr-i] = product-list.i-product[curr-i].                        
                    END.
                END.
                DELETE product-list.
            END.
            FIND NEXT prtable WHERE prtable.prcode = prcode NO-LOCK NO-ERROR.
        END.
        FIND NEXT child-list NO-LOCK NO-ERROR.
    END.
END.

PROCEDURE check-overlapping:
    DO curr-1 = 1 TO NUM-ENTRIES(p-list.rmcat-str, ","):
        mesVal = TRIM(ENTRY(curr-1,p-list.rmcat-str, ",")).
        IF mesVal NE "" THEN
        DO:
          FIND FIRST zimkateg WHERE zimkateg.kurzbez = mesVal NO-LOCK NO-ERROR.
          zikatno = zimkateg.zikatnr.
          DO curr-2 = 1 TO NUM-ENTRIES(p-list.wday-str, ","):
            mesVal = TRIM(ENTRY(curr-2,p-list.wday-str, ",")).
            IF mesVal NE "" THEN
            DO:
              wday = INTEGER(mesVal).
              DO curr-3 = 1 TO NUM-ENTRIES(p-list.adult-str, ","):
                mesVal = TRIM(ENTRY(curr-3,p-list.adult-str, ",")).
                IF mesVal NE "" THEN
                DO:
                  adult = INTEGER(mesVal).
                  DO curr-4 = 1 TO NUM-ENTRIES(p-list.child-str, ","):
                    mesVal = TRIM(ENTRY(curr-4,p-list.child-str, ",")).
                    IF mesVal NE "" THEN
                    DO:
                      child1 = INTEGER(mesVal).
                      FIND FIRST ratecode WHERE ratecode.marknr = markNo 
                          AND ratecode.code    = prcode 
                          AND ratecode.argtnr  = argtNo 
                          AND ratecode.zikatnr = zikatNo
                          AND ratecode.erwachs = adult
                          AND ratecode.kind1   = child1 
                          AND ratecode.kind2   = p-list.kind2 
                          AND ratecode.wday    = wday
                          AND NOT ratecode.startperiod GE p-list.endperiode
                          /*NAUFAL 080321 - adjust validation from LE to LT*/
                          AND NOT ratecode.endperiod LT p-list.startperiode NO-LOCK NO-ERROR. 
                      IF AVAILABLE ratecode THEN
                      DO:
                        error-flag = YES.
                        RETURN.
                      END.
                    END.
                  END.
                END.
              END.
            END. 
          END.
        END.
    END.
END.

PROCEDURE create-child-list:
    FOR EACH queasy WHERE queasy.KEY = 2
        AND NOT queasy.logi2
        AND NUM-ENTRIES(queasy.char3, ";") GT 2
        AND ENTRY(2, queasy.char3, ";") = prcode NO-LOCK:
        CREATE child-list.
        ASSIGN 
            child-list.child-code   = queasy.char1
            child-list.in-percent   = SUBSTR(ENTRY(3, queasy.char3, ";"),1,1) = "%"
            child-list.adjust-value = DECIMAL(SUBSTR(ENTRY(3, queasy.char3, ";"),2)) / 100
        .
    END.
END.

PROCEDURE create-records:
    DO curr-1 = 1 TO NUM-ENTRIES(p-list.rmcat-str, ","):
        mesVal = TRIM(ENTRY(curr-1, p-list.rmcat-str, ",")).
        IF mesVal NE "" THEN
        DO:
          FIND FIRST zimkateg WHERE zimkateg.kurzbez = mesVal NO-LOCK NO-ERROR.
          zikatno = zimkateg.zikatnr.
          DO curr-2 = 1 TO NUM-ENTRIES(p-list.wday-str, ","):
            mesVal = TRIM(ENTRY(curr-2, p-list.wday-str, ",")).
            IF mesVal NE "" THEN
            DO:
              wday = INTEGER(mesVal).
              DO curr-3 = 1 TO NUM-ENTRIES(p-list.adult-str, ","):
                mesVal = TRIM(ENTRY(curr-3, p-list.adult-str, ",")).
                IF mesVal NE "" THEN
                DO:
                  adult = INTEGER(mesVal).
                  DO curr-4 = 1 TO NUM-ENTRIES(p-list.child-str, ","):
                    mesVal = TRIM(ENTRY(curr-4, p-list.child-str, ",")).
                    IF mesVal NE "" THEN
                    DO:
                      child1 = INTEGER(mesVal).
                      RUN create-ratecode.
                    END.
                  END.
                END.
              END.
            END.
          END.
        END.
    END.
END.

PROCEDURE create-ratecode:
  /*ITA -> why use this condition 101218VdHdP?? 
  IF mode-str = "update" THEN DO:
      FIND FIRST ratecode WHERE ratecode.marknr = markNo 
          AND ratecode.code    = prcode 
          AND ratecode.argtnr  = argtNo 
          AND ratecode.zikatnr = zikatNo
          AND ratecode.erwachs = adult
          AND ratecode.kind1   = child1 
          AND ratecode.kind2   = p-list.kind2 
          AND ratecode.wday    = wday
          AND NOT ratecode.startperiod GE p-list.endperiode
          AND NOT ratecode.endperiod LE p-list.startperiode NO-LOCK NO-ERROR. 
      IF AVAILABLE ratecode THEN DO:
         FIND FIRST tb3Buff WHERE tb3Buff.s-recid = INTEGER(RECID(ratecode)) NO-LOCK NO-ERROR.
         IF AVAILABLE tb3Buff THEN DO:
             FIND CURRENT tb3Buff EXCLUSIVE-LOCK.
             DELETE tb3Buff.
             RELEASE tb3Buff.
         END.
         FIND CURRENT ratecode EXCLUSIVE-LOCK.
         DELETE ratecode.
         RELEASE ratecode.
      END.
  END.
*/
  CREATE ratecode.  
  BUFFER-COPY p-list EXCEPT p-list.argtnr p-list.zikatnr TO ratecode. 
  ASSIGN 
    ratecode.marknr      = markNo 
    ratecode.code        = prcode 
    ratecode.argtnr      = argtno 
    ratecode.zikatnr     = zikatno
    ratecode.wday        = wday
    ratecode.erwachs     = adult
    ratecode.kind1       = child1
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

  CREATE tb3Buff.
  BUFFER-COPY ratecode TO tb3Buff.
  ASSIGN tb3Buff.s-recid = INTEGER(RECID(ratecode)).
END.

PROCEDURE update-child-rate-dates:
DEF VARIABLE beg-datum    AS DATE    NO-UNDO.
DEF VARIABLE end-datum    AS DATE    NO-UNDO.
DEF VARIABLE parent-code  AS CHAR    NO-UNDO.

DEF BUFFER rbuff FOR ratecode.

    FOR EACH tb3Buff: /* new created parent rates */
        /**/
      FOR EACH child-list :
        FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = child-list.child-code NO-LOCK.
        ASSIGN 
            parent-code  = ENTRY(2, queasy.char3, ";")
            in-percent   = SUBSTR(ENTRY(3, queasy.char3, ";"),1,1) = "%"
            adjust-value = DECIMAL(SUBSTR(ENTRY(3, queasy.char3, ";"),2)) / 100
        .
        FOR EACH ratecode WHERE ratecode.marknr = markNo 
            AND ratecode.code    = child-list.child-code 
            AND ratecode.argtnr  = argtNo 
            AND ratecode.zikatnr = tb3Buff.zikatnr
            AND ratecode.erwachs = tb3Buff.erwachs
            AND ratecode.kind1   = tb3Buff.kind1 
            AND ratecode.kind2   = tb3Buff.kind2 
            AND ratecode.wday    = tb3Buff.wday
            AND NOT ratecode.endperiode LT tb3Buff.startperiode
            AND NOT ratecode.startperiode GT tb3Buff.endperiode: 
            
            IF ratecode.startperiode LT tb3Buff.startperiode THEN
            DO:
                IF ratecode.endperiode LE tb3Buff.endperiode THEN
                DO:
                  ASSIGN 
                      end-datum           = ratecode.endperiode
                      ratecode.endperiode = tb3Buff.startperiode - 1.
                  CREATE child-ratecode.
                  BUFFER-COPY tb3Buff EXCEPT CODE endperiode TO child-ratecode.
                  ASSIGN 
                      child-ratecode.CODE       = child-list.child-code
                      child-ratecode.endperiode = end-datum
                  .
                  RUN set-child-rate.
                END.
                ELSE 
                DO:
                  CREATE child-ratecode.
                  BUFFER-COPY tb3Buff EXCEPT CODE TO child-ratecode.
                  ASSIGN child-ratecode.CODE = child-list.child-code.
                  RUN set-child-rate.

                  CREATE child-ratecode.
                  BUFFER-COPY ratecode EXCEPT startperiode TO child-ratecode.
                  ASSIGN 
                      ratecode.endperiode         = tb3Buff.startperiode - 1
                      child-ratecode.startperiode = tb3Buff.endperiode + 1
                  .
                END.
            END.
            ELSE IF (ratecode.startperiode GE tb3Buff.startperiode)
              AND (ratecode.endperiode LE tb3Buff.endperiode) THEN
              RUN set-child-rate-1.
            ELSE IF (ratecode.startperiode GE tb3Buff.startperiode)
              AND (ratecode.endperiode GT tb3Buff.endperiode) THEN
            DO:
                ASSIGN
                    beg-datum             = ratecode.startperiode
                    ratecode.startperiode = tb3Buff.endperiode + 1
                .
                CREATE child-ratecode.
                BUFFER-COPY tb3Buff EXCEPT CODE startperiode TO child-ratecode.
                ASSIGN 
                    child-ratecode.CODE         = child-list.child-code
                    child-ratecode.startperiode = beg-datum
                .
                RUN set-child-rate.
            END.
        END.
      END.
    END.
    FOR EACH child-ratecode:
        CREATE ratecode.
        BUFFER-COPY child-ratecode TO ratecode.
        DELETE child-ratecode.
    END.
END.

PROCEDURE update-ratecode-dates:
DEF VARIABLE beg-datum    AS DATE    NO-UNDO.
DEF VARIABLE end-datum    AS DATE    NO-UNDO.
DEF VARIABLE parent-code  AS CHAR    NO-UNDO.
DEF BUFFER rbuff FOR ratecode.

    FOR EACH tb3Buff:
        
        FOR EACH ratecode WHERE ratecode.marknr = markNo 
            AND ratecode.code    = prcode 
            AND ratecode.argtnr  = argtNo 
            AND ratecode.zikatnr = tb3Buff.zikatnr
            AND ratecode.erwachs = tb3Buff.erwachs
            AND ratecode.kind1   = tb3Buff.kind1 
            AND ratecode.kind2   = tb3Buff.kind2 
            AND ratecode.wday    = tb3Buff.wday
            AND NOT ratecode.endperiode LT tb3Buff.startperiode
            AND NOT ratecode.startperiode GT tb3Buff.endperiode 
            AND INTEGER(RECID(ratecode)) NE tb3Buff.s-recid:

            IF ratecode.startperiode LT tb3Buff.startperiode THEN
            DO:
                IF ratecode.endperiode LE tb3Buff.endperiode THEN
                  ASSIGN ratecode.endperiode = tb3Buff.startperiode - 1.
                ELSE 
                DO:
                  CREATE rbuff.
                  BUFFER-COPY ratecode EXCEPT startperiode TO rbuff.
                  ASSIGN 
                      ratecode.endperiode = tb3Buff.startperiode - 1
                      rbuff.startperiode = tb3Buff.endperiode + 1
                  .
                  FIND CURRENT rbuff NO-LOCK.
                END.
            END.
            ELSE
            DO:
                IF ratecode.endperiode LE tb3Buff.endperiode THEN
                    DELETE ratecode.
                ELSE
                ASSIGN ratecode.startperiode = tb3Buff.endperiode + 1.
            END.
        END.
    END.
END.

PROCEDURE set-child-rate:
DEF VAR rounded-rate AS DECIMAL NO-UNDO.
    IF in-percent THEN 
    DO:    
        child-ratecode.zipreis = child-ratecode.zipreis * (1 + adjust-value * 0.01).
        IF round-betrag NE 0 AND child-ratecode.zipreis GE (round-betrag * 10) THEN
        DO:
            RUN round-it (child-ratecode.zipreis, OUTPUT rounded-rate).
            child-ratecode.zipreis = rounded-rate.
        END.
    END.
    ELSE child-ratecode.zipreis = child-ratecode.zipreis + adjust-value.
END.

PROCEDURE set-child-rate-1:
DEF VAR rounded-rate AS DECIMAL NO-UNDO.
    IF in-percent THEN 
    DO:    
        ratecode.zipreis = ratecode.zipreis * (1 + adjust-value * 0.01).
        IF round-betrag NE 0 AND ratecode.zipreis GE (round-betrag * 10) THEN
        DO:
            RUN round-it (ratecode.zipreis, OUTPUT rounded-rate).
            ratecode.zipreis = rounded-rate.
        END.
    END.
    ELSE ratecode.zipreis = ratecode.zipreis + adjust-value.
END.

{round-it.i }

PROCEDURE update-bookengine-config:
    DEFINE VARIABLE cm-gastno AS INT NO-UNDO INIT 0.
    DEFINE BUFFER qsy FOR queasy.
    DEFINE BUFFER bqueasy FOR queasy.
    DEFINE BUFFER zbuff FOR zimkateg.

    DEFINE VARIABLE ifTask      AS CHAR INIT "".
    DEFINE VARIABLE mesToken    AS CHAR INIT "".
    DEFINE VARIABLE mesValue    AS CHAR INIT "".
    DEFINE VARIABLE tokcounter  AS INT  INIT 0.
    DEFINE VARIABLE datum       AS DATE.
    DEFINE VARIABLE cat-flag    AS LOGICAL INIT NO.
    DEFINE VARIABLE roomnr      AS INT  INIT 0.
    DEFINE VARIABLE dyna        AS CHARACTER INIT "".
    DEFINE VARIABLE loopi       AS INTEGER NO-UNDO.
    DEFINE VARIABLE loopj       AS INTEGER NO-UNDO.

    DEFINE VARIABLE loopk       AS INTEGER.
    DEFINE VARIABLE currency    AS CHAR.
    DEFINE VARIABLE serv         AS DECIMAL.
    DEFINE VARIABLE vat          AS DECIMAL.
    DEFINE VARIABLE str          AS CHAR.

    DEFINE BUFFER tqueasy FOR queasy.

    FIND FIRST qsy WHERE qsy.KEY = 152 NO-LOCK NO-ERROR.
    IF AVAILABLE qsy THEN cat-flag = YES.

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

    DO curr-1 = 1 TO NUM-ENTRIES(p-list.rmcat-str, ","):
        mesVal = TRIM(ENTRY(curr-1,p-list.rmcat-str, ",")).
        IF mesVal NE "" THEN
        DO:
            FIND FIRST zbuff WHERE zbuff.kurzbez = mesVal NO-LOCK NO-ERROR.
            IF AVAILABLE zbuff THEN
            DO:
                roomnr = 0.
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

                IF dyna NE "" THEN
                DO:
                    DO tokcounter = 1 TO NUM-ENTRIES(dyna,";"):
                        mesValue = TRIM(ENTRY(tokcounter,dyna, ";")).
                        IF mesValue NE "" THEN
                        DO:
                            DO datum = p-list.startperiode TO p-list.endperiode:
                                /*Naufal - Add create queasy*/
                                FIND FIRST queasy WHERE queasy.KEY = 170 AND queasy.date1 = datum
                                    AND queasy.number1 = roomnr AND queasy.char1 = mesValue NO-LOCK NO-ERROR.
                                IF AVAILABLE queasy THEN
                                DO:
                                    FIND FIRST qsy WHERE qsy.KEY = 170 AND qsy.date1 = datum
                                        AND qsy.number1 = roomnr AND qsy.char1 = mesValue NO-LOCK NO-ERROR.
                                    DO WHILE AVAILABLE qsy:
                                        FIND FIRST bqueasy WHERE RECID(bqueasy) = RECID(qsy) EXCLUSIVE-LOCK NO-ERROR.
                                        IF AVAILABLE bqueasy THEN
                                        DO:
                                            ASSIGN bqueasy.logi2 = YES.
                                            FIND CURRENT bqueasy NO-LOCK.
                                            RELEASE bqueasy.
                                        END.   
                                        FIND NEXT qsy WHERE qsy.KEY = 170 AND qsy.date1 = datum
                                            AND qsy.number1 = roomnr AND qsy.char1 = mesValue NO-LOCK NO-ERROR.
                                    END.
                                END.
                                ELSE IF NOT AVAILABLE queasy THEN
                                DO:
                                    DO loopi = 1 TO NUM-ENTRIES(p-list.adult-str, ","):
                                        IF p-list.child-str NE "" THEN DO:
                                            DO loopj = 1 TO NUM-ENTRIES(p-list.child-str, ","):

                                                FIND FIRST queasy WHERE queasy.KEY = 161 AND ENTRY(1, queasy.char1, ";") = mesValue AND ENTRY(3, queasy.char1, ";") = str
                                                    NO-LOCK NO-ERROR.
                                                DO WHILE AVAILABLE queasy:
                                                    CREATE queasy.
                                                    ASSIGN
                                                        queasy.KEY      = 170
                                                        queasy.date1    = datum
                                                        queasy.char1    = mesValue
                                                        queasy.number1  = roomnr 
                                                        queasy.number2  = INT(ENTRY(loopi,p-list.adult-str, "," ))
                                                        queasy.number3  = INT(ENTRY(loopj,p-list.child-str, "," ))
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
                                                        DO loopk = 1 TO NUM-ENTRIES(bqueasy.char1,";"):
                                                            str = ENTRY(loopk, bqueasy.char1, ";").
                                                            IF SUBSTR(str,1,9)  = "$defcurr$"   THEN 
                                                                ASSIGN currency = SUBSTR(str,10).
                                                            IF currency NE " " THEN LEAVE.
                                                        END.
                                                        queasy.char3   = currency.
                                                    END.*/
                                                    FIND FIRST bqueasy WHERE bqueasy.KEY = 18 AND bqueasy.number1 = markno NO-LOCK NO-ERROR.
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
                                
                                                    FIND NEXT queasy WHERE queasy.KEY = 161 AND ENTRY(1, queasy.char1, ";") = mesValue AND ENTRY(3, queasy.char1, ";") = str
                                                        NO-LOCK NO-ERROR.
                                                END.                                                                               
                                            END.
                                        END.
                                        ELSE DO:

                                            FIND FIRST queasy WHERE queasy.KEY = 161 AND ENTRY(1, queasy.char1, ";") = mesValue AND ENTRY(3, queasy.char1, ";") = str
                                                NO-LOCK NO-ERROR.
                                            DO WHILE AVAILABLE queasy:

                                                CREATE queasy.
                                                ASSIGN
                                                    queasy.KEY      = 170
                                                    queasy.date1    = datum
                                                    queasy.char1    = mesValue
                                                    queasy.number1  = roomnr
                                                    queasy.number2  = INT(ENTRY(loopi,p-list.adult-str, "," ))
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
                                                    DO loopk = 1 TO NUM-ENTRIES(bqueasy.char1,";"):
                                                        str = ENTRY(loopk, bqueasy.char1, ";").
                                                        IF SUBSTR(str,1,9)  = "$defcurr$"   THEN 
                                                            ASSIGN currency = SUBSTR(str,10).
                                                        IF currency NE " " THEN LEAVE.
                                                    END.
                                                    queasy.char3   = currency.
                                                END.*/
                                                FIND FIRST bqueasy WHERE bqueasy.KEY = 18 AND bqueasy.number1 = markno NO-LOCK NO-ERROR.
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
                            
                                                FIND NEXT queasy WHERE queasy.KEY = 161 AND ENTRY(1, queasy.char1, ";") = mesValue AND ENTRY(3, queasy.char1, ";") = str
                                                    NO-LOCK NO-ERROR.
                                            END.                                                                               
                                        END.
                                    END.
                                    
                                END.
                                /*end*/
                            END.
                        END.
                    END.
                END.
                ELSE
                DO:
                    DO datum = p-list.startperiode TO p-list.endperiode:
                        /*Naufal - Add create queasy*/
                        FIND FIRST queasy WHERE queasy.KEY = 170 AND queasy.date1 = datum
                            AND queasy.number1 = roomnr AND queasy.char1 = prcode NO-LOCK NO-ERROR.
                        IF AVAILABLE queasy THEN
                        DO:
                            FIND FIRST qsy WHERE qsy.KEY = 170 AND qsy.date1 = datum
                                AND qsy.number1 = roomnr AND qsy.char1 = prcode NO-LOCK NO-ERROR.
                            DO WHILE AVAILABLE qsy:
                                FIND FIRST bqueasy WHERE RECID(bqueasy) = RECID(qsy) EXCLUSIVE-LOCK NO-ERROR.
                                IF AVAILABLE bqueasy THEN
                                DO:
                                    ASSIGN bqueasy.logi2 = YES.
                                    FIND CURRENT bqueasy NO-LOCK.
                                    RELEASE bqueasy.
                                END.   
                                FIND NEXT qsy WHERE qsy.KEY = 170 AND qsy.date1 = datum
                                    AND qsy.number1 = roomnr AND qsy.char1 = prcode NO-LOCK NO-ERROR.
                            END.
                        END.
                        ELSE IF NOT AVAILABLE queasy THEN
                        DO:
                            DO loopi = 1 TO NUM-ENTRIES(p-list.adult-str, ","):
                                IF p-list.child-str NE "" THEN DO:
                                    DO loopj = 1 TO NUM-ENTRIES(p-list.child-str, ","):

                                        FIND FIRST queasy WHERE queasy.KEY = 161 AND ENTRY(1, queasy.char1, ";") = prcode AND ENTRY(3, queasy.char1, ";") = str
                                            NO-LOCK NO-ERROR.
                                        DO WHILE AVAILABLE queasy:

                                            CREATE queasy.
                                            ASSIGN
                                                queasy.KEY      = 170
                                                queasy.date1    = datum
                                                queasy.char1    = prcode
                                                queasy.number1  = roomnr 
                                                queasy.number2  = INT(ENTRY(loopi,p-list.adult-str, "," ))
                                                queasy.number3  = INT(ENTRY(loopj,p-list.child-str, "," ))
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
                                                DO loopk = 1 TO NUM-ENTRIES(bqueasy.char1,";"):
                                                    str = ENTRY(loopk, bqueasy.char1, ";").
                                                    IF SUBSTR(str,1,9)  = "$defcurr$"   THEN 
                                                        ASSIGN currency = SUBSTR(str,10).
                                                    IF currency NE " " THEN LEAVE.
                                                END.
                                                queasy.char3   = currency.
                                            END.*/
                                            FIND FIRST bqueasy WHERE bqueasy.KEY = 18 AND bqueasy.number1 = markno NO-LOCK NO-ERROR.
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
                        
                                            FIND NEXT queasy WHERE queasy.KEY = 161 AND ENTRY(1, queasy.char1, ";") = mesValue AND ENTRY(3, queasy.char1, ";") = str
                                                NO-LOCK NO-ERROR.
                                        END.
                                    END.
                                END.
                                ELSE DO:

                                    FIND FIRST queasy WHERE queasy.KEY = 161 AND ENTRY(1, queasy.char1, ";") = prcode AND ENTRY(3, queasy.char1, ";") = str
                                        NO-LOCK NO-ERROR.
                                    DO WHILE AVAILABLE queasy:

                                        CREATE queasy.
                                        ASSIGN
                                            queasy.KEY      = 170
                                            queasy.date1    = datum
                                            queasy.char1    = prcode
                                            queasy.number1  = roomnr 
                                            queasy.number2  = INT(ENTRY(loopi,p-list.adult-str, "," ))
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
                                            DO loopk = 1 TO NUM-ENTRIES(bqueasy.char1,";"):
                                                str = ENTRY(loopk, bqueasy.char1, ";").
                                                IF SUBSTR(str,1,9)  = "$defcurr$"   THEN 
                                                    ASSIGN currency = SUBSTR(str,10).
                                                IF currency NE " " THEN LEAVE.
                                            END.
                                            queasy.char3   = currency.
                                        END.*/
                                        FIND FIRST bqueasy WHERE bqueasy.KEY = 18 AND bqueasy.number1 = markno NO-LOCK NO-ERROR.
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
                    
                                        FIND NEXT queasy WHERE queasy.KEY = 161 AND ENTRY(1, queasy.char1, ";") = mesValue AND ENTRY(3, queasy.char1, ";") = str
                                            NO-LOCK NO-ERROR.
                                    END.                                                                        
                                END.                                                            
                            END.
                        END.
                        /*end*/
                    END. 
                END.
            END.                            
        END.
    END.
END.
