import axios from "axios"

let root_url = "http://kruskal.cg-y.com:5001/"

if (process.env.NODE_ENV === "production") {
    // console.log("use end point /")
    root_url = window.location.origin + "/"
}

function getHttp() {

    return axios.create({
        baseURL: root_url,
        timeout: parseInt(60 * 1000), //60s
        Accept: 'application/json',
        'Content-Type': 'application/json',
        headers: {"my-auth-header": "APTX4869!"}
    });
}

export default {
    getHttp, root_url
}