import io from "socket.io-client";

class ConnectionService {
    private _socket: any; 

    constructor(
        private readonly url: string,
        private readonly timeout: number = 1) // timeout in minutes
    { }

    // perhaps I have to add mapping to use store actions
    initialize(): void {
        this._socket = io(
            this.url,
            {
                timeout: this.timeout * 60 * 1000 
            });
            
        this._socket.on("connect", () => { console.log("connection successful") })
    }
}; 

export default ConnectionService;