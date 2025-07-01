DEF TEMP-TABLE t-eg-vendor LIKE eg-vendor.

DEF OUTPUT PARAMETER TABLE FOR t-eg-vendor.

FOR EACH eg-vendor BY eg-vendor.vendor-nr:
    CREATE t-eg-vendor.
    BUFFER-COPY eg-vendor TO t-eg-vendor.
END.
