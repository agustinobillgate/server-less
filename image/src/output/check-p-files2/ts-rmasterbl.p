DEF TEMP-TABLE q1-list
    FIELD rechnr      LIKE bill.rechnr
    FIELD gastnr      LIKE bill.gastnr
    FIELD bill-name   LIKE bill.name
    FIELD name        LIKE guest.name
    FIELD anredefirma LIKE guest.anredefirma
    FIELD groupname   LIKE reservation.groupname
    FIELD saldo       LIKE bill.saldo
    FIELD rec-id      AS INT.

DEF INPUT  PARAMETER h-recid AS INT.
DEF OUTPUT PARAMETER TABLE FOR q1-list.

FIND FIRST vhp.h-bill WHERE RECID(vhp.h-bill) = h-recid NO-LOCK NO-ERROR.
/* FDL Comment => Ticket 533377
IF AVAILABLE vhp.h-bill AND vhp.h-bill.resnr GT 0 THEN
FOR EACH vhp.bill WHERE vhp.bill.flag = 0 
    AND vhp.bill.resnr = vhp.h-bill.resnr AND vhp.bill.reslinnr = 0 NO-LOCK, 
    FIRST vhp.reservation WHERE vhp.reservation.resnr = vhp.bill.resnr NO-LOCK, 
    FIRST vhp.master WHERE vhp.master.resnr = vhp.bill.resnr 
    AND vhp.master.active NO-LOCK, 
    FIRST vhp.guest WHERE vhp.guest.gastnr = vhp.bill.gastnr 
    NO-LOCK BY vhp.bill.name:
    RUN assign-it.
END.
ELSE
*/
FOR EACH vhp.bill WHERE vhp.bill.flag = 0
    AND vhp.bill.zinr = "" AND vhp.bill.resnr GT 0 AND vhp.bill.billtyp = 2
    AND vhp.bill.reslinnr = 0 NO-LOCK,
    FIRST vhp.reservation WHERE vhp.reservation.resnr = vhp.bill.resnr NO-LOCK,
    FIRST vhp.master WHERE vhp.master.resnr = vhp.bill.resnr
    AND vhp.master.active NO-LOCK,
    FIRST vhp.guest WHERE vhp.guest.gastnr = vhp.bill.gastnr 
    NO-LOCK BY vhp.bill.name:
    RUN assign-it.
END.

PROCEDURE assign-it:
    CREATE q1-list.
    ASSIGN
      q1-list.rechnr      = bill.rechnr
      q1-list.gastnr      = bill.gastnr
      q1-list.bill-name   = bill.name
      q1-list.name        = guest.name
      q1-list.anredefirma = guest.anredefirma
      q1-list.groupname   = reservation.groupname
      q1-list.rec-id      = RECID(vhp.bill).
END.
