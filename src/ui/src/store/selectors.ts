import { RootState } from "./store";

export const selectSourceCode = (state: RootState) => state.debug.sourceCode;