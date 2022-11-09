import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { RootState } from '../store';

export interface ExecutableState {
  path?: string;
  active: boolean;
}

const initialState: ExecutableState = {
  path: undefined,
  active: false 
};

export const executableSlice = createSlice({
  name: 'executable',
  initialState,

  reducers: {
    setExecutable: (state, action: PayloadAction<string>) => {
      state.path = action.payload;
    },

    setActive: (state, action: PayloadAction<boolean>) => {
      state.active = action.payload;
    },

    reset: (state) => {
      state.path = undefined;
      state.active = false;
    }
  }
});

export const { reset, setExecutable, setActive } = executableSlice.actions;

export const selectExecutable = (state: RootState) => state.executable;

export default executableSlice.reducer;
