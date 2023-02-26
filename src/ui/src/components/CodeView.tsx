import SyntaxHighlighter from 'react-syntax-highlighter';
import { vs2015 } from 'react-syntax-highlighter/dist/esm/styles/hljs';
import { useAppSelector } from "../store/hooks";
import { selectBreakpoints, selectSourceCode, selectSourceCodeFilePath } from "../store/selectors";


const CodeView = () => {
  const sourceCode = useAppSelector(selectSourceCode);
  const sourceCodeFilePath = useAppSelector(selectSourceCodeFilePath);
  // FIXME: It would not work if path formats are different. Add validation for input path 
  const breakpoints = useAppSelector(selectBreakpoints).filter(breakpoint => breakpoint.source == sourceCodeFilePath);
  const defaulPlaceholder = "// source code here"

  let highlightedLines = breakpoints.map(breakpoint => breakpoint.line_number);

  return (
    <SyntaxHighlighter
      language="csharp"
      wrapLines={true}
      style={vs2015}
      showLineNumbers={true}
      lineProps={(lineNumber) => {
        const style: any = { display: "block", width: "fit-content" };
        if (highlightedLines.includes(lineNumber)) {
          style.backgroundColor = "#762c2c";
          style.color = "#fff"
          style.borderRadius = "4px"
          style.padding = "0 4px 0 4px"
        }
        return { style };
      }}
      className={"syntax-highlighter"}>
      {sourceCode ?? defaulPlaceholder}
    </SyntaxHighlighter>

    /*    <div style={{ fontFamily: 'IBM Plex Mono' }}>
          <CodeBlock
            text={sourceCode ?? defaulPlaceholder}
            showLineNumbers
            highlight={breakpoints.map(b => b.line_number).reduce((prev, curr) => prev + `${curr},`, '')}
            codeContainerStyle={(l:number) =>{ color: 'red'}}
            language="c"
            theme={vs2015}
          />
        </div>*/
  );
};

export default CodeView;