let Error404 = {
    render: async () => {
        return `
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="utf-8">
          <title>Page Not Found</title>
        </head>
        <body>
          <div id="message">
            <h2>404</h2>
            <h1>Page Not Found</h1>
          </div>
        </body>
      </html>
        `
    },

    afterRender: async () => {}
};

export default Error404;