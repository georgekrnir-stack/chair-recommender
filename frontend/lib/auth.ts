"use client";

import { createContext, useContext } from "react";

export interface AuthState {
  isAdmin: boolean;
  loading: boolean;
}

export const AuthContext = createContext<AuthState>({ isAdmin: false, loading: true });

export function useAuth() {
  return useContext(AuthContext);
}
