import { useLocation } from "react-router-dom";

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

let globalCache = {};

function assignState(originalState, updateFields) {
  let newState = Object.assign({}, originalState);
  Object.assign(newState, updateFields);
  return newState;
}


export default { useQuery, globalCache, assignState };