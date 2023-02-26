import SyntaxHighlighter from 'react-syntax-highlighter';
import { vs2015 } from 'react-syntax-highlighter/dist/esm/styles/hljs';
import { useAppDispatch, useAppSelector } from "../store/hooks";
import { selectBreakpoints, selectSourceCode, selectSourceCodeFilePath } from "../store/selectors";
import { setBreakpoint } from '../store/store';


const CodeView = () => {
  const dispatch = useAppDispatch();
  const sourceCode = useAppSelector(selectSourceCode);
  const sourceCodeFilePath = useAppSelector(selectSourceCodeFilePath);

  // FIXME: It would not work if path formats are different. Add validation for input path 
  const breakpoints = useAppSelector(selectBreakpoints).filter(breakpoint => breakpoint.source == sourceCodeFilePath);
  const defaulPlaceholder = "// source code here"

  let highlightedLines = breakpoints.map(breakpoint => breakpoint.line_number);
  const placeBreakpoint = (lineNumber: number) => dispatch(setBreakpoint("break", ""))

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
          style.cursor = "default"
        } else {
          style.cursor = "pointer"
        }
        return { style, onClick: () => placeBreakpoint(lineNumber) };
      }}
      className={"syntax-highlighter"}>
      {sourceCode ?? defaulPlaceholder}
    </SyntaxHighlighter>
  );
};

export default CodeView;