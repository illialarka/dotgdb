import './FileInput.css';
import { BiFolderOpen } from "react-icons/bi";

export interface FileInputProps {
  onClick?: () => void;
}

function FileInput(props: FileInputProps) {
  return (
    <label className="file-input">
      <span>
        Selec file to open and debug
      </span>
      <div data-type="icon">
        <BiFolderOpen/>
      </div>
      <input type="file" className='hide'/>
    </label>
  );
}

export default FileInput;