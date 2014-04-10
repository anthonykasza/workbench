##! Extract exe, pdf, and cab files.

global ext_map: table[string] of string = {
    ["application/x-dosexec"] = "exe",
    ["application/pdf"] = "pdf",
    ["application/zip"] = "zip",
    ["application/vnd.ms-cab-compressed"] = "cab",
    ["text/plain"] = "txt",
    ["image/jpeg"] = "jpg",
    ["image/png"] = "png",
    ["text/html"] = "html",
} &default ="";

event file_new(f: fa_file)
    {
    if (f?$mime_type && (f$mime_type == "application/x-dosexec" || f$mime_type == "application/pdf" || 
        f$mime_type == "application/vnd.ms-cab-compressed" || f$mime_type == "application/zip"))
        {
        local ext = ext_map[f$mime_type];
        local fname = fmt("%s-%s.%s", f$source, f$id, ext);
        Files::add_analyzer(f, Files::ANALYZER_EXTRACT, [$extract_filename=fname]);
        }
    }