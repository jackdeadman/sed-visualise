import { fetchJSON } from './utils/utils';
import url from 'url';

export default class Api {

    static instance = null;

    constructor(remote) {
        this.remote = remote;
    }

    _urlFrom(urlPath) {
        return url.resolve(this.remote, urlPath);
    }

    async fetch(str) {
        const url = this._urlFrom(str);
        console.log(url);
        return fetchJSON(url);
    }

}
