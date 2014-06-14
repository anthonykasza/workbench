##! Extract exe, pdf, jar and cab files.

global ext_map: table[string] of string = {
    ["application/x-dosexec"] = "exe",
    ["application/pdf"] = "pdf",
    ["application/zip"] = "zip",
    ["application/jar"] = "jar",
    ["application/vnd.ms-cab-compressed"] = "cab",
    ["text/plain"] = "txt",
    ["image/gif"] = "gif",
    ["image/jpeg"] = "jpg",
    ["image/png"] = "png",
    ["text/html"] = "html",
    ["application/vnd.ms-fontobject"] = "ms_font",
    ["application/x-shockwave-flash"] = "swf"
} &default ="unknown";

event file_new(f: fa_file)
    {
    if (!f?$mime_type) return;
    local ext = ext_map[f$mime_type];
    if (ext != "txt" && ext != "html" && ext != "ms_font" && ext != "jpg" && ext != "gif" && ext != "png")
        {
        local fname = fmt("%s-%s.%s", f$source, f$id, ext);
        Files::add_analyzer(f, Files::ANALYZER_EXTRACT, [$extract_filename=fname]);
        }
    }
