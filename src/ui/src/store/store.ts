import {
  Action,
  configureStore,
  createSlice,
  PayloadAction,
  ThunkAction } from '@reduxjs/toolkit';
import { Breakpoint } from '../models/breakpoints.model';
import ConnectionService from '../services/ConnectionServie';

export interface DebugState {
  sourceCodeFilePath?: string;
  sourceCode: string | null;
  logs: string[];
  output: string[];
  breakpoints: Breakpoint[];
};

const initialState: DebugState = {
  sourceCodeFilePath: undefined,
  sourceCode: null,
  logs: [],
  output: [],
  breakpoints: [] 
};

const connectionService = new ConnectionService("http://127.0.0.1:5000");
connectionService.initialize(
  {
    content_event: (response) => {
      response.ok 
        ? store.dispatch(setSourceCode(response.content))
        : store.dispatch(appendLog(response.message));
    },
    std_output: (response) => store.dispatch(appendOutput(response.message)),
    breakpoints: (response) => store.dispatch(appendBreakpoint(response.content))
  }
);

export const debugSlice = createSlice({
  name: 'debug',
  initialState,
  reducers: {
    // source code
    setSourceCodeFilePath: (state, action: PayloadAction<string>) => {
      state.sourceCodeFilePath = action.payload;
    },
    setSourceCode: (state, action: PayloadAction<string>) => {
      state.sourceCode = action.payload;
    },
    appendLog: (state, action: PayloadAction<string>) => {
      state.logs = [...state.logs, action.payload]; 
    },
    appendOutput: (state, action: PayloadAction<string>) => {
      state.output = [...state.output, action.payload];
    },

    // breakpoints
    appendBreakpoint: (state, action: PayloadAction<Breakpoint[]>) => {
      state.breakpoints = [...action.payload]
    }
  }
});

export const {
  setSourceCodeFilePath,
  setSourceCode,
  appendLog,
  appendOutput,
  appendBreakpoint
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

export const runDebugger =
  (filePath: string): AppThunk => 
  (dispatch, getState) => {
    connectionService.send("command", { path: filePath })
  };

export const setBreakpoint =
  (command: string, args: string): AppThunk => 
  (dispatch, getState) => {
    connectionService.send("command", { command: command, arguments: args })
  };

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;
