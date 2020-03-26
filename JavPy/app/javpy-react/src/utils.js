import { useLocation } from "react-router-dom";

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

let globalCache = {};


export default { useQuery, globalCache };