import "./EndSession.css";

// FIXME: Not only on closing socket, but also on unscussessful connection
const EndSession = () => {
    return (
    <div className="text-white p-1 background">
        <div>The session has been interrupted or ended.</div>
        <div>Restart dotgdb please!</div>
    </div>);
};

export default EndSession;