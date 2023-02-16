import io from "socket.io-client";

class ConnectionService {
    private _socket: any; 

    constructor(
        private readonly url: string,
        private readonly timeout: number = 1) // timeout in minutes
    { }

    // TODO: implement failure point 
    initialize(eventsHandlers: { [key: string]: (_: any) => void }): void {
        this._socket = io(
            this.url,
            {
                timeout: this.timeout * 60 * 1000 
            });
            
        this._socket.on("connect", () => { console.log("Connection successfuly established.") })

        Object.keys(eventsHandlers).forEach(key => {
            this._socket.on(key, eventsHandlers[key])
        });

        this._socket.on("disconnect", () => {
            console.log("Closing socket...")
            this._socket.close()
            window.open("/end-session")
          });
    }

    send(command: string, params: any): void {
        if (this._socket.connected) {
            this._socket.emit(command, { path: params.path })
        } else {
            console.error("Impossible to emmit command, since socket is closed.")
        }
    }
}; 

export default ConnectionService;