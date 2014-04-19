include "pe.yar"

rule winsock_wsa
{
    meta:                                        
        description = "Communication Calls (Winsock WSA)"
    strings:
        $ ="WSASocket"
        $ ="WSASend"
        $ ="WSARecv"
        $ ="WSAConnect"
        $ ="WSAIoctl"
        $ ="WSAConnect"
    condition:
        any of them and is_pe
}

rule winsock_generic 
{
    meta:                                        
        description = "Communication Calls (Winsock Generic)"
    strings:
        $ ="socket"
        $ ="send"
        $ ="recv"
        $ ="connect"
        $ ="ioctlsocket"
        $ ="closesocket"
    condition:
        any of them 
}

// Not using
private rule has_winsock
{
    meta:                                        
        description = "Communication Calls (Winsock)"
    condition:
        winsock_wsa or winsock_generic and is_pe
}

