
DEFINE TEMP-TABLE fsl LIKE bk-func 
  FIELD deposit          LIKE bk-veran.deposit 
  FIELD limit-date       LIKE bk-veran.limit-date 
  FIELD deposit-payment  LIKE bk-veran.deposit-payment 
  FIELD payment-date     LIKE bk-veran.payment-date 
  FIELD total-paid       LIKE bk-veran.total-paid 
  FIELD payment-userinit LIKE bk-veran.payment-userinit
  FIELD betriebsnr2      LIKE bk-func.betriebsnr
  FIELD cutoff           LIKE bk-reser.limitdate 
  FIELD raum             LIKE bk-reser.raum
  FIELD grund            LIKE b-storno.grund
  FIELD in-sales         LIKE bk-veran.payment-userinit[9]
  FIELD in-conv          LIKE bk-veran.payment-userinit[9]
  . 

DEFINE TEMP-TABLE bstorno LIKE b-storno.

DEF INPUT  PARAMETER TABLE FOR fsl.
DEF INPUT  PARAMETER resnr               AS INT.
DEF INPUT  PARAMETER resline             AS INT.
DEF INPUT  PARAMETER curr-gastnr         AS INT.
DEF INPUT  PARAMETER curr-amd            AS CHAR.
DEF INPUT  PARAMETER user-init           AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR bstorno.

FOR EACH bstorno :
    DELETE bstorno.
END.

FIND FIRST fsl.
FIND FIRST bk-func WHERE bk-func.veran-nr = resnr 
    AND bk-func.veran-seite = resline NO-LOCK NO-ERROR.
IF NOT AVAILABLE bk-func THEN RETURN. /*FT serverless*/

FIND CURRENT bk-func EXCLUSIVE-LOCK. 
ASSIGN 
  bk-func.ape_getraenke[1] = fsl.ape_getraenke[1] 
  bk-func.ape_getraenke[2] = fsl.ape_getraenke[2] 
  bk-func.ape_getraenke[3] = fsl.ape_getraenke[3] 
  bk-func.ape_getraenke[4] = fsl.ape_getraenke[4] 
  bk-func.ape_getraenke[5] = fsl.ape_getraenke[5] 
  bk-func.ape_getraenke[6] = fsl.ape_getraenke[6]
  bk-func.bemerkung        = fsl.bemerkung
  bk-func.f-menu[1]        = fsl.f-menu[1]
  bk-func.gema             = fsl.gema
  bk-func.rpreis[7]        = fsl.rpreis[7]
  bk-func.rpreis[8]        = fsl.rpreis[8] 
  bk-func.rpersonen[1]     = fsl.rpersonen[1]
  bk-func.vkontrolliert    = fsl.vkontrolliert 
  bk-func.nadkarte[1]      = fsl.nadkarte[1] 
  bk-func.auf_datum        = fsl.auf_datum 
  bk-func.vgeschrieben     = fsl.vgeschrieben
  bk-func.geschenk         = fsl.geschenk . 

FIND CURRENT bk-func NO-LOCK. 
RELEASE bk-func.

FIND FIRST b-storno WHERE b-storno.bankettnr = resnr 
      AND b-storno.breslinnr = resline NO-LOCK NO-ERROR.
IF NOT AVAILABLE b-storno THEN
DO:
  CREATE b-storno.
  ASSIGN
  b-storno.bankettnr = resnr 
  b-storno.breslinnr = resline
  b-storno.gastnr    = curr-gastnr
  b-storno.grund[1]  = fsl.grund[1]
  b-storno.usercode  = "1:" + user-init + ":" + STRING(TODAY) + ":" + STRING(TIME) + ":" + "New Amandment 1" + ";" 
  b-storno.datum     = TODAY.
END.
ELSE 
DO:
  FIND CURRENT b-storno EXCLUSIVE-LOCK.
  CASE curr-amd:
      WHEN "1" THEN
      DO:
          IF b-storno.grund[1] EQ ""  THEN
          DO:
              b-storno.grund[1]  = fsl.grund[1].
              b-storno.usercode  = b-storno.usercode + "1:" + user-init + ":" + STRING(TODAY) + ":" + STRING(TIME) + ":" + "New Amandment 1" + ";".
          END.
          IF b-storno.grund[1] NE "" THEN
          DO:
              b-storno.grund[1] = fsl.grund[1].
              b-storno.usercode = b-storno.usercode + "1:" + user-init + ":" + STRING(TODAY) + ":" + STRING(TIME) + ":" + "Change Amandment 1" + ";".
          END.
      END.
      WHEN "2" THEN
      DO:
          IF b-storno.grund[2] EQ ""  THEN
          DO:
              b-storno.grund[2]  = fsl.grund[2].
              b-storno.usercode  = b-storno.usercode + "2:" + user-init + ":" + STRING(TODAY) + ":" + STRING(TIME) + ":" + "New Amandment 2" + ";".
          END.
          ELSE IF b-storno.grund[2] NE "" THEN
          DO:
              b-storno.grund[2]  = fsl.grund[2].
              b-storno.usercode  = b-storno.usercode + "2:" + user-init + ":" + STRING(TODAY) + ":" + STRING(TIME) + ":" + "Change Amandment 2" + ";".
          END.
      END.
      WHEN "3" THEN
      DO:
          IF b-storno.grund[3] EQ ""  THEN
          DO:
              b-storno.grund[3]  = fsl.grund[3].
              b-storno.usercode  = b-storno.usercode + "3:" + user-init + ":" + STRING(TODAY) + ":" + STRING(TIME) + ":" + "New Amandment 3" + ";".
          END.
          ELSE IF b-storno.grund[3] NE "" THEN
          DO:
              b-storno.grund[3]  = fsl.grund[3].
              b-storno.usercode  = b-storno.usercode + "3:" + user-init + ":" + STRING(TODAY) + ":" + STRING(TIME) + ":" + "Change Amandment 3" + ";".
          END.              
      END.
      WHEN "4" THEN
      DO:
          IF b-storno.grund[4] EQ ""  THEN
          DO:
              b-storno.grund[4]  = fsl.grund[4].
              b-storno.usercode  = b-storno.usercode + "4:" + user-init + ":" + STRING(TODAY) + ":" + STRING(TIME) + ":" + "New Amandment 4 " + ";".
          END.
          ELSE IF b-storno.grund[4] NE "" THEN
          DO:
              b-storno.grund[4]  = fsl.grund[4].
              b-storno.usercode  = b-storno.usercode + "4:" + user-init + ":" + STRING(TODAY) + ":" + STRING(TIME) + ":" + "Change Amandment 4" + ";".
          END.
      END.
      WHEN "5" THEN
      DO:
          IF b-storno.grund[5] EQ ""  THEN
          DO:
              b-storno.grund[5]  = fsl.grund[5].
              b-storno.usercode  = b-storno.usercode + "5:" + user-init + ":" + STRING(TODAY) + ":" + STRING(TIME) + ":" + "New Amandment 5" + ";".
          END.
          ELSE IF b-storno.grund[5] NE "" THEN
          DO:
              b-storno.grund[5]  = fsl.grund[5].
              b-storno.usercode  = b-storno.usercode + "5:" + user-init + ":" + STRING(TODAY) + ":" + STRING(TIME) + ":" + "Change Amandment 5" + ";".
          END.              
      END.
      WHEN "6" THEN
      DO:
          IF b-storno.grund[6] EQ ""  THEN
          DO:
              b-storno.grund[6]  = fsl.grund[6].
              b-storno.usercode  = b-storno.usercode + "6:" + user-init + ":" + STRING(TODAY) + ":" + STRING(TIME) + ":" + "New Amandment 6" + ";".
          END.
          ELSE IF b-storno.grund[6] NE "" THEN
          DO:
              b-storno.grund[6]  = fsl.grund[6].
              b-storno.usercode  = b-storno.usercode + "6:" + user-init + ":" + STRING(TODAY) + ":" + STRING(TIME) + ":" + "Change Amandment 6" + ";".
          END.
      END.
      WHEN "7" THEN
      DO:
          IF b-storno.grund[7] EQ ""  THEN
          DO:
              b-storno.grund[7]  = fsl.grund[7].
              b-storno.usercode  = b-storno.usercode + "7:" + user-init + ":" + STRING(TODAY) + ":" + STRING(TIME) + ":" + "New Amandment 7" + ";".
          END.
          ELSE IF b-storno.grund[7] NE "" THEN
          DO:
              b-storno.grund[7]  = fsl.grund[7].
              b-storno.usercode  = b-storno.usercode + "7:" + user-init + ":" + STRING(TODAY) + ":" + STRING(TIME) + ":" + "Change Amandment 7" + ";". /*";".FT serverless*/
          END.              
      END.
      WHEN "8" THEN
      DO:
          IF b-storno.grund[8] EQ ""  THEN
          DO:
              b-storno.grund[8]  = fsl.grund[8].
              b-storno.usercode  = b-storno.usercode + "8:" + user-init + ":" + STRING(TODAY) + ":" + STRING(TIME) + ":" + "New Amandment 8" + ";".
          END.
          ELSE IF b-storno.grund[8] NE "" THEN
          DO:
              b-storno.grund[8]  = fsl.grund[8].
              b-storno.usercode  = b-storno.usercode + "8:" + user-init + ":" + STRING(TODAY) + ":" + STRING(TIME) + ":" + "Change Amandment 8" + ";".
          END.
      END.
      WHEN "9" THEN
      DO:
          IF b-storno.grund[9] EQ ""  THEN
          DO:
              b-storno.grund[9]  = fsl.grund[9].
              b-storno.usercode  = b-storno.usercode + "9:" + user-init + ":" + STRING(TODAY) + ":" + STRING(TIME) + ":" + "New Amandment 9" + ";".
          END.
          ELSE IF b-storno.grund[9] NE "" THEN
          DO:
              b-storno.grund[9]  = fsl.grund[9].
              b-storno.usercode  = b-storno.usercode + "9:" + user-init + ":" + STRING(TODAY) + ":" + STRING(TIME) + ":" + "Change Amandment 9" + ";".
          END.              
      END.
      WHEN "10" THEN
      DO:
          IF b-storno.grund[10] EQ ""  THEN
          DO:
              b-storno.grund[10]  = fsl.grund[10].
              b-storno.usercode  = b-storno.usercode + "10:" + user-init + ":" + STRING(TODAY) + ":" + STRING(TIME) + ":" + "New Amandment 10" + ";".
          END.
          ELSE IF b-storno.grund[10] NE "" THEN
          DO:
              b-storno.grund[10]  = fsl.grund[10].
              b-storno.usercode  = b-storno.usercode + "10:" + user-init + ":" + STRING(TODAY) + ":" + STRING(TIME) + ":" + "Change Amandement 10" + ";".
          END.              
      END.
  END CASE.
  FIND CURRENT b-storno NO-LOCK.
  RELEASE b-storno.
END.

FOR EACH b-storno WHERE b-storno.bankettnr = resnr 
  AND b-storno.breslinnr = resline AND b-storno.gastnr = curr-gastnr NO-LOCK:
    CREATE bstorno.
    BUFFER-COPY b-storno TO bstorno.
END.


