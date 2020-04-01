import React from "react"
import utils from "../../utils";


export default () => {
  const query = utils.useQuery();

  return (
    <iframe title="video" src={query.get("video_url")} style={{ width: "100vw", height: "100vh", margin: 0, padding: 0, border: 0 }} >
      <p>Your browser does not support iframes.</p>
    </iframe>
  )
}