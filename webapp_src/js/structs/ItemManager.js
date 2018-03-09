import PureClass from './PureClass';

export default class ItemManager extends PureClass {

    constructor({inside}) {
        super();
        this.inside = (inside && inside.length) ? inside : [];
    }

    remove(system) {
        let index = this.inside.indexOf(system);
        let inside = this.inside.slice();
        inside.splice(index, 1);
        return this.update({ inside });
    }

    add(system) {
        return this.update({
            inside: this.inside.concat([system])
        });
    }

    map(fn) {
        const newinside = this.inside.map(fn);
        const new1 = this.update({ inside: newinside });
        return new1;
    }

    indexOf(item) {
        return this.inside.indexOf(item);
    }

    get(index) {
        return this.inside[index];
    }

    get length() {
      return this.asArray.length;
    }

    get asArray() {
        return this.inside;
    }
}
