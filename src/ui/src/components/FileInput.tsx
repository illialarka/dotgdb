import classes from './FileInput.module.css';
import { BiFolderOpen } from "react-icons/bi";

export interface FileInputProps {
  onChange: (_: string) => void;
  supportedTypes: string[];
}

function FileInput(props: FileInputProps) {
  let { onChange, supportedTypes } = props;

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const path = event.target.value;
    console.log(event)

    if (path !== "") {
      onChange(path);
    }
  }

  return (
    <label className= {classes.control}>
      <span>
        Open executable for debugging
      </span>
      <input placeholder='Enter path to binary' type="text" onChange={handleFileChange} accept={`${supportedTypes.map(x => x + ' ')}`}/>
    </label>
  );
}

export default FileInput;
