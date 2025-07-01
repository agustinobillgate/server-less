
DEF INPUT  PARAMETER pvILanguage   AS INTEGER      NO-UNDO.
DEFINE OUTPUT PARAMETER i       AS INTEGER INIT 0 NO-UNDO.
DEFINE OUTPUT PARAMETER msg-str AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mn-start".

DEFINE VARIABLE ci-date AS DATE.
DEFINE VARIABLE bill-date AS DATE.
DEFINE BUFFER t-zimmer FOR zimmer.

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.

/*FD July 22, 20222 => Ticket 5F2EE7*/
FIND FIRST htparam WHERE paramnr = 110 NO-LOCK.  /*Invoicing DATE */ 
bill-date = htparam.fdate.  

RUN update-zistatus.

PROCEDURE update-zistatus: 
DEFINE VARIABLE i   AS INTEGER INITIAL 0. 
DEFINE BUFFER zbuff FOR zimmer.
DEFINE BUFFER qbuff FOR queasy.

  FOR EACH res-line WHERE res-line.active-flag = 1 
      AND res-line.resstatus EQ 6 NO-LOCK: 
    i = i + 1. 
    FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK 
      NO-ERROR. 
    IF NOT AVAILABLE zimmer THEN 
    DO: 
      FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK. 
      msg-str = msg-str + CHR(2) + "&W"
              + translateExtended ("ALARM: RmNo incorrect -> Updating Room Status not possible :",lvCAREA,"") 
              + CHR(10)
              + translateExtended ("ResNo :",lvCAREA,"") + STRING(res-line.resnr) + " - " + guest.name.
    END. 
    ELSE 
    DO TRANSACTION: 
      FIND CURRENT zimmer EXCLUSIVE-LOCK. 
      IF res-line.abreise = ci-date THEN zimmer.zistatus = 3.  /* Expct Depart */ 
      ELSE IF res-line.abreise GT ci-date THEN 
        zimmer.zistatus = 4. /* uncleaned */ 
      zimmer.bediener-nr-stat = 0. 
      FIND CURRENT zimmer NO-LOCK. 
    END. 
  END. 
 
  i = 0. 
  FIND FIRST zimmer WHERE zimmer.zistatus = 6 AND sleeping NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE zimmer: 
    FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr 
        AND outorder.gespende LT ci-date NO-LOCK NO-ERROR.
    IF AVAILABLE outorder THEN DO:
        /*ITA 180219 --> masalah jika terdapat lebih dari satu OOO untuk kamar yang sama
        IF outorder.gespende LT ci-date THEN */
        DO TRANSACTION: 
          RUN genoooroombl.p(outorder.zinr).
          i = i + 1. 
          FIND CURRENT zimmer EXCLUSIVE-LOCK. 
          zimmer.zistatus = 2. 

          /*ITA 301019 --> tidak tercreate ke statistik untuk periode yang berakhir dihari yang sama*/
          /*IF outorder.gespende = ci-date THEN*/
          DO:
              FIND FIRST zinrstat WHERE zinrstat.zinr = "ooo" AND zinrstat.datum = outorder.gespende NO-ERROR. 
              IF NOT AVAILABLE zinrstat THEN 
              DO: 
                CREATE zinrstat. 
                ASSIGN 
                  zinrstat.datum = outorder.gespende 
                  zinrstat.zinr = "ooo". 
              END. 
              zinrstat.zimmeranz = zinrstat.zimmeranz + 1. 
          END.
         

          FIND CURRENT outorder EXCLUSIVE-LOCK. 
          DELETE outorder.
          RELEASE outorder.
          zimmer.bediener-nr-stat = 0. 
          FIND CURRENT zimmer NO-LOCK. 
        END. 
    END.
    FIND NEXT zimmer WHERE zimmer.zistatus = 6 NO-LOCK NO-ERROR. 
  END. 

  /*delete OM*/
  FOR EACH zimmer NO-LOCK:
    FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr
        AND outorder.betriebsnr GT 1 NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE outorder :
        IF outorder.gespende LT ci-date THEN 
        DO TRANSACTION: 
          i = i + 1. 
          FIND CURRENT outorder EXCLUSIVE-LOCK. 
          DELETE outorder.
          RELEASE outorder.
        END. 
        FIND NEXT outorder WHERE outorder.zinr = zimmer.zinr
            AND outorder.betriebsnr GT 1 NO-LOCK NO-ERROR.
    END.
  END. /*end.*/

  FOR EACH outorder WHERE outorder.gespstart LE ci-date /*bill-date*/ /*FDL Comment > EEB182*/
      AND outorder.betriebsnr LE 1 NO-LOCK: 
    FIND FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK NO-ERROR. 
    IF AVAILABLE zimmer AND zimmer.zistatus LE 2 THEN 
    DO TRANSACTION: 
      FIND CURRENT zimmer EXCLUSIVE-LOCK. 
      zimmer.zistatus = 6. 
      FIND CURRENT zimmer NO-LOCK. 
    END. 
  END. 
 
  FIND FIRST htparam WHERE paramnr = 250 NO-LOCK. 
  IF htparam.flogical THEN 
  DO: 
    FIND FIRST zimmer WHERE zimmer.zistatus = 0 NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE zimmer: 
      DO TRANSACTION: 
        FIND CURRENT zimmer EXCLUSIVE-LOCK. 
        zimmer.zistatus = 1. 
        zimmer.bediener-nr-stat = 0. 
        FIND CURRENT zimmer NO-LOCK. 
      END. 
      FIND NEXT zimmer WHERE zimmer.zistatus = 0 NO-LOCK NO-ERROR. 
    END. 
  END. 
 
  FIND FIRST zimmer WHERE zimmer.features NE "" NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE zimmer:
    DO TRANSACTION: 
      FIND FIRST zbuff WHERE RECID(zbuff) = RECID(zimmer) EXCLUSIVE-LOCK. 
      ASSIGN 
          zbuff.features = ""
          zbuff.house-status = 0
      .
      FIND CURRENT zbuff NO-LOCK. 
    END. 
    FIND NEXT zimmer WHERE zimmer.features NE "" NO-LOCK NO-ERROR. 
  END.

  FIND FIRST queasy WHERE queasy.KEY = 162 NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE queasy:
      DO TRANSACTION:
          FIND FIRST qbuff WHERE RECID(qbuff) = RECID(queasy).
          DELETE qbuff.
          RELEASE qbuff.
          FIND NEXT queasy WHERE queasy.KEY = 162 NO-LOCK NO-ERROR.
      END.
  END.
END.
