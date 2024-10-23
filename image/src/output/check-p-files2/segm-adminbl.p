DEF TEMP-TABLE sbuff LIKE segment
    FIELD long-bezeich AS CHAR.

DEF OUTPUT PARAMETER TABLE FOR sbuff.

FOR EACH segment /*WHERE segment.vip-level = 0*/ NO-LOCK 
    BY segment.betriebsnr BY segment.segmentgrup BY segment.segmentcode:
    CREATE sbuff.
    BUFFER-COPY segment TO sbuff.
    ASSIGN sbuff.long-bezeich = segment.bezeich.
END.
