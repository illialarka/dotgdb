import classes from './FileInput.module.css';
import { BiFolderOpen } from "react-icons/bi";

function FileInput() {
  return (
    <label className= {classes.control}>
      <span>
        Open executable for debugging
      </span>
      <div data-type="icon">
        <BiFolderOpen/>
      </div>
      <input type="file" className='hide'/>
    </label>
  );
}

export default FileInput;