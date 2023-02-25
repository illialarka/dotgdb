import { RootState } from "./store";

export const selectSourceCode = (state: RootState) => state.debug.sourceCode;

export const selectLogs = (state: RootState) => state.debug.logs;

export const selectOutput = (state: RootState) => state.debug.output;

export const selectBreakpoints = (state: RootState) => state.debug.breakpoints;