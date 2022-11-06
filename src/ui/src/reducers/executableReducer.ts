import { createAsyncThunk, createSlice, PayloadAction } from '@reduxjs/toolkit';
import { RootState, AppThunk } from '../store';
import { fetchCount } from './counterAPI';

export interface ExecutableState {
  path?: string;
}

const initialState: ExecutableState = {
  path: undefined
};

export const executableSlice = createSlice({
  name: 'executable',
  initialState,
  // The `reducers` field lets us define reducers and generate associated actions
  reducers: {
/*
    increment: (state) => {
      // Redux Toolkit allows us to write "mutating" logic in reducers. It
      // doesn't actually mutate the state because it uses the Immer library,
      // which detects changes to a "draft state" and produces a brand new
      // immutable state based off those changes
      state.value += 1;
    },
    decrement: (state) => {
      state.value -= 1;
    },
    // Use the PayloadAction type to declare the contents of `action.payload`
    incrementByAmount: (state, action: PayloadAction<number>) => {
      state.value += action.payload;
    },
  },
  */
  }
});

export const {  } = executableSlice.actions;

export const selectExecutable = (state: RootState) => state.executable;

export default executableSlice.reducer;
