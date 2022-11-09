import { io } from 'socket.io-client'; 
import { useState } from 'react';
import Button from '../components/Button';
import FileInput from '../components/FileInput';
import Link from '../components/Link';
import { selectExecutable, setExecutable } from '../reducers/ExecutableReducer';
import { useAppDispatch, useAppSelector } from '../reducers/hooks';
import classes from './Load.module.css';

const allowedExtensions = [".dll", ".exe"]

function Load() {
    const executable = useAppSelector(selectExecutable);
    const dispatch = useAppDispatch();
    const [errors, setErrors] = useState([]);

    const fileSelected = (path: string) => {

        if (!allowedExtensions.some(ext => path.endsWith(ext))) {
            return;
        }

        const socket = io("http://localhost:5000", { autoConnect: false });

        socket.on("connect", () => {
            console.log("Connection has been established");
        });


        socket.on("disconnect", () => {
            console.log("I am done!")
        });

        dispatch(setExecutable(path));
    };

    const fileInputView = (
        <FileInput onChange={(path) => fileSelected(path)} supportedTypes={allowedExtensions}></FileInput>
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
