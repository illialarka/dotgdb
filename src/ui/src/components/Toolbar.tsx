import Button from "./Button"
import { useAppDispatch, useAppSelector } from "../store/hooks";
import { selectBinaryPath, selectFilePath } from "../store/selectors";

const PathView = () => {
  return (
    <div
      className="w-full truncate rounded-sm border border-gray-300 bg-gray-100 py-1 px-2 text-xs font-medium leading-4 text-gray-700 shadow-inner"> 
      /use/path
    </div>
  );
};

const Toolbar = () => {
  const binaryPath = useAppSelector(selectBinaryPath);
  const filePath = useAppSelector(selectFilePath);
  const dispatch = useAppDispatch();

  return (
    <div className="flex flex-col space-y-2 p-2">
      <div className="flex felx-row space-x-3 text-sm">
        <div>
          File
        </div>
        <div>
          View
        </div>
      </div>
      <div className="grid grid-cols-3 space-x-2">
        <div className="flex flex-row space-x-2 border-r-2 pr-2">
          <PathView></PathView>
          <Button label="Binary"></Button>
        </div>	
        <div className="flex flex-row space-x-2 border-r-2 pr-2">
          <PathView></PathView>
          <Button label="File"></Button>
        </div>	
        <div className="flex flex-row space-x-2">
          <Button label="Run"></Button>
          <Button label="Stop"></Button>
          <Button label="Step Over"></Button>
          <Button label="Step In"></Button>
        </div>
      </div>
    </div>
  )
};

export default Toolbar; 
