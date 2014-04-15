module Conn;
 
export {
	redef record Info += {
		orig_asn: count &optional &log;
		resp_asn: count &optional &log;
	};
}
 
event connection_state_remove(c: connection) 
{
	local orig_asn: count = lookup_asn(c$id$orig_h);
	if (! c$conn?$orig_asn)
	{
		c$conn$orig_asn = orig_asn;
	}
 
	local resp_asn: count = lookup_asn(c$id$resp_h);
	if (! c$conn?$resp_asn)
	{
		c$conn$resp_asn = resp_asn;
	}
}
