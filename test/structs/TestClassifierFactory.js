// Test setup
import chai from 'chai';
import chaiAsPromised from 'chai-as-promised';
import sinon from 'sinon';

import ClassifierFactory from '../../webapp_src/js/structs/ClassifierFactory';

chai.use(chaiAsPromised);
chai.should();

const p = () => {
    return new Promise((resolve, reject) => {
        resolve([1,3,4]);
    });
}

function Api() {}
Api.prototype.fetch = function() { console.log('REALLY SLOW'); };
function Cache() {}
Cache.prototype.fetch = function() { console.log('REALLY SLOW'); };

describe('ClassifierFactory', function() {

    describe('#all', function() {
    
        const api = sinon.mock(Api, 'fetch', () => {
            return Promise.resolve([ '{"foo": "bar"}' ]);
        });

        const cache = sinon.mock(Cache, 'hit');

        const factory = new ClassifierFactory({api: new Api()});

        it('Should get all the classifiers', function() {
            return factory.all().should.eventually.have.length(1);
        });

        it('Should cache the result', function () {
            return factory.all().then(result => {
                return factory.all().should
                        .eventually.equal(result);
            });
        });
    });

    // it('respond with matching records', function() {
    //   return p().should.eventually.have.length(3);
    // });
  });
