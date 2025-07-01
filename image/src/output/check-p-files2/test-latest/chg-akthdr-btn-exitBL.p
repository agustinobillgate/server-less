
DEFINE TEMP-TABLE akthdr1 LIKE akthdr.

DEF INPUT PARAMETER TABLE FOR akthdr1.

FIND FIRST akthdr1.
FIND FIRST akthdr WHERE akthdr.aktnr = akthdr1.aktnr EXCLUSIVE-LOCK.
BUFFER-COPY akthdr1 TO akthdr.
FIND CURRENT akthdr NO-LOCK.
