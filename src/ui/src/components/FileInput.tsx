import classes from './FileInput.module.css';
import { BiFolderOpen } from "react-icons/bi";

export function EmptyOnChange(_: any) {
  // do nothing
}

export interface FileInputProps {
  onChange: (_: string) => void;
}

function FileInput(props: FileInputProps) {
  let { onChange } = props;

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const path = event.target.value;

    if (path !== "") {
      onChange(path);
    }
  }

  return (
    <label className= {classes.control}>
      <span>
        Open executable for debugging
      </span>
      <div data-type="icon">
        <BiFolderOpen/>
      </div>
      <input type="file" className='hide' onChange={handleFileChange}/>
    </label>
  );
}

export default FileInput;