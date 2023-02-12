import { CopyBlock, vs2015 } from "react-code-blocks";

const CodeView = () => {
  return (
    <div style={{ fontFamily: 'IBM Plex Mono' }}>
      <CopyBlock
        text={`// code here`}
        showLineNumbers
        highlight="1,4"
        codeBlock
        language="c"
        theme={vs2015}
      />
    </div>
  );
};

export default CodeView;