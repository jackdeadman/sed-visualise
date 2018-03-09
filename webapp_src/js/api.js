import { fetchJSON, fetch } from './utils/utils';
import url from 'url';
import { api } from '../dev/config';

export default class Api {

    get remote() {
        console.log(api);
        return `${api.basename}:${api.port}`;
    }

    _urlFrom(urlPath) {
        return `${this.remote}/${urlPath}`;
    }

    async classify(classifier, code) {
      return this.fetch(`classify/${classifier}/${code}`);
    }

    async classifiers() {
      return this.fetchJSON('classifiers');
    }

    async fetchJSON(str) {
        const url = this._urlFrom(str);
        return fetchJSON(url);
    }

    async fetch(str) {
        const url = this._urlFrom(str);
        return fetch(url);
    }

}
