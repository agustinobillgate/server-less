DEF TEMP-TABLE t-master LIKE master.
DEF TEMP-TABLE t-guest  LIKE guest.

DEF INPUT PARAMETER resnr           AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER curr-segm       AS INTEGER  NO-UNDO.
DEF OUTPUT PARAMETER bill-receiver  AS CHAR     NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-master.
DEF OUTPUT PARAMETER TABLE FOR t-guest.

DEFINE VARIABLE bill-no AS INTEGER NO-UNDO.
DEFINE BUFFER buff-bill FOR bill. /*FDL*/

  FIND FIRST reservation WHERE reservation.resnr = resnr NO-LOCK.

  FIND FIRST master WHERE master.resnr = resnr NO-ERROR.
  IF NOT AVAILABLE master THEN CREATE master. 

  ASSIGN
    master.resnr        = resnr 
    master.gastnr       = reservation.gastnr 
    master.gastnrpay    = reservation.gastnr 
    master.active       = YES
    master.rechnrstart  = 1
    master.rechnrend    = 1 
    master.umsatzart[1] = YES 
    master.umsatzart[2] = YES 
  . 
 
  FIND FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK. 
  bill-receiver = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
    + guest.anredefirma. 
  FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK. 
  counters.counter = counters.counter + 1. 
  FIND CURRENT counter NO-LOCK. 
  master.rechnr = counters.counter. 

  FIND FIRST bill WHERE bill.resnr = resnr
      AND bill.reslinnr = 0 NO-ERROR.
  IF NOT AVAILABLE bill THEN CREATE bill. 
  ASSIGN 
      bill.resnr = resnr 
      bill.reslinnr = 0 
      bill.rgdruck = 1 
      bill.billtyp = 2 
      bill.rechnr = counters.counter 
      bill.gastnr = gastnrpay 
      bill.name = bill-receiver 
      bill.segmentcode = curr-segm
  . 
  bill-no = bill.rechnr.

  FIND CURRENT bill NO-LOCK. 
  FIND CURRENT master NO-LOCK. 
 
  FIND FIRST reservation WHERE reservation.resnr = resnr EXCLUSIVE-LOCK. 
  reservation.verstat = 1. 
  FIND CURRENT reservation NO-LOCK. 

  CREATE t-master.
  BUFFER-COPY master TO t-master.

  CREATE t-guest.
  BUFFER-COPY guest TO t-guest.

  /*FDL Jan 10, 2024 => Ticket 1DBBEB => Validation Double Bill*/
  FIND FIRST buff-bill WHERE buff-bill.rechnr EQ bill-no
      AND buff-bill.resnr EQ 0 AND buff-bill.reslinnr EQ 1
      AND buff-bill.billtyp NE 2 NO-LOCK NO-ERROR.
  IF AVAILABLE buff-bill THEN
  DO:
      /*FDL Debug*/
      MESSAGE 
          "MASTBILL-CREATEBL" SKIP
          "Origin Bill: " bill-no SKIP
          "Double Bill Number: " STRING(buff-bill.rechnr)
          VIEW-AS ALERT-BOX INFO BUTTONS OK.

      FIND CURRENT buff-bill EXCLUSIVE-LOCK.
      DELETE buff-bill.
      RELEASE buff-bill.
  END.
