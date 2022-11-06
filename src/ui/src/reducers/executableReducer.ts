import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { RootState } from '../store';

export interface ExecutableState {
  path?: string;
}

const initialState: ExecutableState = {
  path: undefined
};

export const executableSlice = createSlice({
  name: 'executable',
  initialState,

  reducers: {
    setExecutable: (state, action: PayloadAction<string>) => {
      state.path = action.payload;
    },

    reset: (state) => {
      state.path = undefined;
    }
  }
});

export const { reset, setExecutable } = executableSlice.actions;

export const selectExecutable = (state: RootState) => state.executable;

export default executableSlice.reducer;
