DEF TEMP-TABLE t-resline LIKE bk-reser.

DEF INPUT  PARAMETER t-resnr AS INT.
DEF INPUT  PARAMETER t-reslinnr AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-resline.

DEFINE BUFFER resline    FOR bk-reser.

FOR EACH resline WHERE resline.veran-nr EQ t-resnr 
    /*AND resline.veran-resnr = t-reslinnr*/ /*MNAUFAL 261121 - bugs saat cancel all banquet dengan nomor reservasi yg sama hanya 1 yang tercancel*/
    NO-LOCK:
    CREATE t-resline.
    BUFFER-COPY resline TO t-resline.
END.
