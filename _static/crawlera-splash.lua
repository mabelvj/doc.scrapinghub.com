function main(splash)
    local host = "proxy.crawlera.com"
    local port = 8010
    local user = "<API key>"
    local password = ""
    local session_header = "X-Crawlera-Session"
    local session_id = "create"

    splash:on_request(function (request)
        request:set_header("X-Crawlera-UA", "desktop")
        request:set_header(session_header, session_id)
        request:set_proxy{host, port, username=user, password=password}
    end)

    splash:on_response_headers(function (response)
        if type(response.headers[session_header]) ~= nil then
            session_id = response.headers[session_header]
        end
    end)

    splash:go(splash.args.url)
    return splash:png()
end