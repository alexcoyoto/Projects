import Header from './views/header.js';
import Footer from './views/footer.js';

import Main from './views/main.js';
import Registration from './views/registration.js';
import Autorization from './views/autorization.js';
import User from './views/user.js';
import Error404 from './views/error404.js';
import Add from './views/add.js';
import Welcome from './views/welcome.js';

import Utils from './utils.js';

const routes = {
    '/main': Main,
    '/autorization': Autorization,
    '/registration': Registration,
    '/user': User,
    '/add': Add,
    '/welcome': Welcome
};

var firstTime = true;

const router = async () => {

    const all = [];
    let request = Utils.parseRequestURL();
    let parsedURL = (request.resource ? '/' + request.resource : '/') + 
        (request.id ? '/:id' : '') + (request.verb ? '/' + request.verb : '');

    const header = null || document.querySelector('header');
    const content = null || document.querySelector('main');
    const footer = null || document.querySelector('footer');

    let page = routes[parsedURL] ? routes[parsedURL] : Error404;

    content.innerHTML = await page.render(); 

    await page.afterRender();

    // Render the header
    header.innerHTML = await Header.render([]);
    await Header.afterRender();
    // Render the footer
    if(firstTime){
        footer.innerHTML = await Footer.render([]);
        await Footer.afterRender();
        firstTime = false;
    }


}

// Listen on hash change:
window.addEventListener('hashchange', router);

// Start:
window.addEventListener('load', () => {
    auth.onAuthStateChanged(firebaseUser => {
            //window.location.hash = '/main';
        router();
    });
});