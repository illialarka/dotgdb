import { runExecutable } from '../services/ExecutableService';
import Button from '../components/Button';
import FileInput from '../components/FileInput';
import Link from '../components/Link';
import { selectExecutable, setExecutable, setActive } from '../reducers/ExecutableReducer';
import { useAppDispatch, useAppSelector } from '../reducers/hooks';
import classes from './Load.module.css';

const allowedExtensions = [".dll", ".exe"]

function Load() {
    const executable = useAppSelector(selectExecutable);
    const dispatch = useAppDispatch();

    const fileSelected = (path: string) => {
        if (!allowedExtensions.some(ext => path.endsWith(ext))) {
            return;
        }

        dispatch(setExecutable(path));
    };

    const onRun = () => {
        if (executable.path) {
            runExecutable(executable.path).then(response => {
                if (response.status == 200) {
                    dispatch(setActive(true));
                }
            })
        }
    }

    return (
        <div className={classes.container}>
            <FileInput onChange={(path) => fileSelected(path)} supportedTypes={allowedExtensions}></FileInput>
            <Button
                disabled={!executable.path}
                type='primary'
                styled='default'
                onClick={onRun}
                label="Run"></Button>
            <Link href='empty' label='Need help?' target='_blank'></Link>
            <span>v0.1.0</span>
        </div>
    );
}

export default Load;
