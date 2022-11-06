import { configureStore, ThunkAction, Action } from '@reduxjs/toolkit';
import executableReducer from './reducers/executableReducer';

export const store = configureStore({
  reducer: {
    executable: executableReducer,
  },
});

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;
