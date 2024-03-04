const logger = (req, res, next) => {
  // This is a middleware that logs all incoming requests.
  // It logs:
  //  - the response status code
  //  - the request method
  //  - the request URL
  //  - the time (in milliseconds) it took for the server to respond

  const t = Date.now();
  next();
  console.log(
    `[${res.statusCode}] ${req.method} ${req.url} (${Date.now() - t}ms)`
  );
};

export default logger;
