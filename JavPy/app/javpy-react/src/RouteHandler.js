import utils from './utils';


export default (prevProps, thisProps) => {
  if (thisProps.history.action === "POP") {
    if (thisProps.location.pathname === "/new") {
      utils.globalCache.new.recover = true;
    } else if (thisProps.location.pathname === "/search/actress") {
      utils.globalCache.searchActress.recover = true;
    }
  }
}