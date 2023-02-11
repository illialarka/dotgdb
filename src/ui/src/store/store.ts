import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface DebugState {
    binaryPath: string | null;
    filePath: string | null;
};

const initialState: DebugState = {
    binaryPath: null,
    filePath: null
};

export const debugSlice = createSlice({
    name: 'debug',
    initialState,
    reducers: {
        setBinaryPath: (state, action: PayloadAction<string>) => {
            state.binaryPath = action.payload;
        },
        setFilePath: (state, action: PayloadAction<string>) => {
            state.filePath = action.payload;
        },
        clearFilePath: (state) => {
            state.filePath = null;
        },
        clearBinaryPath: (state) => {
            state.binaryPath = null;
        }
    }
}); 

export const {
    setBinaryPath,
    setFilePath,
    clearBinaryPath,
    clearFilePath
} = debugSlice.actions;

export default debugSlice.reducer;