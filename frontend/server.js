const { createServer } = require("https");
const { parse } = require("url");
const fs = require("fs");
const next = require("next");

const app = next({ dev: true });
const handle = app.getRequestHandler();

const httpsOptions = {
  key: fs.readFileSync("../conf/key.key"), // Path to your private key
  cert: fs.readFileSync("../conf/crt.crt"),
};

app.prepare().then(() => {
  createServer(httpsOptions, (req, res) => {
    const parsedUrl = parse(req.url, true);
    handle(req, res, parsedUrl);
  }).listen(3000, () => {
    console.log("> Server running on https://localhost:3000");
  });
});
