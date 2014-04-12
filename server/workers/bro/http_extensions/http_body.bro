module HTTP;

export {
    redef record Info += {
	    orig_body_length: 	count &log &optional;
            orig_body_data:	string &log &optional;
	    resp_body_length: 	count &log &optional;
            resp_body_data: 	string &log &optional;
    };
}

event http_entity_data(c: connection, is_orig: bool, length: count, data: string)
{
	if (is_orig)
	{
		if (!c$http?$orig_body_data)
		{
		        c$http$orig_body_data = string_to_ascii_hex(data);
			c$http$orig_body_length = length;
		} else {
			c$http$orig_body_data = string_cat( c$http$orig_body_data, string_to_ascii_hex(data) );
			c$http$orig_body_length += length;
		}

	} else {
		if (!c$http?$resp_body_data)
		{
		        c$http$resp_body_data = string_to_ascii_hex(data);
			c$http$resp_body_length = length;
		} else {
			c$http$resp_body_data = string_cat( c$http$resp_body_data, string_to_ascii_hex(data) );
			c$http$resp_body_length += length;
		}
	}
}
