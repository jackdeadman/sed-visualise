import PureClass from './PureClass';
import { fetch } from '../utils/utils';

export default class Classifier extends PureClass {

    constructor({ id, title, description, remote }) {
        super();
        this.id = id;
        this.title = title;
        this.description = description;
    }

    async labelsFor(audioFileCode) {
        return fetch(audioFileCode);
    }

}
