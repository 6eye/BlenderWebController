#! /usr/bin/env python3

# Copyright (C) <2014> <Joseph Liveccchi, joewashear007@gmail.com>
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


 
from server import WebSocketHttpServer
from server import WebSocketHandler
import customButtons

def main():
    WebSocketHandler.AddCustomButton("", "")
    WebSocketHandler.AddCustomButton("Hello", "Wuit")
    WebSocketHandler.AddCustomButton("World", "Huit")
    run = True
    print()
    print()
    print("*** Starting Websocket Server ***")
    print()
    print("Press Any Key To Quit...")
    print()
    server = WebSocketHttpServer(WebSocketHandler, http_address=('',8000))
    if server.start():
        print()
        server.launch_webpage()
    else:
        print("Error Starting Server")
    while run:
        i = input("Enter Command:")
        if i == "q":
            server.stop()
            print("------------------------------------------")
            run = False
        else:
            if i:
                server.send(i)
    print("Good Bye")

if __name__ == '__main__':
    main()
