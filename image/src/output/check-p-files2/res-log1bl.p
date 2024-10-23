/******************** DEFINE TEMP TABLE ********************/
DEFINE TEMP-TABLE res-log1 
  FIELD flag     AS INTEGER INITIAL 0 
  FIELD resnr    AS INTEGER LABEL "ResNo" FORMAT ">>,>>>,>>9" 
  FIELD name     AS CHAR FORMAT "x(24)" LABEL "Reserved Name" 
  FIELD ankunft1 AS DATE LABEL "Arrival" 
  FIELD ankunft2 AS DATE LABEL "Arrival" 
  FIELD abreise1 AS DATE LABEL "Departure" 
  FIELD abreise2 AS DATE LABEL "Departure" 
  FIELD qty1     AS INTEGER FORMAT ">>9" LABEL "Qty" 
  FIELD qty2     AS INTEGER FORMAT ">>9" LABEL "Qty" 
  FIELD Adult1   AS INTEGER FORMAT ">9" LABEL "A " 
  FIELD adult2   AS INTEGER FORMAT ">9" LABEL "A " 
  FIELD child1   AS INTEGER FORMAT ">9" LABEL "Ch" 
  FIELD child2   AS INTEGER FORMAT ">9" LABEL "Ch" 
  FIELD comp1    AS INTEGER FORMAT ">9" LABEL "CO" 
  FIELD comp2    AS INTEGER FORMAT ">9" LABEL "CO" 
  FIELD rmcat1   AS CHAR FORMAT "x(6)" LABEL "RmCat" 
  FIELD rmcat2   AS CHAR FORMAT "x(6)" LABEL "RmCat" 
  FIELD zinr1    LIKE zimmer.zinr LABEL "RmNo" 
  FIELD zinr2    LIKE zimmer.zinr LABEL "RmNo" 
  FIELD argt1    AS CHAR FORMAT "x(5)" LABEL "ArgtCode" 
  FIELD argt2    AS CHAR FORMAT "x(5)" LABEL "ArgtCode" 
  FIELD rate1    AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "RoomRate" 
  FIELD rate2    AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "RoomRate" 
  FIELD fixrate1 AS CHAR FORMAT "x(3)"  LABEL "FixRate" 
  FIELD fixrate2 AS CHAR FORMAT "x(3)"  LABEL "FixRate" 
  FIELD name1    AS CHAR FORMAT "x(16)" LABEL "GuestName" 
  FIELD name2    AS CHAR FORMAT "x(16)" LABEL "GuestName" 
  FIELD id1      AS CHAR FORMAT "x(3)" LABEL "ID " 
  FIELD id2      AS CHAR FORMAT "x(3)" LABEL "ID " 
  FIELD date1    AS DATE LABEL "Chg-Date" 
  FIELD date2    AS DATE LABEL "Chg-Date" 
  FIELD zeit     AS INTEGER. 

DEFINE INPUT  PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER from-date AS DATE.
DEFINE INPUT  PARAMETER mi-inhouse AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR res-log1.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "res-log1". 

/******************** MAIN LOGIC ********************/
RUN create-list.
/******************** PROCEDURE ********************/
PROCEDURE create-list: 
  DEFINE buffer zimkateg1 FOR zimkateg. 
  DEFINE VARIABLE do-it AS LOGICAL. 

  FOR EACH res-log1: 
    delete res-log1. 
  END. 
 
  FOR EACH reslin-queasy WHERE betriebsnr = 0 AND key = "ResChanges" 
    AND number1 = 0 AND reslin-queasy.date1 = ? AND char3 GT "" 
    AND deci1 = 0 AND logi1 = NO 
    AND reslin-queasy.date2 EQ from-date USE-INDEX k-int_ix NO-LOCK: 
    PROCESS EVENTS. 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr 
      = INTEGER(TRIM(SUBSTR(char3, 51, 3))) NO-LOCK NO-ERROR. 
    FIND FIRST zimkateg1 WHERE zimkateg1.zikatnr 
      = INTEGER(TRIM(SUBSTR(char3, 54, 3))) NO-LOCK NO-ERROR. 
    FIND FIRST res-line WHERE res-line.resnr = reslin-queasy.resnr 
      AND res-line.reslinnr = reslin-queasy.reslinnr NO-LOCK NO-ERROR. 
    FIND FIRST reservation WHERE reservation.resnr = reslin-queasy.resnr 
      NO-LOCK NO-ERROR. 
    do-it = YES. 
    IF mi-inhouse AND AVAILABLE res-line 
      AND res-line.active-flag NE 1 THEN do-it = NO. 
    IF do-it THEN 
    DO: 
      CREATE res-log1. 
      res-log1.resnr = reslin-queasy.resnr. 
      IF AVAILABLE reservation THEN res-log1.name = reservation.name. 

      IF reslin-queasy.char3 MATCHES("*;*") THEN
      DO:
        ASSIGN
          res-log1.ankunft1 = DATE(ENTRY(1,reslin-queasy.char3,";")) 
          res-log1.ankunft2 = DATE(ENTRY(2,reslin-queasy.char3,";"))
          res-log1.abreise1 = DATE(ENTRY(3,reslin-queasy.char3,";")) 
          res-log1.abreise2 = DATE(ENTRY(4,reslin-queasy.char3,";")) 
          res-log1.qty1     = INTEGER(ENTRY(5,reslin-queasy.char3,";"))
          res-log1.qty2     = INTEGER(ENTRY(6,reslin-queasy.char3,";")) 
          res-log1.Adult1   = INTEGER(ENTRY(7,reslin-queasy.char3,";"))
          res-log1.adult2   = INTEGER(ENTRY(8,reslin-queasy.char3,";"))
          res-log1.child1   = INTEGER(ENTRY(9,reslin-queasy.char3,";"))
          res-log1.child2   = INTEGER(ENTRY(10,reslin-queasy.char3,";"))
          res-log1.comp1    = INTEGER(ENTRY(11,reslin-queasy.char3,";"))
          res-log1.comp2    = INTEGER(ENTRY(12,reslin-queasy.char3,";"))
          res-log1.zinr1    = ENTRY(15,reslin-queasy.char3,";")
          res-log1.zinr2    = ENTRY(16,reslin-queasy.char3,";")
          res-log1.argt1    = ENTRY(17,reslin-queasy.char3,";") 
          res-log1.argt2    = ENTRY(18,reslin-queasy.char3,";") 
          res-log1.rate1    = DECIMAL(ENTRY(19,reslin-queasy.char3,";"))
          res-log1.rate2    = DECIMAL(ENTRY(20,reslin-queasy.char3,";")) 
          res-log1.id1      = ENTRY(21,reslin-queasy.char3,";")
          res-log1.id2      = ENTRY(22,reslin-queasy.char3,";") 
          res-log1.name1    = ENTRY(25,reslin-queasy.char3,";") 
          res-log1.name2    = ENTRY(26,reslin-queasy.char3,";") 
          res-log1.fixrate1 = ENTRY(27,reslin-queasy.char3,";") 
          res-log1.fixrate2 = ENTRY(28,reslin-queasy.char3,";") NO-ERROR
        . 

        IF TRIM(ENTRY(23,reslin-queasy.char3,";")) = "" THEN res-log1.date1 = ?. 
        ELSE res-log1.date1 = DATE(ENTRY(23,reslin-queasy.char3,";")).       
        IF TRIM(ENTRY(24,reslin-queasy.char3,";")) = "" THEN res-log1.date2 = ?. 
        ELSE res-log1.date2 = DATE(ENTRY(24,reslin-queasy.char3,";")). 

        FIND FIRST zimkateg WHERE zimkateg.zikatnr 
          = INTEGER(ENTRY(13,reslin-queasy.char3,";")) NO-LOCK NO-ERROR. 
        FIND FIRST zimkateg1 WHERE zimkateg1.zikatnr 
          = INTEGER(ENTRY(14,reslin-queasy.char3,";")) NO-LOCK NO-ERROR. 
        IF AVAILABLE zimkateg THEN res-log1.rmcat1 
          = STRING(zimkateg.kurzbez,"x(6)"). 
        IF AVAILABLE zimkateg1 THEN res-log1.rmcat2 
          = STRING(zimkateg1.kurzbez,"x(6)"). 
      END.
      ELSE
      DO:
        FIND FIRST zimkateg WHERE zimkateg.zikatnr 
          = INTEGER(TRIM(SUBSTR(char3, 51, 3))) NO-LOCK NO-ERROR. 
        FIND FIRST zimkateg1 WHERE zimkateg1.zikatnr 
          = INTEGER(TRIM(SUBSTR(char3, 54, 3))) NO-LOCK NO-ERROR. 
        res-log1.ankunft1 = DATE(SUBSTR(char3, 1, 8)). 
        res-log1.ankunft2 = DATE(SUBSTR(char3, 9, 8)). 
        res-log1.abreise1 = DATE(SUBSTR(char3, 17, 8)). 
        res-log1.abreise2 = DATE(SUBSTR(char3, 25, 8)). 
        res-log1.qty1 = INTEGER(SUBSTR(char3, 33, 3)). 
        res-log1.qty2 = INTEGER(SUBSTR(char3, 36, 3)). 
        res-log1.Adult1 = INTEGER(SUBSTR(char3, 39, 2)). 
        res-log1.adult2 = INTEGER(SUBSTR(char3, 41, 2)). 
        res-log1.child1 = INTEGER(SUBSTR(char3, 43, 2)). 
        res-log1.child2 = INTEGER(SUBSTR(char3, 45, 2)). 
        res-log1.comp1 = INTEGER(SUBSTR(char3, 47, 2)). 
        res-log1.comp2 = INTEGER(SUBSTR(char3, 49, 2)). 
        IF AVAILABLE zimkateg THEN res-log1.rmcat1 
          = STRING(zimkateg.kurzbez,"x(6)"). 
        IF AVAILABLE zimkateg1 THEN res-log1.rmcat2 
          = STRING(zimkateg1.kurzbez,"x(6)"). 
        res-log1.zinr1 = SUBSTR(char3, 57, 4). 
        res-log1.zinr2 = SUBSTR(char3, 61, 4). 
        res-log1.argt1 = SUBSTR(char3, 65, 5). 
        res-log1.argt2 = SUBSTR(char3, 70, 5). 
        res-log1.rate1 = DECIMAL(SUBSTR(char3, 75, 12)). 
        res-log1.rate2 = DECIMAL(SUBSTR(char3, 87, 12)). 
        res-log1.id1 = SUBSTR(char3, 99, 2). 
        res-log1.id2 = SUBSTR(char3, 101, 2). 
        res-log1.date1 = DATE(SUBSTR(char3, 103, 8)). 
        IF SUBSTR(char3, 111, 8) = "        " THEN res-log1.date2 = ?. 
        ELSE res-log1.date2 = DATE(SUBSTR(char3, 111, 8)). 
        IF length(char3) GT 120 THEN 
        DO: 
          res-log1.name1 = SUBSTR(char3, 119, 16). 
          res-log1.name2 = SUBSTR(char3, 135, 16). 
        END. 
        IF length(char3) GT 151 THEN 
        DO: 
          res-log1.fixrate1 = SUBSTR(char3, 151, 3). 
          res-log1.fixrate2 = SUBSTR(char3, 154, 3). 
        END.
      END.
      res-log1.zeit = number2. 
    END. 
  END. 
END.
