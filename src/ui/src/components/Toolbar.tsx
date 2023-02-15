import { useEffect, useState } from "react";
import Button from "./Button"
import Dropdown from "./Dropdown";
import { useAppDispatch } from "../store/hooks";
import { loadFileContent } from "../store/store";
import { useSearchParams } from "react-router-dom";

const SOURCE_CODE_PATH_PARAM = "sourceCodePath";
const EXECUTABLE_PATH_PARAM = "executablePath";

const fileDropdownItems = [
  { label: 'Open executable', callback: () => { } },
  { label: 'Open source file', callback: () => { } },
  { label: 'Clear All', callback: () => { } }
];

const helpDropdownItems = [
  { label: 'GitHub Repo', callback: () => { window.open("https://github.com/illialarka/dotgdb", "_blank") } },
  { label: 'Docs', callback: () => { } }
];

const PathView = (props: {
   placeholder: string | undefined,
   value: string | undefined,
   onChange: (_: string) => void
  }) => {
  const { placeholder, value, onChange } = props;

  return (
    <input
      type="text"
      className="w-full bg-gray-700 truncate py-2 px-3 text-sm font-medium leading-4 darker border border-gray-600"
      value={value || ""}
      placeholder={placeholder}
      onChange={(event) => onChange(event.target.value)}/>
  );
};

const runIcon = (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6">
    <path fillRule="evenodd" d="M4.5 5.653c0-1.426 1.529-2.33 2.779-1.643l11.54 6.348c1.295.712 1.295 2.573 0 3.285L7.28 19.991c-1.25.687-2.779-.217-2.779-1.643V5.653z" clipRule="evenodd" />
  </svg>
);

const stopIcon = (
  <svg  xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6">
    <path fillRule="evenodd" d="M4.5 7.5a3 3 0 013-3h9a3 3 0 013 3v9a3 3 0 01-3 3h-9a3 3 0 01-3-3v-9z" clipRule="evenodd" />
  </svg>
); 

const stepInIcon = (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6">
    <path fillRule="evenodd" d="M12 3.75a.75.75 0 01.75.75v13.19l5.47-5.47a.75.75 0 111.06 1.06l-6.75 6.75a.75.75 0 01-1.06 0l-6.75-6.75a.75.75 0 111.06-1.06l5.47 5.47V4.5a.75.75 0 01.75-.75z" clipRule="evenodd" />
  </svg>
);

const stepOverIcon = (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6">
    <path fillRule="evenodd" d="M15 3.75A5.25 5.25 0 009.75 9v10.19l4.72-4.72a.75.75 0 111.06 1.06l-6 6a.75.75 0 01-1.06 0l-6-6a.75.75 0 111.06-1.06l4.72 4.72V9a6.75 6.75 0 0113.5 0v3a.75.75 0 01-1.5 0V9c0-2.9-2.35-5.25-5.25-5.25z" clipRule="evenodd" />
  </svg>
);

const Toolbar = () => {
  const dispatch = useAppDispatch();
  const pathRegex = /^(?:[a-z]:)?[\/\\]{0,2}(?:[.\/\\ ](?![.\/\\\n])|[^<>:"|?*.\n])+$/
  const [executablePath, setExecutablePath] = useState<string>();
  const [sourceCodePath, setSourceCodePath] = useState<string>();

  // params
  const [searchParams, setSearchParams] = useSearchParams();

  useEffect(() => {
    if (executablePath && pathRegex.test(executablePath)) {
      searchParams.set(EXECUTABLE_PATH_PARAM, executablePath)
    }

    if (sourceCodePath && pathRegex.test(sourceCodePath)) {
      searchParams.set(SOURCE_CODE_PATH_PARAM, sourceCodePath)
    }
    setSearchParams(searchParams)
  },
  [ executablePath, sourceCodePath ]);

  useEffect(
    () => {
      const sourceCodePathValue = searchParams.get(SOURCE_CODE_PATH_PARAM); 
      const executablePathValue = searchParams.get(EXECUTABLE_PATH_PARAM);

      if (sourceCodePathValue && pathRegex.test(sourceCodePathValue)) {
        setSourceCodePath(sourceCodePathValue);
      }

      if (executablePathValue && pathRegex.test(executablePathValue)) {
        setExecutablePath(executablePathValue);
      }
    },
    [searchParams]);
  
  return (
    <div className="flex flex-col space-y-2 text-white">
      <div className="flex felx-row text-sm justify-between">
        <div>
          <Dropdown label="File" items={fileDropdownItems}/>
          <Dropdown label="Help" items={helpDropdownItems}/>
        </div>
        <div>
          <span className="text-xs text-gray-500">
            {executablePath}
          </span>
        </div>
        <div>
        </div>
      </div>
      <div className="grid grid-cols-3 space-x-2">
        <div className="flex flex-row space-x-2 border-r pr-2 border-gray-600">
          <PathView
            placeholder="Select executable"
            value={executablePath}
            onChange={setExecutablePath}/>
          <Button label="Binary"/>
        </div>	
        <div className="flex flex-row space-x-2">
          <PathView
            placeholder="Select file to place breakpoints"
            value={sourceCodePath}
            onChange={setSourceCodePath}/>
          <Button
            label="File"
            disabled={!pathRegex.test(sourceCodePath ?? '')}
            callback={() => dispatch(loadFileContent(sourceCodePath!))}/>
        </div>	
        <div className="flex flex-row space-x-2 justify-end">
          <Button icon={runIcon}/>
          <Button icon={stopIcon}/>
          <Button icon={stepInIcon}/>
          <Button icon={stepOverIcon}/>
        </div>
      </div>
    </div>
  )
};

export default Toolbar; 
