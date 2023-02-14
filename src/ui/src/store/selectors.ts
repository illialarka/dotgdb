import { RootState } from "./store";

export const selectBinaryPath = (state: RootState) => state.debug.binaryPath;
export const selectFilePath = (state: RootState) => state.debug.filePath;