DEFINE TEMP-TABLE age-list 
  FIELD nr              AS INTEGER 
  FIELD paint-it        AS LOGICAL INITIAL NO 
  FIELD rechnr          AS INTEGER FORMAT ">>>>>>>>9" 
  FIELD refno           AS INTEGER FORMAT ">>>>>>>>>" 
  FIELD rechnr2         AS INTEGER FORMAT ">>>>>>>>>"
  FIELD opart           AS INTEGER 
  FIELD zahlkonto       AS INTEGER
  FIELD counter         AS INTEGER
  FIELD gastnr          AS INTEGER 
  FIELD company         AS CHAR
  FIELD billname        AS CHAR FORMAT "x(36)" 
  FIELD gastnrmember    AS INTEGER 
  FIELD zinr            AS CHAR   	/*MT 25/07/12 */
  FIELD datum           AS DATE
  FIELD rgdatum         AS DATE 
  FIELD paydatum        AS DATE 
  FIELD user-init       AS CHAR FORMAT "x(2)" 
  FIELD bezeich         AS CHARACTER FORMAT "x(16)" 
  FIELD wabkurz         AS CHAR FORMAT "x(4)" 
  FIELD debt            AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0 
  FIELD credit          AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0 
  FIELD fdebt           AS DECIMAL LABEL "Foreign-Amt" 
                           FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0 
  FIELD t-debt          AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0   /*MT 20/07/12 */
  FIELD tot-debt        AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0   /*MT 20/07/12 */
  FIELD rid             AS INTEGER INITIAL 0
  FIELD dept            AS INTEGER INITIAL 0
  FIELD gname           AS CHAR    FORMAT "x(36)"
  FIELD voucher         AS CHAR    FORMAT "x(12)"
  FIELD ankunft         AS DATE    FORMAT "99/99/99"
  FIELD abreise         AS DATE    FORMAT "99/99/99"
  FIELD stay            AS INTEGER FORMAT ">>9"
  FIELD remarks         AS CHAR    FORMAT "x(50)" /*MT 130812 */
  FIELD ttl             AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0   /*MT 20/07/12 */

  FIELD resname         AS CHAR
  FIELD comp-name       AS CHAR
  FIELD comp-add        AS CHAR
  FIELD comp-fax        AS CHAR
  FIELD comp-phone      AS CHAR
  INDEX idx1 rechnr dept gastnr
    . 

DEFINE INPUT  PARAMETER TABLE FOR age-list.
DEFINE INPUT  PARAMETER t-artnr     AS INTEGER.
DEFINE INPUT  PARAMETER t-dept      AS INTEGER.
DEFINE INPUT  PARAMETER gastpay     AS INTEGER. /* new gastnr */
DEFINE INPUT  PARAMETER a-gastnr    AS INTEGER. /* old gastnr */
DEFINE INPUT  PARAMETER a-rechnr    AS INTEGER.
DEFINE INPUT  PARAMETER user-init   AS CHARACTER. /*sis 161214*/
DEFINE OUTPUT PARAMETER billname    AS CHARACTER. 


DEFINE VARIABLE temp-billnr AS INTEGER NO-UNDO.


/*sis 161214*/
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.
/*end sis*/

FIND FIRST artikel WHERE artikel.artnr = t-artnr 
    AND artikel.departement = t-dept NO-LOCK.

RUN update-debt-gastnr.

PROCEDURE update-debt-gastnr:
DEFINE BUFFER debt FOR debitor. 
 
/* NEW bill receiver record */ 
  FIND FIRST guest WHERE guest.gastnr = gastpay NO-LOCK. 
 
  FOR EACH age-list WHERE age-list.rechnr = a-rechnr 
    AND age-list.gastnr = a-gastnr: 
    age-list.gastnr = gastpay. 
    IF age-list.billname NE "" THEN 
      age-list.billname = guest.name + ", " + guest.vorname1 
                 + guest.anredefirma + " " + guest.anrede1. 
  END. 
 
  FOR EACH debitor WHERE debitor.rechnr = a-rechnr 
    AND debitor.gastnr = a-gastnr AND debitor.artnr = t-artnr 
    AND debitor.opart GE 0 /*AND debitor.betriebsnr = 0*/ NO-LOCK: 
    IF debitor.betriebsnr = 0 THEN
    DO:
        FIND FIRST debt WHERE RECID(debt) = RECID(debitor) EXCLUSIVE-LOCK 
          NO-ERROR. 
        IF AVAILABLE debt THEN 
        DO: 
          debt.gastnr = gastpay. 
          debt.name = guest.name + ", " + guest.vorname1. 
          FIND CURRENT debt NO-LOCK. 
          IF debt.zahlkonto = 0 THEN 
          DO: 
            FIND FIRST bill WHERE bill.rechnr = a-rechnr 
             /* AND bill.gastnr = gastnr */ EXCLUSIVE-LOCK NO-ERROR. 
            IF AVAILABLE bill THEN 
            DO: 
              ASSIGN
                  bill.name   = guest.name + ", " + guest.vorname1  
                  bill.gastnr = gastpay
                  temp-billnr = bill.rechnr
              . 
              FIND CURRENT bill NO-LOCK. 
              IF bill.resnr GT 0 AND bill.reslinnr GT 0 /* guest folio */ THEN
              DO:
                  FIND FIRST res-line WHERE res-line.resnr = bill.resnr
                      AND res-line.reslinnr = bill.parent-nr NO-ERROR.
                  IF AVAILABLE res-line THEN
                  DO:
                      res-line.gastnrpay = gastpay.
                      FIND CURRENT res-line NO-LOCK.
                  END.
              END.
            END. 
          END. 
        END. 
    END. /*betriebsnr = 0*/
    ELSE
    DO:
        FIND FIRST debt WHERE RECID(debt) = RECID(debitor) EXCLUSIVE-LOCK 
          NO-ERROR. 
        IF AVAILABLE debt THEN
        DO:
            /*
            FIND FIRST h-bill WHERE h-bill.rechnr = debitor.rechnr AND
                h-bill.departement = debitor.betriebsnr NO-LOCK NO-ERROR.
            IF AVAILABLE h-bill THEN
            DO:
                IF h-bill.resnr GT 0 AND h-bill.reslinnr = 0 THEN
                DO:
                    IF debt.zahlkonto = 0 THEN
                    DO:
                        FIND CURRENT h-bill EXCLUSIVE-LOCK.
                        ASSIGN h-bill.resnr = gastpay.
                        FIND CURRENT h-bill NO-LOCK.
                    END.
                    debt.gastnr = gastpay. 
                    debt.name = guest.name. 
                    FIND CURRENT debt NO-LOCK. 
                END.
                ELSE
                DO:
                    HIDE MESSAGE NO-PAUSE.
                    MESSAGE 
                        translateExtended("The selected A/R Record was linked with a reservation.", lvCAREA, "")
                        SKIP
                        translateExtended("Update not possible.", lvCAREA, "")
                        VIEW-AS ALERT-BOX INFORMATION.
                    APPLY "entry" TO from-name IN FRAME frame1.
                    RETURN NO-APPLY.
                END.
            END.*/
/*          IF debt.zahlkonto = 0 THEN    */
            DO:
                debt.gastnr = gastpay.
                debt.NAME   = guest.name + ", " + guest.vorname1 .
                FIND CURRENT debt NO-LOCK.
            END.
        END.
    END.
  END. 

  /* sis 16/12/2014 */
  IF gastpay NE a-gastnr THEN 
  DO: 
  DEF BUFFER gbuff FOR guest.
    FIND FIRST gbuff WHERE gbuff.gastnr = a-gastnr NO-LOCK.
    CREATE res-history. 
    ASSIGN 
        res-history.nr          = bediener.nr 
        res-history.datum       = TODAY
        res-history.zeit        = TIME
        res-history.action      = "Bill Receiver Changed". 

    res-history.aenderung =  gbuff.NAME + CHR(10) + CHR(10)
        + "*** Changed to:" + CHR(10) + CHR(10) 
        + guest.NAME + CHR(10) + CHR(10) 
        + "*** Bill No: " + STRING(temp-billnr). 

    IF AVAILABLE bediener THEN res-history.betriebsnr = bediener.nr. 
    FIND CURRENT res-history NO-LOCK.
    RELEASE res-history. 
  END. 

END. 
