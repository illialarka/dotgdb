import Button from '../components/Button';
import FileInput, { EmptyOnChange } from '../components/FileInput';
import Link from '../components/Link';
import { selectExecutable, setExecutable } from '../reducers/ExecutableReducer';
import { useAppDispatch, useAppSelector } from '../reducers/hooks';
import classes from './Load.module.css';

function Load() {
    const executable = useAppSelector(selectExecutable);
    const dispatch = useAppDispatch();

    const fileInputView = (
        <FileInput onChange={(path) => dispatch(setExecutable(path))}></FileInput>
    );

    const selectedExecutableView = (
        <>
            <span>
                {executable.path}
            </span>
            <Button disabled={false} type='primary' styled='default' onClick={() => {}} label="Run"></Button>
        </>
    );

    const preview = executable.path && executable.path !== ''
        ? selectedExecutableView
        : fileInputView;

    return (
        <div className={classes.container}>
            {preview}
            <Link href='empty' label='Need help?' target='_blank'></Link>
            <span>v0.1.0</span>
        </div>
    );
}

export default Load;