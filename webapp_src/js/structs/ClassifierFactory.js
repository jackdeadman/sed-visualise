import PureClass from './PureClass';
import { fetchJSON } from '../utils/utils';
import Classifier from './Classifier';
import ItemManager from './ItemManager';

export default class ClassifierFactory extends PureClass {

    constructor({ api }) {
        super();
        this.api = api;
        // console.log(api);
        this.classifiers = null;
        this.loading = false;
        this.listeners = [];
    }

    registerOnLoadListener(fn) {
        this.listeners.push(fn);
    }

    waitForLoad() {
        return new Promise((resolve, reject) => {
            this.registerOnLoadListener(resolve);
        });
    }

    async all() {
        // if (this.loading) {
        //     return this.waitForLoad();
        // }

        if (this.classifiers) {
            return this.classifiers;
        }

        this.loading = true;

        // const manager = new ItemManager({
        //     inside: (await fetchJSON(this.remote)).classifiers
        // });

        const inside = await this.api.fetch('classifiers/all');
        const manager = new ItemManager({ inside });

        const classifiers = manager.map(attrs => new Classifier(attrs));
        
        this.loading = false;
        this.classifiers = classifiers;

        this.listeners.forEach(listener => listener(classifiers))

        return classifiers;
    }

    clearCache() {
        this.classifiers = null;
    }
}
