import { CopyBlock } from "react-code-blocks";

const CodeView = () => {
  return (
    <div style={{ fontFamily: 'IBM Plex Mono' }}>
      <CopyBlock
        text={`// code here`}
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