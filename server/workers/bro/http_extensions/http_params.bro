## Monitor HTTP requests for a specific set of unordered parameters 
#
# 	RFC 3986 reserved URI characters (must be encoded if not used as delims)
#		: / ? # [ ] @
#		! $ & ' ( ) * + , ; =

module HTTP;

export {
	redef record Info += {
		params: set[string] &optional &log;
	};
}

function extract_params(uri: string): set[string]
{
	local p: set[string] = set();

	if ( strstr(uri, "?") == 0)
		return p;

	local query: string = split1(uri, /\?/)[2];
	local opv: table[count] of string = split(query, /&/);
	
	for (each in opv)
	{
		add p[ split1(opv[each], /=/)[1] ];
	}
	return p;
}

event http_request(c: connection, method: string, original_URI: string, unescaped_URI: string, version: string)
{
	c$http$params = extract_params(original_URI);
}
