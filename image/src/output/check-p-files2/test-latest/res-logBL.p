DEFINE TEMP-TABLE res-log
  FIELD flag AS CHAR FORMAT "x(1)" LABEL " " 
  FIELD his-recid AS INTEGER 
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
  FIELD id1      AS CHAR FORMAT "x(4)" LABEL "ID " 
  FIELD id2      AS CHAR FORMAT "x(4)" LABEL "ID " 
  FIELD date1    AS DATE LABEL "Chg-Date" 
  FIELD date2    AS DATE LABEL "Chg-Date" 
  FIELD zeit     AS INTEGER. 

DEFINE INPUT  PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEFINE INPUT  PARAMETER inp-resnr    AS INTEGER  NO-UNDO.
DEFINE INPUT  PARAMETER inp-reslinnr AS INTEGER  NO-UNDO.
DEFINE OUTPUT PARAMETER avail-res    AS LOGICAL.
DEFINE OUTPUT PARAMETER tittle       AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR res-log.

{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "res-log". 
    
/************************* MAIN LOGIC *****************************/
FIND FIRST res-line WHERE res-line.resnr = inp-resnr 
  AND res-line.reslinnr = inp-reslinnr NO-LOCK NO-ERROR. 
IF AVAILABLE res-line THEN 
DO:
    avail-res = YES.
    tittle  = " ! " + res-line.name + " -  ResNo: " + STRING(res-line.resnr). 
END.
    /*b1:TITLE = b1:TITLE + " ! " 
  + res-line.name + " -  ResNo: " + STRING(resnr). 
      */
RUN create-list.

/************************ PROCEDURE ************************/
PROCEDURE create-list: 
DEFINE buffer zimkateg1 FOR zimkateg. 
  FOR EACH reslin-queasy WHERE key = "ResChanges" 
    AND reslin-queasy.resnr = inp-resnr 
    AND reslin-queasy.reslinnr = inp-reslinnr
    AND reslin-queasy.char3 NE ? NO-LOCK: 
    
    CREATE res-log. 

    IF reslin-queasy.char3 MATCHES("*;*") THEN
    DO:
      ASSIGN
        res-log.ankunft1 = DATE(ENTRY(1,reslin-queasy.char3,";")) 
        res-log.ankunft2 = DATE(ENTRY(2,reslin-queasy.char3,";"))
        res-log.abreise1 = DATE(ENTRY(3,reslin-queasy.char3,";")) 
        res-log.abreise2 = DATE(ENTRY(4,reslin-queasy.char3,";")) 
        res-log.qty1     = INTEGER(ENTRY(5,reslin-queasy.char3,";"))
        res-log.qty2     = INTEGER(ENTRY(6,reslin-queasy.char3,";")) 
        res-log.Adult1   = INTEGER(ENTRY(7,reslin-queasy.char3,";"))
        res-log.adult2   = INTEGER(ENTRY(8,reslin-queasy.char3,";"))
        res-log.child1   = INTEGER(ENTRY(9,reslin-queasy.char3,";"))
        res-log.child2   = INTEGER(ENTRY(10,reslin-queasy.char3,";"))
        res-log.comp1    = INTEGER(ENTRY(11,reslin-queasy.char3,";"))
        res-log.comp2    = INTEGER(ENTRY(12,reslin-queasy.char3,";"))
        res-log.zinr1    = ENTRY(15,reslin-queasy.char3,";")
        res-log.zinr2    = ENTRY(16,reslin-queasy.char3,";")
        res-log.argt1    = ENTRY(17,reslin-queasy.char3,";") 
        res-log.argt2    = ENTRY(18,reslin-queasy.char3,";") 
        res-log.rate1    = DECIMAL(ENTRY(19,reslin-queasy.char3,";"))
        res-log.rate2    = DECIMAL(ENTRY(20,reslin-queasy.char3,";")) 
        res-log.id1      = ENTRY(21,reslin-queasy.char3,";")
        res-log.id2      = ENTRY(22,reslin-queasy.char3,";") 
        res-log.name1    = ENTRY(25,reslin-queasy.char3,";") 
        res-log.name2    = ENTRY(26,reslin-queasy.char3,";") 
        res-log.fixrate1 = ENTRY(27,reslin-queasy.char3,";") 
        res-log.fixrate2 = ENTRY(28,reslin-queasy.char3,";") NO-ERROR
      . 

      IF TRIM(ENTRY(23,reslin-queasy.char3,";")) = "" THEN res-log.date1 = ?. 
      ELSE res-log.date1 = DATE(ENTRY(23,reslin-queasy.char3,";")).       
      IF TRIM(ENTRY(24,reslin-queasy.char3,";")) = "" THEN res-log.date2 = ?. 
      ELSE res-log.date2 = DATE(ENTRY(24,reslin-queasy.char3,";")). 

      FIND FIRST zimkateg WHERE zimkateg.zikatnr 
        = INTEGER(ENTRY(13,reslin-queasy.char3,";")) NO-LOCK NO-ERROR. 
      FIND FIRST zimkateg1 WHERE zimkateg1.zikatnr 
        = INTEGER(ENTRY(14,reslin-queasy.char3,";")) NO-LOCK NO-ERROR. 
      IF AVAILABLE zimkateg THEN res-log.rmcat1 
        = STRING(zimkateg.kurzbez,"x(6)"). 
      IF AVAILABLE zimkateg1 THEN res-log.rmcat2 
        = STRING(zimkateg1.kurzbez,"x(6)"). 

    END.                                 
    ELSE 
    DO:
      FIND FIRST zimkateg WHERE zimkateg.zikatnr 
        = INTEGER(TRIM(SUBSTR(char3, 51, 3))) NO-LOCK NO-ERROR. 
      FIND FIRST zimkateg1 WHERE zimkateg1.zikatnr 
        = INTEGER(TRIM(SUBSTR(char3, 54, 3))) NO-LOCK NO-ERROR. 
      res-log.ankunft1 = DATE(SUBSTR(char3, 1, 8)). 
      res-log.ankunft2 = DATE(SUBSTR(char3, 9, 8)). 
      res-log.abreise1 = DATE(SUBSTR(char3, 17, 8)). 
      res-log.abreise2 = DATE(SUBSTR(char3, 25, 8)). 
      res-log.qty1 = INTEGER(SUBSTR(char3, 33, 3)). 
      res-log.qty2 = INTEGER(SUBSTR(char3, 36, 3)). 
      res-log.Adult1 = INTEGER(SUBSTR(char3, 39, 2)). 
      res-log.adult2 = INTEGER(SUBSTR(char3, 41, 2)). 
      res-log.child1 = INTEGER(SUBSTR(char3, 43, 2)). 
      res-log.child2 = INTEGER(SUBSTR(char3, 45, 2)). 
      res-log.comp1 = INTEGER(SUBSTR(char3, 47, 2)). 
      res-log.comp2 = INTEGER(SUBSTR(char3, 49, 2)). 
      IF AVAILABLE zimkateg THEN res-log.rmcat1 
        = STRING(zimkateg.kurzbez,"x(6)"). 
      IF AVAILABLE zimkateg1 THEN res-log.rmcat2 
        = STRING(zimkateg1.kurzbez,"x(6)"). 
      res-log.zinr1 = SUBSTR(char3, 57, 4). 
      res-log.zinr2 = SUBSTR(char3, 61, 4). 
      res-log.argt1 = SUBSTR(char3, 65, 5). 
      res-log.argt2 = SUBSTR(char3, 70, 5). 
      res-log.rate1 = DECIMAL(SUBSTR(char3, 75, 12)). 
      res-log.rate2 = DECIMAL(SUBSTR(char3, 87, 12)). 
      res-log.id1 = SUBSTR(char3, 99, 2). 
      res-log.id2 = SUBSTR(char3, 101, 2). 
      
      res-log.date1 = DATE(SUBSTR(char3, 103, 8)) NO-ERROR. 
      IF SUBSTR(char3, 111, 8) = "        " THEN res-log.date2 = ?. 
      ELSE res-log.date2 = DATE(SUBSTR(char3, 111, 8)) NO-ERROR. 
      
      IF LENGTH(char3) GT 120 THEN 
      DO: 
        res-log.name1 = SUBSTR(char3, 119, 16). 
        res-log.name2 = SUBSTR(char3, 135, 16). 
      END. 
      IF length(char3) GT 151 THEN 
      DO: 
        res-log.fixrate1 = SUBSTR(char3, 151, 3). 
        res-log.fixrate2 = SUBSTR(char3, 154, 3). 
      END.                  
    END.
    
    res-log.zeit = reslin-queasy.number2. 
 
    FIND FIRST res-history WHERE res-history.resnr = inp-resnr 
      AND res-history.reslinnr = inp-reslinnr 
      AND res-history.datum = reslin-queasy.date2 
      AND res-history.zeit = reslin-queasy.number2 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE res-history THEN 
    DO: 
        res-log.his-recid = RECID(res-history). 
        res-log.flag = "*". 
    END. 
  END. 
END. 
