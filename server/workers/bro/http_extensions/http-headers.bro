module HTTP;

export
{
	redef record Info += {
		orig_heads:	set[string] &optional &log;
		resp_heads:	set[string] &optional &log;
	};
}

event http_header(c: connection, is_orig: bool, name: string, value: string)
{
	local delim: string = ":";
	local tmp_s_s: set[string] = set();

	if (is_orig)
	{
		if (! c$http?$orig_heads)
		{
			c$http$orig_heads = tmp_s_s;
		}
		add c$http$orig_heads[fmt("%s%s%s", name, delim, value)];
	} else {
		if (! c$http?$resp_heads)
		{
			c$http$resp_heads = tmp_s_s;
		}
		add c$http$resp_heads[fmt("%s%s%s", name, delim, value)];
	}
}
