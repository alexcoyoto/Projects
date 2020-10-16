let Welcome = {
    render: async () => {
        return `
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="utf-8">
          <title>Welcome</title>
        </head>
        <body>
          <div id="message" class="welcomePageContainer">
            <h1 id='titleHead'>Рады бачыць вас на нашым сайце!</h1>
            <p class="welcomeText">Mplayer - гэта сайт, на якім Вы можаце абсалютна задарма слухаць, дадаваць у абранае і нават спампоўваць музыку!
            Перайдзіце па ўкладцы ў левым верхнім куце, каб трапіць на асноўную старонку. Як толькі вы паслухаеце трэк ці дадасце
             яго ў абранае, ён з'явіцца ў Вашым кабінеце (правы верхні кут).</p>
             <h2>Прыемнага праслухоўвання!</h2>
             <img class="welcomeLogo" src="images/logo.png" alt="mainLogo" />
          </div>
        </body>
      </html>
        `
    },

    afterRender: async () => {
        //if(auth.currentUser.email)
            //document.querySelector("#titleHead").innerHTML = `${auth.currentUser.email}, рады бачыць вас на нашым сайце!`;
    }
};

export default Welcome;