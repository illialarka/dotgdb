import { Action, configureStore, createSlice, PayloadAction, ThunkAction } from '@reduxjs/toolkit';

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

export const store = configureStore({
  reducer: {
    debug: debugSlice.reducer 
  }
});

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;