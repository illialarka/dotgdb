import { DebugState } from "./store";

export const selectBinaryPath = (state: DebugState) => state.binaryPath;
export const selectFilePath = (state: DebugState) => state.filePath;