import {
  Action,
  configureStore,
  createSlice,
  PayloadAction,
  ThunkAction } from '@reduxjs/toolkit';
import ConnectionService from '../services/ConnectionServie';

export interface DebugState {
  sourceCode: string | null;
  logs: string[];
};

const initialState: DebugState = {
  sourceCode: null,
  logs: []
};

const connectionService = new ConnectionService("http://127.0.0.1:5000");
connectionService.initialize(
  {
    content_event: (response) => {
      response.ok 
        ? store.dispatch(setSourceCode(response.content))
        : store.dispatch(appendLog(response.message));
    }
  }
);

export const debugSlice = createSlice({
  name: 'debug',
  initialState,
  reducers: {
    // source code
    setSourceCode: (state, action: PayloadAction<string>) => {
      state.sourceCode = action.payload;
    },
    appendLog: (state, action: PayloadAction<string>) => {
      console.log(action)
      state.logs = [...state.logs, action.payload]; 
    }
  }
});

export const {
  setSourceCode,
  appendLog
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