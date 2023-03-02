import SyntaxHighlighter from 'react-syntax-highlighter';
import { vs2015 } from 'react-syntax-highlighter/dist/esm/styles/hljs';
import { useAppDispatch, useAppSelector } from "../store/hooks";
import { selectBreakpoints, selectSourceCode, selectSourceCodeFilePath } from "../store/selectors";
import { setBreakpoint } from '../store/store';
import './CodeView.css';

const CodeView = () => {
  const dispatch = useAppDispatch();
  const sourceCode = useAppSelector(selectSourceCode);
  const sourceCodeFilePath = useAppSelector(selectSourceCodeFilePath);

  // FIXME: It would not work if path formats are different. Add validation for input path 
  const breakpoints = useAppSelector(selectBreakpoints).filter(breakpoint => breakpoint.source == sourceCodeFilePath);

  let highlightedLines = breakpoints.map(breakpoint => breakpoint.line_number);
  const placeBreakpoint = (lineNumber: number) => dispatch(setBreakpoint("break", ""))

  const sourceCodeView = (
    <SyntaxHighlighter
      language="csharp"
      wrapLines={true}
      showLineNumbers={true}
      style={vs2015}
      lineProps={(lineNumber) => {
        return {
          style: highlightedLines.includes(lineNumber)
            ? {
              display: "block",
              backgroundColor: "rgb(248 113 113)",
              borderRadius: "4px"
            }
            : {},
          onClick: () => placeBreakpoint(lineNumber)
        };
      }}
      className={"syntax-highlighter"}>
      {sourceCode!}
    </SyntaxHighlighter>);

  const placeholder = (
    <div className="flex justify-center text-gray-300 p-2">
      <span>
        Load source code
      </span>
    </div>);

  return sourceCode
    ? sourceCodeView
    : placeholder;
};

export default CodeView;