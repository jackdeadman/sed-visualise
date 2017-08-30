import PureClass from './PureClass';

export default class TextFileReader extends PureClass {

    constructor({ encoding='UTF-8' }) {
        this.encoding = encoding;
    }

    async read() {
        let reader = new FileReader();
        reader.readAsText(file, this.encoding);

        return new Promise((resolve, reject) => {
            reader.onload = e => resolve(e.target.result);
            reader.onerror = reject;
        });
    }

}