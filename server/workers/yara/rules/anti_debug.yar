include "pe.yar"

rule process_manip
{
    meta:                                        
        description = "Anti-Debug Imports"
    strings:
        $ = "checkremotedebbugerpresent" nocase
        $ = "isdebuggerpresent" nocase
        $ = "ntqueryinformationprocess" nocase
        $ = "outputdebugstring" nocase
        $ = "queryperformancecounter" nocase
        $ = "gettickcount" nocase
        $ = "findwindow" nocase
    condition:
        any of them and is_pe
}
