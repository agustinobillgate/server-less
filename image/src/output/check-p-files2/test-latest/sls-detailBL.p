
DEFINE TEMP-TABLE layer1-list
    FIELD datum     LIKE akt-line.datum
    FIELD zeit      LIKE akt-line.zeit
    FIELD kontakt   LIKE akt-line.kontakt
    FIELD bemerk    LIKE akt-line.bemerk
    FIELD fname     LIKE akt-line.fname
    FIELD linenr    LIKE akt-line.linenr.

DEFINE TEMP-TABLE layer2-list
    FIELD linenr      LIKE akt-line.linenr
    FIELD bezeich     LIKE akt-code.bezeich
    FIELD datum       LIKE akt-line.datum
    FIELD zeit        LIKE akt-line.zeit
    FIELD dauer       LIKE akt-line.dauer
    FIELD prioritaet  LIKE akt-line.prioritaet
    FIELD kontakt     LIKE akt-line.kontakt
    FIELD regard      LIKE akt-line.regard.

DEFINE TEMP-TABLE layer3-list
    FIELD aktnr             LIKE akthdr.aktnr
    FIELD flag              LIKE akthdr.flag
    FIELD akthdr-bezeich    LIKE akthdr.bezeich
    FIELD akt-code-bezeich  LIKE akt-code.bezeich
    FIELD wertigkeit        LIKE akt-code.wertigkeit
    FIELD stichwort         LIKE akthdr.stichwort
    FIELD t-betrag          LIKE akthdr.t-betrag
    FIELD erl-datum         LIKE akthdr.erl-datum.

DEFINE INPUT PARAMETER layer AS INT.
DEFINE INPUT PARAMETER inp-gastnr AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR layer1-list.
DEFINE OUTPUT PARAMETER TABLE FOR layer2-list.
DEFINE OUTPUT PARAMETER TABLE FOR layer3-list.

IF layer = 1 THEN DO:
 RUN layer1.
END.
ELSE IF layer = 2 THEN DO:
 RUN layer2.
END.
ELSE IF layer = 3 THEN DO:
  RUN layer3.
END.





PROCEDURE layer1:
   FOR EACH akt-line WHERE akt-line.grupnr = 1 
       AND akt-line.gastnr = inp-gastnr NO-LOCK,
       FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK
       BY akt-line.datum BY akt-line.zeit:

       CREATE layer1-list.
       ASSIGN
            layer1-list.datum     = akt-line.datum
            layer1-list.zeit      = akt-line.zeit
            layer1-list.kontakt   = akt-line.kontakt
            layer1-list.bemerk    = akt-line.bemerk
            layer1-list.fname     = akt-line.fname
            layer1-list.linenr    = akt-line.linenr.

   END.
END.

PROCEDURE layer2:
   FOR EACH akt-line WHERE akt-line.flag = 0 
       AND akt-line.gastnr = inp-gastnr NO-LOCK,
       FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode NO-LOCK
       BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:

       CREATE layer2-list.
       ASSIGN
            layer2-list.linenr      = akt-line.linenr
            layer2-list.bezeich     = akt-code.bezeich
            layer2-list.datum       = akt-line.datum
            layer2-list.zeit        = akt-line.zeit
            layer2-list.dauer       = akt-line.dauer
            layer2-list.prioritaet  = akt-line.prioritaet
            layer2-list.kontakt     = akt-line.kontakt
            layer2-list.regard      = akt-line.regard.

   END.
END.

PROCEDURE layer3:
   FOR EACH akthdr WHERE akthdr.gastnr = inp-gastnr NO-LOCK,
       FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
       FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr NO-LOCK
       BY akthdr.next-datum BY akthdr.stufe DESC:

       CREATE layer3-list.
       ASSIGN
            layer3-list.aktnr             = akthdr.aktnr
            layer3-list.flag              = akthdr.flag
            layer3-list.akthdr-bezeich    = akthdr.bezeich
            layer3-list.akt-code-bezeich  = akt-code.bezeich
            layer3-list.wertigkeit        = akt-code.wertigkeit
            layer3-list.stichwort         = akthdr.stichwort
            layer3-list.t-betrag          = akthdr.t-betrag
            layer3-list.erl-datum         = akthdr.erl-datum.


   END.
END.
