import { CopyBlock } from "react-code-blocks";

const CodeView = () => {
  return (
    <div className="h-full" style={{ fontFamily: 'IBM Plex Mono' }}>
      <CopyBlock
        text={`function toBe() {
    if (Math.random() < 0.5) {
    return true;
    } else {
    return false;
        }
rrcsreturn false;
        }

    return true;
    } else {
    return false;
    ieturn false;
        }

    return true;
    } else {
    return false;
    ieturn false;
        }

    return true;
    } else {
    return false;
    i
    return true;
    } else {
    return false;
    if (Math.random() < 0.5) {
    return true;
    } else {
    return false;
    if (Math.random() < 0.5) {
    return true;
    } else {
    return false;
    if (Math.random() < 0.5) {
    return true;
    } else {
    return false;
    if (Math.random() < 0.5) {
    return true;
    } else {
    return false;
    if (Math.random() < 0.5) {
    return true;
    } else {
    return false;
    if (Math.random() < 0.5) {
    return true;
    } else {
    return false;
    if (Math.random() < 0.5) {
    return true;
    } else {
    return false;
 
    }`}
        showLineNumbers
        highlight="1,4"
        codeBlock
        language="js"
        theme="dracula"
      />
    </div>
  );
};

export default CodeView;