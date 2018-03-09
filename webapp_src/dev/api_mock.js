const http = require('http');
const api = require('./config').api;
const url = require('url');

class SimpleServer {
    constructor() {
        this.routes = {
            404: () => '404 Page not found.'
        };
    }

    start() {
        http.createServer((req, res) => {

            // Set CORS headers
            res.setHeader('Access-Control-Allow-Origin', '*');
            res.setHeader('Access-Control-Request-Method', '*');
            res.setHeader('Access-Control-Allow-Methods', 'OPTIONS, GET');
            res.setHeader('Access-Control-Allow-Headers', '*');

            const urlParts = url.parse(req.url, true);

            let cb = this.routes[urlParts.pathname];
            if (!cb) {
              res.writeHead(404, {'Content-Type': 'text/plain'})
              cb = this.routes[404];
            }

            res.end(cb({
              req, url: urlParts, res
            }, res));

        }).listen(api.port);
    }

    get(pattern, callback) {
        this.routes[pattern] = callback;
    }
}

const server = new SimpleServer();

server.get('/classifiers', ({ req, res }) => {
    res.writeHead(200, {'Content-Type': 'text/json'});
    return `{
        "classifiers": [
            {
                "id": "baseline",
                "title": "DCASE 2016 Baseline System",
                "description": "No description provided."
            }
        ]
    }`;
});

server.get('/classify/baseline/w664', ({ req, res }) => {
    res.writeHead(200, {'Content-Type': 'text/plan'});
    return `5.940996	6.282603	(object) snapping
10.159102	10.693792	object impact
12.127057	12.490943	object impact
14.956456	15.364900	object impact
17.837839	18.261135	(object) snapping
18.751267	19.189416	object impact
23.310981	23.697146	object impact
28.761845	29.185141	(object) snapping
31.932851	32.430410	(object) snapping
33.447805	33.819117	(object) snapping`;
});

server.start();
