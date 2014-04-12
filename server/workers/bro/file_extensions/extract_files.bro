event file_new(f: fa_file)
    {
        local fname = fmt("%s-%s", f$source, f$id);
        Files::add_analyzer(f, Files::ANALYZER_EXTRACT, [$extract_filename=fname]);
    }
