import { CopyBlock, vs2015 } from "react-code-blocks";
import { useAppSelector } from "../store/hooks";
import { selectSourceCode } from "../store/selectors";

const CodeView = () => {
  const sourceCode = useAppSelector(selectSourceCode)
  const defaulPlaceholder = "// source code here"

  return (
    <div style={{ fontFamily: 'IBM Plex Mono' }}>
      <CopyBlock
        text={sourceCode ?? defaulPlaceholder}
        showLineNumbers
        codeBlock
        language="c"
        theme={vs2015}
      />
    </div>
  );
};

export default CodeView;