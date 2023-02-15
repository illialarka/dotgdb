import { RootState } from "./store";

export const selectSourceCode = (state: RootState) => state.debug.sourceCode;

export const selectLogs = (state: RootState) => state.debug.logs;