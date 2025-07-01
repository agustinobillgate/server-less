
DEF TEMP-TABLE t-guest          LIKE guest.

DEF INPUT  PARAMETER guestnr        AS INT.
DEF INPUT  PARAMETER gastnr         AS INT.
DEF OUTPUT PARAMETER guestname      AS CHAR.
DEF OUTPUT PARAMETER ind-flag       AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR t-guest.

DEFINE VARIABLE ind-gastnr          AS INTEGER NO-UNDO.
DEFINE VARIABLE wig-gastnr          AS INTEGER NO-UNDO.

FIND FIRST guest WHERE guest.gastnr = guestnr NO-LOCK. 
guestname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
          + " " + guest.anrede1.

FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK.
CREATE t-guest.
BUFFER-COPY guest TO t-guest.

RUN htpint.p(109, OUTPUT wig-gastnr).
RUN htpint.p(123, OUTPUT ind-gastnr).

IF (guest.gastnr = wig-gastnr) OR (guest.gastnr = ind-gastnr) THEN
    ind-flag = YES.
/* SY 16 July 2015 no longer needed
RUN htplogic.p (76, OUTPUT logicalFlag).
*/
