import {
  Action,
  configureStore,
  createSlice,
  PayloadAction,
  ThunkAction } from '@reduxjs/toolkit';
import ConnectionService from '../services/ConnectionServie';
import { selectFilePath } from './selectors';

export interface DebugState {
  binaryPath: string | null;
  filePath: string | null;
  sourceCode: string | null;
};

const initialState: DebugState = {
  binaryPath: null,
  filePath: null,
  sourceCode: null
};

const connectionService = new ConnectionService("http://127.0.0.1:5000");
connectionService.initialize(
  {
    content_event: (response) => store.dispatch(setSourceCode(response.content))
  }
);

export const debugSlice = createSlice({
  name: 'debug',
  initialState,
  reducers: {
    // file
    setFilePath: (state, action: PayloadAction<string>) => {
      state.filePath = action.payload;
    },
    clearFilePath: (state) => {
      state.filePath = null;
    },

    // binary 
    setBinaryPath: (state, action: PayloadAction<string>) => {
      state.binaryPath = action.payload;
    },
    clearBinaryPath: (state) => {
      state.binaryPath = null;
    },

    // source code
    setSourceCode: (state, action: PayloadAction<string>) => {
      console.log(action)
      state.sourceCode = action.payload;
    }
  }
});

export const {
  setBinaryPath,
  setFilePath,
  clearBinaryPath,
  clearFilePath,
  setSourceCode
} = debugSlice.actions;

export default debugSlice.reducer;

export const store = configureStore({
  reducer: {
    debug: debugSlice.reducer
  }
});

export const loadFileContent =
  (filePath: string): AppThunk =>
    (dispatch, getState) => {
      connectionService.send("content", { path: filePath })
    };

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;