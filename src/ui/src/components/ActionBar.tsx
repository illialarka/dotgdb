import { BiRectangle, BiRightArrow } from "react-icons/bi";
import { selectExecutable } from "../reducers/ExecutableReducer";
import { useAppDispatch, useAppSelector } from "../reducers/hooks";
import classes from './ActionBar.module.css';

export function ActionBar() {
    const executable = useAppSelector(selectExecutable);
    const dispatch = useAppDispatch();

    return (
        <div className={classes.container} data-state={executable.active ? "active" : "disabled"}>
            <div className={classes.continue}>
                <BiRightArrow></BiRightArrow>
            </div>
            <div className={classes.stop}>
                <BiRectangle></BiRectangle>
            </div>
        </div>
    );
}