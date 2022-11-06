import FileInput from '../components/FileInput';
import Link from '../components/Link';
import classes from './Load.module.css';

function Load() {
    return (
        <div className={classes.container}>
            <FileInput></FileInput>
            <Link href='empty' label='Need help?' target='_blank'></Link>
            <span>v0.1.0</span>
        </div>
    );
}

export default Load;