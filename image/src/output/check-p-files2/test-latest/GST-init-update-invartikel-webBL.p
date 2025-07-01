DEF TEMP-TABLE t-l-artikel LIKE l-artikel.


DEFINE INPUT PARAMETER TABLE FOR t-l-artikel.

DEF VAR gst-supp AS INT INIT 483.
FOR EACH t-l-artikel BY t-l-artikel.artnr:
    ASSIGN t-l-artikel.lief-nr3 = gst-supp.
    DISP t-l-artikel.artnr t-l-artikel.bezeich.
    UPDATE t-l-artikel.lief-artnr[3].
    IF t-l-artikel.lief-artnr[3] NE "" THEN
    DO:
        RUN gst-init-updatebl.p(t-l-artikel.artnr, gst-supp, t-l-artikel.lief-artnr[3]).
    END.
END.
